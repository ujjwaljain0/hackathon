# Cursor Rules for AI-Assisted Development

This directory contains comprehensive rules for Cursor AI to follow when helping with development tasks. These rules are based on modern best practices and community-proven approaches.

## Rule Files Overview

### 1. `core.mdc` - Core Development Rules
- **Always Applied**: These rules guide every AI interaction
- **Scope**: All files in the project (`**/*`)
- **Purpose**: Fundamental development principles, code quality standards, and best practices

### 2. `feature-development.mdc` - Feature Development Guidelines
- **Manually Applied**: Use when building new features
- **Scope**: Source code files (`src/**/*`, `lib/**/*`, `components/**/*`)
- **Purpose**: Systematic approach to implementing new functionality

### 3. `debugging.mdc` - Debugging & Bug Fix Guidelines
- **Manually Applied**: Use when troubleshooting issues
- **Scope**: All files (`**/*`)
- **Purpose**: Systematic debugging methodology and fix implementation

## How to Use These Rules

### Automatic Application
- **Core rules** are automatically applied to all AI interactions
- No manual intervention required

### Manual Application
When working on specific tasks, you can invoke the specialized rules:

#### For New Features
```
@feature-development
```
This will apply the feature development guidelines to your current task.

#### For Debugging
```
@debugging
```
This will apply the debugging guidelines to help troubleshoot issues.

## Key Benefits

✅ **Consistent Code Quality**: Core rules ensure all generated code follows best practices
✅ **Systematic Development**: Feature development rules provide structured approaches
✅ **Efficient Debugging**: Debugging rules offer proven troubleshooting methodologies
✅ **Language Agnostic**: Works across all programming languages and frameworks
✅ **Community Proven**: Based on analysis of successful development workflows

## Customization

You can modify these rules to match your specific:
- Project architecture patterns
- Coding standards and conventions
- Technology stack preferences
- Team workflow requirements

## Best Practices

1. **Start with Core Rules**: These provide the foundation for all development
2. **Use Specialized Rules**: Apply feature or debugging rules when relevant
3. **Iterate and Improve**: Update rules based on your team's experience
4. **Share with Team**: These rules help maintain consistency across team members

## Rule Format

These rules use the modern `.mdc` format with YAML frontmatter:
- `description`: Human-readable description of the rule set
- `globs`: File patterns where rules apply
- `alwaysApply`: Whether rules are automatically applied

## Getting Started

1. The core rules are already active for all AI interactions
2. When starting a new feature, use `@feature-development`
3. When debugging, use `@debugging`
4. Customize rules as needed for your specific project requirements

---

*These rules are designed to work with Cursor's AI system and will significantly improve your development workflow by ensuring consistent, high-quality code generation and systematic problem-solving approaches.*
