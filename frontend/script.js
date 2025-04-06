window.addEventListener("DOMContentLoaded", () => {
  const chatBody = document.getElementById("chatBody");
  const input = document.getElementById("userInput");
  const sendBtn = document.getElementById("sendBtn");

  let chatHistory = [
    { role: "system", content: "You are a helpful assistant." }
  ];

  async function sendMessage() {
    const message = input.value.trim();
    if (!message) return;

    appendMessage("user", message);
    input.value = "";

    chatHistory.push({ role: "user", content: message });

    try {
      const res = await fetch("/chat", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ messages: chatHistory })
      });

      const data = await res.json();
      if (!data.response) {
        appendMessage("bot", "❌ Sorry, something went wrong.");
        return;
      }

      chatHistory.push({ role: "assistant", content: data.response });
      appendMessage("bot", data.response, message);
    } catch (err) {
      appendMessage("bot", "❌ Network error occurred.");
      console.error("Fetch failed:", err);
    }
  }

  function appendMessage(role, content, userMessage = null) {
    const messageDiv = document.createElement("div");
    messageDiv.className = `message ${role}`;
    messageDiv.innerHTML = marked.parse(content);

    chatBody.appendChild(messageDiv);

    if (role === "bot" && userMessage) {
      const feedback = document.createElement("div");
      feedback.className = "feedback";
      feedback.innerHTML = `
        <img src="https://img.icons8.com/material-rounded/24/000000/thumb-up.png" onclick="sendFeedback('${userMessage}', \`${content}\`, 'up')" />
        <img src="https://img.icons8.com/material-rounded/24/000000/thumbs-down.png" onclick="sendFeedback('${userMessage}', \`${content}\`, 'down')" />
      `;
      messageDiv.appendChild(feedback);
    }

    chatBody.scrollTop = chatBody.scrollHeight;
  }

  async function sendFeedback(message, response, rating) {
    try {
      await fetch("/feedback", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ message, response, rating })
      });
    } catch (err) {
      console.error("Feedback failed:", err);
    }
  }

  // Event listeners
  input.addEventListener("keydown", (e) => {
    if (e.key === "Enter") sendMessage();
  });

  sendBtn.addEventListener("click", sendMessage);
});
