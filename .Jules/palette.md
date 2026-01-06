## 2024-05-23 - Accessibility in Single Page Apps
**Learning:** Dynamic content updates often leave screen reader users unaware of changes.
**Action:** Use `aria-live` regions for status updates and ensure focus management when new content appears.

## 2024-05-24 - Focus Management
**Learning:** Custom interactive elements (like the drag-and-drop zone) need `tabindex="0"`, `role="button"`, and `keydown` event listeners for Enter/Space keys to be accessible.
**Action:** Always add keyboard support to `div`s acting as buttons.
