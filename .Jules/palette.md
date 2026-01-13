# Palette's Journal

## 2024-05-21 - Initial Accessibility Review
**Learning:** The application uses native HTML/JS with Tailwind CSS. Accessibility is decent (aria-labels on remove buttons, keyboard support for drag-and-drop), but focus management during dynamic list updates is missing.
**Action:** When modifying the file list, ensure focus is preserved or logically moved to prevent "loss of context" for screen reader users.

## 2024-05-21 - Focus Management in Dynamic Lists
**Learning:** When removing an item from a list, focus is lost if the removed element was focused.
**Action:** Programmatically move focus to the next available item or back to the main container (drop zone) if the list becomes empty.
