# 🧠 LLM Council - Distributed Multi-Model AI System

[![Python](https://img.shields.io/badge/Python-3.10+-blue.svg)](https://www.python.org/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.115+-green.svg)](https://fastapi.tiangolo.com/)
[![React](https://img.shields.io/badge/React-19.2-blue.svg)](https://reactjs.org/)
[![Docker](https://img.shields.io/badge/Docker-Compose-blue.svg)](https://www.docker.com/)
[![Ollama](https://img.shields.io/badge/Ollama-Local%20LLM-orange.svg)](https://ollama.ai/)

---

## 👥 Team Information

**Institution**: De Vinci Higher Education - Gen AI Course  
**TD Group**: CDOF2 
**Submission Date**: January 2026

**Team Members**:
- Mathys D.,
- Mathéo D.,
- Edouard D.
 
---

## 📋 Project Overview

The **LLM Council** is a fully local, distributed multi-agent AI system that replaces single-model inference with collaborative decision-making. Instead of querying one AI model, the system orchestrates multiple locally-running models through a **three-stage deliberation process** to provide comprehensive, bias-reduced responses.

### Primary Use Cases

1. **🎯 Cognitive Bias Detection**: Analyze text for logical fallacies and reasoning errors
2. **🔬 Bias Analysis Research**: Study how multi-model collaboration reduces individual AI biases through peer review and consensus building

### Key Features

- 🏠 **Fully Local Execution** - No cloud APIs, all models run on your infrastructure
- 🌐 **Distributed Architecture** - Designed to run across multiple machines via REST APIs
- 🐳 **Containerized Deployment** - Docker Compose orchestration for easy setup
- 🦙 **Ollama Integration** - Leverages Ollama for efficient local LLM hosting
- ⚛️ **Modern Web UI** - React-based interface with conversation management
- 🔄 **Async Processing** - FastAPI backend with concurrent model querying
- 💾 **Conversation Storage** - Persistent JSON-based conversation history
- 🎨 **3-Pane Interface** - View all model responses, reviews, and final synthesis

### Three-Stage Deliberation Process

```
┌─────────────────────────────────────────────────────┐
│ STAGE 1: Initial Analysis (Parallel Execution)      │
│       ┌─────────┐  ┌─────────┐  ┌─────────┐         │
│       │ Llama   │  │ Gemma   │  │  Phi3   │         │
│       │ 3.2:1b  │  │ 2:2b    │  │ 3:3.8b  │         │
│       └────┬────┘  └────┬────┘  └────┬────┘         │
│            │   Independent Responses │              │
└────────────┼────────────┼────────────┼──────────────┘
             └────────────┼────────────┘
                          ▼
┌─────────────────────────────────────────────────────┐
│ STAGE 2: Peer Review (Cross-Evaluation)             │
│ Each model anonymously ranks others' responses      │
└─────────────────────────┬───────────────────────────┘
                          ▼
┌─────────────────────────────────────────────────────┐
│ STAGE 3: Final Synthesis (Chairman Model)           │
│        Consolidates all perspectives                │
└─────────────────────────────────────────────────────┘
```

**Why This Approach?**

✅ **Diverse Perspectives**: 3 different models with varying architectures and training  
✅ **Bias Reduction**: Peer review process reduces individual model biases  
✅ **Comprehensive Answers**:  Synthesis combines strengths of all models  
✅ **Full Privacy**: All processing happens locally, no cloud APIs  
✅ **Research Platform**: Study how multi-agent collaboration affects AI bias

---

## 🏗️ Architecture Overview

### Host and Remote Configuration

The LLM Council uses a flexible distributed architecture:

**Host Machine** (Control Node):
- **Always runs**: Chairman model (required for synthesis)
- **Always runs**: Backend API + Frontend UI
- **Can optionally run**: 0 to N councilor models
- **Role**: Orchestrates the entire council, runs the web interface

**Remote Machine(s)** (Compute Nodes):
- **Runs**: 0 to N councilor models each
- **Role**: Provides additional computational capacity for councilor models
- **Scalability**: Add as many remote machines as needed

**Example Configurations**: 

```
Configuration 1: Single Machine (Host Only)
┌─────────────────────────────────────────────────┐
│ Host Machine                                    │
│ ┌─────────┐ ┌─────────┐ ┌─────────┐ ┌──────────┐│
│ │Frontend │ │ Backend │ │Chairman │ │3 Council ││
│ │         │ │         │ │  Model  │ │ Models   ││
│ └─────────┘ └─────────┘ └─────────┘ └──────────┘│
└─────────────────────────────────────────────────┘
Requirements:  16GB+ RAM

Configuration 2: Two Machines (Recommended for this demo)
┌─────────────────────────────────────────────────┐
│ Host Machine                                    │
│       ┌─────────┐ ┌─────────┐ ┌─────────┐       │
│       │Frontend │ │ Backend │ │Chairman │       │
│       │         │ │         │ │  Model  │       │
│       └─────────┘ └─────────┘ └─────────┘       │
└────────────────────┬────────────────────────────┘
                     │ Network Connection
                     ▼
┌─────────────────────────────────────────────────┐
│ Remote Machine                                  │
│ ┌───────────────────────────────────────────┐   │
│ │   3 Councilor Models                      │   │
│ │   (Llama, Gemma, Phi3)                    │   │
│ └───────────────────────────────────────────┘   │
└─────────────────────────────────────────────────┘
Requirements: Host 4GB RAM, Remote 12GB RAM

Configuration 3: Multiple Remotes (Advanced)
┌─────────────────────────────────────────────────┐
│ Host Machine                                    │
│ Frontend + Backend + Chairman + 1 Councilor     │
└──────────┬──────────────────┬───────────────────┘
           │                  │
    ┌──────▼──────┐    ┌──────▼───────┐
    │  Remote 1   │    │   Remote 2   │
    │ 2 Councilors│    │ 1 Councilor  │
    └─────────────┘    └──────────────┘
Total: 1 Chairman + 4 Councilors distributed across 3 machines
```

**Key Points**: 
- The **Host** always includes the Chairman model (required for Stage 3 synthesis)
- The **Host** can run 0 to N councilor models in addition to the Chairman
- Each **Remote** machine can run 0 to N councilor models
- You can have 0 to N Remote machines
- Total councilor count = (Councilors on Host) + (Councilors on Remote 1) + (Councilors on Remote 2) + ...

---

## 🚀 Setup and Installation Instructions

### Prerequisites

- ✅ **1 Host machine** (required)
- ✅ **0-N Remote machines** (optional, for distributed setup)
- ✅ **Docker & Docker Compose** installed on all machines
- ✅ **8GB+ RAM** on Host (for Chairman + Backend + Frontend)
- ✅ **4GB+ RAM per councilor model** on Remote machines
- ✅ **20GB free disk space** for models and data
- ✅ **Local network connectivity** between machines (if using Remote)

**System Requirements:**

|    Component     |               Minimum               |    Recommended   |
|------------------|-------------------------------------|------------------|
| **CPU**          | 4 cores                             | 6+ cores         |
| **RAM (Host)**   | 8GB                                 | 12GB+            |
| **RAM (Remote)** | 8GB per Remote                      | 12GB+ per Remote |
| **Storage**      | 15GB free                           | 25GB+ free       |
| **Network**      | 100Mbps LAN                         | Gigabit LAN      |
| **OS**           | Windows 10, Ubuntu 20.04, macOS 12+ | Latest versions  |

### Installation Steps

#### Step 1: Install Docker

**Windows:**
1. Download [Docker Desktop for Windows](https://www.docker.com/products/docker-desktop/)
2. Install and restart your PC
3. Enable WSL 2 if prompted

**Linux (Ubuntu/Debian):**
```bash
curl -fsSL https://get.docker.com -o get-docker.sh
sudo sh get-docker.sh
sudo usermod -aG docker $USER
```

**macOS:**
1. Download [Docker Desktop for Mac](https://www.docker.com/products/docker-desktop/)
2. Install and start Docker Desktop

#### Step 2: Get Remote Machine IP Address (if using distributed setup)

On **each Remote machine**, open PowerShell/Terminal: 

```bash
# Windows
ipconfig

# Linux/Mac
ip addr
```

Look for the **IPv4 Address** - something like `192.168.1.101` or `10.0.0.X`

#### Step 3: Set Up Remote Machine(s) (Optional - skip if running on Host only)

On **each Remote machine**, clone the repository and start services:

```bash
git clone <your-repository-url>
cd gen-ai-project

# Start the Remote Ollama instance
docker-compose -f docker-compose-pipeline.yaml up -d
```

Wait 2-3 minutes for Ollama to start, then pull the councilor models you want on this Remote: 

```bash
# Pull all 3 councilor models (recommended)
docker exec llm-council-ollama-council ollama pull llama3.2:1b
docker exec llm-council-ollama-council ollama pull gemma2:2b
docker exec llm-council-ollama-council ollama pull phi3:3.8b

# Or pull only specific models
docker exec llm-council-ollama-council ollama pull llama3.2:1b
```

⏰ **This takes 5-10 minutes** depending on your internet speed. 

**Verify Remote is ready:**

```bash
docker exec llm-council-ollama-council ollama list
```

You should see the models you pulled.  ✅

**Configure Firewall:**

**Windows:**
```powershell
New-NetFirewallRule -DisplayName "Ollama LLM Council" `
  -Direction Inbound `
  -LocalPort 11434 `
  -Protocol TCP `
  -Action Allow
```

**Linux:**
```bash
sudo ufw allow 11434/tcp
sudo ufw reload
```

#### Step 4: Set Up Host Machine

On **Host machine**, clone the repository: 

```bash
git clone <your-repository-url>
cd gen-ai-project
```

**Configure Remote machine IP(s)** (skip if not using Remote):

**Option A: Create . env file** (recommended)
```bash
# For single Remote
echo "REMOTE_IP=192.168.1.101" > .env

# For multiple Remotes, edit config.py instead (see Configuration section)
```

**Option B: Edit docker-compose-ollama.yaml**
```yaml
# Line 28 - Change REMOTE_IP to your actual Remote IP
- COUNCIL_IP=${REMOTE_IP:-192.168.1.101}  # ← Update this IP
```

Start Host services:

```bash
docker-compose -f docker-compose-ollama.yaml up -d
```

Pull the chairman model:

```bash
docker exec llm-council-ollama-chairman ollama pull qwen2.5:1. 5b
```

⏰ **Takes 2-3 minutes**

**Optional: Pull councilor models on Host** (if you want some councilors on Host):

```bash
# Pull councilors on Host
docker exec llm-council-ollama-chairman ollama pull llama3.2:1b
docker exec llm-council-ollama-chairman ollama pull gemma2:2b
```

Then edit `backend/config.py` to configure which councilors run on Host vs.  Remote (see Configuration section).

#### Step 5: Test Connection Between Machines (if using Remote)

From **Host machine**, verify it can reach each Remote's Ollama: 

```bash
# Replace 192.168.1.101 with your actual Remote IP
curl http://192.168.1.101:11434/api/tags
```

✅ **Success**:  You should see JSON output listing Remote's models  
❌ **Failure**: Check firewall rules and network connectivity

#### Step 6: Verify Installation

On **Host machine**, open your web browser and navigate to:

```
http://localhost:5173
```

You should see the LLM Council web interface!  🎉

---

## 🎬 Instructions to Run the Demo

### Access the Application

1. Ensure Host services are running:
   ```bash
   # Check on Host
   docker ps
   ```

2. If using Remote machine(s), ensure they are running:
   ```bash
   # Check on each Remote
   docker ps
   ```

3. Open a web browser on **Host** and navigate to:
   ```
   http://localhost:5173
   ```

### Demo Workflow

#### 1. Create a New Conversation

- Click **"+ New Conversation"** in the left sidebar
- A new conversation appears with a timestamp ID

#### 2. Submit a Test Query

Try this example query that demonstrates cognitive bias detection:

```
This product is used by 90% of experts, so it must be the best option available.
```

Or try this one: 

```
Everyone in my social circle agrees with this political view, 
so it must be objectively correct.
```

- Type or paste the query in the text input area
- Click **"Send"** or press `Ctrl+Enter`
- Wait 25-35 seconds for the council to deliberate

#### 3. Observe Multiple Machines Working Together (if using Remote)

**On Remote machine(s)** (watch the console logs):
```bash
# View councilor models processing
docker logs -f llm-council-ollama-council
```

You'll see the councilor models (Llama, Gemma, Phi3) processing the query in parallel.

**On Host machine** (watch the backend logs):
```bash
# View orchestration and chairman synthesis
docker logs -f llm-council-backend
```

You'll see:
- Stage 1: Requests sent to Remote councilor models (and/or Host councilors)
- Stage 2: Peer review calculations
- Stage 3: Chairman model synthesis (always on Host)

#### 4. Review Council Responses

The UI will display three tabs: 

**Stage 1: Initial Responses**
- Click to see individual analysis from each councilor model
- Models may be distributed across Host and Remote machine(s)
- Compare how different models identify different biases
- Notice diversity in reasoning approaches

**Stage 2: Peer Review**
- See how models ranked each other's responses
- Anonymous scoring prevents favoritism
- Highest-ranked response is highlighted

**Stage 3: Chairman Final Answer** (Default view)
- Consolidated synthesis combining all perspectives
- Generated by Chairman model (always on Host)
- Most comprehensive and balanced response
- References points from multiple models

#### 5. Demonstrate Multiple Queries

To show the full system capabilities, try queries covering different bias types:

**Bandwagon Effect:**
```
Most people are buying this cryptocurrency, so it's definitely a safe investment.
```

**Authority Bias:**
```
A famous celebrity endorsed this health supplement, so it must work.
```

**Confirmation Bias:**
```
I only read news sources that confirm my existing beliefs because they're the most accurate.
```

**False Dichotomy:**
```
You're either with us or against us - there's no middle ground on this issue.
```

#### 6. Show Conversation History

- Click on previous conversations in the sidebar
- All messages and metadata are preserved
- Demonstrates persistent storage capability

### Expected Demo Outcome

During the live demo, you should showcase: 

✅ **Distributed Architecture**: 
   - If using Remote:  Show councilor models on Remote, chairman on Host
   - If single machine:  Explain how it can scale to multiple machines

✅ **Council Responses**:  All 3 stages visible in the interface  
✅ **Review Stage**: Models evaluating each other's responses  
✅ **Chairman Final Answer**: Synthesized, comprehensive response (always from Host)  
✅ **Bias Detection**: Clear identification of cognitive biases in test statements

### Demo Troubleshooting

**If models are slow:**
- This is expected for CPU-only inference
- 25-35 seconds is normal for the full 3-stage process
- Mention GPU acceleration would reduce to 10-15 seconds

**If connection fails (distributed setup):**
- Verify all machines are on same network
- Check firewall rules on Remote machines
- Test with:  `curl http://<REMOTE_IP>:11434/api/tags`

**If a model fails:**
- System will continue with remaining models
- Graceful degradation is built-in
- Check logs:  `docker logs llm-council-backend`

---

## 🛠️ Configuration

### Project Structure

```
gen-ai-project/
├── backend/                      # FastAPI backend
│   ├── __init__.py              # Package initializer
│   ├── config.py                # Model configuration
│   ├── council.py               # 3-stage orchestration logic
│   ├── dockerfile               # Backend container
│   ├── main.py                  # API server & endpoints
│   ├── models.py                # Data models (Pydantic)
│   ├── ollama.py                # Ollama API client
│   ├── requirements.txt         # Python dependencies
│   └── storage.py               # Conversation persistence 
│
├── frontend/                    # React UI
│   ├── src/
│   │   ├── api.js               # Backend API client
│   │   ├── App.css              # Application styles
│   │   ├── App.jsx              # Main application
│   │   ├── index.css            # Global styles
│   │   ├── main.jsx             # React entry point
│   │   ├── assets/              # Static assets (images, icons)
│   │   └── components/
│   │       ├── ChatInterface.css    # Chat UI styles
│   │       ├── ChatInterface.jsx    # Chat UI orchestrator
│   │       ├── Sidebar.css          # Sidebar styles
│   │       ├── Sidebar.jsx          # Conversation list
│   │       ├── Stage1.css           # Stage 1 styles
│   │       ├── Stage1.jsx           # Display initial responses
│   │       ├── Stage2.css           # Stage 2 styles
│   │       ├── Stage2.jsx           # Show peer reviews
│   │       ├── Stage3.css           # Stage 3 styles
│   │       └── Stage3.jsx           # Present synthesis
│   ├── dockerfile               # Frontend container
│   ├── eslint.config.js         # ESLint configuration
│   ├── index.html               # HTML entry point
│   ├── package.json             # Node dependencies
│   ├── README.md                # Frontend documentation
│   └── vite.config.js           # Vite build config
│
├── docker-compose-ollama.yaml   # Host services (Chairman + Backend + UI)
├── docker-compose-pipeline.yaml # Remote services (Councilor models)
├── main.py                      # Root Python script
├── README.md                    # This file
└── TECHNICAL_REPORT.md          # Technical documentation
```

### Customizing Model Distribution (Host vs.  Remote)

Edit `backend/config.py` to configure which models run where:

```python
import os

# Host's chairman Ollama (always on Host)
HOST_CHAIRMAN_IP = "ollama-chairman"

# Remote machine IPs (if using distributed setup)
REMOTE_1_IP = os.getenv("REMOTE_IP", "192.168.1.101")
REMOTE_2_IP = os.getenv("REMOTE_2_IP", "192.168.1.102")  # Optional second Remote

COUNCIL_MODELS = [
    # ============================================
    # CHAIRMAN (Always on Host - Required)
    # ============================================
    CouncilModel(
        ip=HOST_CHAIRMAN_IP,
        port=11434,
        model_name="qwen2.5:1.5b",
        role=Role.CHAIRMAN
    ),
    
    # ============================================
    # COUNCILORS (Distributed across machines)
    # ============================================
    
    # Councilors on Remote 1
    CouncilModel(
        ip=REMOTE_1_IP,
        port=11434,
        model_name="llama3.2:1b",
        role=Role.COUNCILOR
    ),
    CouncilModel(
        ip=REMOTE_1_IP,
        port=11434,
        model_name="gemma2:2b",
        role=Role.COUNCILOR
    ),
    CouncilModel(
        ip=REMOTE_1_IP,
        port=11434,
        model_name="phi3:3.8b",
        role=Role.COUNCILOR
    ),
    
    # Optional:  Councilors on Remote 2
    # CouncilModel(
    #     ip=REMOTE_2_IP,
    #     port=11434,
    #     model_name="mistral:7b",
    #     role=Role.COUNCILOR
    # ),
    
    # Optional: Councilors on Host (same machine as Chairman)
    # CouncilModel(
    #     ip=HOST_CHAIRMAN_IP,  # Same Ollama instance as Chairman
    #     port=11434,
    #     model_name="tinyllama:1.1b",
    #     role=Role.COUNCILOR
    # ),
]
```

**Configuration Examples:**

**Example 1: All on Host (Single Machine)**
```python
COUNCIL_MODELS = [
    # Chairman on Host
    CouncilModel(ip="ollama-chairman", model_name="qwen2.5:1.5b", role=Role.CHAIRMAN),
    
    # All councilors also on Host
    CouncilModel(ip="ollama-chairman", model_name="llama3.2:1b", role=Role.COUNCILOR),
    CouncilModel(ip="ollama-chairman", model_name="gemma2:2b", role=Role.COUNCILOR),
    CouncilModel(ip="ollama-chairman", model_name="phi3:3.8b", role=Role.COUNCILOR),
]
```

**Example 2: Host + Single Remote (Recommended for demo)**
```python
COUNCIL_MODELS = [
    # Chairman on Host
    CouncilModel(ip="ollama-chairman", model_name="qwen2.5:1.5b", role=Role.CHAIRMAN),
    
    # All councilors on Remote
    CouncilModel(ip="192.168.1.101", model_name="llama3.2:1b", role=Role.COUNCILOR),
    CouncilModel(ip="192.168.1.101", model_name="gemma2:2b", role=Role.COUNCILOR),
    CouncilModel(ip="192.168.1.101", model_name="phi3:3.8b", role=Role.COUNCILOR),
]
```

**Example 3: Host + Multiple Remotes**
```python
COUNCIL_MODELS = [
    # Chairman on Host
    CouncilModel(ip="ollama-chairman", model_name="qwen2.5:1.5b", role=Role.CHAIRMAN),
    
    # 1 councilor on Host
    CouncilModel(ip="ollama-chairman", model_name="tinyllama:1.1b", role=Role.COUNCILOR),
    
    # 2 councilors on Remote 1
    CouncilModel(ip="192.168.1.101", model_name="llama3.2:1b", role=Role.COUNCILOR),
    CouncilModel(ip="192.168.1.101", model_name="gemma2:2b", role=Role.COUNCILOR),
    
    # 1 councilor on Remote 2
    CouncilModel(ip="192.168.1.102", model_name="phi3:3.8b", role=Role.COUNCILOR),
]
```

### Available Models

**Available models** (pull with `ollama pull <model-name>`):
- Small (1-2B): `tinyllama:1.1b`, `qwen2:1.5b`, `gemma:2b`
- Medium (7B): `llama3:7b`, `mistral:7b`, `qwen2:7b`
- Large (13B+): `llama3:13b`, `mixtral:8x7b`

### Network Configuration

Update environment variables in `.env` file:

```bash
# Remote Machine Network Configuration
REMOTE_IP=192.168.1.101           # Primary Remote machine
REMOTE_2_IP=192.168.1.102         # Optional second Remote
REMOTE_3_IP=192.168.1.103         # Optional third Remote

COUNCIL_IP=192.168.1.101          # For backward compatibility
COUNCIL_PORT=11434                # Ollama port on Remote

# Host Configuration
CHAIRMAN_IP=ollama-chairman
CHAIRMAN_PORT=11434
```

---

## 🔍 Troubleshooting

### Host Can't Connect to Remote

**Symptom:** `curl http://<REMOTE_IP>:11434/api/tags` fails

**Solutions:**

1. Verify Remote IP address:
   ```bash
   # On Remote
   ipconfig  # Windows
   ip addr   # Linux/Mac
   ```

2. Check Ollama is running on Remote:
   ```bash
   docker ps | grep ollama
   ```

3. Test port 11434 is open:
   ```powershell
   # On Host
   Test-NetConnection -ComputerName <REMOTE_IP> -Port 11434
   ```

4. Add firewall rule (see Installation Step 3)

5. Ensure Host and Remote are on same network subnet

### "Model Not Found" Error

**Solution:** Pull the missing model on the appropriate machine:

```bash
# On Remote (for councilor models)
docker exec llm-council-ollama-council ollama pull llama3.2:1b
docker exec llm-council-ollama-council ollama pull gemma2:2b
docker exec llm-council-ollama-council ollama pull phi3:3.8b

# On Host (for chairman model - required)
docker exec llm-council-ollama-chairman ollama pull qwen2.5:1.5b

# On Host (for councilors if running some on Host)
docker exec llm-council-ollama-chairman ollama pull llama3.2:1b
```

### Services Won't Start

**Solution:**

1. Check Docker is running:
   ```bash
   docker ps
   ```

2. View logs:
   ```bash
   # On Host
   docker compose -f docker-compose-ollama.yaml logs
   
   # On Remote
   docker compose -f docker-compose-pipeline.yaml logs
   ```

3. Restart Docker Desktop (Windows/Mac) or:
   ```bash
   sudo systemctl restart docker  # Linux
   ```

### Frontend Shows "Failed to Load Conversations"

**Solution:**

1. Check backend is running on Host:
   ```bash
   curl http://localhost:8000/
   ```

2. Restart backend:
   ```bash
   docker compose restart backend
   ```

### Out of Memory Errors

**Solutions:**

1. Increase Docker memory limit:
   - Docker Desktop → Settings → Resources → Memory
   - Set to at least 8GB on Host, 12GB on Remote

2. Use smaller models (edit `backend/config.py`)

3. Reduce number of councilor models

4. Distribute councilors across more Remote machines

---

## 📚 Useful Commands

### Docker Management

```bash
# Start Host services
docker-compose -f docker-compose-ollama.yaml up -d

# Start Remote services
docker-compose -f docker-compose-pipeline.yaml up -d

# Stop Host services
docker-compose -f docker-compose-ollama.yaml down

# Stop Remote services
docker-compose -f docker-compose-pipeline.yaml down

# View logs on Host
docker compose logs -f backend
docker compose logs -f ollama-chairman

# View logs on Remote
docker compose logs -f ollama-council

# Restart specific service
docker compose restart backend
```

### Ollama Commands

```bash
# List models on Remote
docker exec llm-council-ollama-council ollama list

# List models on Host
docker exec llm-council-ollama-chairman ollama list

# Pull new model on Remote
docker exec llm-council-ollama-council ollama pull <model-name>

# Pull new model on Host
docker exec llm-council-ollama-chairman ollama pull <model-name>

# Remove model
docker exec llm-council-ollama-council ollama rm <model-name>

# Check API status on Remote
curl http://<REMOTE_IP>:11434/api/tags

# Check API status on Host
curl http://localhost:11434/api/tags
```

### Backend API Testing

```bash
# Health check
curl http://localhost:8000/

# List conversations
curl http://localhost:8000/api/conversations

# Get conversation details
curl http://localhost:8000/api/conversations/<conversation-id>
```

---

## 🤖 Generative AI Usage Statement

This project utilized the following AI tools during development:

- **Claude Sonnet 4. 5** (via GitHub Copilot)
  - Code refactoring and optimization
  - Documentation generation
  - Architecture design suggestions
  - Debugging assistance

- **GitHub Copilot**
  - Code completion
  - Boilerplate generation

All AI-generated content was reviewed, tested, and modified by the development team. 

---

## 🙏 Acknowledgments

**Inspired by:**
- Andrej Karpathy's LLM Council concept
- Multi-agent AI research (DeepMind, OpenAI, Anthropic)

**Built with:**
- [Ollama](https://ollama.ai/) - Local LLM infrastructure
- [FastAPI](https://fastapi.tiangolo.com/) - Modern Python web framework
- [React](https://react.dev/) - Frontend UI library
- [Docker](https://www.docker.com/) - Containerization platform

---

## 📄 License

[Add license information as specified by your institution]

---

**For detailed technical information**, see [TECHNICAL_REPORT.md](TECHNICAL_REPORT.md)

**Quick Links**:
- [Architecture Overview](#architecture-overview)
- [Setup Instructions](#setup-and-installation-instructions)
- [Demo Instructions](#instructions-to-run-the-demo)
- [Configuration](#configuration)
- [Troubleshooting](#troubleshooting)
- [Technical Report](TECHNICAL_REPORT.md)


_Written with the assistance of AI tools._