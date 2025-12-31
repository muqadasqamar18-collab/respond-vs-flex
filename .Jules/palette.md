## 2024-05-23 - CLI Visual Hierarchy
**Learning:** Plain text CLI outputs lack visual hierarchy, making it difficult for users to quickly scan results or distinguish between success and failure states.
**Action:** Implement a simple `Palette` class using ANSI escape codes to color-code key information (e.g., Green for success/Flex, Cyan for info/Respond, Red for errors). This improves scannability without adding external dependencies.

## 2025-05-27 - Icon-Only Buttons Accessibility
**Learning:** Dynamic icon-only buttons (like "Remove file") are invisible to screen readers without explicit labels, creating barriers for assistive technology users.
**Action:** Always add `aria-label` and `title` attributes to icon-only buttons. Ensure focus states are visible (e.g., `focus:ring`) since default outlines may be removed by utility classes.
