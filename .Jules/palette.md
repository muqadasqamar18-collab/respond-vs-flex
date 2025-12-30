## 2025-12-30 - Drop Zone Accessibility
**Learning:** Custom interactive elements like file drop zones are invisible to keyboard users if implemented as simple `<div>`s with click listeners.
**Action:** Always add `tabindex="0"`, `role="button"`, and keyboard event handlers (Enter/Space) to non-button interactive elements to ensure full accessibility.
