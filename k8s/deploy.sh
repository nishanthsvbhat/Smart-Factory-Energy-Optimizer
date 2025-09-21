#!/bin/bash

# Smart Factory Energy Optimizer - Kubernetes Deployment Script
# This script automates the deployment of the application to Kubernetes

set -e

# Configuration
NAMESPACE="smart-factory"
DOCKER_REGISTRY="smart-factory"
VERSION="${1:-latest}"

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Function to print colored output
print_status() {
    echo -e "${BLUE}[INFO]${NC} $1"
}

print_success() {
    echo -e "${GREEN}[SUCCESS]${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

print_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

# Function to check if command exists
command_exists() {
    command -v "$1" >/dev/null 2>&1
}

# Check prerequisites
check_prerequisites() {
    print_status "Checking prerequisites..."
    
    if ! command_exists kubectl; then
        print_error "kubectl is not installed. Please install kubectl first."
        exit 1
    fi
    
    if ! command_exists docker; then
        print_error "Docker is not installed. Please install Docker first."
        exit 1
    fi
    
    # Check if kubectl can connect to cluster
    if ! kubectl cluster-info >/dev/null 2>&1; then
        print_error "Cannot connect to Kubernetes cluster. Please check your kubeconfig."
        exit 1
    fi
    
    print_success "Prerequisites check passed"
}

# Build Docker images
build_images() {
    print_status "Building Docker images..."
    
    # Build backend image
    print_status "Building backend image..."
    docker build -f docker/Dockerfile.backend -t ${DOCKER_REGISTRY}/backend:${VERSION} .
    
    # Build frontend image
    print_status "Building frontend image..."
    docker build -f docker/Dockerfile.frontend -t ${DOCKER_REGISTRY}/frontend:${VERSION} .
    
    print_success "Docker images built successfully"
}

# Deploy to Kubernetes
deploy_to_kubernetes() {
    print_status "Deploying to Kubernetes..."
    
    # Create namespace
    print_status "Creating namespace..."
    kubectl apply -f k8s/namespace.yaml
    
    # Apply ConfigMaps
    print_status "Applying ConfigMaps..."
    kubectl apply -f k8s/configmaps.yaml
    
    # Apply Persistent Volumes
    print_status "Applying Persistent Volumes..."
    kubectl apply -f k8s/persistent-volumes.yaml
    
    # Deploy backend
    print_status "Deploying backend..."
    kubectl apply -f k8s/backend-deployment.yaml
    
    # Deploy frontend
    print_status "Deploying frontend..."
    kubectl apply -f k8s/frontend-deployment.yaml
    
    # Apply HPA
    print_status "Applying Horizontal Pod Autoscalers..."
    kubectl apply -f k8s/hpa.yaml
    
    # Apply Ingress
    print_status "Applying Ingress..."
    kubectl apply -f k8s/ingress.yaml
    
    print_success "Kubernetes deployment completed"
}

# Wait for deployments to be ready
wait_for_deployments() {
    print_status "Waiting for deployments to be ready..."
    
    kubectl wait --for=condition=available --timeout=300s deployment/backend-deployment -n ${NAMESPACE}
    kubectl wait --for=condition=available --timeout=300s deployment/frontend-deployment -n ${NAMESPACE}
    
    print_success "All deployments are ready"
}

# Show deployment status
show_status() {
    print_status "Deployment Status:"
    echo ""
    
    print_status "Pods:"
    kubectl get pods -n ${NAMESPACE}
    echo ""
    
    print_status "Services:"
    kubectl get services -n ${NAMESPACE}
    echo ""
    
    print_status "Ingress:"
    kubectl get ingress -n ${NAMESPACE}
    echo ""
    
    print_status "HPA:"
    kubectl get hpa -n ${NAMESPACE}
    echo ""
}

# Get access information
get_access_info() {
    print_status "Access Information:"
    echo ""
    
    # Get ingress IP
    INGRESS_IP=$(kubectl get ingress smart-factory-ingress -n ${NAMESPACE} -o jsonpath='{.status.loadBalancer.ingress[0].ip}' 2>/dev/null || echo "pending")
    
    if [ "$INGRESS_IP" = "pending" ] || [ -z "$INGRESS_IP" ]; then
        INGRESS_IP=$(kubectl get ingress smart-factory-ingress -n ${NAMESPACE} -o jsonpath='{.status.loadBalancer.ingress[0].hostname}' 2>/dev/null || echo "pending")
    fi
    
    if [ "$INGRESS_IP" = "pending" ] || [ -z "$INGRESS_IP" ]; then
        print_warning "Ingress IP is still pending. You can check later with:"
        echo "kubectl get ingress smart-factory-ingress -n ${NAMESPACE}"
        echo ""
        print_status "For local testing, you can use port forwarding:"
        echo "kubectl port-forward service/frontend-service 8080:80 -n ${NAMESPACE}"
        echo "kubectl port-forward service/backend-service 8000:8000 -n ${NAMESPACE}"
    else
        print_success "Application is accessible at:"
        echo "Frontend: http://${INGRESS_IP}"
        echo "API: http://${INGRESS_IP}/api"
    fi
    
    echo ""
    print_status "Add this to your /etc/hosts file for local testing:"
    echo "${INGRESS_IP:-127.0.0.1} smart-factory.local"
}

# Cleanup function
cleanup() {
    print_status "Cleaning up resources..."
    kubectl delete namespace ${NAMESPACE} --ignore-not-found=true
    print_success "Cleanup completed"
}

# Main deployment function
main() {
    echo "Smart Factory Energy Optimizer - Kubernetes Deployment"
    echo "======================================================"
    echo ""
    
    case "${1:-deploy}" in
        "build")
            check_prerequisites
            build_images
            ;;
        "deploy")
            check_prerequisites
            build_images
            deploy_to_kubernetes
            wait_for_deployments
            show_status
            get_access_info
            ;;
        "status")
            show_status
            get_access_info
            ;;
        "cleanup")
            cleanup
            ;;
        *)
            echo "Usage: $0 [build|deploy|status|cleanup]"
            echo ""
            echo "Commands:"
            echo "  build   - Build Docker images only"
            echo "  deploy  - Build images and deploy to Kubernetes (default)"
            echo "  status  - Show current deployment status"
            echo "  cleanup - Remove all resources from Kubernetes"
            exit 1
            ;;
    esac
}

# Run main function with all arguments
main "$@"