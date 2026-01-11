#!/bin/bash
# ============================================================================
# LLM Council Setup Script (Bash)
# ============================================================================
# This script helps set up the LLM Council on Linux/Mac
# Run with: ./setup.sh
# ============================================================================

set -e

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
CYAN='\033[0;36m'
NC='\033[0m' # No Color

echo -e "${CYAN}========================================"
echo -e "  LLM Council - Setup Script"
echo -e "========================================${NC}"
echo ""

# Check if Docker is installed
echo -e "${YELLOW}[1/6] Checking Docker installation...${NC}"
if command -v docker &> /dev/null; then
    docker_version=$(docker --version)
    echo -e "${GREEN}✓ Docker found: $docker_version${NC}"
else
    echo -e "${RED}✗ Docker not found!${NC}"
    echo -e "${RED}Please install Docker from: https://docs.docker.com/get-docker/${NC}"
    exit 1
fi

# Check if Docker Compose is available
echo -e "${YELLOW}[2/6] Checking Docker Compose...${NC}"
if docker compose version &> /dev/null; then
    compose_version=$(docker compose version)
    echo -e "${GREEN}✓ Docker Compose found: $compose_version${NC}"
else
    echo -e "${RED}✗ Docker Compose not found!${NC}"
    exit 1
fi

# Determine setup type
echo ""
echo -e "${YELLOW}[3/6] Select deployment configuration:${NC}"
echo "  1) PC1 - Chairman + Backend + Frontend (connect to remote council)"
echo "  2) PC2 - Council only (provides models for PC1)"
echo "  3) Single PC - All services (for testing)"
echo ""
read -p "Enter choice (1-3): " choice

case $choice in
    1)
        compose_file="docker-compose.pc1.yaml"
        echo -e "${GREEN}✓ Selected: PC1 Configuration${NC}"
        
        echo ""
        read -p "Enter PC2 IP address (e.g., 192.168.1.101): " pc2_ip
        
        if [ -z "$pc2_ip" ]; then
            echo -e "${RED}✗ PC2 IP address is required!${NC}"
            exit 1
        fi
        
        # Set environment variable
        export PC2_IP=$pc2_ip
        echo -e "${GREEN}✓ Council IP set to: $pc2_ip${NC}"
        ;;
    2)
        compose_file="docker-compose.pc2.yaml"
        echo -e "${GREEN}✓ Selected: PC2 Configuration (Council only)${NC}"
        ;;
    3)
        compose_file="docker-compose.full.yaml"
        echo -e "${GREEN}✓ Selected: Single PC Configuration${NC}"
        ;;
    *)
        echo -e "${RED}✗ Invalid choice!${NC}"
        exit 1
        ;;
esac

# Create .env file if it doesn't exist
echo ""
echo -e "${YELLOW}[4/6] Checking environment configuration...${NC}"
if [ ! -f ".env" ]; then
    cp .env.example .env
    echo -e "${GREEN}✓ Created .env file from template${NC}"
    
    if [ "$choice" = "1" ] && [ ! -z "$pc2_ip" ]; then
        # Update .env with PC2 IP
        sed -i "s/COUNCIL_IP=localhost/COUNCIL_IP=$pc2_ip/" .env
        echo -e "${GREEN}✓ Updated .env with PC2 IP${NC}"
    fi
else
    echo -e "${GREEN}✓ .env file already exists${NC}"
fi

# Start services
echo ""
echo -e "${YELLOW}[5/6] Starting Docker services...${NC}"
echo -e "This may take a few minutes on first run..."
docker compose -f $compose_file up -d

echo -e "${GREEN}✓ Services started successfully${NC}"

# Pull models
echo ""
echo -e "${YELLOW}[6/6] Pulling LLM models...${NC}"
echo -e "This will take several minutes depending on your internet speed..."

if [ "$choice" = "2" ]; then
    # PC2 - Pull council models
    echo "Pulling council models..."
    docker exec llm-council-ollama-council ollama pull llama3.2:1b
    docker exec llm-council-ollama-council ollama pull gemma2:2b
    docker exec llm-council-ollama-council ollama pull phi3:3.8b
elif [ "$choice" = "1" ]; then
    # PC1 - Pull chairman model only
    echo "Pulling chairman model..."
    docker exec llm-council-ollama-chairman ollama pull qwen2.5:1.5b
else
    # Single PC - Pull all models
    echo "Pulling chairman model..."
    docker exec llm-council-ollama-chairman ollama pull qwen2.5:1.5b
    
    echo "Pulling council models..."
    docker exec llm-council-ollama-council ollama pull llama3.2:1b
    docker exec llm-council-ollama-council ollama pull gemma2:2b
    docker exec llm-council-ollama-council ollama pull phi3:3.8b
fi

echo -e "${GREEN}✓ Models downloaded successfully${NC}"

# Summary
echo ""
echo -e "${CYAN}========================================"
echo -e "  Setup Complete! 🎉"
echo -e "========================================${NC}"
echo ""

if [ "$choice" = "1" ] || [ "$choice" = "3" ]; then
    echo -e "${GREEN}✓ Frontend: http://localhost:5173${NC}"
    echo -e "${GREEN}✓ Backend API: http://localhost:8000${NC}"
    echo ""
    echo "Open your browser and navigate to http://localhost:5173"
fi

if [ "$choice" = "2" ]; then
    echo -e "${GREEN}✓ Ollama Council running on port 11434${NC}"
    echo ""
    echo "This PC is now ready to serve council models."
    echo "Configure PC1 to connect to this PC's IP address."
fi

echo ""
echo -e "${YELLOW}Useful commands:${NC}"
echo "  docker compose -f $compose_file logs -f     # View logs"
echo "  docker compose -f $compose_file down         # Stop services"
echo "  docker compose -f $compose_file restart      # Restart services"
echo ""
echo "For more information, see DEPLOYMENT.md"
