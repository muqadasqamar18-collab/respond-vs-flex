## 2024-05-23 - CLI Visual Hierarchy
**Learning:** Plain text CLI outputs lack visual hierarchy, making it difficult for users to quickly scan results or distinguish between success and failure states.
**Action:** Implement a simple `Palette` class using ANSI escape codes to color-code key information (e.g., Green for success/Flex, Cyan for info/Respond, Red for errors). This improves scannability without adding external dependencies.

## 2025-05-27 - Custom Interactive Elements Accessibility
**Learning:** Standard divs used as interactive elements (like drag-and-drop zones) are invisible to keyboard users and screen readers, creating a major accessibility barrier.
**Action:** Always add `tabindex="0"`, `role="button"`, `aria-label`, and `keydown` event listeners (for Enter/Space) to any non-button element made interactive. Ensure visible focus states (e.g., `focus:ring`) are present.

## 2025-10-27 - Dynamic List Focus Management
**Learning:** When an item is removed from a list and the list is re-rendered, the focused element is destroyed, causing focus to reset to the document body. This disorients keyboard and screen reader users.
**Action:** When modifying dynamic lists (e.g., deleting items), explicitly calculate the next logical focus target (e.g., the next item or a placeholder) and programmatically set focus after the DOM update. Use stable IDs to track elements across renders.
