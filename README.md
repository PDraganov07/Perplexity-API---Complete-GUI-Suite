# ⚡ Perplexity API - Complete GUI Suite

<div align="center">

![Version](https://img.shields.io/badge/version-2.0.0-blue.svg)
![Python](https://img.shields.io/badge/python-3.8+-green.svg)
![License](https://img.shields.io/badge/license-MIT-orange.svg)
![Platform](https://img.shields.io/badge/platform-Windows%20%7C%20macOS%20%7C%20Linux-lightgrey.svg)

*A beautiful, feature-rich desktop application and localhost API server for Perplexity AI*

[Features](#-features) • [Installation](#-installation) • [Usage](#-usage) • [API Documentation](#-api-documentation) • [Screenshots](#-screenshots)

</div>

---

## 📋 Table of Contents

- [Features](#-features)
- [Requirements](#-requirements)
- [Installation](#-installation)
- [Quick Start](#-quick-start)
- [Usage](#-usage)
  - [GUI Mode](#gui-mode)
  - [API Server](#api-server)
- [API Documentation](#-api-documentation)
- [Configuration](#-configuration)
- [Screenshots](#-screenshots)
- [Contributing](#-contributing)
- [License](#-license)
- [Credits](#-credits)

---

## ✨ Features

### 🎨 Modern GUI
- **Perplexity-inspired design** - Clean, modern interface matching the official Perplexity website
- **Dark mode optimized** - Carefully crafted color palette for comfortable viewing
- **Real-time chat interface** - Smooth, responsive chat bubbles
- **Keyboard shortcuts** - Press `Enter` to send, `Shift+Enter` for new line

### 🤖 Full API Support
- **All Perplexity models**:
  - `sonar` - Fast responses
  - `sonar-pro` - Enhanced reasoning
  - `sonar-deep-research` - In-depth analysis
  - `sonar-reasoning-pro` - Advanced logic
- **Complete parameter control**:
  - Temperature, Top-P, Top-K
  - Presence & Frequency penalties
  - Search modes (web, academic, sec)
  - Language selection (30+ languages)
  - Date filtering & domain restrictions

### 🌐 Localhost API Server
- **RESTful API** running on `localhost:3000`
- **Auto-start** with GUI launch
- **Full endpoint support**:
  - `/api/health` - Health check
  - `/api/chat` - Chat completions
  - `/api/history/clear` - Clear conversation
  - `/api/models` - List available models

### 🔐 Security
- **Encrypted storage** - API keys encrypted with Fernet
- **Machine-specific keys** - Encryption tied to your device
- **Secure config** - Stored in `config.json` with encryption

### 📦 Additional Features
- **Conversation history** - Optional context retention
- **Export chats** - Save conversations to text files
- **Token usage tracking** - Monitor API consumption
- **Return images & videos** - Multimedia search results
- **Related questions** - Get follow-up suggestions

---

## 💻 Requirements

- **Python**: 3.8 or higher
- **Operating System**: Windows, macOS, or Linux
- **Perplexity API Key**: Get one from [Perplexity AI](https://www.perplexity.ai/settings/api)

---

## 📥 Installation

### 1. Clone the Repository

```bash
git clone https://github.com/PDraganov07/perplexity-api-gui.git
cd perplexity-api-gui
