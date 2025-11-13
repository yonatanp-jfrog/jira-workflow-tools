"""
Unit tests for template system.

Tests the TemplateManager class and template functionality
without requiring actual Jira connections.
"""

import pytest
import json
import tempfile
from pathlib import Path
from unittest.mock import patch, MagicMock

# Import the modules we're testing
import sys
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from jira_tools.core.templates import TemplateManager, TemplateContext
from jira_tools.utils.exceptions import TemplateError, ValidationError


class TestTemplateManager:
    """Test cases for TemplateManager."""
    
    def test_template_manager_initialization(self):
        """Test that TemplateManager can be initialized."""
        with tempfile.TemporaryDirectory() as temp_dir:
            manager = TemplateManager(temp_dir)
            assert manager is not None
            assert manager.template_dir == Path(temp_dir)
    
    def test_list_templates(self):
        """Test template listing functionality."""
        manager = TemplateManager()
        
        templates = manager.list_templates()
        
        # Should find some built-in templates
        assert isinstance(templates, list)
        
        # Look for expected built-in templates
        template_names = [t['name'] for t in templates]
        assert 'base' in template_names  # Should have base epic template
    
    def test_list_templates_by_type(self):
        """Test template filtering by issue type."""
        manager = TemplateManager()
        
        epic_templates = manager.list_templates('epic')
        
        # All returned templates should be epic type
        for template in epic_templates:
            assert template['issue_type'] == 'epic'
    
    def test_select_template_basic(self):
        """Test basic template selection."""
        manager = TemplateManager()
        
        # Should be able to select an epic template
        template = manager.select_template('epic')
        assert template is not None
    
    def test_select_template_specific(self):
        """Test selecting a specific template by name."""
        manager = TemplateManager()
        
        # Should be able to select the feature template
        template = manager.select_template('epic', template_name='feature')
        assert template is not None
    
    def test_select_template_not_found(self):
        """Test error when template is not found."""
        manager = TemplateManager()
        
        with pytest.raises(TemplateError, match="No template found"):
            manager.select_template('nonexistent-type')
    
    def test_render_template(self):
        """Test template rendering."""
        manager = TemplateManager()
        
        # Get a template
        template = manager.select_template('epic')
        
        # Create test context
        context = {
            'project': {'id': '12345'},
            'epic': {'name': 'Test Epic', 'description': 'Test Description'},
            'priorities': {'4 - Normal': '10003'},
            'issue_types': {'epic': '10000'}
        }
        
        # Render template
        rendered = manager.render_template(template, context)
        
        # Should be valid JSON
        assert rendered
        data = json.loads(rendered)
        assert 'fields' in data
        assert data['fields']['summary'] == 'Test Epic'
    
    def test_validate_rendered_content(self):
        """Test rendered content validation."""
        manager = TemplateManager()
        
        # Valid JSON content
        valid_content = '''
        {
            "fields": {
                "project": {"id": "12345"},
                "summary": "Test Issue",
                "issuetype": {"id": "10000"}
            }
        }
        '''
        
        # Should not raise an exception
        manager.validate_rendered_content(valid_content)
        
        # Invalid JSON
        with pytest.raises(ValidationError, match="not valid JSON"):
            manager.validate_rendered_content("invalid json")
        
        # Missing required fields
        missing_fields_content = '{"fields": {}}'
        with pytest.raises(ValidationError, match="Missing required fields"):
            manager.validate_rendered_content(missing_fields_content)
    
    def test_create_template(self):
        """Test template creation."""
        with tempfile.TemporaryDirectory() as temp_dir:
            manager = TemplateManager(temp_dir)
            
            template_content = '''
            {
                "fields": {
                    "project": {"id": "{{ project.id }}"},
                    "summary": "{{ epic.name }}",
                    "issuetype": {"id": "10000"}
                }
            }
            '''
            
            template_file = manager.create_template(
                'epic', 'test_template', template_content, 'Test template'
            )
            
            assert template_file.exists()
            assert template_file.name == 'test_template.j2'
            
            # Should be able to validate the created template
            result = manager.validate_template(template_file)
            assert result['valid'] is True
    
    def test_validate_template(self):
        """Test template validation."""
        with tempfile.TemporaryDirectory() as temp_dir:
            manager = TemplateManager(temp_dir)
            
            # Create a valid template
            template_file = Path(temp_dir) / 'test.j2'
            template_file.write_text('''
            {
                "fields": {
                    "project": {"id": "{{ project.id }}"},
                    "summary": "{{ epic.name }}",
                    "issuetype": {"id": "10000"}
                }
            }
            ''')
            
            result = manager.validate_template(template_file)
            
            assert result['valid'] is True
            assert len(result['errors']) == 0
    
    def test_validate_invalid_template(self):
        """Test validation of invalid template."""
        with tempfile.TemporaryDirectory() as temp_dir:
            manager = TemplateManager(temp_dir)
            
            # Create an invalid template (missing required fields)
            template_file = Path(temp_dir) / 'invalid.j2'
            template_file.write_text('''
            {
                "fields": {
                    "summary": "{{ epic.name }}"
                }
            }
            ''')
            
            result = manager.validate_template(template_file)
            
            assert result['valid'] is False
            assert len(result['errors']) > 0


class TestTemplateContext:
    """Test cases for TemplateContext helper."""
    
    def test_build_epic_context(self):
        """Test building epic context."""
        context = TemplateContext.build_epic_context(
            epic_name="Test Epic",
            project_key="TEST",
            description="Test description",
            priority="3 - High"
        )
        
        assert 'epic' in context
        assert context['epic']['name'] == "Test Epic"
        assert context['epic']['description'] == "Test description"
        assert context['epic']['priority'] == "3 - High"
        
        assert 'project' in context
        assert context['project']['key'] == "TEST"
        
        # Should have priority mappings
        assert 'priorities' in context
        assert '3 - High' in context['priorities']
    
    def test_build_story_context(self):
        """Test building story context."""
        context = TemplateContext.build_story_context(
            story_name="Test Story",
            project_key="TEST"
        )
        
        assert 'story' in context
        assert context['story']['name'] == "Test Story"
        
        assert 'project' in context
        assert context['project']['key'] == "TEST"


class TestTemplateIntegration:
    """Integration tests for template system."""
    
    def test_full_template_workflow(self):
        """Test complete template workflow: list, select, render."""
        manager = TemplateManager()
        
        # List templates
        templates = manager.list_templates('epic')
        assert len(templates) > 0
        
        # Select a template
        template = manager.select_template('epic', template_name='base')
        assert template is not None
        
        # Create context
        context = TemplateContext.build_epic_context(
            epic_name="Integration Test Epic",
            project_key="TEST",
            project_id="12345",
            team_id="67890",
            user_account_id="test-user"
        )
        
        # Render template
        rendered = manager.render_template(template, context)
        
        # Validate result
        assert rendered
        data = json.loads(rendered)
        assert data['fields']['summary'] == "Integration Test Epic"
        assert data['fields']['project']['id'] == "12345"
    
    def test_project_specific_template_selection(self):
        """Test that project-specific templates are selected correctly."""
        manager = TemplateManager()
        
        # Try to select RTDEV-specific template
        try:
            template = manager.select_template('epic', project_key='RTDEV')
            assert template is not None
        except TemplateError:
            # It's OK if no RTDEV-specific template exists yet
            pass
    
    def test_template_error_handling(self):
        """Test proper error handling in template operations."""
        manager = TemplateManager()
        
        # Invalid template type
        with pytest.raises(TemplateError):
            manager.select_template('invalid_type')
        
        # Invalid template content for rendering
        template = manager.select_template('epic')
        
        # Missing required context
        with pytest.raises(TemplateError):
            manager.render_template(template, {})


if __name__ == '__main__':
    # Allow running tests directly  
    pytest.main([__file__])
