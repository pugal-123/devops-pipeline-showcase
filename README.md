# 🚀 End-to-End DevOps Pipeline — Showcase Project

<div align="center">

![CI/CD Pipeline](https://github.com/pugal-123/devops-pipeline-showcase/actions/workflows/ci-cd.yml/badge.svg)
![Docker Pulls](https://img.shields.io/docker/pulls/pugal-123/devops-showcase?style=flat-square&logo=docker)
![Python](https://img.shields.io/badge/Python-3.11-3776AB?style=flat-square&logo=python)
![Kubernetes](https://img.shields.io/badge/Kubernetes-Ready-326CE5?style=flat-square&logo=kubernetes)
![License](https://img.shields.io/badge/License-MIT-green?style=flat-square)

**A production-grade DevOps pipeline — from code commit to live Kubernetes deployment — with full observability.**

[📖 How It Works](#-how-it-works) • [⚡ Quick Start](#-quick-start) • [🏗️ Architecture](#️-architecture) • [📊 Monitoring](#-monitoring--observability)

</div>

---

## 🎯 What This Project Demonstrates

This is not a tutorial clone. This is a **real-world DevOps workflow** built from scratch, covering every stage a production system needs:

| Stage | Tool | What It Does |
|-------|------|-------------|
| 📦 **Source Control** | GitHub | Triggers pipeline on every push |
| 🧪 **Testing** | Pytest + Coverage | Runs unit tests with coverage reporting |
| 🔍 **Code Quality** | Flake8 | Linting and style enforcement |
| 🔒 **Security Scan** | Trivy | Scans for CVEs in code and Docker image |
| 🐳 **Containerization** | Docker (multi-stage) | Lean, secure production image |
| 📤 **Registry** | DockerHub | Versioned image storage |
| ☸️ **Deployment** | Kubernetes | Rolling updates, zero downtime |
| 📈 **Monitoring** | Prometheus + Grafana | Live metrics, dashboards, alerting |

---

## 🏗️ Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                        DEVELOPER                                │
│                     git push → main                             │
└───────────────────────────┬─────────────────────────────────────┘
                            │
                            ▼
┌─────────────────────────────────────────────────────────────────┐
│                   GITHUB ACTIONS (CI/CD)                        │
│                                                                 │
│  ┌──────────┐  ┌──────────┐  ┌──────────┐  ┌──────────────┐   │
│  │  Test &  │─►│ Security │─►│  Docker  │─►│  Deploy to   │   │
│  │  Lint    │  │  Scan    │  │ Build &  │  │  Kubernetes  │   │
│  │ (Pytest) │  │ (Trivy)  │  │   Push   │  │   (kubectl)  │   │
│  └──────────┘  └──────────┘  └──────────┘  └──────────────┘   │
└─────────────────────────────────────────────────────────────────┘
                                                      │
                                                      ▼
┌─────────────────────────────────────────────────────────────────┐
│                    KUBERNETES CLUSTER                           │
│                                                                 │
│   ┌─────────────────────────────────────────────────────────┐  │
│   │              devops-showcase namespace                  │  │
│   │                                                         │  │
│   │  ┌─────────┐  ┌─────────┐     ┌───────────────────┐   │  │
│   │  │  Pod 1  │  │  Pod 2  │────►│  Prometheus       │   │  │
│   │  │  Flask  │  │  Flask  │     │  (scrapes /metrics)│  │  │
│   │  └─────────┘  └─────────┘     └────────┬──────────┘   │  │
│   │        │ HPA (auto-scales 2–5)          │              │  │
│   │        └──────────────────────          │              │  │
│   │                                  ┌──────▼──────┐       │  │
│   │                                  │   Grafana   │       │  │
│   │                                  │  Dashboards │       │  │
│   │                                  └─────────────┘       │  │
│   └─────────────────────────────────────────────────────────┘  │
└─────────────────────────────────────────────────────────────────┘
```

---

## 📁 Project Structure

```
devops-pipeline-showcase/
│
├── 📂 .github/
│   └── workflows/
│       └── ci-cd.yml           # Full 5-stage GitHub Actions pipeline
│
├── 📂 app/
│   ├── app.py                  # Flask app with Prometheus metrics
│   ├── requirements.txt
│   ├── Dockerfile              # Multi-stage, non-root, production-ready
│   └── tests/
│       └── test_app.py         # Unit tests (health, metrics, API)
│
├── 📂 k8s/
│   ├── base/
│   │   ├── deployment.yaml     # Rolling update, resource limits, probes
│   │   └── service.yaml        # ClusterIP + HorizontalPodAutoscaler
│   └── monitoring/
│       ├── prometheus.yaml     # Prometheus + alert rules ConfigMap
│       └── grafana.yaml        # Grafana deployment
│
├── 📂 monitoring/
│   └── prometheus.yml          # Local Prometheus config (for Compose)
│
├── docker-compose.yml          # Run full stack locally in 1 command
└── README.md
```

---

## ⚡ Quick Start

### 🖥️ Option 1 — Run Locally (Docker Compose)

No Kubernetes needed. Spin up the entire stack in one command:

```bash
# 1. Clone the repo
git clone https://github.com/pugal-123/devops-pipeline-showcase.git
cd devops-pipeline-showcase

# 2. Start everything
docker compose up -d

# 3. Access the services
open http://localhost:5000        # Flask App
open http://localhost:5000/metrics # Raw Prometheus metrics
open http://localhost:9090        # Prometheus UI
open http://localhost:3000        # Grafana (admin / devops123)
```

### ☸️ Option 2 — Deploy to Kubernetes

```bash
# Apply all manifests
kubectl apply -f k8s/base/
kubectl apply -f k8s/monitoring/

# Watch pods come up
kubectl get pods -n devops-showcase -w

# Access Grafana
kubectl port-forward svc/grafana 3000:3000 -n devops-showcase
```

---

## 📊 Monitoring & Observability

The app exposes custom Prometheus metrics at `/metrics`:

```
# Request counter (by method, endpoint, status code)
http_requests_total{method="GET", endpoint="/", status="200"} 42

# Request latency histogram
http_request_duration_seconds_bucket{endpoint="/api/stats", le="0.1"} 38

# Active users gauge
active_users 67

# App version info
app_info{version="1.0.0", environment="production"} 1
```

### Grafana Dashboard Panels

| Panel | Query |
|-------|-------|
| Request Rate | `rate(http_requests_total[1m])` |
| Error Rate | `rate(http_requests_total{status=~"5.."}[5m])` |
| P95 Latency | `histogram_quantile(0.95, rate(http_request_duration_seconds_bucket[5m]))` |
| Active Users | `active_users` |
| Pod CPU | `rate(container_cpu_usage_seconds_total[5m])` |

### Active Alerts

| Alert | Condition | Severity |
|-------|-----------|----------|
| HighErrorRate | Error rate > 0.1 req/s for 2m | 🔴 Critical |
| PodCrashLooping | Restarts > 3 | 🟡 Warning |
| HighMemoryUsage | Memory > 200MB for 5m | 🟡 Warning |

---

## 🔒 Security Highlights

- ✅ **Non-root container** — runs as `appuser`, not root
- ✅ **Multi-stage Docker build** — no build tools in production image
- ✅ **Trivy scanning** — catches CVEs in code AND final image
- ✅ **Resource limits** — CPU/memory capped to prevent noisy-neighbour issues
- ✅ **Read-only principles** — minimal base image (Alpine)
- ✅ **Health probes** — liveness + readiness for safe rolling updates

---

## ⚙️ GitHub Actions Pipeline Flow

```
Push to main
    │
    ├─► 🧪 Test & Lint          (pytest, flake8, coverage)
    │         │ pass
    ├─► 🔒 Security Scan        (Trivy filesystem scan)
    │         │ pass
    ├─► 🐳 Docker Build & Push  (multi-platform, cached layers)
    │         │ success
    └─► ☸️  Deploy to K8s       (kubectl rolling update)
              │
              └─► 📣 Pipeline Summary
```

---

## 🛠️ Tech Stack

<div align="center">

![Python](https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white)
![Flask](https://img.shields.io/badge/Flask-000000?style=for-the-badge&logo=flask&logoColor=white)
![Docker](https://img.shields.io/badge/Docker-2496ED?style=for-the-badge&logo=docker&logoColor=white)
![Kubernetes](https://img.shields.io/badge/Kubernetes-326CE5?style=for-the-badge&logo=kubernetes&logoColor=white)
![GitHub Actions](https://img.shields.io/badge/GitHub_Actions-2088FF?style=for-the-badge&logo=github-actions&logoColor=white)
![Prometheus](https://img.shields.io/badge/Prometheus-E6522C?style=for-the-badge&logo=prometheus&logoColor=white)
![Grafana](https://img.shields.io/badge/Grafana-F46800?style=for-the-badge&logo=grafana&logoColor=white)

</div>

---

## 👤 Author

**Pugazhenthi Muthu** — DevOps Engineer

[![LinkedIn](https://img.shields.io/badge/LinkedIn-0077B5?style=flat-square&logo=linkedin)](https://www.linkedin.com/in/pugazhenthi-muthu-5b00a01a0/)
[![GitHub](https://img.shields.io/badge/GitHub-181717?style=flat-square&logo=github)](https://github.com/pugal-123)

---

## 📜 License

MIT License — feel free to fork, use, and build on this.
# DevOps Showcase
