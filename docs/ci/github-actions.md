# GitHub Actions CI Guide

This guide shows how to install and run Firefly SBOM Tool in GitHub Actions to generate SBOMs and perform security audits for the repository that triggers the workflow, and optionally for entire GitHub organizations.

## Minimal: Current Repository Scan

Runs on every push/PR, installs via the official install script from the repository, scans the current repo, and uploads reports.

```yaml
name: SBOM Scan

on:
  push:
    branches: [ main ]
  pull_request:
    branches: [ main ]
  workflow_dispatch:

jobs:
  sbom:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-python@v5
        with:
          python-version: '3.10'
      - name: Install Firefly SBOM Tool
        run: |
          curl -sSL https://raw.githubusercontent.com/firefly-oss/sbom-tool/main/install.sh | bash
          echo "$HOME/.local/bin" >> $GITHUB_PATH
      - name: Run SBOM scan (current repo)
        run: firefly-sbom scan --path . --audit --format cyclonedx-json --format html --output sbom-report
      - name: Upload artifacts
        uses: actions/upload-artifact@v4
        with:
          name: sbom-reports
          path: sbom-report*
```

## Matrix: Multiple Python Versions

```yaml
name: SBOM Scan (Matrix)

on: [push, pull_request]

jobs:
  sbom:
    runs-on: ubuntu-latest
    strategy:
      fail-fast: false
      matrix:
        python-version: [ '3.8', '3.10', '3.12' ]
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-python@v5
        with:
          python-version: ${{ matrix.python-version }}
      - name: Install Firefly SBOM Tool
        run: |
          curl -sSL https://raw.githubusercontent.com/firefly-oss/sbom-tool/main/install.sh | bash
          echo "$HOME/.local/bin" >> $GITHUB_PATH
      - run: firefly-sbom scan --path . --audit --format cyclonedx-json --output sbom-${{ matrix.python-version }}
      - uses: actions/upload-artifact@v4
        with:
          name: sbom-reports
          path: sbom-*
```

## Organization Scan (Scheduled)

Requires a PAT with repo and read:org scopes in repo secret GITHUB_TOKEN_ORG (do not overwrite default GITHUB_TOKEN).

```yaml
name: Organization SBOM Scan (Scheduled)

on:
  schedule:
    - cron: '0 3 * * 1' # Mondays at 03:00 UTC
  workflow_dispatch:

jobs:
  scan-org:
    runs-on: ubuntu-latest
    permissions:
      contents: read
      issues: write
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-python@v5
        with:
          python-version: '3.10'
      - name: Install Firefly SBOM Tool
        run: |
          curl -sSL https://raw.githubusercontent.com/firefly-oss/sbom-tool/main/install.sh | bash
          echo "$HOME/.local/bin" >> $GITHUB_PATH
      - name: Run org scan
        env:
          GITHUB_TOKEN: ${{ secrets.GITHUB_TOKEN_ORG }}
        run: |
          mkdir -p reports
          firefly-sbom scan-org --org your-org \
            --audit --parallel 6 \
            --format cyclonedx-json --format html \
            --output-dir reports
      - uses: actions/upload-artifact@v4
        with:
          name: org-sbom-reports
          path: reports
```

## Caching Dependencies

If your scans invoke language-native tools (npm, maven, go), caching can speed up runs. Example for Python projects:

```yaml
- uses: actions/cache@v4
  with:
    path: ~/.cache/pip
    key: ${{ runner.os }}-pip-${{ hashFiles('**/requirements*.txt') }}
    restore-keys: |
      ${{ runner.os }}-pip-
```

## Failing Builds on Critical Vulnerabilities

You can choose to fail the job if critical vulnerabilities are found using the configuration file or CLI.

```yaml
- name: Run SBOM scan and fail on critical
  run: |
    firefly-sbom scan --path . --audit --format cyclonedx-json --output sbom
    python - <<'PY'
    import json, sys
    data = json.load(open('sbom.json')) if os.path.exists('sbom.json') else {}
    vulns = data.get('vulnerabilities', [])
    if any((v.get('severity') or '').lower() == 'critical' for v in vulns):
        print('Critical vulnerabilities found. Failing build.')
        sys.exit(1)
    PY
```

Alternatively, set audit.fail_on_critical: true in your config file.

## Recommended Permissions

For repository scans, the default GITHUB_TOKEN with contents: read is enough. For creating issues, set permissions:

```yaml
permissions:
  contents: read
  issues: write
```

## Tips

- Prefer installing via the official install script for consistency with local usage and to ensure latest repository installation path works.
- Use workflow_dispatch to allow manual runs.
- Store organization PATs in repository or organization secrets and reference via env.
- Upload artifacts to inspect detailed HTML reports.

