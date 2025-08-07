# Contributing to Firefly SBOM Tool

Thank you for your interest in contributing to the Firefly SBOM Tool! This document provides guidelines and instructions for contributing.

## Code of Conduct

By participating in this project, you agree to abide by our Code of Conduct, which promotes a respectful and inclusive community.

## How to Contribute

### Reporting Issues

- Check if the issue already exists in the [issue tracker](https://github.com/firefly-oss/sbom-tool/issues)
- Provide detailed information about the issue
- Include steps to reproduce, expected behavior, and actual behavior
- Add relevant labels (bug, enhancement, documentation, etc.)

### Submitting Pull Requests

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Make your changes
4. Add tests for new functionality
5. Ensure all tests pass (`pytest`)
6. Format code with Black (`black src/`)
7. Commit your changes (`git commit -m 'Add amazing feature'`)
8. Push to your branch (`git push origin feature/amazing-feature`)
9. Open a Pull Request

### Development Setup

```bash
# Clone your fork
git clone https://github.com/your-username/sbom-tool.git
cd sbom-tool

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install in development mode
pip install -e .
pip install -r requirements-dev.txt

# Run tests
pytest

# Run linting
flake8 src/
mypy src/

# Format code
black src/
```

### Adding Language Support

To add support for a new programming language:

1. Create a new scanner in `src/firefly_sbom/scanners/`
2. Inherit from the `Scanner` base class
3. Implement `detect()` and `scan()` methods
4. Add the scanner to `src/firefly_sbom/scanners/__init__.py`
5. Update the core generator to include your scanner
6. Add tests in `tests/scanners/`
7. Update documentation

Example scanner structure:

```python
from .base import Scanner
from pathlib import Path
from typing import List, Dict, Any

class MyLanguageScanner(Scanner):
    def detect(self, path: Path) -> bool:
        # Return True if this scanner can handle the repository
        return (path / "my-package-file.json").exists()
    
    def scan(self, path: Path, include_dev: bool = False) -> List[Dict[str, Any]]:
        # Scan and return list of components
        components = []
        # ... scanning logic ...
        return components
```

### Testing

- Write unit tests for new functionality
- Ensure code coverage remains above 80%
- Test with real-world repositories
- Include integration tests for new scanners

### Documentation

- Update README.md for new features
- Add docstrings to all functions and classes
- Include examples in documentation
- Update API documentation if needed

## Commit Guidelines

We follow conventional commits specification:

- `feat:` New feature
- `fix:` Bug fix
- `docs:` Documentation changes
- `style:` Code style changes (formatting, etc.)
- `refactor:` Code refactoring
- `test:` Test additions or modifications
- `chore:` Maintenance tasks

## Release Process

1. Update version in `setup.py` and `src/firefly_sbom/__init__.py`
2. Update CHANGELOG.md
3. Create a release PR
4. After merge, tag the release
5. GitHub Actions will automatically publish to PyPI

## Questions?

Feel free to reach out through:
- GitHub Issues
- Discussions
- Email: oss@firefly.com

## License

By contributing, you agree that your contributions will be licensed under the Apache License 2.0.
