# API Reference

This document provides comprehensive API documentation for the Firefly SBOM Tool Python library.

## Core Classes

### SBOMGenerator

The main class for generating SBOM reports.

```python
class SBOMGenerator:
    def __init__(self, config: Config = None)
```

#### Methods

##### scan_repository
```python
def scan_repository(
    path: Path,
    include_dev: bool = False,
    audit: bool = False
) -> Dict[str, Any]
```

Scan a single repository and generate SBOM data.

**Parameters:**
- `path` (Path): Path to the repository to scan
- `include_dev` (bool): Include development dependencies
- `audit` (bool): Enable security vulnerability scanning

**Returns:**
- Dict[str, Any]: SBOM data structure

**Example:**
```python
from pathlib import Path
from firefly_sbom import SBOMGenerator, Config

generator = SBOMGenerator()
sbom_data = generator.scan_repository(
    path=Path('./my-project'),
    include_dev=False,
    audit=True
)
```

##### scan_organization
```python
def scan_organization(
    org: str,
    output_dir: Path,
    audit: bool = False,
    parallel: int = 4,
    formats: List[str] = None
) -> Dict[str, Any]
```

Scan an entire GitHub organization.

**Parameters:**
- `org` (str): GitHub organization name
- `output_dir` (Path): Output directory for reports
- `audit` (bool): Enable security audit
- `parallel` (int): Number of parallel workers
- `formats` (List[str]): Output formats to generate

**Returns:**
- Dict[str, Any]: Organization scan summary

**Example:**
```python
org_summary = generator.scan_organization(
    org='firefly-oss',
    output_dir=Path('./reports'),
    audit=True,
    parallel=8,
    formats=['html', 'json', 'markdown']
)
```

##### generate_report
```python
def generate_report(
    sbom_data: Dict[str, Any],
    format: str,
    output_path: Path = None
) -> Path
```

Generate a report from SBOM data.

**Parameters:**
- `sbom_data` (Dict[str, Any]): SBOM data structure
- `format` (str): Output format
- `output_path` (Path, optional): Custom output path

**Returns:**
- Path: Path to generated report

**Example:**
```python
report_path = generator.generate_report(
    sbom_data=sbom_data,
    format='html',
    output_path=Path('custom-report.html')
)
```

##### detect_technology_stack
```python
def detect_technology_stack(path: Path) -> List[Dict[str, Any]]
```

Detect technology stack in a repository.

**Parameters:**
- `path` (Path): Repository path

**Returns:**
- List[Dict[str, Any]]: List of detected technologies

### Config

Configuration management class.

```python
class Config:
    def __init__(self, config_dict: Dict[str, Any] = None)
```

#### Class Methods

##### from_file
```python
@classmethod
def from_file(cls, config_path: str) -> Config
```

Load configuration from a YAML file.

**Parameters:**
- `config_path` (str): Path to configuration file

**Returns:**
- Config: Configuration instance

**Example:**
```python
config = Config.from_file('.sbom-config.yaml')
```

##### from_env
```python
@classmethod
def from_env(cls) -> Config
```

Load configuration from environment variables.

**Returns:**
- Config: Configuration instance

#### Methods

##### validate
```python
def validate(self) -> List[str]
```

Validate configuration and return any errors.

**Returns:**
- List[str]: List of validation errors

## Scanner Interface

Abstract base class for technology-specific scanners.

```python
class Scanner(ABC):
    @abstractmethod
    def detect(self, path: Path) -> bool:
        """Detect if this scanner applies to the given path."""
        pass
    
    @abstractmethod
    def scan(
        self,
        path: Path,
        include_dev: bool = False
    ) -> List[Dict[str, Any]]:
        """Scan for dependencies and return component list."""
        pass
```

### Available Scanners

- `PythonScanner` - Python projects (requirements.txt, setup.py, pyproject.toml)
- `NodeScanner` - Node.js projects (package.json, yarn.lock)
- `MavenScanner` - Java/Maven projects (pom.xml)
- `GoScanner` - Go projects (go.mod)
- `RubyScanner` - Ruby projects (Gemfile)
- `RustScanner` - Rust projects (Cargo.toml)
- `FlutterScanner` - Flutter/Dart projects (pubspec.yaml)

## GitHub Integration

### GitHubAPI

GitHub API client for organization scanning.

```python
class GitHubAPI:
    def __init__(self, token: Optional[str] = None)
```

#### Methods

##### get_organization_repositories
```python
def get_organization_repositories(
    org: str,
    repo_type: str = "all",
    include_private: bool = True,
    include_forks: bool = False,
    include_archived: bool = False
) -> List[Dict]
```

Get repositories from a GitHub organization.

##### filter_repositories
```python
def filter_repositories(
    repos: List[Dict],
    include_patterns: Optional[List[str]] = None,
    exclude_patterns: Optional[List[str]] = None,
    languages: Optional[List[str]] = None,
    topics: Optional[List[str]] = None,
    min_size_kb: Optional[int] = None,
    max_size_kb: Optional[int] = None
) -> List[Dict]
```

Filter repositories based on various criteria.

##### validate_access
```python
def validate_access(self, org: str) -> Dict[str, bool]
```

Validate GitHub API access for an organization.

## Data Structures

### SBOM Data Structure

The SBOM data returned by `scan_repository` follows this structure:

```python
{
    "metadata": {
        "tool": "firefly-sbom",
        "version": "1.0.0",
        "timestamp": "2024-08-07T16:00:00Z",
        "repository": "/path/to/repo"
    },
    "components": [
        {
            "name": "package-name",
            "version": "1.2.3",
            "type": "library",
            "language": "Python",
            "license": "MIT",
            "purl": "pkg:pypi/package-name@1.2.3",
            "hashes": ["sha256:..."],
            "dependencies": ["dep1", "dep2"]
        }
    ],
    "vulnerabilities": [
        {
            "id": "CVE-2024-1234",
            "component": "package-name",
            "severity": "high",
            "description": "Vulnerability description",
            "references": ["https://..."]
        }
    ],
    "stats": {
        "total_components": 247,
        "direct_deps": 42,
        "transitive_deps": 205,
        "vulnerabilities_by_severity": {
            "critical": 1,
            "high": 5,
            "medium": 10,
            "low": 3
        }
    }
}
```

### Organization Summary Structure

The organization summary returned by `scan_organization` follows this structure:

```python
{
    "organization": "firefly-oss",
    "scan_date": "2024-08-07T16:00:00Z",
    "total_repositories": 15,
    "successful_scans": 14,
    "failed_scans": 1,
    "total_components": 1250,
    "total_vulnerabilities": 23,
    "repositories": [
        {
            "name": "core-banking-accounts",
            "status": "success",
            "components": 85,
            "vulnerabilities": 2,
            "technologies": ["Java", "Spring Boot"]
        }
    ]
}
```

## Error Handling

### Exceptions

#### SBOMGeneratorError
```python
class SBOMGeneratorError(Exception):
    """Base exception for SBOM generation errors."""
    pass
```

#### GitHubAPIError
```python
class GitHubAPIError(Exception):
    """Exception for GitHub API related errors."""
    pass
```

#### ScannerError
```python
class ScannerError(Exception):
    """Exception for scanner-specific errors."""
    pass
```

### Example Error Handling

```python
from firefly_sbom import SBOMGenerator, SBOMGeneratorError, GitHubAPIError

try:
    generator = SBOMGenerator()
    sbom_data = generator.scan_repository(Path('./project'))
except SBOMGeneratorError as e:
    print(f"SBOM generation failed: {e}")
except Exception as e:
    print(f"Unexpected error: {e}")
```

## Utilities

### Logger

```python
from firefly_sbom.utils.logger import get_logger

logger = get_logger(__name__)
logger.info("Scanning repository...")
```

### Parallel Processing

```python
from firefly_sbom.utils.parallel import ParallelExecutor

executor = ParallelExecutor(max_workers=4)
results = executor.map(scan_function, repositories)
```

## Examples

### Basic Usage
```python
from pathlib import Path
from firefly_sbom import SBOMGenerator, Config

# Create generator with default configuration
generator = SBOMGenerator()

# Scan a repository
sbom_data = generator.scan_repository(
    path=Path('./my-project'),
    audit=True
)

# Generate HTML report
generator.generate_report(sbom_data, 'html')
```

### Advanced Configuration
```python
# Custom configuration
config = Config({
    'scan': {
        'include_dev_dependencies': True,
        'parallel_workers': 8
    },
    'audit': {
        'fail_on_critical': True,
        'severity_threshold': 'medium'
    },
    'output': {
        'formats': ['cyclonedx-json', 'html'],
        'include_metadata': True
    }
})

generator = SBOMGenerator(config)
```

### Organization Scanning
```python
import os
from pathlib import Path

# Set GitHub token
os.environ['GITHUB_TOKEN'] = 'your_token_here'

# Scan organization
org_summary = generator.scan_organization(
    org='firefly-oss',
    output_dir=Path('./reports'),
    audit=True,
    parallel=6,
    formats=['html', 'cyclonedx-json', 'markdown']
)

print(f"Scanned {org_summary['total_repositories']} repositories")
print(f"Found {org_summary['total_vulnerabilities']} vulnerabilities")
```
