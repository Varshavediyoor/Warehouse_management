const launcher = document.getElementById("chatbot-launcher");
const container = document.getElementById("chatbot-container");

const startChatBtn = document.getElementById("start-chat-btn");
const welcomeScreen = document.getElementById("welcome-screen");
const chatScreen = document.getElementById("chat-screen");

const closeChat = document.getElementById("close-chat");
const welcomeCloseBtn = document.querySelector(".welcome-close-btn"); // ✅ added

const chatBody = document.getElementById("chat-body");
const chatInput = document.getElementById("chat-input");
const sendBtn = document.getElementById("send-btn");

/* -----------------------------
   OPEN WELCOME WINDOW
------------------------------ */
launcher.addEventListener("click", () => {
  container.classList.add("active");
});

/* -----------------------------
   START CHAT
------------------------------ */
startChatBtn.addEventListener("click", () => {
  container.classList.add("chat-active");
});

/* -----------------------------
   CLOSE FROM WELCOME SCREEN
------------------------------ */
welcomeCloseBtn.addEventListener("click", () => {
  container.classList.remove("active", "chat-active");
});

/* -----------------------------
   CLOSE FROM CHAT SCREEN
------------------------------ */
closeChat.addEventListener("click", () => {
  container.classList.remove("active", "chat-active");
});

/* -----------------------------
   SEND MESSAGE
------------------------------ */
sendBtn.addEventListener("click", sendMessage);
chatInput.addEventListener("keypress", e => {
  if (e.key === "Enter") sendMessage();
});

function sendMessage() {
  const msg = chatInput.value.trim();
  if (!msg) return;

  const userMsg = document.createElement("div");
  userMsg.className = "user-msg";
  userMsg.textContent = msg;
  chatBody.appendChild(userMsg);
  chatInput.value = "";

  chatBody.scrollTop = chatBody.scrollHeight;

  setTimeout(() => {
    const botMsg = document.createElement("div");
    botMsg.className = "bot-msg";
    botMsg.textContent = "Thanks! Our team will assist you shortly 😊";
    chatBody.appendChild(botMsg);
    chatBody.scrollTop = chatBody.scrollHeight;
  }, 1000);
}
