# Firefly SBOM Tool - Project Summary

## Overview
The Firefly SBOM Tool is a comprehensive Software Bill of Materials (SBOM) generation and auditing tool designed specifically for the Firefly Open Banking Platform ecosystem. It supports multiple technology stacks and provides security auditing capabilities.

## Key Features

### 1. Multi-Language Support
- **Java/Maven**: Full support for Maven multi-module projects
- **Python**: Support for pip, Poetry, and Pipenv
- **Flutter/Dart**: Pubspec.yaml parsing
- **Node.js**: package.json and npm support
- **Go**: go.mod support

### 2. SBOM Formats
- CycloneDX (JSON/XML)
- SPDX (JSON/YAML)
- HTML reports with visualizations

### 3. Security Features
- Vulnerability scanning using NVD, OSV, and GitHub Security Advisories
- License compliance checking
- Configurable severity thresholds
- Automated issue creation for critical vulnerabilities

### 4. Automation & CI/CD
- GitHub Actions workflow included
- Docker support for containerized scanning
- CLI interface for easy integration
- Parallel processing for organization-wide scans

## Project Structure

```
sbom-tool/
├── src/firefly_sbom/
│   ├── __init__.py           # Main package initialization
│   ├── cli.py                # CLI interface
│   ├── core.py               # Core SBOM generator
│   ├── config.py             # Configuration management
│   ├── scanners/             # Language-specific scanners
│   │   ├── base.py          # Base scanner class
│   │   ├── maven.py         # Java/Maven scanner
│   │   ├── python.py        # Python scanner
│   │   ├── flutter.py       # Flutter scanner
│   │   ├── node.py          # Node.js scanner
│   │   └── go.py            # Go scanner
│   ├── generators/           # Report generators
│   │   └── __init__.py      # CycloneDX, SPDX, HTML generators
│   ├── auditors/            # Security auditing
│   │   └── __init__.py      # Vulnerability scanning
│   └── utils/               # Utility functions
│       └── logger.py        # Logging utilities
├── examples/
│   ├── scan_organization.py # Example usage script
│   └── config.yaml          # Example configuration
├── .github/workflows/
│   └── sbom-scan.yml        # GitHub Actions workflow
├── Dockerfile               # Docker container definition
├── docker-compose.yml       # Docker Compose configuration
├── requirements.txt         # Python dependencies
├── setup.py                # Package setup
├── LICENSE                  # Apache 2.0 License
├── README.md               # Main documentation
└── CONTRIBUTING.md         # Contribution guidelines
```

## Usage Examples

### Basic CLI Usage

```bash
# Install the tool
pip install -e .

# Scan a single repository
firefly-sbom scan --path /path/to/repo --format cyclonedx-json --audit

# Scan entire organization
firefly-sbom scan-org --org firefly-oss --output-dir ./reports --audit

# Detect technology stack
firefly-sbom detect --path /path/to/repo

# Initialize configuration
firefly-sbom init --template github-actions
```

### Docker Usage

```bash
# Build Docker image
docker build -t firefly-sbom .

# Run with Docker
docker run -v $(pwd):/repos firefly-sbom scan --path /repos --format all

# Use Docker Compose
docker-compose up
```

### Python API Usage

```python
from firefly_sbom import SBOMGenerator, Config

# Create configuration
config = Config({
    'audit': {'fail_on_critical': True},
    'output': {'formats': ['cyclonedx-json', 'html']}
})

# Initialize generator
generator = SBOMGenerator(config)

# Scan repository
sbom_data = generator.scan_repository(
    path=Path('/path/to/repo'),
    audit=True
)

# Generate report
generator.generate_report(sbom_data, format='cyclonedx-json')
```

## Configuration

The tool can be configured via:
1. YAML configuration files
2. Environment variables
3. Command-line arguments

Key configuration options:
- Dependency inclusion (dev dependencies)
- Security audit settings
- Output formats and metadata
- Cache settings
- GitHub integration

## Security & Compliance

- **License**: Apache License 2.0
- **Security Scanning**: Integrated vulnerability detection
- **License Compliance**: Configurable allowed/denied licenses
- **Audit Trail**: Complete metadata and timestamps in reports

## Integration Points

1. **CI/CD Pipelines**: GitHub Actions, GitLab CI, Jenkins
2. **Container Registries**: Docker Hub, GitHub Container Registry
3. **Security Tools**: Integration with vulnerability databases
4. **Monitoring**: Export metrics and reports

## Next Steps for Production

1. **Testing**: Add comprehensive unit and integration tests
2. **Documentation**: Generate API documentation with Sphinx
3. **Performance**: Optimize for large-scale scanning
4. **Monitoring**: Add metrics and logging
5. **Distribution**: Publish to PyPI and container registries

## Support

- GitHub Issues: https://github.com/firefly-oss/sbom-tool/issues
- Documentation: https://firefly-oss.github.io/sbom-tool
- Email: oss@firefly.com

## License

Copyright 2024 Firefly OSS

Licensed under the Apache License, Version 2.0
