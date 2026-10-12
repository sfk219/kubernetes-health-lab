# Kubernetes Health Lab

A runnable **cloud-native service** with health checks and Prometheus-format metrics. Includes Docker packaging and Kubernetes manifests for deployment, readiness/liveness probes, Service and Kustomize dev overlay.

## Run locally
```bash
python -m app.server
curl http://localhost:8080/live
curl http://localhost:8080/ready
curl http://localhost:8080/metrics
```

## Build and deploy to a local Kind cluster
```bash
kind create cluster --name portfolio
docker build -t kubernetes-health-lab:local .
kind load docker-image kubernetes-health-lab:local --name portfolio
kubectl apply -k k8s/overlays/dev
kubectl port-forward svc/kubernetes-health-lab 8080:80
```

**Tech:** Python, Docker, Kubernetes, Kustomize, HTTP probes and observability. This is a learning project; a live Kubernetes deployment has not been verified.