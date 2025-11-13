# 🚀 **Getting Started with Jira Workflow Tools**

**Complete setup and basic usage guide for the modern Jira workflow system.**

*Project successfully renamed from "Jira" to "jira-workflow-tools" for clarity.*

---

## 📋 **What You'll Learn**

- **5-minute setup** - Get running quickly
- **Basic usage** - Create epics and view issues  
- **Configuration** - Environment variables and private mode
- **First workflows** - Your essential daily commands

---

## 🎯 **Prerequisites**

- **Python 3.9+** - `python3 --version`
- **Jira access** - Your organization's Jira instance
- **API token** - From your Jira profile settings

---

## ⚡ **Quick Setup (5 minutes)**

### **Step 1: Install Dependencies**
```bash
# Navigate to project directory
cd /path/to/jira-workflow-tools

# Install required packages  
pip3 install -r requirements.txt

# Verify installation
python3 -m jira_tools --help
```

### **Step 2: Configure Credentials**
```bash
# Copy environment template
cp env.template .env

# Edit with your credentials
# JIRA_BASE_URL=https://your-org.atlassian.net
# JIRA_AUTH_TOKEN=your_api_token_here
# JIRA_USER_ACCOUNT_ID=your_account_id (optional)
```

### **Step 3: Test Configuration**
```bash
# Verify setup
python3 -m jira_tools test-config

# Should show: ✅ Configuration is valid
```

---

## 🎮 **Basic Commands**

### **View Issues**
```bash
# View any Jira issue
python3 -m jira_tools viewer RTDEV-12345
python3 -m jira_tools viewer "https://company.atlassian.net/browse/RTDEV-12345"

# Different output formats
python3 -m jira_tools viewer RTDEV-12345 --format markdown
python3 -m jira_tools viewer RTDEV-12345 --raw --output report.json
```

### **Create Epics**
```bash
# Interactive mode (recommended for beginners)
python3 -m jira_tools epic --interactive

# Direct creation
python3 -m jira_tools epic "My New Feature" --project RTDEV

# Advanced epic with all fields including role assignments
python3 -m jira_tools epic "Complex Feature" --project RTDEV \
  --template RTDEV-epic-lifecycle --commitment-level "Hard Commitment" \
  --area "Features & Innovation" --product-priority P1 \
  --technical-writer "michael.berman" --ux-designer "sarah.jones" --dry-run
```

### **Work with Templates**
```bash
# List available templates
python3 -m jira_tools templates list

# Create epic with specific template
python3 -m jira_tools epic "My Epic" --template RTDEV-epic-lifecycle --project RTDEV

# Describe what a template does
python3 -m jira_tools templates describe APP-epic-core
```

---

## 🔒 **Configuration Options**

### **Method 1: Environment Variables** (Recommended)
```bash
# In your .env file:
JIRA_BASE_URL=https://your-org.atlassian.net
JIRA_AUTH_TOKEN=your_api_token_here
JIRA_USER_ACCOUNT_ID=your_account_id  # Optional
```

### **Method 2: Private Mode** (Enhanced Security)
```bash
# Set up encrypted local storage
python3 -m jira_tools private setup

# Check private mode status
python3 -m jira_tools private status

# Backup private configuration
python3 -m jira_tools private backup
```

### **Get Your API Token**
1. Go to your Jira profile → **Security** → **API tokens**
2. Click **Create API token**
3. Give it a name (e.g., "Jira Tools")
4. Copy the token and paste into `.env` file

### **Find Your Account ID** (Optional)
```bash
# After basic setup, this command will show your account ID:
python3 -m jira_tools test-config
```

---

## 🎯 **Essential Workflows**

### **Daily Issue Review**
```bash
# Quick issue check
python3 -m jira_tools viewer RTDEV-12345

# Save issue details to file
python3 -m jira_tools viewer RTDEV-12345 --format markdown --output reports/
```

### **Epic Creation Workflow**
```bash
# For new users - interactive mode
python3 -m jira_tools epic --interactive

# For experienced users - direct creation
python3 -m jira_tools epic "Epic Name" --project RTDEV --description "Epic description"

# Always test first with dry-run
python3 -m jira_tools epic "Test Epic" --project RTDEV --dry-run
```

### **Template-Based Creation**
```bash
# Use built-in templates
python3 -m jira_tools epic "Feature Epic" --template RTDEV-epic-lifecycle --project RTDEV
python3 -m jira_tools epic "Bug Fix Epic" --template RTDEV-bug-lifecycle --project RTDEV

# List what's available
python3 -m jira_tools templates list

# Understand what a template does
python3 -m jira_tools templates describe RTDEV-epic-lifecycle
```

---

## 🚨 **Common Setup Issues**

### **"Command not found" Error**
```bash
# Use python3 explicitly
python3 -m jira_tools --help

# Check Python version
python3 --version  # Should be 3.9+
```

### **Authentication Failures**
```bash
# Verify your credentials
cat .env  # Check JIRA_BASE_URL and JIRA_AUTH_TOKEN

# Test connectivity
curl -I https://your-org.atlassian.net

# Regenerate API token if needed
```

### **Missing Dependencies**
```bash
# Reinstall requirements
pip3 install -r requirements.txt

# For private mode features
pip3 install -r requirements-private.txt
```

### **Template Not Found**
```bash
# Check available templates
python3 -m jira_tools templates list

# Understand what a template does
python3 -m jira_tools templates describe APP-epic-core

# Current templates available:
# - APP-epic-core (APP project epics)
# - APP-bug-core (APP project bugs) 
# - RTDEV-epic-lifecycle (RTDEV project epics)
# - RTDEV-bug-lifecycle (RTDEV project bugs)
# - RTDEV-task-lifecycle (RTDEV project tasks)
```

---

## 🎊 **You're Ready!**

### **Next Steps**
1. **Try interactive mode:** `python3 -m jira_tools epic --interactive`
2. **Explore templates:** `python3 -m jira_tools templates list`
3. **Set up private mode:** `python3 -m jira_tools private setup` (optional)
4. **Read workflows guide:** See `WORKFLOWS_AND_TROUBLESHOOTING.md` for advanced usage

### **Get Help**
```bash
# Comprehensive help system
python3 -m jira_tools --help
python3 -m jira_tools epic --help
python3 -m jira_tools viewer --help
python3 -m jira_tools templates --help
python3 -m jira_tools private --help
```

### **Quick Reference Card**
```bash
# The commands you'll use most:
python3 -m jira_tools epic --interactive              # Create epic (guided)
python3 -m jira_tools viewer ISSUE-123                # View issue
python3 -m jira_tools templates list                  # See templates
python3 -m jira_tools templates describe APP-epic-core # Understand template
python3 -m jira_tools test-config                     # Check setup

# Role assignments (NEW):
python3 -m jira_tools epic "My Epic" --template APP-epic-core \
  --technical-writer "michael.berman" --ux-designer "sarah.jones"
```

---

**Happy epic creating!** 🎯

*Need more advanced workflows? See `WORKFLOWS_AND_TROUBLESHOOTING.md`*  
*Still using legacy scripts? See root `MIGRATION_GUIDE.md`*
