# Troubleshooting

Solutions to common issues with Notify-MCP.

---

## Server Not Starting

**Problem:** Server fails to start or Claude can't find it.

**Solutions:**

```bash
# Test server manually
uv run python -m notify_mcp

# Check if uv is in PATH
which uv

# Use absolute paths in config
"command": "/full/path/to/uv"
```

---

## Notifications Not Appearing

**Problem:** Published notifications don't show up.

**Reason:** In stdio mode, you must retrieve notifications explicitly.

**Solution:**

```
Show me recent notifications from engineering channel
```

Or use the resource directly:
```
notification://engineering/recent
```

---

## Database Locked Error

**Problem:** `database is locked` error

**Solutions:**

```bash
# Stop all server instances
pkill -f "notify_mcp"

# Remove stale lock files
rm ~/.notify-mcp/storage.db-wal
rm ~/.notify-mcp/storage.db-shm

# Restart server
```

---

## Filters Not Working

**Problem:** Subscribed with filter but see unwanted notifications.

**Explanation:** Filters apply when **retrieving** notifications, not at publish time.

**Solution:** When you read `notification://<channel>/recent`, only notifications matching your subscription filters are returned.

---

## Import Errors

**Problem:** `ModuleNotFoundError: No module named 'mcp'`

**Solutions:**

```bash
# Install dependencies
uv sync

# Or with pip
pip install mcp pydantic

# Verify installation
uv run python -c "import mcp; print('OK')"
```

---

## Permission Errors

**Problem:** Cannot write to database file.

**Solutions:**

```bash
# Check file permissions
ls -l ~/.notify-mcp/storage.db

# Fix permissions
chmod 644 ~/.notify-mcp/storage.db
chmod 755 ~/.notify-mcp/

# Use different path
NOTIFY_MCP_SQLITE_PATH=/tmp/notify-mcp.db
```

---

## Claude Doesn't See MCP Tools

**Problem:** MCP tools don't appear in Claude.

**Solutions:**

1. Check configuration file path is correct
2. Restart Claude Desktop completely
3. Verify the `cwd` points to the correct directory
4. Check Claude logs for errors

---

## Need More Help?

- **GitHub Issues:** [Report a bug](https://github.com/osick/notify-mcp/issues)
- **Documentation:** Browse other guides
- **Examples:** Check [code examples](../examples/basic-usage.md)

---

**Still stuck?** Create an issue on GitHub with:
- Your configuration file (redact sensitive info)
- Error messages
- Steps to reproduce
- OS and Python version
