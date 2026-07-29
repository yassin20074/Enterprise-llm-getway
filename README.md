# Enterprise LLM Gateway & Guardrails System

A high-performance, production-ready LLM Gateway built with FastAPI, Redis, NeMo Guardrails, Langfuse, and Prometheus.

This system serves as an enterprise middleware layer that sits between client applications and Large Language Model providers. It handles security, caching, rate limiting, observability, and infrastructure monitoring in a unified Microservices architecture.

---

## ✨ Key Features

* 🛡️ Security & Guardrails: Automated prompt injection prevention and safety alignment using NVIDIA NeMo Guardrails.
* ⚡ Caching & Performance: High-speed exact caching using Redis to eliminate redundant LLM API calls (reducing costs and response latency).
* 🚦 Rate Limiting: Built-in IP/User rate limiting (e.g., 5 requests/min) to prevent API abuse.
* 🔍 Observability & Tracing: Full request tracing, token usage, latency, and cost tracking via Langfuse.
* 📊 Metrics & Monitoring: System performance metrics exposed via Prometheus and visualized with Grafana.
* 🐳 Fully Containerized: One-command deployment using Docker & Docker Compose.

---

## 🏗️ System Architecture

`text
[ Client App ]
      │
      ▼
[ Enterprise LLM Gateway (FastAPI) ]
      ├── 1. Rate Limiter (Redis)
      ├── 2. Prompt Injection Guardrails (NeMo)
      ├── 3. Exact Response Cache (Redis)
      ├── 4. LLM Provider (Groq API / Llama 3.3)
      └── 5. Observability (Langfuse Traces)
      │
      └──► Metrics exposed at /metrics ──► [ Prometheus ] ──► [ Grafana Dashboard ]


**Create By : Yassin Sanad**
