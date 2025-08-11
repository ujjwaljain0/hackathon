# Global User Rules for Cursor AI

Copy the content below to your Cursor Settings → General → Rules for AI

---

## Communication Style
- Reply in a concise, professional style
- Avoid unnecessary repetition or filler language  
- Don't apologize for errors - identify and fix them directly
- Ask specific, targeted questions when clarification is needed
- Provide reasoning for technical decisions and recommendations

## Code Generation Preferences
- Always use TypeScript when JavaScript is requested (unless specifically told otherwise)
- Prefer functional programming patterns over object-oriented when appropriate
- Use modern ES6+ syntax and features
- Implement proper error handling in all code
- Include type definitions and interfaces for all data structures

## Default Frameworks & Libraries
- React: Use functional components with hooks
- Node.js: Use ES modules and async/await
- CSS: Prefer CSS modules or styled-components over global styles
- Testing: Use Jest and React Testing Library for React projects
- Database: Use parameterized queries and proper ORM patterns

## Quality Standards
- Write self-documenting code with clear variable names
- Add comments only for complex business logic
- Implement proper input validation and sanitization
- Include error boundaries and graceful error handling
- Follow accessibility best practices (ARIA labels, semantic HTML)

## Performance Considerations
- Optimize for bundle size and loading performance
- Use lazy loading for non-critical components
- Implement proper caching strategies
- Consider SEO implications for web applications
- Minimize re-renders and expensive operations

## Security Mindset
- Always validate inputs from external sources
- Use environment variables for sensitive configuration
- Implement proper authentication and authorization
- Follow OWASP security guidelines
- Use HTTPS for all external communications

---

## How to Apply These Rules

1. Open Cursor Settings (Cmd/Ctrl + ,)
2. Go to General → Rules for AI
3. Copy and paste the content above (excluding the header and this section)
4. Save the settings

These rules will apply to all your projects and set your personal coding preferences for AI interactions.
