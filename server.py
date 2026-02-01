from flask import Flask, jsonify, send_from_directory, request
from flask_cors import CORS
import os
import psycopg2

# ======================================================
# CONFIG APP
# ======================================================
app = Flask(__name__, static_folder="static", template_folder="templates")
CORS(app)

# ======================================================
# DATABASE (SUPABASE / POSTGRES)
# ======================================================
DB_HOST = os.environ.get("DB_HOST", "db.phqsoznnrrcjyebzyfht.supabase.co")
DB_NAME = os.environ.get("DB_NAME", "postgres")
DB_USER = os.environ.get("DB_USER", "postgres")
DB_PASS = os.environ.get("DB_PASS", "Ieqcentral2026*")
DB_PORT = os.environ.get("DB_PORT", "5432")

def get_conn():
    return psycopg2.connect(
        host=DB_HOST,
        database=DB_NAME,
        user=DB_USER,
        password=DB_PASS,
        port=DB_PORT
    )

# ======================================================
# STATIC / PWA
# ======================================================
@app.route("/sw.js")
def sw():
    return send_from_directory("static", "sw.js")

@app.route("/manifest.json")
def manifest():
    return send_from_directory("static", "manifest.json")

# ======================================================
# API
# ======================================================
@app.route("/api/me")
def me():
    return jsonify(ok=True, user={"nome": "Administrador", "role": "admin"})

@app.route("/api/estatisticas")
def estatisticas():
    conn = get_conn()
    c = conn.cursor()
    c.execute("SELECT COUNT(*) FROM alunos")
    alunos = c.fetchone()[0]
    c.execute("SELECT COUNT(*) FROM usuarios")
    equipe = c.fetchone()[0]
    conn.close()
    return jsonify(ok=True, alunos=alunos, equipe=equipe)

# ======================================================
# FRONTEND
# ======================================================
@app.route("/")
def index():
    return send_from_directory("templates", "index.html")

# ======================================================
# WSGI ENTRYPOINT (IMPORTANTE)
# ======================================================
# NÃO coloque app.run aqui para produção

