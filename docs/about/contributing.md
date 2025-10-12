# Contributing

Thank you for your interest in contributing to Notify-MCP!

---

## Ways to Contribute

### Report Bugs

Found a bug? Create an issue:

- **Title:** Clear description of the issue
- **Steps to reproduce:** Detailed reproduction steps
- **Expected behavior:** What should happen
- **Actual behavior:** What actually happens
- **Environment:** OS, Python version, MCP SDK version

[Report a bug](https://github.com/osick/notify-mcp/issues/new?labels=bug)

---

### Suggest Features

Have an idea? Create a feature request:

- **Title:** Concise feature description
- **Problem:** What problem does it solve?
- **Solution:** Proposed implementation
- **Alternatives:** Other approaches considered
- **Use case:** Real-world scenario

[Suggest a feature](https://github.com/osick/notify-mcp/issues/new?labels=feature-request)

---

### Contribute Code

Ready to code? Follow these steps:

#### 1. Fork the Repository

```bash
git clone https://github.com/your-username/notify-mcp.git
cd notify-mcp
```

#### 2. Create a Feature Branch

```bash
git checkout -b feature/your-feature-name
```

#### 3. Set Up Development Environment

```bash
uv sync
uv sync --extra dev
```

#### 4. Make Your Changes

- Follow existing code style
- Add tests for new functionality
- Update documentation

#### 5. Run Tests

```bash
# Run all tests
uv run pytest

# Run with coverage
uv run pytest --cov=src/notify_mcp

# Run specific test
uv run pytest tests/test_your_feature.py -v
```

#### 6. Run Linting

```bash
# Check code style
uv run ruff check src/

# Format code
uv run ruff format src/

# Type checking
uv run mypy src/notify_mcp
```

#### 7. Commit Your Changes

```bash
git add .
git commit -m "feat: Add your feature description"
```

**Commit message format:**
- `feat:` New feature
- `fix:` Bug fix
- `docs:` Documentation changes
- `test:` Test additions or changes
- `refactor:` Code refactoring

#### 8. Push and Create Pull Request

```bash
git push origin feature/your-feature-name
```

Then create a Pull Request on GitHub.

---

## Code Style

- **Python:** Follow PEP 8
- **Line length:** 100 characters
- **Type hints:** Required for all functions
- **Docstrings:** Google style

---

## Testing Requirements

All contributions must include tests:

- **Unit tests:** For business logic
- **Integration tests:** For component interaction
- **Coverage:** Aim for 80%+ on new code

---

## Documentation

Update documentation for:

- New features
- API changes
- Configuration changes
- Breaking changes

---

## Code Review Process

1. **Automated checks:** Tests, linting, type checking must pass
2. **Review:** Maintainer reviews code
3. **Feedback:** Address review comments
4. **Approval:** Maintainer approves
5. **Merge:** PR merged to main

---

## Development Setup

### Prerequisites

- Python 3.11+
- uv package manager
- Git

### Install Development Dependencies

```bash
uv sync --extra dev
```

### Run Development Server

```bash
uv run python -m notify_mcp
```

### Run Tests Continuously

```bash
uv run pytest-watch
```

---

## Questions?

- **Chat:** [GitHub Discussions](https://github.com/osick/notify-mcp/discussions)
- **Issues:** [GitHub Issues](https://github.com/osick/notify-mcp/issues)

---

## Code of Conduct

Be respectful, inclusive, and constructive. We welcome contributors of all skill levels.

---

**Ready to contribute? [Fork the repository →](https://github.com/osick/notify-mcp/fork)**
