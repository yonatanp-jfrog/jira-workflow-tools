"""
Jira Field Mappings and Value Mappings

This module contains comprehensive mappings for Jira custom fields and their values,
extracted from the legacy system to maintain full compatibility.
"""

from typing import Dict, Any, Optional
from dataclasses import dataclass


@dataclass
class JiraFieldMapping:
    """Represents a Jira field mapping with metadata."""
    field_id: str
    display_name: str
    field_type: str
    required: bool = False
    description: str = ""


class JiraFieldMappings:
    """
    Centralized Jira field mappings and value mappings.
    
    This class provides access to all Jira custom field IDs and their corresponding
    value mappings, ensuring consistency across the application.
    """
    
    # ============================================================================
    # JIRA CUSTOM FIELD MAPPINGS
    # ============================================================================
    
    FIELD_MAPPINGS = {
        'teams': JiraFieldMapping(
            field_id='customfield_10129',
            display_name='Teams',
            field_type='array',
            required=False,
            description='Team assignment for the issue'
        ),
        'product_backlog': JiraFieldMapping(
            field_id='customfield_10119', 
            display_name='Product Backlog',
            field_type='array',
            required=False,
            description='Product backlog classification'
        ),
        'product_manager': JiraFieldMapping(
            field_id='customfield_10044',
            display_name='Product Manager',
            field_type='user',
            required=False,
            description='Assigned product manager'
        ),
        'commitment_reason': JiraFieldMapping(
            field_id='customfield_10508',
            display_name='Commitment Reason',
            field_type='select',
            required=False,
            description='Reason for commitment level'
        ),
        'area': JiraFieldMapping(
            field_id='customfield_10167',
            display_name='Area',
            field_type='select',
            required=True,
            description='Work area classification (Features, Enablers, KTLO)'
        ),
        'commitment_level': JiraFieldMapping(
            field_id='customfield_10450',
            display_name='Commitment Level',
            field_type='select',
            required=False,
            description='Level of commitment (Hard, Soft, KTLO)'
        ),
        'product_priority': JiraFieldMapping(
            field_id='customfield_10327',
            display_name='Product Priority',
            field_type='select',
            required=False,
            description='Product priority ranking (P0-P4)'
        )
    }
    
    # ============================================================================
    # FIELD VALUE MAPPINGS (Display Name → Jira ID)
    # ============================================================================
    
    PRIORITY_MAPPINGS = {
        '1 - Blocker': '10000',
        '1 - Highest': '10001', 
        '2 - Critical': '10001',
        '2 - High': '10002',
        '3 - High': '10002', 
        '4 - Normal': '10003',
        '5 - Minor': '10004',
        '5 - Low': '10004',
        '6 - Trivial': '10005'
    }
    
    COMMITMENT_LEVEL_MAPPINGS = {
        'Hard Commitment': '11277',
        'Soft Commitment': '11278',
        'KTLO': '11279'
    }
    
    AREA_MAPPINGS = {
        'Features & Innovation': '10312',
        'Enablers & Tech Debt': '10311', 
        'KTLO': '10313'
    }
    
    COMMITMENT_REASON_MAPPINGS = {
        'Roadmap': '11490',
        'Customer Commitment': '11491',
        'Security': '11492'
    }
    
    PRODUCT_PRIORITY_MAPPINGS = {
        'P0': '11498',
        'P1': '11499',
        'P2': '11500', 
        'P3': '11501',
        'P4': '11502'
    }
    
    # ============================================================================
    # PROJECT-SPECIFIC DEFAULTS
    # ============================================================================
    
    PROJECT_DEFAULTS = {
        'RTDEV': {
            'team': 'dev-artifactory-lifecycle',
            'team_id': '10145',
            'project_id': '10129',
            'default_area': 'Features & Innovation',
            'default_commitment_reason': 'Roadmap'
        },
        'APP': {
            'team': 'App Core',
            'team_id': '12980',
            'project_id': '10246',
            'default_area': 'Features & Innovation', 
            'default_commitment_reason': 'Roadmap'
        }
    }
    
    # ============================================================================
    # UTILITY METHODS
    # ============================================================================
    
    @classmethod
    def get_field_id(cls, field_name: str) -> str:
        """Get Jira field ID for a field name."""
        if field_name not in cls.FIELD_MAPPINGS:
            raise ValueError(f"Unknown field: {field_name}")
        return cls.FIELD_MAPPINGS[field_name].field_id
    
    @classmethod
    def get_field_mapping(cls, field_name: str) -> JiraFieldMapping:
        """Get complete field mapping for a field name."""
        if field_name not in cls.FIELD_MAPPINGS:
            raise ValueError(f"Unknown field: {field_name}")
        return cls.FIELD_MAPPINGS[field_name]
    
    @classmethod
    def get_priority_id(cls, priority_name: str) -> str:
        """Get Jira priority ID for a priority name."""
        if priority_name not in cls.PRIORITY_MAPPINGS:
            raise ValueError(f"Unknown priority: {priority_name}")
        return cls.PRIORITY_MAPPINGS[priority_name]
    
    @classmethod
    def get_commitment_level_id(cls, commitment_level: str) -> str:
        """Get Jira commitment level ID.""" 
        if commitment_level not in cls.COMMITMENT_LEVEL_MAPPINGS:
            raise ValueError(f"Unknown commitment level: {commitment_level}")
        return cls.COMMITMENT_LEVEL_MAPPINGS[commitment_level]
    
    @classmethod
    def get_area_id(cls, area: str) -> str:
        """Get Jira area ID."""
        if area not in cls.AREA_MAPPINGS:
            raise ValueError(f"Unknown area: {area}")
        return cls.AREA_MAPPINGS[area]
    
    @classmethod
    def get_commitment_reason_id(cls, reason: str) -> str:
        """Get Jira commitment reason ID."""
        if reason not in cls.COMMITMENT_REASON_MAPPINGS:
            raise ValueError(f"Unknown commitment reason: {reason}")
        return cls.COMMITMENT_REASON_MAPPINGS[reason]
    
    @classmethod
    def get_product_priority_id(cls, priority: str) -> str:
        """Get Jira product priority ID."""
        if priority not in cls.PRODUCT_PRIORITY_MAPPINGS:
            raise ValueError(f"Unknown product priority: {priority}")
        return cls.PRODUCT_PRIORITY_MAPPINGS[priority]
    
    @classmethod
    def get_project_defaults(cls, project_key: str) -> Dict[str, Any]:
        """Get default values for a project."""
        if project_key not in cls.PROJECT_DEFAULTS:
            raise ValueError(f"Unknown project: {project_key}")
        return cls.PROJECT_DEFAULTS[project_key]
    
    @classmethod
    def get_available_choices(cls) -> Dict[str, list]:
        """Get all available choices for CLI options."""
        return {
            'priorities': list(cls.PRIORITY_MAPPINGS.keys()),
            'commitment_levels': list(cls.COMMITMENT_LEVEL_MAPPINGS.keys()),
            'areas': list(cls.AREA_MAPPINGS.keys()),
            'commitment_reasons': list(cls.COMMITMENT_REASON_MAPPINGS.keys()),
            'product_priorities': list(cls.PRODUCT_PRIORITY_MAPPINGS.keys()),
            'projects': list(cls.PROJECT_DEFAULTS.keys())
        }
    
    @classmethod
    def build_jira_payload_field(cls, field_name: str, value: Any, project_key: str = None) -> Dict[str, Any]:
        """
        Build a Jira payload field based on field type and value.
        
        Args:
            field_name: The field name (e.g., 'teams', 'commitment_level')
            value: The value to set
            project_key: Project key for context-specific handling
            
        Returns:
            Dictionary with properly formatted field for Jira payload
        """
        if field_name not in cls.FIELD_MAPPINGS:
            raise ValueError(f"Unknown field: {field_name}")
            
        mapping = cls.FIELD_MAPPINGS[field_name]
        field_id = mapping.field_id
        field_type = mapping.field_type
        
        if field_type == 'select':
            # Handle select fields (commitment_level, area, etc.)
            if field_name == 'commitment_level':
                return {field_id: {"id": cls.get_commitment_level_id(value)}}
            elif field_name == 'area':
                return {field_id: {"id": cls.get_area_id(value)}}
            elif field_name == 'commitment_reason':
                return {field_id: {"id": cls.get_commitment_reason_id(value)}}
            elif field_name == 'product_priority':
                return {field_id: {"id": cls.get_product_priority_id(value)}}
        
        elif field_type == 'array':
            # Handle array fields (teams, product_backlog)
            if field_name == 'teams':
                # Teams need special handling based on project
                if project_key and value:
                    project_defaults = cls.get_project_defaults(project_key)
                    if value == project_defaults['team']:
                        return {field_id: [{"id": project_defaults['team_id']}]}
                    else:
                        # Fallback - use project default team ID
                        return {field_id: [{"id": project_defaults['team_id']}]}
            elif field_name == 'product_backlog':
                return {field_id: [value] if isinstance(value, str) else value}
        
        elif field_type == 'user':
            # Handle user fields (product_manager)
            if field_name == 'product_manager':
                return {field_id: {"accountId": value}}
        
        # Fallback for unknown field types
        return {field_id: value}
    
    @classmethod
    def validate_field_value(cls, field_name: str, value: Any) -> bool:
        """Validate that a field value is acceptable."""
        if field_name not in cls.FIELD_MAPPINGS:
            return False
            
        if field_name == 'commitment_level':
            return value in cls.COMMITMENT_LEVEL_MAPPINGS
        elif field_name == 'area':
            return value in cls.AREA_MAPPINGS
        elif field_name == 'commitment_reason':
            return value in cls.COMMITMENT_REASON_MAPPINGS
        elif field_name == 'product_priority':
            return value in cls.PRODUCT_PRIORITY_MAPPINGS
        elif field_name == 'teams':
            # Teams validation would need project context
            return isinstance(value, str) and len(value) > 0
        elif field_name == 'product_backlog':
            return isinstance(value, str) and len(value) > 0
        elif field_name == 'product_manager':
            # Basic validation for account ID format
            return isinstance(value, str) and len(value) > 0
        
        return True


# Create a global instance for easy access
jira_fields = JiraFieldMappings()
