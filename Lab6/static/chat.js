
const form = document.getElementById("chat-form");
const input = document.getElementById("message-input");
const sendButton = document.getElementById("send-button");
const resetButton = document.getElementById("reset-button");
const messages = document.getElementById("messages");

// 新增：取得 AI 模型選擇器
const modelSelect = document.getElementById("model-select");

// 新增：依照選擇顯示模型名稱
function getModelName() {
    return modelSelect.value === "gemini"
        ? "Gemini"
        : "OpenRouter";
}

// 原本的訊息顯示函式
function addMessage(text, type) {
    const div = document.createElement("div");

    div.className = "message " + type;
    div.textContent = text;

    messages.appendChild(div);
    messages.scrollTop = messages.scrollHeight;

    return div;
}

// 傳送訊息
form.addEventListener("submit", async (event) => {
    event.preventDefault();

    const message = input.value.trim();

    if (!message) return;

    // 記錄本次選擇的模型
    const selectedModel = modelSelect.value;
    const modelName = getModelName();

    addMessage("You：" + message, "user-message");

    input.value = "";
    input.disabled = true;
    sendButton.disabled = true;
    modelSelect.disabled = true;

    // 新增：等待提示
    const loadingMessage = addMessage(
        modelName + "：正在思考中⋯",
        "ai"
    );

    try {
        const response = await fetch("/api/chat", {
            method: "POST",

            headers: {
                "Content-Type": "application/json"
            },

            body: JSON.stringify({
                message: message,
                model: selectedModel
            })
        });

        const data = await response.json();

        if (!response.ok) {
            throw new Error(
                data.error || "伺服器發生錯誤"
            );
        }

        // 更新等待提示為真正回答
        loadingMessage.textContent =
            modelName + "：" + data.reply;

    } catch (error) {
        loadingMessage.className =
            "message error-message";

        loadingMessage.textContent =
            "Error：" + error.message;

    } finally {
        input.disabled = false;
        sendButton.disabled = false;
        modelSelect.disabled = false;
        input.focus();
    }
});

// 重設對話
resetButton.addEventListener("click", async () => {
    resetButton.disabled = true;

    try {
        const response = await fetch("/api/reset", {
            method: "POST"
        });

        if (!response.ok) {
            throw new Error("重設對話失敗");
        }

        messages.innerHTML = "";

        addMessage(
            getModelName() + "：已開始新的對話。",
            "ai"
        );

    } catch (error) {
        addMessage(
            "Error：" + error.message,
            "error-message"
        );

    } finally {
        resetButton.disabled = false;
    }
});
