# Contributing

We welcome contributions to the Energy Storage Data Processor! This document provides guidelines for contributing to the project.

## Getting Started

### Prerequisites

- Python 3.8 or higher
- pip package manager
- Git

### Setup

1. Fork the repository
2. Clone your fork:
   ```bash
   git clone https://github.com/your-username/energy-storage-processor.git
   cd energy-storage-processor
   ```
3. Set up the development environment:
   ```bash
   pip install -r requirements.txt
   pip install -e .
   ```

## Development Workflow

### 1. Create a Branch

Create a new branch for your feature or bug fix:

```bash
git checkout -b feature/amazing-feature
git checkout -b bugfix/fix-something
```

### 2. Make Changes

- Follow the existing code style
- Add tests for new functionality
- Update documentation as needed
- Ensure all tests pass

### 3. Test Your Changes

```bash
# Run all tests
pytest tests/

# Run specific test file
pytest tests/test_processors.py

# Run functionality test
python test_functionality.py

# Validate project structure
python validate_structure.py
```

### 4. Commit Your Changes

```bash
git add .
git commit -m "feat: add amazing feature"
```

Use conventional commit messages:
- `feat:` for new features
- `fix:` for bug fixes
- `docs:` for documentation changes
- `style:` for code style changes
- `refactor:` for code refactoring
- `test:` for test changes
- `chore:` for other changes

### 5. Push and Create Pull Request

```bash
git push origin feature/amazing-feature
```

Then create a Pull Request on GitHub.

## Coding Standards

### Python Code Style

- Follow PEP 8 style guidelines
- Use black for code formatting
- Use flake8 for linting
- Use mypy for type checking

```bash
# Format code
black src/

# Lint code
flake8 src/

# Type check
mypy src/
```

### Documentation

- Update README.md for new features
- Add docstrings to all public functions and classes
- Update configuration documentation
- Add examples for new functionality

### Testing

- Write unit tests for new features
- Include integration tests
- Test both success and error cases
- Aim for high test coverage

## Pull Request Guidelines

### PR Description

Include a clear description of:
- What the change does
- Why it's needed
- How it was tested
- Any breaking changes

### PR Checklist

- [ ] Code follows the project's style guidelines
- [ ] Tests pass locally and in CI
- [ ] Documentation is updated
- [ ] Commit messages follow conventional format
- [ ] PR description is clear and complete
- [ ] Changes are reviewed and approved by maintainers

### Breaking Changes

If your change includes breaking changes:
- Document them clearly in the PR description
- Update the version number according to semantic versioning
- Provide migration instructions if applicable

## Issue Guidelines

### Bug Reports

When reporting bugs, please include:
- Steps to reproduce
- Expected behavior
- Actual behavior
- Environment information (OS, Python version, etc.)
- Error messages and stack traces

### Feature Requests

When requesting features, please include:
- Clear description of the feature
- Use case and motivation
- Any implementation suggestions
- Potential alternatives considered

## Architecture Overview

The project follows a modular architecture:

```
src/
├── core/           # Core processing logic
├── readers/        # File readers (CSV, Excel)
├── processors/     # Data processing components
├── writers/        # File writers
├── utils/          # Utility functions
└── models/         # Data models
```

### Adding New Features

1. **New File Format Support**
   - Add a new reader class in `src/readers/`
   - Update the reader factory
   - Add tests
   - Update documentation

2. **New Processing Rules**
   - Update configuration schema
   - Modify processor logic
   - Add tests
   - Update examples

3. **New Output Formats**
   - Add a new writer class in `src/writers/`
   - Update the writer factory
   - Add tests
   - Update documentation

## Release Process

1. Update version number in setup.py and relevant files
2. Update CHANGELOG.md
3. Create a release on GitHub
4. Create a new tag
5. Publish to PyPI (if applicable)

## Community Guidelines

- Be respectful and constructive
- Ask questions and help others
- Share your knowledge and experience
- Participate in discussions
- Help maintain a positive environment

## Getting Help

If you need help:
- Check the documentation
- Search existing issues
- Create a new issue with clear description
- Join our community discussions

Thank you for contributing to the Energy Storage Data Processor!