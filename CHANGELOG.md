# Changelog

All notable changes to the Firefly SBOM Tool will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Added
- Initial release of Firefly SBOM Tool
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
  - SPDX 2.3 (JSON and Tag-Value)
  - CycloneDX 1.4 (JSON and XML)
  - Custom JSON format
  - Markdown reports
- GitHub integration:
  - Scan single repositories
  - Scan entire organizations
  - Parallel repository processing
- Advanced features:
  - License detection and analysis
  - Vulnerability scanning via OSV API
  - Dependency tree visualization
  - Technology stack detection
  - SBOM signing and verification
- CLI interface with multiple commands:
  - `scan`: Scan a single repository
  - `scan-org`: Scan GitHub organization
  - `detect`: Detect technology stack
  - `verify`: Verify SBOM signatures
  - `init`: Initialize configuration
- Configuration management:
  - YAML configuration files
  - Environment variable support
  - Multiple configuration profiles
- Installation scripts:
  - Cross-platform installation script
  - Uninstallation script
  - Shell completions for Bash and Zsh
- Comprehensive documentation:
  - README with quick start guide
  - API reference
  - Contributing guidelines
  - Code of conduct

### Changed
- N/A (Initial release)

### Deprecated
- N/A (Initial release)

### Removed
- N/A (Initial release)

### Fixed
- N/A (Initial release)

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
