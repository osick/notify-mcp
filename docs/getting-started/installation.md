# Installation

This guide will help you install Notify-MCP on your system.

---

## Prerequisites

- **Python 3.11 or higher**
- **uv** package manager (recommended) or pip

---

## Install uv (Recommended)

uv is a fast Python package manager that makes installation simple:

=== "macOS / Linux"

    ```bash
    curl -LsSf https://astral.sh/uv/install.sh | sh
    ```

=== "Windows (PowerShell)"

    ```powershell
    powershell -c "irm https://astral.sh/uv/install.ps1 | iex"
    ```

---

## Install Notify-MCP

### Step 1: Clone the Repository

```bash
git clone https://github.com/osick/notify-mcp.git
cd notify-mcp/packages/community
```

### Step 2: Install Dependencies

```bash
# Using uv (recommended)
uv sync

# Or using pip
pip install -e .
```

### Step 3: Verify Installation

```bash
# Test the server starts
uv run python -m notify_mcp --help

# You should see usage information
```

---

## Next Steps

Now that Notify-MCP is installed:

1. **[Configure Your AI Assistant →](configuration.md)**
2. **[Follow the Quick Start Guide →](quick-start.md)**

---

## Troubleshooting

### Python Version Issues

```bash
# Check Python version
python --version  # Should be 3.11+

# If too old, install Python 3.11+
# macOS: brew install python@3.11
# Ubuntu: sudo apt install python3.11
# Windows: Download from python.org
```

### uv Not Found

```bash
# Add uv to PATH (after installation)
export PATH="$HOME/.cargo/bin:$PATH"

# Or use full path
~/.cargo/bin/uv sync
```

### Permission Errors

```bash
# Use virtual environment
python3.11 -m venv .venv
source .venv/bin/activate  # Linux/macOS
# .venv\Scripts\activate  # Windows

pip install -e .
```

---

For more help, see the [Troubleshooting Guide](../guides/troubleshooting.md).
