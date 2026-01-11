# 🚀 Quick Start - 2-PC Setup

## What You'll Build

```
PC1: Chairman + Web Interface
        ↕
PC2: Council Models (3 AI advisors)
```

## Prerequisites

- ✅ 2 PCs on same network
- ✅ Docker installed on both
- ✅ 8GB+ RAM per PC

---

## Setup in 5 Minutes

### Step 1: Get PC2's IP Address

**On PC2**, open PowerShell:
```powershell
ipconfig
```
Look for "IPv4 Address" - something like `192.168.1.101`

---

### Step 2: Set Up PC2 (The Council)

**On PC2**, clone and run:
```powershell
git clone <your-repo>
cd gen-ai-project
docker-compose -f docker-compose.pc2.yaml up -d
```

Wait 2-3 minutes, then pull models:
```powershell
docker exec llm-council-ollama-council ollama pull llama3.2:1b
docker exec llm-council-ollama-council ollama pull gemma2:2b
docker exec llm-council-ollama-council ollama pull phi3:3.8b
```

⏰ This takes 5-10 minutes depending on internet speed.

✅ PC2 is ready when you see:
```powershell
docker exec llm-council-ollama-council ollama list
```
Shows 3 models.

---

### Step 3: Set Up PC1 (The Chairman)

**On PC1**, clone and configure:
```powershell
git clone <your-repo>
cd gen-ai-project

# Create config file
Copy-Item .env.example .env

# Edit .env and change this line:
# COUNCIL_IP=192.168.1.101  ← YOUR PC2 IP HERE
notepad .env
```

Start services:
```powershell
docker-compose -f docker-compose.pc1.yaml up -d
```

Pull chairman model:
```powershell
docker exec llm-council-ollama-chairman ollama pull qwen2.5:1.5b
```

⏰ Takes 2-3 minutes.

---

### Step 4: Test Connection

From PC1:  #change IP address with the one on PC 2
```powershell
curl http://192.168.1.101:11434/api/tags
```

✅ Should show PC2's models

---

### Step 5: Use the Application

**On PC1**, open browser:
```
http://localhost:5173
```

Try this query:
```
Ce produit est utilisé par 90% des experts, donc il doit être le meilleur.
```

Watch as:
1. 3 models analyze (from PC2)
2. Models review each other (PC2)
3. Chairman synthesizes answer (PC1)

---

## Troubleshooting

### ❌ PC1 can't connect to PC2

**Fix firewall on PC2:**
```powershell
New-NetFirewallRule -DisplayName "Ollama" -Direction Inbound -LocalPort 11434 -Protocol TCP -Action Allow
```

### ❌ "Model not found"

**Pull models again:**
```powershell
docker exec llm-council-ollama-council ollama pull llama3.2:1b
```

### ❌ Services won't start

**Check Docker:**
```powershell
docker ps
```

**View logs:**
```powershell
docker compose logs -f
```

---

## What's Next?

✅ **It works?** Great! Now read [README_NEW.md](README_NEW.md) for details

✅ **Need help?** Check [DEPLOYMENT.md](DEPLOYMENT.md) for troubleshooting

✅ **Want to customize?** Edit `backend/config.py` to change models

---

## Stop Services

```powershell
# PC1
docker-compose -f docker-compose.pc1.yaml down

# PC2  
docker-compose -f docker-compose.pc2.yaml down
```

---

## Useful Commands

```powershell
# View logs
docker compose logs -f

# Check model status
docker exec llm-council-ollama-council ollama list

# Restart services
docker compose restart
```

---

**Need more help?** See [QUICK_REFERENCE.md](QUICK_REFERENCE.md) for all commands

🎉 **Enjoy your local LLM Council!**
