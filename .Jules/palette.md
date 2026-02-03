## 2024-05-23 - CLI Visual Hierarchy
**Learning:** Plain text CLI outputs lack visual hierarchy, making it difficult for users to quickly scan results or distinguish between success and failure states.
**Action:** Implement a simple `Palette` class using ANSI escape codes to color-code key information (e.g., Green for success/Flex, Cyan for info/Respond, Red for errors). This improves scannability without adding external dependencies.

## 2025-05-27 - Custom Interactive Elements Accessibility
**Learning:** Standard divs used as interactive elements (like drag-and-drop zones) are invisible to keyboard users and screen readers, creating a major accessibility barrier.
**Action:** Always add `tabindex="0"`, `role="button"`, `aria-label`, and `keydown` event listeners (for Enter/Space) to any non-button element made interactive. Ensure visible focus states (e.g., `focus:ring`) are present.

## 2025-02-18 - Focus Management in Dynamic Lists
**Learning:** When items are removed from a list and the DOM is rebuilt, keyboard focus is lost to the `body`, forcing users to re-navigate the entire page.
**Action:** Implement programmatic focus restoration after list updates. Calculate the next logical focus target (e.g., same index or previous item) before deletion and explicitly focus it after the DOM updates.

## 2025-06-01 - Non-blocking Notifications Layering
**Learning:** Notification containers often block clicks to underlying UI elements even when empty or when toasts are spaced out.
**Action:** Apply `pointer-events-none` to the toast container so it's transparent to clicks, but explicitly set `pointer-events-auto` on the toast messages themselves to ensure they remain interactive (e.g., for dismissal).
