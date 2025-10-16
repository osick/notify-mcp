# HTTP Transport Deployment Guide

Deploy notify-mcp with HTTP transport for remote access and team collaboration.

---

## Overview

HTTP transport enables:
- 🌐 Remote access from anywhere on your network
- 👥 Multiple concurrent AI clients
- ☁️ Cloud deployment (Railway, Render, Fly.io, AWS, etc.)
- 🔄 Real-time collaboration across teams

**Security Note**: Community Edition has **no authentication**. Only use on trusted networks or upgrade to Enterprise for production security.

---

## Local Network Deployment

### Quick Start

```bash
# 1. Set environment variables
export NOTIFY_MCP_TRANSPORT_TYPE=http
export NOTIFY_MCP_HTTP_HOST=0.0.0.0
export NOTIFY_MCP_HTTP_PORT=8000
export NOTIFY_MCP_STORAGE_TYPE=sqlite
export NOTIFY_MCP_SQLITE_PATH=~/.notify-mcp/storage.db

# 2. Run server
uv run python -m notify_mcp
```

Server will be available at: `http://<your-ip>:8000/mcp`

### Using Example Script

```bash
# Run standalone HTTP server
uv run python examples/run_http_server.py
```

### Configuration File (.env)

Create `.env` file in project root:

```bash
NOTIFY_MCP_TRANSPORT_TYPE=http
NOTIFY_MCP_HTTP_HOST=0.0.0.0
NOTIFY_MCP_HTTP_PORT=8000
NOTIFY_MCP_STORAGE_TYPE=sqlite
NOTIFY_MCP_SQLITE_PATH=/shared/notify-mcp.db
NOTIFY_MCP_LOG_LEVEL=INFO
```

Then run:
```bash
uv run python -m notify_mcp
```

---

## Cloud Deployment

### Railway

**1. Create `Procfile`:**
```
web: uv run python -m notify_mcp
```

**2. Configure Environment Variables:**
```bash
NOTIFY_MCP_TRANSPORT_TYPE=http
NOTIFY_MCP_HTTP_HOST=0.0.0.0
NOTIFY_MCP_HTTP_PORT=$PORT  # Railway provides this
NOTIFY_MCP_STORAGE_TYPE=sqlite
NOTIFY_MCP_SQLITE_PATH=/app/data/notify-mcp.db
```

**3. Deploy:**
```bash
railway up
```

**4. Get URL:**
```bash
railway domain
# Example: https://notify-mcp-production.up.railway.app/mcp
```

---

### Render

**1. Create `render.yaml`:**
```yaml
services:
  - type: web
    name: notify-mcp
    env: python
    buildCommand: uv sync
    startCommand: uv run python -m notify_mcp
    envVars:
      - key: NOTIFY_MCP_TRANSPORT_TYPE
        value: http
      - key: NOTIFY_MCP_HTTP_HOST
        value: 0.0.0.0
      - key: NOTIFY_MCP_HTTP_PORT
        value: 8000
      - key: NOTIFY_MCP_STORAGE_TYPE
        value: sqlite
      - key: NOTIFY_MCP_SQLITE_PATH
        value: /opt/render/project/src/data/notify-mcp.db
```

**2. Deploy:**
Connect GitHub repo to Render and deploy.

**3. Access:**
`https://notify-mcp.onrender.com/mcp`

---

### Fly.io

**1. Install flyctl:**
```bash
curl -L https://fly.io/install.sh | sh
```

**2. Create `fly.toml`:**
```toml
app = "notify-mcp"
primary_region = "iad"

[build]
  builder = "paketobuildpacks/builder:base"

[env]
  NOTIFY_MCP_TRANSPORT_TYPE = "http"
  NOTIFY_MCP_HTTP_HOST = "0.0.0.0"
  NOTIFY_MCP_HTTP_PORT = "8080"
  NOTIFY_MCP_STORAGE_TYPE = "sqlite"
  NOTIFY_MCP_SQLITE_PATH = "/data/notify-mcp.db"

[http_service]
  internal_port = 8080
  force_https = true
  auto_stop_machines = true
  auto_start_machines = true
  min_machines_running = 0

[[vm]]
  cpu_kind = "shared"
  cpus = 1
  memory_mb = 256
```

**3. Deploy:**
```bash
fly launch
fly deploy
```

**4. Access:**
```bash
fly status
# Example: https://notify-mcp.fly.dev/mcp
```

---

### AWS EC2

**1. Launch EC2 Instance** (Ubuntu 22.04)

**2. SSH and Install:**
```bash
# Update system
sudo apt update && sudo apt upgrade -y

# Install uv
curl -LsSf https://astral.sh/uv/install.sh | sh

# Clone repo
git clone <repo-url>
cd notify-mcp/packages/community

# Install dependencies
uv sync
```

**3. Create systemd Service** (`/etc/systemd/system/notify-mcp.service`):
```ini
[Unit]
Description=Notify-MCP HTTP Server
After=network.target

[Service]
Type=simple
User=ubuntu
WorkingDirectory=/home/ubuntu/notify-mcp/packages/community
Environment="NOTIFY_MCP_TRANSPORT_TYPE=http"
Environment="NOTIFY_MCP_HTTP_HOST=0.0.0.0"
Environment="NOTIFY_MCP_HTTP_PORT=8000"
Environment="NOTIFY_MCP_STORAGE_TYPE=sqlite"
Environment="NOTIFY_MCP_SQLITE_PATH=/var/lib/notify-mcp/storage.db"
ExecStart=/home/ubuntu/.local/bin/uv run python -m notify_mcp
Restart=always
RestartSec=10

[Install]
WantedBy=multi-user.target
```

**4. Start Service:**
```bash
sudo systemctl daemon-reload
sudo systemctl enable notify-mcp
sudo systemctl start notify-mcp
sudo systemctl status notify-mcp
```

**5. Configure Security Group:**
- Open port 8000 (or your chosen port)
- Restrict to your IP range or VPN

**6. Access:**
`http://<ec2-public-ip>:8000/mcp`

---

## Docker Deployment

**1. Create `Dockerfile`:**
```dockerfile
FROM python:3.11-slim

WORKDIR /app

# Install uv
RUN pip install uv

# Copy project
COPY . .

# Install dependencies
RUN uv sync

# Expose port
EXPOSE 8000

# Run server
CMD ["uv", "run", "python", "-m", "notify_mcp"]
```

**2. Create `docker-compose.yml`:**
```yaml
version: '3.8'

services:
  notify-mcp:
    build: .
    ports:
      - "8000:8000"
    environment:
      - NOTIFY_MCP_TRANSPORT_TYPE=http
      - NOTIFY_MCP_HTTP_HOST=0.0.0.0
      - NOTIFY_MCP_HTTP_PORT=8000
      - NOTIFY_MCP_STORAGE_TYPE=sqlite
      - NOTIFY_MCP_SQLITE_PATH=/data/notify-mcp.db
    volumes:
      - notify-data:/data

volumes:
  notify-data:
```

**3. Run:**
```bash
docker-compose up -d
```

**4. Access:**
`http://localhost:8000/mcp`

---

## Client Configuration

### Connecting from Claude/ChatGPT

Once your HTTP server is running, configure MCP clients to connect:

**MCP Client Configuration:**
```json
{
  "mcpServers": {
    "notify-mcp-remote": {
      "url": "http://your-server:8000/mcp",
      "transport": "http"
    }
  }
}
```

**Note**: Client HTTP support depends on the MCP client implementation. Check client documentation for HTTP transport support.

---

## Health Check

Test your HTTP server:

```bash
# Check server is running
curl http://localhost:8000/mcp

# Should return MCP protocol information
```

---

## Troubleshooting

### Server Won't Start

**Check port availability:**
```bash
lsof -i :8000
# Or use different port
export NOTIFY_MCP_HTTP_PORT=3000
```

### Can't Connect Remotely

**Check firewall:**
```bash
# Ubuntu/Debian
sudo ufw allow 8000

# RHEL/CentOS
sudo firewall-cmd --add-port=8000/tcp --permanent
sudo firewall-cmd --reload
```

**Verify server is listening:**
```bash
netstat -tulpn | grep 8000
```

### Permission Denied on Port < 1024

Use port >= 1024 or run with sudo (not recommended):
```bash
export NOTIFY_MCP_HTTP_PORT=8000
```

---

## Security Recommendations

### Community Edition (Current)

- ✅ Use on **private/internal networks only**
- ✅ Use **VPN** for remote access
- ✅ Configure **firewall** to restrict IPs
- ❌ **Do NOT expose to public internet** (no authentication)

### Upgrade to Enterprise

For production deployments with public access:
- 🔐 JWT/OAuth authentication
- 📊 Monitoring and alerting
- 🏢 Multi-tenancy support
- 💾 PostgreSQL with connection pooling
- 🔒 TLS encryption
- 📈 SLA guarantees

Contact: enterprise@example.com

---

## Performance Tuning

### Concurrent Clients

Community Edition with SQLite supports **5-20 concurrent users**. For more:

**Upgrade to Enterprise Edition** with PostgreSQL:
- 20-100+ concurrent users
- Connection pooling
- Better write performance

### Storage Location

For best performance:
```bash
# Use SSD for database
NOTIFY_MCP_SQLITE_PATH=/fast-ssd/notify-mcp.db

# Or use shared network storage for team access
NOTIFY_MCP_SQLITE_PATH=/nfs/shared/notify-mcp.db
```

---

## Monitoring

### Logs

```bash
# View logs
journalctl -u notify-mcp -f

# Or docker logs
docker-compose logs -f notify-mcp
```

### Health Endpoint

Coming in future release:
```bash
curl http://localhost:8000/health
```

---

For production deployments with authentication, monitoring, and enterprise support, see **[Enterprise Edition](../../enterprise/README.enterprise.md)**.
