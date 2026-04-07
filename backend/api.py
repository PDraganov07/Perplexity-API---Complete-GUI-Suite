#!/usr/bin/env python3

import os
import json
import base64
import hashlib
import requests
from datetime import datetime
from typing import Optional, Dict, Any

from flask import Flask, request, jsonify
from flask_cors import CORS
from cryptography.fernet import Fernet

APP_VERSION   = "2.0.0"
API_PORT      = 3000
CONFIG_FILE   = os.path.join(os.path.dirname(__file__), "config.json")

MODELS = [
    "sonar",
    "sonar-pro",
    "sonar-deep-research",
    "sonar-reasoning-pro",
]

SEARCH_MODES       = ["web", "academic", "sec"]
RESEARCH_EFFORTS   = ["low", "medium", "high"]
RECENCY_FILTERS    = ["none", "day", "week", "month", "year"]
SEARCH_CTX_SIZES   = ["low", "medium", "high"]
LANGUAGES = [
    "none","English","Spanish","French","German","Italian",
    "Portuguese","Russian","Japanese","Korean","Chinese",
    "Arabic","Hindi","Dutch","Turkish","Polish","Swedish",
    "Norwegian","Danish","Finnish","Greek","Czech","Romanian",
    "Hungarian","Thai","Vietnamese","Indonesian","Malay",
    "Hebrew","Persian","Ukrainian","Bulgarian",
]

class ConfigManager:
    def __init__(self):
        self.config_file = CONFIG_FILE
        self.key         = self._get_or_create_key()
        self.cipher      = Fernet(self.key)

    def _get_or_create_key(self) -> bytes:
        machine_id   = f"{os.getenv('COMPUTERNAME','default')}{os.getenv('USERNAME','user')}"
        key_material = hashlib.sha256(machine_id.encode()).digest()
        return base64.urlsafe_b64encode(key_material)

    def save_config(self, api_key: str) -> bool:
        try:
            encrypted = self.cipher.encrypt(api_key.encode()).decode()
            config = {
                "perplexity-api": {
                    "token":      encrypted,
                    "created_at": datetime.now().isoformat(),
                    "version":    APP_VERSION,
                },
                "settings": {
                    "theme":      "dark",
                    "last_model": "sonar-pro",
                },
            }
            with open(self.config_file, "w") as f:
                json.dump(config, f, indent=2)
            return True
        except Exception as e:
            print(f"[ConfigManager] save error: {e}")
            return False

    def load_api_key(self) -> Optional[str]:
        try:
            if not os.path.exists(self.config_file):
                return None
            with open(self.config_file, "r") as f:
                config = json.load(f)
            encrypted = config.get("perplexity-api", {}).get("token")
            if not encrypted:
                return None
            return self.cipher.decrypt(encrypted.encode()).decode()
        except Exception as e:
            print(f"[ConfigManager] load error: {e}")
            return None

    def delete_config(self) -> bool:
        try:
            if os.path.exists(self.config_file):
                os.remove(self.config_file)
            return True
        except Exception as e:
            print(f"[ConfigManager] delete error: {e}")
            return False

class PerplexityClient:
    def __init__(self, api_key: str):
        self.api_key = api_key
        self.base_url = "https://api.perplexity.ai"
        self.conversation_history: list = []

    def chat(
        self,
        prompt: str,
        model: str = "sonar-pro",
        system_prompt: Optional[str] = None,
        temperature: float = 0.7,
        max_tokens: Optional[int] = None,
        top_p: float = 1.0,
        top_k: int = 0,
        presence_penalty: float = 0.0,
        frequency_penalty: float = 0.0,
        search_mode: Optional[str] = None,
        research_effort: Optional[str] = None,
        return_images: bool = False,
        return_related_questions: bool = False,
        return_videos: bool = False,
        search_recency_filter: Optional[str] = None,
        search_date_after: Optional[str] = None,
        search_date_before: Optional[str] = None,
        search_domain_filter: Optional[list] = None,
        language: Optional[str] = None,
        search_context_size: Optional[str] = None,
        response_format: Optional[dict] = None,
        use_conversation_history: bool = False,
    ) -> Dict[str, Any]:

        messages: list = []
        if system_prompt:
            messages.append({"role": "system", "content": system_prompt})
        if use_conversation_history:
            messages.extend(self.conversation_history)
        messages.append({"role": "user", "content": prompt})

        payload: Dict[str, Any] = {
            "model":             model,
            "messages":          messages,
            "temperature":       temperature,
            "top_p":             top_p,
            "presence_penalty":  presence_penalty,
            "frequency_penalty": frequency_penalty,
        }

        if max_tokens:
            payload["max_tokens"] = max_tokens
        if top_k > 0:
            payload["top_k"] = top_k
        if search_mode and search_mode != "web":
            payload["search_mode"] = search_mode
        if research_effort and research_effort != "medium":
            payload["research_effort"] = research_effort
        if return_images:
            payload["return_images"] = True
        if return_related_questions:
            payload["return_related_questions"] = True
        if return_videos:
            payload["return_videos"] = True
        if search_recency_filter and search_recency_filter != "none":
            payload["search_recency_filter"] = search_recency_filter
        if search_date_after:
            payload["search_date_after"] = search_date_after
        if search_date_before:
            payload["search_date_before"] = search_date_before
        if search_domain_filter:
            payload["search_domain_filter"] = search_domain_filter
        if language and language != "none":
            payload["language"] = language
        if search_context_size and search_context_size != "medium":
            payload["search_context_size"] = search_context_size
        if response_format:
            payload["response_format"] = response_format

        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type":  "application/json",
        }

        resp = requests.post(
            f"{self.base_url}/chat/completions",
            headers=headers,
            json=payload,
            timeout=120,
        )
        resp.raise_for_status()
        data = resp.json()

        if use_conversation_history:
            self.conversation_history.append({"role": "user",      "content": prompt})
            self.conversation_history.append({"role": "assistant", "content": data["choices"][0]["message"]["content"]})

        return data

    def clear_history(self):
        self.conversation_history = []

flask_app      = Flask(__name__)
CORS(flask_app)

config_manager = ConfigManager()
client: Optional[PerplexityClient] = None

def _get_client():
    global client
    if client is None:
        key = config_manager.load_api_key()
        if key:
            client = PerplexityClient(key)
    return client

@flask_app.route("/api/health", methods=["GET"])
def health():
    return jsonify({
        "status":     "healthy",
        "version":    APP_VERSION,
        "has_key":    config_manager.load_api_key() is not None,
        "timestamp":  datetime.now().isoformat(),
    })

@flask_app.route("/api/models", methods=["GET"])
def get_models():
    return jsonify({
        "models":           MODELS,
        "search_modes":     SEARCH_MODES,
        "research_efforts": RESEARCH_EFFORTS,
        "recency_filters":  RECENCY_FILTERS,
        "ctx_sizes":        SEARCH_CTX_SIZES,
        "languages":        LANGUAGES,
    })

@flask_app.route("/api/config/key", methods=["GET"])
def key_status():
    key = config_manager.load_api_key()
    return jsonify({"has_key": key is not None})

@flask_app.route("/api/config/key", methods=["POST"])
def save_key():
    global client
    data    = request.json or {}
    api_key = data.get("api_key", "").strip()
    if not api_key:
        return jsonify({"error": "api_key is required"}), 400
    if config_manager.save_config(api_key):
        client = PerplexityClient(api_key)
        return jsonify({"status": "saved"})
    return jsonify({"error": "Failed to save"}), 500

@flask_app.route("/api/config/key", methods=["DELETE"])
def delete_key():
    global client
    config_manager.delete_config()
    client = None
    return jsonify({"status": "deleted"})

@flask_app.route("/api/chat", methods=["POST"])
def chat():
    c = _get_client()
    if not c:
        return jsonify({"error": "No API key configured"}), 401

    data   = request.json or {}
    prompt = data.get("prompt", "").strip()
    if not prompt:
        return jsonify({"error": "prompt is required"}), 400

    try:
        result = c.chat(
            prompt=prompt,
            model=data.get("model", "sonar-pro"),
            system_prompt=data.get("system_prompt"),
            temperature=float(data.get("temperature", 0.7)),
            max_tokens=data.get("max_tokens"),
            top_p=float(data.get("top_p", 1.0)),
            top_k=int(data.get("top_k", 0)),
            presence_penalty=float(data.get("presence_penalty", 0.0)),
            frequency_penalty=float(data.get("frequency_penalty", 0.0)),
            search_mode=data.get("search_mode"),
            research_effort=data.get("research_effort"),
            return_images=bool(data.get("return_images", False)),
            return_related_questions=bool(data.get("return_related_questions", False)),
            return_videos=bool(data.get("return_videos", False)),
            search_recency_filter=data.get("search_recency_filter"),
            search_date_after=data.get("search_date_after"),
            search_date_before=data.get("search_date_before"),
            search_domain_filter=data.get("search_domain_filter"),
            language=data.get("language"),
            search_context_size=data.get("search_context_size"),
            response_format=data.get("response_format"),
            use_conversation_history=bool(data.get("use_conversation_history", False)),
        )
        return jsonify(result)
    except requests.HTTPError as e:
        return jsonify({"error": f"Perplexity API error: {e.response.status_code} {e.response.text}"}), 502
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@flask_app.route("/api/history/clear", methods=["POST"])
def clear_history():
    c = _get_client()
    if c:
        c.clear_history()
    return jsonify({"status": "cleared"})

if __name__ == "__main__":
    print(f"[Perplexity Backend] v{APP_VERSION} - port {API_PORT}")
    flask_app.run(host="127.0.0.1", port=API_PORT, debug=False, use_reloader=False)
