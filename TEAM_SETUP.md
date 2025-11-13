# 🎯 Jira Workflow Tools - Team Setup Guide

**Internal team setup guide for the comprehensive Jira workflow toolkit.**

*Project renamed from "Jira" to "jira-workflow-tools" to better reflect its capabilities.*

---

## 🚀 Quick Start for Team Members

### Prerequisites
- Python 3.9+ installed
- Access to JFrog Jira instance
- Your Jira API token

### 1. Clone and Setup
```bash
# Clone the repository (replace with your team's repo URL)
git clone https://github.com/your-team/jira-workflow-tools.git
cd jira-workflow-tools

# Install dependencies
pip3 install -r requirements.txt
```

### 2. Configure Credentials
```bash
# Copy the template
cp env.template .env

# Edit .env with your credentials
# IMPORTANT: Never commit the .env file!
```

### 3. Test Your Setup
```bash
# Test configuration and connection
python3 -m jira_tools test-config

# Should show:
# ✅ Configuration valid
# ✅ Connection successful!
# 👤 Logged in as: Your Name
```

### 4. Start Using the Tools
```bash
# View a Jira ticket
python3 -m jira_tools viewer RTDEV-12345

# Create an epic with modern templates
python3 -m jira_tools epic --interactive

# List available templates
python3 -m jira_tools templates list

# Get help
python3 -m jira_tools --help
```

---

## 🔒 Security Features Implemented

### ✅ **Security Audit Complete**
- ❌ **Removed**: Hardcoded personal account ID (`712020:23cfbba9...`)
- ❌ **Removed**: Hardcoded JFrog URLs 
- ❌ **Secured**: Sensitive Published Issues moved to `.jira-staging/`
- ✅ **Added**: Comprehensive `.gitignore` with security patterns
- ✅ **Added**: Environment variable validation

### ✅ **New Project Structure**
```
jira-workflow-tools/
├── jira_tools/                  # 📦 Main package
│   ├── core/                    # 🏗️ Core functionality
│   │   ├── config.py           # ⚙️ Modern config management
│   │   ├── client.py           # 🌐 Improved Jira client
│   │   ├── templates.py        # 🎯 Human-readable template system
│   │   └── template_translator.py # 🔄 Jira API translation
│   ├── commands/               # 🖥️ CLI commands
│   ├── utils/                  # 🛠️ Utilities
│   └── __main__.py             # 🎯 CLI entry point
├── templates/                  # 📋 Human-readable templates
│   ├── APP-epic-core.j2        # APP epic template
│   ├── RTDEV-epic-lifecycle.j2 # RTDEV epic template
│   ├── RTDEV-bug-lifecycle.j2  # RTDEV bug template
│   └── FIELD_MAPPINGS.md       # Field reference guide
├── tests/                      # 🧪 Testing framework
├── .jira-staging/              # 🔒 Secure local staging
├── .gitignore                  # 🛡️ Comprehensive security
├── env.template                # 📋 Configuration template
└── requirements*.txt           # 📦 Dependencies
```

### ✅ **Modern CLI Interface**
- 🎯 New command structure: `python3 -m jira_tools [command]`
- 🧪 Built-in configuration testing
- 🔍 Enhanced issue viewer with rich formatting
- 📋 Human-readable template system with automatic Jira translation
- 👥 Role assignment support (technical writers, UX designers, architects)
- 🛡️ Proper error handling and security validation

---

## 🛠️ Available Commands

### Configuration
```bash
python3 -m jira_tools setup           # Basic setup guide
python3 -m jira_tools setup --private # Private mode (Phase 4)
python3 -m jira_tools test-config     # Test connection
```

### Epic & Issue Management
```bash
python3 -m jira_tools epic --interactive                    # Create epic (guided)
python3 -m jira_tools epic "My Epic" --template APP-epic-core --project APP
python3 -m jira_tools epic "Bug Fix" --template RTDEV-bug-lifecycle --project RTDEV
python3 -m jira_tools viewer PROJ-123                       # View issue
python3 -m jira_tools templates list                        # List templates
python3 -m jira_tools templates describe APP-epic-core      # Understand template
python3 -m jira_tools --help                               # Show all commands
```

---

## 🔧 Configuration Options

### Environment Variables (.env file)
```bash
# Required
JIRA_BASE_URL=https://jfrog-int.atlassian.net
JIRA_AUTH_TOKEN=your_base64_token
JIRA_USER_ACCOUNT_ID=your_account_id

# Optional (for private mode - Phase 4)
JIRA_PRIVATE_MODE=true
ORGANIZATION_CONFIG=jfrog
```

### Getting Your API Token
1. Go to: https://id.atlassian.com/manage-profile/security/api-tokens
2. Create a new token
3. Base64 encode: `echo -n "your-email@jfrog.com:your-token" | base64`
4. Use the result as `JIRA_AUTH_TOKEN`

---

## 🚨 Security Guidelines

### ⚠️ **NEVER COMMIT THESE FILES:**
- `.env` - Contains your credentials
- `.jira-staging/` - Contains sensitive data
- Any file with `secret`, `token`, or `credential` in the name

### ✅ **Safe Practices:**
- Always use the `.env` file for credentials
- Keep `.env` secure and never share it
- Use private mode (coming in Phase 4) for enhanced security
- Report any security issues to the team immediately

---

## 🆘 Getting Help

### For Team Members:
1. **Check this guide** - Most common issues are covered here
2. **Test your config** - Run `python3 -m jira_tools test-config`
3. **Create a GitHub issue** - Use our team repository
4. **Ask on team Slack** - #jira-tools channel (if available)

### Common Issues:
- **"Configuration invalid"** - Check your `.env` file format
- **"Connection failed"** - Verify your API token is correct
- **"Module not found"** - Run `pip3 install -r requirements.txt`

---

## 📋 Implementation Status

### ✅ **Implementation Complete**
- ✅ Security audit and cleanup
- ✅ Modern project structure  
- ✅ Full CLI interface with all commands
- ✅ Configuration management (environment variables + private mode)
- ✅ Human-readable template system with automatic Jira translation
- ✅ Role assignment support (technical writers, UX designers, architects)
- ✅ Enhanced epic creation with interactive mode
- ✅ Local staging with comprehensive security
- ✅ Template analysis and validation
- ✅ Team setup guide and documentation

---

## 📞 Team Contacts

- **Repository Maintainer**: [Your Name]
- **Security Issues**: Report immediately to team lead
- **Feature Requests**: Create GitHub issue with label `enhancement`

---

*Last Updated: Full Implementation Complete*
*Version: 3.0.0-team with Human-Readable Templates*
