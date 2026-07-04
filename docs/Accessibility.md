# Accessibility (a11y) Standards

ShopSense AI is committed to being an inclusive platform. We must adhere to WCAG 2.1 AA standards.

## 1. Keyboard Navigation
- **Focus Rings:** Every interactive element (links, buttons, inputs) MUST have a highly visible focus state (e.g., a 2px solid blue outline) for users navigating via `Tab`.
- **Skip Links:** Provide a hidden "Skip to main content" link at the very top of the DOM that becomes visible on focus, allowing users to bypass the navigation menu.
- **Modals & Dialogs:** When a modal opens (e.g., Price Alert signup), focus must be trapped inside the modal until it is closed. Hitting `Escape` must close the modal.

## 2. Screen Readers
- **Semantic HTML:** Use `<header>`, `<nav>`, `<main>`, `<article>`, and `<footer>` instead of a soup of `<div>` tags.
- **ARIA Attributes:** Use `aria-label`, `aria-hidden`, and `aria-expanded` strictly where necessary (e.g., for icon-only buttons).
- **Alt Text:** Every product image must have descriptive `alt` text (e.g., `alt="Apple iPhone 15 in Blue, Back View"`). Do NOT use generic text like `alt="image"`.

## 3. Visual & Color Standards
- **Color Contrast:** The contrast ratio between text and its background must be at least 4.5:1 for normal text and 3:1 for large text. This is critical for the Deep Blue and Emerald Green palettes.
- **Color Reliance:** Do not rely solely on color to convey information. (e.g., Error states must have a red border AND an error icon or text).
- **Dark/Light Mode:** Ensure both themes maintain strict contrast ratios.

## 4. Typography & Responsiveness
- **Scalable Text:** Use `rem` for font sizes instead of `px` so text scales based on the user's browser/OS settings.
- **Touch Targets:** On mobile devices, interactive elements must be at least `44x44px` with sufficient padding to prevent accidental clicks.
- **Motion:** Respect the user's OS `prefers-reduced-motion` setting. Disable all micro-animations and smooth scrolling if this flag is true.
