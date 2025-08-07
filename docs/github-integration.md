# GitHub Integration

The Firefly SBOM Tool provides comprehensive GitHub API integration for scanning entire organizations with advanced filtering and parallel processing capabilities.

## 🔧 Setup

### GitHub Personal Access Token

For scanning private repositories and accessing organization data, you'll need a GitHub Personal Access Token:

1. **Create a Personal Access Token**:
   - Go to GitHub Settings > Developer settings > Personal access tokens > Tokens (classic)
   - Click "Generate new token (classic)"
   - Select the following scopes:
     - `repo` - Full control of private repositories
     - `read:org` - Read org and team membership
     - `read:user` - Read user profile data

2. **Set the token as an environment variable**:
   ```bash
   export GITHUB_TOKEN="ghp_your_personal_access_token_here"
   ```

3. **Or pass it directly via CLI**:
   ```bash
   firefly-sbom scan-org --org firefly-oss --github-token "ghp_your_token"
   ```

## 📋 Basic Organization Scanning

### Simple Organization Scan
```bash
# Basic organization scan
firefly-sbom scan-org --org firefly-oss

# With security audit enabled
firefly-sbom scan-org --org firefly-oss --audit

# With custom output directory
firefly-sbom scan-org --org firefly-oss --output-dir ./my-reports
```

## 🔍 Repository Filtering

### By Repository Type
```bash
# Include private repositories (requires appropriate token permissions)
firefly-sbom scan-org --org firefly-oss --include-private

# Exclude forked repositories
firefly-sbom scan-org --org firefly-oss --no-forks

# Exclude archived repositories
firefly-sbom scan-org --org firefly-oss --no-archived

# Combine multiple filters
firefly-sbom scan-org --org firefly-oss --include-private --no-forks --no-archived
```

### By Programming Language
```bash
# Scan only Python and JavaScript repositories
firefly-sbom scan-org --org firefly-oss --languages Python JavaScript

# Scan Java-based microservices
firefly-sbom scan-org --org firefly-oss --languages Java Kotlin
```

### By Topics/Tags
```bash
# Scan repositories tagged with "microservice" or "api"
firefly-sbom scan-org --org firefly-oss --topics microservice api

# Scan core banking components
firefly-sbom scan-org --org firefly-oss --topics core-banking payment-processing
```

### Specific Repository Lists
```bash
# Scan specific repositories only
firefly-sbom scan-org --org firefly-oss \
  --repos core-banking-accounts \
  --repos core-lending-loan-origination \
  --repos common-platform-user-mgmt

# Use a repository list file
cat > repos.txt << EOF
core-banking-accounts
core-banking-ledger
core-lending-loan-origination
common-platform-user-mgmt
# Lines starting with # are ignored as comments
EOF

firefly-sbom scan-org --org firefly-oss --repos-file repos.txt
```

## ⚡ Performance Optimization

### Parallel Processing
```bash
# Use 8 parallel workers for faster scanning
firefly-sbom scan-org --org firefly-oss --parallel 8

# Adjust batch size for memory management (default: 10)
firefly-sbom scan-org --org firefly-oss --batch-size 5 --parallel 4
```

### Combined vs Individual Reports
```bash
# Generate individual reports only (faster for large organizations)
firefly-sbom scan-org --org firefly-oss --no-combined

# Generate both individual and combined reports (default)
firefly-sbom scan-org --org firefly-oss --combined
```

## 🚦 Rate Limiting and Error Handling

The tool automatically handles GitHub API rate limiting:
- **Rate Limit Detection**: Monitors API response headers for rate limit status
- **Automatic Retry**: Waits for rate limit reset with exponential backoff
- **Error Recovery**: Continues scanning other repositories if individual repositories fail
- **Detailed Logging**: Provides verbose output for debugging API issues

## ✅ Access Validation

Before scanning, the tool validates your GitHub access:
```bash
# Use verbose mode to see access validation details
firefly-sbom scan-org --org firefly-oss --verbose
```

The tool checks:
- Organization read access
- Private repository permissions
- Member repository access
- Rate limit status

## 📊 Output Formats

### Multi-Format Reports
```bash
# Generate reports in multiple formats
firefly-sbom scan-org --org firefly-oss \
  --format cyclonedx-json \
  --format html \
  --format markdown \
  --audit
```

### Available Formats
- `cyclonedx-json` - Industry standard SBOM format
- `cyclonedx-xml` - XML variant of CycloneDX
- `spdx-json` - Linux Foundation standard
- `spdx-yaml` - YAML variant of SPDX
- `html` - Interactive web report
- `markdown` - Documentation format
- `text` - Plain text report
- `json` - Raw JSON data

## 🔍 Troubleshooting

### Debug GitHub API Issues
```bash
# Verbose mode for debugging
firefly-sbom scan-org --org firefly-oss \
  --verbose \
  --parallel 1

# Test with a single repository first
firefly-sbom scan-org --org firefly-oss \
  --repos your-test-repo \
  --verbose
```

### Common Issues

1. **Authentication Errors**: Ensure your GitHub token has the correct scopes
2. **Rate Limiting**: The tool handles this automatically, but you can reduce parallel workers
3. **Private Repository Access**: Ensure your token has `repo` scope for private repositories
4. **Organization Access**: Ensure you have read access to the organization

## 📈 Performance Metrics

Expected scanning performance:
- **Small organization** (< 10 repos): 1-3 minutes
- **Medium organization** (10-50 repos): 5-15 minutes  
- **Large organization** (50-200 repos): 15-60 minutes
- **Enterprise organization** (200+ repos): 1-4 hours

*Performance varies based on repository size, dependencies, and parallel workers configured.*

## 🐳 Docker Integration

### Containerized Organization Scanning
```bash
# Scan organization using Docker
docker run --rm \
  -e GITHUB_TOKEN="$GITHUB_TOKEN" \
  -v $(pwd)/reports:/reports \
  ghcr.io/firefly-oss/sbom-tool:latest \
  scan-org --org firefly-oss \
  --output-dir /reports \
  --audit --parallel 4
```

## 📚 Advanced Examples

For more detailed examples and use cases, see the [GitHub Integration Examples](examples/github_integration_examples.md).
