import tkinter as tk
from tkinter import ttk, messagebox
import os
import sys
import json
import subprocess
import threading

CONFIG_FILE = os.path.expanduser("~/.aider_ui_config.json")
TEMP_CMD_FILE = os.path.expanduser("~/.aider_cmd.ps1")
LANG_FILE = os.path.expanduser("~/.aider_ui_langs.json")

# ==================== 預設語言包資料庫 ====================
DEFAULT_LANGS = {
    "zh_TW": {
        "lang_name": "繁體中文",
        "app_title": "Aider 視覺化中控台",
        "settings_title": "🧠 模型設定與金鑰管理",
        "platform": "選擇平台:",
        "model": "指定模型:",
        "manage_list": "⚙️ 管理清單",
        "api_key": "填入 Key:",
        "save_key": "💾 儲存 Key",
        "key_status": "🔑 平台金鑰狀態:",
        "lang_label": "🌐 語言:",
        "copy_start": "⚡ 複製啟動指令 (至終端機貼上)",
        "project_files": "📁 專案檔案 (雙擊或右鍵加入):",
        "add_context": "➕ 加入視野 (/add)",
        "add_readonly": "🔒 唯讀加入 (/read-only)",
        "pending_files": "📋 待處理檔案清單 (目前已選：{count} 個):",
        "collab_mode": "⚙️ 協作模式",
        "copy_mode": "📋 複製切換指令",
        "tab_1": "🌐 1. 視野與記憶",
        "tab_2": "💻 2. 寫扣與測試",
        "tab_3": "🌐 3. 外部與 Git",
        "tab_4": "⚙️ 4. 系統設定",
        "prompt_label": "🗣️ 給 AI 的指令:",
        "copy_normal": "📋 一般複製",
        "copy_paste": "📋 包裝為 /paste",
        "clear": "🗑️ 清空",
        "help_title": "📚 完整百科 (雙擊自動輸入):",
        "search": "🔍 搜尋:",
        "cmd_header": "指令",
        "desc_header": "用途說明",
        "toast_copied": "✅ 指令已複製，請至終端機右鍵貼上！",
        "toast_prepared": "✅ 已準備指令：",
        "toast_key_saved": "✅ 金鑰儲存成功",
        "msg_warn": "提示",
        "msg_success": "成功",
        "msg_empty_input": "目前輸入框是空的！",
        "msg_select_file": "請先選取檔案！",
        "msg_select_model": "請輸入或選擇正確的模型！",
        "msg_restart": "語言已切換！\n請重新啟動程式以套用新的語言介面。",
        "fetching_models": "🔄 背景抓取模型中...",
        "fav_tag": "[⭐ 最愛] ",
        "hist_tag": "[🕒 歷史] ",
        "m_mgr_fav": "⭐ 切換最愛狀態",
        "m_mgr_up": "⬆️ 往上移動",
        "m_mgr_down": "⬇️ 往下移動",
        "m_mgr_del": "❌ 刪除模型",
        "m_mgr_save": "💾 儲存並關閉",
        "m_add": "➕ 加入選取檔案 (/add)",
        "m_drop": "➖ 移出檔案 (/drop)",
        "m_readonly": "🔒 唯讀加入 (/read-only)",
        "m_context": "📊 查看記憶狀態 (/context)",
        "m_map": "🗺️ 強制更新地圖 (/map-refresh)",
        "m_clear": "🧹 清空對話記憶 (/clear)",
        "m_reset": "💥 徹底重置 (/reset)",
        "m_diff": "🔍 查看程式差異 (/diff)",
        "m_undo": "⏪ 撤銷上次修改 (/undo)",
        "m_lint": "🧹 語法檢查 (/lint)",
        "m_test": "🧪 執行測試 (/test)",
        "m_run": "▶️ 執行終端機指令 (/run)",
        "m_ask": "💬 切換純問答 (/ask)",
        "m_architect": "🏗️ 切換架構師 (/architect)",
        "m_reason": "🧠 推理力度 (/reasoning-effort)",
        "m_think": "⏱️ 思考上限 (/think-tokens)",
        "m_web": "🌐 抓取網頁內容 (/web)",
        "m_copy": "📝 複製 AI 回覆 (/copy)",
        "m_editor": "✍️ 開啟外部編輯器 (/editor)",
        "m_edit": "✏️ 手動編輯檔案 (/edit)",
        "m_voice": "🎙️ 語音輸入 (/voice)",
        "m_git": "📦 執行 Git 指令 (/git)",
        "m_commit": "💾 自動生成 Commit (/commit)",
        "m_models": "🤖 搜尋可用模型 (/models)",
        "m_model_switch": "🔄 臨時切換至指定模型 (/model)",
        "m_settings": "⚙️ 查看當前設定 (/settings)",
        "m_tokens": "🪙 查看 Token 消耗 (/tokens)",
        "m_help": "❓ 查看幫助說明 (/help)",
        "m_exit": "🚪 安全退出 Aider (/exit)",
        "help_cmds": [
            ["/add", "將檔案加入 AI 的閱讀視野"], ["/architect", "進入架構師模式"],
            ["/ask", "進入詢問模式"], ["/chat-mode", "切換對話模式"],
            ["/clear", "清空過去的對話歷史"], ["/code", "進入寫程式碼模式"],
            ["/commit", "手動讓 Aider 進行 Git Commit"], ["/context", "顯示目前的上下文狀態"],
            ["/copy", "複製 AI 的最後一次回覆"], ["/copy-context", "複製目前的上下文內容"],
            ["/diff", "顯示自上次提交以來的代碼變更"], ["/drop", "將檔案移出視野，節省 Token"],
            ["/edit", "編輯檔案"], ["/editor", "開啟外部編輯器"],
            ["/editor-model", "切換編輯器使用的模型"], ["/exit", "退出 Aider"],
            ["/git", "執行 Git 指令"], ["/help", "取得 Aider 的幫助資訊"],
            ["/lint", "檢查並修復程式碼語法錯誤"], ["/load", "載入歷史紀錄檔案"],
            ["/ls", "列出目前已加入 Context 的檔案"], ["/map", "顯示目前專案的架構地圖"],
            ["/map-refresh", "強制重新整理專案地圖"], ["/model", "切換目前使用的 AI 模型"],
            ["/models", "搜尋並列出所有可用的模型"], ["/multiline-mode", "切換多行輸入模式"],
            ["/paste", "貼上內容到對話中"], ["/quit", "退出 Aider"],
            ["/read-only", "以唯讀模式加入檔案"], ["/reasoning-effort", "設定思考深度 (推理力度)"],
            ["/report", "回報問題或錯誤"], ["/reset", "清空所有檔案與對話歷史"],
            ["/run", "執行終端機指令"], ["/save", "儲存對話歷史"],
            ["/settings", "顯示目前的設定檔狀態"], ["/test", "執行測試指令"],
            ["/think-tokens", "設定思考過程的最大 Token 數"], ["/tokens", "顯示目前花費的 Token 數量"],
            ["/undo", "🌟 撤銷上一次的修改與 Git 提交"], ["/voice", "使用語音與 Aider 對話"],
            ["/weak-model", "切換弱模型"], ["/web", "抓取網頁內容提供給 AI"]
        ],
        "edit_lang": "✍️ 編輯語言包",
        "msg_open_err": "無法自動開啟檔案，請手動前往修改：\n{path}",
    },
    "en": {
        "lang_name": "English",
        "app_title": "Aider Visual Console",
        "settings_title": "🧠 Model & API Key Settings",
        "platform": "Platform:",
        "model": "Model:",
        "manage_list": "⚙️ Manage List",
        "api_key": "API Key:",
        "save_key": "💾 Save Key",
        "key_status": "🔑 Key Status:",
        "lang_label": "🌐 Language:",
        "copy_start": "⚡ Copy Startup Cmd (Paste in Terminal)",
        "project_files": "📁 Project Files (Double/Right Click to Add):",
        "add_context": "➕ Add to Context (/add)",
        "add_readonly": "🔒 Add Read-only (/read-only)",
        "pending_files": "📋 Pending Files (Selected: {count}):",
        "collab_mode": "⚙️ Collab Mode",
        "copy_mode": "📋 Copy Mode Cmd",
        "tab_1": "🌐 1. Context & Memory",
        "tab_2": "💻 2. Code & Test",
        "tab_3": "🌐 3. External & Git",
        "tab_4": "⚙️ 4. System Settings",
        "prompt_label": "🗣️ Prompt for AI:",
        "copy_normal": "📋 Copy Prompt",
        "copy_paste": "📋 Wrap in /paste",
        "clear": "🗑️ Clear",
        "help_title": "📚 Encyclopedia (Double Click):",
        "search": "🔍 Search:",
        "cmd_header": "Command",
        "desc_header": "Description",
        "toast_copied": "✅ Command copied, right-click in terminal to paste!",
        "toast_prepared": "✅ Command prepared: ",
        "toast_key_saved": "✅ Key saved successfully",
        "msg_warn": "Warning",
        "msg_success": "Success",
        "msg_empty_input": "Prompt box is empty!",
        "msg_select_file": "Please select a file first!",
        "msg_select_model": "Please specify a model!",
        "msg_restart": "Language changed!\nPlease restart the app to apply the new UI language.",
        "fetching_models": "🔄 Fetching models in background...",
        "fav_tag": "[⭐ Fav] ",
        "hist_tag": "[🕒 Hist] ",
        "m_mgr_fav": "⭐ Toggle Favorite",
        "m_mgr_up": "⬆️ Move Up",
        "m_mgr_down": "⬇️ Move Down",
        "m_mgr_del": "❌ Delete Model",
        "m_mgr_save": "💾 Save & Close",
        "m_add": "➕ Add Files (/add)",
        "m_drop": "➖ Drop Files (/drop)",
        "m_readonly": "🔒 Add Read-only (/read-only)",
        "m_context": "📊 Check Memory (/context)",
        "m_map": "🗺️ Refresh Map (/map-refresh)",
        "m_clear": "🧹 Clear Chat (/clear)",
        "m_reset": "💥 Full Reset (/reset)",
        "m_diff": "🔍 View Diff (/diff)",
        "m_undo": "⏪ Undo Last Edit (/undo)",
        "m_lint": "🧹 Lint Code (/lint)",
        "m_test": "🧪 Run Tests (/test)",
        "m_run": "▶️ Run Cmd (/run)",
        "m_ask": "💬 Ask Mode (/ask)",
        "m_architect": "🏗️ Architect Mode (/architect)",
        "m_reason": "🧠 Reasoning Effort (/reasoning-effort)",
        "m_think": "⏱️ Think Tokens (/think-tokens)",
        "m_web": "🌐 Scrape Web (/web)",
        "m_copy": "📝 Copy AI Reply (/copy)",
        "m_editor": "✍️ Open Editor (/editor)",
        "m_edit": "✏️ Edit File (/edit)",
        "m_voice": "🎙️ Voice Input (/voice)",
        "m_git": "📦 Git Command (/git)",
        "m_commit": "💾 Generate Commit (/commit)",
        "m_models": "🤖 Search Models (/models)",
        "m_model_switch": "🔄 Switch to Model (/model)",
        "m_settings": "⚙️ View Settings (/settings)",
        "m_tokens": "🪙 Token Usage (/tokens)",
        "m_help": "❓ Help Docs (/help)",
        "m_exit": "🚪 Exit Aider (/exit)",
        "help_cmds": [
            ["/add", "Add files to context"], ["/architect", "Enter architect mode"],
            ["/ask", "Enter ask mode"], ["/chat-mode", "Switch chat mode"],
            ["/clear", "Clear chat history"], ["/code", "Enter code mode"],
            ["/commit", "Generate git commit"], ["/context", "Show current context"],
            ["/copy", "Copy last AI reply"], ["/copy-context", "Copy current context"],
            ["/diff", "Show code changes since last commit"], ["/drop", "Remove files from context"],
            ["/edit", "Edit a file"], ["/editor", "Open external editor"],
            ["/editor-model", "Switch editor model"], ["/exit", "Exit Aider"],
            ["/git", "Run git command"], ["/help", "Show help documentation"],
            ["/lint", "Lint and fix code"], ["/load", "Load chat history"],
            ["/ls", "List files in context"], ["/map", "Show repo map"],
            ["/map-refresh", "Force map refresh"], ["/model", "Switch AI model"],
            ["/models", "Search available models"], ["/multiline-mode", "Toggle multiline mode"],
            ["/paste", "Paste multi-line content"], ["/quit", "Quit Aider"],
            ["/read-only", "Add files read-only"], ["/reasoning-effort", "Set reasoning effort"],
            ["/report", "Report an issue"], ["/reset", "Drop all files and clear chat"],
            ["/run", "Run shell command"], ["/save", "Save chat history"],
            ["/settings", "Show current settings"], ["/test", "Run tests"],
            ["/think-tokens", "Set thinking tokens limit"], ["/tokens", "Show token usage"],
            ["/undo", "🌟 Undo last edit and commit"], ["/voice", "Use voice input"],
            ["/weak-model", "Switch weak model"], ["/web", "Scrape webpage content"]
        ],
        "edit_lang": "✍️ Edit Lang Pack",
        "msg_open_err": "Cannot open file automatically, please edit manually:\n{path}",
    }
}

class AiderUI:
    def __init__(self, root):
        self.root = root
        self.config = self.load_config()
        self.lang_dict = self.load_languages()
        
        # 取得目前設定的語言，如果找不到就退回英文
        self.current_lang = self.config.get("language", "zh_TW")
        if self.current_lang not in self.lang_dict:
            self.current_lang = "en"
            
        self.root.title(self._("app_title"))
        self.root.geometry("1050x850") 
        self.root.configure(padx=10, pady=10)

        self.selected_files_set = set()
        self.current_fetched_models = [] 
        self.all_commands = self._("help_cmds")

        self.create_widgets()
        self.init_tree_root()
        self.update_file_counter()

    # ==================== 🌐 多國語言翻譯引擎 ====================
    def load_languages(self):
        if not os.path.exists(LANG_FILE):
            with open(LANG_FILE, "w", encoding="utf-8") as f:
                json.dump(DEFAULT_LANGS, f, ensure_ascii=False, indent=4)
            return DEFAULT_LANGS
        try:
            with open(LANG_FILE, "r", encoding="utf-8") as f:
                return json.load(f)
        except:
            return DEFAULT_LANGS

    def open_lang_file(self):
        # 確保檔案已經存在
        if not os.path.exists(LANG_FILE):
            self.load_languages()
            
        try:
            # 根據不同作業系統，呼叫預設的文字編輯器
            if sys.platform == "win32":
                os.startfile(LANG_FILE)
            elif sys.platform == "darwin":  # macOS
                subprocess.call(["open", LANG_FILE])
            else:  # Linux
                subprocess.call(["xdg-open", LANG_FILE])
        except Exception as e:
            messagebox.showerror(self._("msg_warn"), self._("msg_open_err").format(path=LANG_FILE))

    def _(self, key):
        # 尋找當前語言包中的文字，找不到就退回英文，再找不到就直接印出 Key
        return self.lang_dict.get(self.current_lang, {}).get(key, self.lang_dict.get("en", {}).get(key, key))

    def on_lang_change(self, event):
        selected_name = self.lang_var.get()
        # 反向尋找選擇的語言代碼
        for code, data in self.lang_dict.items():
            if data.get("lang_name") == selected_name:
                self.config["language"] = code
                self.save_config()
                messagebox.showinfo(self._("msg_warn"), self._("msg_restart"))
                break

    # ==================== 🌟 自動消失的吐司通知 ====================
    def show_toast(self, message):
        toast = tk.Toplevel(self.root)
        toast.wm_overrideredirect(True)
        toast.attributes("-topmost", True)
        
        frame = tk.Frame(toast, bg="#4CAF50", highlightbackground="#388E3C", highlightthickness=1)
        frame.pack(fill=tk.BOTH, expand=True)
        lbl = tk.Label(frame, text=message, bg="#4CAF50", fg="white", padx=20, pady=10, font=("", 10, "bold"))
        lbl.pack()
        
        toast.update_idletasks()
        w = toast.winfo_width()
        x = self.root.winfo_x() + (self.root.winfo_width() // 2) - (w // 2)
        y = self.root.winfo_y() + self.root.winfo_height() - 100
        toast.geometry(f"+{x}+{y}")
        
        self.root.after(1500, toast.destroy)

    def copy_and_toast(self, text, focus_input=False):
        self.root.clipboard_clear()
        self.root.clipboard_append(text)
        self.root.update()
        
        if focus_input:
            self.prompt_text.delete("1.0", tk.END)
            self.prompt_text.insert(tk.END, text)
            self.prompt_text.focus()
            self.show_toast(f"{self._('toast_prepared')}{text.strip()}")
        else:
            self.show_toast(self._('toast_copied'))

    # ==================== 設定與資料庫管理 ====================
    def load_config(self):
        default_keys = {"OpenRouter": "", "Gemini": "", "DeepSeek": "", "Anthropic": "", "OpenAI": ""}
        if os.path.exists(CONFIG_FILE):
            with open(CONFIG_FILE, "r") as f:
                data = json.load(f)
                if "keys" not in data:
                    data["keys"] = default_keys.copy()
                    data["keys"]["Gemini"] = data.get("gemini_key", "")
                    data["keys"]["DeepSeek"] = data.get("deepseek_key", "")
                if "saved_models" not in data:
                    data["saved_models"] = {p: [] for p in default_keys.keys()}
                data.setdefault("language", "zh_TW")
                return data
        return {"keys": default_keys, "saved_models": {p: [] for p in default_keys.keys()}, "language": "zh_TW"}

    def save_config(self):
        with open(CONFIG_FILE, "w") as f: json.dump(self.config, f)

    def update_keys_listbox(self):
        self.keys_listbox.delete(0, tk.END)
        for provider, key in self.config["keys"].items():
            if key:
                masked = key[:4] + "..." + key[-4:] if len(key) > 8 else "***"
                self.keys_listbox.insert(tk.END, f"✅ {provider}: {masked}")
            else:
                self.keys_listbox.insert(tk.END, f"❌ {provider}: ")

    def on_provider_change(self, event):
        provider = self.provider_var.get()
        if not provider: return
        self.key_entry.delete(0, tk.END)
        self.key_entry.insert(0, self.config["keys"].get(provider, ""))
        self.current_fetched_models = []
        self.refresh_combo_display()
        self.model_combo.set(self._("fetching_models"))
        threading.Thread(target=self.fetch_models_bg, args=(provider,), daemon=True).start()

    def fetch_models_bg(self, provider):
        prefix_map = {"OpenRouter": "openrouter/", "Gemini": "gemini/", "DeepSeek": "deepseek/", "Anthropic": "claude", "OpenAI": "gpt"}
        search_term = prefix_map.get(provider, "")
        try:
            startupinfo = None
            if os.name == 'nt':
                startupinfo = subprocess.STARTUPINFO()
                startupinfo.dwFlags |= subprocess.STARTF_USESHOWWINDOW
            env_copy = os.environ.copy()
            env_map = {"OpenRouter": "OPENROUTER_API_KEY", "Gemini": "GEMINI_API_KEY", "DeepSeek": "DEEPSEEK_API_KEY", "Anthropic": "ANTHROPIC_API_KEY", "OpenAI": "OPENAI_API_KEY"}
            for prov, key in self.config["keys"].items():
                if key: env_copy[env_map.get(prov)] = key

            result = subprocess.run(
                f"aider --list-models {search_term}",
                shell=True, capture_output=True, text=True, encoding="utf-8", errors="ignore",
                env=env_copy, startupinfo=startupinfo, timeout=20  
            )
            models = []
            for line in result.stdout.splitlines() + result.stderr.splitlines():
                line = line.strip()
                if line.startswith("- "): models.append(line[2:].strip())
            self.root.after(0, self.update_fetched_models, models)
        except Exception:
            self.root.after(0, self.update_fetched_models, [])

    def update_fetched_models(self, models):
        self.current_fetched_models = models
        self.refresh_combo_display()
        if "🔄" in self.model_combo.get(): self.model_combo.set("")

    def refresh_combo_display(self):
        provider = self.provider_var.get()
        if not provider: return
        saved = self.config.get("saved_models", {}).get(provider, [])
        favs = [m["id"] for m in saved if m.get("favorite")]
        history = [m["id"] for m in saved if not m.get("favorite")]

        combo_values = []
        if favs: combo_values.extend([f"{self._('fav_tag')}{m}" for m in favs])
        if history: combo_values.extend([f"{self._('hist_tag')}{m}" for m in history])
        existing = set(favs + history)
        new_fetched = [m for m in self.current_fetched_models if m not in existing]
        if new_fetched:
            if combo_values: combo_values.append("--------------------------------")
            combo_values.extend([f"☁️ {m}" for m in new_fetched])
        self.model_combo['values'] = combo_values

    def open_model_manager(self):
        provider = self.provider_var.get()
        if not provider: return messagebox.showwarning(self._("msg_warn"), self._("platform"))
        mgr = tk.Toplevel(self.root)
        mgr.title(f"⚙️ {provider}")
        mgr.geometry("550x350")
        mgr.grab_set()

        list_frame = ttk.Frame(mgr)
        list_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=10, pady=10)
        btn_frame = ttk.Frame(mgr)
        btn_frame.pack(side=tk.RIGHT, fill=tk.Y, padx=10, pady=10)

        listbox = tk.Listbox(list_frame, font=("", 10))
        listbox.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar = ttk.Scrollbar(list_frame, orient="vertical", command=listbox.yview)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        listbox.config(yscrollcommand=scrollbar.set)

        saved_list = self.config["saved_models"].setdefault(provider, [])

        def render_list():
            listbox.delete(0, tk.END)
            for item in saved_list:
                prefix = self._("fav_tag") if item.get("favorite") else self._("hist_tag")
                listbox.insert(tk.END, prefix + item["id"])

        def get_selected_idx():
            sel = listbox.curselection(); return sel[0] if sel else None

        def toggle_fav():
            if (idx := get_selected_idx()) is not None:
                saved_list[idx]["favorite"] = not saved_list[idx].get("favorite")
                render_list(); listbox.selection_set(idx)

        def move_up():
            if (idx := get_selected_idx()) is not None and idx > 0:
                saved_list[idx], saved_list[idx-1] = saved_list[idx-1], saved_list[idx]
                render_list(); listbox.selection_set(idx-1)

        def move_down():
            if (idx := get_selected_idx()) is not None and idx < len(saved_list) - 1:
                saved_list[idx], saved_list[idx+1] = saved_list[idx+1], saved_list[idx]
                render_list(); listbox.selection_set(idx+1)

        def delete_item():
            if (idx := get_selected_idx()) is not None:
                del saved_list[idx]; render_list()

        def save_and_close():
            self.save_config(); self.refresh_combo_display(); mgr.destroy()

        render_list()
        ttk.Button(btn_frame, text=self._("m_mgr_fav"), command=toggle_fav).pack(fill=tk.X, pady=5)
        ttk.Button(btn_frame, text=self._("m_mgr_up"), command=move_up).pack(fill=tk.X, pady=5)
        ttk.Button(btn_frame, text=self._("m_mgr_down"), command=move_down).pack(fill=tk.X, pady=5)
        ttk.Button(btn_frame, text=self._("m_mgr_del"), command=delete_item).pack(fill=tk.X, pady=15)
        ttk.Button(btn_frame, text=self._("m_mgr_save"), command=save_and_close).pack(side=tk.BOTTOM, fill=tk.X)

    def on_key_list_select(self, event):
        selection = self.keys_listbox.curselection()
        if selection:
            provider = self.keys_listbox.get(selection[0]).split(" ")[1].replace(":", "")
            self.provider_var.set(provider)
            self.on_provider_change(None)

    def save_single_key(self):
        if not (provider := self.provider_var.get()): return
        self.config["keys"][provider] = self.key_entry.get().strip()
        self.save_config(); self.update_keys_listbox()
        self.show_toast(self._("toast_key_saved"))

    # ==================== 🛠️ 全新國際化 UI 佈局 ====================
    def create_widgets(self):
        top_frame = ttk.LabelFrame(self.root, text=self._("settings_title"), padding=10)
        top_frame.pack(fill=tk.X, pady=(0, 10))

        top_left = ttk.Frame(top_frame)
        top_left.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        top_right = ttk.Frame(top_frame)
        top_right.pack(side=tk.RIGHT, fill=tk.Y, padx=(10, 0))

        ttk.Label(top_left, text=self._("platform")).grid(row=0, column=0, sticky=tk.W, pady=2)
        self.provider_var = tk.StringVar(value="")
        provider_combo = ttk.Combobox(top_left, textvariable=self.provider_var, width=15, state="readonly")
        provider_combo['values'] = ["OpenRouter", "Gemini", "DeepSeek", "Anthropic", "OpenAI"]
        provider_combo.grid(row=0, column=1, sticky=tk.W, pady=2, padx=5)
        provider_combo.bind("<<ComboboxSelected>>", self.on_provider_change)

        ttk.Label(top_left, text=self._("model")).grid(row=1, column=0, sticky=tk.W, pady=2)
        self.model_combo = ttk.Combobox(top_left, width=45)
        self.model_combo.grid(row=1, column=1, sticky=tk.W, pady=2, padx=5)
        ttk.Button(top_left, text=self._("manage_list"), command=self.open_model_manager).grid(row=1, column=2, padx=2)

        ttk.Label(top_left, text=self._("api_key")).grid(row=2, column=0, sticky=tk.W, pady=2)
        self.key_entry = ttk.Entry(top_left, width=35, show="*")
        self.key_entry.grid(row=2, column=1, sticky=tk.W, pady=2, padx=5)
        ttk.Button(top_left, text=self._("save_key"), command=self.save_single_key).grid(row=2, column=2, padx=2)

        # 🌟 語言切換選單
        lang_frame = ttk.Frame(top_right)
        lang_frame.pack(fill=tk.X, pady=(0, 2))
        ttk.Label(lang_frame, text=self._("lang_label")).pack(side=tk.LEFT)
        ttk.Button(lang_frame, text=self._("edit_lang"), command=self.open_lang_file).pack(side=tk.RIGHT, padx=(5, 0))
        self.lang_var = tk.StringVar()
        lang_combo = ttk.Combobox(lang_frame, textvariable=self.lang_var, state="readonly", width=12)
        lang_combo['values'] = [v.get("lang_name", k) for k, v in self.lang_dict.items()]
        lang_combo.set(self._("lang_name"))
        lang_combo.pack(side=tk.RIGHT)
        lang_combo.bind("<<ComboboxSelected>>", self.on_lang_change)

        ttk.Label(top_right, text=self._("key_status")).pack(anchor=tk.W)
        self.keys_listbox = tk.Listbox(top_right, height=4, width=30)
        self.keys_listbox.pack(fill=tk.BOTH, expand=True, pady=(0, 5))
        self.keys_listbox.bind("<<ListboxSelect>>", self.on_key_list_select)
        
        tk.Button(top_right, text=self._("copy_start"), bg="#2196F3", fg="white", font=("", 10, "bold"), pady=4, command=self.copy_startup_command).pack(fill=tk.X, side=tk.BOTTOM)
        self.update_keys_listbox()

        main_paned = ttk.PanedWindow(self.root, orient=tk.HORIZONTAL)
        main_paned.pack(fill=tk.BOTH, expand=True)

        # ---------------- 🌟 左側：檔案與清單 ----------------
        left_frame = ttk.Frame(main_paned)
        main_paned.add(left_frame, weight=1)

        left_vertical_paned = tk.PanedWindow(left_frame, orient=tk.VERTICAL, sashrelief=tk.RAISED, sashwidth=6, bg="#cccccc")
        left_vertical_paned.pack(fill=tk.BOTH, expand=True)

        tree_frame = ttk.Frame(left_vertical_paned)
        left_vertical_paned.add(tree_frame, stretch="always", height=250)
        ttk.Label(tree_frame, text=self._("project_files")).pack(anchor=tk.W, pady=(0, 5))
        self.tree = ttk.Treeview(tree_frame, selectmode="extended")
        self.tree.pack(fill=tk.BOTH, expand=True)
        self.tree.bind("<Double-1>", self.on_tree_double_click)
        self.tree.bind("<<TreeviewOpen>>", self.on_tree_open)
        
        # 右鍵選單綁定
        self.tree_menu = tk.Menu(self.root, tearoff=0)
        self.tree_menu.add_command(label=self._("add_context"), command=self.rc_add)
        self.tree_menu.add_command(label=self._("add_readonly"), command=self.rc_readonly)
        self.tree.bind("<Button-3>", self.show_tree_menu)

        list_frame = ttk.Frame(left_vertical_paned)
        left_vertical_paned.add(list_frame, stretch="always", height=150)
        
        self.list_label = ttk.Label(list_frame, text="")
        self.list_label.pack(anchor=tk.W, pady=(0, 5))
        self.selected_listbox = tk.Listbox(list_frame)
        self.selected_listbox.pack(fill=tk.BOTH, expand=True, pady=(0, 2))
        self.selected_listbox.bind("<Double-1>", self.on_listbox_double_click)

        # ---------------- 右側：動態變形區 ----------------
        right_frame = ttk.Frame(main_paned)
        main_paned.add(right_frame, weight=3)

        mode_frame = ttk.LabelFrame(right_frame, text=self._("collab_mode"), padding=5)
        mode_frame.pack(side=tk.TOP, fill=tk.X, pady=(0, 5))
        self.mode_var = tk.StringVar(value="code")
        ttk.Radiobutton(mode_frame, text="💻 Code", variable=self.mode_var, value="code").pack(side=tk.LEFT, padx=5)
        ttk.Radiobutton(mode_frame, text="💬 Ask", variable=self.mode_var, value="ask").pack(side=tk.LEFT, padx=5)
        ttk.Radiobutton(mode_frame, text="🏗️ Architect", variable=self.mode_var, value="architect").pack(side=tk.LEFT, padx=5)
        ttk.Button(mode_frame, text=self._("copy_mode"), command=self.copy_mode_command).pack(side=tk.RIGHT, padx=5)

        right_vertical_paned = tk.PanedWindow(right_frame, orient=tk.VERTICAL, sashrelief=tk.RAISED, sashwidth=6, bg="#cccccc")
        right_vertical_paned.pack(side=tk.TOP, fill=tk.BOTH, expand=True)

        self.macro_notebook = ttk.Notebook(right_vertical_paned)
        right_vertical_paned.add(self.macro_notebook, stretch="always", height=120)

        tab1 = ttk.Frame(self.macro_notebook)
        self.macro_notebook.add(tab1, text=self._("tab_1"))
        ttk.Button(tab1, text=self._("m_add"), command=self.macro_add).grid(row=0, column=0, sticky=tk.EW, padx=2, pady=5)
        ttk.Button(tab1, text=self._("m_drop"), command=self.macro_drop).grid(row=0, column=1, sticky=tk.EW, padx=2, pady=5)
        ttk.Button(tab1, text=self._("m_readonly"), command=self.macro_readonly).grid(row=0, column=2, sticky=tk.EW, padx=2, pady=5)
        ttk.Button(tab1, text=self._("m_context"), command=lambda: self.copy_and_toast("/context")).grid(row=1, column=0, sticky=tk.EW, padx=2, pady=5)
        ttk.Button(tab1, text=self._("m_map"), command=lambda: self.copy_and_toast("/map-refresh")).grid(row=1, column=1, sticky=tk.EW, padx=2, pady=5)
        ttk.Button(tab1, text=self._("m_clear"), command=lambda: self.copy_and_toast("/clear")).grid(row=1, column=2, sticky=tk.EW, padx=2, pady=5)
        ttk.Button(tab1, text=self._("m_reset"), command=lambda: self.copy_and_toast("/reset")).grid(row=2, column=0, columnspan=3, sticky=tk.EW, padx=2, pady=5)
        for i in range(3): tab1.columnconfigure(i, weight=1)

        tab2 = ttk.Frame(self.macro_notebook)
        self.macro_notebook.add(tab2, text=self._("tab_2"))
        ttk.Button(tab2, text=self._("m_diff"), command=lambda: self.copy_and_toast("/diff")).grid(row=0, column=0, sticky=tk.EW, padx=2, pady=5)
        ttk.Button(tab2, text=self._("m_undo"), command=lambda: self.copy_and_toast("/undo")).grid(row=0, column=1, sticky=tk.EW, padx=2, pady=5)
        ttk.Button(tab2, text=self._("m_lint"), command=lambda: self.copy_and_toast("/lint")).grid(row=0, column=2, sticky=tk.EW, padx=2, pady=5)
        ttk.Button(tab2, text=self._("m_test"), command=lambda: self.copy_and_toast("/test")).grid(row=1, column=0, sticky=tk.EW, padx=2, pady=5)
        ttk.Button(tab2, text=self._("m_run"), command=lambda: self.copy_and_toast("/run ", focus_input=True)).grid(row=1, column=1, sticky=tk.EW, padx=2, pady=5)
        ttk.Button(tab2, text=self._("m_ask"), command=lambda: self.copy_and_toast("/chat-mode ask")).grid(row=1, column=2, sticky=tk.EW, padx=2, pady=5)
        ttk.Button(tab2, text=self._("m_architect"), command=lambda: self.copy_and_toast("/chat-mode architect")).grid(row=2, column=0, sticky=tk.EW, padx=2, pady=5)
        ttk.Button(tab2, text=self._("m_reason"), command=lambda: self.copy_and_toast("/reasoning-effort ", focus_input=True)).grid(row=2, column=1, sticky=tk.EW, padx=2, pady=5)
        ttk.Button(tab2, text=self._("m_think"), command=lambda: self.copy_and_toast("/think-tokens ", focus_input=True)).grid(row=2, column=2, sticky=tk.EW, padx=2, pady=5)
        for i in range(3): tab2.columnconfigure(i, weight=1)

        tab3 = ttk.Frame(self.macro_notebook)
        self.macro_notebook.add(tab3, text=self._("tab_3"))
        ttk.Button(tab3, text=self._("m_web"), command=lambda: self.copy_and_toast("/web ", focus_input=True)).grid(row=0, column=0, sticky=tk.EW, padx=2, pady=5)
        ttk.Button(tab3, text=self._("m_copy"), command=lambda: self.copy_and_toast("/copy")).grid(row=0, column=1, sticky=tk.EW, padx=2, pady=5)
        ttk.Button(tab3, text=self._("m_editor"), command=lambda: self.copy_and_toast("/editor")).grid(row=0, column=2, sticky=tk.EW, padx=2, pady=5)
        ttk.Button(tab3, text=self._("m_edit"), command=lambda: self.copy_and_toast("/edit ", focus_input=True)).grid(row=1, column=0, sticky=tk.EW, padx=2, pady=5)
        ttk.Button(tab3, text=self._("m_voice"), command=lambda: self.copy_and_toast("/voice")).grid(row=1, column=1, sticky=tk.EW, padx=2, pady=5)
        ttk.Button(tab3, text=self._("m_git"), command=lambda: self.copy_and_toast("/git ", focus_input=True)).grid(row=1, column=2, sticky=tk.EW, padx=2, pady=5)
        ttk.Button(tab3, text=self._("m_commit"), command=lambda: self.copy_and_toast("/commit")).grid(row=2, column=0, columnspan=3, sticky=tk.EW, padx=2, pady=5)
        for i in range(3): tab3.columnconfigure(i, weight=1)

        tab4 = ttk.Frame(self.macro_notebook)
        self.macro_notebook.add(tab4, text=self._("tab_4"))
        ttk.Button(tab4, text=self._("m_models"), command=lambda: self.copy_and_toast("/models ", focus_input=True)).grid(row=0, column=0, sticky=tk.EW, padx=2, pady=5)
        ttk.Button(tab4, text=self._("m_model_switch"), command=self.macro_model_switch).grid(row=0, column=1, sticky=tk.EW, padx=2, pady=5)
        ttk.Button(tab4, text=self._("m_settings"), command=lambda: self.copy_and_toast("/settings")).grid(row=0, column=2, sticky=tk.EW, padx=2, pady=5)
        ttk.Button(tab4, text=self._("m_tokens"), command=lambda: self.copy_and_toast("/tokens")).grid(row=1, column=0, sticky=tk.EW, padx=2, pady=5)
        ttk.Button(tab4, text=self._("m_help"), command=lambda: self.copy_and_toast("/help")).grid(row=1, column=1, sticky=tk.EW, padx=2, pady=5)
        ttk.Button(tab4, text=self._("m_exit"), command=lambda: self.copy_and_toast("/exit")).grid(row=1, column=2, sticky=tk.EW, padx=2, pady=5)
        for i in range(3): tab4.columnconfigure(i, weight=1)

        bottom_horizontal_paned = tk.PanedWindow(right_vertical_paned, orient=tk.HORIZONTAL, sashrelief=tk.RAISED, sashwidth=6, bg="#cccccc")
        right_vertical_paned.add(bottom_horizontal_paned, stretch="always")

        # 🌟 終極強化版輸入框
        input_frame = ttk.Frame(bottom_horizontal_paned)
        bottom_horizontal_paned.add(input_frame, stretch="always", width=350)
        
        input_header_frame = ttk.Frame(input_frame)
        input_header_frame.pack(fill=tk.X, pady=(0, 2))
        ttk.Label(input_header_frame, text=self._("prompt_label")).pack(side=tk.LEFT, anchor=tk.W)
        
        ttk.Button(input_header_frame, text=self._("copy_normal"), command=self.copy_prompt_command).pack(side=tk.RIGHT, padx=2)
        ttk.Button(input_header_frame, text=self._("copy_paste"), command=self.copy_paste_command).pack(side=tk.RIGHT, padx=2)
        ttk.Button(input_header_frame, text=self._("clear"), command=self.clear_prompt).pack(side=tk.RIGHT, padx=2)

        self.prompt_text = tk.Text(input_frame)
        self.prompt_text.pack(fill=tk.BOTH, expand=True, padx=(0, 2))
        self.prompt_text.bind("<Control-Return>", lambda e: self.copy_prompt_command())

        # 🌟 帶有搜尋列的百科區
        help_frame = ttk.Frame(bottom_horizontal_paned)
        bottom_horizontal_paned.add(help_frame, stretch="always")
        
        help_header_frame = ttk.Frame(help_frame)
        help_header_frame.pack(fill=tk.X, pady=(0, 2))
        ttk.Label(help_header_frame, text=self._("help_title")).pack(side=tk.LEFT, anchor=tk.W)
        
        ttk.Label(help_header_frame, text=self._("search")).pack(side=tk.LEFT, padx=(10, 2))
        self.help_search_var = tk.StringVar()
        search_entry = ttk.Entry(help_header_frame, textvariable=self.help_search_var, width=15)
        search_entry.pack(side=tk.LEFT, fill=tk.X, expand=True)
        search_entry.bind("<KeyRelease>", self.filter_help)
        
        columns = ("cmd", "desc")
        self.help_tree = ttk.Treeview(help_frame, columns=columns, show="headings")
        self.help_tree.heading("cmd", text=self._("cmd_header"))
        self.help_tree.heading("desc", text=self._("desc_header"))
        self.help_tree.column("cmd", width=95, stretch=tk.NO, anchor=tk.CENTER)
        self.help_tree.column("desc", width=120, stretch=tk.YES)
        
        help_scroll = ttk.Scrollbar(help_frame, orient=tk.VERTICAL, command=self.help_tree.yview)
        self.help_tree.configure(yscroll=help_scroll.set)
        self.help_tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        help_scroll.pack(side=tk.RIGHT, fill=tk.Y)

        self.help_tree.bind("<Double-1>", self.on_help_double_click)
        self.filter_help()

    # ==================== 檔案樹狀圖與計數器 ====================
    def update_file_counter(self):
        count = len(self.selected_files_set)
        self.list_label.config(text=self._("pending_files").format(count=count))

    def show_tree_menu(self, event):
        item = self.tree.identify_row(event.y)
        if item:
            self.tree.selection_set(item)
            values = self.tree.item(item, "values")
            if values and values[1] == "file":
                self.tree_menu.post(event.x_root, event.y_root)

    def rc_add(self):
        item = self.tree.selection()[0]
        file_path = self.tree.item(item, "values")[0]
        if file_path not in self.selected_files_set:
            self.selected_files_set.add(file_path)
            self.selected_listbox.insert(tk.END, file_path)
            self.update_file_counter()
        self.copy_and_toast(f"/add \"{file_path}\"")

    def rc_readonly(self):
        item = self.tree.selection()[0]
        file_path = self.tree.item(item, "values")[0]
        if file_path not in self.selected_files_set:
            self.selected_files_set.add(file_path)
            self.selected_listbox.insert(tk.END, file_path)
            self.update_file_counter()
        self.copy_and_toast(f"/read-only \"{file_path}\"")

    def populate_tree(self, parent_node, path):
        for item in self.tree.get_children(parent_node): self.tree.delete(item)
        try: entries = os.listdir(path)
        except PermissionError: return 
        dirs = sorted([d for d in entries if os.path.isdir(os.path.join(path, d))])
        files = sorted([f for f in entries if os.path.isfile(os.path.join(path, f))])
        ignore_dirs = {'.git', 'build', 'node_modules', '.gradle', '.idea', '__pycache__', 'AppData'}

        for d in dirs:
            if d in ignore_dirs or d.startswith('.'): continue
            node = self.tree.insert(parent_node, "end", text=d, values=(os.path.join(path, d), "dir"))
            self.tree.insert(node, "end", text="...")
        for f in files:
            self.tree.insert(parent_node, "end", text=f, values=(os.path.relpath(os.path.join(path, f), os.getcwd()), "file"))

    def on_tree_open(self, event):
        node = self.tree.focus()
        children = self.tree.get_children(node)
        if len(children) == 1 and self.tree.item(children[0], "text") == "...":
            self.populate_tree(node, self.tree.item(node, "values")[0])

    def init_tree_root(self):
        self.tree.delete(*self.tree.get_children())
        cwd = os.getcwd()
        root_node = self.tree.insert("", "end", text=f"📁 {os.path.basename(cwd) or cwd}", values=(cwd, "root"), open=True)
        self.populate_tree(root_node, cwd)

    def on_tree_double_click(self, event):
        item = self.tree.selection()[0]
        values = self.tree.item(item, "values")
        if values and values[1] == "file" and values[0] not in self.selected_files_set:
            self.selected_files_set.add(values[0])
            self.selected_listbox.insert(tk.END, values[0])
            self.update_file_counter()

    def on_listbox_double_click(self, event):
        sel = self.selected_listbox.curselection()
        if sel:
            file_path = self.selected_listbox.get(sel[0])
            self.selected_listbox.delete(sel[0])
            self.selected_files_set.remove(file_path)
            self.update_file_counter()

    # ==================== 🌟 指令產出與神級互動 ====================
    def filter_help(self, event=None):
        query = self.help_search_var.get().lower()
        for item in self.help_tree.get_children():
            self.help_tree.delete(item)
        for cmd, desc in self.all_commands:
            if query in cmd.lower() or query in desc.lower():
                self.help_tree.insert("", tk.END, values=(cmd, desc))

    def on_help_double_click(self, event):
        if sel := self.help_tree.selection():
            cmd = self.help_tree.item(sel[0], "values")[0]
            if cmd == "/model":
                self.macro_model_switch()
            else:
                self.copy_and_toast(cmd + " ", focus_input=True)

    def macro_model_switch(self):
        raw_model = self.model_combo.get().strip()
        clean_model = raw_model.replace(self._("fav_tag"), "").replace(self._("hist_tag"), "").replace("☁️ ", "").strip()
        if not clean_model or "---" in clean_model or "🔄" in clean_model:
            self.copy_and_toast("/model ", focus_input=True)
        else:
            self.copy_and_toast(f"/model {clean_model}")

    def copy_mode_command(self):
        self.copy_and_toast(f"/chat-mode {self.mode_var.get()}")

    def clear_prompt(self):
        self.prompt_text.delete("1.0", tk.END)

    def copy_prompt_command(self):
        text = self.prompt_text.get("1.0", tk.END).strip()
        if not text: return messagebox.showwarning(self._("msg_warn"), self._("msg_empty_input"))
        self.copy_and_toast(text)
        
    def copy_paste_command(self):
        text = self.prompt_text.get("1.0", tk.END).strip()
        if not text:
            self.copy_and_toast("/paste", focus_input=True)
        else:
            self.copy_and_toast(f"/paste\n{text}")

    def macro_add(self):
        if not self.selected_files_set: return messagebox.showwarning(self._("msg_warn"), self._("msg_select_file"))
        self.copy_and_toast("/add " + " ".join([f'"{f}"' for f in self.selected_files_set]))

    def macro_drop(self):
        if not self.selected_files_set: return messagebox.showwarning(self._("msg_warn"), self._("msg_select_file"))
        self.copy_and_toast("/drop " + " ".join([f'"{f}"' for f in self.selected_files_set]))

    def macro_readonly(self):
        if not self.selected_files_set: return messagebox.showwarning(self._("msg_warn"), self._("msg_select_file"))
        self.copy_and_toast("/read-only " + " ".join([f'"{f}"' for f in self.selected_files_set]))

    def get_startup_cmd(self):
        raw_model = self.model_combo.get().strip()
        if not raw_model or "--------------------------------" in raw_model or "🔄" in raw_model:
            messagebox.showwarning(self._("msg_warn"), self._("msg_select_model"))
            return ""

        clean_model = raw_model.replace(self._("fav_tag"), "").replace(self._("hist_tag"), "").replace("☁️ ", "").strip()
        provider = self.provider_var.get()
        if provider:
            saved = self.config["saved_models"].setdefault(provider, [])
            if not any(m["id"] == clean_model for m in saved):
                saved.append({"id": clean_model, "favorite": False})
                self.save_config(); self.refresh_combo_display()

        mode = self.mode_var.get()
        prompt = self.prompt_text.get("1.0", tk.END).strip()
        files_args = " ".join([f'"{f}"' for f in self.selected_files_set])
        message_arg = f'-m "{prompt}"' if prompt else ""
        
        mode_arg = f"--chat-mode {mode}" if mode != "code" else ""
        env_map = {"OpenRouter": "OPENROUTER_API_KEY", "Gemini": "GEMINI_API_KEY", "DeepSeek": "DEEPSEEK_API_KEY", "Anthropic": "ANTHROPIC_API_KEY", "OpenAI": "OPENAI_API_KEY"}
        
        env_setup = []
        for prov, key in self.config["keys"].items():
            if key: env_setup.append(f'$env:{env_map.get(prov)}="{key}"')
        env_str = "; ".join(env_setup) + ("; " if env_setup else "")
        
        return f'{env_str}aider --model {clean_model} {mode_arg} --map-tokens 1024 {files_args} {message_arg}'.strip()

    def copy_startup_command(self):
        if cmd := self.get_startup_cmd(): self.copy_and_toast(cmd)

if __name__ == "__main__":
    app = AiderUI(tk.Tk())
    app.root.mainloop()