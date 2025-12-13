# Claude Code Best Practices Toolkit - Agent Harness

Long-running agent pattern that prevents context overflow. Each worker runs ONE task, exits, next worker picks up.

---

## Core Pattern

```
┌─────────────┐     ┌─────────────┐     ┌─────────────┐
│  Objective  │────▶│ Initializer │────▶│   Tasks     │
└─────────────┘     │   Agent     │     │  (JSON)     │
                    └─────────────┘     └──────┬──────┘
                                               │
                    ┌─────────────┐             │
                    │   Worker    │◀────────────┘
                    │   Agent     │─────▶ Execute one task
                    └─────────────┘       Update state
                          │               Exit
                          ▼
                    [Next worker picks up next task]
```

---

## Directory Structure

```
.harness/
├── init.py           # Creates tasks from objective
├── work.py           # Executes one task per run
├── run.sh            # Loop wrapper with error handling
├── requirements.txt  # anthropic>=0.39.0
└── state/
    ├── tasks.json    # Task tracking (red → green)
    ├── objective.txt # Original objective
    └── logs/         # Per-task execution logs
```

---

## File: init.py

```python
#!/usr/bin/env python3
"""
Initialize harness with an objective.
Uses Claude to break objective into discrete tasks.
"""

import anthropic
import json
import sys
from pathlib import Path
from datetime import datetime

def init_harness(objective: str, state_dir: str = "state"):
    """Break objective into tasks using Claude."""
    
    client = anthropic.Anthropic()
    state_path = Path(state_dir)
    state_path.mkdir(parents=True, exist_ok=True)
    (state_path / "logs").mkdir(exist_ok=True)
    
    # Save objective
    (state_path / "objective.txt").write_text(objective)
    
    # Ask Claude to decompose
    response = client.messages.create(
        model="claude-sonnet-4-20250514",
        max_tokens=4096,
        messages=[{
            "role": "user",
            "content": f"""Break this objective into discrete, executable tasks.

OBJECTIVE: {objective}

Rules:
- Each task must be completable in one Claude session
- Tasks should be ordered by dependency
- Each task has clear acceptance criteria
- Output valid JSON only

Format:
{{
  "tasks": [
    {{
      "id": "T001",
      "title": "Short title",
      "description": "What to do",
      "acceptance_criteria": [
        {{"criterion": "Specific testable condition", "passes": false}}
      ],
      "dependencies": [],
      "status": "open",
      "result": null,
      "started_at": null,
      "completed_at": null
    }}
  ]
}}"""
        }]
    )
    
    # Parse and save
    content = response.content[0].text
    # Extract JSON from response
    if "```json" in content:
        content = content.split("```json")[1].split("```")[0]
    elif "```" in content:
        content = content.split("```")[1].split("```")[0]
    
    tasks_data = json.loads(content.strip())
    
    # Add metadata
    tasks_data["metadata"] = {
        "objective": objective,
        "created_at": datetime.now().isoformat(),
        "total_tasks": len(tasks_data["tasks"])
    }
    
    (state_path / "tasks.json").write_text(
        json.dumps(tasks_data, indent=2)
    )
    
    print(f"✅ Initialized {len(tasks_data['tasks'])} tasks")
    for task in tasks_data["tasks"]:
        print(f"   {task['id']}: {task['title']}")
    
    return tasks_data


def main():
    if len(sys.argv) < 2:
        print("Usage: python init.py 'Your objective here'")
        print("       python init.py --from-file objective.txt")
        sys.exit(1)
    
    if sys.argv[1] == "--from-file":
        objective = Path(sys.argv[2]).read_text().strip()
    else:
        objective = " ".join(sys.argv[1:])
    
    init_harness(objective)


if __name__ == "__main__":
    main()
```

---

## File: work.py

```python
#!/usr/bin/env python3
"""
Execute one task from the harness.
Reads state, picks next task, executes, updates state, exits.
"""

import anthropic
import json
import sys
import subprocess
from pathlib import Path
from datetime import datetime

def load_state(state_dir: str = "state"):
    """Load current task state."""
    state_path = Path(state_dir)
    tasks_file = state_path / "tasks.json"
    
    if not tasks_file.exists():
        print("❌ No tasks.json found. Run init.py first.")
        sys.exit(1)
    
    return json.loads(tasks_file.read_text())


def save_state(data: dict, state_dir: str = "state"):
    """Save task state."""
    state_path = Path(state_dir)
    (state_path / "tasks.json").write_text(
        json.dumps(data, indent=2)
    )


def get_next_task(data: dict):
    """Get next open task respecting dependencies."""
    completed_ids = {
        t["id"] for t in data["tasks"] 
        if t["status"] == "done"
    }
    
    for task in data["tasks"]:
        if task["status"] == "open":
            # Check dependencies
            deps = set(task.get("dependencies", []))
            if deps.issubset(completed_ids):
                return task
    
    return None


def show_status(data: dict):
    """Display current progress."""
    total = len(data["tasks"])
    done = sum(1 for t in data["tasks"] if t["status"] == "done")
    in_progress = sum(1 for t in data["tasks"] if t["status"] == "in_progress")
    failed = sum(1 for t in data["tasks"] if t["status"] == "failed")
    
    print(f"\n{'='*50}")
    print(f"📊 Progress: {done}/{total} tasks complete")
    print(f"   ✅ Done: {done}")
    print(f"   🔄 In Progress: {in_progress}")
    print(f"   ❌ Failed: {failed}")
    print(f"   ⏳ Remaining: {total - done - in_progress - failed}")
    print(f"{'='*50}\n")
    
    for task in data["tasks"]:
        status_icon = {
            "done": "✅",
            "in_progress": "🔄",
            "failed": "❌",
            "open": "⬚"
        }.get(task["status"], "?")
        
        # Show acceptance criteria status
        criteria = task.get("acceptance_criteria", [])
        passing = sum(1 for c in criteria if c.get("passes", False))
        
        print(f"  {status_icon} {task['id']}: {task['title']} [{passing}/{len(criteria)} criteria]")


def execute_task(task: dict, data: dict, state_dir: str = "state"):
    """Execute a single task using Claude."""
    
    client = anthropic.Anthropic()
    state_path = Path(state_dir)
    
    # Mark in progress
    task["status"] = "in_progress"
    task["started_at"] = datetime.now().isoformat()
    save_state(data, state_dir)
    
    # Build context
    objective = data["metadata"]["objective"]
    completed = [t for t in data["tasks"] if t["status"] == "done"]
    
    context = f"""You are executing a task as part of a larger objective.

OBJECTIVE: {objective}

COMPLETED TASKS:
{json.dumps([{"id": t["id"], "title": t["title"], "result": t["result"]} for t in completed], indent=2)}

CURRENT TASK:
{json.dumps(task, indent=2)}

ACCEPTANCE CRITERIA (all must pass):
{json.dumps(task["acceptance_criteria"], indent=2)}

Instructions:
1. Execute this task completely
2. For each acceptance criterion, verify it passes
3. Report results in this exact JSON format:

{{
  "success": true/false,
  "result_summary": "What was accomplished",
  "files_modified": ["list", "of", "files"],
  "acceptance_results": [
    {{"criterion": "...", "passes": true/false, "evidence": "..."}}
  ],
  "notes": "Any important observations"
}}
"""
    
    print(f"\n🔄 Executing: {task['id']} - {task['title']}")
    print(f"   Criteria to satisfy: {len(task['acceptance_criteria'])}")
    
    response = client.messages.create(
        model="claude-sonnet-4-20250514",
        max_tokens=8192,
        messages=[{"role": "user", "content": context}]
    )
    
    result_text = response.content[0].text
    
    # Log full response
    log_file = state_path / "logs" / f"{task['id']}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"
    log_file.write_text(result_text)
    
    # Parse result
    try:
        if "```json" in result_text:
            result_json = result_text.split("```json")[1].split("```")[0]
        elif "```" in result_text:
            result_json = result_text.split("```")[1].split("```")[0]
        else:
            result_json = result_text
        
        result = json.loads(result_json.strip())
        
        # Update acceptance criteria
        if "acceptance_results" in result:
            for ar in result["acceptance_results"]:
                for tc in task["acceptance_criteria"]:
                    if tc["criterion"] == ar["criterion"]:
                        tc["passes"] = ar["passes"]
                        tc["evidence"] = ar.get("evidence", "")
                        tc["verified_at"] = datetime.now().isoformat()
        
        # Check if all criteria pass
        all_pass = all(c.get("passes", False) for c in task["acceptance_criteria"])
        
        if result.get("success", False) and all_pass:
            task["status"] = "done"
            task["result"] = result.get("result_summary", "Completed")
            print(f"   ✅ Task completed successfully")
        else:
            task["status"] = "failed"
            task["result"] = result.get("result_summary", "Failed")
            failing = [c["criterion"] for c in task["acceptance_criteria"] if not c.get("passes", False)]
            print(f"   ❌ Task failed. Failing criteria: {failing}")
        
    except json.JSONDecodeError:
        task["status"] = "failed"
        task["result"] = "Failed to parse result"
        print(f"   ❌ Failed to parse task result")
    
    task["completed_at"] = datetime.now().isoformat()
    save_state(data, state_dir)
    
    return task["status"] == "done"


def main():
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("--state-dir", default="state")
    parser.add_argument("--status", action="store_true")
    args = parser.parse_args()
    
    data = load_state(args.state_dir)
    
    if args.status:
        show_status(data)
        return
    
    task = get_next_task(data)
    
    if task is None:
        print("🎉 All tasks complete!")
        show_status(data)
        sys.exit(0)
    
    success = execute_task(task, data, args.state_dir)
    show_status(data)
    
    sys.exit(0 if success else 1)


if __name__ == "__main__":
    main()
```

---

## File: run.sh

```bash
#!/bin/bash
# Run harness worker in a loop with error handling.
#
# Usage:
#   ./run.sh              # Run until complete
#   ./run.sh --once       # Run one task only
#   ./run.sh --status     # Show status

set -e

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
cd "$SCRIPT_DIR"

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m'

# Configuration
DELAY=${HARNESS_DELAY:-3}
MAX_FAILURES=${HARNESS_MAX_FAILURES:-3}
STATE_DIR=${HARNESS_STATE_DIR:-state}

# Parse args
if [[ "$1" == "--once" ]]; then
    python work.py --state-dir "$STATE_DIR"
    exit $?
fi

if [[ "$1" == "--status" ]]; then
    python work.py --status --state-dir "$STATE_DIR"
    exit $?
fi

if [[ "$1" == "--help" ]]; then
    echo "Usage: ./run.sh [--once|--status|--help]"
    echo ""
    echo "Environment variables:"
    echo "  HARNESS_DELAY        Seconds between tasks (default: 3)"
    echo "  HARNESS_MAX_FAILURES Max consecutive failures before exit (default: 3)"
    echo "  HARNESS_STATE_DIR    State directory (default: state)"
    exit 0
fi

# Check initialization
if [[ ! -f "$STATE_DIR/tasks.json" ]]; then
    echo -e "${RED}❌ Harness not initialized.${NC}"
    echo "Run: python init.py 'Your objective here'"
    exit 1
fi

# Trap for clean shutdown
cleanup() {
    echo -e "\n${YELLOW}🛑 Shutting down gracefully...${NC}"
    python work.py --status --state-dir "$STATE_DIR"
    exit 0
}
trap cleanup SIGINT SIGTERM

# Main loop
echo -e "${GREEN}🚀 Starting harness loop${NC}"
echo "   Delay: ${DELAY}s | Max failures: ${MAX_FAILURES}"
echo "   Press Ctrl+C to stop"
echo ""

failures=0

while true; do
    if python work.py --state-dir "$STATE_DIR"; then
        failures=0
    else
        exit_code=$?
        if [[ $exit_code -eq 0 ]]; then
            echo -e "${GREEN}🎉 All tasks complete!${NC}"
            python work.py --status --state-dir "$STATE_DIR"
            exit 0
        fi
        
        ((failures++))
        echo -e "${YELLOW}⚠️  Task failed (${failures}/${MAX_FAILURES})${NC}"
        
        if [[ $failures -ge $MAX_FAILURES ]]; then
            echo -e "${RED}❌ Max failures reached. Stopping.${NC}"
            python work.py --status --state-dir "$STATE_DIR"
            exit 1
        fi
    fi
    
    # Check if done
    remaining=$(python -c "
import json
from pathlib import Path
tasks = json.loads(Path('$STATE_DIR/tasks.json').read_text())
open_tasks = [t for t in tasks['tasks'] if t['status'] in ('open', 'in_progress')]
print(len(open_tasks))
" 2>/dev/null || echo "0")
    
    if [[ "$remaining" == "0" ]]; then
        echo -e "${GREEN}🎉 All tasks complete!${NC}"
        python work.py --status --state-dir "$STATE_DIR"
        exit 0
    fi
    
    sleep "$DELAY"
done
```

---

## File: state/tasks.json (Example)

```json
{
  "metadata": {
    "objective": "Build a REST API for task management",
    "created_at": "2025-12-08T10:00:00",
    "total_tasks": 5
  },
  "tasks": [
    {
      "id": "T001",
      "title": "Initialize FastAPI project",
      "description": "Create project structure with FastAPI, pyproject.toml, basic health endpoint",
      "acceptance_criteria": [
        {"criterion": "pyproject.toml exists with FastAPI dependency", "passes": false},
        {"criterion": "GET /health returns 200", "passes": false},
        {"criterion": "Project runs with uvicorn", "passes": false}
      ],
      "dependencies": [],
      "status": "open",
      "result": null,
      "started_at": null,
      "completed_at": null
    },
    {
      "id": "T002",
      "title": "Add Task model and database",
      "description": "Create SQLModel Task entity, SQLite database, migrations",
      "acceptance_criteria": [
        {"criterion": "Task model has id, title, status, created_at fields", "passes": false},
        {"criterion": "Database file created on startup", "passes": false},
        {"criterion": "Can create Task programmatically", "passes": false}
      ],
      "dependencies": ["T001"],
      "status": "open",
      "result": null,
      "started_at": null,
      "completed_at": null
    }
  ]
}
```

---

## Integration with Toolkit

Add to `.claude/commands/harness-init.md`:

```markdown
# /project:harness-init

Initialize the agent harness for complex objectives.

## Steps

1. Create `.harness/` directory
2. Copy harness files (init.py, work.py, run.sh)
3. Ask for objective
4. Run `python .harness/init.py "OBJECTIVE"`
5. Show generated tasks

## Usage

```bash
# After init
cd .harness
./run.sh           # Run all tasks
./run.sh --once    # Run one task
./run.sh --status  # Show progress
```
```

Add to `.claude/CLAUDE.md`:

```markdown
## Harness Mode

For complex objectives (>5 features, >2 hours work):

1. Use `/project:harness-init` to decompose into tasks
2. Each task has acceptance criteria (red until verified)
3. Worker executes ONE task, exits
4. Next worker picks up next task
5. Prevents context overflow on long-running work

Key: Tasks stay `"passes": false` (red) until ALL acceptance criteria verified.
```

---

## Quick Start

```bash
# 1. Install
pip install anthropic

# 2. Set API key
export ANTHROPIC_API_KEY="your-key"

# 3. Initialize
python init.py "Build a CLI tool for managing dotfiles"

# 4. Run
./run.sh

# 5. Check status anytime
./run.sh --status
```

---

## Why This Pattern Works

1. **Context isolation** - Each task runs in fresh context
2. **Human checkpoints** - Can review/intervene between tasks
3. **Resumable** - Stop anytime, continue later
4. **Auditable** - Full logs per task in `state/logs/`
5. **Red/green tracking** - Clear pass/fail on each criterion
