/**
 * Example test file for TypeScript projects using Vitest/Jest.
 *
 * Run with: npm test
 */

import { describe, it, expect, beforeEach, afterEach, vi } from 'vitest';
// For Jest, use: import { describe, it, expect, beforeEach, afterEach, jest } from '@jest/globals';

describe('Example Test Suite', () => {
  it('should pass basic assertion', () => {
    expect(1 + 1).toBe(2);
  });

  it('should test objects', () => {
    const obj = { name: 'test', value: 42 };
    expect(obj).toEqual({ name: 'test', value: 42 });
    expect(obj).toHaveProperty('name');
  });

  it('should test arrays', () => {
    const arr = [1, 2, 3];
    expect(arr).toContain(2);
    expect(arr).toHaveLength(3);
  });

  it('should test async functions', async () => {
    const result = await asyncExample();
    expect(result).toBe('success');
  });

  it('should test promises', () => {
    return expect(Promise.resolve('done')).resolves.toBe('done');
  });

  it('should test errors', () => {
    expect(() => {
      throw new Error('test error');
    }).toThrow('test error');
  });
});

describe('Mocking Example', () => {
  it('should mock functions', () => {
    const mockFn = vi.fn();
    // For Jest: const mockFn = jest.fn();

    mockFn('arg1', 'arg2');

    expect(mockFn).toHaveBeenCalledWith('arg1', 'arg2');
    expect(mockFn).toHaveBeenCalledTimes(1);
  });

  it('should mock modules', async () => {
    vi.mock('./external-service', () => ({
      fetchData: vi.fn().mockResolvedValue({ data: 'mocked' }),
    }));

    // Test code using mocked module
  });
});

describe('Lifecycle Hooks', () => {
  let testData: any;

  beforeEach(() => {
    // Setup before each test
    testData = { count: 0 };
  });

  afterEach(() => {
    // Cleanup after each test
    testData = null;
  });

  it('should use setup data', () => {
    testData.count += 1;
    expect(testData.count).toBe(1);
  });
});

describe('Parametrized Tests', () => {
  it.each([
    [1, 2, 3],
    [2, 3, 5],
    [5, 5, 10],
  ])('should add %i + %i = %i', (a, b, expected) => {
    expect(a + b).toBe(expected);
  });
});

// Integration tests
describe('Integration Tests', () => {
  it.skip('should test API endpoint', async () => {
    // Mark as skip or use test.integration tag
    // Test against real/mock API
  });
});

// E2E tests
describe('E2E Tests', () => {
  it.skip('should complete user workflow', async () => {
    // Full user journey test
    // 1. Setup
    // 2. Execute workflow
    // 3. Verify results
    // 4. Cleanup
  });
});

// Helper functions
async function asyncExample(): Promise<string> {
  return Promise.resolve('success');
}

// Type testing (with TypeScript)
interface User {
  id: number;
  name: string;
}

describe('Type Tests', () => {
  it('should work with typed data', () => {
    const user: User = { id: 1, name: 'Test' };
    expect(user.id).toBe(1);
    expect(user.name).toBe('Test');
  });
});
