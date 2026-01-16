# Technical Report - LLM Council Local Deployment

## Project Information

**Team Members:** DECKER Mathys, DUGUE Mathéo, D'ABOVILLE Edouard
                __Credits:__ Noufel BOUCHENEB for the frontend

**Project:** LLM Council - Local Deployment with Distributed Architecture  
**Based On:** [Andrej Karpathy's LLM Council](https://github.com/karpathy/LLM-council)  
**Date:** January 2026  
**Architecture:**  Multiple PC Distributed System  

---

## Executive Summary

This project successfully refactors the original LLM Council system from a cloud-based architecture (using OpenRouter) to a fully local, distributed system using Ollama. The implementation supports multiple PC configuration where:

- **Host_PC** hosts the Chairman LLM, Backend API, Frontend and at least 1 Council LLM
- **Remote_PC** host multiple Council LLMs for diverse perspectives

The system maintains all three stages of the original council workflow while providing complete data privacy, zero cost per query, and horizontal scalability.

---

## Key Design Decisions

### 1. Ollama as LLM Infrastructure

**Decision:** Use Ollama instead of GPT4All, Llamafile, or direct HuggingFace integration.

**Rationale:**
- ✅ **REST API**: Built-in HTTP API for network communication
- ✅ **Simple Model Management**: Easy pull, list, and run commands
- ✅ **Docker Support**: Official Docker images for easy deployment
- ✅ **Multi-model**: Run multiple models on single instance
- ✅ **GPU Acceleration**: Automatic GPU detection and usage
- ✅ **Active Development**: Regular updates and growing model library

**Trade-offs:**
- Limited to Ollama-supported models
- Requires Ollama running on each machine
- Additional layer between code and models

### 2. Distributed Architecture

**Decision:** Separate Chairman from Council on different machines.

**Rationale:**
- ✅ **Requirement Compliance**: Meets project specifications
- ✅ **Load Distribution**: Spreads computational load
- ✅ **Role Separation**: Chairman only synthesizes, never participates
- ✅ **Scalability**: Can add more council nodes easily
- ✅ **Resource Optimization**: Different machines can have different specs

**Implementation:**
```
Host_PC (Chairman + Council): 1 model for synthesis and possibility to have 1 council member
Remote_PC (Council):  3+ models for initial responses and peer review
```

### 3. Docker Containerization

**Decision:** Full containerization with Docker Compose.

**Rationale:**
- ✅ **Reproducibility**: Same environment on all machines
- ✅ **Easy Deployment**: One-command setup
- ✅ **Isolation**: Each service in its own container
- ✅ **Network Management**: Built-in service discovery
- ✅ **Version Control**: Infrastructure as code

**Structure:**
- 1 Docker Compose file 
- Persistent volumes for model storage
- Custom networks for service communication


## Architecture Overview

### System Architecture

```
┌──────────────────────────────────────────────────────────┐
│                    Host_PC (Chairman)                    │
│                                                          │
│  ┌────────────┐     ┌──────────────┐    ┌────────────┐   │
│  │  Frontend  │───▶│   Backend    │───▶│  Ollama    │   │
│  │  (React)   │     │  (FastAPI)   │    │  Chairman  │   │
│  │   :5173    │     │    :8000     │    │   :11434   │   │
│  └────────────┘     └──────┬───────┘    └────────────┘   │
│                            │                             │
└────────────────────────────┼─────────────────────────────┘
                             │
                             │ HTTP REST API
                             │ (Ollama Chat Endpoint)
                             │
┌────────────────────────────▼─────────────────────────────┐
│                    Remote_PC (Council)                   |
│                                                          │
│              ┌────────────────────────┐                  │
│              │   Ollama Council       │                  │
│              │      :11434            │                  │
│              │                        │                  │
│              │  ┌──────────────────┐  │                  │
│              │  │ llama3.2:1b      │  │                  │
│              │  │ (Councilor_1)    │  │                  │
│              │  └──────────────────┘  │                  │
│              │  ┌──────────────────┐  │                  │ 
│              │  │ gemma2:2b        │  │                  │
│              │  │ (Councilor_2)    │  │                  │
│              │  └──────────────────┘  │                  │
│              │  ┌──────────────────┐  │                  │
│              │  │ phi3:3.8b        │  │                  │
│              │  │ (Councilor_3)    │  │                  │
│              │  └──────────────────┘  │                  │
│              └────────────────────────┘                  │
│                                                          │
└──────────────────────────────────────────────────────────┘
```
---

## Chosen LLM Models

### Chairman Model (PC1)

**Model:** `qwen2.5:1.5b`

**Characteristics:**
- Size: ~1.0 GB
- Parameters: 1.5 billion
- Optimized for: Fast synthesis and summarization
- Speed: ⚡⚡⚡ Very Fast

**Why Chosen:**
- Small enough for quick responses
- Sufficient for synthesis task (not initial reasoning)
- Good balance of quality and speed
- Tested for French language support

### Council Models (PC2)

#### Councilor 1: `llama3.2:1b`
- **Size:** ~1.3 GB
- **Specialty:** General reasoning
- **Speed:** ⚡⚡⚡ Very Fast
- **Role:** Fast initial response generation

#### Councilor 2: `gemma2:2b`
- **Size:** ~1.6 GB  
- **Specialty:** Balanced performance
- **Speed:** ⚡⚡ Fast
- **Role:** Quality analysis with reasonable speed

#### Councilor 3: `phi3:3.8b`
- **Size:** ~2.3 GB
- **Specialty:** Complex reasoning
- **Speed:** ⚡⚡ Fast
- **Role:** Deep analysis and bias detection

**Why This Mix:**
- **Diversity:** Different model families (Meta, Google, Microsoft)
- **Complementary:** Different strengths and reasoning patterns
- **Practical:** All run efficiently on consumer hardware
- **Scalable:** Can add more models easily

---

## Technical Implementation Details

### Backend (FastAPI)

**File Structure:**
```
backend/
├── main.py          # API endpoints
├── council.py       # 3-stage orchestration logic
├── ollama.py        # Ollama client (NEW - replaces openrouter.py)
├── config.py        # Configuration management
├── models.py        # Data models (CouncilModel, Role enums)
├── storage.py       # Conversation persistence
├── Dockerfile       # Docker image definition
└── requirements.txt # Python dependencies
```

**Key Changes:**
1. **New Module:** `ollama.py` replaces `openrouter.py`
   - Communicates with Ollama REST API
   - Supports parallel queries
   - Includes health check functionality
   
2. **Enhanced Config:** `config.py`
   - Environment variable integration
   - Separate Chairman and Council configuration
   - Easy model customization

3. **Improved Council:** `council.py`
   - Better error handling
   - Support for distributed models
   - Enhanced logging

