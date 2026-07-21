<div align="center">

# 🧠 PyAssistant Analytics

### Dashboard personal de productividad con IA · Personal AI-powered productivity dashboard

[![Python](https://img.shields.io/badge/Python-3.11+-blue.svg)](https://www.python.org/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.110+-009688.svg)](https://fastapi.tiangolo.com/)
[![License](https://img.shields.io/badge/license-MIT-green.svg)](LICENSE)
[![Status](https://img.shields.io/badge/status-active-success.svg)]()
[![Code style](https://img.shields.io/badge/code%20style-PEP8-blue.svg)](https://peps.python.org/pep-0008/)

[🌐 Demo en vivo](#-demo-en-vivo--live-demo) ·
[📖 Documentación API](#-documentación-api--api-docs) ·
[🚀 Instalación rápida](#-instalación-rápida--quick-start) ·
[💬 Contribuir](#-contribuir--contributing)

</div>

---

## 📑 Tabla de Contenidos / Table of Contents

- [🇪🇸 Español](#-español)
  - [Descripción](#-descripción)
  - [Características](#-características)
  - [Stack Técnico](#-stack-técnico)
  - [Demo en Vivo](#-demo-en-vivo)
  - [Instalación Rápida](#-instalación-rápida)
  - [Uso](#-uso)
  - [Deploy](#-deploy)
  - [Roadmap](#-roadmap)
  - [Licencia](#-licencia)
  - [Autor](#-autor)
- [🇬🇧 English](#-english)
  - [Description](#-description)
  - [Features](#-features)
  - [Tech Stack](#-tech-stack)
  - [Live Demo](#-live-demo)
  - [Quick Start](#-quick-start)
  - [Usage](#-usage)
  - [Deployment](#-deployment)
  - [Roadmap](#-roadmap-1)
  - [License](#-license-1)
  - [Author](#-author)
- [🤝 Contribuir / Contributing](#-contribuir--contributing)

---

# 🇪🇸 Español

## 📋 Descripción

**PyAssistant Analytics** es un dashboard personal de productividad potenciado con Inteligencia Artificial que te permite rastrear, visualizar y analizar cómo inviertes tu tiempo. Combina un backend moderno en Python (FastAPI) con un frontend elegante y un asistente de IA conversacional (Google Gemini) que te ayuda a identificar patrones y mejorar tu productividad.

### ¿Para quién es esto?

- 👨‍💻 **Desarrolladores** que quieren rastrear su tiempo de coding, learning y reuniones
- 📊 **Profesionales de datos** que necesitan analizar su productividad con visualizaciones
- 🤖 **Entusiastas de IA** que quieren ver un ejemplo real de aplicación con LLMs
- 🎓 **Estudiantes** que buscan un proyecto full-stack para su portafolio
- 💼 **Consultores y freelancers** que facturan por horas y necesitan insights

## ✨ Características

### Core
- 📝 **CRUD completo de actividades** con categorías personalizables
- 📊 **Visualizaciones interactivas** con Chart.js (barras, doughnut, líneas)
- ⏱️ **Tracking de tiempo** con auto-cálculo de duraciones
- 🏷️ **Sistema de categorías** con colores e iconos personalizables
- 📅 **Filtros por fecha y categoría** para análisis específicos

### Analytics
- 📈 **Resumen general** con KPIs clave (horas, score promedio, mejor día)
- 📉 **Tendencias diarias/semanales** con comparativas
- 🎯 **Distribución por categoría** con porcentajes y scores
- ⚡ **Cálculo automático de streaks** (rachas de días productivos)
- 🏆 **Top categorías y días más productivos**

### Inteligencia Artificial
- 🤖 **Insights personalizados** generados por Gemini AI
- 💬 **Chat conversacional** sobre tus propios datos
- 🌍 **Respuestas en español o inglés** (detecta automáticamente)
- 📝 **Recomendaciones accionables** basadas en tus patrones

### Técnico
- 🚀 **API REST documentada** automáticamente (Swagger/OpenAPI)
- 🐳 **Docker-ready** para deploy en cualquier cloud
- 🌐 **Bilingüe** (ES/EN) con switcher en el frontend
- 📱 **Responsive** (funciona en móvil, tablet, desktop)
- 🔒 **Configuración segura** con variables de entorno

## 🛠️ Stack Técnico

| Capa | Tecnología | Propósito |
|------|-----------|-----------|
| **Backend** | Python 3.11+ | Lenguaje principal |
| **API Framework** | FastAPI 0.110+ | Endpoints REST con auto-docs |
| **ORM** | SQLAlchemy 2.0+ | Mapeo objeto-relacional |
| **Validación** | Pydantic 2.6+ | Validación de datos con tipos |
| **Base de datos** | SQLite | Almacenamiento local sin config |
| **IA** | Google Gemini 2.0 Flash | Análisis de productividad |
| **Frontend** | HTML5 + CSS3 + JS | Interfaz sin frameworks |
| **Charts** | Chart.js 4.4+ | Visualizaciones interactivas |
| **Server (dev)** | Uvicorn | ASGI server con hot-reload |
| **Server (prod)** | Gunicorn | WSGI server production-grade |
| **Container** | Docker | Deploy reproducible |
| **Deploy** | Railway | Hosting gratuito para demos |

## 🌐 Demo en Vivo

🔗 **[Ver demo en vivo](https://pyassistant-analytics.up.railway.app)** *(próximamente)*

> La demo incluye datos de ejemplo. Para usar con tus propios datos, sigue la [guía de instalación](#-instalación-rápida).

## 🚀 Instalación Rápida

### Prerrequisitos
- Python 3.11 o superior
- pip 21+
- Git (opcional, para clonar)

### Opción 1: Local con Python

```bash
# 1. Clonar el repositorio
git clone https://github.com/IvanArias77/pyassistant-analytics.git
cd pyassistant-analytics

# 2. Crear entorno virtual
cd backend
python -m venv venv
# Windows:
venv\Scripts\activate
# Mac/Linux:
source venv/bin/activate

# 3. Instalar dependencias
pip install -r requirements.txt

# 4. Configurar variables de entorno
cp .env.example .env
# Editar .env y agregar tu GEMINI_API_KEY (opcional)
# Obtener gratis en: https://aistudio.google.com/app/apikey

# 5. Generar datos de ejemplo
python -m data.seed

# 6. Iniciar el servidor
uvicorn main:app --reload
```

Abrir en el navegador: [http://localhost:8000](http://localhost:8000)

### Opción 2: Con Docker

```bash
# 1. Clonar y configurar
git clone https://github.com/IvanArias77/pyassistant-analytics.git
cd pyassistant-analytics
cp backend/.env.example backend/.env
# Editar backend/.env con tu API key

# 2. Levantar el contenedor
docker-compose up --build
```

Abrir en: [http://localhost:8000](http://localhost:8000)

## 💻 Uso

### Dashboard Web

Una vez que el servidor está corriendo, puedes:

1. **Ver el resumen** de tu productividad en los últimos 30 días
2. **Explorar tendencias** haciendo click en "Tendencia Diaria"
3. **Analizar distribución** por categoría en "Por Categoría"
4. **Preguntar a la IA** sobre tus datos en "Chat con IA"
5. **Agregar actividades** nuevas con el formulario

### API REST

La API está documentada automáticamente en `/docs` (Swagger UI) o `/redoc` (ReDoc).

Ejemplos con `curl`:

```bash
# Health check
curl http://localhost:8000/api/health

# Listar actividades
curl http://localhost:8000/api/activities/

# Crear una actividad
curl -X POST http://localhost:8000/api/activities/ \
  -H "Content-Type: application/json" \
  -d '{
    "title": "Code review",
    "category_id": 1,
    "duration_minutes": 45,
    "start_time": "2026-01-15T10:00:00",
    "productivity_score": 8
  }'

# Obtener resumen
curl http://localhost:8000/api/analytics/summary?days=30

# Chat con IA
curl -X POST http://localhost:8000/api/chat/ask \
  -H "Content-Type: application/json" \
  -d '{"question": "¿Cuál fue mi mejor semana?", "days": 30}'
```

## 🚢 Deploy

### Railway (Recomendado - Gratis)

1. **Sube tu código a GitHub:**
   ```bash
   git init
   git add .
   git commit -m "Initial commit"
   git remote add origin https://github.com/TU_USUARIO/pyassistant-analytics.git
   git push -u origin main
   ```

2. **Conecta con Railway:**
   - Ve a [railway.app](https://railway.app)
   - "New Project" → "Deploy from GitHub repo"
   - Selecciona tu repositorio

3. **Configura variables de entorno:**
   - En Railway, ve a "Variables"
   - Agrega: `GEMINI_API_KEY=tu_key` y `DEBUG=False`

4. **¡Listo!** En 3-5 minutos tendrás tu URL pública.

### Docker en cualquier cloud

```bash
# Build
docker build -t pyassistant-analytics .

# Run
docker run -p 8000:8000 \
  -e GEMINI_API_KEY=tu_key \
  -e DEBUG=False \
  pyassistant-analytics
```

## 🗺️ Roadmap

### ✅ v1.0 (Actual)
- [x] CRUD de actividades
- [x] Dashboard con 4 vistas
- [x] Integración con Gemini AI
- [x] Chat conversacional
- [x] Bilingüe (ES/EN)
- [x] Docker + Railway ready

### 🚧 v1.1 (Próximamente)
- [ ] Autenticación de usuarios
- [ ] PWA para móvil
- [ ] Exportar reportes a PDF
- [ ] Integración con Google Calendar
- [ ] Goals tracking con notificaciones

### 💡 v2.0 (Futuro)
- [ ] Multi-usuario con roles
- [ ] Dashboard para equipos
- [ ] Mobile app nativa
- [ ] API pública con rate limiting
- [ ] Marketplace de dashboards

¿Ideas? [Abre un issue](https://github.com/IvanArias77/pyassistant-analytics/issues) o [contribuye](#-contribuir--contributing).

## 📄 Licencia

Este proyecto está bajo la **Licencia MIT**. Ver [LICENSE](LICENSE) para más detalles.

```
MIT License - Puedes usar, modificar y distribuir libremente.
Solo se requiere mantener el aviso de copyright original.
```

## 👤 Autor

**Iván Arias G.**
Ingeniero Mecatrónico | Data, Automation & AI

- 🔗 LinkedIn: [linkedin.com/in/ivan-arias-993587233](https://linkedin.com/in/ivan-arias-993587233)
- 💻 GitHub: [@IvanArias77](https://github.com/IvanArias77)
- 📧 Email: ivan.ariasg@hotmail.com
- 🌎 Ubicación: Cartagena, Colombia

---

# 🇬🇧 English

## 📋 Description

**PyAssistant Analytics** is a personal productivity dashboard powered by Artificial Intelligence that lets you track, visualize, and analyze how you spend your time. It combines a modern Python backend (FastAPI) with an elegant frontend and a conversational AI assistant (Google Gemini) that helps you identify patterns and improve your productivity.

### Who is this for?

- 👨‍💻 **Developers** who want to track their coding, learning, and meeting time
- 📊 **Data professionals** who need to analyze their productivity with visualizations
- 🤖 **AI enthusiasts** who want to see a real-world LLM application example
- 🎓 **Students** looking for a full-stack project for their portfolio
- 💼 **Consultants and freelancers** who bill by the hour and need insights

## ✨ Features

### Core
- 📝 **Full CRUD for activities** with customizable categories
- 📊 **Interactive visualizations** with Chart.js (bar, doughnut, line)
- ⏱️ **Time tracking** with auto-calculated durations
- 🏷️ **Category system** with customizable colors and icons
- 📅 **Filters by date and category** for specific analysis

### Analytics
- 📈 **General summary** with key KPIs (hours, avg score, best day)
- 📉 **Daily/weekly trends** with comparisons
- 🎯 **Category distribution** with percentages and scores
- ⚡ **Automatic streak calculation** (productive day streaks)
- 🏆 **Top categories and most productive days**

### Artificial Intelligence
- 🤖 **Personalized insights** generated by Gemini AI
- 💬 **Conversational chat** about your own data
- 🌍 **Spanish or English responses** (auto-detection)
- 📝 **Actionable recommendations** based on your patterns

### Technical
- 🚀 **Auto-documented REST API** (Swagger/OpenAPI)
- 🐳 **Docker-ready** for any cloud deployment
- 🌐 **Bilingual** (ES/EN) with frontend switcher
- 📱 **Responsive** (works on mobile, tablet, desktop)
- 🔒 **Secure configuration** with environment variables

## 🛠️ Tech Stack

| Layer | Technology | Purpose |
|-------|-----------|---------|
| **Backend** | Python 3.11+ | Main language |
| **API Framework** | FastAPI 0.110+ | REST endpoints with auto-docs |
| **ORM** | SQLAlchemy 2.0+ | Object-relational mapping |
| **Validation** | Pydantic 2.6+ | Data validation with types |
| **Database** | SQLite | Local storage, no config |
| **AI** | Google Gemini 2.0 Flash | Productivity analysis |
| **Frontend** | HTML5 + CSS3 + JS | Framework-free interface |
| **Charts** | Chart.js 4.4+ | Interactive visualizations |
| **Server (dev)** | Uvicorn | ASGI server with hot-reload |
| **Server (prod)** | Gunicorn | Production-grade WSGI |
| **Container** | Docker | Reproducible deploys |
| **Hosting** | Railway | Free hosting for demos |

## 🌐 Live Demo

🔗 **[View live demo](https://pyassistant-analytics.up.railway.app)** *(coming soon)*

> The demo includes sample data. To use with your own data, follow the [quick start guide](#-quick-start).

## 🚀 Quick Start

### Prerequisites
- Python 3.11 or higher
- pip 21+
- Git (optional, to clone)

### Option 1: Local with Python

```bash
# 1. Clone the repository
git clone https://github.com/IvanArias77/pyassistant-analytics.git
cd pyassistant-analytics

# 2. Create virtual environment
cd backend
python -m venv venv
# Windows:
venv\Scripts\activate
# Mac/Linux:
source venv/bin/activate

# 3. Install dependencies
pip install -r requirements.txt

# 4. Configure environment variables
cp .env.example .env
# Edit .env and add your GEMINI_API_KEY (optional)
# Get free key at: https://aistudio.google.com/app/apikey

# 5. Generate sample data
python -m data.seed

# 6. Start the server
uvicorn main:app --reload
```

Open in browser: [http://localhost:8000](http://localhost:8000)

### Option 2: With Docker

```bash
# 1. Clone and configure
git clone https://github.com/IvanArias77/pyassistant-analytics.git
cd pyassistant-analytics
cp backend/.env.example backend/.env
# Edit backend/.env with your API key

# 2. Start the container
docker-compose up --build
```

Open at: [http://localhost:8000](http://localhost:8000)

## 💻 Usage

### Web Dashboard

Once the server is running, you can:

1. **View the summary** of your productivity in the last 30 days
2. **Explore trends** by clicking "Daily Trend"
3. **Analyze distribution** by category in "By Category"
4. **Ask the AI** about your data in "AI Chat"
5. **Add new activities** with the form

### REST API

The API is auto-documented at `/docs` (Swagger UI) or `/redoc` (ReDoc).

Examples with `curl`:

```bash
# Health check
curl http://localhost:8000/api/health

# List activities
curl http://localhost:8000/api/activities/

# Create an activity
curl -X POST http://localhost:8000/api/activities/ \
  -H "Content-Type: application/json" \
  -d '{
    "title": "Code review",
    "category_id": 1,
    "duration_minutes": 45,
    "start_time": "2026-01-15T10:00:00",
    "productivity_score": 8
  }'

# Get summary
curl http://localhost:8000/api/analytics/summary?days=30

# AI chat
curl -X POST http://localhost:8000/api/chat/ask \
  -H "Content-Type: application/json" \
  -d '{"question": "What was my best week?", "days": 30}'
```

## 🚢 Deployment

### Railway (Recommended - Free)

1. **Push your code to GitHub:**
   ```bash
   git init
   git add .
   git commit -m "Initial commit"
   git remote add origin https://github.com/YOUR_USERNAME/pyassistant-analytics.git
   git push -u origin main
   ```

2. **Connect with Railway:**
   - Go to [railway.app](https://railway.app)
   - "New Project" → "Deploy from GitHub repo"
   - Select your repository

3. **Configure environment variables:**
   - In Railway, go to "Variables"
   - Add: `GEMINI_API_KEY=your_key` and `DEBUG=False`

4. **Done!** In 3-5 minutes you'll have your public URL.

### Docker on any cloud

```bash
# Build
docker build -t pyassistant-analytics .

# Run
docker run -p 8000:8000 \
  -e GEMINI_API_KEY=your_key \
  -e DEBUG=False \
  pyassistant-analytics
```

## 🗺️ Roadmap

### ✅ v1.0 (Current)
- [x] Activities CRUD
- [x] Dashboard with 4 views
- [x] Gemini AI integration
- [x] Conversational chat
- [x] Bilingual (ES/EN)
- [x] Docker + Railway ready

### 🚧 v1.1 (Coming soon)
- [ ] User authentication
- [ ] PWA for mobile
- [ ] PDF report export
- [ ] Google Calendar integration
- [ ] Goals tracking with notifications

### 💡 v2.0 (Future)
- [ ] Multi-user with roles
- [ ] Team dashboards
- [ ] Native mobile app
- [ ] Public API with rate limiting
- [ ] Dashboard marketplace

Ideas? [Open an issue](https://github.com/IvanArias77/pyassistant-analytics/issues) or [contribute](#-contribuir--contributing).

## 📄 License

This project is under the **MIT License**. See [LICENSE](LICENSE) for details.

```
MIT License - You can use, modify, and distribute freely.
Just maintain the original copyright notice.
```

## 👤 Author

**Iván Arias G.**
Mechatronics Engineer | Data, Automation & AI

- 🔗 LinkedIn: [linkedin.com/in/ivan-arias-993587233](https://linkedin.com/in/ivan-arias-993587233)
- 💻 GitHub: [@IvanArias77](https://github.com/IvanArias77)
- 📧 Email: ivan.ariasg@hotmail.com
- 🌎 Location: Cartagena, Colombia

---

# 🤝 Contribuir / Contributing

🇪🇸 **¿Quieres contribuir?** ¡Genial! Las contribuciones son bienvenidas:

1. 🍴 Fork el proyecto
2. 🌿 Crea tu feature branch (`git checkout -b feature/AmazingFeature`)
3. 💾 Commit tus cambios (`git commit -m 'Add some AmazingFeature'`)
4. 📤 Push al branch (`git push origin feature/AmazingFeature`)
5. 🔃 Abre un Pull Request

🇬🇧 **Want to contribute?** Awesome! Contributions are welcome:

1. 🍴 Fork the project
2. 🌿 Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. 💾 Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. 📤 Push to the branch (`git push origin feature/AmazingFeature`)
5. 🔃 Open a Pull Request

### 📋 Guidelines / Pautas

- ✅ Follow PEP 8 style guide
- ✅ Add tests for new features
- ✅ Update documentation as needed
- ✅ Be respectful and constructive

---

## 🙏 Agradecimientos / Acknowledgments

- [FastAPI](https://fastapi.tiangolo.com/) — Por el mejor framework web de Python
- [Google Gemini](https://ai.google.dev/) — Por democratizar el acceso a LLMs
- [Chart.js](https://www.chartjs.org/) — Por visualizaciones hermosas y simples
- [SQLAlchemy](https://www.sqlalchemy.org/) — Por hacer ORM un placer
- [Pydantic](https://docs.pydantic.dev/) — Por validación que se siente natural
- [Railway](https://railway.app/) — Por hosting gratuito para devs

---

## ⭐ ¿Te gustó el proyecto? / Like this project?

Si te fue útil, considera:
- ⭐ Darle una estrella en GitHub
- 🐦 Compartirlo en redes sociales
- 💬 Comentar tu experiencia
- 🤝 Contribuir con mejoras

🇪🇸 *Hecho con ❤️ y ☕ en Cartagena, Colombia*

🇬🇧 *Made with ❤️ and ☕ in Cartagena, Colombia*

---

<div align="center">

**[⬆ Volver arriba / Back to top](#-pyassistant-analytics)**

</div>
