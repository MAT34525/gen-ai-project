# LLM Council - Local Deployment

[![Ollama](https://img.shields.io/badge/Ollama-Enabled-blue)](https://ollama.ai)
[![Docker](https://img.shields.io/badge/Docker-Ready-blue)](https://www.docker.com/)
[![Python](https://img.shields.io/badge/Python-3.10+-green)](https://www.python.org/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.100+-teal)](https://fastapi.tiangolo.com/)
[![React](https://img.shields.io/badge/React-18+-purple)](https://react.dev/)

> **Distributed Multi-LLM System for Collaborative AI Reasoning**

A refactored implementation of [Andrej Karpathy's LLM Council](https://github.com/karpathy/LLM-council) that runs entirely on **local LLMs** using **Ollama** in a distributed architecture.

## ✨ What's New

✅ **Fully Local** - No cloud APIs, no OpenRouter, runs 100% locally  
✅ **Distributed Architecture** - Chairman and Council on separate machines  
✅ **Ollama Integration** - Simple, scalable REST API for local LLMs  
✅ **Docker Ready** - Containerized for easy multi-machine deployment  
✅ **2-PC Configuration** - Optimized for Chairman (PC1) + Council (PC2) setup  

## 📋 Table of Contents

- [What Is the LLM Council?](#what-is-the-llm-council)
- [Architecture](#architecture)
- [Quick Start](#quick-start)
- [Deployment](#deployment)
- [Configuration](#configuration)
- [Development](#development)
- [Project Structure](#project-structure)
- [Improvements Over Original](#improvements-over-original)
- [Troubleshooting](#troubleshooting)
- [Contributing](#contributing)

## 🤔 What Is the LLM Council?

The LLM Council is a **multi-stage collaborative reasoning system** where multiple LLMs work together:

### Stage 1: First Opinions 🗣️
- User submits a query
- Multiple LLMs generate independent responses
- Each perspective is preserved and displayed

### Stage 2: Peer Review 📊
- LLMs anonymously review each other's responses
- Each model ranks others on accuracy and insight
- Identities are anonymized to prevent bias

### Stage 3: Chairman Synthesis ⚖️
- A dedicated Chairman LLM synthesizes all inputs
- Considers original responses + peer rankings
- Produces a final, well-reasoned answer

**Why?** This approach leverages:
- 🎯 **Diversity of reasoning** - Different models, different perspectives
- 🔍 **Self-critique** - Models evaluate each other's work
- 🧠 **Collective intelligence** - Synthesis produces better results than any single model

## 🏗️ Architecture

```
┌─────────────────────────────────────┐
│           PC1 (Chairman)            │
│                                     │
│  ┌──────────┐  ┌────────────────┐  │
│  │ Frontend │─▶│ Backend (API)  │  │
│  │  :5173   │  │    :8000       │  │
│  └──────────┘  └────────┬───────┘  │
│                         │           │
│  ┌──────────────────────▼────────┐ │
│  │ Ollama Chairman :11434        │ │
│  │ • qwen2.5:1.5b                │ │
│  │ • Role: Final synthesis       │ │
│  └───────────────────────────────┘ │
└─────────────────┬───────────────────┘
                  │ Network (REST API)
                  │
┌─────────────────▼───────────────────┐
│           PC2 (Council)             │
│                                     │
│  ┌───────────────────────────────┐ │
│  │ Ollama Council :11434         │ │
│  │                               │ │
│  │ • llama3.2:1b (Councilor_1)  │ │
│  │ • gemma2:2b   (Councilor_2)  │ │
│  │ • phi3:3.8b   (Councilor_3)  │ │
│  │                               │ │
│  │ Role: Initial response +      │ │
│  │       Peer review             │ │
│  └───────────────────────────────┘ │
└─────────────────────────────────────┘
```

### Key Principles

1. **Chairman Separation** - Runs on dedicated machine, only synthesizes
2. **Council Distribution** - Multiple models on separate machine(s)
3. **REST Communication** - Machines communicate via Ollama REST API
4. **Model Independence** - Each model runs in its own Ollama instance

## 🚀 Quick Start

### Prerequisites

- **2 PCs** with network connectivity (or 1 PC for testing)
- **Docker & Docker Compose** installed on both
- **8GB+ RAM** recommended per PC
- **Network access** between PCs on port 11434

### 1. Clone Repository (Both PCs)

```bash
git clone https://github.com/yourusername/gen-ai-project.git
cd gen-ai-project
```

### 2. Set Up PC2 (Council)

```bash
# Start Council Ollama
docker-compose -f docker-compose.pc2.yaml up -d

# Pull council models (takes 5-10 minutes)
docker exec llm-council-ollama-council ollama pull llama3.2:1b
docker exec llm-council-ollama-council ollama pull gemma2:2b
docker exec llm-council-ollama-council ollama pull phi3:3.8b

# Verify
docker exec llm-council-ollama-council ollama list
```

### 3. Set Up PC1 (Chairman + Backend + Frontend)

```bash
# Configure PC2 IP address
cp .env.example .env
# Edit .env and set COUNCIL_IP to PC2's IP address

# Or use environment variable
export PC2_IP=192.168.1.101

# Start PC1 services
docker-compose -f docker-compose.pc1.yaml up -d

# Pull chairman model
docker exec llm-council-ollama-chairman ollama pull qwen2.5:1.5b

# Verify all services
docker ps
```

### 4. Access Application

Open browser on PC1:
```
http://localhost:5173
```

### 5. Test with a Query

Try this example query about cognitive bias:
```
Ce produit est utilisé par 90% des experts, donc il doit être le meilleur.
```

Watch as:
1. ✅ Council models analyze (from PC2)
2. ✅ Models review each other's work (PC2)
3. ✅ Chairman synthesizes final answer (PC1)

## 📚 Deployment

For detailed deployment instructions including:
- Network configuration
- Firewall settings
- GPU acceleration
- Troubleshooting
- Production considerations

See **[DEPLOYMENT.md](DEPLOYMENT.md)** 📖

## ⚙️ Configuration

### Environment Variables

Create a `.env` file (use `.env.example` as template):

```bash
# Chairman (PC1)
CHAIRMAN_IP=localhost
CHAIRMAN_PORT=11434
CHAIRMAN_MODEL=qwen2.5:1.5b

# Council (PC2)
COUNCIL_IP=192.168.1.101  # ← Set to PC2's IP
COUNCIL_PORT=11434
```

### Customize Models

Edit `backend/config.py`:

```python
COUNCIL_BASE_MODELS = [
    # Chairman (PC1)
    CouncilModel(
        ip=CHAIRMAN_IP,
        port=CHAIRMAN_PORT,
        model_name="llama3.2:3b",  # Change model
        role=Role.CHAIRMAN
    ),
    # Council (PC2)
    CouncilModel(
        ip=COUNCIL_IP,
        port=COUNCIL_PORT,
        model_name="mistral:7b",  # Different model
        role=Role.COUNCILOR,
        custom_name="Councilor_1"
    ),
    # Add more models...
]
```

### Available Models

Popular Ollama models for this project:

| Model | Size | Best For | Speed |
|-------|------|----------|-------|
| `llama3.2:1b` | 1.3GB | Fast responses | ⚡⚡⚡ |
| `gemma2:2b` | 1.6GB | Balanced | ⚡⚡ |
| `phi3:3.8b` | 2.3GB | Reasoning | ⚡⚡ |
| `qwen2.5:1.5b` | 1.0GB | Synthesis | ⚡⚡⚡ |
| `mistral:7b` | 4.1GB | Quality | ⚡ |

See [Ollama Models](https://ollama.ai/library) for full list.

## 💻 Development

### Without Docker

**PC2 (Council):**
```bash
# Install Ollama
curl -fsSL https://ollama.com/install.sh | sh

# Pull models
ollama pull llama3.2:1b
ollama pull gemma2:2b
ollama pull phi3:3.8b
```

**PC1 (Backend + Frontend):**
```bash
# Install Ollama
curl -fsSL https://ollama.com/install.sh | sh
ollama pull qwen2.5:1.5b

# Backend
cd backend
pip install -r requirements.txt
export COUNCIL_IP=192.168.1.101
uvicorn main:app --reload --host 0.0.0.0 --port 8000

# Frontend (separate terminal)
cd frontend
npm install
npm run dev
```

### Project Structure

```
gen-ai-project/
├── backend/                 # FastAPI backend
│   ├── main.py             # API endpoints
│   ├── council.py          # 3-stage orchestration
│   ├── ollama.py           # Ollama client
│   ├── config.py           # Configuration
│   ├── models.py           # Data models
│   ├── storage.py          # Conversation storage
│   └── requirements.txt    # Python dependencies
│
├── frontend/                # React frontend
│   ├── src/
│   │   ├── App.jsx         # Main app
│   │   ├── components/     # React components
│   │   └── api.js          # API client
│   └── package.json        # Node dependencies
│
├── data/                    # Conversation storage
│   └── conversations/
│
├── docker-compose.full.yaml    # All services (testing)
├── docker-compose.pc1.yaml     # PC1 services
├── docker-compose.pc2.yaml     # PC2 services
├── .env.example                # Environment template
├── DEPLOYMENT.md               # Deployment guide
└── README.md                   # This file
```

## 🎯 Improvements Over Original

| Feature | Original | This Version |
|---------|----------|--------------|
| **LLM Provider** | OpenRouter (cloud) | Ollama (local) |
| **Architecture** | Single machine | Distributed (2+ PCs) |
| **API** | OpenRouter API | REST API (Ollama) |
| **Deployment** | Manual setup | Docker Compose |
| **Chairman** | Mixed with council | Dedicated instance |
| **Cost** | Pay per token | Free (local) |
| **Privacy** | Data sent to cloud | 100% local |
| **Scalability** | Limited by API | Horizontal scaling |
| **Models** | Fixed providers | Any Ollama model |

### Additional Enhancements

✨ **Better Error Handling** - Graceful failures, timeout management  
✨ **Health Checks** - Monitor model availability  
✨ **Configurable** - Easy environment-based configuration  
✨ **Docker Ready** - One-command deployment  
✨ **Documentation** - Comprehensive guides and examples  

## 🔧 Troubleshooting

### Cannot connect to PC2

```bash
# Check firewall (Windows)
New-NetFirewallRule -DisplayName "Ollama" -Direction Inbound -LocalPort 11434 -Protocol TCP -Action Allow

# Test connectivity from PC1
curl http://<PC2_IP>:11434/api/tags
```

### Models not found

```bash
# Pull models manually
docker exec llm-council-ollama-council ollama pull llama3.2:1b
```

### Slow responses

- Use smaller models (1-3B parameters)
- Enable GPU acceleration (see DEPLOYMENT.md)
- Increase timeout in config

### Out of memory

- Use smaller models
- Reduce number of council models
- Increase Docker memory limit

See **[DEPLOYMENT.md](DEPLOYMENT.md)** for more troubleshooting.

## 🤝 Contributing

This is a student project for educational purposes. Contributions, suggestions, and improvements are welcome!

### Generative AI Usage Declaration

⚠️ **Mandatory Declaration**: This project used Generative AI tools.

**Tools Used:**
- GitHub Copilot - Code completion and refactoring
- Claude Sonnet 4.5 - Architecture design and documentation
- ChatGPT - Debugging and optimization suggestions

**Purpose:**
- Refactoring OpenRouter to Ollama integration
- Docker configuration and deployment setup
- Documentation writing and formatting
- Code review and best practices

**Note:** All AI-generated code was reviewed, tested, and modified as needed.

## 📄 License

This project is based on [karpathy/LLM-council](https://github.com/karpathy/LLM-council).

## 🙏 Acknowledgments

- **Andrej Karpathy** - Original LLM Council concept
- **Ollama** - Local LLM infrastructure
- **FastAPI** - Backend framework
- **React** - Frontend framework

## 📞 Support

- 📖 Read [DEPLOYMENT.md](DEPLOYMENT.md) for setup help
- 🐛 Check logs: `docker-compose logs -f`
- 🔍 Search existing issues
- 💬 Open a new issue for bugs/features

---

**Made with ❤️ for distributed AI systems**
