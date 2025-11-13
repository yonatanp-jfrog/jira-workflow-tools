# Pull Request

## 📋 Description
<!-- Provide a clear description of what this PR does -->

### Type of Change
<!-- Check the relevant option -->
- [ ] 🐛 Bug fix (non-breaking change that fixes an issue)
- [ ] ✨ New feature (non-breaking change that adds functionality)
- [ ] 💥 Breaking change (fix or feature that would cause existing functionality to not work as expected)
- [ ] 📚 Documentation update
- [ ] 🎨 Template addition/modification
- [ ] 🔧 Configuration change
- [ ] 🧪 Tests

## 🧪 Testing
<!-- Describe how you tested these changes -->

### Commands Tested
```bash
# List the commands you tested
python3 -m jira_tools test-config
python3 -m jira_tools templates list
# etc.
```

### Test Results
- [ ] All existing functionality still works
- [ ] New functionality works as expected
- [ ] Templates validate successfully (if applicable)
- [ ] Configuration tests pass
- [ ] No security issues introduced

## 📝 Changes Made
<!-- List the specific changes made -->

### Files Modified
- [ ] Core functionality (`jira_tools/core/`)
- [ ] CLI commands (`jira_tools/commands/` or `__main__.py`)
- [ ] Templates (`templates/` or `builtin_templates/`)
- [ ] Configuration (`config/`, `.env`, etc.)
- [ ] Documentation (`*.md` files)
- [ ] Tests (`tests/`)

### Security Considerations
- [ ] No hardcoded secrets or credentials added
- [ ] No sensitive data exposed in templates
- [ ] No changes that could compromise security
- [ ] All new files respect `.gitignore` patterns

## 🎯 Related Issues
<!-- Link any related issues -->
Fixes #(issue_number)
Related to #(issue_number)

## 📚 Documentation
<!-- Check if documentation needs updates -->
- [ ] Documentation updated (if needed)
- [ ] Template descriptions added/updated (if applicable)
- [ ] TEAM_SETUP.md updated (if setup process changed)
- [ ] Comments added to complex code

## ✅ Checklist
<!-- Check all that apply -->
- [ ] Code follows the existing style and patterns
- [ ] Self-review completed
- [ ] Templates validated (if applicable)
- [ ] No breaking changes to existing workflows
- [ ] Commit messages are clear and descriptive
- [ ] Ready for team review

## 💬 Additional Notes
<!-- Any additional information for reviewers -->

### Breaking Changes
<!-- If there are breaking changes, describe them here -->
None

### Migration Required
<!-- If team members need to take action, describe it here -->
None

---

## For Reviewers
<!-- Guidance for team members reviewing this PR -->

### Review Focus Areas
- [ ] Functionality works as described
- [ ] Security considerations addressed
- [ ] No hardcoded secrets or sensitive data
- [ ] Templates are valid and useful
- [ ] Documentation is clear and accurate
- [ ] Changes don't break existing workflows

### Testing Commands
```bash
# Commands for reviewers to test
python3 -m jira_tools test-config
python3 -m jira_tools templates list
# Add specific commands relevant to the changes
```
