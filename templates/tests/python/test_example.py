"""
Example test file for Python projects using pytest.

Run with: pytest tests/
"""

import pytest
from typing import Any


class TestExample:
    """Example test class demonstrating best practices."""

    def test_basic_assertion(self):
        """Test basic assertions."""
        assert 1 + 1 == 2

    def test_with_fixture(self, example_fixture):
        """Test using a fixture."""
        assert example_fixture is not None

    @pytest.mark.parametrize("input,expected", [
        (1, 2),
        (2, 4),
        (3, 6),
    ])
    def test_parametrized(self, input: int, expected: int):
        """Test with multiple parameter sets."""
        assert input * 2 == expected

    @pytest.mark.asyncio
    async def test_async_function(self):
        """Test async functions."""
        result = await async_example()
        assert result == "success"


@pytest.fixture
def example_fixture() -> dict[str, Any]:
    """Example fixture providing test data."""
    return {"key": "value"}


async def async_example() -> str:
    """Example async function."""
    return "success"


# Integration test example
@pytest.mark.integration
class TestIntegration:
    """Integration tests - may require external services."""

    def test_api_endpoint(self):
        """Test actual API endpoint."""
        # Mock or test against real service
        pass


# End-to-end test example
@pytest.mark.e2e
class TestE2E:
    """End-to-end tests - full user workflows."""

    def test_user_workflow(self):
        """Test complete user workflow."""
        # 1. User creates account
        # 2. User logs in
        # 3. User performs action
        # 4. Verify result
        pass
