"""
Integration tests for CLI commands
"""

import pytest
import json
import yaml
from pathlib import Path
from unittest.mock import patch, Mock
from click.testing import CliRunner

from firefly_sbom.cli import cli


class TestCLICommands:
    """Test CLI command integration"""
    
    def setup_method(self):
        """Setup for each test method"""
        self.runner = CliRunner()
    
    def test_version_command(self):
        """Test --version command"""
        result = self.runner.invoke(cli, ['--version'])
        assert result.exit_code == 0
        assert 'firefly-sbom, version 1.0.0' in result.output
    
    def test_help_command(self):
        """Test --help command"""
        result = self.runner.invoke(cli, ['--help'])
        assert result.exit_code == 0
        assert 'Firefly SBOM Tool' in result.output
        assert 'scan' in result.output
        assert 'detect' in result.output
        assert 'init' in result.output
        assert 'scan-org' in result.output
    
    def test_init_command(self, temp_dir):
        """Test init command"""
        with self.runner.isolated_filesystem():
            result = self.runner.invoke(cli, ['init'])
            assert result.exit_code == 0
            assert 'Created configuration file' in result.output
            
            # Check that config file was created
            config_file = Path('.sbom-config.yaml')
            assert config_file.exists()
            
            # Verify config file content
            with open(config_file, 'r') as f:
                config_data = yaml.safe_load(f)
            
            assert 'scan' in config_data
            assert 'audit' in config_data
            assert 'output' in config_data
            assert config_data['scan']['max_depth'] == 5
    
    def test_init_command_custom_template(self):
        """Test init command with custom template"""
        with self.runner.isolated_filesystem():
            result = self.runner.invoke(cli, ['init', '--template', 'comprehensive'])
            assert result.exit_code == 0
            assert 'comprehensive' in result.output
    
    def test_detect_command(self, temp_dir):
        """Test detect command"""
        with self.runner.isolated_filesystem():
            # Create a Python project
            Path('requirements.txt').write_text('requests==2.28.1\nflask==2.2.2')
            Path('package.json').write_text('{"name": "test", "dependencies": {}}')
            
            result = self.runner.invoke(cli, ['detect', '--path', '.'])
            assert result.exit_code == 0
            assert 'Detected Technologies' in result.output
            assert 'Python' in result.output
    
    def test_scan_command_basic(self):
        """Test basic scan command"""
        with self.runner.isolated_filesystem():
            # Create a simple Python project
            Path('requirements.txt').write_text('requests==2.28.1')
            
            result = self.runner.invoke(cli, [
                'scan', 
                '--path', '.', 
                '--output', 'test.json'
            ])
            assert result.exit_code == 0
            assert 'Scanning repository' in result.output
            assert 'Generated' in result.output
            
            # Check output file was created
            output_file = Path('test.json')
            assert output_file.exists()
            
            # Verify it's valid JSON
            with open(output_file, 'r') as f:
                data = json.load(f)
            assert 'bomFormat' in data or 'components' in data  # CycloneDX format
    
    def test_scan_command_multiple_formats(self):
        """Test scan command with multiple output formats"""
        with self.runner.isolated_filesystem():
            Path('requirements.txt').write_text('flask==2.2.2')
            
            result = self.runner.invoke(cli, [
                'scan', 
                '--path', '.',
                '--output', 'test',
                '--format', 'html',
                '--format', 'json'
            ])
            assert result.exit_code == 0
            
            # Should create both files
            assert Path('test.html').exists()
            assert Path('test.json').exists()
    
    def test_scan_command_with_config(self):
        """Test scan command using configuration file"""
        with self.runner.isolated_filesystem():
            # Create config file
            config_data = {
                'scan': {
                    'include_dev_dependencies': True,
                    'max_depth': 3
                },
                'output': {
                    'formats': ['html']
                }
            }
            
            with open('.sbom-config.yaml', 'w') as f:
                yaml.dump(config_data, f)
            
            # Create project
            Path('requirements.txt').write_text('pytest==7.1.3')
            
            result = self.runner.invoke(cli, [
                'scan', 
                '--path', '.',
                '--output', 'configured_test.html'
            ])
            assert result.exit_code == 0
            assert Path('configured_test.html').exists()
    
    def test_scan_command_with_audit(self):
        """Test scan command with security audit enabled"""
        with self.runner.isolated_filesystem():
            Path('requirements.txt').write_text('django==3.0')  # Older version might have vulns
            
            result = self.runner.invoke(cli, [
                'scan',
                '--path', '.',
                '--output', 'audit_test.json',
                '--audit'
            ])
            # Command should complete even if audit finds issues
            assert result.exit_code in [0, 1]  # May exit with 1 if vulnerabilities found
    
    def test_scan_command_verbose_mode(self):
        """Test scan command with verbose output"""
        with self.runner.isolated_filesystem():
            Path('requirements.txt').write_text('requests==2.28.1')
            
            result = self.runner.invoke(cli, [
                'scan',
                '--path', '.',
                '--output', 'verbose_test.json',
                '-v'
            ])
            assert result.exit_code == 0
            # Verbose mode should show more details
            assert len(result.output) > 100  # Should have substantial output
    
    @patch('firefly_sbom.core.requests.get')
    def test_scan_org_command_help(self, mock_get):
        """Test scan-org command help (without actually calling GitHub API)"""
        result = self.runner.invoke(cli, ['scan-org', '--help'])
        assert result.exit_code == 0
        assert 'GitHub organization' in result.output
        assert '--org' in result.output
        assert '--output-dir' in result.output
    
    def test_scan_org_command_missing_org(self):
        """Test scan-org command with missing organization parameter"""
        result = self.runner.invoke(cli, ['scan-org'])
        assert result.exit_code != 0
        assert 'Missing option' in result.output or 'required' in result.output.lower()
    
    def test_config_validation_warnings(self):
        """Test configuration validation with invalid settings"""
        with self.runner.isolated_filesystem():
            # Create invalid config
            config_data = {
                'audit': {
                    'severity_threshold': 'invalid_severity'
                },
                'output': {
                    'formats': ['invalid_format']
                }
            }
            
            with open('.sbom-config.yaml', 'w') as f:
                yaml.dump(config_data, f)
            
            Path('requirements.txt').write_text('requests==2.28.1')
            
            result = self.runner.invoke(cli, [
                'scan',
                '--path', '.',
                '--output', 'test.json',
                '-v'
            ])
            # Should still work but may show warnings
            assert result.exit_code == 0
    
    def test_error_handling_invalid_path(self):
        """Test error handling for invalid scan path"""
        result = self.runner.invoke(cli, [
            'scan',
            '--path', '/nonexistent/path',
            '--output', 'test.json'
        ])
        assert result.exit_code != 0
        assert 'not found' in result.output.lower() or 'invalid' in result.output.lower()
    
    def test_error_handling_permission_denied(self):
        """Test error handling for permission issues"""
        with self.runner.isolated_filesystem():
            Path('requirements.txt').write_text('requests==2.28.1')
            
            # Try to write to a directory that doesn't exist and can't be created
            result = self.runner.invoke(cli, [
                'scan',
                '--path', '.',
                '--output', '/root/forbidden/test.json'  # Should fail on most systems
            ])
            # Should handle the error gracefully
            assert result.exit_code != 0


class TestCLIConfigIntegration:
    """Test CLI integration with different configuration sources"""
    
    def setup_method(self):
        self.runner = CliRunner()
    
    def test_config_precedence_cli_over_file(self):
        """Test that CLI arguments override config file settings"""
        with self.runner.isolated_filesystem():
            # Create config with HTML format
            config_data = {
                'output': {
                    'formats': ['html']
                }
            }
            with open('.sbom-config.yaml', 'w') as f:
                yaml.dump(config_data, f)
            
            Path('requirements.txt').write_text('requests==2.28.1')
            
            # Override with CLI argument for JSON
            result = self.runner.invoke(cli, [
                'scan',
                '--path', '.',
                '--output', 'test.json',
                '--format', 'json'
            ])
            assert result.exit_code == 0
            assert Path('test.json').exists()
            # HTML file should not be created due to CLI override
            assert not Path('test.html').exists()
    
    def test_environment_variable_integration(self):
        """Test integration with environment variables"""
        with self.runner.isolated_filesystem():
            Path('requirements.txt').write_text('requests==2.28.1')
            
            # Test with environment variables
            env_vars = {
                'SBOM_OUTPUT_FORMATS': 'html,json',
                'SBOM_INCLUDE_DEV': 'true'
            }
            
            result = self.runner.invoke(cli, [
                'scan',
                '--path', '.',
                '--output', 'env_test'
            ], env=env_vars)
            
            assert result.exit_code == 0
