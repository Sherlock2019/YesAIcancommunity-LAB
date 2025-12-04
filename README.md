# 🎯 YES AI CAN Community LAB

> **The place where problems meet solutions, pain points meet cures, and people help people.**

A comprehensive AI agent platform for building, deploying, and managing intelligent assistants across enterprise use cases. From credit appraisal to fraud detection, from chatbots to compliance agents—all powered by open-source LLMs and modern ML frameworks.

[![License](https://img.shields.io/badge/license-MIT-blue.svg)](LICENSE)
[![Python](https://img.shields.io/badge/python-3.10+-blue.svg)](https://www.python.org/downloads/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.115+-green.svg)](https://fastapi.tiangolo.com/)
[![Streamlit](https://img.shields.io/badge/Streamlit-1.35+-red.svg)](https://streamlit.io/)

---

## 📋 Table of Contents

- [Overview](#-overview)
- [Key Features](#-key-features)
- [Architecture](#-architecture)
- [Available Agents](#-available-agents)
- [Quick Start](#-quick-start)
- [Installation](#-installation)
- [Usage](#-usage)
- [Configuration](#-configuration)
- [Development](#-development)
- [Deployment](#-deployment)
- [Documentation](#-documentation)
- [Contributing](#-contributing)
- [License](#-license)

---

## 🌟 Overview

**YES AI CAN Community LAB** is an enterprise-grade AI agent platform that enables organizations to rapidly prototype, deploy, and scale intelligent automation solutions. Built with a focus on explainability, compliance, and real-world business value.

### What Makes This Special?

- **🚀 Rapid Prototyping**: Build production-ready AI agents in minutes, not months
- **🔓 Open Source First**: Powered by Ollama, Hugging Face, and open-source LLMs
- **🎯 Business-Focused**: Pre-built agents for credit, fraud, compliance, and more
- **🔍 Explainable AI**: Built-in SHAP explanations for regulatory compliance
- **🏗️ Modular Architecture**: Ontology-driven design for easy customization
- **📊 Production-Ready**: Complete with monitoring, logging, and deployment tools

---

## ✨ Key Features

### 🤖 AI Agent Platform
- **Multi-Agent System**: Deploy multiple specialized agents simultaneously
- **Agent Builder**: Visual interface for creating custom agents without code
- **Agent Library**: Pre-configured templates for common use cases
- **Dynamic Orchestration**: Intelligent routing and task delegation

### 🧠 Machine Learning
- **Hybrid Models**: Combine tabular ML (LightGBM, XGBoost) with LLMs
- **AutoML Integration**: Automated model selection and hyperparameter tuning
- **Model Registry**: Centralized model versioning and deployment
- **RAG Support**: Retrieval-Augmented Generation with ChromaDB

### 💬 Natural Language
- **Multi-LLM Support**: Mistral, Llama 3, Phi-3, Gemma 2, Qwen 2
- **Ollama Integration**: Local LLM inference without API costs
- **Streaming Responses**: Real-time token streaming for better UX
- **Context Management**: Efficient prompt engineering and token optimization

### 🛡️ Enterprise Features
- **Authentication & Authorization**: Role-based access control
- **Audit Logging**: Complete activity tracking for compliance
- **Data Privacy**: On-premise deployment with no data leaving your infrastructure
- **API-First Design**: RESTful APIs with OpenAPI documentation

### 📊 Analytics & Monitoring
- **CEO Dashboard**: Executive-level insights and KPIs
- **Real-Time Monitoring**: Live agent performance metrics
- **Visitor Tracking**: User behavior analytics
- **Error Logging**: Centralized error tracking and alerting

---

## 🏗️ Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                     Streamlit Web UI                        │
│  (Agent Builder | Challenge Hub | Dashboards | Chatbots)   │
└─────────────────┬───────────────────────────────────────────┘
                  │
                  │ HTTP/WebSocket
                  │
┌─────────────────▼───────────────────────────────────────────┐
│                     FastAPI Backend                         │
│  ┌──────────────┬──────────────┬──────────────────────┐    │
│  │   Agents     │   Training   │   Reports            │    │
│  │   Router     │   Router     │   Router             │    │
│  └──────────────┴──────────────┴──────────────────────┘    │
└─────────────────┬───────────────────────────────────────────┘
                  │
    ┌─────────────┼─────────────┐
    │             │             │
┌───▼────┐  ┌────▼─────┐  ┌───▼──────┐
│ Ollama │  │ ChromaDB │  │ SQLite   │
│  LLMs  │  │   RAG    │  │   DB     │
└────────┘  └──────────┘  └──────────┘
```

### Technology Stack

**Frontend:**
- Streamlit 1.35+ (Interactive UI)
- Plotly & Altair (Data Visualization)
- Custom CSS/JS (Responsive Design)

**Backend:**
- FastAPI 0.115+ (REST API)
- Uvicorn (ASGI Server)
- SQLAlchemy 2.0+ (ORM)
- Pydantic 2.9+ (Data Validation)

**Machine Learning:**
- scikit-learn 1.4+ (Classical ML)
- LightGBM, XGBoost, Random Forest
- SHAP 0.45+ (Model Explainability)
- sentence-transformers (Embeddings)

**LLM & NLP:**
- Ollama (Local LLM Inference)
- Hugging Face Transformers
- ChromaDB (Vector Database)
- BGE Embeddings & Rerankers

**DevOps:**
- Docker & Docker Compose
- Kubernetes (K8s manifests included)
- Bash automation scripts
- Git-based version control

---

## 🤖 Available Agents

### Financial Services

#### 💳 Credit Appraisal Agent
- **Purpose**: Automated credit risk assessment and loan decisioning
- **Models**: LightGBM (scoring) + Mistral 7B (narratives)
- **Features**: SHAP explanations, risk scoring, approval recommendations
- **Use Cases**: Personal loans, business credit, mortgage pre-approval

#### 🏦 Asset Appraisal Agent
- **Purpose**: Real estate and asset valuation
- **Models**: LightGBM (valuation) + Mistral 7B (reports)
- **Features**: Comparative market analysis, automated reports
- **Use Cases**: Property valuation, collateral assessment

#### 📊 Credit Scoring Agent
- **Purpose**: Fast credit score calculations and explanations
- **Models**: Phi-3 3.8B (explanations)
- **Features**: Real-time scoring, factor analysis
- **Use Cases**: Quick credit checks, pre-qualification

#### 🧩 Unified Risk Agent
- **Purpose**: Holistic risk assessment across multiple dimensions
- **Models**: LightGBM (scoring) + Mistral 7B (analysis)
- **Features**: Multi-factor risk modeling, portfolio analysis
- **Use Cases**: Enterprise risk management, compliance reporting

### Security & Compliance

#### 🛡️ Anti-Fraud & KYC Agent
- **Purpose**: Fraud detection and identity verification
- **Models**: Random Forest (detection) + Phi-3 3.8B (alerts)
- **Features**: Real-time fraud scoring, KYC workflow automation
- **Use Cases**: Transaction monitoring, customer onboarding

#### ⚖️ Legal Compliance Agent
- **Purpose**: Regulatory compliance checking and documentation
- **Models**: Mistral 7B (regulatory analysis)
- **Features**: Policy validation, compliance reporting
- **Use Cases**: GDPR compliance, financial regulations

### Operations & Support

#### 💬 Chatbot Assistant
- **Purpose**: Customer support and FAQ automation
- **Models**: Mistral 7B (conversations)
- **Features**: Context-aware responses, multi-turn dialogs
- **Use Cases**: Customer service, internal helpdesk

#### 🏢 Real Estate Evaluator
- **Purpose**: Property analysis and market insights
- **Models**: LightGBM + Mistral 7B
- **Features**: Market trend analysis, investment recommendations
- **Use Cases**: Real estate investment, property management

#### 📈 CEO Driver Dashboard
- **Purpose**: Executive KPI monitoring and insights
- **Features**: Real-time metrics, trend analysis, alerts
- **Use Cases**: Executive reporting, business intelligence

### Platform Tools

#### 🔧 Agent Builder
- **Purpose**: Visual agent creation without coding
- **Features**: Drag-and-drop interface, template library
- **Use Cases**: Rapid prototyping, custom agent development

#### 📚 Agent Library
- **Purpose**: Browse and deploy pre-built agent templates
- **Features**: Searchable catalog, one-click deployment
- **Use Cases**: Quick starts, best practices reference

#### 🎯 Challenge Hub
- **Purpose**: Community-driven problem-solution marketplace
- **Features**: Submit challenges, propose solutions, collaborate
- **Use Cases**: Crowdsourced innovation, knowledge sharing

---

## 🚀 Quick Start

### Prerequisites

- **Python 3.10+**
- **Ollama** (for local LLM inference)
- **8GB+ RAM** (16GB recommended)
- **Linux/macOS/WSL2** (Windows with WSL2)

### One-Command Start

```bash
# Clone the repository
git clone https://github.com/yourusername/YesAIcancommunity-LAB.git
cd YesAIcancommunity-LAB

# Run the startup script (installs dependencies, starts services)
./start.sh
```

This will:
1. ✅ Create a virtual environment
2. ✅ Install all dependencies
3. ✅ Start Ollama server
4. ✅ Pull default LLM model (gemma2:9b)
5. ✅ Start FastAPI backend (port 8100)
6. ✅ Start Streamlit UI (port 8504)

### Access the Platform

- **🌐 Web UI**: http://localhost:8504
- **📘 API Docs**: http://localhost:8100/docs
- **📊 Health Check**: http://localhost:8100/health

---

## 📦 Installation

### Option 1: Local Development (Recommended)

```bash
# 1. Clone the repository
git clone https://github.com/yourusername/YesAIcancommunity-LAB.git
cd YesAIcancommunity-LAB

# 2. Create virtual environment
python3 -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate

# 3. Install dependencies
pip install -r services/api/requirements.txt
pip install -r services/ui/requirements.txt

# 4. Install and start Ollama
curl -fsSL https://ollama.com/install.sh | sh
ollama serve &
ollama pull gemma2:9b

# 5. Set environment variables
export PYTHONPATH=$(pwd)
export OLLAMA_HOST=http://127.0.0.1:11434
export API_PORT=8100
export UI_PORT=8504

# 6. Start services
uvicorn services.api.main:app --host 0.0.0.0 --port 8100 --reload &
streamlit run services/ui/app.py --server.port 8504 --server.address 0.0.0.0
```

### Option 2: Docker Compose

```bash
# 1. Clone the repository
git clone https://github.com/yourusername/YesAIcancommunity-LAB.git
cd YesAIcancommunity-LAB

# 2. Build and start containers
docker-compose up --build

# Access at http://localhost:8080
```

### Option 3: Kubernetes

```bash
# 1. Apply Kubernetes manifests
kubectl apply -f k8s/deployment.yaml

# 2. Check deployment status
kubectl get pods
kubectl get services

# 3. Access via LoadBalancer or NodePort
kubectl port-forward service/ai-agent-ui 8080:8080
```

---

## 🎮 Usage

### Using Pre-Built Agents

1. **Navigate to Agent Library** in the web UI
2. **Select an agent** (e.g., Credit Appraisal)
3. **Upload data** or enter information
4. **Run analysis** and view results
5. **Export reports** (PDF, JSON, CSV)

### Building Custom Agents

1. **Open Agent Builder** from the main menu
2. **Choose a template** or start from scratch
3. **Configure settings**:
   - Select LLM model
   - Define input schema
   - Set up prompts
   - Configure outputs
4. **Test your agent** with sample data
5. **Deploy** to production

### Using the API

```python
import requests

# Example: Credit Appraisal
response = requests.post(
    "http://localhost:8100/v1/agents/credit/appraise",
    json={
        "applicant_name": "John Doe",
        "annual_income": 75000,
        "credit_score": 720,
        "loan_amount": 250000,
        "employment_years": 5
    }
)

result = response.json()
print(f"Decision: {result['decision']}")
print(f"Risk Score: {result['risk_score']}")
print(f"Explanation: {result['explanation']}")
```

### Training Custom Models

```bash
# Train a credit model with your data
python services/train/train_credit.py \
  --data data/credit_applications.csv \
  --model lightgbm \
  --output agents/credit_appraisal/models/production/

# The trained model will be automatically loaded by the agent
```

---

## ⚙️ Configuration

### Environment Variables

Create a `.env` file in the project root:

```bash
# API Configuration
API_PORT=8100
API_HOST=0.0.0.0

# UI Configuration
UI_PORT=8504
STREAMLIT_SERVER_PORT=8504
STREAMLIT_SERVER_ADDRESS=0.0.0.0

# Ollama Configuration
OLLAMA_HOST=http://127.0.0.1:11434
OLLAMA_MODEL=gemma2:9b
SANDBOX_CHATBOT_MODEL=gemma2:9b

# Database
DATABASE_URL=sqlite:///./data/app.db

# CORS
CORS_ALLOW_ORIGINS=http://localhost:8504,http://localhost:3000

# Logging
LOG_LEVEL=INFO
LOG_DIR=.logs

# Feature Flags
ENABLE_TRAINING=true
ENABLE_EXPORTS=true
ENABLE_VISITOR_TRACKING=true
```

### Model Configuration

Edit `config/agent_model_presets.yaml` to customize model recommendations:

```yaml
tabular_models:
  credit_appraisal:
    primary: "LightGBM"
    fallback: "RandomForest"
    alternatives: ["XGBoost", "LogisticRegression"]
    reason: "Best for credit risk with imbalanced data"

llm_models:
  credit_appraisal:
    primary: "mistral:7b-instruct"
    fallback: "phi3:3.8b"
    alternatives: ["gemma2:9b", "llama3:8b-instruct"]
    reason: "Balanced performance for credit explanations"
```

### Agent Configuration

Each agent has its own configuration in `agents/{agent_name}/config.json`:

```json
{
  "name": "Credit Appraisal Agent",
  "version": "1.0.0",
  "description": "Automated credit risk assessment",
  "models": {
    "tabular": "lightgbm",
    "llm": "mistral:7b-instruct"
  },
  "features": {
    "shap_explanations": true,
    "pdf_reports": true,
    "api_enabled": true
  },
  "thresholds": {
    "high_risk": 0.7,
    "medium_risk": 0.4,
    "low_risk": 0.2
  }
}
```

---

## 🛠️ Development

### Project Structure

```
YesAIcancommunity-LAB/
├── services/
│   ├── api/                    # FastAPI backend
│   │   ├── main.py            # API entry point
│   │   ├── routers/           # API endpoints
│   │   ├── models/            # Database models
│   │   └── requirements.txt
│   └── ui/                    # Streamlit frontend
│       ├── app.py             # UI entry point
│       ├── pages/             # Agent pages
│       ├── utils/             # Shared utilities
│       └── requirements.txt
├── agents/                    # Agent definitions
│   ├── credit_appraisal/
│   ├── asset_appraisal/
│   └── anti_fraud_kyc/
├── ontology/                  # Ontology engine
│   ├── engine.py
│   ├── objects.py
│   └── registry.py
├── scripts/                   # Automation scripts
│   ├── backup.sh
│   ├── deploy.sh
│   └── train_from_merged.sh
├── k8s/                       # Kubernetes manifests
├── docker-compose.yml
├── Dockerfile
├── start.sh                   # Main startup script
└── README.md
```

### Running Tests

```bash
# Run all tests
pytest

# Run specific test suite
pytest tests/test_agents.py

# Run with coverage
pytest --cov=services --cov-report=html
```

### Code Quality

```bash
# Format code
black services/ ontology/

# Lint code
flake8 services/ ontology/

# Type checking
mypy services/ ontology/
```

### Adding a New Agent

1. **Create agent directory**:
   ```bash
   mkdir -p agents/my_agent/{models,config,data}
   ```

2. **Create agent page**:
   ```bash
   cp services/ui/pages/agent_template.py services/ui/pages/my_agent.py
   ```

3. **Configure agent**:
   ```bash
   cp agents/credit_appraisal/config.json agents/my_agent/config.json
   # Edit config.json with your settings
   ```

4. **Add to navigation**:
   Edit `services/ui/app.py` to add your agent to the menu.

5. **Test your agent**:
   ```bash
   streamlit run services/ui/pages/my_agent.py
   ```

---

## 🚢 Deployment

### Production Checklist

- [ ] Set strong passwords and API keys
- [ ] Configure HTTPS/TLS certificates
- [ ] Set up database backups
- [ ] Configure monitoring and alerting
- [ ] Review and adjust resource limits
- [ ] Enable audit logging
- [ ] Test disaster recovery procedures
- [ ] Document runbooks

### Docker Deployment

```bash
# Build production image
docker build -t yesaican-lab:latest .

# Run with production settings
docker run -d \
  --name yesaican-lab \
  -p 8080:8080 \
  -e STREAMLIT_SERVER_PORT=8080 \
  -e OLLAMA_URL=http://ollama:11434 \
  -v $(pwd)/data:/app/data \
  -v $(pwd)/agents:/app/agents \
  yesaican-lab:latest
```

### Kubernetes Deployment

```bash
# Create namespace
kubectl create namespace yesaican

# Apply configurations
kubectl apply -f k8s/deployment.yaml -n yesaican

# Scale deployment
kubectl scale deployment ai-agent-ui --replicas=3 -n yesaican

# Check status
kubectl get all -n yesaican
```

### Cloud Deployment

#### AWS ECS
```bash
# Build and push to ECR
aws ecr get-login-password --region us-east-1 | docker login --username AWS --password-stdin <account>.dkr.ecr.us-east-1.amazonaws.com
docker tag yesaican-lab:latest <account>.dkr.ecr.us-east-1.amazonaws.com/yesaican-lab:latest
docker push <account>.dkr.ecr.us-east-1.amazonaws.com/yesaican-lab:latest

# Deploy to ECS (use AWS Console or CLI)
```

#### Google Cloud Run
```bash
# Build and push to GCR
gcloud builds submit --tag gcr.io/<project-id>/yesaican-lab

# Deploy to Cloud Run
gcloud run deploy yesaican-lab \
  --image gcr.io/<project-id>/yesaican-lab \
  --platform managed \
  --region us-central1 \
  --allow-unauthenticated
```

---

## 📚 Documentation

### Available Guides

- **[Agent Setup Guide](COPIED_AGENT_SETUP_GUIDE.md)** - Detailed agent configuration
- **[Model Presets](AGENT_MODEL_PRESETS.md)** - Recommended models per agent
- **[Chatbot Behavior](CHATBOT_BEHAVIOR_RECOMMENDATIONS.md)** - Chatbot best practices
- **[Log Monitoring](LOG_MONITORING_GUIDE.md)** - Monitoring and debugging
- **[Visitor Tracking](VISITOR_TRACKING_README.md)** - Analytics setup
- **[RAG Configuration](RAG_CONFIGURATION_ANALYSIS.md)** - RAG system setup
- **[Optimization Summary](OPTIMIZATION_SUMMARY.md)** - Performance tuning

### API Documentation

Full API documentation is available at `/docs` when the API server is running:
- **Swagger UI**: http://localhost:8100/docs
- **ReDoc**: http://localhost:8100/redoc
- **OpenAPI JSON**: http://localhost:8100/openapi.json

### Architecture Diagrams

See the `/docs` directory for detailed architecture diagrams and flow charts.

---

## 🤝 Contributing

We welcome contributions from the community! Here's how you can help:

### Ways to Contribute

1. **🐛 Report Bugs**: Open an issue with reproduction steps
2. **💡 Suggest Features**: Share your ideas in discussions
3. **📝 Improve Docs**: Fix typos, add examples, clarify instructions
4. **🔧 Submit Code**: Fix bugs, add features, improve performance
5. **🎨 Design**: Improve UI/UX, create assets
6. **📊 Share Datasets**: Contribute training data (anonymized)

### Development Workflow

1. **Fork the repository**
2. **Create a feature branch**: `git checkout -b feature/amazing-feature`
3. **Make your changes**: Follow code style guidelines
4. **Test thoroughly**: Add tests for new features
5. **Commit your changes**: `git commit -m 'Add amazing feature'`
6. **Push to branch**: `git push origin feature/amazing-feature`
7. **Open a Pull Request**: Describe your changes clearly

### Code Style

- **Python**: Follow PEP 8, use Black formatter
- **Type Hints**: Use type annotations for all functions
- **Docstrings**: Use Google-style docstrings
- **Comments**: Explain "why", not "what"
- **Tests**: Maintain >80% code coverage

---

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

## 🙏 Acknowledgments

### Technologies

- **[Ollama](https://ollama.com/)** - Local LLM inference
- **[Hugging Face](https://huggingface.co/)** - Model hub and transformers
- **[FastAPI](https://fastapi.tiangolo.com/)** - Modern web framework
- **[Streamlit](https://streamlit.io/)** - Interactive web apps
- **[LightGBM](https://lightgbm.readthedocs.io/)** - Gradient boosting framework
- **[SHAP](https://shap.readthedocs.io/)** - Model explainability

### Community

Special thanks to all contributors who have helped shape this project!

---

## 📞 Support

### Getting Help

- **📖 Documentation**: Check the guides in this repo
- **💬 Discussions**: Join our community discussions
- **🐛 Issues**: Report bugs on GitHub Issues
- **📧 Email**: support@yesaican.community

### Community

- **Discord**: [Join our server](https://discord.gg/yesaican)
- **Twitter**: [@YesAICan](https://twitter.com/yesaican)
- **LinkedIn**: [YES AI CAN Community](https://linkedin.com/company/yesaican)

---

## 🗺️ Roadmap

### Q1 2025
- [ ] Multi-language support (Vietnamese, Spanish, French)
- [ ] Advanced RAG with graph databases
- [ ] Fine-tuning pipeline for custom models
- [ ] Mobile app (iOS/Android)

### Q2 2025
- [ ] Enterprise SSO integration
- [ ] Advanced analytics dashboard
- [ ] A/B testing framework
- [ ] Model marketplace

### Q3 2025
- [ ] Federated learning support
- [ ] Edge deployment (Raspberry Pi, mobile)
- [ ] Voice interface integration
- [ ] Real-time collaboration features

### Q4 2025
- [ ] Multi-tenant SaaS platform
- [ ] Advanced security features
- [ ] Compliance certifications (SOC 2, ISO 27001)
- [ ] Global CDN deployment

---

## 📊 Project Stats

![GitHub stars](https://img.shields.io/github/stars/yourusername/YesAIcancommunity-LAB?style=social)
![GitHub forks](https://img.shields.io/github/forks/yourusername/YesAIcancommunity-LAB?style=social)
![GitHub issues](https://img.shields.io/github/issues/yourusername/YesAIcancommunity-LAB)
![GitHub pull requests](https://img.shields.io/github/issues-pr/yourusername/YesAIcancommunity-LAB)

---

<div align="center">

**Made with ❤️ by the YES AI CAN Community**

[Website](https://yesaican.community) • [Documentation](https://docs.yesaican.community) • [Blog](https://blog.yesaican.community)

</div>
