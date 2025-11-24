# 🎯 Jira Workflow Tools - AI-Powered Team Edition

**Modern, secure, and AI-integrated toolkit for seamless Jira workflow management.**

*Designed for AI assistants, perfect for humans. This tool is specifically designed for **Cursor AI** integration - simply describe your Jira needs in natural language and let Cursor handle the technical details.*

## 🚀 **Quick Examples**

```
💬 "Create a high-priority bug for APP core-team, assign Sarah as UX designer, and format the result for our team meeting"

💬 "Help me understand what the RTDEV-epic-lifecycle template includes and when I should use it"

💬 "Set up a complex epic with technical writer and architect assignments for our new mobile initiative"

💬 "Create an RTDEV bug for authentication issues and attach these files: error-screenshot.png, logs.txt, config.json"
```

## 🚀 **Quick Start (2 minutes)**

### **Prerequisites**
- **Python 3.9+** - `python3 --version`
- **JFrog Jira access** - Access to your team's Jira instance
- **API token** - We'll help you create this during setup

### **Automated Setup**

**New Interactive Onboarding (Recommended):**
```bash
git clone https://github.com/yonatanp-jfrog/jira-workflow-tools.git
cd jira-workflow-tools
pip3 install -r requirements.txt
python3 -m jira_tools onboard
```

### **🎯 What You'll See During Setup**

The interactive wizard provides a friendly, step-by-step experience:

**Welcome Screen:**
```
🎯 Welcome to JFrog Jira Workflow Tools Setup Wizard!

This interactive setup will configure your environment in just a few minutes.
We'll guide you through:
• Jira connection and authentication
• Project and team discovery  
• Template personalization for JFrog workflows
• Custom field mapping
• Configuration validation

Let's get you set up for productive Jira workflows!
```

**Step 1/6: JFrog Jira Configuration**
```
First, let's connect to your Jira instance.
Jira URL [https://jfrog-int.atlassian.net]: ⏎
   # Just press Enter to use JFrog default, or type custom URL

⚡ Validating Jira connection... ✅ Connected successfully!
   Server: Jira
   Version: 9.4.0
```

**Step 2/6: Authentication Setup**
```
Now let's set up your authentication credentials.
What's your JFrog email address?: john.doe@jfrog.com

📝 Let's create your API token...
Opening the Atlassian API token page...

⚠️  IMPORTANT: When creating your token:
   ✅ Click "Create API token" 
   ❌ DO NOT click "Create API token with scopes"

🌐 Browser opened to: https://id.atlassian.com/manage-profile/security/api-tokens

After creating your token:
1. Give it a name like 'JFrog Jira Tools'
2. Copy the generated token
3. Paste it below (input will be hidden)

Paste your API token: ••••••••••••••••

⚡ Testing authentication... ✅ Authentication successful!
   Welcome, John Doe!
   Account ID: 557058:f58131cb-b67d-43c7-b30d-6b58d40bd077
```

**Step 3/6: JFrog Project Discovery**
```
Let's discover your accessible projects and teams...
✅ Found 23 accessible projects

Which project do you primarily work with?
Primary project [RTDEV]: ⏎
   # Press Enter for RTDEV default, or type: APP, XRAY, etc.

Do you work with any additional projects?
Enter as comma-separated list (e.g., APP,XRAY) or press Enter to skip:
Additional projects: APP,XRAY

✅ Found 15 teams in your selected projects

Available teams:
┏━━━━━━━━┳━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┳━━━━━━━━━━━┓
┃ Number ┃ Team Name                 ┃ Project   ┃
┡━━━━━━━━╇━━━━━━━━━━━━━━━━━━━━━━━━━━━━━╇━━━━━━━━━━━┩
│ 1      │ dev-artifactory-lifecycle │ RTDEV     │
│ 2      │ platform-team             │ RTDEV     │
│ 3      │ app-core                  │ APP       │
│ 4      │ security-team             │ Multiple  │
│ ... (showing first 4 of 15 teams)

Select your team (number or name): 1
✅ Selected team: dev-artifactory-lifecycle
```

**Step 4/6: JFrog Template Personalization**
```
Let's customize templates with your JFrog preferences...

Template preferences:
Default priority for new issues? [High/Normal/Low] (Normal): ⏎
Default Product Manager [john.doe@jfrog.com]: ⏎
Epic naming prefix convention [RLM 4Q25 -]: ⏎
Default Product Backlog format [Q4-25-Backlog]: Q1-26-Backlog
Default Commitment Reason [Roadmap/Customer Commitment/Security] (Roadmap): ⏎

✅ Template personalization settings saved!
These will be used as defaults when creating new issues.
```

**Step 5/6: JFrog Custom Field Configuration**
```
Discovering JFrog Jira custom fields...
✅ Using JFrog-standard custom field mappings
   • Team field: customfield_10129
   • Product Manager field: customfield_10044
   • Commitment Level: customfield_10450
   • Area: customfield_10167

Epic prefix for RTDEV project [RTDEV]: ⏎
```

**Step 6/6: Configuration Validation & Testing**
```
Running final validation checks...
⚡ Testing Jira API connection... ✅ Jira API connection
⚡ Validating permissions... ✅ Permissions validated
⚡ Saving configuration... ✅ Configuration saved
```

**🎉 Setup Complete!**
```
🎉 Setup Complete! Your JFrog Jira Workflow Tools are ready to use.

📁 Configuration saved to: .env
🏢 Connected to: https://jfrog-int.atlassian.net
👤 User: john.doe@jfrog.com
📂 Primary project: RTDEV
👥 Team: dev-artifactory-lifecycle

🚀 Try these commands to get started:

Basic Commands:
• python -m jira_tools epic "My First Epic" --project RTDEV
• python -m jira_tools viewer RTDEV-12345
• python -m jira_tools templates list

Need help? Run: python -m jira_tools --help
Re-run setup anytime: python -m jira_tools onboard --reconfigure
```

**⚡ Total setup time: Under 2 minutes!**

### **Cursor AI Setup (Alternative)**

1. **Clone and Open in Cursor**
```bash
git clone https://github.com/yonatanp-jfrog/jira-workflow-tools.git
cd jira-workflow-tools
cursor . # Opens project in Cursor
```

2. **Ask Cursor to Set Everything Up**
```
💬 Ask Cursor: "Run the interactive onboarding to set up my JFrog Jira tools"
🤖 Cursor will: Run python3 -m jira_tools onboard and guide you through
```

### **Getting Your API Token (or ask Cursor to guide you!)**
```
💬 Ask Cursor: "Help me get a Jira API token"
🤖 Cursor will guide you through the process, or follow these steps:
```

1. Go to: **https://id.atlassian.com/manage-profile/security/api-tokens**
2. Click **"Create API token"** (NOT "Create API token with scopes")
3. Give it a name (e.g., "AI Jira Tools")
4. Copy the generated token immediately (you won't see it again!)
5. Paste the token into your `.env` file as `JIRA_AUTH_TOKEN=your_token_here`

## 💡 **How to Get Better AI Results**

**Include these details in your requests for optimal AI assistance:**

- **Project**: `RTDEV` or `APP`
- **Team**: `platform-team`, `core-team`, `dev-artifactory-lifecycle`, `mobile-team`, etc.
- **Type**: `epic` (large initiatives), `bug` (defects), `task` (work items), `story` (features)
- **Priority**: `high`, `critical`, `normal`, `low`
- **Roles**: Mention if you need `technical-writer`, `ux-designer`, or `architect` assignments

**Examples of well-structured requests:**
```
✅ "Create a high-priority bug for APP core-team with UX designer assigned"
✅ "Make an RTDEV lifecycle epic for platform-team with technical writer" 
✅ "Create an APP epic for core-team focused on user authentication features"
✅ "Show RTDEV-12345 details formatted for our team documentation"
✅ "List all templates available for APP project work"
```

## 🤖 **Why Cursor AI Integration?**

**🚀 Cursor + Jira Tools = ⚡**

- **Full Codebase Context** - Cursor understands templates, configs, and project structure
- **Natural Language Interface** - No command memorization needed
- **Smart Suggestions** - Cursor suggests appropriate templates based on your project
- **Error Prevention** - AI validates before execution and explains what will happen
- **Rich Formatting** - Perfect output formatting for documentation, standups, reports
- **Instant Learning** - Cursor teaches you the tool as you use it
- **Workflow Integration** - Seamlessly fits into your existing development process

**🎯 Cursor-Specific Advantages**

- **@codebase context** - Cursor sees all templates and configurations
- **Real-time validation** - Cursor checks your .env setup and suggests fixes
- **Smart completions** - Cursor autocompletes project names, team names, and options
- **Documentation integration** - Cursor references this README and all docs automatically

---


## 🔒 **Security & Team Features**

### **✅ Production Ready**
- **No hardcoded secrets** - Environment variables or encrypted private mode
- **Safe for team sharing** - No organizational data embedded in code
- **Comprehensive security** - Input validation, secure defaults, audit trail
- **Role-based assignments** - Technical writers, UX designers, architects
- **Private mode available** - Encrypted credential storage with OS keyring

### **👥 Team Collaboration**
- **Consistent AI experience** - Same interface for all team members
- **Template system** - Human-readable, shareable, customizable
- **Rich output formats** - Console, markdown, JSON with proper formatting
- **Professional documentation** - GitHub integration with issue templates

---

## 🏗️ **Project Structure**

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
├── docs/                       # 📚 Documentation
├── .gitignore                  # 🛡️ Comprehensive security
├── env.template                # 📋 Configuration template
└── requirements*.txt           # 📦 Dependencies
```

## 🎨 **Available Templates & Projects**

### **Current Templates**
```bash
# List all available templates
python3 -m jira_tools templates list

# Understand what a template does  
python3 -m jira_tools templates describe APP-epic-core
python3 -m jira_tools templates describe RTDEV-epic-lifecycle
```

### **Built-in Templates**
- **APP-epic-core** - Customer-facing features and core application epics
- **APP-bug-core** - Critical application bugs and customer issues
- **RTDEV-epic-lifecycle** - Platform features and Artifactory lifecycle work  
- **RTDEV-bug-lifecycle** - Platform bugs and infrastructure issues
- **RTDEV-task-lifecycle** - Operational tasks and development work

---

## 📚 **Advanced Documentation**

### **Team Resources**
- **[Workflows & Troubleshooting](docs/WORKFLOWS_AND_TROUBLESHOOTING.md)** - Advanced workflows and problem solving
- **[Staged Epic Workflow](docs/STAGED_EPIC_WORKFLOW.md)** - Collaborative epic creation process
- **[Template Field Mappings](templates/FIELD_MAPPINGS.md)** - Field reference for custom templates

### **Support & Contributing**
- **🐛 Bug Reports:** [Create Issue](../../issues/new?template=bug-report.yml)
- **💡 Feature Requests:** [Create Issue](../../issues/new?template=feature-request.yml)  
- **❓ Team Support:** [Create Issue](../../issues/new?template=team-support.yml)

---

## 🛠️ **Manual Usage** (Advanced Users/Non-Cursor Scenarios)

*For direct command-line usage when not using Cursor AI or for advanced automation*

### **Core Commands**
```bash
# Configuration and testing
python3 -m jira_tools --help           # Main help system
python3 -m jira_tools test-config      # Test your setup

# Epic creation
python3 -m jira_tools epic --interactive                    # Interactive wizard
python3 -m jira_tools epic "Epic Name" --project RTDEV      # Direct creation
python3 -m jira_tools epic "Complex Epic" --project RTDEV \
  --template RTDEV-epic-lifecycle --commitment-level "Hard Commitment" \
  --area "Features & Innovation" --technical-writer "sarah.jones"

# Epic creation with file attachments
python3 -m jira_tools epic "Bug Fix Epic" --project RTDEV \
  --template RTDEV-epic-lifecycle --attach "error-log.txt,screenshot.png"
python3 -m jira_tools epic "Design Epic" --project APP \
  --template APP-epic-core --attach "mockup.pdf,wireframe.png,specs.docx"

# Issue viewing  
python3 -m jira_tools viewer RTDEV-12345                    # View issue
python3 -m jira_tools viewer "https://company.atlassian.net/browse/RTDEV-12345" --format markdown
python3 -m jira_tools viewer RTDEV-12345 --raw --output report.json

# Template management
python3 -m jira_tools templates list                        # List templates
python3 -m jira_tools templates describe APP-epic-core      # Understand template
```

### **Advanced Configuration**
```bash
# Private mode (encrypted storage)
python3 -m jira_tools private setup    # Set up encrypted storage
python3 -m jira_tools private status   # Check private mode status
python3 -m jira_tools private backup   # Backup configuration

# Template validation
python3 -m jira_tools templates validate path/to/template.j2
```

### **Manual Troubleshooting**
```bash
# Common diagnostic commands
python3 --version                       # Check Python version (need 3.9+)
python3 -m jira_tools test-config      # Verify credentials and connectivity
python3 -m jira_tools templates list   # Check available templates
pip3 install -r requirements.txt       # Reinstall dependencies if needed
```

---

## 🧪 **Testing & Validation**

```bash
# Test the tool without making changes
python3 -m jira_tools epic "Test Epic" --project RTDEV --dry-run

# Run comprehensive test suite
python3 tests/test_runner.py

# Validate templates
python3 -m jira_tools templates validate templates/APP-epic-core.j2
```

---

## 🚨 **Legacy System Migration**

> **IMPORTANT:** Legacy scripts (`epic_creator.py`, `create_epic.py`, `jira_viewer.py`) are **DEPRECATED** and will be removed on **2025-03-01**. 

**Migration is simple:** All legacy functionality is available in the modern system with enhanced features and security.

---

## 🎯 **System Status**

| Component | Status | Security | Cursor Integration | Team Ready |
|-----------|--------|----------|-------------------|------------|
| **Core System** | ✅ Production | ✅ Secure | ✅ Fully Optimized | ✅ Yes |
| **Templates** | ✅ Active | ✅ Validated | ✅ Context-Aware | ✅ Yes |
| **Documentation** | ✅ Complete | ✅ Reviewed | ✅ Cursor-Ready | ✅ Yes |
| **Cursor Workflows** | ✅ Tested | ✅ Secure | ✅ Native Support | ✅ Yes |

---

**🎉 Ready to streamline your Jira workflow with Cursor AI!**

*Have questions? Just ask Cursor - it knows this entire codebase and is designed to help you use these tools effortlessly!*