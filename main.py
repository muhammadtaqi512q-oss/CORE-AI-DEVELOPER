import os
import sqlite3
from flask import Flask, render_template_string, request, jsonify

app = Flask(__name__)

# Database configuration (Checks local folder first, then fallback to KingAIData)
LOCAL_DB = "taqi.db"
DB_DIR = os.path.join(os.path.expanduser("~"), "KingAIData")
DEFAULT_DB = os.path.join(DB_DIR, "taqi.db")

if os.path.exists(LOCAL_DB):
    DB_NAME = LOCAL_DB
elif os.path.exists(DEFAULT_DB):
    DB_NAME = DEFAULT_DB
else:
    DB_NAME = LOCAL_DB

def query_king(user_query):
    """Fetch matching reply from taqi.db with exact and partial matching."""
    if not os.path.exists(DB_NAME):
        return "⚠️ Database 'taqi.db' not found. Please place it in the project folder!"
    
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    query_clean = user_query.strip().lower()

    # Exact match
    cursor.execute("SELECT reply FROM knowledge WHERE keyword = ?", (query_clean,))
    row = cursor.fetchone()

    # Partial/Substring match if exact not found
    if not row:
        cursor.execute("SELECT reply FROM knowledge WHERE ? LIKE '%' || keyword || '%'", (query_clean,))
        row = cursor.fetchone()

    conn.close()
    return row[0] if row else "👑 KING AI: Mujh ko is keyword ya query ke baray mein data nahi mila. Pehle Data add karein!"

# Ultra-Modern, Beautiful Neon UI Template for KING AI
HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>KING AI - Powered by Taqi.db</title>
    <script src="https://cdn.tailwindcss.com"></script>
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css">
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Outfit:wght@300;400;500;600;700;800&display=swap');
        body { font-family: 'Outfit', sans-serif; }
        .glass-panel { background: rgba(15, 23, 42, 0.85); backdrop-filter: blur(20px); border: 1px solid rgba(99, 102, 241, 0.2); }
        .glow-effect { box-shadow: 0 0 40px -10px rgba(99, 102, 241, 0.3); }
        .chat-bubble { background: rgba(30, 41, 59, 0.7); backdrop-filter: blur(10px); border: 1px solid rgba(255, 255, 255, 0.05); }
        ::-webkit-scrollbar { width: 6px; }
        ::-webkit-scrollbar-track { background: #090d16; }
        ::-webkit-scrollbar-thumb { background: #374151; border-radius: 3px; }
    </style>
</head>
<body class="bg-[#07090e] text-slate-100 min-h-screen flex flex-col justify-between selection:bg-indigo-500 selection:text-white">

    <!-- Top Navigation Header -->
    <header class="glass-panel sticky top-0 z-50 px-6 py-4 flex items-center justify-between border-b border-slate-800/80">
        <div class="flex items-center space-x-3">
            <div class="bg-gradient-to-tr from-indigo-600 via-purple-600 to-pink-500 p-2.5 rounded-2xl shadow-lg shadow-indigo-500/30 animate-pulse">
                <i class="fa-solid fa-crown text-white text-lg"></i>
            </div>
            <div>
                <h1 class="font-extrabold text-xl tracking-wider text-transparent bg-clip-text bg-gradient-to-r from-indigo-400 via-purple-300 to-pink-400">KING AI</h1>
                <p class="text-[11px] text-slate-400 font-medium tracking-wide">Autonomous Neural Engine • Created by Muhammad Taqi</p>
            </div>
        </div>
        <div class="flex items-center space-x-2">
            <span class="inline-flex items-center px-3 py-1 rounded-full text-xs font-semibold bg-emerald-500/10 text-emerald-400 border border-emerald-500/20">
                <span class="w-2 h-2 rounded-full bg-emerald-400 animate-ping mr-2"></span> Database Active
            </span>
        </div>
    </header>

    <!-- Main Chat Workspace -->
    <main class="flex-grow flex items-center justify-center p-3 sm:p-6">
        <div class="w-full max-w-3xl glass-panel glow-effect rounded-3xl shadow-2xl flex flex-col h-[82vh] overflow-hidden">
            
            <!-- Chat Header Info -->
            <div class="px-6 py-4 border-b border-slate-800/80 bg-slate-900/40 flex items-center justify-between">
                <div class="flex items-center space-x-3">
                    <div class="w-10 h-10 rounded-xl bg-gradient-to-br from-indigo-500 to-violet-600 flex items-center justify-center shadow-md">
                        <i class="fa-solid fa-robot text-white text-sm"></i>
                    </div>
                    <div>
                        <h2 class="font-bold text-sm text-slate-200">KING Intelligence System</h2>
                        <p class="text-[11px] text-indigo-400">Connected to taqi.db knowledge repository</p>
                    </div>
                </div>
                <button onclick="clearChat()" class="text-xs text-slate-400 hover:text-rose-400 transition px-3 py-1.5 rounded-lg bg-slate-800/60 border border-slate-700/50">
                    <i class="fa-solid fa-trash-can mr-1.5"></i> Clear Chat
                </button>
            </div>

            <!-- Messages Area -->
            <div id="chat-messages" class="flex-grow p-4 sm:p-6 overflow-y-auto space-y-4 text-sm">
                <div class="flex items-start space-x-3 animate-fade-in">
                    <div class="w-8 h-8 rounded-xl bg-gradient-to-tr from-indigo-600 to-purple-600 text-white flex-shrink-0 flex items-center justify-center shadow-lg">
                        <i class="fa-solid fa-crown text-xs"></i>
                    </div>
                    <div class="chat-bubble p-4 rounded-2xl max-w-[85%] text-slate-200 shadow-md">
                        <p class="font-semibold text-indigo-300 mb-1">KING AI 👑</p>
                        Assalam-o-Alaikum! Main <b>KING AI</b> hoon, jise Muhammad Taqi ne banaya hai. Aapke <b>taqi.db</b> database mein jitne keywords saved hain, unke mutabiq mujh se kuch bhi poochein!
                    </div>
                </div>
            </div>

            <!-- Chat Input Box -->
            <div class="p-4 sm:p-5 border-t border-slate-800/80 bg-slate-900/60">
                <form id="chat-form" onsubmit="sendMessage(event)" class="flex items-center space-x-3">
                    <input type="text" id="user-input" autocomplete="off" required placeholder="Type a keyword or question (e.g. hello, python)..." class="flex-grow bg-slate-950 border border-slate-700/80 rounded-2xl px-5 py-3.5 text-sm focus:outline-none focus:border-indigo-500 focus:ring-2 focus:ring-indigo-500/20 transition text-slate-100 placeholder:text-slate-500 shadow-inner">
                    <button type="submit" class="bg-gradient-to-r from-indigo-600 to-violet-600 hover:from-indigo-500 hover:to-violet-500 text-white px-6 py-3.5 rounded-2xl text-sm font-semibold shadow-lg shadow-indigo-600/30 transition-all duration-300 flex items-center justify-center group">
                        <span>Send</span>
                        <i class="fa-solid fa-paper-plane ml-2 group-hover:translate-x-1 transition-transform"></i>
                    </button>
                </form>
            </div>

        </div>
    </main>

    <!-- Footer -->
    <footer class="py-4 text-center text-xs text-slate-500 border-t border-slate-900 bg-[#05070c]">
        KING AI Engine • Powered by SQLite (taqi.db) & Python • Created with ❤️ by Muhammad Taqi
    </footer>

    <!-- Frontend Script Logic -->
    <script>
        async function sendMessage(e) {
            e.preventDefault();
            const inputField = document.getElementById('user-input');
            const query = inputField.value.trim();
            if (!query) return;

            const container = document.getElementById('chat-messages');

            // Append User Message
            container.innerHTML += `
                <div class="flex items-start justify-end space-x-3 animate-fade-in">
                    <div class="bg-gradient-to-r from-indigo-600 to-violet-600 text-white p-4 rounded-2xl max-w-[85%] text-sm shadow-lg">
                        ${escapeHtml(query)}
                    </div>
                    <div class="w-8 h-8 rounded-xl bg-slate-800 text-slate-300 flex-shrink-0 flex items-center justify-center font-bold text-xs shadow">
                        You
                    </div>
                </div>
            `;
            inputField.value = '';
            container.scrollTop = container.scrollHeight;

            // Fetch Response from Python Backend
            try {
                const res = await fetch('/api/ask', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({ query })
                });
                const data = await res.json();

                // Append KING AI Response
                container.innerHTML += `
                    <div class="flex items-start space-x-3 animate-fade-in">
                        <div class="w-8 h-8 rounded-xl bg-gradient-to-tr from-indigo-600 to-purple-600 text-white flex-shrink-0 flex items-center justify-center shadow-lg">
                            <i class="fa-solid fa-crown text-xs"></i>
                        </div>
                        <div class="chat-bubble p-4 rounded-2xl max-w-[85%] text-slate-200 overflow-x-auto shadow-md">
                            <p class="font-semibold text-indigo-300 mb-1">KING AI 👑</p>
                            <pre class="whitespace-pre-wrap font-sans leading-relaxed">${escapeHtml(data.reply)}</pre>
                        </div>
                    </div>
                `;
            } catch (err) {
                container.innerHTML += `
                    <div class="flex items-start space-x-3">
                        <div class="w-8 h-8 rounded-xl bg-rose-600/20 text-rose-400 flex-shrink-0 flex items-center justify-center"><i class="fa-solid fa-triangle-exclamation text-xs"></i></div>
                        <div class="chat-bubble border-rose-500/20 p-4 rounded-2xl max-w-[85%] text-rose-300">
                            Connection error with KING AI server.
                        </div>
                    </div>
                `;
            }
            container.scrollTop = container.scrollHeight;
        }

        function clearChat() {
            document.getElementById('chat-messages').innerHTML = `
                <div class="flex items-start space-x-3">
                    <div class="w-8 h-8 rounded-xl bg-gradient-to-tr from-indigo-600 to-purple-600 text-white flex-shrink-0 flex items-center justify-center shadow-lg">
                        <i class="fa-solid fa-crown text-xs"></i>
                    </div>
                    <div class="chat-bubble p-4 rounded-2xl max-w-[85%] text-slate-200 shadow-md">
                        <p class="font-semibold text-indigo-300 mb-1">KING AI 👑</p>
                        Chat cleared! Aap naye keywords search kar sakte hain.
                    </div>
                </div>
            `;
        }

        function escapeHtml(text) {
            return text.replace(/&/g, "&amp;").replace(/</g, "&lt;").replace(/>/g, "&gt;");
        }
    </script>
</body>
</html>
"""

@app.route("/")
def index():
    return render_template_string(HTML_TEMPLATE)

@app.route("/api/ask", methods=["POST"])
def ask_ai():
    data = request.get_json()
    query = data.get("query", "")
    reply_text = query_king(query)
    return jsonify({"reply": reply_text})

if __name__ == "__main__":
    print("========================================")
    print("👑 KING AI MODERN WEB ENGINE (main.py)")
    print("CREATED BY MUHAMMAD TAQI")
    print(f"Target DB: {DB_NAME}")
    print("Local URL: http://127.0.0.1:5000")
    print("========================================")
    app.run(host="0.0.0.0", port=5000, debug=True)