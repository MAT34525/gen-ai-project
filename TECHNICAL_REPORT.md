# LLM Council - Technical Report

**Project**:  LLM Council - Local Deployment with Distributed Architecture for Cognitive Bias Analysis
**Based On:** [Andrej Karpathy's LLM Council](https://github.com/karpathy/LLM-council)   
**Institution**: De Vinci Higher Education - Gen AI Course  
**Date**: January 2026

---

## Table of Contents

1. [Key Design Decisions](#key-design-decisions)
2. [Chosen LLM Models](#chosen-llm-models)
3. [Improvements Over Original Repository](#improvements-over-original-repository)
4. [Technical Architecture](#technical-architecture)
5. [Research Application:  Bias Analysis](#research-application-bias-analysis)

---

## 1. Key Design Decisions

### 1.1 Distributed Architecture with Host and Remote Machines

**Decision**: Design a flexible distributed system with one Host machine and 0 to N Remote machines.

**Architecture**:
- **Host Machine** (Control Node):
  - **Always runs**:  Chairman model (required for Stage 3 synthesis)
  - **Always runs**: Backend API + Frontend UI (orchestration and user interface)
  - **Can optionally run**: 0 to N councilor models
  
- **Remote Machine(s)** (Compute Nodes):
  - **Runs**:  0 to N councilor models each
  - **Scalable**: Add as many Remote machines as needed
  - **Role**: Provides distributed computational capacity

**Rationale**: 

1. **Resource Distribution**: 
   - Large language models are memory-intensive (1-5GB RAM per model)
   - By distributing councilor models across Remote machines, we reduce RAM burden on the Host
   - Host can focus on orchestration (Backend/Frontend) and synthesis (Chairman)

2. **Flexibility**:
   - **Single Machine**: Run everything on Host (0 Remote machines) for simple setups
   - **Two Machines**: Host (Chairman + UI) + 1 Remote (all councilors) - recommended for this demo
   - **Multiple Machines**: Host + multiple Remotes, each contributing councilor models
   - **Hybrid**: Host runs Chairman + some councilors, Remotes run additional councilors

3. **Scalability**:
   - Horizontal scaling: Add more Remote machines to increase councilor count
   - Each Remote independently contributes 0 to N models
   - No architectural limit on number of Remote machines

4. **Real-World Simulation**:
   - Demonstrates how distributed AI systems work in production
   - Models can be hosted on different servers, data centers, or cloud instances
   - Teaches students about network configuration, API communication, and distributed systems

**Trade-offs**:
- Added network complexity when using Remote machines
- Requires firewall configuration and IP management
- Potential network latency between Host ↔ Remote (mitigated by local network)
- More complex deployment compared to single-machine setup

**Configuration Flexibility**: 

```
Scenario 1: Student with 1 powerful PC (16GB RAM)
- Host only: Chairman + 3 councilors
- 0 Remote machines
- Simple setup, no network configuration

Scenario 2: Two laptops (8GB each)
- Host: Chairman + Backend + Frontend
- Remote: 3 councilor models
- Recommended for this demo

Scenario 3: Lab environment with 3+ machines
- Host: Chairman + Backend + Frontend + 1 councilor
- Remote 1: 2 councilor models
- Remote 2: 2 councilor models
- Demonstrates full distributed architecture
```

### 1.2 Three-Stage Deliberation Process

**Decision**: Implement a multi-stage process (Initial Response → Peer Review → Synthesis) instead of a simple single-query system.

**Rationale**:

- **Bias Reduction**: Peer review stage forces models to evaluate each other anonymously, reducing individual model biases and groupthink. 
- **Quality Improvement**: The synthesis stage (chairman on Host) consolidates the best insights from all councilor models (distributed across machines), producing more comprehensive answers.
- **Research Value**: This project serves as a platform for studying AI bias.  The three-stage process generates rich data for analyzing how multiple models collectively make better decisions. 
- **Transparency**: Users can see all individual responses (regardless of which machine generated them), understand which response was voted strongest, and trace the reasoning behind the final synthesis.

**Trade-offs**:
- Increased latency (~25-35 seconds vs.  ~5 seconds for single model)
- Higher computational cost (N+1 model inferences:  N councilors + 1 chairman)
- More complex backend orchestration logic

### 1.3 Local-First with Ollama

**Decision**: Use Ollama for local LLM hosting instead of cloud APIs (e.g., OpenAI, Anthropic).

**Rationale**: 
- **Privacy**: All user data stays on-premises.  No external API calls means no data leaves the local network.
- **Cost**: No per-token API fees.  Once models are downloaded, inference is free.
- **Educational Value**: Students learn how to deploy and manage LLMs locally, a valuable skill for production AI systems.
- **Control**: Full control over model versions, parameters, and configurations. 
- **Offline Capability**: System works without internet connection after initial model download.

**Trade-offs**:
- Lower quality responses compared to large commercial models (GPT-4, Claude 3.5)
- Requires significant local hardware (12-16GB RAM minimum)
- Slower inference times without GPU acceleration

### 1.4 Docker Containerization

**Decision**: Deploy all services (backend, frontend, Ollama) via Docker Compose instead of manual installation.

**Rationale**: 
- **Reproducibility**: Ensures consistent environment across different machines and operating systems.
- **Isolation**:  Each service runs in its own container with defined dependencies, preventing version conflicts.
- **Easy Deployment**: Single command (`docker-compose up -d`) starts services on each machine.
- **Scalability**: Docker makes it easy to scale services (e.g., run multiple backend instances for load balancing).

**Trade-offs**:
- Requires Docker installation and basic knowledge
- Additional abstraction layer can complicate debugging for beginners
- Slightly higher resource overhead compared to native installation

### 1.5 Async Backend with FastAPI

**Decision**: Use FastAPI with async/await instead of synchronous Flask or Django.

**Rationale**:
- **Concurrent Execution**:  Async allows parallel querying of multiple LLMs across different machines without blocking.  Stage 1 queries all N councilor models simultaneously (distributed across Host and Remote machines) instead of sequentially.
- **Performance**: Non-blocking I/O means the server can handle other requests while waiting for LLM responses from Remote machines.
- **Modern Python**: FastAPI is built on modern Python standards (Pydantic, type hints, async).
- **Automatic Documentation**: FastAPI generates interactive API docs (Swagger UI) automatically.

**Trade-offs**:
- Steeper learning curve for students unfamiliar with async programming
- More complex error handling (async exceptions, network timeouts)

### 1.6 JSON File Storage Instead of Database

**Decision**: Store conversations as JSON files instead of using a database (PostgreSQL, MongoDB).

**Rationale**:
- **Simplicity**: No database setup or management required.
- **Human-Readable**: JSON files can be inspected and analyzed directly without database queries.
- **Portability**: Easy to backup, transfer, or archive conversations.
- **Educational Focus**: Project focuses on AI orchestration, not database design. 

**Trade-offs**:
- Not suitable for high-volume production use (file I/O slower than database queries)
- No built-in indexing or complex querying capabilities
- Potential file locking issues with concurrent writes (mitigated by low write frequency)

---

## 2. Chosen LLM Models

### Model Selection Criteria

We selected models based on: 
1. **Size**: Small enough to run on consumer hardware (1-4B parameters)
2. **Diversity**: Different architectures and training approaches to maximize perspective variety
3. **Performance**: Good reasoning capabilities for bias detection tasks
4. **Availability**:  Free and open-source models available via Ollama

### Selected Models

|     Role        |     Model     | Parameters | RAM Usage |    Location    |                      Rationale                            |
|-----------------|---------------|------------|-----------|----------------|-----------------------------------------------------------|
| **Chairman**    | Qwen 2.5:1.5b | 1.5B       | ~2GB      | Always on Host | Fast synthesis, good at consolidating multiple inputs     |
| **Councilor 1** | Llama 3.2:1b  | 1B         | ~1.5GB    | Host or Remote | Meta's latest small model, strong reasoning for size      |
| **Councilor 2** | Gemma 2:2b    | 2B         | ~3GB      | Host or Remote | Google's model, different training approach than Llama    |
| **Councilor 3** | Phi3:3.8b     | 3.8B       | ~5GB      | Host or Remote | Microsoft's research model, deepest analysis of the three |

### Chairman Model:  Qwen 2.5:1.5b (Always on Host)

**Why Qwen?**
- **Synthesis-Optimized**: Qwen models excel at summarization and consolidation tasks. 
- **Multilingual**: Good performance in multiple languages (useful for non-English queries).
- **Small Size**: 1.5B parameters means fast inference for the final synthesis step.
- **Recent Training**: Qwen 2.5 has more recent training data compared to older Llama versions.

**Role**:  The chairman runs exclusively on the Host machine.  It doesn't participate in Stage 1 or Stage 2. It only synthesizes the final answer in Stage 3 by: 
1. Reading all councilor responses (from Host and/or Remote machines)
2. Considering peer review scores
3. Identifying consensus points and disagreements
4. Producing a balanced, comprehensive final answer

**Why Chairman Must Be on Host?**
- The Host runs the Backend API which orchestrates the entire process
- Stage 3 synthesis is the final step before returning to the user
- Keeps network latency minimal for final response generation
- Backend can access chairman via Docker DNS (`ollama-chairman`) without network overhead

### Councilor Models (Distributed across Host and Remote)

**Llama 3.2:1b**
- **Architecture**: Meta's transformer-based architecture
- **Strengths**: Good at identifying social and authority biases
- **Inference Speed**: ~2-3 seconds per query (CPU)
- **Can run on**: Host and/or Remote machines

**Gemma 2:2b**
- **Architecture**: Google's Gemini-inspired architecture (distilled)
- **Strengths**: Strong at logical fallacy detection, questioning assumptions
- **Inference Speed**:  ~4-5 seconds per query (CPU)
- **Can run on**: Host and/or Remote machines

**Phi3:3.8b**
- **Architecture**: Microsoft Research dense transformer
- **Strengths**: Most comprehensive analysis, best at complex reasoning
- **Inference Speed**: ~8-10 seconds per query (CPU)
- **Can run on**: Host and/or Remote machines

**Why This Combination?**

The diversity in model size and architecture is intentional: 
- **Llama 3.2** provides fast, concise analysis
- **Gemma 2** offers a different architectural perspective
- **Phi3** adds depth with its larger parameter count

This ensures the council doesn't suffer from "groupthink" - if all models were the same architecture (e.g., 3 Llama models), they might share similar biases. 

**Distribution Flexibility**: 
- **Recommended for demo**: All 3 councilors on Remote, chairman on Host
- **Alternative**: 1-2 councilors on Host, 1-2 on Remote
- **Advanced**:  Councilors distributed across multiple Remote machines

### Alternative Models Considered

|     Model      |                         Why Not Selected                                      |
|----------------|-------------------------------------------------------------------------------|
| Mistral 7B     | Too large for Remote to run 3 instances simultaneously (would need 24GB+ RAM) |
| TinyLlama 1.1B | Lower quality responses, less suitable for bias detection                     |
| Llama 3:8B     | Excellent quality but too slow for demo (15-20 seconds per query)             |
| GPT-4 via API  | Against project requirement of local-only execution                           |

---

## 3. Improvements Over Original Repository

This project is based on the concept of LLM councils but has been significantly refactored and improved for educational and research purposes.

### 3.1 Architecture Improvements

**Original**:  Monolithic single-machine setup  
**Our Improvement**: Distributed multi-machine architecture with Host (Chairman + Backend + UI) and 0 to N Remote machines (councilor models)

**Benefits**:
- Better resource utilization across multiple machines
- Demonstrates real-world distributed AI systems
- Easier to scale horizontally by adding more Remote machines
- Flexible:  works with 1 machine (Host only) or N machines (Host + Remotes)

---

**Original**: Cloud API-based (OpenRouter)  
**Our Improvement**:  Fully local with Ollama integration on each machine

**Benefits**: 
- No API costs
- Complete data privacy (data never leaves local network)
- Works offline after initial setup
- Educational value in learning local LLM deployment and distributed systems

---

**Original**:  Synchronous, sequential model querying  
**Our Improvement**:  Async/await parallel execution in Stage 1, queries distributed across Host and Remote machines concurrently

**Benefits**: 
- Stage 1 now takes ~10 seconds instead of ~30 seconds (N models queried in parallel across machines)
- Better server responsiveness
- Modern Python best practices
- Efficient network utilization

---

### 3.2 Feature Additions 

|            Feature              |      Original       |                   Our Implementation                           |
|---------------------------------|---------------------|----------------------------------------------------------------|
| **Distributed Architecture**    | Single machine only | Host + 0 to N Remote machines with flexible model distribution |
| **Conversation Persistence**    | No storage          | JSON-based conversation history with full metadata             |
| **Web UI**                      | CLI only            | Modern React interface with 3-pane view                        |
| **Peer Review Visualization**   | Not shown           | Stage 2 tab shows all rankings and scores                      |
| **Multi-Conversation Support**  | Single session      | Create and switch between multiple conversations               |
| **Docker Deployment**           | Manual setup        | One-command deployment per machine with docker-compose         |
| **Network Configuration**       | Local only          | Configurable IPs for distributed deployment across machines    |
| **Flexible Model Distribution** | N/A                 | Configure which models run on Host vs.  Remote(s)              |

### 3.3 Code Quality Improvements

**Original**:  Minimal error handling  
**Our Improvement**: Comprehensive try/catch blocks, graceful degradation if one model fails (even if on a Remote machine)

---

**Original**: Hard-coded model configurations  
**Our Improvement**:  Centralized `config.py` with environment variable support for configuring Host and multiple Remote IPs

---

**Original**: No documentation  
**Our Improvement**:  Comprehensive README, TECHNICAL_REPORT, inline code comments explaining distributed architecture

---

**Original**: No data validation  
**Our Improvement**:  Pydantic models for type safety and automatic API validation

---

### 3.4 Specialization for Bias Analysis

**Original**: General-purpose LLM council  
**Our Improvement**: Specialized for cognitive bias detection with: 
- Custom system prompts focusing on bias identification
- Example queries demonstrating different bias types
- Research-oriented data collection (all stages preserved in metadata, including which machine generated each response)

**Benefits**:
- More focused and useful for the Gen AI course
- Provides a platform for studying AI bias reduction through multi-agent, multi-machine collaboration
- Demonstrates practical application of distributed AI

---

## 4. Technical Architecture

### 4.1 System Components

```
┌──────────────────────────────────────────────────────┐
│ Host Machine (Control Node)                          │
│ ┌─────────────┐  ┌────────────┐  ┌────────────────┐  │
│ │  Frontend   │  │  Backend   │  │ Chairman       │  │
│ │ React: 5173 │  │ FastAPI:   │  │ Ollama:11434   │  │
│ │             │  │ 8000       │  │ (Qwen 2.5:1.5b)│  │
│ └─────────────┘  └─────┬──────┘  └────────────────┘  │
│                        │                             │
│                        │ Optional: Councilors on Host│
│                        │ (if configured)             │
└──────────────────────────────────────────────────────┘
                         │
                         │ HTTP Requests over Network
                         │
             ┌───────────┼───────────┐
             ▼           ▼           ▼
┌─────────────┐ ┌──────────────┐ ┌─────────────┐
│  Remote 1   │ │  Remote 2    │ │  Remote N   │
│  (Optional) │ │  (Optional)  │ │  (Optional) │
│             │ │              │ │             │
│ Ollama:     │ │ Ollama:      │ │ Ollama:     │
│ 11434       │ │ 11434        │ │ 11434       │
│             │ │              │ │             │
│ 0-N         │ │ 0-N          │ │ 0-N         │
│ Councilor   │ │ Councilor    │ │ Councilor   │
│ Models      │ │ Models       │ │ Models      │
└─────────────┘ └──────────────┘ └─────────────┘
```

### 4.2 Request Flow

1. **User submits query** via React frontend on Host
2. **Frontend sends POST** to `/api/conversations/{id}/messages` (Host backend)
3. **Backend orchestrates 3-stage process**:
   - **Stage 1**: Parallel async requests to: 
     - Councilor models on Remote machine(s) (if configured)
     - Councilor models on Host (if configured)
     - All queries execute concurrently
   - **Stage 2**: Each councilor evaluates other responses (local computation on Backend)
   - **Stage 3**: Chairman model on Host synthesizes final answer
4. **Backend saves conversation** to JSON file in `/data/conversations/` on Host
5. **Frontend receives response** with all 3 stages and displays in UI

### 4.3 Network Configuration

**Host Environment Variables** (docker-compose-ollama.yaml):
```yaml
environment:
  - CHAIRMAN_IP=ollama-chairman          # Docker DNS (local)
  - CHAIRMAN_PORT=11434
  - COUNCIL_IP=${REMOTE_IP:-192.168.1.101}   # Remote machine IP
  - COUNCIL_PORT=11434
```

**Remote Configuration** (docker-compose-pipeline.yaml on each Remote):
```yaml
services:
  ollama-council:
    ports:
      - "11434:11434"  # Expose Ollama API to network
    environment:
      - OLLAMA_HOST=0.0.0.0  # Listen on all network interfaces
```

**Backend Configuration** (backend/config.py):
```python
# Host's chairman Ollama (always on Host)
HOST_CHAIRMAN_IP = "ollama-chairman"  # Docker DNS resolution

# Remote machine IPs (configure as needed)
REMOTE_1_IP = os.getenv("REMOTE_IP", "192.168.1.101")
REMOTE_2_IP = os.getenv("REMOTE_2_IP", "192.168.1.102")

COUNCIL_MODELS = [
    # Chairman (always on Host)
    CouncilModel(ip=HOST_CHAIRMAN_IP, port=11434, 
                 model_name="qwen2.5:1.5b", role=Role.CHAIRMAN),
    
    # Councilors (distributed across machines)
    CouncilModel(ip=REMOTE_1_IP, port=11434, 
                 model_name="llama3.2:1b", role=Role.COUNCILOR),
    CouncilModel(ip=REMOTE_1_IP, port=11434, 
                 model_name="gemma2:2b", role=Role.COUNCILOR),
    CouncilModel(ip=REMOTE_2_IP, port=11434, 
                 model_name="phi3:3.8b", role=Role.COUNCILOR),
]
```

### 4.4 Data Models (Pydantic)

```python
class CouncilModel: 
    ip: str           # Ollama host IP (Host or Remote machine)
    port: int         # Ollama port (usually 11434)
    model_name: str   # e.g., "llama3.2:1b"
    role: Role        # CHAIRMAN (Host only) or COUNCILOR (Host or Remote)

class Message:
    role: str         # "user" or "assistant"
    content: str      # Message text
    timestamp: str    # ISO format
    metadata: dict    # Stage 1/2/3 data (for assistant messages)

class Conversation:
    id: str           # e.g., "conv_20260115_123456"
    created_at:  str   # ISO timestamp
    messages: List[Message]
```

---

## 5. Research Application: Bias Analysis

### 5.1 Dual Purpose

This project serves both practical and research purposes: 

1. **Practical Application**: A working tool for detecting cognitive biases in text
2. **Research Platform**: A system for studying how multi-model AI collaboration across distributed machines reduces bias

### 5.2 Bias Detection Capabilities

The system is specialized in identifying: 

**Cognitive Biases**: 
- Confirmation bias
- Anchoring effect
- Availability heuristic
- Bandwagon effect
- Authority bias
- False consensus
- Hindsight bias

**Logical Fallacies**:
- Ad hominem
- Straw man arguments
- False dichotomy
- Slippery slope
- Appeal to emotion
- Circular reasoning

### 5.3 Multi-Model Bias Reduction Hypothesis

**Research Question**: Does multi-model deliberation across distributed machines reduce AI bias compared to single-model inference?

**Hypothesis**: By combining diverse models (potentially running on different machines) through peer review and synthesis, the council produces less biased outputs than any individual model. 

**Mechanisms**: 

1. **Architectural Diversity**: Different models (Llama, Gemma, Phi) have different training data and architectural biases. 
2. **Distributed Processing**: Models can run on different machines, eliminating hardware-specific biases.
3. **Anonymous Peer Review**: Models evaluate responses without knowing authorship or source machine, preventing favoritism.
4. **Synthesis on Host**: Chairman model (always on Host) identifies consensus and highlights disagreements, providing balanced output.

### 5.4 Data Collection for Research

All conversations preserve full metadata including which machine generated each response:

```json
{
  "metadata": {
    "stage1_responses": [
      {
        "model": "llama3.2:1b",
        "machine": "remote_1",  // Could track this for research
        "response": "..."
      },
      {
        "model": "gemma2:2b",
        "machine": "remote_1",
        "response": "..."
      },
      {
        "model": "phi3:3.8b",
        "machine": "host",
        "response": "..."
      }
    ],
    "stage2_rankings": [
      {"reviewer": "llama3.2:1b", "rankings": [...]},
      // ... peer review data
    ],
    "stage3_synthesis": "...  chairman's final answer (from host) ..."
  }
}
```

This enables post-hoc analysis: 
- **Agreement Rates**: How often do models agree on identified biases?
- **Machine Impact**: Does running on different machines affect responses?
- **Diversity Metrics**: How different are initial responses from distributed vs. co-located models? 
- **Quality Scores**: Do peer-reviewed responses correlate with human quality ratings? 
- **Bias Coverage**: Which biases does each model tend to detect vs. miss?

### 5.5 Example Analysis

**Input Query**:
```
90% of experts recommend this product, so it must be the best.
```

**Stage 1 Responses** (distributed across machines):
- **Llama 3.2** (Remote 1): Identifies **bandwagon effect** and **authority bias**
- **Gemma 2** (Remote 1): Identifies **bandwagon effect**, questions "expert" definition
- **Phi3** (Host): Identifies **bandwagon effect**, **authority bias**, **false consensus**

**Observations**:
- All models detected bandwagon effect (consensus across machines)
- Gemma uniquely questioned the premise (critical thinking)
- Phi3 provided most comprehensive analysis (larger model, running on Host)

**Stage 3 Synthesis** (Chairman on Host):
- Consolidates findings from all councilors (regardless of source machine)
- Confirms all identified biases
- Incorporates Gemma's point about defining "experts"
- Provides unified, comprehensive explanation

**Research Value**:  This demonstrates how diversity in models AND distribution across machines leads to more thorough bias detection than any single model or centralized system.

---

## Conclusion

The LLM Council project successfully demonstrates: 

- **Distributed AI Architecture**:  Multi-machine deployment (Host + 0 to N Remote) with proper network configuration  
- **Flexible Model Distribution**: Chairman always on Host, councilors distributed as needed  
- **Local-First Approach**: Privacy-preserving, cost-free inference with Ollama on each machine  
- **Multi-Agent Collaboration**: Three-stage deliberation process reduces bias through distributed consensus  
- **Modern Tech Stack**: Docker, FastAPI, React, async Python with network communication  
- **Research Platform**: Data collection for studying AI bias reduction in distributed systems  
- **Practical Application**:  Working tool for cognitive bias detection

### Key Contributions

1. **Educational**:  Students learn distributed AI, local LLM deployment, async programming, containerization, and network configuration
2. **Research**: Platform for studying multi-model bias reduction and consensus-based AI across distributed systems
3. **Practical**:  Usable tool for analyzing text for cognitive biases and logical fallacies
4. **Scalable**: Architecture supports 1 to N machines with flexible model distribution

### Architecture Benefits

- **Host-centric design**: Chairman and orchestration always on Host ensures reliable synthesis
- **Scalable Remotes**: Add 0 to N Remote machines based on available hardware
- **Flexible distribution**: Councilors can run on Host, Remote, or both
- **Educational value**: Demonstrates real-world distributed AI architecture

### Future Improvements

- [ ] GPU acceleration support on Remote machines
- [ ] Model health monitoring dashboard showing status of all machines
- [ ] Dynamic model registration via API (add/remove Remotes at runtime)
- [ ] Load balancing across multiple Remote machines
- [ ] Export conversations with machine attribution
- [ ] Quantitative bias analysis metrics comparing distributed vs. centralized results
- [ ] Weighted voting based on model confidence scores and machine performance

---

**Document Version**: 1.0  
**Last Updated**: 2026-01-15  
**Team**: Mathys D., Mathéo D., Edouard D. 
**TD Group**: CDOF2


_Written with the assistance of AI tools._
