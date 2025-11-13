# 🎯 Jira Workflow Tools - AI-Powered Team Edition

**Modern, secure, and AI-integrated toolkit for seamless Jira workflow management.**

*Designed for AI assistants, perfect for humans.*

---

## 🤖 **Cursor AI-First Workflow** (Primary Usage)

This tool is specifically designed for **Cursor AI** integration. Instead of memorizing commands, simply describe your Jira needs in natural language and let Cursor handle the technical details.

### **✨ How It Works with Cursor**

1. **Open this project in Cursor** - AI understands the entire codebase context
2. **Describe your Jira task** in natural language to Cursor
3. **Cursor translates** your request into the appropriate tool commands  
4. **Tool executes** securely with your credentials
5. **Results formatted** exactly how you need them

### **💡 Pro Tips for Cursor Users**

- **Be specific**: Mention project (RTDEV/APP), team, and priority for better results
- **Ask for explanations**: "Explain what this template does before running it"
- **Request dry-runs**: "Show me what this would create without actually doing it"
- **Format requests**: "Format the output for our team documentation"
- **Role assignments**: "Assign the UX designer and technical writer to this epic"

### **🚀 Advanced Cursor Workflows**

```
💬 "Create a high-priority bug for APP core-team, assign Sarah as UX designer, and format the result for our team meeting"

💬 "I need to bulk-check the status of tickets RTDEV-12345, RTDEV-12346, and RTDEV-12347"

💬 "Help me understand what the RTDEV-epic-lifecycle template includes and when I should use it"

💬 "Set up a complex epic with technical writer and architect assignments for our new mobile initiative"
```

### **💡 How to Get Better AI Results**

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

### **🚀 Why Cursor + Jira Tools = ⚡**

- **Full Codebase Context** - Cursor understands templates, configs, and project structure
- **Natural Language Interface** - No command memorization needed
- **Smart Suggestions** - Cursor suggests appropriate templates based on your project
- **Error Prevention** - AI validates before execution and explains what will happen
- **Rich Formatting** - Perfect output formatting for documentation, standups, reports
- **Instant Learning** - Cursor teaches you the tool as you use it
- **Workflow Integration** - Seamlessly fits into your existing development process

### **🎯 Cursor-Specific Advantages**

- **@codebase context** - Cursor sees all templates and configurations
- **Real-time validation** - Cursor checks your .env setup and suggests fixes
- **Smart completions** - Cursor autocompletes project names, team names, and options
- **Documentation integration** - Cursor references this README and all docs automatically

---

## ⚡ **Cursor Setup (5 minutes)**

### **Prerequisites**
- **Cursor IDE** - Download from cursor.com if not installed
- **Python 3.9+** - `python3 --version`
- **Your team's Jira access** - Organization Jira instance
- **API token** - From your Jira profile settings

### **Cursor Setup Steps**

1. **Clone and Open in Cursor**
```bash
git clone https://github.com/yonatanp-jfrog/jira-workflow-tools.git
cd jira-workflow-tools
cursor . # Opens project in Cursor
```

2. **Install Dependencies (Let Cursor Help!)**
```
💬 Ask Cursor: "Install the Python dependencies for this project"
🤖 Cursor will: pip3 install -r requirements.txt
```

3. **Configure Credentials with Cursor**
```
💬 Ask Cursor: "Set up my Jira credentials using the env template"
🤖 Cursor will:
  - Copy env.template to .env
  - Guide you through filling in your credentials
  - Help you get your API token
```

4. **Test Setup with Cursor**
```
💬 Ask Cursor: "Test my Jira configuration"
🤖 Cursor will: Run python3 -m jira_tools test-config
✅ Should show: Configuration valid, Connection successful!
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

---

## 🎯 **Daily Cursor Workflows**

### **Typical Cursor Chat Examples**

```
💬 "I need to create an epic for the RTDEV platform team about improving our authentication system"

🤖 Cursor responds: I'll help you create that epic. Based on your request, I'll use the RTDEV-epic-lifecycle template since this is for the platform team. Let me run:

python3 -m jira_tools epic "Authentication System Improvements" \
  --project RTDEV --template RTDEV-epic-lifecycle \
  --team "dev-artifactory-lifecycle" --area "Features & Innovation"

Would you like me to add any specific role assignments or adjust the priority?
```

```
💬 "Show me the details of ticket RTDEV-12345 and format it nicely for our team standup"

🤖 Cursor responds: I'll fetch that ticket and format it for your standup. Let me get the details:

python3 -m jira_tools viewer RTDEV-12345 --format markdown

This will give you a clean markdown format perfect for sharing in your standup notes.
```

```
💬 "What Jira templates do we have available for APP project bugs?"

🤖 Cursor responds: Let me check the available templates for you:

python3 -m jira_tools templates list

Based on the project structure, for APP project bugs you'll want to use:
- APP-bug-core: For critical application bugs and customer issues

Would you like me to show you what fields this template includes?
```

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