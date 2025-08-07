# Firefly SBOM Tool 🔒

<div align="center">

[![License](https://img.shields.io/badge/License-Apache%202.0-blue.svg)](https://opensource.org/licenses/Apache-2.0)
[![Python Version](https://img.shields.io/badge/python-3.8%2B-blue)](https://www.python.org/downloads/)
[![GitHub Stars](https://img.shields.io/github/stars/firefly-oss/sbom-tool?style=social)](https://github.com/firefly-oss/sbom-tool)
[![Docker Pulls](https://img.shields.io/docker/pulls/fireflyoss/sbom-tool)](https://hub.docker.com/r/fireflyoss/sbom-tool)

**A comprehensive Software Bill of Materials (SBOM) generation and security auditing tool for modern multi-technology stacks**

[Installation](#-installation) • [Quick Start](#-quick-start) • [Features](#-features) • [Documentation](#-documentation) • [Contributing](#-contributing)

</div>

---

## 📖 Table of Contents

- [Overview](#-overview)
- [Features](#-features)
- [Supported Technologies](#-supported-technologies)
- [Installation](#-installation)
- [Quick Start](#-quick-start)
- [Usage Guide](#-usage-guide)
- [Configuration](#-configuration)
- [Output Formats](#-output-formats)
- [CI/CD Integration](#-cicd-integration)
- [API Reference](#-api-reference)
- [Contributing](#-contributing)
- [License](#-license)

## 🎯 Overview

The **Firefly SBOM Tool** is an enterprise-grade solution for generating Software Bill of Materials (SBOM) documents and performing comprehensive security audits across multiple programming languages and frameworks. Designed for the Firefly Open Banking Platform ecosystem, it provides:

- 🚀 **Parallel scanning** of entire GitHub organizations
- 🔍 **Deep dependency analysis** with transitive dependency tracking
- 🛡️ **Security vulnerability detection** using multiple databases
- 📊 **Multiple output formats** including HTML, Markdown, JSON, CycloneDX, and SPDX
- ⚡ **High performance** with configurable parallel workers
- 🎨 **Beautiful reports** with modern, responsive design

## ✨ Features

### Core Capabilities

- **🔄 Parallel Organization Scanning**: Scan entire GitHub organizations with parallel repository processing
- **📦 Multi-Language Support**: Automatic detection and analysis of 7+ technology stacks
- **🔒 Security Auditing**: Comprehensive vulnerability scanning with CVE database integration
- **📋 License Compliance**: Automated license detection and compliance checking
- **📊 Rich Reporting**: Generate beautiful HTML, Markdown, and text reports
- **🔧 Flexible Configuration**: YAML-based configuration with environment variable support
- **🐳 Container Ready**: Full Docker support for isolated scanning
- **⚙️ CI/CD Integration**: Native support for GitHub Actions, GitLab CI, and Jenkins

### Advanced Features

- **Dependency Deduplication**: Intelligent component deduplication across technologies
- **Temporary Cloning**: Efficient temporary directory management for organization scans
- **Batch Processing**: Memory-efficient batch processing for large organizations
- **Custom Output Formats**: Support for industry standards (CycloneDX, SPDX) and custom formats
- **Real-time Progress**: Rich terminal UI with progress indicators and status updates
- **Incremental Scanning**: Cache support for faster subsequent scans

## 🛠️ Supported Technologies

| Language/Framework | Package Managers | Lock Files | Detection |
|-------------------|-----------------|------------|--------|
| **Java/Spring Boot** | Maven | pom.xml | ✅ Multi-module support |
| **Python** | pip, Poetry, Pipenv | requirements.txt, Pipfile.lock, poetry.lock | ✅ Full support |
| **Node.js/TypeScript** | npm, yarn, pnpm | package-lock.json, yarn.lock | ✅ Framework detection |
| **Flutter/Dart** | pub | pubspec.lock | ✅ SDK version tracking |
| **Go** | go modules | go.mod, go.sum | ✅ Replace directives |
| **Ruby** | Bundler | Gemfile.lock | ✅ Group dependencies |
| **Rust** | Cargo | Cargo.lock | ✅ Workspace support |
| **Angular** | npm/yarn | package-lock.json | ✅ Auto-detected |
| **React** | npm/yarn | package-lock.json | ✅ Auto-detected |
| **Vue.js** | npm/yarn | package-lock.json | ✅ Auto-detected |

## 📦 Installation

### Prerequisites

- Python 3.8 or higher
- Git 2.0 or higher
- Optional: Docker 20.10+ for containerized scanning
- Optional: Language-specific tools for enhanced scanning (Maven, npm, go, etc.)

### Method 1: Quick Install Script (Recommended)

```bash
# Download and run the install script
curl -sSL https://raw.githubusercontent.com/firefly-oss/sbom-tool/main/install.sh | bash

# Or with wget
wget -qO- https://raw.githubusercontent.com/firefly-oss/sbom-tool/main/install.sh | bash
```

### Method 2: Install from PyPI

```bash
# Install latest stable version
pip install firefly-sbom-tool

# Or install with all optional dependencies
pip install firefly-sbom-tool[all]
```

### Method 3: Install from Source

```bash
# Clone the repository
git clone https://github.com/firefly-oss/sbom-tool.git
cd sbom-tool

# Install in development mode
pip install -e .

# Or use the install script
./install.sh
```

### Method 4: Docker Installation

```bash
# Pull the latest image
docker pull ghcr.io/firefly-oss/sbom-tool:latest

# Create an alias for easy usage
alias firefly-sbom='docker run --rm -v $(pwd):/workspace ghcr.io/firefly-oss/sbom-tool:latest'
```

### Method 5: Homebrew (macOS/Linux)

```bash
# Add the Firefly tap
brew tap firefly-oss/tools

# Install the tool
brew install firefly-sbom-tool
```

### Verify Installation

```bash
# Check version
firefly-sbom --version

# Run help
firefly-sbom --help
```

## 🚀 Quick Start

### 1. Scan a Single Repository

```bash
# Basic scan with default settings
firefly-sbom scan --path ./my-project

# Scan with security audit and all formats
firefly-sbom scan --path ./my-project --audit --format all

# Include development dependencies
firefly-sbom scan --path ./my-project --include-dev --format html
```

### 2. Scan a GitHub Organization

```bash
# Scan entire organization with parallel processing
firefly-sbom scan-org --org firefly-oss --parallel 8

# Scan with custom output directory and formats
firefly-sbom scan-org \
  --org firefly-oss \
  --output-dir ./sbom-reports \
  --format html --format json --format markdown \
  --audit \
  --parallel 8
```

### 3. Detect Technology Stack

```bash
# Detect technologies in a repository
firefly-sbom detect --path ./my-project
```

### 4. Initialize Configuration

```bash
# Create a basic configuration file
firefly-sbom init

# Create GitHub Actions configuration
firefly-sbom init --template github-actions
```

## 📚 Usage Guide

### Command Line Interface

#### Main Commands

| Command | Description | Example |
|---------|-------------|------|
| `scan` | Scan a single repository | `firefly-sbom scan --path /repo --audit` |
| `scan-org` | Scan entire GitHub organization | `firefly-sbom scan-org --org firefly-oss` |
| `detect` | Detect technology stack | `firefly-sbom detect --path /repo` |
| `init` | Initialize configuration | `firefly-sbom init --template basic` |

#### Global Options

```bash
firefly-sbom [OPTIONS] COMMAND [ARGS]...

Options:
  --version           Show version and exit
  -c, --config PATH   Configuration file path
  -v, --verbose       Enable verbose output
  --help             Show help and exit
```

#### Scan Command Options

```bash
firefly-sbom scan [OPTIONS]

Options:
  -p, --path PATH           Repository path to scan [required]
  -f, --format FORMAT       Output format (cyclonedx-json, spdx-json, html, markdown, text, json, all)
  -o, --output PATH         Output file path
  --audit                   Enable security vulnerability scanning
  --include-dev            Include development dependencies
  --help                   Show help and exit
```

#### Scan-Org Command Options

```bash
firefly-sbom scan-org [OPTIONS]

Options:
  -o, --org TEXT           GitHub organization name [required]
  -d, --output-dir PATH    Output directory for reports (default: ./sbom-reports)
  -f, --format FORMAT      Output formats (can specify multiple)
  --audit                  Enable security vulnerability scanning
  --include-dev           Include development dependencies
  -p, --parallel INT      Number of parallel workers (default: 4)
  --combined/--no-combined Generate combined organization report (default: combined)
  --batch-size INT        Batch size for processing repositories (default: 10)
  --help                  Show help and exit
```

### Python API Usage

```python
from pathlib import Path
from firefly_sbom import SBOMGenerator, Config

# Initialize with configuration
config = Config({
    'scan': {
        'include_dev_dependencies': False,
        'parallel_workers': 4
    },
    'audit': {
        'vulnerability_databases': ['nvd', 'osv'],
        'fail_on_critical': True
    },
    'output': {
        'formats': ['cyclonedx-json', 'html'],
        'include_metadata': True
    }
})

# Create generator
generator = SBOMGenerator(config)

# Scan a single repository
sbom_data = generator.scan_repository(
    path=Path('/path/to/repo'),
    include_dev=False,
    audit=True
)

# Generate reports
generator.generate_report(
    sbom_data=sbom_data,
    format='html',
    output_path=Path('sbom-report.html')
)

# Scan entire organization
org_summary = generator.scan_organization(
    org='firefly-oss',
    output_dir=Path('./reports'),
    audit=True,
    parallel=8,
    formats=['html', 'json', 'markdown']
)
```

## ⚙️ Configuration

### Configuration File Structure

Create a `.sbom-config.yaml` file:

```yaml
# Scanning configuration
scan:
  include_dev_dependencies: false
  max_depth: 5
  parallel_workers: 4
  ignore_patterns:
    - '*.test.*'
    - '*.spec.*'
    - 'node_modules/'
    - 'venv/'
    - '.git/'
  follow_symlinks: false
  scan_archives: false

# Security audit configuration
audit:
  vulnerability_databases:
    - nvd      # National Vulnerability Database
    - osv      # Open Source Vulnerabilities
    - ghsa     # GitHub Security Advisories
  fail_on_critical: true
  severity_threshold: medium  # low, medium, high, critical
  ignore_vulnerabilities: []
  check_licenses: true
  allowed_licenses:
    - Apache-2.0
    - MIT
    - BSD-3-Clause
    - BSD-2-Clause
    - ISC
    - LGPL-3.0
    - MPL-2.0
  denied_licenses:
    - GPL-3.0
    - AGPL-3.0
    - Commercial

# Output configuration
output:
  formats:
    - cyclonedx-json
    - spdx-json
    - html
    - markdown
  include_metadata: true
  timestamp: true
  pretty_print: true
  compress: false
  sign_reports: false

# Cache configuration
cache:
  enabled: true
  directory: ~/.cache/firefly-sbom
  ttl_hours: 24
  max_size_mb: 500

# GitHub integration
github:
  token: ${GITHUB_TOKEN}  # Use environment variable
  api_url: https://api.github.com
  create_issues: false
  create_pr_on_vulnerabilities: false
```

### Environment Variables

| Variable | Description | Default |
|----------|-------------|---------|
| `GITHUB_TOKEN` | GitHub API token for organization scanning | None |
| `SBOM_CONFIG_PATH` | Path to configuration file | `.sbom-config.yaml` |
| `SBOM_OUTPUT_DIR` | Default output directory | `./sbom-reports` |
| `SBOM_PARALLEL_WORKERS` | Number of parallel workers | `4` |
| `SBOM_INCLUDE_DEV` | Include dev dependencies | `false` |
| `SBOM_AUDIT_ENABLED` | Enable security audit by default | `false` |
| `SBOM_LOG_LEVEL` | Logging level (DEBUG, INFO, WARNING, ERROR) | `INFO` |

## 📊 Output Formats

### Available Formats

| Format | Extension | Description | Use Case |
|--------|-----------|-------------|----------|
| **CycloneDX JSON** | `.cyclonedx.json` | Industry standard SBOM format | Tool integration |
| **CycloneDX XML** | `.cyclonedx.xml` | XML variant of CycloneDX | Legacy systems |
| **SPDX JSON** | `.spdx.json` | Linux Foundation standard | Compliance |
| **SPDX YAML** | `.spdx.yaml` | YAML variant of SPDX | Human-readable |
| **HTML** | `.html` | Interactive web report | Viewing/Sharing |
| **Markdown** | `.md` | Documentation format | GitHub/GitLab |
| **Text** | `.txt` | Plain text report | CLI/Logs |
| **JSON** | `.json` | Raw JSON data | API integration |

### Output Directory Structure

```
sbom-reports/
├── organization-summary.html       # Combined HTML report
├── organization-summary.json       # Combined JSON data
├── organization-summary.md         # Combined Markdown
├── organization-summary.txt        # Combined text report
│
├── repository-1/
│   ├── sbom.cyclonedx.json       # CycloneDX format
│   ├── sbom.spdx.json            # SPDX format
│   ├── sbom.html                 # HTML report
│   ├── sbom.md                   # Markdown report
│   └── sbom.json                 # Raw JSON data
│
├── repository-2/
│   └── ... (same structure)
│
└── failed-scans.log              # Log of failed scans
```

## 🔧 CI/CD Integration

### GitHub Actions

```yaml
name: SBOM Generation

on:
  push:
    branches: [ main ]
  schedule:
    - cron: '0 0 * * 0'  # Weekly scan

jobs:
  sbom-scan:
    runs-on: ubuntu-latest
    
    steps:
    - uses: actions/checkout@v3
    
    - name: Set up Python
      uses: actions/setup-python@v4
      with:
        python-version: '3.10'
    
    - name: Install Firefly SBOM Tool
      run: pip install firefly-sbom-tool
    
    - name: Run SBOM Scan
      run: |
        firefly-sbom scan \
          --path . \
          --format cyclonedx-json \
          --format html \
          --audit \
          --output sbom-report
    
    - name: Upload SBOM Reports
      uses: actions/upload-artifact@v3
      with:
        name: sbom-reports
        path: sbom-report*
        retention-days: 30
    
    - name: Check for Critical Vulnerabilities
      run: |
        if [ -f "sbom-report.json" ]; then
          critical_count=$(jq '.vulnerabilities | map(select(.severity == "critical")) | length' sbom-report.json)
          if [ "$critical_count" -gt "0" ]; then
            echo "::error::Found $critical_count critical vulnerabilities"
            exit 1
          fi
        fi
```

### GitLab CI

```yaml
sbom-scan:
  stage: security
  image: python:3.10
  
  before_script:
    - pip install firefly-sbom-tool
  
  script:
    - firefly-sbom scan --path . --audit --format all
  
  artifacts:
    reports:
      cyclonedx: sbom.cyclonedx.json
    paths:
      - sbom.*
    expire_in: 30 days
  
  only:
    - main
    - merge_requests
```

### Jenkins Pipeline

```groovy
pipeline {
    agent any
    
    stages {
        stage('SBOM Generation') {
            steps {
                sh '''
                    pip install firefly-sbom-tool
                    firefly-sbom scan \
                        --path . \
                        --audit \
                        --format cyclonedx-json \
                        --format html
                '''
            }
        }
        
        stage('Archive Reports') {
            steps {
                archiveArtifacts artifacts: 'sbom.*', fingerprint: true
            }
        }
    }
}
```

## 🐳 Docker Usage

### Basic Docker Commands

```bash
# Scan current directory
docker run --rm -v $(pwd):/workspace \
  ghcr.io/firefly-oss/sbom-tool:latest \
  scan --path /workspace

# Scan with output directory
docker run --rm \
  -v $(pwd):/workspace \
  -v $(pwd)/reports:/reports \
  ghcr.io/firefly-oss/sbom-tool:latest \
  scan --path /workspace --output /reports/sbom.json

# Scan organization with GitHub token
docker run --rm \
  -e GITHUB_TOKEN=$GITHUB_TOKEN \
  -v $(pwd)/reports:/reports \
  ghcr.io/firefly-oss/sbom-tool:latest \
  scan-org --org firefly-oss --output-dir /reports
```

### Docker Compose

```yaml
version: '3.8'

services:
  sbom-scanner:
    image: ghcr.io/firefly-oss/sbom-tool:latest
    environment:
      - GITHUB_TOKEN=${GITHUB_TOKEN}
    volumes:
      - ./:/workspace:ro
      - ./reports:/reports
    command: scan --path /workspace --output-dir /reports --audit --format all
```

## 📊 Report Examples

### HTML Report Features

- 📈 Interactive dependency graphs
- 🔍 Searchable component lists
- 🎨 Modern, responsive design
- 📊 Statistics dashboard
- 🔒 Vulnerability highlights
- 📋 License distribution charts
- 🔗 External links to package registries

### Sample Output

<details>
<summary>Click to see sample HTML report screenshot</summary>

```
┌─────────────────────────────────────────────┐
│  📦 Software Bill of Materials              │
│                                             │
│  Repository: firefly-core-banking          │
│  Generated: 2024-01-20T10:30:00Z          │
│                                             │
│  ┌─────────────────────────────────────┐   │
│  │ Total Components        │    247    │   │
│  │ Direct Dependencies     │     42    │   │
│  │ Transitive Dependencies │    205    │   │
│  │ Vulnerabilities        │      3    │   │
│  └─────────────────────────────────────┘   │
│                                             │
│  🔒 Security Vulnerabilities (3)           │
│  ├─ CRITICAL: CVE-2024-1234 in log4j      │
│  ├─ HIGH: CVE-2024-5678 in spring-core    │
│  └─ MEDIUM: CVE-2024-9012 in commons-io   │
│                                             │
│  📊 License Distribution                   │
│  ├─ Apache-2.0: 45%                       │
│  ├─ MIT: 30%                              │
│  ├─ BSD-3-Clause: 15%                     │
│  └─ Other: 10%                            │
└─────────────────────────────────────────────┘
```

</details>

## 🔌 API Reference

### Core Classes

#### SBOMGenerator

```python
class SBOMGenerator:
    def __init__(self, config: Config = None)
    
    def scan_repository(
        path: Path,
        include_dev: bool = False,
        audit: bool = False
    ) -> Dict[str, Any]
    
    def scan_organization(
        org: str,
        output_dir: Path,
        audit: bool = False,
        parallel: int = 4,
        formats: List[str] = None
    ) -> Dict[str, Any]
    
    def generate_report(
        sbom_data: Dict[str, Any],
        format: str,
        output_path: Path = None
    ) -> Path
```

#### Config

```python
class Config:
    def __init__(self, config_dict: Dict[str, Any] = None)
    
    @classmethod
    def from_file(cls, config_path: str) -> Config
    
    @classmethod
    def from_env(cls) -> Config
    
    def validate(self) -> List[str]
```

### Scanner Interface

```python
class Scanner(ABC):
    @abstractmethod
    def detect(self, path: Path) -> bool
    
    @abstractmethod
    def scan(
        self,
        path: Path,
        include_dev: bool = False
    ) -> List[Dict[str, Any]]
```

## 🤝 Contributing

We welcome contributions! Please see our [Contributing Guide](CONTRIBUTING.md) for details.

### Development Setup

```bash
# Clone repository
git clone https://github.com/firefly-oss/sbom-tool.git
cd sbom-tool

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install in development mode
pip install -e ".[dev]"

# Run tests
pytest

# Run linting
flake8 src/
black src/ --check
mypy src/
```

## 📄 License

Copyright 2024 Firefly OSS

Licensed under the Apache License, Version 2.0. See [LICENSE](LICENSE) for details.

## 🏦 About Firefly

Firefly is an OpenCore Banking Platform providing modern, cloud-native financial infrastructure. Visit [firefly-oss](https://github.com/firefly-oss) for more information.

## 🔗 Links

- 📚 [Full Documentation](https://firefly-oss.github.io/sbom-tool)
- 🐛 [Issue Tracker](https://github.com/firefly-oss/sbom-tool/issues)
- 📦 [PyPI Package](https://pypi.org/project/firefly-sbom-tool/)
- 🐳 [Docker Hub](https://hub.docker.com/r/fireflyoss/sbom-tool)
- 💬 [Discussions](https://github.com/firefly-oss/sbom-tool/discussions)
- 📈 [Releases](https://github.com/firefly-oss/sbom-tool/releases)

## 🙏 Acknowledgments

This tool integrates with and builds upon several excellent open-source projects:

- [CycloneDX](https://cyclonedx.org/) - SBOM standard
- [SPDX](https://spdx.dev/) - Software Package Data Exchange
- [OSV](https://osv.dev/) - Open Source Vulnerabilities database
- [Rich](https://github.com/Textualize/rich) - Terminal formatting

---

<div align="center">

**Made with ❤️ by the Firefly OSS Team**

[Report Bug](https://github.com/firefly-oss/sbom-tool/issues/new?labels=bug) • [Request Feature](https://github.com/firefly-oss/sbom-tool/issues/new?labels=enhancement) • [Join Community](https://github.com/firefly-oss/discussions)

</div>
