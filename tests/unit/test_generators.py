"""
Unit tests for report generators
"""

import pytest
import json
import yaml
from pathlib import Path
from unittest.mock import patch, Mock

from firefly_sbom.generators import (
    CycloneDXGenerator, 
    SPDXGenerator, 
    HTMLGenerator, 
    MarkdownGenerator, 
    TextGenerator
)


class TestCycloneDXGenerator:
    """Test CycloneDX SBOM generator"""
    
    def test_init_json(self):
        """Test CycloneDX generator initialization with JSON format"""
        generator = CycloneDXGenerator('json')
        assert generator.format_type == 'json'
    
    def test_init_xml(self):
        """Test CycloneDX generator initialization with XML format"""
        generator = CycloneDXGenerator('xml')
        assert generator.format_type == 'xml'
    
    @patch('firefly_sbom.generators.make_outputter')
    def test_generate_json(self, mock_make_outputter, sample_sbom_data, temp_dir):
        """Test CycloneDX JSON generation"""
        # Mock the outputter
        mock_outputter = Mock()
        mock_outputter.output_as_string.return_value = '{"test": "cyclonedx_json"}'
        mock_make_outputter.return_value = mock_outputter
        
        generator = CycloneDXGenerator('json')
        output_path = temp_dir / 'test.json'
        
        generator.generate(sample_sbom_data, output_path)
        
        # Verify file was created with expected content
        assert output_path.exists()
        with open(output_path, 'r') as f:
            content = f.read()
        assert '{"test": "cyclonedx_json"}' in content
        
        # Verify make_outputter was called correctly
        mock_make_outputter.assert_called_once()
        call_args = mock_make_outputter.call_args
        assert call_args[1]['output_format'].name == 'JSON'
    
    @patch('firefly_sbom.generators.make_outputter')
    def test_generate_xml(self, mock_make_outputter, sample_sbom_data, temp_dir):
        """Test CycloneDX XML generation"""
        # Mock the outputter
        mock_outputter = Mock()
        mock_outputter.output_as_string.return_value = '<test>cyclonedx_xml</test>'
        mock_make_outputter.return_value = mock_outputter
        
        generator = CycloneDXGenerator('xml')
        output_path = temp_dir / 'test.xml'
        
        generator.generate(sample_sbom_data, output_path)
        
        # Verify file was created with expected content
        assert output_path.exists()
        with open(output_path, 'r') as f:
            content = f.read()
        assert '<test>cyclonedx_xml</test>' in content
        
        # Verify make_outputter was called correctly
        mock_make_outputter.assert_called_once()
        call_args = mock_make_outputter.call_args
        assert call_args[1]['output_format'].name == 'XML'


class TestSPDXGenerator:
    """Test SPDX generator"""
    
    def test_init_json(self):
        """Test SPDX generator initialization with JSON format"""
        generator = SPDXGenerator('json')
        assert generator.format_type == 'json'
    
    def test_init_yaml(self):
        """Test SPDX generator initialization with YAML format"""
        generator = SPDXGenerator('yaml')
        assert generator.format_type == 'yaml'
    
    def test_generate_json(self, sample_sbom_data, temp_dir):
        """Test SPDX JSON generation"""
        generator = SPDXGenerator('json')
        output_path = temp_dir / 'test.spdx.json'
        
        generator.generate(sample_sbom_data, output_path)
        
        # Verify file was created and contains valid JSON
        assert output_path.exists()
        with open(output_path, 'r') as f:
            data = json.load(f)
        
        assert data['spdxVersion'] == 'SPDX-2.3'
        assert data['name'] == 'SBOM Document'
        assert len(data['packages']) == 3
        assert data['packages'][0]['name'] == 'requests'
        assert data['packages'][0]['version'] == '2.28.1'
    
    def test_generate_yaml(self, sample_sbom_data, temp_dir):
        """Test SPDX YAML generation"""
        generator = SPDXGenerator('yaml')
        output_path = temp_dir / 'test.spdx.yaml'
        
        generator.generate(sample_sbom_data, output_path)
        
        # Verify file was created and contains valid YAML
        assert output_path.exists()
        with open(output_path, 'r') as f:
            data = yaml.safe_load(f)
        
        assert data['spdxVersion'] == 'SPDX-2.3'
        assert data['name'] == 'SBOM Document'
        assert len(data['packages']) == 3
        assert data['packages'][0]['name'] == 'requests'


class TestHTMLGenerator:
    """Test HTML report generator"""
    
    def test_generate(self, sample_sbom_data, temp_dir):
        """Test HTML report generation"""
        generator = HTMLGenerator()
        output_path = temp_dir / 'test.html'
        
        generator.generate(sample_sbom_data, output_path)
        
        # Verify file was created
        assert output_path.exists()
        
        with open(output_path, 'r') as f:
            content = f.read()
        
        # Check HTML structure and content
        assert '<!DOCTYPE html>' in content
        assert '<html lang="en">' in content
        assert 'Software Bill of Materials' in content
        assert 'test-repo' in content
        assert 'Python' in content
        assert 'JavaScript' in content
        assert 'requests' in content
        assert 'flask' in content
        assert 'werkzeug' in content
        assert '2.28.1' in content
        assert 'Apache-2.0' in content
        assert 'BSD-3-Clause' in content
    
    def test_generate_with_vulnerabilities(self, sample_sbom_data, temp_dir):
        """Test HTML report generation with vulnerabilities"""
        # Add vulnerabilities to sample data
        sample_sbom_data['vulnerabilities'] = [
            {
                'component': 'requests',
                'id': 'CVE-2023-1234',
                'severity': 'high',
                'description': 'Test vulnerability'
            }
        ]
        sample_sbom_data['stats']['vulnerabilities'] = 1
        
        generator = HTMLGenerator()
        output_path = temp_dir / 'test_vuln.html'
        
        generator.generate(sample_sbom_data, output_path)
        
        with open(output_path, 'r') as f:
            content = f.read()
        
        assert 'Security Vulnerabilities' in content
        assert 'CVE-2023-1234' in content
        assert 'high' in content.lower()
        assert 'Test vulnerability' in content
    
    def test_generate_org_summary(self, sample_org_summary, temp_dir):
        """Test organization summary HTML generation"""
        generator = HTMLGenerator()
        output_path = temp_dir / 'org_summary.html'
        
        generator.generate_org_summary(sample_org_summary, output_path)
        
        assert output_path.exists()
        
        with open(output_path, 'r') as f:
            content = f.read()
        
        assert 'Organization SBOM Summary' in content
        assert 'test-org' in content
        assert 'test-repo-1' in content
        assert 'test-repo-2' in content
        assert 'Python' in content
        assert 'JavaScript' in content


class TestMarkdownGenerator:
    """Test Markdown report generator"""
    
    def test_generate(self, sample_sbom_data, temp_dir):
        """Test Markdown report generation"""
        generator = MarkdownGenerator()
        output_path = temp_dir / 'test.md'
        
        generator.generate(sample_sbom_data, output_path)
        
        assert output_path.exists()
        
        with open(output_path, 'r') as f:
            content = f.read()
        
        # Check Markdown structure and content
        assert '# Software Bill of Materials' in content
        assert '## 📋 Metadata' in content
        assert '## 📊 Statistics' in content
        assert '## 📦 Components' in content
        assert 'test-repo' in content
        assert 'Python' in content
        assert 'requests' in content
        assert '2.28.1' in content
        assert 'Apache-2.0' in content
        assert '| requests | 2.28.1 | library | Apache-2.0 | direct |' in content
    
    def test_generate_with_vulnerabilities(self, sample_sbom_data, temp_dir):
        """Test Markdown report generation with vulnerabilities"""
        # Add vulnerabilities to sample data
        sample_sbom_data['vulnerabilities'] = [
            {
                'component': 'flask',
                'id': 'CVE-2023-5678',
                'severity': 'medium',
                'description': 'Another test vulnerability'
            }
        ]
        sample_sbom_data['stats']['vulnerabilities'] = 1
        
        generator = MarkdownGenerator()
        output_path = temp_dir / 'test_vuln.md'
        
        generator.generate(sample_sbom_data, output_path)
        
        with open(output_path, 'r') as f:
            content = f.read()
        
        assert '## 🔒 Security Vulnerabilities' in content
        assert 'CVE-2023-5678' in content
        assert 'MEDIUM' in content
        assert 'Another test vulnerability' in content
    
    def test_generate_org_summary(self, sample_org_summary, temp_dir):
        """Test organization summary Markdown generation"""
        generator = MarkdownGenerator()
        output_path = temp_dir / 'org_summary.md'
        
        generator.generate_org_summary(sample_org_summary, output_path)
        
        assert output_path.exists()
        
        with open(output_path, 'r') as f:
            content = f.read()
        
        assert '# Organization SBOM Summary' in content
        assert '## 🏢 test-org' in content
        assert '## 📊 Overall Statistics' in content
        assert '## 📂 Repository Summary' in content
        assert 'test-repo-1' in content
        assert 'SUCCESS' in content


class TestTextGenerator:
    """Test plain text report generator"""
    
    def test_generate(self, sample_sbom_data, temp_dir):
        """Test text report generation"""
        generator = TextGenerator()
        output_path = temp_dir / 'test.txt'
        
        generator.generate(sample_sbom_data, output_path)
        
        assert output_path.exists()
        
        with open(output_path, 'r') as f:
            content = f.read()
        
        # Check text structure and content
        assert 'SOFTWARE BILL OF MATERIALS' in content
        assert '=' * 60 in content
        assert 'REPOSITORY: test-repo' in content
        assert 'TECHNOLOGIES: Python, JavaScript' in content
        assert 'STATISTICS:' in content
        assert 'Total Components: 3' in content
        assert 'COMPONENTS:' in content
        assert 'requests @ 2.28.1 [library] - Apache-2.0 (direct)' in content
        assert 'flask @ 2.2.2 [library] - BSD-3-Clause (direct)' in content
        assert 'Firefly SBOM Tool v1.0.0' in content
    
    def test_generate_org_summary(self, sample_org_summary, temp_dir):
        """Test organization summary text generation"""
        generator = TextGenerator()
        output_path = temp_dir / 'org_summary.txt'
        
        generator.generate_org_summary(sample_org_summary, output_path)
        
        assert output_path.exists()
        
        with open(output_path, 'r') as f:
            content = f.read()
        
        assert 'ORGANIZATION SBOM SUMMARY' in content
        assert 'ORGANIZATION: test-org' in content
        assert 'TOTAL REPOSITORIES: 2' in content
        assert 'REPOSITORIES:' in content
        assert 'test-repo-1: SUCCESS' in content
        assert 'test-repo-2: SUCCESS' in content
