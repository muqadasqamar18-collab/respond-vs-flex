## 2024-05-23 - Custom CLI Palette
**Learning:** For small Python CLIs, a custom `Palette` class using ANSI escape codes is better than adding heavy dependencies like `rich` or `colorama`. It keeps the project lightweight while still improving UX significantly.
**Action:** Implement `Palette` class with `flex` (blue/green), `respond` (yellow/magenta), and `dim` styles for cleaner output.
