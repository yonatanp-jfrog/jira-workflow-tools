# 🎯 Jira Workflow Tools - Internal Team Edition

**Modern, secure, and feature-complete toolkit for Jira workflow management.**

*Formerly known as "Jira" project - now properly named to reflect its comprehensive workflow capabilities.*

> 🚨 **IMPORTANT - LEGACY DEPRECATION:** Legacy scripts (`epic_creator.py`, `create_epic.py`, `jira_viewer.py`) are **DEPRECATED** and will be removed on **2025-03-01**. Use the modern `python3 -m jira_tools` system instead.

---

## 🚀 Quick Start for Team Members

### ⚡ **Modern Jira Workflow System** (All users)
```bash
# Clone, install, configure  
git clone https://github.com/your-team/jira-workflow-tools.git
cd jira-workflow-tools
pip3 install -r requirements.txt
cp env.template .env
# Edit .env with your credentials, then:
python3 -m jira_tools test-config

# Create epics (basic and advanced) 
python3 -m jira_tools epic "My New Feature" --template APP-epic-core --project APP
python3 -m jira_tools epic --interactive  # Step-by-step wizard
python3 -m jira_tools epic "Complex Epic" --project RTDEV \
  --template RTDEV-epic-lifecycle --commitment-level "Hard Commitment" --area "Features & Innovation" \
  --technical-writer "michael.berman" --ux-designer "sarah.jones"

# View issues with enhanced capabilities  
python3 -m jira_tools viewer RTDEV-12345
python3 -m jira_tools viewer "https://company.atlassian.net/browse/RTDEV-12345" --format markdown
python3 -m jira_tools viewer "Check issue RTDEV-12345" --raw

# Explore system capabilities and understand templates
python3 -m jira_tools templates list                        # List all templates with descriptive names
python3 -m jira_tools templates describe APP-epic-core      # Understand what a template does  
python3 -m jira_tools templates describe RTDEV-epic-lifecycle  # RTDEV lifecycle template
python3 -m jira_tools templates describe RTDEV-bug-lifecycle   # RTDEV bug template
python3 -m jira_tools epic "My Epic" --explain             # Quick template explanation
python3 -m jira_tools --help
```

### 🚨 **Migrating from Legacy Scripts?**
The modern system (`python3 -m jira_tools`) replaces legacy scripts with enhanced features, security, and team collaboration support.

---

## 🎯 **System Features**

### 🔒 **Modern Jira Workflow System** (`jira_tools/`)
**Complete replacement for legacy scripts with enhanced capabilities**

**✅ Key Features:**
- **Enhanced epic creation** with human-readable templates and all legacy fields
- **Interactive wizard mode** with step-by-step prompts and smart defaults
- **Advanced issue viewer** with URL parsing, multiple formats, and rich display
- **Human-readable template system** with automatic Jira API translation
- **Role assignment support** - technical writers, UX designers, architects
- **Private mode** with encrypted credential storage for enhanced security
- **Local staging** with comprehensive security measures
- **Rich CLI** with beautiful output, comprehensive help, and error guidance
- **No hardcoded secrets** - secure environment variable or private mode configuration
- **Professional architecture** - modular, testable, maintainable codebase

**🎮 Available Commands:**
```bash
python3 -m jira_tools --help           # Main help system
python3 -m jira_tools epic --help      # Epic creation (basic + advanced + interactive)
python3 -m jira_tools viewer --help    # Issue viewing (enhanced with URL parsing)
python3 -m jira_tools private --help   # Private mode (encrypted local storage)
python3 -m jira_tools staging --help   # Local staging (secure issue preparation)
python3 -m jira_tools templates --help # Template management (Jinja2 + validation)
```

---

## 📊 **Why Choose the Modern System?**

### **🆕 New Users**
- **Secure by default** - no hardcoded secrets or organizational data
- **Well documented** - comprehensive guides and help system
- **Team-friendly** - GitHub integration and professional architecture
- **Modern best practices** - modular code, comprehensive testing

### **🔧 Advanced Feature Users**  
- **All legacy fields available** - commitment levels, areas, product priorities, etc.
- **Enhanced interactive workflows** - smarter prompts and defaults
- **Template system** - Jinja2-powered, customizable, shareable
- **Multiple output formats** - console, markdown, JSON with rich formatting

### **👥 Team Collaboration**
- **No security risks** - no hardcoded secrets for safe team sharing
- **Private mode** - encrypted local storage for enhanced security
- **GitHub integration** - professional issue templates and documentation
- **Consistent experience** - same interface and capabilities for all team members

### **⚡ Power Users**
- **More configuration options** - all legacy fields + role assignments
- **Human-readable templates** - no more cryptic field IDs, plain English configuration
- **Advanced field mappings** - comprehensive Jira custom field support with automatic translation
- **Role-based assignments** - assign technical writers, UX designers, architects
- **Enhanced URL parsing** - works with any Jira URL format
- **Professional output** - rich console display + multiple export formats

---

## 🔒 **Security & Best Practices**

### **Modern System Security** ✅
- **No hardcoded secrets** - uses environment variables or encrypted private mode
- **Secure credential storage** - OS keyring integration for private mode
- **Safe for team sharing** - no organizational data embedded in code
- **Comprehensive security validation** - automated scanning and auditing
- **Professional security practices** - input validation, error handling, secure defaults

### **⚠️ Legacy System Security Issues** 
- **DEPRECATED - Contains security risks** - hardcoded JFrog-specific URLs and data
- **Not suitable for team sharing** - embedded organizational information
- **Missing dependencies** - broken imports may cause runtime failures
- **No active maintenance** - security issues will not be fixed

**🚨 Recommendation:** Migrate to modern system immediately for security and reliability.

---

## 📚 **Documentation**

### **🚀 Essential Guides** (Start Here)
- **[Getting Started](docs/GETTING_STARTED.md)** - Complete setup and basic usage guide
- **[Workflows & Troubleshooting](docs/WORKFLOWS_AND_TROUBLESHOOTING.md)** - Advanced workflows and problem solving
- **[Staged Epic Workflow](docs/STAGED_EPIC_WORKFLOW.md)** - Two-phase collaborative epic creation

### **🔄 Migration & Team Setup**
- **[Team Setup Guide](TEAM_SETUP.md)** - Complete team onboarding instructions
- **[Field Mappings](templates/FIELD_MAPPINGS.md)** - Human-readable template field reference

---

## 🧪 **Testing & Validation**

```bash
# Run comprehensive test suite
python3 tests/test_runner.py

# Test specific systems
python3 -m jira_tools test-config     # New system
python3 epic_creator.py --help        # Legacy system
```

**✅ All tests passing:** Security validation, functionality tests, CLI validation, template system

---

## 🤝 **Contributing & Support**

### **Team Support:**
- **🐛 Bug Reports:** [Create Issue](../../issues/new?template=bug-report.yml)
- **💡 Feature Requests:** [Create Issue](../../issues/new?template=feature-request.yml)  
- **❓ Team Support:** [Create Issue](../../issues/new?template=team-support.yml)

### **Contributing:**
- Both systems are actively maintained
- New system preferred for new features
- Legacy system maintained for compatibility
- See GitHub templates for contribution guidelines

---

## 🎯 **System Status**

| System | Status | Security | Features | Team Ready |
|--------|--------|----------|----------|------------|
| **New Modular** | ✅ Production | ✅ Secure | 🔄 Growing | ✅ Yes |
| **Legacy Enhanced** | ✅ Stable | ⚠️ JFrog-specific | ✅ Complete | ✅ With caution |

---

## 🚀 **Getting Started**

1. **Follow** [TEAM_SETUP.md](TEAM_SETUP.md) for detailed setup
2. **Read** [Getting Started Guide](docs/GETTING_STARTED.md) for basic usage
3. **Explore** [templates/FIELD_MAPPINGS.md](templates/FIELD_MAPPINGS.md) to understand template fields
4. **Test** your configuration with `python3 -m jira_tools test-config`
5. **Create** your first epic with `python3 -m jira_tools epic --interactive`

**🎉 Ready to streamline your Jira workflow with human-readable templates!**