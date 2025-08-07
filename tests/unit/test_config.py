"""
Unit tests for the configuration module
"""

import pytest
import tempfile
import os
from pathlib import Path
import yaml

from firefly_sbom.config import Config, ScanConfig, AuditConfig, OutputConfig, CacheConfig


class TestScanConfig:
    """Test ScanConfig dataclass"""
    
    def test_default_values(self):
        """Test default configuration values"""
        config = ScanConfig()
        assert config.include_dev_dependencies is False
        assert config.max_depth == 5
        assert config.parallel_workers == 4
        assert config.follow_symlinks is False
        assert config.scan_archives is False
        assert '*.test.*' in config.ignore_patterns
        assert 'node_modules/' in config.ignore_patterns
    
    def test_custom_values(self):
        """Test custom configuration values"""
        config = ScanConfig(
            include_dev_dependencies=True,
            max_depth=10,
            parallel_workers=8,
            ignore_patterns=['custom_pattern'],
            follow_symlinks=True,
            scan_archives=True
        )
        assert config.include_dev_dependencies is True
        assert config.max_depth == 10
        assert config.parallel_workers == 8
        assert config.ignore_patterns == ['custom_pattern']
        assert config.follow_symlinks is True
        assert config.scan_archives is True


class TestAuditConfig:
    """Test AuditConfig dataclass"""
    
    def test_default_values(self):
        """Test default audit configuration values"""
        config = AuditConfig()
        assert config.vulnerability_databases == ['nvd', 'osv', 'ghsa']
        assert config.fail_on_critical is True
        assert config.severity_threshold == 'medium'
        assert config.ignore_vulnerabilities == []
        assert config.check_licenses is True
        assert 'Apache-2.0' in config.allowed_licenses
        assert 'MIT' in config.allowed_licenses
        assert 'GPL-3.0' in config.denied_licenses
    
    def test_custom_values(self):
        """Test custom audit configuration values"""
        config = AuditConfig(
            vulnerability_databases=['custom_db'],
            fail_on_critical=False,
            severity_threshold='high',
            ignore_vulnerabilities=['CVE-2023-1234'],
            check_licenses=False,
            allowed_licenses=['MIT'],
            denied_licenses=['GPL-3.0']
        )
        assert config.vulnerability_databases == ['custom_db']
        assert config.fail_on_critical is False
        assert config.severity_threshold == 'high'
        assert config.ignore_vulnerabilities == ['CVE-2023-1234']
        assert config.check_licenses is False
        assert config.allowed_licenses == ['MIT']
        assert config.denied_licenses == ['GPL-3.0']


class TestOutputConfig:
    """Test OutputConfig dataclass"""
    
    def test_default_values(self):
        """Test default output configuration values"""
        config = OutputConfig()
        assert config.formats == ['cyclonedx-json', 'html']
        assert config.include_metadata is True
        assert config.timestamp is True
        assert config.pretty_print is True
        assert config.compress is False
        assert config.sign_reports is False
    
    def test_custom_values(self):
        """Test custom output configuration values"""
        config = OutputConfig(
            formats=['spdx-json'],
            include_metadata=False,
            timestamp=False,
            pretty_print=False,
            compress=True,
            sign_reports=True
        )
        assert config.formats == ['spdx-json']
        assert config.include_metadata is False
        assert config.timestamp is False
        assert config.pretty_print is False
        assert config.compress is True
        assert config.sign_reports is True


class TestCacheConfig:
    """Test CacheConfig dataclass"""
    
    def test_default_values(self):
        """Test default cache configuration values"""
        config = CacheConfig()
        assert config.enabled is True
        assert config.directory == '~/.cache/firefly-sbom'
        assert config.ttl_hours == 24
        assert config.max_size_mb == 500


class TestConfig:
    """Test main Config class"""
    
    def test_default_config(self):
        """Test default configuration creation"""
        config = Config()
        assert isinstance(config.scan, ScanConfig)
        assert isinstance(config.audit, AuditConfig)
        assert isinstance(config.output, OutputConfig)
        assert isinstance(config.cache, CacheConfig)
        assert config.github_token is None
        assert config.proxy is None
        assert config.timeout == 300
        assert config.verbose is False
    
    def test_config_from_dict(self):
        """Test configuration creation from dictionary"""
        config_dict = {
            'scan': {
                'include_dev_dependencies': True,
                'max_depth': 10
            },
            'audit': {
                'fail_on_critical': False,
                'severity_threshold': 'high'
            },
            'output': {
                'formats': ['cyclonedx-xml', 'spdx-json']
            },
            'cache': {
                'enabled': False
            },
            'github': {
                'token': 'test_token'
            },
            'proxy': 'http://proxy.example.com:8080',
            'timeout': 600,
            'verbose': True
        }
        
        config = Config(config_dict)
        assert config.scan.include_dev_dependencies is True
        assert config.scan.max_depth == 10
        assert config.audit.fail_on_critical is False
        assert config.audit.severity_threshold == 'high'
        assert config.output.formats == ['cyclonedx-xml', 'spdx-json']
        assert config.cache.enabled is False
        assert config.github_token == 'test_token'
        assert config.proxy == 'http://proxy.example.com:8080'
        assert config.timeout == 600
        assert config.verbose is True
    
    def test_config_from_file(self, temp_dir):
        """Test configuration loading from YAML file"""
        config_dict = {
            'scan': {
                'include_dev_dependencies': True,
                'max_depth': 8
            },
            'audit': {
                'severity_threshold': 'low'
            }
        }
        
        config_file = temp_dir / 'test_config.yaml'
        with open(config_file, 'w') as f:
            yaml.dump(config_dict, f)
        
        config = Config.from_file(str(config_file))
        assert config.scan.include_dev_dependencies is True
        assert config.scan.max_depth == 8
        assert config.audit.severity_threshold == 'low'
    
    def test_config_from_file_not_found(self):
        """Test configuration loading from non-existent file"""
        with pytest.raises(FileNotFoundError):
            Config.from_file('non_existent_file.yaml')
    
    def test_config_from_env(self, monkeypatch):
        """Test configuration loading from environment variables"""
        monkeypatch.setenv('SBOM_INCLUDE_DEV', 'true')
        monkeypatch.setenv('SBOM_MAX_DEPTH', '7')
        monkeypatch.setenv('SBOM_FAIL_ON_CRITICAL', 'false')
        monkeypatch.setenv('SBOM_SEVERITY_THRESHOLD', 'high')
        monkeypatch.setenv('SBOM_OUTPUT_FORMATS', 'cyclonedx-json,html')
        monkeypatch.setenv('GITHUB_TOKEN', 'env_token')
        
        config = Config.from_env()
        assert config.scan.include_dev_dependencies is True
        assert config.scan.max_depth == 7
        assert config.audit.fail_on_critical is False
        assert config.audit.severity_threshold == 'high'
        assert config.output.formats == ['cyclonedx-json', 'html']
        assert config.github_token == 'env_token'
    
    def test_config_to_dict(self):
        """Test configuration serialization to dictionary"""
        config = Config({
            'scan': {'max_depth': 6},
            'github': {'token': 'test_token'}
        })
        
        config_dict = config.to_dict()
        assert config_dict['scan']['max_depth'] == 6
        assert config_dict['github']['token'] == 'test_token'
        assert config_dict['audit']['severity_threshold'] == 'medium'  # default
        assert config_dict['output']['formats'] == ['cyclonedx-json', 'html']  # default
    
    def test_config_save(self, temp_dir):
        """Test configuration saving to file"""
        config = Config({'scan': {'max_depth': 7}})
        config_file = temp_dir / 'saved_config.yaml'
        
        config.save(str(config_file))
        
        assert config_file.exists()
        with open(config_file, 'r') as f:
            loaded_dict = yaml.safe_load(f)
        
        assert loaded_dict['scan']['max_depth'] == 7
    
    def test_config_validate(self):
        """Test configuration validation"""
        # Valid configuration
        config = Config()
        warnings = config.validate()
        assert len(warnings) == 0
        
        # Invalid severity threshold
        config = Config({'audit': {'severity_threshold': 'invalid'}})
        warnings = config.validate()
        assert len(warnings) == 1
        assert 'Invalid severity threshold' in warnings[0]
        
        # Invalid output format
        config = Config({'output': {'formats': ['invalid_format']}})
        warnings = config.validate()
        assert len(warnings) == 1
        assert 'Invalid output format' in warnings[0]
    
    def test_github_token_priority(self, monkeypatch):
        """Test GitHub token priority: config > environment"""
        monkeypatch.setenv('GITHUB_TOKEN', 'env_token')
        
        # Config without GitHub token should use env
        config = Config()
        assert config.github_token == 'env_token'
        
        # Config with GitHub token should override env
        config = Config({'github': {'token': 'config_token'}})
        assert config.github_token == 'config_token'
