# Kubernetes Deployment Guide

This directory contains all the Kubernetes manifests and deployment scripts for the Smart Factory Energy Optimizer application.

## Prerequisites

- Kubernetes cluster (local or cloud)
- kubectl configured to connect to your cluster
- Docker installed and running
- nginx-ingress controller installed in your cluster

## Quick Start

### For Windows (PowerShell):
```powershell
# Deploy everything
.\deploy.ps1 deploy

# Check status
.\deploy.ps1 status

# Cleanup
.\deploy.ps1 cleanup
```

### For Linux/macOS (Bash):
```bash
# Make script executable
chmod +x deploy.sh

# Deploy everything
./deploy.sh deploy

# Check status
./deploy.sh status

# Cleanup
./deploy.sh cleanup
```

## Manual Deployment

If you prefer to deploy manually:

```bash
# 1. Create namespace
kubectl apply -f namespace.yaml

# 2. Apply configuration
kubectl apply -f configmaps.yaml
kubectl apply -f persistent-volumes.yaml

# 3. Deploy applications
kubectl apply -f backend-deployment.yaml
kubectl apply -f frontend-deployment.yaml

# 4. Configure autoscaling
kubectl apply -f hpa.yaml

# 5. Setup ingress
kubectl apply -f ingress.yaml
```

## Architecture Overview

### Components

1. **Namespace**: `smart-factory` - Isolated environment for all resources
2. **Backend**: FastAPI application with ML model (2 replicas)
3. **Frontend**: React app served by nginx (2 replicas)
4. **ConfigMaps**: Configuration for both applications
5. **Services**: ClusterIP services for internal communication
6. **Ingress**: External access with nginx ingress controller
7. **HPA**: Horizontal Pod Autoscaler for automatic scaling
8. **PVC**: Persistent storage for model data and logs

### Network Architecture

```
Internet → Ingress → Frontend Service → Frontend Pods
                  ↘ Backend Service → Backend Pods
```

## Configuration Files

### namespace.yaml
Creates the `smart-factory` namespace for resource isolation.

### configmaps.yaml
- **backend-config**: Environment variables for FastAPI
- **nginx-config**: Custom nginx configuration with API routing

### backend-deployment.yaml
- Deployment with 2 replicas
- Resource limits: 512Mi memory, 500m CPU
- Health checks on `/health` endpoint
- ClusterIP service on port 8000

### frontend-deployment.yaml
- Deployment with 2 replicas
- Resource limits: 256Mi memory, 200m CPU
- nginx serving static files with API proxy
- ClusterIP service on port 80

### ingress.yaml
- Two ingress configurations: local and production
- Routes `/api/*` to backend, everything else to frontend
- CORS configuration
- Security headers
- Rate limiting

### hpa.yaml
- Backend: 2-10 replicas based on CPU (70%) and memory (80%)
- Frontend: 2-5 replicas based on CPU (60%) and memory (70%)

### persistent-volumes.yaml
- `model-data-pvc`: 1Gi for ML model storage
- `logs-pvc`: 5Gi for application logs

## Access Configuration

### Local Development

Add to your hosts file:
- **Windows**: `C:\Windows\System32\drivers\etc\hosts`
- **Linux/macOS**: `/etc/hosts`

```
127.0.0.1 smart-factory.local
```

### Production

Update `ingress.yaml` with your domain:
```yaml
- host: your-domain.com
```

## Monitoring and Scaling

### Check Pod Status
```bash
kubectl get pods -n smart-factory
```

### View Logs
```bash
# Backend logs
kubectl logs -f deployment/backend-deployment -n smart-factory

# Frontend logs
kubectl logs -f deployment/frontend-deployment -n smart-factory
```

### Scale Manually
```bash
# Scale backend
kubectl scale deployment backend-deployment --replicas=5 -n smart-factory

# Scale frontend
kubectl scale deployment frontend-deployment --replicas=3 -n smart-factory
```

### Autoscaling Status
```bash
kubectl get hpa -n smart-factory
```

## Troubleshooting

### Common Issues

1. **Pods not starting**
   ```bash
   kubectl describe pod <pod-name> -n smart-factory
   ```

2. **Service not accessible**
   ```bash
   kubectl get svc -n smart-factory
   kubectl get endpoints -n smart-factory
   ```

3. **Ingress not working**
   ```bash
   kubectl describe ingress smart-factory-ingress -n smart-factory
   ```

4. **Check ingress controller**
   ```bash
   kubectl get pods -n ingress-nginx
   ```

### Port Forwarding for Testing

If ingress is not working, use port forwarding:

```bash
# Frontend
kubectl port-forward service/frontend-service 8080:80 -n smart-factory

# Backend
kubectl port-forward service/backend-service 8000:8000 -n smart-factory
```

Then access:
- Frontend: http://localhost:8080
- Backend API: http://localhost:8000

## Security Features

- Non-root containers
- Read-only root filesystem where possible
- Security contexts with dropped capabilities
- Resource limits and requests
- Network policies (can be added)
- CORS configuration
- Security headers
- Rate limiting

## Production Considerations

1. **TLS/SSL**: Configure cert-manager for automatic certificates
2. **Monitoring**: Add Prometheus and Grafana
3. **Logging**: Configure centralized logging (ELK stack)
4. **Backup**: Setup persistent volume backups
5. **Network Policies**: Implement network segmentation
6. **Secrets**: Use Kubernetes secrets for sensitive data
7. **Image Security**: Scan images for vulnerabilities

## Cleanup

Remove all resources:
```bash
kubectl delete namespace smart-factory
```

This will remove all resources in the namespace including deployments, services, configmaps, and persistent volumes.