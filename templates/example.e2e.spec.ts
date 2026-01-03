import { test, expect } from '@playwright/test';

/**
 * Example E2E Test Suite
 * Copy to your project's tests/e2e folder and customize
 */

test.describe('Application E2E Tests', () => {

  test.beforeEach(async ({ page }) => {
    // Navigate to home page before each test
    await page.goto('/');
  });

  test('homepage loads correctly', async ({ page }) => {
    // Check page title
    await expect(page).toHaveTitle(/My App/);

    // Check main heading exists
    await expect(page.getByRole('heading', { level: 1 })).toBeVisible();
  });

  test('navigation works', async ({ page }) => {
    // Click a navigation link
    await page.click('nav a[href="/about"]');

    // Verify URL changed
    await expect(page).toHaveURL(/.*about/);
  });

  test('user can log in', async ({ page }) => {
    // Navigate to login
    await page.goto('/login');

    // Fill in credentials
    await page.fill('input[name="email"]', 'test@example.com');
    await page.fill('input[name="password"]', 'password123');

    // Submit form
    await page.click('button[type="submit"]');

    // Verify logged in (redirected to dashboard)
    await expect(page).toHaveURL(/.*dashboard/);

    // Verify user greeting appears
    await expect(page.getByText(/Welcome/)).toBeVisible();
  });

  test('form validation works', async ({ page }) => {
    await page.goto('/contact');

    // Submit empty form
    await page.click('button[type="submit"]');

    // Check for validation errors
    await expect(page.getByText(/required/i)).toBeVisible();
  });

  test('API integration works', async ({ page }) => {
    await page.goto('/dashboard');

    // Wait for data to load
    await page.waitForSelector('[data-testid="data-list"]');

    // Verify data appears
    const items = await page.locator('[data-testid="data-item"]').count();
    expect(items).toBeGreaterThan(0);
  });

});

// Visual regression test example
test('homepage visual regression', async ({ page }) => {
  await page.goto('/');
  await expect(page).toHaveScreenshot('homepage.png', {
    maxDiffPixels: 100,
  });
});

// API mock example
test('works with mocked API', async ({ page }) => {
  // Mock API response
  await page.route('**/api/users', async route => {
    await route.fulfill({
      status: 200,
      contentType: 'application/json',
      body: JSON.stringify([
        { id: 1, name: 'Test User' }
      ]),
    });
  });

  await page.goto('/users');
  await expect(page.getByText('Test User')).toBeVisible();
});
