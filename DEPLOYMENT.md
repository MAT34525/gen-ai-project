# LLM Council - 2-PC Deployment Guide

This guide explains how to deploy the LLM Council system across two PCs with a distributed architecture:
- **PC1**: Chairman LLM + Backend + Frontend
- **PC2**: Council LLMs (3+ models)

## Architecture Overview

```
┌─────────────────────────────────────┐
│           PC1 (Chairman)            │
│  ┌──────────┐  ┌────────────────┐  │
│  │ Frontend │─▶│ Backend (API)  │  │
│  │  :5173   │  │    :8000       │  │
│  └──────────┘  └────────┬───────┘  │
│                         │           │
│  ┌──────────────────────▼────────┐ │
│  │  Ollama Chairman              │ │
│  │  :11434                       │ │
│  │  Model: qwen2.5:1.5b          │ │
│  │  Role: Synthesis only         │ │
│  └───────────────────────────────┘ │
└─────────────────┬───────────────────┘
                  │ Network
                  │
┌─────────────────▼───────────────────┐
│           PC2 (Council)             │
│  ┌───────────────────────────────┐ │
│  │  Ollama Council               │ │
│  │  :11434                       │ │
│  │                               │ │
│  │  Models:                      │ │
│  │  - llama3.2:1b (Councilor_1) │ │
│  │  - gemma2:2b   (Councilor_2) │ │
│  │  - phi3:3.8b   (Councilor_3) │ │
│  │                               │ │
│  │  Role: Initial responses &    │ │
│  │        Peer review            │ │
│  └───────────────────────────────┘ │
└─────────────────────────────────────┘
```

## Prerequisites

### Both PCs
- Docker and Docker Compose installed
- Network connectivity between PC1 and PC2
- Sufficient RAM (8GB+ recommended per PC)
- (Optional) NVIDIA GPU with Docker GPU support for faster inference

### Network Requirements
- PC1 must be able to reach PC2 on port 11434
- Firewall rules allowing communication between PCs
- Static IP addresses or reliable hostname resolution

## Quick Start

### Step 1: Get IP Addresses

On **PC2**, find your IP address:

**Windows:**
```powershell
ipconfig
```
Look for "IPv4 Address" (e.g., 192.168.1.101)

**Linux/Mac:**
```bash
ip addr show
# or
ifconfig
```

### Step 2: Set Up PC2 (Council)

1. Clone the repository on PC2:
```bash
git clone <your-repo-url>
cd gen-ai-project
```

2. Start the Council Ollama instance:
```bash
docker-compose -f docker-compose.pc2.yaml up -d
```

3. Verify Ollama is running:
```bash
docker ps
curl http://localhost:11434/api/tags
```

4. Pull the council models (this will take some time):
```bash
docker exec llm-council-ollama-council ollama pull llama3.2:1b
docker exec llm-council-ollama-council ollama pull gemma2:2b
docker exec llm-council-ollama-council ollama pull phi3:3.8b
```

5. Verify models are available:
```bash
docker exec llm-council-ollama-council ollama list
```

### Step 3: Set Up PC1 (Chairman + Backend + Frontend)

1. Clone the repository on PC1:
```bash
git clone <your-repo-url>
cd gen-ai-project
```

2. Create `.env` file with PC2's IP address:
```bash
# Copy the example file
cp .env.example .env

# Edit .env and set:
CHAIRMAN_IP=localhost
CHAIRMAN_PORT=11434
CHAIRMAN_MODEL=qwen2.5:1.5b

# IMPORTANT: Set this to PC2's actual IP address
COUNCIL_IP=192.168.1.101
COUNCIL_PORT=11434
```

Alternatively, use environment variables:
```bash
export PC2_IP=192.168.1.101
```

3. Start PC1 services:
```bash
docker-compose -f docker-compose.pc1.yaml up -d
```

4. Pull the Chairman model:
```bash
docker exec llm-council-ollama-chairman ollama pull qwen2.5:1.5b
```

5. Verify all services are running:
```bash
docker ps
```
You should see:
- llm-council-frontend
- llm-council-backend
- llm-council-ollama-chairman

### Step 4: Access the Application

Open your web browser on PC1 and navigate to:
```
http://localhost:5173
```

## Testing the Setup

### Test 1: Check Ollama Connectivity

From PC1, test connection to PC2's Ollama:
```bash
curl http://<PC2_IP>:11434/api/tags
```

### Test 2: Submit a Query

1. Open the web interface at http://localhost:5173
2. Submit a test query, for example:
   ```
   Ce produit est utilisé par 90% des experts, donc il doit être le meilleur.
   ```
3. Wait for the 3-stage process to complete:
   - Stage 1: Council models respond (from PC2)
   - Stage 2: Council models review each other
   - Stage 3: Chairman synthesizes (from PC1)

### Test 3: Verify Distributed Processing

Check logs to confirm models are being queried on different machines:

**PC1 Backend logs:**
```bash
docker logs llm-council-backend
```

**PC2 Council logs:**
```bash
docker logs llm-council-ollama-council
```

## Alternative Setup: Without Docker

### PC2 (Council)

1. Install Ollama:
```bash
curl -fsSL https://ollama.com/install.sh | sh
```

2. Start Ollama (it runs as a service automatically)

3. Pull council models:
```bash
ollama pull llama3.2:1b
ollama pull gemma2:2b
ollama pull phi3:3.8b
```

4. Make sure Ollama is accessible from network:
```bash
# Edit /etc/systemd/system/ollama.service (Linux)
# Add: Environment="OLLAMA_HOST=0.0.0.0"

sudo systemctl restart ollama
```

### PC1 (Chairman + Backend + Frontend)

1. Install Ollama:
```bash
curl -fsSL https://ollama.com/install.sh | sh
```

2. Pull chairman model:
```bash
ollama pull qwen2.5:1.5b
```

3. Set up Python backend:
```bash
cd backend
pip install -r requirements.txt

# Set environment variables
export CHAIRMAN_IP=localhost
export COUNCIL_IP=192.168.1.101

# Run backend
python -m uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

4. Set up Frontend:
```bash
cd frontend
npm install
npm run dev
```

## Troubleshooting

### Issue: Cannot connect to PC2 from PC1

**Solutions:**
1. Check firewall on PC2:
   ```bash
   # Windows
   New-NetFirewallRule -DisplayName "Ollama" -Direction Inbound -LocalPort 11434 -Protocol TCP -Action Allow
   
   # Linux
   sudo ufw allow 11434/tcp
   ```

2. Verify Ollama is listening on all interfaces:
   ```bash
   docker exec llm-council-ollama-council netstat -tlnp | grep 11434
   ```

3. Test network connectivity:
   ```bash
   # From PC1
   telnet <PC2_IP> 11434
   ```

### Issue: Models are slow or timing out

**Solutions:**
1. Increase timeout in backend config (default: 180s)
2. Use smaller models
3. Enable GPU acceleration (see GPU Setup section)
4. Reduce number of council models

### Issue: "Model not found" errors

**Solution:**
Pull models manually:
```bash
# On PC2
docker exec llm-council-ollama-council ollama pull llama3.2:1b

# On PC1
docker exec llm-council-ollama-chairman ollama pull qwen2.5:1.5b
```

### Issue: Backend cannot connect to Ollama instances

**Solution:**
Check environment variables are set correctly:
```bash
docker exec llm-council-backend env | grep -E "(CHAIRMAN|COUNCIL)"
```

## GPU Acceleration (Optional)

If you have NVIDIA GPUs, enable GPU support for faster inference:

1. Install NVIDIA Container Toolkit:
```bash
# Ubuntu/Debian
distribution=$(. /etc/os-release;echo $ID$VERSION_ID)
curl -s -L https://nvidia.github.io/nvidia-docker/gpgkey | sudo apt-key add -
curl -s -L https://nvidia.github.io/nvidia-docker/$distribution/nvidia-docker.list | sudo tee /etc/apt/sources.list.d/nvidia-docker.list

sudo apt-get update && sudo apt-get install -y nvidia-container-toolkit
sudo systemctl restart docker
```

2. Uncomment GPU sections in docker-compose files:
```yaml
deploy:
  resources:
    reservations:
      devices:
        - driver: nvidia
          count: 1
          capabilities: [gpu]
```

3. Restart services:
```bash
docker-compose -f docker-compose.pc1.yaml down
docker-compose -f docker-compose.pc1.yaml up -d
```

## Customization

### Change Models

Edit `backend/config.py`:
```python
CHAIRMAN_MODEL = "llama3.2:3b"  # Use a different chairman model

# Add/modify council models
COUNCIL_BASE_MODELS = [
    CouncilModel(
        ip=COUNCIL_IP,
        port=COUNCIL_PORT,
        model_name="mistral:7b",  # Use different model
        role=Role.COUNCILOR,
        custom_name="Councilor_1"
    ),
    # ... more models
]
```

### Change Ports

If port 11434 is already in use:

1. Update `.env`:
   ```
   CHAIRMAN_PORT=11435
   COUNCIL_PORT=11436
   ```

2. Update docker-compose files to expose the new ports

## Production Considerations

1. **Security:**
   - Use HTTPS for frontend
   - Add authentication to backend API
   - Restrict Ollama to internal network only

2. **Performance:**
   - Use GPU acceleration
   - Increase RAM allocation for Docker
   - Use SSD storage for model files

3. **Monitoring:**
   - Set up logging aggregation
   - Monitor resource usage (RAM, GPU, CPU)
   - Track response times

4. **Backup:**
   - Back up conversation data (`data/conversations/`)
   - Document your configuration

## Next Steps

- Explore [README.md](README.md) for project overview
- Check [backend/README.md](backend/README.md) for API documentation
- Customize prompts in [backend/config.py](backend/config.py)
- Add more council models for diverse perspectives

## Support

For issues or questions:
1. Check logs: `docker-compose logs -f`
2. Verify network connectivity between PCs
3. Ensure all models are downloaded
4. Check firewall settings
