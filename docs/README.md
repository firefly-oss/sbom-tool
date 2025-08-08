# Firefly SBOM Tool Documentation

Welcome to the comprehensive documentation for the Firefly SBOM Tool.

## 📚 Documentation Contents

### Getting Started
- [Installation Guide](installation.md) - Install the tool using various methods
- [CHANGELOG](CHANGELOG.md) - Version history and release notes

### User Guides
- [GitHub Integration](github-integration.md) - Scan GitHub organizations with advanced filtering
- [Configuration](configuration.md) - Comprehensive configuration options
- [Scanner Documentation](SCANNERS.md) - Supported languages and package managers

### Developer Resources
- [API Reference](api-reference.md) - Python API documentation
- [Contributing Guide](CONTRIBUTING.md) - How to contribute to the project
- [Project Summary](PROJECT_SUMMARY.md) - Technical overview and architecture

### Examples
- [Basic Usage Examples](examples/config.yaml) - Configuration examples
- [Organization Scanning](examples/scan_organization.py) - Python API examples
- [GitHub Integration Examples](examples/github_integration_examples.md) - Advanced GitHub scanning examples
- [GitHub Actions Workflow](ci/github-actions.md) - CI setup and templates

## 🚀 Quick Links

### Installation
```bash
# Quick install (recommended)
curl -sSL https://raw.githubusercontent.com/firefly-oss/sbom-tool/main/install.sh | bash

# From PyPI
pip install firefly-sbom-tool

# From source
git clone https://github.com/firefly-oss/sbom-tool.git && cd sbom-tool && pip install -e .
```

### Basic Usage
```bash
# Scan a repository
firefly-sbom scan --path ./my-project --audit

# Scan GitHub organization
export GITHUB_TOKEN="your_token"
firefly-sbom scan-org --org firefly-oss --audit --parallel 8
```

## 🆕 New Features (v1.0.0)

- **🐙 GitHub API Integration** - Full organization scanning with filtering
- **⚡ Parallel Processing** - High-performance scanning with configurable workers
- **🔍 Advanced Filtering** - Filter by language, topics, repository type
- **📊 Rich Reports** - Multiple output formats with interactive HTML reports
- **🔒 Security Auditing** - Comprehensive vulnerability scanning

## 📖 Core Concepts

### SBOM Generation
The tool automatically detects technology stacks and generates Software Bill of Materials (SBOM) documents in industry-standard formats including CycloneDX and SPDX.

### GitHub Organization Scanning
Scan entire GitHub organizations with advanced filtering by programming language, topics, repository type (private/public/forks/archived), and more.

### Security Auditing
Comprehensive vulnerability scanning using multiple databases including NVD (National Vulnerability Database), OSV (Open Source Vulnerabilities), and GitHub Security Advisories.

### Multi-Language Support
Native support for Python, Java/Maven, Node.js, Go, Ruby, Rust, Flutter/Dart, and more with automatic dependency detection.

## 🔗 External Links

- **GitHub Repository**: https://github.com/firefly-oss/sbom-tool
- **PyPI Package**: https://pypi.org/project/firefly-sbom-tool/
- **Docker Images**: https://hub.docker.com/r/fireflyoss/sbom-tool
- **Issue Tracker**: https://github.com/firefly-oss/sbom-tool/issues

## 🤝 Getting Help

- **Documentation**: You're reading it! 📖
- **GitHub Issues**: Report bugs or request features
- **GitHub Discussions**: Ask questions and share ideas
- **Contributing**: See our [Contributing Guide](CONTRIBUTING.md)

## 📄 License

Licensed under the Apache License, Version 2.0. See the main repository for full license details.
