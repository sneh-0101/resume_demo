# Deployment Guide - Flask Resume Analyzer

## 🚀 Quick Deployment Options

### Option 1: Local Development (5 minutes)

```bash
# 1. Install dependencies
pip install -r requirements_flask.txt
python -m spacy download en_core_web_sm

# 2. Run server
python run.py

# 3. Visit http://localhost:5000
```

### Option 2: Heroku Deployment (10 minutes)

**Prerequisites**: Heroku CLI installed

```bash
# 1. Create Procfile
echo "web: gunicorn -w 4 -b 0.0.0.0:\$PORT run:app" > Procfile

# 2. Create runtime.txt
echo "python-3.11.0" > runtime.txt

# 3. Login to Heroku
heroku login

# 4. Create app
heroku create your-app-name

# 5. Add PostgreSQL
heroku addons:create heroku-postgresql:hobby-dev

# 6. Set environment variables
heroku config:set SECRET_KEY=your-secure-key
heroku config:set FLASK_ENV=production

# 7. Deploy
git push heroku main

# 8. Initialize database
heroku run python -c "from flask_app import create_app, db; app = create_app(); app.app_context().push(); db.create_all()"
```

### Option 3: Docker Deployment (15 minutes)

**Create Dockerfile:**
```dockerfile
FROM python:3.11-slim

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements
COPY requirements_flask.txt .

# Install Python packages
RUN pip install --no-cache-dir -r requirements_flask.txt
RUN python -m spacy download en_core_web_sm

# Copy application
COPY . .

# Create uploads directory
RUN mkdir -p uploads

# Expose port
EXPOSE 5000

# Run application
CMD ["gunicorn", "-w", "4", "-b", "0.0.0.0:5000", "run:app"]
```

**Build and run:**
```bash
# Build image
docker build -t resume-analyzer .

# Run container
docker run -p 5000:5000 \
  -e SECRET_KEY=your-key \
  -e DATABASE_URL=sqlite:///app.db \
  resume-analyzer

# Visit http://localhost:5000
```

**Docker Compose (with PostgreSQL):**
```yaml
version: '3.8'

services:
  web:
    build: .
    ports:
      - "5000:5000"
    environment:
      - FLASK_ENV=production
      - SECRET_KEY=your-secret-key
      - DATABASE_URL=postgresql://user:password@db:5432/resume_analyzer
    depends_on:
      - db
    volumes:
      - ./uploads:/app/uploads

  db:
    image: postgres:15
    environment:
      - POSTGRES_USER=user
      - POSTGRES_PASSWORD=password
      - POSTGRES_DB=resume_analyzer
    volumes:
      - postgres_data:/var/lib/postgresql/data

volumes:
  postgres_data:
```

Run with: `docker-compose up`

### Option 4: AWS EC2 Deployment (20 minutes)

**1. Launch EC2 Instance**
- Ubuntu 22.04 LTS
- t2.micro (free tier eligible)
- Security group: Allow HTTP (80), HTTPS (443), SSH (22)

**2. SSH into instance**
```bash
ssh -i your-key.pem ubuntu@your-instance-ip
```

**3. Install dependencies**
```bash
sudo apt update
sudo apt install -y python3-pip python3-venv git nginx

# Install spaCy requirements
sudo apt install -y build-essential
```

**4. Clone and setup**
```bash
git clone https://github.com/your-repo.git
cd AI-Driven-Resume-Analyzer
python3 -m venv venv
source venv/bin/activate
pip install -r requirements_flask.txt
python -m spacy download en_core_web_sm
```

**5. Configure Gunicorn**
Create `/home/ubuntu/resume_analyzer/gunicorn_config.py`:
```python
import multiprocessing

bind = "127.0.0.1:5000"
workers = multiprocessing.cpu_count() * 2 + 1
max_requests = 1000
timeout = 30
```

**6. Create systemd service**
Create `/etc/systemd/system/resume-analyzer.service`:
```ini
[Unit]
Description=Resume Analyzer
After=network.target

[Service]
User=ubuntu
WorkingDirectory=/home/ubuntu/AI-Driven-Resume-Analyzer
Environment="PATH=/home/ubuntu/AI-Driven-Resume-Analyzer/venv/bin"
ExecStart=/home/ubuntu/AI-Driven-Resume-Analyzer/venv/bin/gunicorn -c gunicorn_config.py run:app

[Install]
WantedBy=multi-user.target
```

**7. Enable and start service**
```bash
sudo systemctl daemon-reload
sudo systemctl enable resume-analyzer
sudo systemctl start resume-analyzer
```

**8. Configure Nginx**
Create `/etc/nginx/sites-available/resume-analyzer`:
```nginx
server {
    listen 80;
    server_name your-domain.com;

    location / {
        proxy_pass http://127.0.0.1:5000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }

    location /static/ {
        alias /home/ubuntu/AI-Driven-Resume-Analyzer/flask_app/static/;
    }
}
```

**9. Enable and test Nginx**
```bash
sudo ln -s /etc/nginx/sites-available/resume-analyzer /etc/nginx/sites-enabled/
sudo nginx -t
sudo systemctl restart nginx
```

**10. Setup SSL with Let's Encrypt**
```bash
sudo apt install -y certbot python3-certbot-nginx
sudo certbot --nginx -d your-domain.com
```

### Option 5: Google Cloud Platform Deployment

**1. Create Cloud Run service**
```bash
gcloud run deploy resume-analyzer \
  --source . \
  --platform managed \
  --region us-central1 \
  --allow-unauthenticated
```

**2. Configure Cloud SQL**
```bash
gcloud sql instances create resume-analyzer-db \
  --database-version POSTGRES_15 \
  --tier db-f1-micro \
  --region us-central1
```

**3. Set environment variables**
```bash
gcloud run services update resume-analyzer \
  --set-env-vars DATABASE_URL=postgresql://...
```

## 🔒 Production Checklist

### Security
- [ ] Change SECRET_KEY to secure random value
- [ ] Set DEBUG=False
- [ ] Use environment variables for all secrets
- [ ] Enable HTTPS/SSL
- [ ] Configure CORS if needed
- [ ] Set secure cookie flags
- [ ] Use strong database password

### Performance
- [ ] Use production database (PostgreSQL)
- [ ] Configure Gunicorn workers (2 × CPU cores + 1)
- [ ] Enable gzip compression
- [ ] Configure caching headers
- [ ] Use CDN for static files

### Monitoring
- [ ] Setup error logging (Sentry)
- [ ] Configure application monitoring (New Relic)
- [ ] Setup health checks
- [ ] Configure log aggregation
- [ ] Setup alerts for errors

### Backup & Recovery
- [ ] Configure database backups
- [ ] Test backup recovery
- [ ] Setup upload directory backups
- [ ] Document recovery procedures

## 📊 Performance Tuning

### Database Optimization
```python
# Add indexes to frequently queried fields
class User(db.Model):
    username = db.Column(db.String(80), unique=True, index=True)
    email = db.Column(db.String(120), unique=True, index=True)
```

### Caching Strategy
```python
from flask_caching import Cache

cache = Cache(app, config={'CACHE_TYPE': 'redis'})

@app.route('/analysis/history')
@cache.cached(timeout=300)
def history():
    return render_template('analysis/history.html', ...)
```

### Database Connection Pooling
```python
app.config['SQLALCHEMY_ENGINE_OPTIONS'] = {
    'pool_size': 10,
    'pool_recycle': 3600,
    'pool_pre_ping': True,
}
```

## 🚨 Troubleshooting Deployment

**Issue: Port already in use**
```bash
# Find process using port
lsof -i :5000
# Kill process
kill -9 <PID>
```

**Issue: Module not found**
```bash
# Ensure all dependencies installed
pip install -r requirements_flask.txt
# Verify virtual environment activated
which python
```

**Issue: Database connection error**
```bash
# Check DATABASE_URL environment variable
echo $DATABASE_URL
# Test connection
python -c "from flask_app import create_app; app = create_app(); app.app_context().push()"
```

**Issue: spaCy model not found**
```bash
python -m spacy download en_core_web_sm
```

## 📈 Scaling Strategies

### Horizontal Scaling
- Use load balancer (nginx, HAProxy)
- Run multiple Gunicorn instances
- Separate database server
- Cache layer (Redis)

### Database Optimization
- Migrate to PostgreSQL
- Add read replicas
- Archive old data
- Optimize queries

### Static File Serving
- Use CDN (CloudFlare, Akamai)
- Enable compression
- Set cache headers
- Minify CSS/JS

## 📚 Documentation

For more information:
- [FLASK_README.md](FLASK_README.md) - Comprehensive guide
- [QUICK_START.md](QUICK_START.md) - Quick setup
- [config.py](flask_app/config.py) - Configuration details

---

**Deployment Status**: ✅ Ready for Production
