# Firefly SBOM Tool - Supported Scanners

## Overview
The Firefly SBOM Tool supports comprehensive dependency scanning across multiple programming languages and frameworks. Each scanner is designed to handle the specific package management systems and dependency formats of its target technology.

## Implemented Scanners

### 1. Java/Maven Scanner (`maven.py`)
**Detects:** `pom.xml` files  
**Features:**
- Multi-module Maven project support
- Parses both `pom.xml` and Maven dependency tree
- Supports Maven CLI integration when available
- Handles transitive dependencies
- Extracts scope information (compile, runtime, test, provided)

**Supported Files:**
- `pom.xml`
- Maven dependency tree output

### 2. Python Scanner (`python.py`)
**Detects:** Python package files  
**Features:**
- Multiple package manager support (pip, Poetry, Pipenv)
- Parses `requirements.txt`, `setup.py`, `pyproject.toml`, `Pipfile`, `Pipfile.lock`, `poetry.lock`
- Handles development dependencies
- Supports version range specifications
- Extracts package metadata from lock files

**Supported Files:**
- `requirements*.txt`
- `setup.py`
- `setup.cfg`
- `pyproject.toml`
- `Pipfile` / `Pipfile.lock`
- `poetry.lock`

### 3. Node.js/TypeScript/Angular Scanner (`node.py`)
**Detects:** `package.json` files  
**Features:**
- Full npm, yarn, and pnpm support
- Parses lock files for exact versions (`package-lock.json`, `yarn.lock`, `pnpm-lock.yaml`)
- Framework detection (Angular, React, Vue, Next.js, TypeScript)
- Handles different dependency types (dependencies, devDependencies, peerDependencies, optionalDependencies)
- Supports scoped packages (@org/package)
- Integrity hash extraction from lock files

**Supported Files:**
- `package.json`
- `package-lock.json`
- `yarn.lock`
- `pnpm-lock.yaml`
- `angular.json`
- `tsconfig.json`

### 4. Flutter/Dart Scanner (`flutter.py`)
**Detects:** `pubspec.yaml` files  
**Features:**
- Parses `pubspec.yaml` and `pubspec.lock`
- Handles Flutter SDK and Dart SDK versions
- Supports git and path dependencies
- Extracts exact versions from lock files
- Development dependency support
- Flutter CLI integration when available

**Supported Files:**
- `pubspec.yaml`
- `pubspec.lock`

### 5. Go Scanner (`go.py`)
**Detects:** `go.mod` files  
**Features:**
- Parses `go.mod` and `go.sum`
- Full `go list` command integration
- Handles replace directives
- Checksum verification from `go.sum`
- Supports indirect dependencies
- Workspace support
- Build tool dependency detection (`tools.go`)

**Supported Files:**
- `go.mod`
- `go.sum`
- `tools.go`

### 6. Ruby Scanner (`ruby.py`)
**Detects:** `Gemfile` files  
**Features:**
- Parses `Gemfile` and `Gemfile.lock`
- Bundler integration when available
- Group-based dependencies (development, test)
- Ruby version detection
- Handles version specifications
- Bundler version tracking

**Supported Files:**
- `Gemfile`
- `Gemfile.lock`

### 7. Rust Scanner (`rust.py`)
**Detects:** `Cargo.toml` files  
**Features:**
- Parses `Cargo.toml` and `Cargo.lock`
- Cargo metadata integration
- Workspace support
- Build dependencies
- Target-specific dependencies
- Feature flags support
- Git and path dependencies
- Checksum verification

**Supported Files:**
- `Cargo.toml`
- `Cargo.lock`

## Scanner Architecture

### Base Scanner Class
All scanners inherit from the `Scanner` base class which provides:
- Component creation with standardized format
- Package URL (purl) generation
- License normalization
- Hash calculation utilities
- JSON file parsing helpers

### Common Features Across All Scanners
1. **Exact Version Resolution**: Prefer lock files over manifest files
2. **CLI Tool Integration**: Use native tools when available for better accuracy
3. **Fallback Parsing**: Direct file parsing when tools aren't available
4. **Development Dependencies**: Optional inclusion via `include_dev` flag
5. **Scope Detection**: Differentiate between direct, transitive, dev, and optional dependencies
6. **Error Resilience**: Continue scanning even if individual components fail

## Output Format

Each scanner produces components in a standardized format:

```json
{
  "name": "package-name",
  "version": "1.2.3",
  "type": "library",
  "scope": "direct|transitive|dev|optional",
  "purl": "pkg:type/namespace/name@version",
  "license": "Apache-2.0",
  "description": "Package description",
  "hashes": [
    {"alg": "sha256", "content": "hash-value"}
  ],
  "repository": "https://github.com/org/repo",
  "author": "Author Name"
}
```

## Adding New Scanners

To add support for a new language or framework:

1. Create a new scanner file in `src/firefly_sbom/scanners/`
2. Inherit from the `Scanner` base class
3. Implement required methods:
   - `detect(path)`: Check if the scanner applies
   - `scan(path, include_dev)`: Perform the actual scanning
4. Add the scanner to `scanners/__init__.py`
5. Register in `core.py` `_initialize_scanners()` method
6. Add detection logic to `detect_technology_stack()` in `core.py`

## Usage Examples

### Scanning a Multi-Language Project

```python
from firefly_sbom import SBOMGenerator

generator = SBOMGenerator()

# Automatically detects all technologies
sbom_data = generator.scan_repository(
    path="/path/to/repo",
    include_dev=True,
    audit=True
)

# Access technology-specific components
for component in sbom_data['components']:
    print(f"{component['name']}@{component['version']} ({component['purl']})")
```

### Direct Scanner Usage

```python
from firefly_sbom.scanners import PythonScanner
from firefly_sbom.config import Config

scanner = PythonScanner(Config())
components = scanner.scan(Path("/path/to/python/project"), include_dev=False)
```

## Performance Considerations

- **Parallel Scanning**: Multiple technologies are scanned concurrently
- **Caching**: Results can be cached to avoid re-scanning
- **Lock File Priority**: Lock files are parsed first for better performance
- **Lazy Loading**: CLI tools are only invoked when necessary

## License

Copyright 2024 Firefly OSS  
Licensed under the Apache License, Version 2.0
