## 2024-05-23 - CLI Visual Hierarchy
**Learning:** Plain text CLI outputs lack visual hierarchy, making it difficult for users to quickly scan results or distinguish between success and failure states.
**Action:** Implement a simple `Palette` class using ANSI escape codes to color-code key information (e.g., Green for success/Flex, Cyan for info/Respond, Red for errors). This improves scannability without adding external dependencies.

## 2025-05-27 - Custom Interactive Elements Accessibility
**Learning:** Standard divs used as interactive elements (like drag-and-drop zones) are invisible to keyboard users and screen readers, creating a major accessibility barrier.
**Action:** Always add `tabindex="0"`, `role="button"`, `aria-label`, and `keydown` event listeners (for Enter/Space) to any non-button element made interactive. Ensure visible focus states (e.g., `focus:ring`) are present.

## 2025-06-03 - Dynamic List Focus Management
**Learning:** When removing items from a list that re-renders (like `innerHTML` updates), the element with focus is destroyed, causing focus to revert to `<body>`. This disorients keyboard and screen reader users.
**Action:** Before removing an item, calculate the next logical focus target (next item, previous item, or parent container). After re-rendering, programmatically restore focus to that target ID.
