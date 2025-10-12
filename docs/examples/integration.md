# Integration Examples

Integrate Notify-MCP with external tools and services.

---

## CI/CD Integration

### GitHub Actions

```yaml
- name: Notify team of deployment
  run: |
    python - << 'EOF'
    import asyncio
    from mcp import ClientSession
    # ... MCP client code to publish deployment notification
    EOF
```

---

## Monitoring Integration

### Datadog Webhook

```python
# Datadog webhook → Notify-MCP
@app.route('/webhook/datadog', methods=['POST'])
def datadog_webhook():
    alert = request.json
    # Publish alert to Notify-MCP
    publish_notification(
        channel="production",
        title=f"Alert: {alert['title']}",
        body=alert['body'],
        priority="critical"
    )
```

---

## Custom Integrations

See complete integration examples in: [Usage Guide](../USAGE_GUIDE.md)
