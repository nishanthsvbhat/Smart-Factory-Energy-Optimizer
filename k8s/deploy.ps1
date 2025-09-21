# Smart Factory Energy Optimizer - PowerShell Deployment Script
# This script automates the deployment of the application to Kubernetes on Windows

param(
    [Parameter(Position=0)]
    [ValidateSet("build", "deploy", "status", "cleanup")]
    [string]$Action = "deploy",
    
    [Parameter()]
    [string]$Version = "latest"
)

# Configuration
$Namespace = "smart-factory"
$DockerRegistry = "smart-factory"

# Function to write colored output
function Write-Status {
    param([string]$Message)
    Write-Host "[INFO] $Message" -ForegroundColor Blue
}

function Write-Success {
    param([string]$Message)
    Write-Host "[SUCCESS] $Message" -ForegroundColor Green
}

function Write-Warning {
    param([string]$Message)
    Write-Host "[WARNING] $Message" -ForegroundColor Yellow
}

function Write-Error {
    param([string]$Message)
    Write-Host "[ERROR] $Message" -ForegroundColor Red
}

# Function to check if command exists
function Test-Command {
    param([string]$Command)
    $null = Get-Command $Command -ErrorAction SilentlyContinue
    return $?
}

# Check prerequisites
function Test-Prerequisites {
    Write-Status "Checking prerequisites..."
    
    if (-not (Test-Command "kubectl")) {
        Write-Error "kubectl is not installed. Please install kubectl first."
        exit 1
    }
    
    if (-not (Test-Command "docker")) {
        Write-Error "Docker is not installed. Please install Docker first."
        exit 1
    }
    
    # Check if kubectl can connect to cluster
    try {
        kubectl cluster-info | Out-Null
        if ($LASTEXITCODE -ne 0) {
            throw "Cannot connect to cluster"
        }
    }
    catch {
        Write-Error "Cannot connect to Kubernetes cluster. Please check your kubeconfig."
        exit 1
    }
    
    Write-Success "Prerequisites check passed"
}

# Build Docker images
function Build-Images {
    Write-Status "Building Docker images..."
    
    # Build backend image
    Write-Status "Building backend image..."
    docker build -f docker/Dockerfile.backend -t "$DockerRegistry/backend:$Version" .
    if ($LASTEXITCODE -ne 0) {
        Write-Error "Failed to build backend image"
        exit 1
    }
    
    # Build frontend image
    Write-Status "Building frontend image..."
    docker build -f docker/Dockerfile.frontend -t "$DockerRegistry/frontend:$Version" .
    if ($LASTEXITCODE -ne 0) {
        Write-Error "Failed to build frontend image"
        exit 1
    }
    
    Write-Success "Docker images built successfully"
}

# Deploy to Kubernetes
function Deploy-ToKubernetes {
    Write-Status "Deploying to Kubernetes..."
    
    # Create namespace
    Write-Status "Creating namespace..."
    kubectl apply -f k8s/namespace.yaml
    
    # Apply ConfigMaps
    Write-Status "Applying ConfigMaps..."
    kubectl apply -f k8s/configmaps.yaml
    
    # Apply Persistent Volumes
    Write-Status "Applying Persistent Volumes..."
    kubectl apply -f k8s/persistent-volumes.yaml
    
    # Deploy backend
    Write-Status "Deploying backend..."
    kubectl apply -f k8s/backend-deployment.yaml
    
    # Deploy frontend
    Write-Status "Deploying frontend..."
    kubectl apply -f k8s/frontend-deployment.yaml
    
    # Apply HPA
    Write-Status "Applying Horizontal Pod Autoscalers..."
    kubectl apply -f k8s/hpa.yaml
    
    # Apply Ingress
    Write-Status "Applying Ingress..."
    kubectl apply -f k8s/ingress.yaml
    
    Write-Success "Kubernetes deployment completed"
}

# Wait for deployments to be ready
function Wait-ForDeployments {
    Write-Status "Waiting for deployments to be ready..."
    
    kubectl wait --for=condition=available --timeout=300s deployment/backend-deployment -n $Namespace
    kubectl wait --for=condition=available --timeout=300s deployment/frontend-deployment -n $Namespace
    
    Write-Success "All deployments are ready"
}

# Show deployment status
function Show-Status {
    Write-Status "Deployment Status:"
    Write-Host ""
    
    Write-Status "Pods:"
    kubectl get pods -n $Namespace
    Write-Host ""
    
    Write-Status "Services:"
    kubectl get services -n $Namespace
    Write-Host ""
    
    Write-Status "Ingress:"
    kubectl get ingress -n $Namespace
    Write-Host ""
    
    Write-Status "HPA:"
    kubectl get hpa -n $Namespace
    Write-Host ""
}

# Get access information
function Get-AccessInfo {
    Write-Status "Access Information:"
    Write-Host ""
    
    # Get ingress IP
    $IngressIP = kubectl get ingress smart-factory-ingress -n $Namespace -o jsonpath='{.status.loadBalancer.ingress[0].ip}' 2>$null
    
    if (-not $IngressIP) {
        $IngressIP = kubectl get ingress smart-factory-ingress -n $Namespace -o jsonpath='{.status.loadBalancer.ingress[0].hostname}' 2>$null
    }
    
    if (-not $IngressIP) {
        Write-Warning "Ingress IP is still pending. You can check later with:"
        Write-Host "kubectl get ingress smart-factory-ingress -n $Namespace"
        Write-Host ""
        Write-Status "For local testing, you can use port forwarding:"
        Write-Host "kubectl port-forward service/frontend-service 8080:80 -n $Namespace"
        Write-Host "kubectl port-forward service/backend-service 8000:8000 -n $Namespace"
    }
    else {
        Write-Success "Application is accessible at:"
        Write-Host "Frontend: http://$IngressIP"
        Write-Host "API: http://$IngressIP/api"
    }
    
    Write-Host ""
    Write-Status "Add this to your C:\Windows\System32\drivers\etc\hosts file for local testing:"
    if ($IngressIP) {
        Write-Host "$IngressIP smart-factory.local"
    }
    else {
        Write-Host "127.0.0.1 smart-factory.local"
    }
}

# Cleanup function
function Remove-Deployment {
    Write-Status "Cleaning up resources..."
    kubectl delete namespace $Namespace --ignore-not-found=true
    Write-Success "Cleanup completed"
}

# Main function
function Main {
    Write-Host "Smart Factory Energy Optimizer - Kubernetes Deployment" -ForegroundColor Cyan
    Write-Host "======================================================" -ForegroundColor Cyan
    Write-Host ""
    
    switch ($Action) {
        "build" {
            Test-Prerequisites
            Build-Images
        }
        "deploy" {
            Test-Prerequisites
            Build-Images
            Deploy-ToKubernetes
            Wait-ForDeployments
            Show-Status
            Get-AccessInfo
        }
        "status" {
            Show-Status
            Get-AccessInfo
        }
        "cleanup" {
            Remove-Deployment
        }
        default {
            Write-Host "Usage: .\deploy.ps1 [build|deploy|status|cleanup] [-Version <version>]"
            Write-Host ""
            Write-Host "Commands:"
            Write-Host "  build   - Build Docker images only"
            Write-Host "  deploy  - Build images and deploy to Kubernetes (default)"
            Write-Host "  status  - Show current deployment status"
            Write-Host "  cleanup - Remove all resources from Kubernetes"
            Write-Host ""
            Write-Host "Parameters:"
            Write-Host "  -Version - Docker image version tag (default: latest)"
            exit 1
        }
    }
}

# Run main function
Main