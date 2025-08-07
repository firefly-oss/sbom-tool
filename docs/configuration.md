# Configuration

The Firefly SBOM Tool supports flexible configuration through YAML files, environment variables, and command-line arguments.

## Configuration File Structure

Create a `.sbom-config.yaml` file in your project root or specify a custom path with `--config`:

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

## Environment Variables

| Variable | Description | Default |
|----------|-------------|---------|
| `GITHUB_TOKEN` | GitHub API token for organization scanning | None |
| `SBOM_CONFIG_PATH` | Path to configuration file | `.sbom-config.yaml` |
| `SBOM_OUTPUT_DIR` | Default output directory | `./sbom-reports` |
| `SBOM_PARALLEL_WORKERS` | Number of parallel workers | `4` |
| `SBOM_INCLUDE_DEV` | Include dev dependencies | `false` |
| `SBOM_AUDIT_ENABLED` | Enable security audit by default | `false` |
| `SBOM_LOG_LEVEL` | Logging level (DEBUG, INFO, WARNING, ERROR) | `INFO` |

## Configuration Templates

Generate configuration files with predefined templates:

```bash
# Basic configuration
firefly-sbom init --template basic

# GitHub Actions configuration
firefly-sbom init --template github-actions

# GitLab CI configuration
firefly-sbom init --template gitlab-ci

# Jenkins configuration
firefly-sbom init --template jenkins
```

## Configuration Precedence

Configuration values are applied in the following order (highest to lowest priority):

1. **Command-line arguments**
2. **Environment variables**
3. **Configuration file**
4. **Default values**

## Scan Configuration

### Basic Settings
```yaml
scan:
  include_dev_dependencies: false  # Include development dependencies
  max_depth: 5                    # Maximum dependency depth
  parallel_workers: 4             # Number of parallel scanners
```

### Ignore Patterns
```yaml
scan:
  ignore_patterns:
    - '*.test.*'        # Ignore test files
    - '*.spec.*'        # Ignore spec files
    - 'node_modules/'   # Ignore Node.js modules
    - 'venv/'          # Ignore Python virtual environments
    - '.git/'          # Ignore Git directories
    - '**/__pycache__/' # Ignore Python cache
```

### Advanced Options
```yaml
scan:
  follow_symlinks: false    # Follow symbolic links
  scan_archives: false     # Scan inside archive files
  timeout_seconds: 300     # Scanner timeout
```

## Security Audit Configuration

### Vulnerability Databases
```yaml
audit:
  vulnerability_databases:
    - nvd   # National Vulnerability Database
    - osv   # Open Source Vulnerabilities
    - ghsa  # GitHub Security Advisories
```

### Severity Filtering
```yaml
audit:
  severity_threshold: medium  # Minimum severity to report
  fail_on_critical: true     # Exit with error on critical vulnerabilities
  ignore_vulnerabilities:    # CVEs to ignore
    - CVE-2021-44228
    - CVE-2021-45046
```

### License Configuration
```yaml
audit:
  check_licenses: true
  allowed_licenses:
    - Apache-2.0
    - MIT
    - BSD-3-Clause
    - ISC
  denied_licenses:
    - GPL-3.0
    - AGPL-3.0
    - Commercial
```

## Output Configuration

### Format Selection
```yaml
output:
  formats:
    - cyclonedx-json  # CycloneDX JSON format
    - cyclonedx-xml   # CycloneDX XML format
    - spdx-json      # SPDX JSON format
    - spdx-yaml      # SPDX YAML format
    - html           # HTML report
    - markdown       # Markdown report
    - text           # Plain text report
    - json           # Raw JSON data
```

### Report Options
```yaml
output:
  include_metadata: true    # Include generation metadata
  timestamp: true          # Add timestamps to reports
  pretty_print: true       # Format JSON output
  compress: false          # Compress output files
  sign_reports: false      # Sign SBOM reports
```

## Cache Configuration

### Basic Settings
```yaml
cache:
  enabled: true                    # Enable caching
  directory: ~/.cache/firefly-sbom # Cache directory
  ttl_hours: 24                   # Time to live in hours
  max_size_mb: 500                # Maximum cache size
```

### Advanced Options
```yaml
cache:
  compress_entries: true    # Compress cache entries
  cleanup_on_startup: true # Clean expired entries on startup
  ignore_patterns:         # Patterns to exclude from caching
    - '*.lock'
    - '*.tmp'
```

## GitHub Integration

### Authentication
```yaml
github:
  token: ${GITHUB_TOKEN}           # Use environment variable
  api_url: https://api.github.com  # GitHub API URL
```

### Automation Features
```yaml
github:
  create_issues: false                  # Create issues for vulnerabilities
  create_pr_on_vulnerabilities: false  # Create PRs for vulnerability fixes
  issue_labels:                         # Labels for created issues
    - security
    - dependencies
```

## Validation

Validate your configuration file:

```bash
# Check configuration syntax
firefly-sbom init --validate

# Show effective configuration
firefly-sbom --config my-config.yaml --verbose scan --help
```

## Examples

### Development Configuration
```yaml
scan:
  include_dev_dependencies: true
  parallel_workers: 2

audit:
  fail_on_critical: false
  severity_threshold: high

output:
  formats: [html, json]
```

### Production Configuration
```yaml
scan:
  include_dev_dependencies: false
  parallel_workers: 8

audit:
  fail_on_critical: true
  severity_threshold: medium
  vulnerability_databases: [nvd, osv, ghsa]

output:
  formats: [cyclonedx-json, spdx-json, html]
  sign_reports: true
```

### CI/CD Configuration
```yaml
scan:
  parallel_workers: 4

audit:
  fail_on_critical: true
  severity_threshold: high

output:
  formats: [cyclonedx-json]
  include_metadata: true

cache:
  enabled: false  # Disable caching in CI
```
