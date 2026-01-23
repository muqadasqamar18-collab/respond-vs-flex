## 2024-05-23 - CLI Visual Hierarchy
**Learning:** Plain text CLI outputs lack visual hierarchy, making it difficult for users to quickly scan results or distinguish between success and failure states.
**Action:** Implement a simple `Palette` class using ANSI escape codes to color-code key information (e.g., Green for success/Flex, Cyan for info/Respond, Red for errors). This improves scannability without adding external dependencies.

## 2025-05-27 - Custom Interactive Elements Accessibility
**Learning:** Standard divs used as interactive elements (like drag-and-drop zones) are invisible to keyboard users and screen readers, creating a major accessibility barrier.
**Action:** Always add `tabindex="0"`, `role="button"`, `aria-label`, and `keydown` event listeners (for Enter/Space) to any non-button element made interactive. Ensure visible focus states (e.g., `focus:ring`) are present.

## 2026-01-23 - Dynamic List Focus Management
**Learning:** Re-rendering lists via `innerHTML` destroys the focused element, causing focus to revert to `body` and disrupting keyboard navigation.
**Action:** When modifying lists (e.g., deleting items), calculate the next logical focus target *before* the update, pass it to the render function, and programmatically apply focus to the new element (using stable IDs) after the DOM update.
