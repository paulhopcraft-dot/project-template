package example_test

// Example test file for Go projects using standard testing package.
//
// Run with: go test ./...
// Coverage: go test -cover ./...
// Verbose: go test -v ./...

import (
	"context"
	"errors"
	"testing"
	"time"
)

// TestBasicAssertion demonstrates basic test structure
func TestBasicAssertion(t *testing.T) {
	got := 1 + 1
	want := 2

	if got != want {
		t.Errorf("got %d, want %d", got, want)
	}
}

// TestWithSubtests demonstrates table-driven tests with subtests
func TestWithSubtests(t *testing.T) {
	tests := []struct {
		name     string
		input    int
		expected int
	}{
		{"double 1", 1, 2},
		{"double 2", 2, 4},
		{"double 3", 3, 6},
	}

	for _, tt := range tests {
		t.Run(tt.name, func(t *testing.T) {
			got := tt.input * 2
			if got != tt.expected {
				t.Errorf("got %d, want %d", got, tt.expected)
			}
		})
	}
}

// TestWithTestify demonstrates using testify package (if available)
// Uncomment if using github.com/stretchr/testify
/*
import "github.com/stretchr/testify/assert"

func TestWithTestify(t *testing.T) {
	assert.Equal(t, 2, 1+1)
	assert.NotNil(t, "string")
	assert.True(t, true)
}
*/

// TestErrorHandling demonstrates error testing
func TestErrorHandling(t *testing.T) {
	err := returnsError()
	if err == nil {
		t.Error("expected error, got nil")
	}

	if !errors.Is(err, ErrExample) {
		t.Errorf("expected ErrExample, got %v", err)
	}
}

// TestContextTimeout demonstrates testing with context
func TestContextTimeout(t *testing.T) {
	ctx, cancel := context.WithTimeout(context.Background(), 100*time.Millisecond)
	defer cancel()

	result := make(chan string, 1)

	go func() {
		time.Sleep(50 * time.Millisecond)
		result <- "done"
	}()

	select {
	case <-ctx.Done():
		t.Error("context timeout")
	case res := <-result:
		if res != "done" {
			t.Errorf("got %s, want done", res)
		}
	}
}

// BenchmarkExample demonstrates benchmark testing
func BenchmarkExample(b *testing.B) {
	for i := 0; i < b.N; i++ {
		_ = expensiveOperation()
	}
}

// TestMain allows setup/teardown for entire test suite
func TestMain(m *testing.M) {
	// Setup
	setup()

	// Run tests
	code := m.Run()

	// Teardown
	teardown()

	// Exit with test result code
	os.Exit(code)
}

// Example tests - appear in godoc
func ExampleAdd() {
	result := Add(1, 2)
	fmt.Println(result)
	// Output: 3
}

// Helpers and test data
var ErrExample = errors.New("example error")

func returnsError() error {
	return ErrExample
}

func expensiveOperation() int {
	sum := 0
	for i := 0; i < 1000; i++ {
		sum += i
	}
	return sum
}

func setup() {
	// Initialize test database, configs, etc.
}

func teardown() {
	// Cleanup resources
}

// Integration test example (use build tags)
// Build with: go test -tags=integration

//go:build integration
// +build integration

func TestIntegration(t *testing.T) {
	if testing.Short() {
		t.Skip("skipping integration test in short mode")
	}

	// Test with real external services
}

// Parallel tests
func TestParallel(t *testing.T) {
	t.Parallel() // Run this test in parallel with others

	tests := []struct {
		name string
		fn   func(t *testing.T)
	}{
		{"test1", func(t *testing.T) { /* ... */ }},
		{"test2", func(t *testing.T) { /* ... */ }},
	}

	for _, tt := range tests {
		tt := tt // Capture range variable
		t.Run(tt.name, func(t *testing.T) {
			t.Parallel() // Run subtests in parallel
			tt.fn(t)
		})
	}
}
