# LLM Council - Quick Reference Guide

## 🚀 Quick Commands

### Setup

```bash
# PowerShell (Windows)
.\setup.ps1

# Bash (Linux/Mac)
chmod +x setup.sh
./setup.sh
```

### Start Services

```bash
# PC1 (Chairman + Backend + Frontend)
docker compose -f docker-compose.pc1.yaml up -d

# PC2 (Council)
docker compose -f docker-compose.pc2.yaml up -d

# Single PC (all services)
docker compose -f docker-compose.full.yaml up -d
```

### Stop Services

```bash
docker compose -f docker-compose.pc1.yaml down
docker compose -f docker-compose.pc2.yaml down
```

### View Logs

```bash
# All services
docker compose logs -f

# Specific service
docker logs llm-council-backend -f
docker logs llm-council-ollama-chairman -f
docker logs llm-council-ollama-council -f
```

### Pull Models

```bash
# Chairman (PC1)
docker exec llm-council-ollama-chairman ollama pull qwen2.5:1.5b

# Council (PC2)
docker exec llm-council-ollama-council ollama pull llama3.2:1b
docker exec llm-council-ollama-council ollama pull gemma2:2b
docker exec llm-council-ollama-council ollama pull phi3:3.8b
```

### Check Model Status

```bash
# List available models
docker exec llm-council-ollama-chairman ollama list
docker exec llm-council-ollama-council ollama list

# Check Ollama API
curl http://localhost:11434/api/tags
```

## 🔧 Troubleshooting Commands

### Check Container Status

```bash
docker ps -a
```

### Restart Services

```bash
docker compose restart
```

### Remove and Rebuild

```bash
docker compose down
docker compose up -d --build
```

### Check Network Connectivity

```bash
# From PC1, test connection to PC2
curl http://<PC2_IP>:11434/api/tags

# Test from within container
docker exec llm-council-backend curl http://<PC2_IP>:11434/api/tags
```

### View Environment Variables

```bash
docker exec llm-council-backend env | grep -E "(CHAIRMAN|COUNCIL)"
```

### Clear Everything and Start Fresh

```bash
# Stop all services
docker compose down

# Remove volumes (WARNING: deletes all model data)
docker volume rm llm-council-ollama-chairman llm-council-ollama-council

# Restart
docker compose up -d
```

## 📊 Monitoring

### Resource Usage

```bash
# CPU and memory usage
docker stats

# Disk usage
docker system df
```

### Service Health

```bash
# Check if services are responding
curl http://localhost:8000/
curl http://localhost:11434/api/tags
```

## 🔐 Firewall Configuration

### Windows (PowerShell - Run as Administrator)

```powershell
# Allow Ollama port
New-NetFirewallRule -DisplayName "Ollama LLM Council" -Direction Inbound -LocalPort 11434 -Protocol TCP -Action Allow

# Check rule
Get-NetFirewallRule -DisplayName "Ollama LLM Council"
```

### Linux (Ubuntu/Debian)

```bash
# Allow Ollama port
sudo ufw allow 11434/tcp

# Check status
sudo ufw status
```

### macOS

```bash
# Firewall settings via System Preferences
# Allow incoming connections for Docker
```

## 📝 Environment Variables Reference

| Variable | Default | Description |
|----------|---------|-------------|
| `CHAIRMAN_IP` | localhost | IP of Chairman Ollama instance |
| `CHAIRMAN_PORT` | 11434 | Port for Chairman Ollama |
| `CHAIRMAN_MODEL` | qwen2.5:1.5b | Model for synthesis |
| `COUNCIL_IP` | localhost | IP of Council Ollama instance |
| `COUNCIL_PORT` | 11434 | Port for Council Ollama |

## 🌐 URLs

| Service | URL | Description |
|---------|-----|-------------|
| Frontend | http://localhost:5173 | Web interface |
| Backend API | http://localhost:8000 | FastAPI backend |
| API Docs | http://localhost:8000/docs | Interactive API documentation |
| Chairman Ollama | http://localhost:11434 | Chairman LLM API |
| Council Ollama | http://\<PC2_IP\>:11434 | Council LLM API |

## 📦 Model Sizes

| Model | Size | RAM Required |
|-------|------|--------------|
| llama3.2:1b | ~1.3GB | 4GB+ |
| gemma2:2b | ~1.6GB | 4GB+ |
| phi3:3.8b | ~2.3GB | 6GB+ |
| qwen2.5:1.5b | ~1.0GB | 4GB+ |
| mistral:7b | ~4.1GB | 8GB+ |

## 🔄 Common Workflows

### Adding a New Model

1. Update `backend/config.py`:
   ```python
   CouncilModel(
       ip=COUNCIL_IP,
       port=COUNCIL_PORT,
       model_name="new-model:tag",
       role=Role.COUNCILOR,
       custom_name="Councilor_4"
   )
   ```

2. Pull the model:
   ```bash
   docker exec llm-council-ollama-council ollama pull new-model:tag
   ```

3. Restart backend:
   ```bash
   docker compose restart backend
   ```

### Changing Chairman Model

1. Update `.env`:
   ```
   CHAIRMAN_MODEL=llama3.2:3b
   ```

2. Pull new model:
   ```bash
   docker exec llm-council-ollama-chairman ollama pull llama3.2:3b
   ```

3. Restart services:
   ```bash
   docker compose restart
   ```

### Moving to Production

1. Use strong firewall rules
2. Enable HTTPS for frontend
3. Add authentication to backend
4. Set up monitoring and logging
5. Regular backups of `data/conversations/`
6. Use GPU acceleration if available

## 📚 Additional Resources

- [Full README](README_NEW.md)
- [Deployment Guide](DEPLOYMENT.md)
- [Ollama Documentation](https://ollama.ai/docs)
- [FastAPI Documentation](https://fastapi.tiangolo.com/)
- [Docker Documentation](https://docs.docker.com/)

## 🆘 Getting Help

1. Check logs: `docker compose logs -f`
2. Verify network connectivity
3. Ensure models are downloaded
4. Check firewall settings
5. See DEPLOYMENT.md for detailed troubleshooting
6. Open an issue on GitHub

---

**Keep this file handy for quick reference! 📌**
