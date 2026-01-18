## 2024-05-23 - CLI Visual Hierarchy
**Learning:** Plain text CLI outputs lack visual hierarchy, making it difficult for users to quickly scan results or distinguish between success and failure states.
**Action:** Implement a simple `Palette` class using ANSI escape codes to color-code key information (e.g., Green for success/Flex, Cyan for info/Respond, Red for errors). This improves scannability without adding external dependencies.

## 2025-05-27 - Custom Interactive Elements Accessibility
**Learning:** Standard divs used as interactive elements (like drag-and-drop zones) are invisible to keyboard users and screen readers, creating a major accessibility barrier.
**Action:** Always add `tabindex="0"`, `role="button"`, `aria-label`, and `keydown` event listeners (for Enter/Space) to any non-button element made interactive. Ensure visible focus states (e.g., `focus:ring`) are present.

## 2026-01-18 - Dynamic List Focus Management
**Learning:** Removing items from a dynamic list (like `innerHTML` re-renders) causes focus loss to the document body, forcing keyboard users to re-navigate the entire page.
**Action:** When modifying lists, programmatically shift focus to the nearest relevant element (next item, previous item, or parent container) immediately after the DOM update to preserve context.
