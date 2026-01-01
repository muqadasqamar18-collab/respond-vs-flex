## 2024-05-23 - CLI Visual Hierarchy
**Learning:** Plain text CLI outputs lack visual hierarchy, making it difficult for users to quickly scan results or distinguish between success and failure states.
**Action:** Implement a simple `Palette` class using ANSI escape codes to color-code key information (e.g., Green for success/Flex, Cyan for info/Respond, Red for errors). This improves scannability without adding external dependencies.

## 2025-05-27 - Keyboard Accessible Drag & Drop
**Learning:** Custom interactive elements like drag-and-drop zones are often inaccessible to keyboard users because they lack semantic roles and focus states.
**Action:** Always add `tabindex="0"`, `role="button"`, and explicit keyboard event listeners (Enter/Space) to non-button interactive elements to ensure inclusivity.
