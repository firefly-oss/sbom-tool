# Installation Guide

This guide covers all available methods to install the Firefly SBOM Tool.

## Prerequisites

- Python 3.8 or higher
- Git 2.0 or higher
- Optional: Docker 20.10+ for containerized scanning
- Optional: Language-specific tools for enhanced scanning (Maven, npm, go, etc.)

## Method 1: Quick Install Script (Recommended)

```bash
# Download and run the install script
curl -sSL https://raw.githubusercontent.com/firefly-oss/sbom-tool/main/install.sh | bash

# Or with wget
wget -qO- https://raw.githubusercontent.com/firefly-oss/sbom-tool/main/install.sh | bash
```

## Method 2: Install from PyPI

```bash
# Install latest stable version
pip install firefly-sbom-tool

# Or install with all optional dependencies
pip install firefly-sbom-tool[all]
```

## Method 3: Install from Source

```bash
# Clone the repository
git clone https://github.com/firefly-oss/sbom-tool.git
cd sbom-tool

# Install in development mode
pip install -e .

# Or use the install script
./install.sh
```

## Method 4: Docker Installation

```bash
# Pull the latest image
docker pull ghcr.io/firefly-oss/sbom-tool:latest

# Create an alias for easy usage
alias firefly-sbom='docker run --rm -v $(pwd):/workspace ghcr.io/firefly-oss/sbom-tool:latest'
```

## Method 5: Homebrew (macOS/Linux)

```bash
# Add the Firefly tap
brew tap firefly-oss/tools

# Install the tool
brew install firefly-sbom-tool
```

## Verify Installation

```bash
# Check version
firefly-sbom --version

# Run help
firefly-sbom --help
```

## Troubleshooting

### Common Issues

1. **Python Version**: Ensure you're using Python 3.8 or higher
2. **Virtual Environment**: Consider using a virtual environment to avoid conflicts
3. **Dependencies**: Some scanners require language-specific tools (Maven, npm, etc.)
4. **Permissions**: On some systems, you may need to use `sudo` for system-wide installation

### Virtual Environment Setup

```bash
# Create virtual environment
python -m venv sbom-env
source sbom-env/bin/activate  # On Windows: sbom-env\Scripts\activate

# Install the tool
pip install firefly-sbom-tool

# Verify installation
firefly-sbom --version
```
