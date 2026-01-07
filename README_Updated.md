# LLM Council - Local Distributed Multi-Model AI System

[![Python](https://img.shields.io/badge/Python-3.10+-blue.svg)](https://www.python.org/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.115+-green.svg)](https://fastapi.tiangolo.com/)
[![React](https://img.shields.io/badge/React-19.2-blue.svg)](https://reactjs.org/)
[![Docker](https://img.shields.io/badge/Docker-Compose-blue.svg)](https://www.docker.com/)
[![Ollama](https://img.shields.io/badge/Ollama-Local%20LLM-orange.svg)](https://ollama.ai/)

A distributed multi-LLM system that replaces single-model inference with collaborative decision-making. Instead of querying one AI model, the LLM Council orchestrates multiple locally-running models to answer queries, review each other's responses, and synthesize a final output through a designated Chairman model.

## 🎯 What This Project Does

The LLM Council implements a **3-stage collaborative AI reasoning system**:

1. **Stage 1: Initial Responses** - Multiple LLMs independently analyze the user's query
2. **Stage 2: Peer Review** - Models anonymously evaluate and rank each other's outputs
3. **Stage 3: Final Synthesis** - A Chairman LLM compiles all perspectives into a unified answer

This approach provides diverse perspectives, reduces individual model biases, and produces more comprehensive responses than single-model systems.

### Key Features

- 🏠 **Fully Local Execution** - No cloud APIs, all models run on your infrastructure
- 🌐 **Distributed Architecture** - Designed to run across multiple machines via REST APIs
- 🐳 **Containerized Deployment** - Docker Compose orchestration for easy setup
- 🦙 **Ollama Integration** - Leverages Ollama for efficient local LLM hosting
- ⚛️ **Modern Web UI** - React-based interface with conversation management
- 🔄 **Async Processing** - FastAPI backend with concurrent model querying
- 💾 **Conversation Storage** - Persistent JSON-based conversation history
- 🎨 **3-Pane Interface** - View all model responses, reviews, and final synthesis

## 🚀 Why This Project is Useful

### For Developers
- Learn distributed AI system architecture
- Understand multi-model orchestration patterns
- Practice with modern async Python and React
- Explore local LLM deployment strategies

### For Researchers
- Compare multiple models side-by-side
- Study inter-model evaluation patterns
- Analyze consensus-building in AI systems
- Experiment with cognitive bias detection

### For Teams
- Run private AI inference without cloud dependencies
- Scale across multiple machines for better performance
- Customize models for specific tasks
- Maintain full control over data and processing

## 📋 Prerequisites

- **Docker & Docker Compose** - For containerized deployment
- **Python 3.10+** - For local development
- **Node.js 18+** - For frontend development
- **4GB+ RAM per model** - Recommended for small models (1-2B parameters)
- **CUDA-capable GPU** (Optional) - For accelerated inference

## 🔧 Installation & Setup

### Quick Start with Docker (Recommended)

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd gen-ai-project
   ```

2. **Start all services**
   ```bash
   docker-compose up -d
   ```

   This will start:
   - Ollama server (port 11434)
   - Backend API (port 8001)
   - Frontend UI (port 5173)

3. **Access the application**
   
   Open your browser to [http://localhost:5173](http://localhost:5173)

### Local Development Setup

#### Backend Setup

1. **Install dependencies with uv** (recommended)
   ```bash
   uv sync
   ```

   Or with pip:
   ```bash
   pip install -r backend/requirements.txt
   ```

2. **Start the backend server**
   ```bash
   uv run python -m backend.main
   # or
   cd backend
   python -m main
   ```

   Backend runs on [http://localhost:8001](http://localhost:8001)

#### Frontend Setup

1. **Install Node.js dependencies**
   ```bash
   cd frontend
   npm install
   ```

2. **Start the development server**
   ```bash
   npm run dev
   ```

   Frontend runs on [http://localhost:5173](http://localhost:5173)

#### Ollama Setup

1. **Install Ollama** from [ollama.ai](https://ollama.ai/)

2. **Pull required models**
   ```bash
   ollama pull qwen2.5:1.5b
   ollama pull llama3.2:1b
   ollama pull gemma3:1b
   ```

## 💡 Usage Examples

### Basic Query Workflow

1. **Create a new conversation** by clicking "+ New Conversation" in the sidebar

2. **Submit your query** in the text area (e.g., "Analyze this statement for cognitive biases: 'Everyone says this is the best product, so it must be true'")

3. **Stage 1: View individual model responses**
   - Each councilor model provides its analysis
   - Responses appear in separate tabs for easy comparison

4. **Stage 2: Review peer evaluations**
   - Models rank each other's responses
   - Anonymous scoring prevents favoritism

5. **Stage 3: Read the Chairman's synthesis**
   - Final consolidated answer combining all perspectives
   - Most comprehensive response appears in the main view

### Configuration

Edit [backend/config.py](backend/config.py) to customize the council:

```python
COUNCIL_BASE_MODELS = [
    CouncilModel(
        ip="ollama", 
        model_name="qwen2.5:1.5b", 
        role=Role.CHAIRMAN
    ),
    CouncilModel(
        ip="ollama", 
        model_name="llama3.2:1b", 
        role=Role.COUNCILOR,
        prompt="Custom system prompt here",
        custom_name="Analyst-1"
    ),
    # Add more models...
]
```

### Distributed Deployment

To run models on separate machines:

1. **On each machine**, install and run Ollama
   ```bash
   ollama serve
   ```

2. **Update `backend/config.py`** with remote IPs
   ```python
   CouncilModel(ip="192.168.1.100", port=11434, model_name="llama3.2:1b")
   CouncilModel(ip="192.168.1.101", port=11434, model_name="qwen2.5:1.5b")
   ```

3. **Ensure network connectivity** between machines (port 11434)

## 📁 Project Structure

```
gen-ai-project/
├── backend/                  # FastAPI backend
│   ├── main.py              # API endpoints & server
│   ├── council.py           # 3-stage council orchestration
│   ├── config.py            # Model configuration
│   ├── models.py            # CouncilModel class
│   ├── openrouter.py        # LLM query functions
│   ├── storage.py           # Conversation persistence
│   ├── requirements.txt     # Python dependencies
│   └── dockerfile           # Backend container
├── frontend/                # React UI
│   ├── src/
│   │   ├── App.jsx          # Main application
│   │   ├── api.js           # Backend API client
│   │   └── components/      # UI components
│   │       ├── ChatInterface.jsx
│   │       ├── Sidebar.jsx
│   │       ├── Stage1.jsx   # Initial responses
│   │       ├── Stage2.jsx   # Peer reviews
│   │       └── Stage3.jsx   # Final synthesis
│   ├── package.json         # Node dependencies
│   └── dockerfile           # Frontend container
├── docker-compose.yaml      # Multi-service orchestration
├── pyproject.toml          # Python project config (uv)
└── README.md               # This file
```

## 🔌 API Reference

### Core Endpoints

- `GET /` - Health check
- `GET /api/conversations` - List all conversations
- `POST /api/conversations` - Create new conversation
- `GET /api/conversations/{id}` - Get conversation details
- `POST /api/conversations/{id}/messages` - Send message (triggers 3-stage process)
- `POST /api/register` - Register new LLM to council

### Example: Send a Message

```bash
curl -X POST http://localhost:8001/api/conversations/{conversation_id}/messages \
  -H "Content-Type: application/json" \
  -d '{"content": "What are the main cognitive biases in advertising?"}'
```

Response includes:
- `stage1_responses`: Individual model outputs
- `stage2_rankings`: Peer review scores
- `stage3_synthesis`: Chairman's final answer

## 🛠️ Troubleshooting

### Common Issues

**Models not pulling on startup**
```bash
# Manually pull models
docker exec ollama ollama pull qwen2.5:1.5b
docker exec ollama ollama pull llama3.2:1b
docker exec ollama ollama pull gemma3:1b
```

**Backend can't connect to Ollama**
- Ensure Ollama is running: `docker ps | grep ollama`
- Check network connectivity: `curl http://localhost:11434/api/tags`

**Frontend shows "Failed to load conversations"**
- Verify backend is running: `curl http://localhost:8001/`
- Check CORS settings in [backend/main.py](backend/main.py#L19)

**Out of memory errors**
- Use smaller models (1-2B parameters)
- Reduce number of concurrent models
- Enable GPU acceleration if available

### Enabling GPU Support

Uncomment GPU configuration in [docker-compose.yaml](docker-compose.yaml):

```yaml
deploy:
  resources:
    reservations:
      devices:
        - driver: nvidia
          count: 1
          capabilities: [gpu]
```

Requires NVIDIA Container Toolkit installed.

## 📊 Performance Considerations

- **Small models (1-2B)**: 2-4 GB RAM per model, faster inference
- **Medium models (7B)**: 8-12 GB RAM, better quality
- **Large models (13B+)**: 16+ GB RAM, best quality but slower

Running 3 small models + 1 chairman requires ~12-16 GB RAM total.

## 🤝 Where to Get Help

- **Technical Questions**: Open an issue in the repository
- **Ollama Documentation**: [https://ollama.ai/docs](https://ollama.ai/docs)
- **FastAPI Docs**: [https://fastapi.tiangolo.com](https://fastapi.tiangolo.com)
- **React Resources**: [https://react.dev](https://react.dev)

## 👥 Maintainers & Contributors

This project was developed as part of the **Gen AI course at De Vinci Higher Education**.

### Current Team
- [Add team member names here]
- TD Group: [Add TD group number]

### Original Concept
Inspired by Andrej Karpathy's LLM Council concept, refactored to run entirely on local infrastructure.

## 🤖 Generative AI Usage Statement

This project utilized the following AI tools during development:

- **Claude Sonnet 4.5** (via GitHub Copilot)
  - Code refactoring and optimization
  - Documentation generation
  - Architecture design suggestions
  - Debugging assistance

- **GitHub Copilot**
  - Code completion
  - Boilerplate generation

All AI-generated content was reviewed, tested, and modified by the development team.

## 🔄 Changelog

### Current Version
- ✅ Removed OpenRouter dependency
- ✅ Integrated Ollama for local LLM execution
- ✅ Implemented Docker containerization
- ✅ Created distributed REST API architecture
- ✅ Built 3-pane React interface
- ✅ Added conversation persistence
- ✅ Specialized in cognitive bias detection

### Planned Improvements
- [ ] Model health monitoring dashboard
- [ ] Token usage tracking
- [ ] Dynamic model registration UI
- [ ] Export conversation to Markdown/PDF
- [ ] Dark/Light theme toggle
- [ ] Response comparison diff view

## 📝 License

[Add license information - typically specified by the course/institution]

## 🙏 Acknowledgments

- **Andrej Karpathy** for the original LLM Council concept
- **Ollama Team** for excellent local LLM infrastructure
- **FastAPI & React communities** for robust frameworks
- **De Vinci Higher Education** for project guidance

---

**Note**: This is an educational project demonstrating distributed AI architecture and local LLM deployment. For production use, consider additional security hardening, error handling, and performance optimization.

## 📸 Screenshots

![3-Stage Workflow](docs/workflow-diagram.png)
*Example of the 3-stage council process*

![Web Interface](docs/ui-screenshot.png)
*Main application interface showing conversation management and responses*

---

**Quick Links**:
- [Installation](#installation--setup) | [Usage](#usage-examples) | [API Docs](#api-reference) | [Troubleshooting](#troubleshooting)
