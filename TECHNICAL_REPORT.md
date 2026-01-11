# Technical Report - LLM Council Local Deployment

## Project Information

**Project:** LLM Council - Local Deployment with Distributed Architecture  
**Based On:** [Andrej Karpathy's LLM Council](https://github.com/karpathy/LLM-council)  
**Date:** January 2026  
**Architecture:** 2-PC Distributed System  

---

## Executive Summary

This project successfully refactors the original LLM Council system from a cloud-based architecture (using OpenRouter) to a fully local, distributed system using Ollama. The implementation supports a 2-PC configuration where:

- **PC1** hosts the Chairman LLM, Backend API, and Frontend
- **PC2** hosts multiple Council LLMs for diverse perspectives

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
PC1 (Chairman): 1 model for synthesis
PC2 (Council):  3+ models for initial responses and peer review
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
- 3 Docker Compose files for different scenarios
- Persistent volumes for model storage
- Custom networks for service communication

### 4. Configuration Management

**Decision:** Environment variables + centralized config file.

**Rationale:**
- ✅ **Flexibility**: Change IPs without code changes
- ✅ **Security**: Sensitive data in .env (not committed)
- ✅ **Easy Deployment**: Different configs for dev/prod
- ✅ **Clear Documentation**: .env.example as template

**Key Variables:**
- `CHAIRMAN_IP` / `CHAIRMAN_PORT` / `CHAIRMAN_MODEL`
- `COUNCIL_IP` / `COUNCIL_PORT`

---

## Architecture Overview

### System Architecture

```
┌──────────────────────────────────────────────────────────┐
│                    PC1 (Chairman)                        │
│                                                          │
│  ┌────────────┐    ┌──────────────┐    ┌────────────┐  │
│  │  Frontend  │───▶│   Backend    │───▶│  Ollama    │  │
│  │  (React)   │    │  (FastAPI)   │    │  Chairman  │  │
│  │   :5173    │    │    :8000     │    │   :11434   │  │
│  └────────────┘    └──────┬───────┘    └────────────┘  │
│                           │                              │
└───────────────────────────┼──────────────────────────────┘
                            │
                            │ HTTP REST API
                            │ (Ollama Chat Endpoint)
                            │
┌───────────────────────────▼──────────────────────────────┐
│                    PC2 (Council)                         │
│                                                          │
│              ┌────────────────────────┐                 │
│              │   Ollama Council       │                 │
│              │      :11434            │                 │
│              │                        │                 │
│              │  ┌──────────────────┐ │                 │
│              │  │ llama3.2:1b      │ │                 │
│              │  │ (Councilor_1)    │ │                 │
│              │  └──────────────────┘ │                 │
│              │  ┌──────────────────┐ │                 │
│              │  │ gemma2:2b        │ │                 │
│              │  │ (Councilor_2)    │ │                 │
│              │  └──────────────────┘ │                 │
│              │  ┌──────────────────┐ │                 │
│              │  │ phi3:3.8b        │ │                 │
│              │  │ (Councilor_3)    │ │                 │
│              │  └──────────────────┘ │                 │
│              └────────────────────────┘                 │
│                                                          │
└──────────────────────────────────────────────────────────┘
```

### Communication Flow

#### Stage 1: First Opinions
```
User Query → Backend → Council Models (PC2) ─┐
                                              ├→ Collect Responses
Backend ← Council Models (PC2) ───────────────┘
```

#### Stage 2: Peer Review
```
Responses → Backend → Anonymize → Council Models (PC2) ─┐
                                                         ├→ Rank Others
Backend ← Rankings ← Council Models (PC2) ───────────────┘
```

#### Stage 3: Chairman Synthesis
```
All Data → Backend → Chairman Model (PC1) ─┐
                                            ├→ Synthesize
Backend ← Final Answer ← Chairman (PC1) ────┘
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

## Improvements Over Original Repository

### 1. Local Execution (Privacy & Cost)

| Aspect | Original | This Version |
|--------|----------|--------------|
| **Data Privacy** | Sent to cloud | 100% local |
| **Cost per Query** | $0.01-0.10 | $0.00 |
| **Internet Required** | Yes | No (after setup) |
| **API Limits** | Rate limited | None |

### 2. Distributed Architecture

| Aspect | Original | This Version |
|--------|----------|--------------|
| **Chairman** | Mixed with council | Dedicated PC/instance |
| **Scaling** | Vertical only | Horizontal possible |
| **Load Distribution** | Single machine | Multiple machines |
| **Resource Allocation** | Shared | Optimized per role |

### 3. Infrastructure

| Aspect | Original | This Version |
|--------|----------|--------------|
| **Deployment** | Manual | Docker Compose |
| **Configuration** | Code changes | Environment variables |
| **Setup Time** | 30+ minutes | 5-10 minutes |
| **Reproducibility** | Low | High |

### 4. Documentation

**Original:**
- Basic README
- Setup instructions
- No deployment guide

**This Version:**
- Comprehensive README with architecture diagrams
- Detailed DEPLOYMENT.md (60+ sections)
- QUICK_REFERENCE.md for common commands
- Setup scripts (PowerShell + Bash)
- .env.example with detailed comments
- Multiple docker-compose files for different scenarios

### 5. Additional Features

✨ **Health Checks:** Monitor model availability  
✨ **Error Handling:** Graceful failures, better timeout management  
✨ **Configurability:** Easy model changes via config file  
✨ **Network Diagnostics:** Tools to debug connectivity issues  
✨ **GPU Support:** Optional GPU acceleration  
✨ **Model Management:** Automatic pulling and creation  

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

### Frontend (React + Vite)

**Unchanged but benefits:**
- Same UI/UX
- Faster responses (local models)
- No API costs
- Works offline

### Docker Configuration

**3 Docker Compose Files:**

1. **docker-compose.full.yaml**
   - All services on one machine
   - For development/testing
   - 5 containers total

2. **docker-compose.pc1.yaml**
   - Chairman + Backend + Frontend
   - Connects to remote council
   - 3 containers

3. **docker-compose.pc2.yaml**
   - Council Ollama only
   - Serves models to PC1
   - 1 container

**Volumes:**
- `ollama-chairman-data`: Persistent model storage for Chairman
- `ollama-council-data`: Persistent model storage for Council
- `./data`: Conversation history

### Network Communication

**Protocol:** HTTP REST (Ollama Chat API)

**Endpoint:** `POST http://{ip}:{port}/api/chat`

**Payload:**
```json
{
  "model": "llama3.2:1b",
  "messages": [
    {"role": "system", "content": "..."},
    {"role": "user", "content": "..."}
  ],
  "stream": false
}
```

**Security Considerations:**
- No authentication (internal network only)
- Consider VPN for remote setup
- Firewall rules for port 11434

---

## Testing & Validation

### Test Scenarios

#### ✅ Test 1: Single PC (Development)
- All services on one machine
- Verified 3-stage workflow
- Confirmed model independence

#### ✅ Test 2: 2-PC Setup (Production)
- Chairman on PC1
- Council on PC2
- Verified network communication
- Tested failover scenarios

#### ✅ Test 3: Model Variety
- Tested with different model combinations
- Verified custom prompts work
- Confirmed French language support

### Performance Metrics

**Response Times (on consumer hardware):**
- Stage 1 (3 models): 15-30 seconds
- Stage 2 (3 reviews): 20-40 seconds  
- Stage 3 (synthesis): 5-10 seconds
- **Total:** 40-80 seconds per query

**Resource Usage:**
- RAM: 6-8 GB for 4 models (1.5-3.8B params)
- CPU: 50-90% during inference
- Network: <100 KB per query

---

## Deployment Scenarios

### Scenario 1: Solo Developer (1 PC)
```bash
docker-compose -f docker-compose.full.yaml up -d
```
All services on one machine, suitable for development.

### Scenario 2: Team of 2 (2 PCs)
- **PC1:** Chairman + Backend + Frontend
- **PC2:** 3 Council models

```bash
# PC2
docker-compose -f docker-compose.pc2.yaml up -d

# PC1
export PC2_IP=192.168.1.101
docker-compose -f docker-compose.pc1.yaml up -d
```

### Scenario 3: Team of 3-5 (3+ PCs)
- **PC1:** Chairman + Backend + Frontend
- **PC2:** Councilor 1 + Councilor 2
- **PC3:** Councilor 3 + additional models

Requires custom docker-compose configuration.

---

## Challenges & Solutions

### Challenge 1: OpenRouter Removal
**Problem:** Original code tightly coupled to OpenRouter  
**Solution:** Created new `ollama.py` module with same interface  
**Impact:** Minimal changes to `council.py` logic

### Challenge 2: Network Communication
**Problem:** LLMs need to communicate across machines  
**Solution:** Ollama REST API + environment-based configuration  
**Impact:** Flexible, scalable architecture

### Challenge 3: Model Management
**Problem:** Multiple models across multiple machines  
**Solution:** Docker volumes + automatic model pulling  
**Impact:** Simplified deployment

### Challenge 4: Configuration Complexity
**Problem:** Different setups need different configs  
**Solution:** Multiple docker-compose files + .env variables  
**Impact:** Easy to switch between scenarios

---

## Future Enhancements

### Potential Improvements

1. **UI Enhancements**
   - Real-time progress indicators
   - Model health status dashboard
   - Dark mode
   - Side-by-side response comparison

2. **Performance**
   - Response caching
   - Parallel stage execution where possible
   - Model warm-up on startup

3. **Scalability**
   - Kubernetes deployment
   - Load balancing for multiple council nodes
   - Automatic model distribution

4. **Monitoring**
   - Prometheus metrics
   - Grafana dashboards
   - Response time tracking
   - Model usage analytics

5. **Security**
   - HTTPS support
   - Authentication/authorization
   - API rate limiting
   - Audit logging

---

## Lessons Learned

### Technical Lessons

1. **Ollama is Production-Ready:** Stable, well-documented, easy to use
2. **Docker Simplifies Deployment:** Consistent environments across machines
3. **Local LLMs are Viable:** Good enough for many use cases
4. **Network Latency:** Less critical than inference time for this use case

### Project Management

1. **Documentation is Critical:** Good docs save deployment time
2. **Automation Pays Off:** Setup scripts reduce errors
3. **Test Incrementally:** Verify each component before integration
4. **Plan for Failure:** Timeouts, retries, error messages matter

---

## Conclusion

This project successfully achieves all mandatory requirements:

✅ **Local LLM Execution:** 100% local via Ollama  
✅ **Distributed Architecture:** Chairman + Council on separate PCs  
✅ **REST API Communication:** Ollama HTTP API  
✅ **Chairman Separation:** Dedicated instance, synthesis only  
✅ **Full 3-Stage Workflow:** All stages functional  

### Key Achievements

1. **Zero Cost:** No API fees, runs indefinitely
2. **Privacy:** All data stays local
3. **Scalable:** Easy to add more models/machines
4. **Documented:** Comprehensive guides for deployment
5. **Maintainable:** Clean code, clear architecture

### Production Readiness

The system is ready for:
- ✅ Academic demonstrations
- ✅ Internal company use  
- ✅ Privacy-sensitive applications
- ✅ Offline environments
- ⚠️ Public internet (needs security hardening)

---

## Generative AI Usage Declaration

### Tools Used

1. **GitHub Copilot**
   - Code completion and suggestions
   - Boilerplate generation
   - Refactoring assistance

2. **Claude Sonnet 4.5 (via GitHub Copilot Chat)**
   - Architecture design discussions
   - Documentation writing
   - Code review and optimization
   - Docker configuration
   - Bash/PowerShell script creation

3. **ChatGPT** (limited use)
   - Quick syntax checks
   - Debugging specific errors

### Purposes

- **Refactoring:** OpenRouter → Ollama migration
- **Infrastructure:** Docker Compose configurations
- **Documentation:** README, DEPLOYMENT.md, guides
- **Automation:** Setup scripts for Windows/Linux
- **Best Practices:** Code structure and error handling
- **Design:** Architecture decisions and diagrams

### Declaration

All AI-generated code and documentation was:
- ✅ Reviewed line by line
- ✅ Tested thoroughly
- ✅ Modified to fit project requirements
- ✅ Understood completely by the team

No code was blindly copy-pasted. AI was used as a collaborative tool to enhance productivity, not replace understanding.

---

## References

- [Andrej Karpathy's LLM Council](https://github.com/karpathy/LLM-council)
- [Ollama Documentation](https://ollama.ai/docs)
- [FastAPI Documentation](https://fastapi.tiangolo.com/)
- [Docker Documentation](https://docs.docker.com/)
- [React Documentation](https://react.dev/)

---

**Project Repository:** [GitHub Link]  
**Demo Video:** [Link if available]  
**Deployment Guide:** [DEPLOYMENT.md](DEPLOYMENT.md)  
**Quick Reference:** [QUICK_REFERENCE.md](QUICK_REFERENCE.md)  

---

*This technical report was created as part of the LLM Council Local Deployment project.*
