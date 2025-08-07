# Changelog

All notable changes to the Firefly SBOM Tool will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [1.0.0] - 2024-08-07

### Added
- **Initial Release**: Complete SBOM generation and auditing tool
- **🆕 GitHub API Integration**: Full GitHub API integration for organization scanning
  - Authentication via GitHub personal access tokens
  - Rate limiting and retry logic with exponential backoff
  - Repository filtering by language, topics, type (private/public/forks/archived)
  - Support for specific repository lists and file-based repository selection
  - Access validation and capability detection
- **🚀 Parallel Organization Scanning**: High-performance organization-wide scanning
  - Configurable parallel workers (default: 4, customizable up to system limits)
  - Batch processing for memory-efficient large organization scans
  - Combined organization reports with statistics and summaries
  - Failed scan logging and error handling
- **🔍 Advanced Repository Filtering**: Granular control over which repositories to scan
  - Filter by programming languages (Python, JavaScript, Java, Go, etc.)
  - Filter by GitHub topics/tags for targeted scanning
  - Include/exclude private repositories, forks, and archived repos
  - Support for repository whitelists via command line or file
- Support for multiple package managers and languages:
  - Python (requirements.txt, Pipfile, pyproject.toml, setup.py)
  - JavaScript/TypeScript (package.json, yarn.lock, package-lock.json)
  - Java (pom.xml, build.gradle)
  - Go (go.mod, go.sum)
  - Ruby (Gemfile, Gemfile.lock)
  - Rust (Cargo.toml, Cargo.lock)
  - PHP (composer.json, composer.lock)
  - .NET (*.csproj, packages.config)
  - Flutter/Dart (pubspec.yaml, pubspec.lock)
- Multiple output formats:
  - SPDX 2.3 (JSON and YAML)
  - CycloneDX 1.4 (JSON and XML)
  - Custom JSON format
  - HTML reports with interactive features
  - Markdown reports for documentation
  - Plain text reports for logs/CLI
- **Enhanced CLI Interface**: Rich terminal UI with progress indicators
  - `scan`: Scan a single repository
  - `scan-org`: Scan entire GitHub organizations with filtering
  - `detect`: Detect technology stack
  - `init`: Initialize configuration with templates
  - Verbose output modes with detailed logging
  - Rich formatting with colors, tables, and progress bars
- **Comprehensive Configuration System**:
  - YAML configuration files with validation
  - Environment variable support with precedence handling
  - Multiple configuration templates (basic, github-actions, gitlab-ci, jenkins)
  - GitHub token management via environment variables
- Advanced features:
  - License detection and analysis
  - Vulnerability scanning via multiple databases (NVD, OSV, GHSA)
  - Dependency tree visualization
  - Technology stack detection with auto-discovery
  - Component deduplication across technologies
  - Temporary directory management for organization scans
- Installation and distribution:
  - Cross-platform installation script
  - Uninstallation script
  - Package distribution setup for PyPI
  - Docker container support
- Comprehensive documentation:
  - README with quick start guide and advanced examples
  - GitHub API integration guide
  - Organization scanning documentation
  - Configuration templates and examples
  - API reference documentation
  - Contributing guidelines and development setup

### Changed
- N/A (Initial release)

### Deprecated
- N/A (Initial release)

### Removed
- N/A (Initial release)

### Fixed
- **CycloneDX Integration**: Fixed import issues with CycloneDX library (updated to use `make_outputter`)
- **Configuration Parsing**: Fixed dataclass field access for default values
- **Dependencies**: Removed invalid Python dependencies (`concurrent-futures`, `asyncio`)
- **Code Quality**: Applied consistent formatting with Black and isort
- **Test Coverage**: Added comprehensive unit and integration tests

### Security
- N/A (Initial release)

## [0.1.0] - 2024-01-XX (Planned)

Initial public release.

---

## Release Notes Format

For each release, we include:

### Types of changes
- **Added** for new features
- **Changed** for changes in existing functionality
- **Deprecated** for soon-to-be removed features
- **Removed** for now removed features
- **Fixed** for any bug fixes
- **Security** in case of vulnerabilities

### Version numbering
We follow Semantic Versioning:
- **MAJOR** version for incompatible API changes
- **MINOR** version for backwards-compatible functionality additions
- **PATCH** version for backwards-compatible bug fixes

### Links
[Unreleased]: https://github.com/firefly-oss/sbom-tool/compare/v0.1.0...HEAD
[0.1.0]: https://github.com/firefly-oss/sbom-tool/releases/tag/v0.1.0
