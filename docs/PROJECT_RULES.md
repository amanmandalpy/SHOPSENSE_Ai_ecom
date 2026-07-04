# ShopSense AI: Project Rules Engine

> **PRIORITY DIRECTIVE**
> This Rules Engine has the highest priority. Every future task must follow these rules. Do not ignore these rules. Do not override these rules. Do not invent your own architecture. Do not remove any existing feature unless explicitly instructed. Always preserve backward compatibility. Never delete existing code unless replacing it with a better implementation. Always think like a Senior Software Architect. 
> 
> **Whenever a future prompt conflicts with these rules, THIS RULES ENGINE ALWAYS WINS.**

---

## 1. Project Goal
Build a production-ready AI Shopping Comparison Platform. The project must be:
- Scalable and Maintainable
- Secure and Accessible
- SEO Friendly and Responsive
- Fast and Professional
- Suitable for real users and future affiliate integrations

## 2. General Development Rules
- **Never** generate demo code, placeholder code, TODO comments, or unfinished implementations.
- **Never** skip validation.
- **Never** hardcode secrets, credentials, or URLs. Always use environment variables.
- **Always** write production-ready code.

## 3. Coding Standards
- Follow **Clean Architecture**, **SOLID Principles**, **DRY**, and **KISS**.
- Use Reusable Components and Modular Design.
- Enforce Consistent Naming and write Small Functions.
- Ensure Readable Code with Meaningful Variable Names.
- Write Meaningful Comments only where absolutely required.

## 4. Project Structure Rules
- Respect the existing folder structure.
- **Never** randomly create folders or duplicate files.
- Group similar features together and keep the project highly organized.

## 5. Django Rules
- Use Django Best Practices and Class-Based Views where appropriate.
- Use Django REST Framework where APIs are required.
- Use Model Managers when needed.
- Use Signals *only* if absolutely necessary.
- **Optimize ORM Queries:** Avoid N+1 Queries. Use `select_related()` and `prefetch_related()` where appropriate. Never write inefficient database queries.

## 6. Database Rules
- Use **PostgreSQL**.
- Normalize tables properly and avoid duplicate data.
- Use Foreign Keys correctly and indexes where required.
- Maintain data integrity and never store unnecessary information.

## 7. UI Rules
- Modern, Premium, and Minimal UI.
- Responsive and **Mobile First**.
- Professional Typography, Consistent Spacing, Accessible Colors, and Smooth Animations.
- Reusable Components with absolute zero clutter.

## 8. UX Rules
- Fast navigation, simple interactions, and minimal clicks.
- Helpful empty states and human-readable error messages.
- Professional loading states (Skeleton loading where appropriate).
- Meaningful feedback after every action.

## 9. Security Rules
- Protect against: SQL Injection, Cross Site Scripting (XSS), CSRF, and Clickjacking.
- Implement strict Rate Limiting, Input Validation, and Output Escaping.
- Use Secure Cookies, Secure Headers, and JWT Security.
- **Never** expose secrets.

## 10. SEO Rules
Every public page MUST include:
- Meta Title & Meta Description
- Canonical URL
- OpenGraph & Twitter Cards
- Structured Data (Schema markup) where appropriate
- SEO Friendly URLs
- Global `robots.txt` and `sitemap.xml`

## 11. Performance Rules
- Optimize images, database queries, and static files.
- Minimize network requests.
- Implement Lazy loading and Caching (Redis/CDN) where useful.
- Guarantee fast page loading.

## 12. Accessibility Rules
- Strictly follow **WCAG 2.1 AA** standards.
- Full Keyboard Navigation and Screen Reader compatibility.
- Use Proper Labels, Good Color Contrast, and Visible Focus States.

## 13. Error Handling
- **Never crash.** Handle all exceptions gracefully.
- Log useful information but **never** expose sensitive internal errors to the user.
- Provide user-friendly, actionable messages.

## 14. Logging Rules
- Log important events, authentication flows, critical failures, and unexpected exceptions.
- **Never** log secrets, passwords, or PII.

## 15. Testing Rules
- Every feature must be testable.
- Validate inputs, rigorously test edge cases, and handle invalid requests.

## 16. Git Rules
- Keep commits small.
- One feature per commit.
- Never mix unrelated changes.

## 17. Documentation
- Update documentation immediately whenever the architecture changes.
- Do not let documentation become outdated.
