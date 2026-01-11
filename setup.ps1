#!/usr/bin/env pwsh
# ============================================================================
# LLM Council Setup Script (PowerShell)
# ============================================================================
# This script helps set up the LLM Council on Windows
# Run with: .\setup.ps1
# ============================================================================

$ErrorActionPreference = "Stop"

Write-Host "========================================" -ForegroundColor Cyan
Write-Host "  LLM Council - Setup Script" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

# Check if Docker is installed
Write-Host "[1/6] Checking Docker installation..." -ForegroundColor Yellow
try {
    $dockerVersion = docker --version
    Write-Host "✓ Docker found: $dockerVersion" -ForegroundColor Green
} catch {
    Write-Host "✗ Docker not found!" -ForegroundColor Red
    Write-Host "Please install Docker Desktop from: https://www.docker.com/products/docker-desktop" -ForegroundColor Red
    exit 1
}

# Check if Docker Compose is available
Write-Host "[2/6] Checking Docker Compose..." -ForegroundColor Yellow
try {
    $composeVersion = docker compose version
    Write-Host "✓ Docker Compose found: $composeVersion" -ForegroundColor Green
} catch {
    Write-Host "✗ Docker Compose not found!" -ForegroundColor Red
    exit 1
}

# Determine setup type
Write-Host ""
Write-Host "[3/6] Select deployment configuration:" -ForegroundColor Yellow
Write-Host "  1) PC1 - Chairman + Backend + Frontend (connect to remote council)"
Write-Host "  2) PC2 - Council only (provides models for PC1)"
Write-Host "  3) Single PC - All services (for testing)"
Write-Host ""
$choice = Read-Host "Enter choice (1-3)"

switch ($choice) {
    "1" {
        $composeFile = "docker-compose.pc1.yaml"
        Write-Host "✓ Selected: PC1 Configuration" -ForegroundColor Green
        
        Write-Host ""
        $pc2Ip = Read-Host "Enter PC2 IP address (e.g., 192.168.1.101)"
        
        if ($pc2Ip -eq "") {
            Write-Host "✗ PC2 IP address is required!" -ForegroundColor Red
            exit 1
        }
        
        # Set environment variable
        $env:PC2_IP = $pc2Ip
        Write-Host "✓ Council IP set to: $pc2Ip" -ForegroundColor Green
    }
    "2" {
        $composeFile = "docker-compose.pc2.yaml"
        Write-Host "✓ Selected: PC2 Configuration (Council only)" -ForegroundColor Green
    }
    "3" {
        $composeFile = "docker-compose.full.yaml"
        Write-Host "✓ Selected: Single PC Configuration" -ForegroundColor Green
    }
    default {
        Write-Host "✗ Invalid choice!" -ForegroundColor Red
        exit 1
    }
}

# Create .env file if it doesn't exist
Write-Host ""
Write-Host "[4/6] Checking environment configuration..." -ForegroundColor Yellow
if (-not (Test-Path ".env")) {
    Copy-Item ".env.example" ".env"
    Write-Host "✓ Created .env file from template" -ForegroundColor Green
    
    if ($choice -eq "1" -and $pc2Ip) {
        # Update .env with PC2 IP
        (Get-Content ".env") -replace "COUNCIL_IP=localhost", "COUNCIL_IP=$pc2Ip" | Set-Content ".env"
        Write-Host "✓ Updated .env with PC2 IP" -ForegroundColor Green
    }
} else {
    Write-Host "✓ .env file already exists" -ForegroundColor Green
}

# Start services
Write-Host ""
Write-Host "[5/6] Starting Docker services..." -ForegroundColor Yellow
Write-Host "This may take a few minutes on first run..." -ForegroundColor Gray
docker compose -f $composeFile up -d

if ($LASTEXITCODE -ne 0) {
    Write-Host "✗ Failed to start services!" -ForegroundColor Red
    exit 1
}

Write-Host "✓ Services started successfully" -ForegroundColor Green

# Pull models
Write-Host ""
Write-Host "[6/6] Pulling LLM models..." -ForegroundColor Yellow
Write-Host "This will take several minutes depending on your internet speed..." -ForegroundColor Gray

if ($choice -eq "2") {
    # PC2 - Pull council models
    Write-Host "Pulling council models..." -ForegroundColor Gray
    docker exec llm-council-ollama-council ollama pull llama3.2:1b
    docker exec llm-council-ollama-council ollama pull gemma2:2b
    docker exec llm-council-ollama-council ollama pull phi3:3.8b
} elseif ($choice -eq "1") {
    # PC1 - Pull chairman model only
    Write-Host "Pulling chairman model..." -ForegroundColor Gray
    docker exec llm-council-ollama-chairman ollama pull qwen2.5:1.5b
} else {
    # Single PC - Pull all models
    Write-Host "Pulling chairman model..." -ForegroundColor Gray
    docker exec llm-council-ollama-chairman ollama pull qwen2.5:1.5b
    
    Write-Host "Pulling council models..." -ForegroundColor Gray
    docker exec llm-council-ollama-council ollama pull llama3.2:1b
    docker exec llm-council-ollama-council ollama pull gemma2:2b
    docker exec llm-council-ollama-council ollama pull phi3:3.8b
}

Write-Host "✓ Models downloaded successfully" -ForegroundColor Green

# Summary
Write-Host ""
Write-Host "========================================" -ForegroundColor Cyan
Write-Host "  Setup Complete! 🎉" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

if ($choice -eq "1" -or $choice -eq "3") {
    Write-Host "✓ Frontend: http://localhost:5173" -ForegroundColor Green
    Write-Host "✓ Backend API: http://localhost:8000" -ForegroundColor Green
    Write-Host ""
    Write-Host "Open your browser and navigate to http://localhost:5173" -ForegroundColor White
}

if ($choice -eq "2") {
    Write-Host "✓ Ollama Council running on port 11434" -ForegroundColor Green
    Write-Host ""
    Write-Host "This PC is now ready to serve council models." -ForegroundColor White
    Write-Host "Configure PC1 to connect to this PC's IP address." -ForegroundColor White
}

Write-Host ""
Write-Host "Useful commands:" -ForegroundColor Yellow
Write-Host "  docker compose -f $composeFile logs -f     # View logs"
Write-Host "  docker compose -f $composeFile down         # Stop services"
Write-Host "  docker compose -f $composeFile restart      # Restart services"
Write-Host ""
Write-Host "For more information, see DEPLOYMENT.md" -ForegroundColor Gray
