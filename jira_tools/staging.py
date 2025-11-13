"""
Local staging system for Jira Workflow Tools.

Provides secure, local-only staging for sensitive Jira content with comprehensive
security warnings and automatic protection measures.

Features:
- Local-only staging with comprehensive security warnings
- Automatic git protection and secure permissions
- Integration with private mode for enhanced security
- Staged content never leaves the local machine
- Security audit and validation capabilities
"""

import os
import json
import shutil
from pathlib import Path
from datetime import datetime
from typing import Dict, Any, Optional, List

from rich.console import Console
from rich.panel import Panel
from rich.prompt import Confirm
from rich.table import Table

from jira_tools.utils.exceptions import StagingError

console = Console()


class LocalStaging:
    """
    Secure local staging for sensitive Jira content.
    
    Provides comprehensive security measures to ensure staged content
    never accidentally leaves the local machine.
    """
    
    def __init__(self, staging_dir: Optional[str] = None):
        """
        Initialize local staging.
        
        Args:
            staging_dir: Custom staging directory. If None, uses .jira-staging
        """
        if staging_dir:
            self.staging_dir = Path(staging_dir)
        else:
            # Try private mode staging first, fall back to .jira-staging
            try:
                from jira_tools.private_mode import private_mode_manager
                if private_mode_manager.is_configured():
                    self.staging_dir = private_mode_manager.staging_dir
                else:
                    self.staging_dir = Path(".jira-staging")
            except Exception:
                self.staging_dir = Path(".jira-staging")
        
        self.gitignore_entries = [
            "# Jira Tools - Local staging only (contains sensitive data)",
            f"{self.staging_dir}/",
            "*.jira-local",
            "*.jira-staged",
            ".env.local",
            ".jira-staging/",
            ".jira-private/"
        ]
        
        self._ensure_security_setup()
    
    def _ensure_security_setup(self):
        """Ensure comprehensive security measures are in place."""
        # Create staging directory with secure permissions
        self.staging_dir.mkdir(mode=0o700, parents=True, exist_ok=True)
        
        # Ensure secure permissions on existing directory
        if os.name != 'nt':  # Unix-like systems
            os.chmod(self.staging_dir, 0o700)
        
        # Ensure gitignore protection
        self._ensure_gitignore()
        
        # Create security warning file
        self._create_security_readme()
    
    def _ensure_gitignore(self):
        """Ensure staging directory is protected in .gitignore."""
        # Look for .gitignore in current directory and parent directories
        current_dir = Path.cwd()
        gitignore_updated = False
        
        for search_dir in [current_dir] + list(current_dir.parents):
            gitignore_path = search_dir / ".gitignore"
            
            # If we find a .gitignore, update it
            if gitignore_path.exists():
                self._update_gitignore(gitignore_path)
                gitignore_updated = True
                break
        
        # If no .gitignore found, create one in current directory
        if not gitignore_updated:
            gitignore_path = current_dir / ".gitignore"
            self._update_gitignore(gitignore_path)
    
    def _update_gitignore(self, gitignore_path: Path):
        """Update gitignore file with staging exclusions."""
        if gitignore_path.exists():
            content = gitignore_path.read_text()
        else:
            content = ""
        
        entries_to_add = [
            entry for entry in self.gitignore_entries 
            if entry not in content
        ]
        
        if entries_to_add:
            with gitignore_path.open("a") as f:
                f.write("\n" + "\n".join(entries_to_add) + "\n")
    
    def _create_security_readme(self):
        """Create comprehensive security warning in staging directory."""
        readme_path = self.staging_dir / "README_SECURITY.md"
        
        content = f"""# ⚠️  SECURITY WARNING ⚠️

**THIS DIRECTORY CONTAINS LOCAL STAGING FILES WITH SENSITIVE DATA**

## 🚨 CRITICAL SECURITY RULES:

### ✅ SAFE:
- Keep this directory on your local machine ONLY
- Let the Jira Tools manage permissions automatically
- Use the built-in commands to manage staged content

### ❌ NEVER DO:
- **NEVER** commit this directory to version control
- **NEVER** share files from this directory with others
- **NEVER** copy files to public locations (email, cloud storage, etc.)
- **NEVER** change file permissions to be more permissive

## 📁 What's Stored Here:
- **Staged Jira issues** with organization-specific field IDs
- **Custom field mappings** and project configurations  
- **Team assignments** and user account IDs
- **API request payloads** ready for Jira submission

## 🔒 Security Measures:
- **Directory permissions**: `700` (owner access only)
- **File permissions**: `600` (owner read/write only)
- **Git protection**: Automatically excluded from version control
- **Local-only operation**: Content never leaves your machine

## 🎯 Purpose:
This staging area allows you to:
1. **Review issues before creation** - See exactly what will be sent to Jira
2. **Batch operations** - Stage multiple issues and create them together
3. **Template testing** - Validate template rendering before use
4. **Offline preparation** - Prepare issues while offline

## 📋 File Format:
Files are stored as `.jira-staged` JSON files containing:
- Complete Jira API payload
- Metadata (timestamp, template used, etc.)
- Security headers and warnings

## 🧹 Cleanup:
- Staged files are automatically cleaned up after successful creation
- Use `python -m jira_tools staging clean` to manually clean old files
- Use `python -m jira_tools staging list` to see staged content

## 🚨 If You See This Directory in a Public Repository:
**THIS IS A SECURITY VIOLATION** - Contact the repository maintainer immediately!

---
**Generated by Jira Workflow Tools Local Staging**  
**Last updated: {datetime.now().isoformat()}**  
**Directory: {self.staging_dir.absolute()}**
"""
        
        readme_path.write_text(content)
        if os.name != 'nt':
            os.chmod(readme_path, 0o600)
    
    def stage_issue(self, issue_data: Dict[str, Any], filename: str, 
                   issue_type: str = "issue", template_used: Optional[str] = None) -> Path:
        """
        Stage issue locally with comprehensive security warnings.
        
        Args:
            issue_data: Complete Jira issue payload
            filename: Base filename (without extension)
            issue_type: Type of issue being staged
            template_used: Template that was used to generate the issue
            
        Returns:
            Path to staged file
        """
        # Show security warning for first-time users
        self._show_security_warning(issue_type)
        
        # Add comprehensive security header
        staged_content = self._add_security_header(issue_data, issue_type, template_used)
        
        # Write to staging file
        stage_file = self.staging_dir / f"{filename}.jira-staged"
        
        # Ensure file doesn't already exist (prevent overwriting)
        counter = 1
        while stage_file.exists():
            stage_file = self.staging_dir / f"{filename}_{counter}.jira-staged"
            counter += 1
        
        stage_file.write_text(staged_content)
        
        # Set restrictive permissions
        if os.name != 'nt':
            os.chmod(stage_file, 0o600)
        
        console.print(f"✅ Staged locally: [yellow]{stage_file.name}[/yellow]")
        console.print("🔒 File secured with owner-only permissions")
        console.print(f"📍 Location: {stage_file.parent}")
        
        return stage_file
    
    def _add_security_header(self, content: Dict[str, Any], issue_type: str, 
                           template_used: Optional[str] = None) -> str:
        """Add comprehensive security header to staged content."""
        
        # Analyze content for sensitive data indicators
        sensitive_indicators = self._analyze_sensitivity(content)
        
        header = f"""{{
  "_security_warning": {{
    "message": "⚠️  LOCAL STAGING FILE - CONTAINS SENSITIVE DATA",
    "rules": [
      "NEVER commit this file to version control",
      "NEVER share this file outside your organization",
      "NEVER copy to cloud storage or public locations",
      "DELETE after successful Jira issue creation"
    ],
    "contains_sensitive_data": {len(sensitive_indicators) > 0},
    "sensitivity_indicators": {json.dumps(sensitive_indicators)},
    "issue_type": "{issue_type}",
    "template_used": "{template_used or 'unknown'}",
    "staged_timestamp": "{datetime.now().isoformat()}",
    "staging_directory": "{self.staging_dir.absolute()}",
    "git_protected": true,
    "file_permissions": "600 (owner read/write only)"
  }},
  "_jira_payload": """
        
        footer = """
}"""
        
        return header + json.dumps(content, indent=2) + footer
    
    def _analyze_sensitivity(self, content: Dict[str, Any]) -> List[str]:
        """Analyze content for sensitive data indicators."""
        indicators = []
        
        content_str = json.dumps(content).lower()
        
        # Check for common sensitive patterns
        sensitive_patterns = [
            ("project_ids", "project"),
            ("user_account_ids", "accountid"),
            ("custom_fields", "customfield"),
            ("team_assignments", "team"),
            ("internal_urls", "jfrog"),
            ("organization_data", "atlassian.net")
        ]
        
        for indicator_name, pattern in sensitive_patterns:
            if pattern in content_str:
                indicators.append(indicator_name)
        
        return indicators
    
    def _show_security_warning(self, issue_type: str):
        """Show security warning for staging operations."""
        # Only show detailed warning periodically to avoid spam
        warning_file = self.staging_dir / ".last_warning"
        show_warning = True
        
        if warning_file.exists():
            try:
                last_warning = datetime.fromisoformat(warning_file.read_text())
                # Show warning if it's been more than 24 hours
                show_warning = (datetime.now() - last_warning).total_seconds() > 86400
            except Exception:
                show_warning = True
        
        if show_warning:
            console.print(Panel(
                f"[bold red]🔒 STAGING SECURITY NOTICE[/bold red]\n\n"
                f"You are staging a [yellow]{issue_type}[/yellow] locally.\n\n"
                f"[bold]Staged files contain sensitive organizational data and should:[/bold]\n"
                f"• Stay on your local machine ONLY\n"
                f"• Never be committed to version control\n"
                f"• Never be shared outside your organization\n\n"
                f"[green]✅ This staging area is automatically protected with secure permissions[/green]",
                title="Local Staging Security"
            ))
            
            # Update warning timestamp
            warning_file.write_text(datetime.now().isoformat())
            if os.name != 'nt':
                os.chmod(warning_file, 0o600)
    
    def list_staged(self) -> List[Dict[str, Any]]:
        """List all staged files with metadata."""
        staged_files = []
        
        if not self.staging_dir.exists():
            return staged_files
        
        for staged_file in self.staging_dir.glob("*.jira-staged"):
            try:
                content = json.loads(staged_file.read_text())
                security_info = content.get("_security_warning", {})
                
                file_info = {
                    "filename": staged_file.name,
                    "path": staged_file,
                    "issue_type": security_info.get("issue_type", "unknown"),
                    "template_used": security_info.get("template_used", "unknown"),
                    "staged_timestamp": security_info.get("staged_timestamp"),
                    "contains_sensitive_data": security_info.get("contains_sensitive_data", True),
                    "sensitivity_indicators": security_info.get("sensitivity_indicators", []),
                    "file_size": staged_file.stat().st_size,
                    "modified": datetime.fromtimestamp(staged_file.stat().st_mtime)
                }
                
                # Extract issue summary if available
                jira_payload = content.get("_jira_payload", {})
                if isinstance(jira_payload, dict) and "fields" in jira_payload:
                    file_info["summary"] = jira_payload["fields"].get("summary", "No summary")
                else:
                    file_info["summary"] = "No summary"
                
                staged_files.append(file_info)
                
            except Exception as e:
                # Skip files that can't be parsed
                console.print(f"⚠️  Warning: Could not parse {staged_file.name}: {e}")
                continue
        
        return sorted(staged_files, key=lambda x: x["modified"], reverse=True)
    
    def load_staged_file(self, filename: str) -> Optional[Dict[str, Any]]:
        """Load a staged file and return the Jira payload."""
        stage_file = self.staging_dir / filename
        
        if not stage_file.exists():
            raise StagingError(f"Staged file not found: {filename}")
        
        try:
            content = json.loads(stage_file.read_text())
            return content.get("_jira_payload")
        except Exception as e:
            raise StagingError(f"Failed to load staged file {filename}: {e}")
    
    def remove_staged_file(self, filename: str) -> bool:
        """Remove a staged file."""
        stage_file = self.staging_dir / filename
        
        if not stage_file.exists():
            return False
        
        try:
            stage_file.unlink()
            console.print(f"🗑️  Removed staged file: {filename}")
            return True
        except Exception as e:
            console.print(f"❌ Failed to remove {filename}: {e}")
            return False
    
    def clean_old_files(self, days_old: int = 7) -> int:
        """Clean up old staged files."""
        if not self.staging_dir.exists():
            return 0
        
        cutoff_time = datetime.now().timestamp() - (days_old * 86400)
        removed_count = 0
        
        for staged_file in self.staging_dir.glob("*.jira-staged"):
            try:
                if staged_file.stat().st_mtime < cutoff_time:
                    staged_file.unlink()
                    removed_count += 1
            except Exception:
                continue
        
        if removed_count > 0:
            console.print(f"🧹 Cleaned up {removed_count} old staged files (older than {days_old} days)")
        
        return removed_count
    
    def validate_staging_security(self) -> Dict[str, Any]:
        """Validate staging directory security."""
        validation_results = {
            "secure": True,
            "warnings": [],
            "errors": [],
            "recommendations": []
        }
        
        # Check directory exists
        if not self.staging_dir.exists():
            validation_results["warnings"].append("Staging directory doesn't exist")
            return validation_results
        
        # Check directory permissions (Unix only)
        if os.name != 'nt':
            dir_mode = oct(self.staging_dir.stat().st_mode)[-3:]
            if dir_mode != '700':
                validation_results["errors"].append(f"Directory permissions are {dir_mode}, should be 700")
                validation_results["secure"] = False
        
        # Check gitignore protection
        gitignore_protected = self._check_gitignore_protection()
        if not gitignore_protected:
            validation_results["warnings"].append("Staging directory may not be protected by .gitignore")
        
        # Check for old files
        old_files = []
        if self.staging_dir.exists():
            cutoff_time = datetime.now().timestamp() - (7 * 86400)  # 7 days
            for staged_file in self.staging_dir.glob("*.jira-staged"):
                if staged_file.stat().st_mtime < cutoff_time:
                    old_files.append(staged_file.name)
        
        if old_files:
            validation_results["recommendations"].append(
                f"Found {len(old_files)} old staged files. Consider cleaning up with: "
                "python -m jira_tools staging clean"
            )
        
        return validation_results
    
    def _check_gitignore_protection(self) -> bool:
        """Check if staging directory is protected by gitignore."""
        current_dir = Path.cwd()
        
        for search_dir in [current_dir] + list(current_dir.parents):
            gitignore = search_dir / ".gitignore"
            if gitignore.exists():
                content = gitignore.read_text()
                if str(self.staging_dir) in content or ".jira-staging/" in content:
                    return True
        
        return False


# Global staging instance
local_staging = LocalStaging()
