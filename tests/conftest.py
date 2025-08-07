"""
Test configuration and fixtures for Firefly SBOM Tool
"""

import pytest
import tempfile
import shutil
from pathlib import Path
from unittest.mock import Mock, patch
import os
import sys

# Add src to Python path for testing
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from firefly_sbom.config import Config


@pytest.fixture
def temp_dir():
    """Create a temporary directory for testing"""
    temp_dir = tempfile.mkdtemp()
    yield Path(temp_dir)
    shutil.rmtree(temp_dir)


@pytest.fixture
def sample_config():
    """Create a sample configuration for testing"""
    return Config({
        'scan': {
            'include_dev_dependencies': False,
            'max_depth': 3,
            'parallel_workers': 2
        },
        'audit': {
            'fail_on_critical': False,
            'severity_threshold': 'medium'
        },
        'output': {
            'formats': ['cyclonedx-json', 'html']
        }
    })


@pytest.fixture
def mock_github_response():
    """Mock GitHub API response"""
    mock_repos = [
        {
            'name': 'test-repo-1',
            'clone_url': 'https://github.com/test/test-repo-1.git',
            'default_branch': 'main',
            'language': 'Python',
            'size': 1024
        },
        {
            'name': 'test-repo-2', 
            'clone_url': 'https://github.com/test/test-repo-2.git',
            'default_branch': 'main',
            'language': 'JavaScript',
            'size': 2048
        }
    ]
    return mock_repos


@pytest.fixture
def fixtures_dir():
    """Return path to test fixtures directory"""
    return Path(__file__).parent / "fixtures"


@pytest.fixture
def sample_sbom_data():
    """Sample SBOM data for testing generators"""
    return {
        'metadata': {
            'repository_name': 'test-repo',
            'repository': 'test-repo',
            'timestamp': '2024-01-01T00:00:00Z',
            'technologies': ['Python', 'JavaScript'],
            'tool': {
                'name': 'Firefly SBOM Tool',
                'version': '1.0.0'
            }
        },
        'components': [
            {
                'name': 'requests',
                'version': '2.28.1',
                'type': 'library',
                'license': 'Apache-2.0',
                'scope': 'direct'
            },
            {
                'name': 'flask',
                'version': '2.2.2',
                'type': 'library',
                'license': 'BSD-3-Clause',
                'scope': 'direct'
            },
            {
                'name': 'werkzeug',
                'version': '2.2.2',
                'type': 'library',
                'license': 'BSD-3-Clause',
                'scope': 'transitive'
            }
        ],
        'stats': {
            'total_components': 3,
            'direct_deps': 2,
            'transitive_deps': 1,
            'vulnerabilities': 0
        },
        'vulnerabilities': []
    }


@pytest.fixture
def sample_org_summary():
    """Sample organization summary for testing"""
    return {
        'organization': 'test-org',
        'scan_date': '2024-01-01T00:00:00Z',
        'total_repositories': 2,
        'successful_scans': 2,
        'failed_scans': 0,
        'total_components': 10,
        'total_vulnerabilities': 1,
        'repositories': [
            {
                'name': 'test-repo-1',
                'status': 'success',
                'components': 5,
                'vulnerabilities': 0,
                'technologies': ['Python']
            },
            {
                'name': 'test-repo-2',
                'status': 'success',
                'components': 5,
                'vulnerabilities': 1,
                'technologies': ['JavaScript', 'TypeScript']
            }
        ]
    }


# Mock external dependencies for testing
@pytest.fixture(autouse=True)
def mock_external_tools():
    """Mock external tool dependencies"""
    with patch('shutil.which') as mock_which:
        # Mock availability of external tools
        def which_side_effect(tool):
            available_tools = ['git', 'python3', 'node', 'npm', 'go']
            return f'/usr/bin/{tool}' if tool in available_tools else None
        
        mock_which.side_effect = which_side_effect
        yield mock_which
