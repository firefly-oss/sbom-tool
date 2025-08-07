# GitHub Integration Examples

This document showcases the new GitHub API integration features added to the Firefly SBOM Tool v1.0.0.

## 🔧 Quick Setup

### 1. Set up your GitHub token
```bash
export GITHUB_TOKEN="ghp_your_personal_access_token_here"
```

### 2. Test the GitHub API connection
```bash
# Basic organization scanning
firefly-sbom scan-org --org firefly-oss --verbose
```

## 🎯 Targeted Scanning Examples

### Scan Specific Technologies
```bash
# Scan only Python microservices
firefly-sbom scan-org --org firefly-oss \
  --languages Python \
  --topics microservice \
  --audit --parallel 4

# Scan Java/Spring Boot applications
firefly-sbom scan-org --org firefly-oss \
  --languages Java \
  --topics spring-boot api \
  --format cyclonedx-json --format html
```

### Repository Filtering
```bash
# Exclude forks and archived repositories
firefly-sbom scan-org --org firefly-oss \
  --no-forks --no-archived \
  --include-private

# Scan core banking repositories only
firefly-sbom scan-org --org firefly-oss \
  --repos core-banking-accounts \
  --repos core-banking-ledger \
  --repos core-lending-loan-origination \
  --audit --format all
```

## 🚀 Performance Optimization

### High-Performance Scanning
```bash
# Maximum parallel processing (adjust based on your system)
firefly-sbom scan-org --org firefly-oss \
  --parallel 12 \
  --batch-size 5 \
  --output-dir ./high-speed-scan

# Memory-efficient scanning for large organizations
firefly-sbom scan-org --org firefly-oss \
  --parallel 4 \
  --batch-size 3 \
  --no-combined
```

## 📋 Repository List Management

### Using Repository Files
```bash
# Create a repository list
cat > critical-repos.txt << EOF
# Core banking services
core-banking-accounts
core-banking-ledger
core-lending-loan-origination

# Common platform services
common-platform-user-mgmt
common-platform-customer-mgmt
common-platform-document-mgmt
EOF

# Scan from the list
firefly-sbom scan-org --org firefly-oss \
  --repos-file critical-repos.txt \
  --audit --format cyclonedx-json --format html
```

## 🔒 Security-Focused Scanning

### Complete Security Audit
```bash
# Comprehensive security scan with all databases
firefly-sbom scan-org --org firefly-oss \
  --audit \
  --format cyclonedx-json --format html --format markdown \
  --parallel 6 \
  --output-dir ./security-audit-$(date +%Y%m%d)
```

## 📊 Output Examples

### Multi-Format Organization Report
```bash
# Generate reports in all formats for compliance
firefly-sbom scan-org --org firefly-oss \
  --format cyclonedx-json \
  --format cyclonedx-xml \
  --format spdx-json \
  --format spdx-yaml \
  --format html \
  --format markdown \
  --format text \
  --audit --combined
```

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

## 🎉 Advanced Features

### GitHub API Rate Limit Handling
The tool automatically handles GitHub API rate limits:
- Monitors rate limit headers
- Waits for rate limit reset
- Retries failed requests
- Continues scanning after rate limit recovery

### Access Validation
Before scanning, the tool validates:
- Organization read access
- Private repository permissions  
- Member repository access
- API token validity

## 📈 Performance Metrics

Expected scanning performance:
- **Small organization** (< 10 repos): 1-3 minutes
- **Medium organization** (10-50 repos): 5-15 minutes  
- **Large organization** (50-200 repos): 15-60 minutes
- **Enterprise organization** (200+ repos): 1-4 hours

*Performance varies based on repository size, dependencies, and parallel workers configured.*
