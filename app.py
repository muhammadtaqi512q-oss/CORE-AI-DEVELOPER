from flask import Flask, render_template_string, request, jsonify
import sqlite3
import os

app = Flask(__name__)

# Use a safe directory for SQLite database to prevent Windows permission locks
DB_DIR = os.path.join(os.path.expanduser("~"), "KingAIData")
os.makedirs(DB_DIR, exist_ok=True)
DB_NAME = os.path.join(DB_DIR, "taqi.db")

def init_db():
    """Initialize the SQLite database and create the knowledge table if it doesn't exist."""
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS knowledge (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            keyword TEXT UNIQUE NOT NULL,
            reply TEXT NOT NULL
        )
    ''')
    conn.commit()
    conn.close()

# HTML + CSS + JS Frontend Template (Single File for Zero-Setup)
HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>KING AI - Created by Muhammad Taqi</title>
    <script src="https://cdn.tailwindcss.com"></script>
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css">
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@300;400;500;600;700&display=swap');
        body { font-family: 'Plus Jakarta Sans', sans-serif; }
        .glass { background: rgba(17, 24, 39, 0.75); backdrop-filter: blur(16px); border: 1px solid rgba(255, 255, 255, 0.1); }
        .glass-card { background: rgba(31, 41, 55, 0.5); backdrop-filter: blur(12px); border: 1px solid rgba(255, 255, 255, 0.05); }
    </style>
</head>
<body class="bg-slate-950 text-slate-100 min-h-screen flex flex-col justify-between selection:bg-indigo-500 selection:text-white">

    <!-- Header -->
    <header class="glass sticky top-0 z-50 px-6 py-4 flex items-center justify-between border-b border-slate-800">
        <div class="flex items-center space-x-3 cursor-pointer" onclick="goHome()">
            <div class="bg-gradient-to-tr from-indigo-600 to-violet-500 p-2.5 rounded-xl shadow-lg shadow-indigo-500/30">
                <i class="fa-solid fa-crown text-white text-lg"></i>
            </div>
            <div>
                <h1 class="font-bold text-lg tracking-wide text-transparent bg-clip-text bg-gradient-to-r from-indigo-400 to-violet-300">KING AI</h1>
                <p class="text-xs text-slate-400 font-medium">Created by Muhammad Taqi</p>
            </div>
        </div>
        <div id="nav-btns" class="hidden space-x-2">
            <button onclick="switchTab('add')" id="btn-add" class="px-4 py-2 text-xs font-semibold rounded-lg bg-slate-800 hover:bg-slate-700 transition border border-slate-700"><i class="fa-solid fa-plus mr-1.5"></i> Add Data</button>
            <button onclick="switchTab('chat')" id="btn-chat" class="px-4 py-2 text-xs font-semibold rounded-lg bg-slate-800 hover:bg-slate-700 transition border border-slate-700"><i class="fa-solid fa-comments mr-1.5"></i> Chat</button>
        </div>
    </header>

    <!-- Main Container -->
    <main class="flex-grow flex items-center justify-center p-4 sm:p-6">
        
        <!-- Home / Welcome Options View -->
        <div id="view-home" class="w-full max-w-xl text-center space-y-8 animate-fade-in">
            <div class="space-y-3">
                <span class="inline-flex items-center px-3 py-1 rounded-full text-xs font-medium bg-indigo-500/10 text-indigo-400 border border-indigo-500/20">
                    <span class="w-2 h-2 rounded-full bg-indigo-400 animate-pulse mr-2"></span> Next-Gen Neural Assistant
                </span>
                <h2 class="text-4xl sm:text-5xl font-extrabold tracking-tight">Welcome to <span class="text-transparent bg-clip-text bg-gradient-to-r from-indigo-400 via-purple-400 to-pink-400">KING AI</span></h2>
                <p class="text-slate-400 text-sm sm:text-base max-w-md mx-auto">Train custom data including code snippets or chat instantly with your intelligent knowledge base.</p>
            </div>

            <div class="grid grid-cols-1 sm:grid-cols-2 gap-4 max-w-lg mx-auto pt-2">
                <button onclick="switchTab('add')" class="glass-card hover:bg-slate-800/80 p-6 rounded-2xl text-left transition-all duration-300 group hover:border-indigo-500/50 hover:shadow-xl hover:shadow-indigo-500/10">
                    <div class="w-12 h-12 rounded-xl bg-indigo-600/20 text-indigo-400 flex items-center justify-center mb-4 group-hover:scale-110 transition-transform">
                        <i class="fa-solid fa-database text-xl"></i>
                    </div>
                    <h3 class="font-bold text-lg mb-1">Add Data</h3>
                    <p class="text-xs text-slate-400">Teach KING AI keywords and code replies (Python, HTML, etc.).</p>
                </button>

                <button onclick="switchTab('chat')" class="glass-card hover:bg-slate-800/80 p-6 rounded-2xl text-left transition-all duration-300 group hover:border-violet-500/50 hover:shadow-xl hover:shadow-violet-500/10">
                    <div class="w-12 h-12 rounded-xl bg-violet-600/20 text-violet-400 flex items-center justify-center mb-4 group-hover:scale-110 transition-transform">
                        <i class="fa-solid fa-bolt text-xl"></i>
                    </div>
                    <h3 class="font-bold text-lg mb-1">Chat</h3>
                    <p class="text-xs text-slate-400">Interact with your database and query custom smart replies.</p>
                </button>
            </div>
        </div>

        <!-- Add Data View -->
        <div id="view-add" class="hidden w-full max-w-xl glass p-6 sm:p-8 rounded-3xl shadow-2xl">
            <div class="flex items-center justify-between mb-6 pb-4 border-b border-slate-800">
                <div class="flex items-center space-x-3">
                    <div class="p-2.5 bg-indigo-600/20 text-indigo-400 rounded-xl"><i class="fa-solid fa-database"></i></div>
                    <div>
                        <h3 class="font-bold text-lg">Add Training Data</h3>
                        <p class="text-xs text-slate-400">Save keywords and multi-language code replies</p>
                    </div>
                </div>
                <button onclick="goHome()" class="text-slate-400 hover:text-white text-sm"><i class="fa-solid fa-xmark text-lg"></i></button>
            </div>

            <form id="add-form" onsubmit="handleTrain(event)" class="space-y-4">
                <div>
                    <label class="block text-xs font-semibold text-slate-300 uppercase tracking-wider mb-2">Keywords (comma separated)</label>
                    <input type="text" id="train-keyword" required placeholder="e.g. hello, hi, python template" class="w-full bg-slate-900 border border-slate-700 rounded-xl px-4 py-3 text-sm focus:outline-none focus:border-indigo-500 transition text-slate-100 placeholder:text-slate-600">
                </div>
                <div>
                    <label class="block text-xs font-semibold text-slate-300 uppercase tracking-wider mb-2">Reply / Code Output</label>
                    <textarea id="train-reply" rows="6" required placeholder="Paste plain text, Python code, HTML snippets, etc..." class="w-full bg-slate-900 border border-slate-700 rounded-xl px-4 py-3 text-sm font-mono focus:outline-none focus:border-indigo-500 transition text-slate-100 placeholder:text-slate-600"></textarea>
                </div>
                <div class="flex items-center justify-between pt-2">
                    <span id="train-status" class="text-xs font-medium text-emerald-400"></span>
                    <button type="submit" class="bg-indigo-600 hover:bg-indigo-500 text-white px-6 py-3 rounded-xl text-sm font-semibold shadow-lg shadow-indigo-600/30 transition flex items-center space-x-2">
                        <i class="fa-solid fa-floppy-disk"></i><span>Save Data</span>
                    </button>
                </div>
            </form>
        </div>

        <!-- Chat View -->
        <div id="view-chat" class="hidden w-full max-w-2xl glass rounded-3xl shadow-2xl flex flex-col h-[75vh] sm:h-[80vh]">
            <!-- Chat Header -->
            <div class="p-4 sm:p-6 flex items-center justify-between border-b border-slate-800">
                <div class="flex items-center space-x-3">
                    <div class="relative">
                        <div class="w-10 h-10 rounded-xl bg-violet-600/20 text-violet-400 flex items-center justify-center"><i class="fa-solid fa-robot"></i></div>
                        <span class="absolute bottom-0 right-0 w-3 h-3 bg-emerald-500 border-2 border-slate-900 rounded-full"></span>
                    </div>
                    <div>
                        <h3 class="font-bold text-sm">KING AI Chat</h3>
                        <p class="text-[11px] text-emerald-400">Active • Database Synced</p>
                    </div>
                </div>
                <button onclick="goHome()" class="text-slate-400 hover:text-white text-sm"><i class="fa-solid fa-xmark text-lg"></i></button>
            </div>

            <!-- Messages Area -->
            <div id="chat-messages" class="flex-grow p-4 sm:p-6 overflow-y-auto space-y-4 font-normal text-sm">
                <div class="flex items-start space-x-3">
                    <div class="w-8 h-8 rounded-lg bg-violet-600/20 text-violet-400 flex-shrink-0 flex items-center justify-center"><i class="fa-solid fa-robot text-xs"></i></div>
                    <div class="glass-card p-4 rounded-2xl max-w-[80%] text-slate-200">
                        Hello! I am <b>KING</b>, created by Muhammad Taqi. Ask me anything based on the keywords saved in the database!
                    </div>
                </div>
            </div>

            <!-- Chat Input Bar -->
            <div class="p-4 sm:p-6 border-t border-slate-800 bg-slate-900/50 rounded-b-3xl">
                <form id="chat-form" onsubmit="handleChat(event)" class="flex items-center space-x-2">
                    <input type="text" id="chat-input" autocomplete="off" required placeholder="Type a keyword (e.g. hello)..." class="flex-grow bg-slate-900 border border-slate-700 rounded-xl px-4 py-3 text-sm focus:outline-none focus:border-violet-500 transition text-slate-100 placeholder:text-slate-600">
                    <button type="submit" class="bg-violet-600 hover:bg-violet-500 text-white px-5 py-3 rounded-xl text-sm font-semibold shadow-lg shadow-violet-600/30 transition flex items-center justify-center">
                        <i class="fa-solid fa-paper-plane"></i>
                    </button>
                </form>
            </div>
        </div>

    </main>

    <!-- Footer -->
    <footer class="py-4 text-center text-xs text-slate-500 border-t border-slate-900">
        KING AI Engine • Powered by SQLite & Flask • Developed by Muhammad Taqi
    </footer>

    <!-- Script Utilities -->
    <script>
        function switchTab(tab) {
            document.getElementById('view-home').classList.add('hidden');
            document.getElementById('view-add').classList.add('hidden');
            document.getElementById('view-chat').classList.add('hidden');
            document.getElementById('nav-btns').classList.remove('hidden');

            if (tab === 'add') {
                document.getElementById('view-add').classList.remove('hidden');
            } else if (tab === 'chat') {
                document.getElementById('view-chat').classList.remove('hidden');
            }
        }

        function goHome() {
            document.getElementById('view-home').classList.remove('hidden');
            document.getElementById('view-add').classList.add('hidden');
            document.getElementById('view-chat').classList.add('hidden');
            document.getElementById('nav-btns').classList.add('hidden');
        }

        async function handleTrain(e) {
            e.preventDefault();
            const keyword = document.getElementById('train-keyword').value;
            const reply = document.getElementById('train-reply').value;
            const status = document.getElementById('train-status');

            const res = await fetch('/api/add', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ keyword, reply })
            });
            const data = await res.json();
            
            if (data.success) {
                status.innerText = "Successfully saved!";
                document.getElementById('add-form').reset();
                setTimeout(() => status.innerText = "", 3000);
            } else {
                status.innerText = "Error saving data.";
                status.className = "text-xs font-medium text-rose-400";
            }
        }

        async function handleChat(e) {
            e.preventDefault();
            const inputField = document.getElementById('chat-input');
            const query = inputField.value.trim();
            if (!query) return;

            const container = document.getElementById('chat-messages');

            // Append User Message
            container.innerHTML += `
                <div class="flex items-start justify-end space-x-3">
                    <div class="bg-indigo-600 text-white p-4 rounded-2xl max-w-[80%] text-sm shadow-md">
                        ${escapeHtml(query)}
                    </div>
                </div>
            `;
            inputField.value = '';
            container.scrollTop = container.scrollHeight;

            // Fetch AI Response
            try {
                const res = await fetch('/api/chat', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({ query })
                });
                const data = await res.json();

                // Append AI Response
                container.innerHTML += `
                    <div class="flex items-start space-x-3">
                        <div class="w-8 h-8 rounded-lg bg-violet-600/20 text-violet-400 flex-shrink-0 flex items-center justify-center"><i class="fa-solid fa-robot text-xs"></i></div>
                        <div class="glass-card p-4 rounded-2xl max-w-[80%] text-slate-200 overflow-x-auto">
                            <pre class="whitespace-pre-wrap font-sans">${escapeHtml(data.reply)}</pre>
                        </div>
                    </div>
                `;
            } catch (err) {
                container.innerHTML += `
                    <div class="flex items-start space-x-3">
                        <div class="w-8 h-8 rounded-lg bg-rose-600/20 text-rose-400 flex-shrink-0 flex items-center justify-center"><i class="fa-solid fa-triangle-exclamation text-xs"></i></div>
                        <div class="glass-card border-rose-500/20 p-4 rounded-2xl max-w-[80%] text-rose-300">
                            Server connection error.
                        </div>
                    </div>
                `;
            }
            container.scrollTop = container.scrollHeight;
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

@app.route("/api/add", methods=["POST"])
def add_data():
    data = request.get_json()
    keywords = data.get("keyword", "")
    reply = data.get("reply", "")

    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    kw_list = [kw.strip().lower() for kw in keywords.split(",") if kw.strip()]

    try:
        for kw in kw_list:
            cursor.execute('''
                INSERT INTO knowledge (keyword, reply) VALUES (?, ?)
                ON CONFLICT(keyword) DO UPDATE SET reply=excluded.reply
            ''', (kw, reply))
        conn.commit()
        success = True
    except Exception as e:
        print(e)
        success = False
    finally:
        conn.close()

    return jsonify({"success": success})

@app.route("/api/chat", methods=["POST"])
def chat():
    data = request.get_json()
    query = data.get("query", "").strip().lower()

    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    cursor.execute("SELECT reply FROM knowledge WHERE keyword = ?", (query,))
    row = cursor.fetchone()

    if not row:
        cursor.execute("SELECT reply FROM knowledge WHERE ? LIKE '%' || keyword || '%'", (query,))
        row = cursor.fetchone()

    conn.close()

    if row:
        reply_text = row[0]
    else:
        reply_text = "Sorry, data not found."

    return jsonify({"reply": reply_text})

if __name__ == "__main__":
    init_db()
    print("========================================")
    print("KING AI IS RUNNING...")
    print("CREATED BY MUHAMMAD TAQI")
    print("Access locally at: http://127.0.0.1:5000")
    print("========================================")
    app.run(host="0.0.0.0", port=5000, debug=True)