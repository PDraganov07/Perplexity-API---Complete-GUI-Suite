#!/usr/bin/env python3
"""
Perplexity API Complete GUI - Modern Design
Created by: https://community.perplexity.ai/u/brembo/summary
GitHub: https://github.com/PDraganov07
"""

import os
import json
import base64
import threading
import requests
from datetime import datetime
from typing import Optional, Dict, Any
import customtkinter as ctk
from tkinter import messagebox
from flask import Flask, request, jsonify
from cryptography.fernet import Fernet
import hashlib

MODELS = [
    "sonar",
    "sonar-pro", 
    "sonar-deep-research",
    "sonar-reasoning-pro"
]

SEARCH_MODES = ["web", "academic", "sec"]
RESEARCH_EFFORTS = ["low", "medium", "high"]
RECENCY_FILTERS = ["none", "day", "week", "month", "year"]
SEARCH_CONTEXT_SIZES = ["low", "medium", "high"]
LANGUAGES = [
    "none", "English", "Spanish", "French", "German", "Italian", 
    "Portuguese", "Russian", "Japanese", "Korean", "Chinese", 
    "Arabic", "Hindi", "Dutch", "Turkish", "Polish", "Swedish", 
    "Norwegian", "Danish", "Finnish", "Greek", "Czech", "Romanian", 
    "Hungarian", "Thai", "Vietnamese", "Indonesian", "Malay", 
    "Hebrew", "Persian", "Ukrainian", "Bulgarian"
]

CONFIG_FILE = "config.json"
APP_VERSION = "1.0.0"
API_PORT = 3000

COLORS = {
    "primary_bg": "#0A0A0A",
    "secondary_bg": "#121212",
    "tertiary_bg": "#1A1A1A",
    "sidebar_bg": "#0D0D0D",
    "accent": "#20B79F",
    "accent_hover": "#1A9680",
    "accent_dim": "#1A8870",
    "text_primary": "#ECECEC",
    "text_secondary": "#8E8E93",
    "text_tertiary": "#636366",
    "border": "#2C2C2E",
    "user_bubble": "#202124",
    "ai_bubble": "#0F0F0F",
    "error": "#FF453A",
    "success": "#30D158",
    "input_bg": "#1C1C1E",
    "hover": "#2C2C2E"
}

class ConfigManager:
    def __init__(self):
        self.config_file = CONFIG_FILE
        self.key = self._get_or_create_key()
        self.cipher = Fernet(self.key)
    
    def _get_or_create_key(self) -> bytes:
        machine_id = f"{os.getenv('COMPUTERNAME', 'default')}{os.getenv('USERNAME', 'user')}"
        key_material = hashlib.sha256(machine_id.encode()).digest()
        return base64.urlsafe_b64encode(key_material)
    
    def save_config(self, api_key: str) -> bool:
        try:
            encrypted_key = self.cipher.encrypt(api_key.encode()).decode()
            
            config = {
                "perplexity-api": {
                    "token": encrypted_key,
                    "created_at": datetime.now().isoformat(),
                    "version": APP_VERSION
                },
                "settings": {
                    "theme": "dark",
                    "last_model": "sonar-pro"
                }
            }
            
            with open(self.config_file, 'w') as f:
                json.dump(config, f, indent=2)
            return True
        except Exception as e:
            print(f"Error saving config: {e}")
            return False
    
    def load_api_key(self) -> Optional[str]:
        try:
            if not os.path.exists(self.config_file):
                return None
            
            with open(self.config_file, 'r') as f:
                config = json.load(f)
            
            encrypted_key = config.get("perplexity-api", {}).get("token")
            if not encrypted_key:
                return None
            
            decrypted = self.cipher.decrypt(encrypted_key.encode())
            return decrypted.decode()
        except Exception as e:
            print(f"Error loading config: {e}")
            return None
    
    def delete_config(self) -> bool:
        try:
            if os.path.exists(self.config_file):
                os.remove(self.config_file)
            return True
        except Exception as e:
            print(f"Error deleting config: {e}")
            return False

class PerplexityClient:
    def __init__(self, api_key: str):
        self.api_key = api_key
        self.base_url = "https://api.perplexity.ai"
        self.conversation_history = []
    
    def chat(self, 
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
             use_conversation_history: bool = False) -> Dict[str, Any]:
        
        messages = []
        
        if system_prompt:
            messages.append({"role": "system", "content": system_prompt})
        
        if use_conversation_history:
            messages.extend(self.conversation_history)
        
        messages.append({"role": "user", "content": prompt})
        
        payload = {
            "model": model,
            "messages": messages,
            "temperature": temperature,
            "top_p": top_p,
            "presence_penalty": presence_penalty,
            "frequency_penalty": frequency_penalty
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
            "Content-Type": "application/json"
        }
        
        response = requests.post(
            f"{self.base_url}/chat/completions",
            headers=headers,
            json=payload,
            timeout=120
        )
        
        response.raise_for_status()
        response_data = response.json()
        
        if use_conversation_history:
            self.conversation_history.append({"role": "user", "content": prompt})
            self.conversation_history.append({
                "role": "assistant",
                "content": response_data['choices'][0]['message']['content']
            })
        
        return response_data
    
    def clear_history(self):
        self.conversation_history = []

flask_app = Flask(__name__)
perplexity_client = None

@flask_app.route('/api/health', methods=['GET'])
def health_check():
    return jsonify({
        "status": "healthy",
        "version": APP_VERSION,
        "timestamp": datetime.now().isoformat()
    })

@flask_app.route('/api/chat', methods=['POST'])
def api_chat():
    if not perplexity_client:
        return jsonify({"error": "API client not initialized"}), 500
    
    try:
        data = request.json
        prompt = data.get('prompt')
        
        if not prompt:
            return jsonify({"error": "Prompt is required"}), 400
        
        response = perplexity_client.chat(
            prompt=prompt,
            model=data.get('model', 'sonar-pro'),
            system_prompt=data.get('system_prompt'),
            temperature=data.get('temperature', 0.7),
            max_tokens=data.get('max_tokens'),
            top_p=data.get('top_p', 1.0),
            top_k=data.get('top_k', 0),
            presence_penalty=data.get('presence_penalty', 0.0),
            frequency_penalty=data.get('frequency_penalty', 0.0),
            search_mode=data.get('search_mode'),
            research_effort=data.get('research_effort'),
            return_images=data.get('return_images', False),
            return_related_questions=data.get('return_related_questions', False),
            return_videos=data.get('return_videos', False),
            search_recency_filter=data.get('search_recency_filter'),
            search_date_after=data.get('search_date_after'),
            search_date_before=data.get('search_date_before'),
            search_domain_filter=data.get('search_domain_filter'),
            language=data.get('language'),
            search_context_size=data.get('search_context_size'),
            response_format=data.get('response_format'),
            use_conversation_history=data.get('use_conversation_history', False)
        )
        
        return jsonify(response)
    
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@flask_app.route('/api/history/clear', methods=['POST'])
def clear_history():
    if perplexity_client:
        perplexity_client.clear_history()
        return jsonify({"status": "history cleared"})
    return jsonify({"error": "Client not initialized"}), 500

@flask_app.route('/api/models', methods=['GET'])
def get_models():
    return jsonify({"models": MODELS})

def start_flask_server():
    flask_app.run(host='0.0.0.0', port=API_PORT, debug=False, use_reloader=False)

class APIKeyWindow(ctk.CTkToplevel):
    def __init__(self, parent, config_manager: ConfigManager, on_success_callback):
        super().__init__(parent)
        
        self.config_manager = config_manager
        self.on_success = on_success_callback
        
        self.title("API Key Setup")
        self.geometry("550x350")
        self.resizable(False, False)
        
        self.configure(fg_color=COLORS["primary_bg"])
        
        self.transient(parent)
        self.grab_set()
        
        self.create_widgets()
        
        self.update_idletasks()
        x = (self.winfo_screenwidth() // 2) - (self.winfo_width() // 2)
        y = (self.winfo_screenheight() // 2) - (self.winfo_height() // 2)
        self.geometry(f"+{x}+{y}")
    
    def create_widgets(self):
        main_frame = ctk.CTkFrame(self, fg_color=COLORS["primary_bg"])
        main_frame.pack(fill="both", expand=True, padx=40, pady=40)
        
        icon_label = ctk.CTkLabel(
            main_frame,
            text="🔐",
            font=ctk.CTkFont(size=48)
        )
        icon_label.pack(pady=(0, 15))
        
        title = ctk.CTkLabel(
            main_frame,
            text="Connect Your API Key",
            font=ctk.CTkFont(size=26, weight="bold"),
            text_color=COLORS["text_primary"]
        )
        title.pack(pady=(0, 8))
        
        subtitle = ctk.CTkLabel(
            main_frame,
            text="Your key will be encrypted and stored securely",
            font=ctk.CTkFont(size=13),
            text_color=COLORS["text_secondary"]
        )
        subtitle.pack(pady=(0, 25))
        
        self.api_key_entry = ctk.CTkEntry(
            main_frame,
            placeholder_text="pplx-xxxxxxxxxxxxxxxxxxxxxxxx",
            width=440,
            height=48,
            font=ctk.CTkFont(size=13),
            fg_color=COLORS["input_bg"],
            border_color=COLORS["border"],
            border_width=1,
            corner_radius=10
        )
        self.api_key_entry.pack(pady=(0, 18))
        self.api_key_entry.bind("<Return>", lambda e: self.save_api_key())
        
        save_btn = ctk.CTkButton(
            main_frame,
            text="Continue",
            command=self.save_api_key,
            width=440,
            height=48,
            corner_radius=10,
            fg_color=COLORS["accent"],
            hover_color=COLORS["accent_hover"],
            font=ctk.CTkFont(size=14, weight="bold")
        )
        save_btn.pack(pady=(0, 8))
        
        cancel_btn = ctk.CTkButton(
            main_frame,
            text="Cancel",
            command=self.destroy,
            width=440,
            height=48,
            fg_color=COLORS["tertiary_bg"],
            hover_color=COLORS["hover"],
            border_width=1,
            border_color=COLORS["border"],
            corner_radius=10,
            font=ctk.CTkFont(size=14)
        )
        cancel_btn.pack()
        
        self.api_key_entry.focus()
    
    def save_api_key(self):
        api_key = self.api_key_entry.get().strip()
        
        if not api_key:
            messagebox.showerror("Error", "Please enter an API key")
            return
        
        if not api_key.startswith("pplx-"):
            result = messagebox.askyesno(
                "Warning",
                "API key doesn't start with 'pplx-'. Continue anyway?"
            )
            if not result:
                return
        
        if self.config_manager.save_config(api_key):
            messagebox.showinfo("Success", "API key saved successfully!")
            self.on_success(api_key)
            self.destroy()
        else:
            messagebox.showerror("Error", "Failed to save API key")

class ChatBubble(ctk.CTkFrame):
    def __init__(self, master, text, is_user=False, **kwargs):
        bg_color = COLORS["user_bubble"] if is_user else COLORS["ai_bubble"]
        super().__init__(
            master,
            fg_color=bg_color,
            corner_radius=16,
            **kwargs
        )
        
        icon = "👤" if is_user else "⚡"
        role = "You" if is_user else "Answer"
        
        header = ctk.CTkLabel(
            self,
            text=f"{icon}  {role}",
            font=ctk.CTkFont(size=13, weight="bold"),
            text_color=COLORS["text_secondary"],
            anchor="w"
        )
        header.pack(anchor="w", padx=18, pady=(14, 8))
        
        message = ctk.CTkLabel(
            self,
            text=text,
            font=ctk.CTkFont(size=14),
            text_color=COLORS["text_primary"],
            anchor="w",
            justify="left",
            wraplength=650
        )
        message.pack(anchor="w", padx=18, pady=(0, 14), fill="x")

class PerplexityGUI(ctk.CTk):
    def __init__(self):
        super().__init__()
        
        self.config_manager = ConfigManager()
        self.client = None
        self.server_running = False
        
        self.title(f"Perplexity - v{APP_VERSION}")
        self.geometry("1500x900")
        
        ctk.set_appearance_mode("dark")
        
        self.configure(fg_color=COLORS["primary_bg"])
        
        saved_key = self.config_manager.load_api_key()
        
        if saved_key:
            self.initialize_client(saved_key)
            self.create_main_interface()
            self.start_server()
        else:
            self.create_main_interface()
            self.after(100, self.show_api_key_setup)
    
    def show_api_key_setup(self):
        APIKeyWindow(self, self.config_manager, self.on_api_key_saved)
    
    def on_api_key_saved(self, api_key: str):
        self.initialize_client(api_key)
        self.start_server()
    
    def initialize_client(self, api_key: str):
        global perplexity_client
        try:
            self.client = PerplexityClient(api_key)
            perplexity_client = self.client
            if hasattr(self, 'status_label'):
                self.update_status("Ready", "success")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to initialize: {e}")
    
    def start_server(self):
        if not self.server_running:
            threading.Thread(target=start_flask_server, daemon=True).start()
            self.server_running = True
            if hasattr(self, 'api_status_label'):
                self.api_status_label.configure(
                    text=f"🟢 localhost:{API_PORT}",
                    text_color=COLORS["success"]
                )
    
    def create_main_interface(self):
        self.grid_columnconfigure(0, weight=0)
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)
        
        self.create_sidebar()
        self.create_chat_area()
    
    def create_sidebar(self):
        sidebar = ctk.CTkFrame(
            self,
            width=300,
            fg_color=COLORS["sidebar_bg"],
            corner_radius=0
        )
        sidebar.grid(row=0, column=0, sticky="nsew")
        sidebar.grid_propagate(False)
        
        header_frame = ctk.CTkFrame(sidebar, fg_color="transparent", height=70)
        header_frame.pack(fill="x", padx=20, pady=(20, 10))
        header_frame.pack_propagate(False)
        
        logo_frame = ctk.CTkFrame(header_frame, fg_color="transparent")
        logo_frame.pack(side="left")
        
        logo = ctk.CTkLabel(
            logo_frame,
            text="⚡",
            font=ctk.CTkFont(size=28)
        )
        logo.pack(side="left", padx=(0, 8))
        
        title_frame = ctk.CTkFrame(logo_frame, fg_color="transparent")
        title_frame.pack(side="left")
        
        title = ctk.CTkLabel(
            title_frame,
            text="Perplexity",
            font=ctk.CTkFont(size=18, weight="bold"),
            text_color=COLORS["text_primary"],
            anchor="w"
        )
        title.pack(anchor="w")
        
        version = ctk.CTkLabel(
            title_frame,
            text=f"v{APP_VERSION}",
            font=ctk.CTkFont(size=10),
            text_color=COLORS["text_tertiary"],
            anchor="w"
        )
        version.pack(anchor="w")
        
        separator = ctk.CTkFrame(sidebar, height=1, fg_color=COLORS["border"])
        separator.pack(fill="x", padx=20, pady=(10, 15))
        
        settings_frame = ctk.CTkScrollableFrame(
            sidebar,
            fg_color="transparent"
        )
        settings_frame.pack(fill="both", expand=True, padx=18, pady=0)
        
        self.create_setting_section(settings_frame, "🤖 Model")
        self.model_var = ctk.StringVar(value="sonar-pro")
        self.create_compact_dropdown(settings_frame, self.model_var, MODELS)
        
        self.create_setting_section(settings_frame, "🔍 Search Mode")
        self.search_mode_var = ctk.StringVar(value="web")
        self.create_compact_dropdown(settings_frame, self.search_mode_var, SEARCH_MODES)
        
        self.create_setting_section(settings_frame, "🌡️ Temperature")
        self.temperature_var = ctk.DoubleVar(value=0.7)
        temp_frame = ctk.CTkFrame(settings_frame, fg_color="transparent")
        temp_frame.pack(fill="x", pady=(0, 18))
        
        temp_slider = ctk.CTkSlider(
            temp_frame,
            from_=0.0,
            to=2.0,
            variable=self.temperature_var,
            number_of_steps=20,
            fg_color=COLORS["tertiary_bg"],
            progress_color=COLORS["accent"],
            button_color=COLORS["accent"],
            button_hover_color=COLORS["accent_hover"],
            height=16
        )
        temp_slider.pack(side="left", fill="x", expand=True)
        
        self.temp_label = ctk.CTkLabel(
            temp_frame,
            text="0.7",
            font=ctk.CTkFont(size=12),
            text_color=COLORS["text_secondary"],
            width=38
        )
        self.temp_label.pack(side="right", padx=(12, 0))
        self.temperature_var.trace_add('write', lambda *args: self.temp_label.configure(text=f"{self.temperature_var.get():.1f}"))
        
        self.create_setting_section(settings_frame, "⚙️ Options")
        
        self.return_images_var = ctk.BooleanVar(value=False)
        self.create_modern_checkbox(settings_frame, "📷 Return Images", self.return_images_var)
        
        self.return_videos_var = ctk.BooleanVar(value=False)
        self.create_modern_checkbox(settings_frame, "🎥 Return Videos", self.return_videos_var)
        
        self.return_related_var = ctk.BooleanVar(value=False)
        self.create_modern_checkbox(settings_frame, "❓ Related Questions", self.return_related_var)
        
        self.use_history_var = ctk.BooleanVar(value=False)
        self.create_modern_checkbox(settings_frame, "💬 History", self.use_history_var)
        
        separator2 = ctk.CTkFrame(sidebar, height=1, fg_color=COLORS["border"])
        separator2.pack(fill="x", padx=20, pady=18)
        
        bottom_frame = ctk.CTkFrame(sidebar, fg_color="transparent")
        bottom_frame.pack(fill="x", padx=20, pady=(0, 20))
        
        self.create_icon_button(bottom_frame, "🔑", "API Key", self.change_api_key)
        self.create_icon_button(bottom_frame, "📚", "Docs", self.show_api_docs)
        self.create_icon_button(bottom_frame, "💾", "Export", self.export_chat)
        
        self.api_status_label = ctk.CTkLabel(
            bottom_frame,
            text="🔴 Server Stopped",
            font=ctk.CTkFont(size=11),
            text_color=COLORS["text_tertiary"]
        )
        self.api_status_label.pack(pady=(12, 0))
    
    def create_chat_area(self):
        chat_container = ctk.CTkFrame(
            self,
            fg_color=COLORS["primary_bg"]
        )
        chat_container.grid(row=0, column=1, sticky="nsew", padx=0, pady=0)
        chat_container.grid_rowconfigure(0, weight=1)
        chat_container.grid_rowconfigure(1, weight=0)
        chat_container.grid_columnconfigure(0, weight=1)
        
        self.chat_frame = ctk.CTkScrollableFrame(
            chat_container,
            fg_color=COLORS["primary_bg"]
        )
        self.chat_frame.grid(row=0, column=0, sticky="nsew", padx=50, pady=30)
        
        welcome_frame = ctk.CTkFrame(self.chat_frame, fg_color="transparent")
        welcome_frame.pack(expand=True, pady=120)
        
        welcome_icon = ctk.CTkLabel(
            welcome_frame,
            text="⚡",
            font=ctk.CTkFont(size=72)
        )
        welcome_icon.pack()
        
        welcome_title = ctk.CTkLabel(
            welcome_frame,
            text="Ask anything",
            font=ctk.CTkFont(size=38, weight="bold"),
            text_color=COLORS["text_primary"]
        )
        welcome_title.pack(pady=(15, 8))
        
        welcome_subtitle = ctk.CTkLabel(
            welcome_frame,
            text="Get instant answers with cited sources",
            font=ctk.CTkFont(size=15),
            text_color=COLORS["text_secondary"]
        )
        welcome_subtitle.pack()
        
        input_container = ctk.CTkFrame(
            chat_container,
            fg_color=COLORS["primary_bg"]
        )
        input_container.grid(row=1, column=0, sticky="ew", padx=50, pady=(0, 35))
        input_container.grid_columnconfigure(0, weight=1)
        
        input_frame = ctk.CTkFrame(
            input_container,
            fg_color=COLORS["input_bg"],
            corner_radius=20,
            border_width=1,
            border_color=COLORS["border"]
        )
        input_frame.pack(fill="x")
        input_frame.grid_columnconfigure(0, weight=1)
        
        self.user_input = ctk.CTkTextbox(
            input_frame,
            height=70,
            font=ctk.CTkFont(size=14),
            fg_color=COLORS["input_bg"],
            border_width=0,
            corner_radius=0,
            wrap="word",
            text_color=COLORS["text_primary"]
        )
        self.user_input.grid(row=0, column=0, sticky="ew", padx=22, pady=18)
        
        self.user_input.bind("<Return>", self.handle_enter)
        self.user_input.bind("<Shift-Return>", self.handle_shift_enter)
        
        button_frame = ctk.CTkFrame(input_frame, fg_color="transparent")
        button_frame.grid(row=0, column=1, padx=18, pady=18)
        
        self.send_btn = ctk.CTkButton(
            button_frame,
            text="→",
            command=self.send_message,
            width=52,
            height=52,
            corner_radius=12,
            border_width=0,
            fg_color=COLORS["accent"],
            hover_color=COLORS["accent_hover"],
            text_color="white",
            font=ctk.CTkFont(size=22, weight="bold")
        )
        self.send_btn.pack()
        
        hint_label = ctk.CTkLabel(
            input_container,
            text="Press Enter to send • Shift+Enter for new line",
            font=ctk.CTkFont(size=11),
            text_color=COLORS["text_tertiary"]
        )
        hint_label.pack(pady=(10, 0))
        
        self.status_bar = ctk.CTkFrame(
            input_container,
            fg_color="transparent",
            height=25
        )
        self.status_bar.pack(fill="x", pady=(8, 0))
        
        self.status_label = ctk.CTkLabel(
            self.status_bar,
            text="Ready" if self.client else "⚠️ No API Key",
            font=ctk.CTkFont(size=12),
            text_color=COLORS["text_secondary"]
        )
        self.status_label.pack(side="left")
    
    def handle_enter(self, event):
        self.send_message()
        return "break"
    
    def handle_shift_enter(self, event):
        return
    
    def create_setting_section(self, parent, title):
        label = ctk.CTkLabel(
            parent,
            text=title,
            font=ctk.CTkFont(size=12, weight="bold"),
            text_color=COLORS["text_secondary"],
            anchor="w"
        )
        label.pack(fill="x", pady=(8, 10))
    
    def create_compact_dropdown(self, parent, variable, values):
        dropdown = ctk.CTkOptionMenu(
            parent,
            variable=variable,
            values=values,
            fg_color=COLORS["tertiary_bg"],
            button_color=COLORS["accent"],
            button_hover_color=COLORS["accent_hover"],
            dropdown_fg_color=COLORS["tertiary_bg"],
            corner_radius=10,
            height=38,
            font=ctk.CTkFont(size=13)
        )
        dropdown.pack(fill="x", pady=(0, 18))
        return dropdown
    
    def create_modern_checkbox(self, parent, text, variable):
        checkbox = ctk.CTkCheckBox(
            parent,
            text=text,
            variable=variable,
            fg_color=COLORS["accent"],
            hover_color=COLORS["accent_hover"],
            border_color=COLORS["border"],
            corner_radius=6,
            font=ctk.CTkFont(size=12)
        )
        checkbox.pack(anchor="w", pady=6)
        return checkbox
    
    def create_icon_button(self, parent, icon, text, command):
        btn = ctk.CTkButton(
            parent,
            text=f"{icon}  {text}",
            command=command,
            fg_color=COLORS["tertiary_bg"],
            hover_color=COLORS["hover"],
            corner_radius=10,
            height=42,
            anchor="w",
            font=ctk.CTkFont(size=13)
        )
        btn.pack(fill="x", pady=4)
        return btn
    
    def update_status(self, message, status_type="info"):
        color_map = {
            "success": COLORS["success"],
            "error": COLORS["error"],
            "info": COLORS["text_secondary"]
        }
        self.status_label.configure(
            text=message,
            text_color=color_map.get(status_type, COLORS["text_secondary"])
        )
    
    def change_api_key(self):
        APIKeyWindow(self, self.config_manager, self.on_api_key_saved)
    
    def show_api_docs(self):
        docs_content = f"""╔══════════════════════════════════════════════════════════╗
║       PERPLEXITY API - LOCALHOST SERVER v{APP_VERSION}       ║
╚══════════════════════════════════════════════════════════╝

🌐 Base URL: http://localhost:{API_PORT}

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

📍 ENDPOINTS

┌─────────────────────────────────────────────────────────┐
│ 1. Health Check                                         │
└─────────────────────────────────────────────────────────┘

   GET /api/health
   
   Response:
   {{
     "status": "healthy",
     "version": "{APP_VERSION}",
     "timestamp": "2026-01-26T22:19:00.000000"
   }}

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

┌─────────────────────────────────────────────────────────┐
│ 2. Chat Completion                                      │
└─────────────────────────────────────────────────────────┘

   POST /api/chat
   Content-Type: application/json

   ✨ Basic Request:
   {{
     "prompt": "What is quantum computing?",
     "model": "sonar-pro"
   }}

   ⚙️ Advanced Request (all parameters):
   {{
     "prompt": "Explain AI",
     "model": "sonar-pro",
     "system_prompt": "Be concise",
     "temperature": 0.7,
     "max_tokens": 1000,
     "top_p": 1.0,
     "top_k": 0,
     "presence_penalty": 0.0,
     "frequency_penalty": 0.0,
     "search_mode": "web",
     "research_effort": "medium",
     "return_images": true,
     "return_related_questions": true,
     "return_videos": false,
     "search_recency_filter": "month",
     "search_date_after": "01/01/2024",
     "search_date_before": "12/31/2024",
     "search_domain_filter": ["arxiv.org", "nature.com"],
     "language": "English",
     "search_context_size": "medium",
     "use_conversation_history": false
   }}

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

┌─────────────────────────────────────────────────────────┐
│ 3. Clear Conversation History                          │
└─────────────────────────────────────────────────────────┘

   POST /api/history/clear
   
   Response:
   {{
     "status": "history cleared"
   }}

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

┌─────────────────────────────────────────────────────────┐
│ 4. Get Available Models                                 │
└─────────────────────────────────────────────────────────┘

   GET /api/models
   
   Response:
   {{
     "models": ["sonar", "sonar-pro", "sonar-deep-research", 
                "sonar-reasoning-pro"]
   }}

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

💻 EXAMPLE CODE

┌─────────────────────────────────────────────────────────┐
│ cURL                                                    │
└─────────────────────────────────────────────────────────┘

curl -X POST http://localhost:{API_PORT}/api/chat \\
  -H "Content-Type: application/json" \\
  -d '{{
    "prompt": "What is machine learning?",
    "model": "sonar-pro",
    "temperature": 0.5
  }}'

┌─────────────────────────────────────────────────────────┐
│ Python - requests                                       │
└─────────────────────────────────────────────────────────┘

import requests

response = requests.post(
    "http://localhost:{API_PORT}/api/chat",
    json={{
        "prompt": "Explain neural networks",
        "model": "sonar-pro",
        "return_images": True
    }}
)

result = response.json()
print(result['choices'][0]['message']['content'])

┌─────────────────────────────────────────────────────────┐
│ JavaScript - fetch                                      │
└─────────────────────────────────────────────────────────┘

fetch('http://localhost:{API_PORT}/api/chat', {{
  method: 'POST',
  headers: {{ 'Content-Type': 'application/json' }},
  body: JSON.stringify({{
    prompt: 'What is deep learning?',
    model: 'sonar-pro'
  }})
}})
.then(res => res.json())
.then(data => console.log(data));

┌─────────────────────────────────────────────────────────┐
│ PowerShell                                              │
└─────────────────────────────────────────────────────────┘

$body = @{{
    prompt = "What is AI?"
    model = "sonar-pro"
}} | ConvertTo-Json

Invoke-RestMethod -Uri "http://localhost:{API_PORT}/api/chat" `
  -Method Post -Body $body -ContentType "application/json"

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

📊 PARAMETER REFERENCE

┌──────────────────────┬──────────────┬──────────────────┐
│ Parameter            │ Type         │ Values           │
├──────────────────────┼──────────────┼──────────────────┤
│ model                │ string       │ sonar, sonar-pro │
│                      │              │ sonar-deep-..    │
│ temperature          │ float        │ 0.0 - 2.0        │
│ top_p                │ float        │ 0.0 - 1.0        │
│ top_k                │ integer      │ 0 - 100          │
│ max_tokens           │ integer      │ 1 - 4096         │
│ presence_penalty     │ float        │ -2.0 to 2.0      │
│ frequency_penalty    │ float        │ -2.0 to 2.0      │
│ search_mode          │ string       │ web, academic,   │
│                      │              │ sec              │
│ research_effort      │ string       │ low, medium,     │
│                      │              │ high             │
│ search_recency_filter│ string       │ day, week, month,│
│                      │              │ year             │
│ language             │ string       │ English, Spanish,│
│                      │              │ French, etc      │
│ return_images        │ boolean      │ true, false      │
│ return_videos        │ boolean      │ true, false      │
│ return_related_...   │ boolean      │ true, false      │
└──────────────────────┴──────────────┴──────────────────┘

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

📝 NOTES

• Server runs on port {API_PORT} automatically
• API key encrypted in config.json
• Press Enter to send, Shift+Enter for new line
• Full conversation history support
• All parameters optional except 'prompt'

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Created by: https://github.com/PDraganov07
Community: https://community.perplexity.ai/u/brembo/summary
        """
        
        docs_window = ctk.CTkToplevel(self)
        docs_window.title("API Documentation")
        docs_window.geometry("800x700")
        docs_window.configure(fg_color=COLORS["primary_bg"])
        
        text_widget = ctk.CTkTextbox(
            docs_window,
            font=ctk.CTkFont(size=11, family="Courier New"),
            fg_color=COLORS["secondary_bg"],
            text_color=COLORS["text_primary"]
        )
        text_widget.pack(fill="both", expand=True, padx=20, pady=20)
        text_widget.insert("1.0", docs_content)
        text_widget.configure(state="disabled")
    
    def export_chat(self):
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"perplexity_chat_{timestamp}.txt"
        
        try:
            content = ""
            for widget in self.chat_frame.winfo_children():
                if isinstance(widget, ChatBubble):
                    role = widget.winfo_children()[0].cget("text")
                    text = widget.winfo_children()[1].cget("text")
                    content += f"{role}\n{text}\n\n{'='*60}\n\n"
            
            with open(filename, 'w', encoding='utf-8') as f:
                f.write(content)
            
            self.update_status(f"Exported to {filename}", "success")
        except Exception as e:
            self.update_status(f"Export failed", "error")
    
    def send_message(self):
        if not self.client:
            messagebox.showerror("Error", "No API key configured")
            return
        
        prompt = self.user_input.get("1.0", "end-1c").strip()
        
        if not prompt:
            return
        
        for widget in self.chat_frame.winfo_children():
            widget.destroy()
        
        user_bubble = ChatBubble(self.chat_frame, prompt, is_user=True)
        user_bubble.pack(fill="x", pady=(0, 20), padx=0)
        
        self.send_btn.configure(state="disabled", text="⋯")
        self.update_status("Searching...", "info")
        
        self.user_input.delete("1.0", "end")
        
        threading.Thread(target=self.process_message, args=(prompt,), daemon=True).start()
    
    def process_message(self, prompt: str):
        try:
            response = self.client.chat(
                prompt=prompt,
                model=self.model_var.get(),
                temperature=self.temperature_var.get(),
                search_mode=self.search_mode_var.get(),
                return_images=self.return_images_var.get(),
                return_videos=self.return_videos_var.get(),
                return_related_questions=self.return_related_var.get(),
                use_conversation_history=self.use_history_var.get()
            )
            
            content = response['choices'][0]['message']['content']
            
            self.after(0, lambda: self.display_response(content, response))
            
        except Exception as e:
            self.after(0, lambda: self.display_error(str(e)))
    
    def display_response(self, content, response):
        ai_bubble = ChatBubble(self.chat_frame, content, is_user=False)
        ai_bubble.pack(fill="x", pady=(0, 20), padx=0)
        
        if 'usage' in response and response['usage']:
            tokens = response['usage'].get('total_tokens', 'N/A')
            info_frame = ctk.CTkFrame(
                self.chat_frame,
                fg_color=COLORS["secondary_bg"],
                corner_radius=12
            )
            info_frame.pack(fill="x", pady=(0, 20), padx=0)
            
            ctk.CTkLabel(
                info_frame,
                text=f"📊 {tokens} tokens used",
                font=ctk.CTkFont(size=12),
                text_color=COLORS["text_tertiary"]
            ).pack(padx=18, pady=10)
        
        self.send_btn.configure(state="normal", text="→")
        self.update_status("Ready", "success")
    
    def display_error(self, error):
        error_frame = ctk.CTkFrame(
            self.chat_frame,
            fg_color=COLORS["error"],
            corner_radius=14
        )
        error_frame.pack(fill="x", pady=(0, 20), padx=0)
        
        ctk.CTkLabel(
            error_frame,
            text=f"⚠️  {error}",
            font=ctk.CTkFont(size=13),
            text_color="white"
        ).pack(padx=18, pady=12)
        
        self.send_btn.configure(state="normal", text="→")
        self.update_status("Error occurred", "error")

def main():
    app = PerplexityGUI()
    app.mainloop()

if __name__ == "__main__":
    main()
