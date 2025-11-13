"""
Template engine for Jira issue creation with Jinja2 support.

This module provides a flexible, team-friendly template system for creating
Jira issues with customizable fields, validation, and context-aware selection.

Features:
- Jinja2-powered templates with full programming capabilities
- Context-aware template selection (project, issue type, etc.)
- Template validation and error reporting
- User customization support (local overrides)
- Built-in templates for common JFrog workflows
"""

import json
import yaml
from pathlib import Path
from typing import Dict, Any, List, Optional, Union
from jinja2 import Environment, FileSystemLoader, Template, TemplateError, select_autoescape

from ..utils.exceptions import TemplateError as CustomTemplateError, ValidationError
from .field_mappings import jira_fields
from .template_translator import template_translator


class TemplateManager:
    """
    Manages Jira issue templates with Jinja2 support.
    
    Provides template loading, rendering, validation, and context-aware selection
    for team-friendly Jira issue creation.
    """
    
    def __init__(self, template_dir: Union[str, Path] = None):
        """
        Initialize template manager.
        
        Args:
            template_dir: Directory containing templates. If None, uses default.
        """
        self.template_dir = Path(template_dir) if template_dir else self._get_default_template_dir()
        self.template_dir.mkdir(parents=True, exist_ok=True)
        
        # Set up Jinja2 environment
        self.env = Environment(
            loader=FileSystemLoader([
                str(self.template_dir)
            ]),
            autoescape=select_autoescape(['html', 'xml']),
            trim_blocks=True,
            lstrip_blocks=True
        )
        
        # Add custom filters
        self.env.filters['to_json'] = json.dumps
        self.env.filters['from_yaml'] = yaml.safe_load
        
        # Template metadata cache
        self._template_cache = {}
    
    def _get_default_template_dir(self) -> Path:
        """Get default template directory (project root/templates)."""
        current_file = Path(__file__)
        project_root = current_file.parent.parent.parent
        return project_root / "templates"
    
    def _get_builtin_template_dir(self) -> Path:
        """Get built-in template directory."""
        return Path(__file__).parent / "builtin_templates"
    
    def list_templates(self, issue_type: Optional[str] = None) -> List[Dict[str, Any]]:
        """
        List available templates.
        
        Args:
            issue_type: Filter by issue type (epic, story, task, bug)
            
        Returns:
            List of template metadata dictionaries
        """
        templates = []
        
        # Search only user templates (built-in templates have been moved to regular templates)
        for search_dir in [self.template_dir]:
            if not search_dir.exists():
                continue
                
            for template_file in search_dir.rglob("*.j2"):
                try:
                    metadata = self._get_template_metadata(template_file, search_dir)
                    
                    # Filter by issue type if specified
                    if issue_type and metadata.get('issue_type') != issue_type:
                        continue
                    
                    templates.append(metadata)
                except Exception as e:
                    # Skip invalid templates but log the issue
                    print(f"Warning: Skipping invalid template {template_file}: {e}")
        
        return sorted(templates, key=lambda t: (
            t['project'], 
            t['issue_type'], 
            t['name']
        ))
    
    def _get_template_metadata(self, template_file: Path, base_dir: Path) -> Dict[str, Any]:
        """Extract metadata from template file (flat structure with filename as template name)."""
        relative_path = template_file.relative_to(base_dir)
        
        # Template name is the filename without .j2 extension
        filename_template_name = template_file.stem
        
        # Extract metadata from template header
        header_metadata = self._extract_template_metadata(template_file)
        
        # Get fields from header - use filename as template name if not specified in header
        template_name = header_metadata.get('name', filename_template_name)
        project = header_metadata.get('project')
        issue_type = header_metadata.get('issue_type')
        team = header_metadata.get('team', 'optional')
        description = header_metadata.get('description', 'No description available')
        
        # Validate mandatory fields from header metadata
        if not project:
            raise ValueError(f"Template {template_file} missing mandatory 'project' field in header")
        if not issue_type:
            raise ValueError(f"Template {template_file} missing mandatory 'issue_type' field in header")
        
        # Ensure template name matches filename (consistency requirement)
        if template_name != filename_template_name:
            print(f"Warning: Template {template_file} has name '{template_name}' but filename suggests '{filename_template_name}'. Using filename.")
            template_name = filename_template_name
        
        return {
            'name': template_name,
            'project': project,
            'issue_type': issue_type,
            'team': team if team != 'optional' else None,
            'description': description,
            'path': str(relative_path),
            'full_path': str(template_file),
            'is_builtin': False,  # All templates are now user templates in flat structure
            'size': template_file.stat().st_size
        }
    
    def _extract_template_metadata(self, template_file: Path) -> Dict[str, str]:
        """Extract metadata from template header comment."""
        try:
            content = template_file.read_text()
            lines = content.split('\n')
            
            metadata = {}
            in_header = False
            
            for line in lines[:15]:  # Check first 15 lines for header
                line = line.strip()
                
                # Start of header comment
                if line.startswith('{#'):
                    in_header = True
                    continue
                
                # End of header comment  
                if line.endswith('#}'):
                    break
                    
                # Parse metadata lines
                if in_header and ':' in line:
                    key, value = line.split(':', 1)
                    metadata[key.strip()] = value.strip()
            
            return metadata
        except Exception:
            return {}
    
    def _extract_template_description(self, template_file: Path) -> str:
        """Extract description from template header - backward compatibility."""
        metadata = self._extract_template_metadata(template_file)
        return metadata.get('description', 'No description available')
    
    def select_template(self, issue_type: str, project_key: Optional[str] = None, 
                       template_name: Optional[str] = None, context: Optional[str] = None) -> Template:
        """
        Select appropriate template based on criteria.
        
        Args:
            issue_type: Type of issue (epic, story, task, bug)
            project_key: Project key for project-specific templates
            template_name: Specific template name to use
            context: Additional context (feature, bugfix, etc.)
            
        Returns:
            Jinja2 Template object
            
        Raises:
            CustomTemplateError: If no suitable template found
        """
        # Priority order for template selection:
        # 1. Explicit template name
        # 2. Project + issue type + context
        # 3. Project + issue type
        # 4. Issue type + context
        # 5. Issue type (base template)
        
        template_candidates = []
        
        if template_name:
            # Explicit template requested
            template_candidates.extend([
                f"{issue_type}/{template_name}.j2",
                f"{template_name}.j2"
            ])
        
        if project_key:
            # Project-specific templates
            template_candidates.extend([
                f"{project_key}/{issue_type}/{context}.j2" if context else None,
                f"{project_key}/{issue_type}/base.j2",
                f"{issue_type}/{project_key}_{context}.j2" if context else None,
                f"{issue_type}/{project_key}.j2"
            ])
        
        if context:
            # Context-specific templates
            template_candidates.append(f"{issue_type}/{context}.j2")
        
        # Base templates
        template_candidates.extend([
            f"{issue_type}/base.j2",
            f"{issue_type}/default.j2"
        ])
        
        # Remove None values
        template_candidates = [t for t in template_candidates if t]
        
        # Try to load templates in priority order
        for candidate in template_candidates:
            try:
                template = self.env.get_template(candidate)
                return template
            except TemplateError:
                continue
        
        # If no template found, raise error with helpful message
        available_templates = [t['path'] for t in self.list_templates(issue_type)]
        raise CustomTemplateError(
            f"No template found for issue type '{issue_type}'. "
            f"Available templates: {', '.join(available_templates) if available_templates else 'None'}"
        )
    
    def render_template(self, template: Template, context: Dict[str, Any]) -> str:
        """
        Render template with given context and translate to Jira API format.
        
        Args:
            template: Jinja2 template to render
            context: Template context variables
            
        Returns:
            Rendered template translated to Jira API format
            
        Raises:
            CustomTemplateError: If rendering fails
            ValidationError: If rendered content is invalid
        """
        try:
            # First render the template with human-readable values
            human_readable_rendered = template.render(**context)
            
            # Validate rendered content as JSON
            self.validate_rendered_content(human_readable_rendered)
            
            # Translate from human-readable to Jira API format
            jira_api_rendered = template_translator.translate_template(human_readable_rendered)
            
            return jira_api_rendered
            
        except TemplateError as e:
            raise CustomTemplateError(f"Template rendering failed: {e}")
        except Exception as e:
            raise CustomTemplateError(f"Unexpected error during rendering: {e}")
    
    def validate_rendered_content(self, content: str) -> None:
        """
        Validate rendered template content.
        
        Args:
            content: Rendered template content
            
        Raises:
            ValidationError: If content is invalid
        """
        if not content or not content.strip():
            raise ValidationError("Rendered template is empty")
        
        # Try to parse as JSON (Jira API format)
        try:
            data = json.loads(content)
            
            # Basic Jira issue structure validation
            if not isinstance(data, dict):
                raise ValidationError("Rendered content must be a JSON object")
            
            if 'fields' not in data:
                raise ValidationError("Rendered content must have 'fields' key")
            
            fields = data['fields']
            if not isinstance(fields, dict):
                raise ValidationError("'fields' must be an object")
            
            # Check required fields for human-readable format
            required_fields = ['project', 'summary', 'issue_type']
            missing_fields = [field for field in required_fields if field not in fields]
            
            if missing_fields:
                raise ValidationError(f"Missing required fields: {', '.join(missing_fields)}")
            
            # Validate field formats for human-readable format
            # Human-readable format uses strings, not objects
            if 'project' in fields and not isinstance(fields['project'], str):
                raise ValidationError("'project' field must be a string in human-readable format")
            
            if 'issue_type' in fields and not isinstance(fields['issue_type'], str):
                raise ValidationError("'issue_type' field must be a string in human-readable format")
                
        except json.JSONDecodeError as e:
            raise ValidationError(f"Rendered content is not valid JSON: {e}")
    
    def create_template(self, issue_type: str, template_name: str, content: str, 
                       description: Optional[str] = None) -> Path:
        """
        Create a new template file.
        
        Args:
            issue_type: Issue type (epic, story, task, bug)
            template_name: Name for the template
            content: Template content
            description: Optional description
            
        Returns:
            Path to created template file
        """
        # Create directory if needed
        type_dir = self.template_dir / issue_type
        type_dir.mkdir(parents=True, exist_ok=True)
        
        # Create template file
        template_file = type_dir / f"{template_name}.j2"
        
        # Add description header if provided
        if description:
            header = f"{{# description: {description} #}}\n"
            content = header + content
        
        template_file.write_text(content)
        
        # Clear cache
        self._template_cache.clear()
        
        return template_file
    
    def validate_template(self, template_path: Union[str, Path]) -> Dict[str, Any]:
        """
        Validate a template file.
        
        Args:
            template_path: Path to template file
            
        Returns:
            Validation result dictionary
        """
        template_path = Path(template_path)
        result = {
            'valid': False,
            'errors': [],
            'warnings': [],
            'metadata': {}
        }
        
        try:
            # Check file exists
            if not template_path.exists():
                result['errors'].append(f"Template file not found: {template_path}")
                return result
            
            # Try to load template
            try:
                template_content = template_path.read_text()
                template = self.env.from_string(template_content)
                
                # Try to render with minimal context
                test_context = {
                    'project': {'id': '12345', 'key': 'TEST'},
                    'epic': {'name': 'Test Epic', 'description': 'Test Description', 'priority': '4 - Normal'},
                    'story': {'name': 'Test Story', 'description': 'Test Description', 'priority': '4 - Normal'},
                    'task': {'name': 'Test Task', 'description': 'Test Description', 'priority': '4 - Normal'},
                    'bug': {'name': 'Test Bug', 'description': 'Test Description', 'priority': '4 - Normal'},
                    'team': {'id': '12345', 'name': 'Test Team'},
                    'user': {'account_id': 'test-account-id'},
                        'priorities': jira_fields.PRIORITY_MAPPINGS,
                        'issue_types': {'epic': '10000', 'story': '10001', 'task': '10003', 'bug': '10004'},
                        'commitment_levels': jira_fields.COMMITMENT_LEVEL_MAPPINGS,
                        'areas': jira_fields.AREA_MAPPINGS,
                        'commitment_reasons': jira_fields.COMMITMENT_REASON_MAPPINGS,
                        'product_priorities': jira_fields.PRODUCT_PRIORITY_MAPPINGS,
                        'field_ids': {name: mapping.field_id for name, mapping in jira_fields.FIELD_MAPPINGS.items()}
                }
                
                rendered = template.render(**test_context)
                
                # Validate rendered content
                self.validate_rendered_content(rendered)
                
                result['valid'] = True
                result['metadata'] = self._get_template_metadata(template_path, template_path.parent)
                
            except TemplateError as e:
                result['errors'].append(f"Template syntax error: {e}")
            except ValidationError as e:
                result['errors'].append(f"Template validation error: {e}")
            except Exception as e:
                result['errors'].append(f"Unexpected error: {e}")
        
        except Exception as e:
            result['errors'].append(f"Failed to validate template: {e}")
        
        return result
    
    def describe_template(self, template_name: str, issue_type: str = None) -> Dict[str, Any]:
        """
        Get detailed, user-friendly description of what a template does.
        
        Args:
            template_name: Name of the template to describe
            issue_type: Optional issue type to narrow search
            
        Returns:
            Dictionary with detailed template information
        """
        template_path = self._find_template_path(template_name, issue_type)
        if not template_path:
            raise CustomTemplateError(f"Template '{template_name}' not found")
            
        # Get basic template info
        template_dir = template_path.parent.parent if template_path.parent.name != 'builtin_templates' else self._get_builtin_template_dir()
        metadata = self._get_template_metadata(template_path, template_dir)
        
        # Read template content for analysis
        template_content = template_path.read_text()
        template = self.env.from_string(template_content)
        
        # Create comprehensive test context to see what fields get set
        test_context = self._build_comprehensive_test_context()
        
        try:
            # Render with comprehensive context to see all possible fields
            human_readable_rendered = template.render(**test_context)
            
            # Translate to Jira API format for analysis
            jira_api_rendered = template_translator.translate_template(human_readable_rendered)
            rendered_json = json.loads(jira_api_rendered)
            
            # Analyze what fields are set
            fields_analysis = self._analyze_template_fields(rendered_json, template_content)
            
            return {
                'name': metadata['name'],
                'type': metadata.get('issue_type', 'unknown'), 
                'description': metadata['description'],
                'source': 'Custom' if not metadata.get('is_builtin', False) else 'Built-in',
                'path': str(template_path),
                'summary': self._generate_template_summary(metadata, fields_analysis),
                'fields': fields_analysis,
                'usage_examples': self._generate_usage_examples(metadata['name'], metadata.get('issue_type', 'unknown'))
            }
            
        except Exception as e:
            return {
                'name': metadata['name'],
                'type': metadata.get('issue_type', 'unknown'),
                'description': metadata['description'],
                'source': 'Custom' if not metadata.get('is_builtin', False) else 'Built-in',
                'path': str(template_path),
                'error': f"Could not analyze template: {e}",
                'fields': {},
                'usage_examples': []
            }
    
    def _find_template_by_name(self, template_name: str) -> Optional[Path]:
        """Find template by unique name (searches all templates and matches by name metadata)."""
        try:
            templates = self.list_templates()
            for template in templates:
                if template['name'] == template_name:
                    return Path(template['full_path'])
            return None
        except Exception:
            return None
    
    def _find_template_path(self, template_name: str, issue_type: str = None) -> Optional[Path]:
        """Find template path - search in flat template directory by filename."""
        # Primary: Search by unique template name in flat structure
        template_path = self._find_template_by_name(template_name)
        if template_path:
            return template_path
            
        # Fallback: Direct filename search in flat directory
        template_file = self.template_dir / f"{template_name}.j2"
        if template_file.exists():
            return template_file
                    
        return None
    
    def _build_comprehensive_test_context(self) -> Dict[str, Any]:
        """Build comprehensive context for template analysis."""
        return {
            'project': {'id': '10129', 'key': 'RTDEV'},
            # New generic issue context (works for all issue types)
            'issue': {
                'title': 'Sample Issue Title',
                'description': 'Sample description',
                'priority': '4 - Normal',
                'commitment_level': 'Hard Commitment',
                'area': 'Features & Innovation',
                'commitment_reason': 'Roadmap',
                'product_backlog': 'Q4-25-Backlog',
                'product_priority': 'P1',
                'parent': 'RTDEV-12345'
            },
            # Legacy epic context for backwards compatibility
            'epic': {
                'name': 'Sample Epic Name', 
                'description': 'Sample description',
                'priority': '4 - Normal',
                'commitment_level': 'Hard Commitment',
                'area': 'Features & Innovation',
                'commitment_reason': 'Roadmap',
                'product_backlog': 'Q4-25-Backlog',
                'product_priority': 'P1',
                'parent': 'RTDEV-12345'
            },
            'team': {'id': '10145', 'name': 'Sample Team'},
            'user': {'account_id': 'sample-account-id'},
            'priorities': jira_fields.PRIORITY_MAPPINGS,
            'issue_types': {'epic': '10000', 'story': '10001', 'task': '10003', 'bug': '10004'},
            'commitment_levels': jira_fields.COMMITMENT_LEVEL_MAPPINGS,
            'areas': jira_fields.AREA_MAPPINGS,
            'commitment_reasons': jira_fields.COMMITMENT_REASON_MAPPINGS,
            'product_priorities': jira_fields.PRODUCT_PRIORITY_MAPPINGS,
            'field_ids': {name: mapping.field_id for name, mapping in jira_fields.FIELD_MAPPINGS.items()}
        }
    
    def _analyze_template_fields(self, rendered_json: Dict[str, Any], template_content: str) -> Dict[str, Any]:
        """Analyze what fields a template sets and their values."""
        fields = rendered_json.get('fields', {})
        analysis = {
            'always_set': [],
            'conditional': [],
            'user_provided': [],
            'defaults_used': []
        }
        
        # Map field IDs to human names
        field_mappings = {
            'customfield_10129': 'Team Assignment',
            'customfield_10119': 'Product Backlog', 
            'customfield_10044': 'Product Manager',
            'customfield_10508': 'Commitment Reason',
            'customfield_10167': 'Area',
            'customfield_10450': 'Commitment Level',
            'customfield_10327': 'Product Priority'
        }
        
        reverse_priority_map = {v: k for k, v in jira_fields.PRIORITY_MAPPINGS.items()}
        reverse_commitment_map = {v: k for k, v in jira_fields.COMMITMENT_LEVEL_MAPPINGS.items()}
        reverse_area_map = {v: k for k, v in jira_fields.AREA_MAPPINGS.items()}
        reverse_reason_map = {v: k for k, v in jira_fields.COMMITMENT_REASON_MAPPINGS.items()}
        
        for field_key, field_value in fields.items():
            human_name = field_mappings.get(field_key, field_key)
            
            # Analyze field values
            if field_key == 'project':
                project_id = field_value.get('id', '')
                project_name = 'RTDEV' if project_id == '10129' else 'APP' if project_id == '10246' else f'Project {project_id}'
                analysis['always_set'].append({
                    'field': 'Project',
                    'value': project_name,
                    'description': f'Sets project to {project_name}'
                })
            elif field_key == 'summary':
                analysis['user_provided'].append({
                    'field': 'Epic Title',
                    'value': 'Your epic name',
                    'description': 'Uses the epic name you provide'
                })
            elif field_key == 'description':
                if field_value and field_value != 'None':
                    analysis['defaults_used'].append({
                        'field': 'Description',
                        'value': 'Template-specific structure',
                        'description': 'Uses rich template structure if you don\'t provide description'
                    })
                else:
                    analysis['user_provided'].append({
                        'field': 'Description', 
                        'value': 'Your description',
                        'description': 'Uses description you provide'
                    })
            elif field_key == 'priority':
                priority_id = field_value.get('id', '')
                priority_name = reverse_priority_map.get(priority_id, f'Priority {priority_id}')
                if 'default' in template_content and 'priority' in template_content:
                    analysis['defaults_used'].append({
                        'field': 'Priority',
                        'value': priority_name,
                        'description': f'Defaults to "{priority_name}" unless you specify different'
                    })
                else:
                    analysis['always_set'].append({
                        'field': 'Priority',
                        'value': priority_name,
                        'description': f'Always sets priority to "{priority_name}"'
                    })
            elif field_key in field_mappings:
                # Handle custom fields
                if isinstance(field_value, list) and field_value:
                    if 'id' in field_value[0]:
                        if human_name == 'Team Assignment':
                            team_id = field_value[0]['id']
                            team_name = 'dev-artifactory-lifecycle' if team_id == '10145' else 'App Core' if team_id == '12980' else f'Team {team_id}'
                            analysis['always_set'].append({
                                'field': human_name,
                                'value': team_name,
                                'description': f'Assigns to "{team_name}" team'
                            })
                        else:
                            analysis['always_set'].append({
                                'field': human_name,
                                'value': str(field_value[0].get('id', field_value[0])),
                                'description': f'Sets {human_name.lower()}'
                            })
                    else:
                        # Product backlog or similar string array
                        analysis['defaults_used'].append({
                            'field': human_name,
                            'value': field_value[0] if field_value else 'N/A',
                            'description': f'Defaults to "{field_value[0]}" unless you specify different'
                        })
                elif isinstance(field_value, dict):
                    if 'id' in field_value:
                        field_id = field_value['id']
                        if human_name == 'Commitment Level':
                            level_name = reverse_commitment_map.get(field_id, f'Level {field_id}')
                            analysis['defaults_used'].append({
                                'field': human_name,
                                'value': level_name, 
                                'description': f'Defaults to "{level_name}" unless you specify different'
                            })
                        elif human_name == 'Area':
                            area_name = reverse_area_map.get(field_id, f'Area {field_id}')
                            analysis['defaults_used'].append({
                                'field': human_name,
                                'value': area_name,
                                'description': f'Defaults to "{area_name}" unless you specify different'
                            })
                        elif human_name == 'Commitment Reason':
                            reason_name = reverse_reason_map.get(field_id, f'Reason {field_id}')
                            analysis['defaults_used'].append({
                                'field': human_name,
                                'value': reason_name,
                                'description': f'Defaults to "{reason_name}" unless you specify different'
                            })
                        else:
                            analysis['always_set'].append({
                                'field': human_name,
                                'value': str(field_id),
                                'description': f'Sets {human_name.lower()}'
                            })
            elif field_key == 'parent':
                analysis['conditional'].append({
                    'field': 'Parent Epic',
                    'value': 'Your parent epic key',
                    'description': 'Only set if you provide --parent option'
                })
        
        # Check template content for conditional fields
        if '{%- if epic.parent %}' in template_content:
            if not any(f['field'] == 'Parent Epic' for f in analysis['conditional']):
                analysis['conditional'].append({
                    'field': 'Parent Epic',
                    'value': 'Your parent epic key',
                    'description': 'Only set if you provide --parent option'
                })
                
        if '{%- if epic.product_priority %}' in template_content:
            analysis['conditional'].append({
                'field': 'Product Priority',
                'value': 'Your choice (P0-P4)',
                'description': 'Only set if you provide --product-priority option'
            })
            
        if '{%- if user.account_id %}' in template_content:
            analysis['conditional'].append({
                'field': 'Product Manager',
                'value': 'Your account',
                'description': 'Only set if your account ID is available'
            })
        
        return analysis
    
    def _generate_template_summary(self, metadata: Dict[str, Any], fields_analysis: Dict[str, Any]) -> str:
        """Generate a human-readable summary of what the template does."""
        name = metadata.get('name', 'Unknown')
        template_type = metadata.get('issue_type', 'unknown')
        description = metadata.get('description', '')
        
        always_count = len(fields_analysis.get('always_set', []))
        conditional_count = len(fields_analysis.get('conditional', []))
        defaults_count = len(fields_analysis.get('defaults_used', []))
        
        summary = f"This {template_type} template"
        
        if description:
            summary += f" is {description.lower()}"
        
        summary += f". It automatically sets {always_count} required fields"
        
        if defaults_count > 0:
            summary += f", provides {defaults_count} smart defaults"
            
        if conditional_count > 0:
            summary += f", and supports {conditional_count} optional advanced fields"
            
        summary += "."
        
        return summary
    
    def _generate_usage_examples(self, template_name: str, template_type: str) -> List[str]:
        """Generate usage examples for the template."""
        examples = []
        
        # For project-specific templates, use the appropriate project
        if template_type == 'APP':
            project = 'APP'
        elif template_type == 'RTDEV':
            project = 'RTDEV'
        else:
            project = 'RTDEV'  # Default
        
        if template_type in ['epic', 'unknown', 'APP', 'RTDEV']:
            examples.append(f'python3 -m jira_tools epic "My New Epic" --template {template_name} --project {project}')
            examples.append(f'python3 -m jira_tools epic "Test Epic" --template {template_name} --project {project} --dry-run')
            
            if 'advanced' in template_name or 'feature' in template_name:
                examples.append(f'python3 -m jira_tools epic "Complex Epic" --template {template_name} --project {project} --commitment-level "Hard Commitment" --area "Features & Innovation"')
        
        return examples


class TemplateContext:
    """Helper class for building template contexts."""
    
    @staticmethod
    def build_epic_context(epic_name: str, project_key: str, **kwargs) -> Dict[str, Any]:
        """Build context for epic templates with comprehensive field mappings."""
        # Build shared issue data for both epic and issue objects (backward compatibility)
        issue_data = {
            'title': epic_name,
            'name': epic_name,  # Legacy support
            'description': kwargs.get('description'),
            'priority': kwargs.get('priority', '4 - Normal'),
            'commitment_level': kwargs.get('commitment_level'),
            'area': kwargs.get('area'),
            'commitment_reason': kwargs.get('commitment_reason'),
            'product_backlog': kwargs.get('product_backlog'),
            'product_priority': kwargs.get('product_priority'),
            'product_manager': kwargs.get('product_manager'),
            'parent': kwargs.get('parent')
        }
        
        # Build optional assignee contexts
        assignee_contexts = {}
        
        # Technical Writer
        if kwargs.get('technical_writer'):
            assignee_contexts['tech_writer'] = {'account_id': kwargs['technical_writer']}
            
        # UX Designer  
        if kwargs.get('ux_designer'):
            assignee_contexts['ux'] = {'account_id': kwargs['ux_designer']}
            
        # Architect
        if kwargs.get('architect'):
            assignee_contexts['architect'] = {'account_id': kwargs['architect']}

        context = {
            # New generic issue object (for new templates)
            'issue': issue_data,
            # Legacy epic object (for backward compatibility)
            'epic': issue_data,
            'project': {
                'key': project_key,
                'id': kwargs.get('project_id', ''),
            },
            'team': {
                'name': kwargs.get('team_name', ''),
                'id': kwargs.get('team_id', '')
            },
            'user': {
                'account_id': kwargs.get('user_account_id', '')
            },
            # Use the comprehensive mappings from jira_fields
            'priorities': jira_fields.PRIORITY_MAPPINGS,
            'issue_types': {'epic': '10000', 'story': '10001', 'task': '10003', 'bug': '10004'},
            'commitment_levels': jira_fields.COMMITMENT_LEVEL_MAPPINGS,
            'areas': jira_fields.AREA_MAPPINGS,
            'commitment_reasons': jira_fields.COMMITMENT_REASON_MAPPINGS,
            'product_priorities': jira_fields.PRODUCT_PRIORITY_MAPPINGS,
            'field_ids': {name: mapping.field_id for name, mapping in jira_fields.FIELD_MAPPINGS.items()}
        }
        
        # Add assignee contexts
        context.update(assignee_contexts)
        
        return context
    
    @staticmethod
    def build_story_context(story_name: str, project_key: str, **kwargs) -> Dict[str, Any]:
        """Build context for story templates."""
        context = TemplateContext.build_epic_context(story_name, project_key, **kwargs)
        context['story'] = context.pop('epic')  # Rename epic to story
        return context


# Global template manager instance
template_manager = TemplateManager()
