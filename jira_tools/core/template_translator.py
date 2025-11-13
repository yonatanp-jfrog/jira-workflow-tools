"""
Template Translator - Converts human-readable template values to Jira API format.

This module handles the translation between user-friendly template values
and the cryptic field IDs required by the Jira API.
"""

from typing import Dict, Any, Optional
import json


class TemplateTranslator:
    """Translates human-readable template values to Jira API format."""
    
    # Field mapping from human-readable names to Jira field IDs
    FIELD_MAPPINGS = {
        # Core fields
        'project': 'project',
        'summary': 'summary', 
        'description': 'description',
        'issue_type': 'issuetype',
        'priority': 'priority',
        'parent': 'parent',
        
        # Custom fields
        'team': 'customfield_10129',
        'product_backlog': 'customfield_10119',
        'product_manager': 'customfield_10044',
        'commitment_level': 'customfield_10450',
        'area': 'customfield_10167',
        'commitment_reason': 'customfield_10508',
        'product_priority': 'customfield_10327',
        'ux_designer': 'customfield_10200',
        'technical_writer': 'customfield_10201',
        'architect': 'customfield_10202',
    }
    
    # Project mappings
    PROJECT_MAPPINGS = {
        'RTDEV': '10129',
        'APP': '10246',
    }
    
    # Issue type mappings
    ISSUE_TYPE_MAPPINGS = {
        'epic': '10000',
        'story': '10001', 
        'task': '10003',
        'bug': '10004',
    }
    
    # Team mappings
    TEAM_MAPPINGS = {
        'dev-artifactory-lifecycle': '10145',
        'app-core': '12980',
        'security-team': '10146',
        'platform-team': '10147',
        'api-team': '10148',
        'devops-team': '10149',
        'qa-team': '10150',
        'performance-team': '10151',
        'data-team': '10152',
        'integration-team': '10153',
        'support-team': '10154',
        'research-team': '10155',
    }
    
    # Priority mappings
    PRIORITY_MAPPINGS = {
        'Blocker': '1',
        'Highest': '2', 
        'Critical': '3',
        'High': '4',
        'Normal': '5',
        'Minor': '6',
        'Low': '7',
        'Trivial': '8',
    }
    
    # Commitment level mappings
    COMMITMENT_LEVEL_MAPPINGS = {
        'Hard Commitment': '12345',
        'Soft Commitment': '12346',
        'KTLO': '12347',
    }
    
    # Area mappings
    AREA_MAPPINGS = {
        'Features & Innovation': '23456',
        'Enablers & Tech Debt': '23457',
        'KTLO': '23458',
    }
    
    # Commitment reason mappings
    COMMITMENT_REASON_MAPPINGS = {
        'Roadmap': '34567',
        'Customer Commitment': '34568',
        'Security': '34569',
    }
    
    # Product priority mappings
    PRODUCT_PRIORITY_MAPPINGS = {
        'P0': '45678',
        'P1': '45679',
        'P2': '45680',
        'P3': '45681',
        'P4': '45682',
    }
    
    def translate_template(self, rendered_template: str) -> str:
        """
        Translate a rendered template from human-readable format to Jira API format.
        
        Args:
            rendered_template: JSON string with human-readable field names and values
            
        Returns:
            JSON string formatted for Jira API
        """
        try:
            # Parse the human-readable template
            template_data = json.loads(rendered_template)
            
            # Extract fields
            if 'fields' not in template_data:
                raise ValueError("Template must have 'fields' section")
                
            human_readable_fields = template_data['fields']
            jira_fields = {}
            
            # Translate each field
            for field_name, field_value in human_readable_fields.items():
                jira_field_name = self.FIELD_MAPPINGS.get(field_name, field_name)
                jira_field_value = self._translate_field_value(field_name, field_value)
                
                # Only include fields that have valid values (not None or "None")
                if jira_field_value is not None and jira_field_value != "None":
                    jira_fields[jira_field_name] = jira_field_value
            
            # Build final Jira API payload
            jira_payload = {
                'fields': jira_fields
            }
            
            return json.dumps(jira_payload, indent=2)
            
        except json.JSONDecodeError as e:
            raise ValueError(f"Invalid JSON in template: {e}")
        except Exception as e:
            raise ValueError(f"Translation error: {e}")
    
    def _translate_field_value(self, field_name: str, field_value: Any) -> Any:
        """Translate a specific field value to Jira format."""
        
        # Skip None values and "None" strings (from template rendering)
        if field_value is None or field_value == "None":
            return None
            
        # Project field
        if field_name == 'project':
            project_id = self.PROJECT_MAPPINGS.get(field_value)
            if project_id:
                return {'id': project_id}
            return field_value
            
        # Issue type field  
        elif field_name == 'issue_type':
            issue_type_id = self.ISSUE_TYPE_MAPPINGS.get(field_value)
            if issue_type_id:
                return {'id': issue_type_id}
            return field_value
            
        # Priority field - handle both "Normal" and "4 - Normal" formats
        elif field_name == 'priority':
            # First try direct mapping
            priority_id = self.PRIORITY_MAPPINGS.get(field_value)
            if priority_id:
                return {'id': priority_id}
            
            # Try extracting just the name part (e.g., "4 - Normal" -> "Normal")
            if ' - ' in str(field_value):
                priority_name = str(field_value).split(' - ', 1)[1]
                priority_id = self.PRIORITY_MAPPINGS.get(priority_name)
                if priority_id:
                    return {'id': priority_id}
            
            # If no mapping found, return the original value
            return {'id': str(field_value)}
            
        # Team field
        elif field_name == 'team':
            team_id = self.TEAM_MAPPINGS.get(field_value)
            if team_id:
                return [{'id': team_id}]
            return field_value
            
        # Product backlog (array field)
        elif field_name == 'product_backlog':
            return [field_value]
            
        # User fields (account ID fields)
        elif field_name in ['product_manager', 'ux_designer', 'technical_writer', 'architect']:
            return {'accountId': field_value}
            
        # Select fields (commitment level, area, commitment reason, product priority)
        elif field_name == 'commitment_level':
            commitment_id = self.COMMITMENT_LEVEL_MAPPINGS.get(field_value)
            if commitment_id:
                return {'id': commitment_id}
            return field_value
            
        elif field_name == 'area':
            # Handle HTML entity decoding (& becomes &amp; in templates)
            import html
            decoded_value = html.unescape(str(field_value)) if field_value else field_value
            area_id = self.AREA_MAPPINGS.get(decoded_value)
            if area_id:
                return {'id': area_id}
            return field_value
            
        elif field_name == 'commitment_reason':
            reason_id = self.COMMITMENT_REASON_MAPPINGS.get(field_value)
            if reason_id:
                return {'id': reason_id}
            return field_value
            
        elif field_name == 'product_priority':
            priority_id = self.PRODUCT_PRIORITY_MAPPINGS.get(field_value)
            if priority_id:
                return {'id': priority_id}
            return field_value
            
        # Parent field (epic link)
        elif field_name == 'parent':
            return {'key': field_value}
            
        # Default: return as-is
        else:
            return field_value


# Global translator instance
template_translator = TemplateTranslator()
