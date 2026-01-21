# Deployment Guide

## Docker Deployment

### Build Image
```bash
docker build -t resume-ai:latest .
```

### Run Container
```bash
docker run -d \
  -p 8000:80 \
  --name resume-ai \
  resume-ai:latest
```

### Docker Compose (Recommended)
```yaml
version: '3.8'

services:
  api:
    build: .
    ports:
      - "8000:80"
    environment:
      - PROJECT_NAME=Resume AI
      - API_V1_STR=/api/v1
    restart: unless-stopped
    volumes:
      - ./temp_uploads:/code/temp_uploads
```

Run with:
```bash
docker-compose up -d
```

## Production Deployment

### 1. Environment Setup
```bash
# .env (production)
PROJECT_NAME="Resume AI Production"
API_V1_STR="/api/v1"
MAX_UPLOAD_SIZE=10485760
ALLOWED_ORIGINS=https://yourdomain.com
```

### 2. Reverse Proxy (Nginx)
```nginx
server {
    listen 80;
    server_name api.yourdomain.com;

    location / {
        proxy_pass http://localhost:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        
        # File upload size
        client_max_body_size 10M;
    }
}
```

### 3. SSL/TLS (Let's Encrypt)
```bash
sudo certbot --nginx -d api.yourdomain.com
```

### 4. Process Manager (systemd)
```ini
# /etc/systemd/system/resume-ai.service
[Unit]
Description=Resume AI API
After=network.target

[Service]
Type=simple
User=www-data
WorkingDirectory=/opt/resume-ai
Environment="PATH=/opt/resume-ai/venv/bin"
ExecStart=/opt/resume-ai/venv/bin/uvicorn app.main:app --host 0.0.0.0 --port 8000
Restart=always

[Install]
WantedBy=multi-user.target
```

Enable and start:
```bash
sudo systemctl enable resume-ai
sudo systemctl start resume-ai
```

## Cloud Platforms

### AWS (EC2 + ALB)
1. Launch EC2 instance (t3.medium recommended)
2. Install Docker
3. Deploy container
4. Configure ALB with health checks on `/health`
5. Set up Auto Scaling Group

### Google Cloud Run
```bash
gcloud run deploy resume-ai \
  --source . \
  --platform managed \
  --region us-central1 \
  --allow-unauthenticated
```

### Heroku
```bash
heroku create resume-ai-app
git push heroku main
```

## Monitoring

### Health Checks
```bash
# Endpoint
GET /health

# Expected response
{"status": "ok", "app_name": "Resume AI"}
```

### Logging
```python
# Already configured in app/core/logging.py
# Logs to stdout (Docker-friendly)
```

### Metrics (Optional)
Add Prometheus metrics:
```bash
pip install prometheus-fastapi-instrumentator
```

## Performance Tuning

### Gunicorn (Multi-worker)
```bash
gunicorn app.main:app \
  --workers 4 \
  --worker-class uvicorn.workers.UvicornWorker \
  --bind 0.0.0.0:8000
```

### Caching (Redis)
For production, consider caching embeddings:
```python
# Cache frequently used job descriptions
# Cache resume embeddings for repeat queries
```

## Security Checklist

- [ ] Update CORS `allow_origins` to specific domains
- [ ] Enable HTTPS/TLS
- [ ] Add rate limiting
- [ ] Set up firewall rules
- [ ] Regular security updates
- [ ] Monitor logs for suspicious activity
- [ ] Implement API authentication if needed

## Backup & Recovery

Since the system is stateless:
- No database backups needed
- Code versioned in Git
- Model files cached locally (re-downloadable)

## Troubleshooting

### High Memory Usage
- Reduce embedding batch size
- Use smaller model (e.g., `paraphrase-MiniLM-L3-v2`)
- Limit concurrent requests

### Slow Response Times
- Add caching layer
- Use GPU for embeddings (if available)
- Optimize chunking parameters

### File Upload Errors
- Check `MAX_UPLOAD_SIZE` setting
- Verify disk space in `/tmp`
- Check file permissions
