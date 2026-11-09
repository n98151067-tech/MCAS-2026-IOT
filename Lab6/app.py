
import os
from functools import wraps

from dotenv import load_dotenv
from flask import (
    Flask,
    jsonify,
    redirect,
    render_template,
    request,
    session,
    url_for,
)
from google import genai
from openai import OpenAI


# =========================
# Environment Variables
# =========================

load_dotenv()

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
GEMINI_MODEL = os.getenv(
    "GEMINI_MODEL",
    "gemini-3.8-flash",
)

OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")
OPENROUTER_MODEL = os.getenv(
    "OPENROUTER_MODEL",
    "openrouter/free",
)

SECRET_KEY = os.getenv("SECRET_KEY")


# 檢查環境變數
if not GEMINI_API_KEY:
    raise RuntimeError(
        "找不到 GEMINI_API_KEY，請先在 .env 填入 API Key。"
    )

if not OPENROUTER_API_KEY:
    raise RuntimeError(
        "找不到 OPENROUTER_API_KEY，請先在 .env 填入 API Key。"
    )

if not SECRET_KEY or SECRET_KEY == "CHANGE_ME":
    raise RuntimeError(
        "請在 .env 設定安全的 SECRET_KEY。"
    )


# =========================
# Flask
# =========================

app = Flask(__name__)
app.secret_key = SECRET_KEY


# Lab 示範帳號
# 正式系統不應使用明文密碼
USERS = {
    "admin": "1234",
}


# =========================
# Gemini
# =========================

gemini_client = genai.Client(
    api_key=GEMINI_API_KEY
)


def ask_gemini(
    message,
    previous_interaction_id=None,
):
    params = {
        "model": GEMINI_MODEL,
        "input": message,
    }

    # 延續上一輪對話
    if previous_interaction_id:
        params["previous_interaction_id"] = (
            previous_interaction_id
        )

    interaction = gemini_client.interactions.create(
        **params
    )

    reply = (
        interaction.output_text or ""
    ).strip()

    if not reply:
        reply = "Gemini 沒有回傳文字內容。"

    return reply, interaction.id


# =========================
# OpenRouter
# =========================

openrouter_client = OpenAI(
    base_url="https://openrouter.ai/api/v1",
    api_key=OPENROUTER_API_KEY,
    timeout=90.0,
)


def ask_openrouter(message):

    response = openrouter_client.chat.completions.create(
        model=OPENROUTER_MODEL,
        messages=[
            {
                "role": "user",
                "content": message,
            }
        ],
    )

    if not response.choices:
        raise RuntimeError(
            "OpenRouter 沒有回傳任何選項。"
        )

    reply = (
        response.choices[0].message.content or ""
    ).strip()

    if not reply:
        raise RuntimeError(
            "OpenRouter 沒有回傳文字內容。"
        )

    return reply


# =========================
# Login Required
# =========================

def login_required(view):

    @wraps(view)
    def wrapped(*args, **kwargs):

        if "user" not in session:

            # API 不做 redirect
            if request.path.startswith("/api/"):
                return jsonify({
                    "error": "請先登入"
                }), 401

            return redirect(
                url_for("login")
            )

        return view(*args, **kwargs)

    return wrapped


# =========================
# Login
# =========================

@app.route(
    "/",
    methods=["GET", "POST"],
)
def login():

    if request.method == "POST":

        username = request.form.get(
            "username", ""
        ).strip()

        password = request.form.get(
            "password", ""
        )

        if (
            username in USERS
            and USERS[username] == password
        ):

            session.clear()
            session["user"] = username

            return redirect(
                url_for("chat_room")
            )

        return render_template(
            "login.html",
            msg="帳號或密碼錯誤",
        )

    if "user" in session:
        return redirect(
            url_for("chat_room")
        )

    return render_template(
        "login.html"
    )


# =========================
# Chat Page
# =========================

@app.get("/chat")
@login_required
def chat_room():

    return render_template(
        "chat.html",
        username=session["user"],
    )


# =========================
# AI Chat API
# Gemini / OpenRouter
# =========================

@app.post("/api/chat")
@login_required
def api_chat():

    data = request.get_json(silent=True) or {}

    message = str(
        data.get("message", "")
    ).strip()

    # 取得使用者選擇的模型
    model = data.get(
        "model",
        "gemini"
    )

    # 檢查訊息
    if not message:
        return jsonify({
            "error": "訊息不可為空"
        }), 400

    if len(message) > 2000:
        return jsonify({
            "error": "訊息過長"
        }), 400

    # 檢查模型名稱
    if model not in ("gemini", "openrouter"):
        return jsonify({
            "error": "不支援的 AI 模型"
        }), 400

    try:

        if model == "gemini":

            previous_id = session.get(
                "gemini_interaction_id"
            )

            reply, interaction_id = ask_gemini(
                message,
                previous_id,
            )

            # 保存 Gemini 對話 ID
            session[
                "gemini_interaction_id"
            ] = interaction_id

        elif model == "openrouter":

            # OpenRouter 暫時使用單輪對話
            reply = ask_openrouter(message)

        return jsonify({
            "reply": reply,
            "model": model,
        })

    except Exception:

        app.logger.exception(
            "AI API 呼叫失敗，model=%s",
            model,
        )

        return jsonify({
            "error":
            "AI API 呼叫失敗，"
            "請檢查 API Key、模型設定及終端機紀錄。"
        }), 502


# =========================
# Reset Conversation
# =========================

@app.post("/api/reset")
@login_required
def reset_chat():

    # 清除 Gemini 對話紀錄
    session.pop(
        "gemini_interaction_id",
        None,
    )

    # OpenRouter 為單輪對話，
    # 目前沒有伺服器端歷史紀錄需要清除

    return jsonify({
        "ok": True
    })


# =========================
# Logout
# =========================

@app.post("/logout")
@login_required
def logout():

    session.clear()

    return redirect(
        url_for("login")
    )


# =========================
# Run Server
# =========================

if __name__ == "__main__":

    print(
        "=== Lab6 Flask Server ==="
    )

    print(
        "Listening on http://0.0.0.0:3000"
    )

    print(
        "Debug mode is OFF"
    )

    app.run(
        host="0.0.0.0",
        port=3000,
        debug=False,
    )
