# Deployment Guide

## Production Deployment

### Security Considerations

⚠️ **IMPORTANT**: This application is designed for local/private use. For public deployment, additional security measures are required.

### Environment Setup

1. **Create production environment file**
   ```bash
   cp env.example .env
   ```

2. **Configure environment variables**
   ```env
   HOST=0.0.0.0
   PORT=8000
   DEBUG=False
   SECRET_KEY=your-very-secure-secret-key-here
   ALLOWED_HOSTS=yourdomain.com,www.yourdomain.com
   CORS_ORIGINS=https://yourdomain.com
   ```

### Backend Deployment

#### Using Docker (Recommended)

1. **Create Dockerfile**
   ```dockerfile
   FROM python:3.11-slim
   
   WORKDIR /app
   COPY backend/requirements.txt .
   RUN pip install -r requirements.txt
   
   COPY backend/ .
   EXPOSE 8000
   
   CMD ["python", "-m", "src.main"]
   ```

2. **Build and run**
   ```bash
   docker build -t ytdlp-webui .
   docker run -p 8000:8000 --env-file .env ytdlp-webui
   ```

#### Manual Deployment

1. **Install dependencies**
   ```bash
   cd backend
   python -m venv venv
   source venv/bin/activate
   pip install -r requirements.txt
   ```

2. **Run with production server**
   ```bash
   uvicorn src.main:app --host 0.0.0.0 --port 8000 --workers 4
   ```

### Frontend Deployment

1. **Build for production**
   ```bash
   cd frontend
   npm run build
   ```

2. **Serve with nginx**
   ```nginx
   server {
       listen 80;
       server_name yourdomain.com;
       
       location / {
           root /path/to/frontend/dist;
           try_files $uri $uri/ /index.html;
       }
       
       location /api {
           proxy_pass http://localhost:8000;
           proxy_set_header Host $host;
           proxy_set_header X-Real-IP $remote_addr;
       }
   }
   ```

### Security Hardening

#### For Public Deployment

1. **Add authentication**
   - Implement user login system
   - Add rate limiting
   - Use HTTPS only

2. **Network security**
   - Use reverse proxy (nginx/Apache)
   - Configure firewall rules
   - Enable SSL/TLS certificates

3. **File system security**
   - Restrict file permissions
   - Monitor disk usage
   - Implement file size limits

4. **Application security**
   - Add input validation
   - Implement CSRF protection
   - Use secure headers

### Monitoring

1. **Log monitoring**
   ```bash
   tail -f logs/app.log
   ```

2. **Resource monitoring**
   - CPU usage
   - Memory usage
   - Disk space
   - Network traffic

3. **Health checks**
   ```bash
   curl http://localhost:8000/health
   ```

### Backup Strategy

1. **Configuration backup**
   ```bash
   tar -czf config-backup.tar.gz .env *.md
   ```

2. **Database backup** (if using database)
   ```bash
   # Add database backup commands here
   ```

### Troubleshooting

#### Common Issues

1. **Port already in use**
   ```bash
   lsof -i :8000
   kill -9 <PID>
   ```

2. **Permission denied**
   ```bash
   chmod +x scripts/*.sh
   ```

3. **Dependencies not found**
   ```bash
   pip install -r requirements.txt
   npm install
   ```

### Performance Optimization

1. **Backend optimization**
   - Use multiple workers
   - Enable gzip compression
   - Implement caching

2. **Frontend optimization**
   - Enable gzip compression
   - Use CDN for static assets
   - Implement lazy loading

### Scaling

For high-traffic deployments:

1. **Load balancing**
   - Use nginx load balancer
   - Multiple backend instances
   - Database clustering

2. **Caching**
   - Redis for session storage
   - CDN for static files
   - Application-level caching

### Maintenance

1. **Regular updates**
   ```bash
   pip install --upgrade -r requirements.txt
   npm update
   ```

2. **Security patches**
   - Monitor security advisories
   - Update dependencies regularly
   - Apply security patches promptly

3. **Log rotation**
   ```bash
   logrotate /etc/logrotate.d/ytdlp-webui
   ```

## Support

For deployment issues:
- Check logs: `tail -f logs/app.log`
- Verify configuration: `python -c "import os; print(os.environ.get('HOST'))"`
- Test connectivity: `curl http://localhost:8000/health`

