// Import elements
const importButton = document.getElementById("import-button");
const fileInput = document.getElementById("file-input");
const documentName = document.getElementById("document-name");

// Chat elements
const questionInput = document.getElementById("question-input");
const chatMessages = document.querySelector(".chat-messages");

// Import document
importButton.addEventListener("click", () => {
    fileInput.click();
});


fileInput.addEventListener("change", async () => {
    const file = fileInput.files[0];
    if (!file) {
        return;
    }

    documentName.textContent = `⟳ Processing ${file.name}...`;
    const formData = new FormData();
    formData.append("file", file);

    try {
        const response = await fetch(
            "http://127.0.0.1:8000/api/upload",
            {
                method: "POST",
                body: formData
            }
        );

        const data = await response.json();
        if (!response.ok) {
            throw new Error(
                data.detail || "Document processing failed."
            );
        }
        documentName.textContent = `✓ ${data.filename} · ${data.pages} pages · ${data.chunks} chunks`;
    } catch (error) {
        documentName.textContent = `✕ Failed to process ${file.name}`;
        console.error("Upload failed:", error);
    }
});


// Send question
questionInput.addEventListener("keydown", async (event) => {
    if (event.key !== "Enter" || event.shiftKey) {
        return;
    }
    event.preventDefault();
    const question = questionInput.value.trim();

    if (!question) {
        return;
    }

    addMessage(question, "outgoing");
    questionInput.value = "";
    const thinkingMessage = addThinkingMessage();

    try {
        const response = await fetch(
            "http://127.0.0.1:8000/api/query",
            {
                method: "POST",
                headers: {
                    "Content-Type": "application/json"
                },
                body: JSON.stringify({
                    question: question
                })
            }
        );
        const data = await response.json();
        if (!response.ok) {
            throw new Error(
                data.error || "Question failed."
            );
        }
        thinkingMessage.remove();
        addMessage(data.answer, "incoming");
        if (data.answer.toLowerCase().includes("i don't know")) {
            clearRetrieval();
        } else {
            displayRetrieval(
                data.chunks,
                data.distances
            );
        }
    } catch (error) {
        thinkingMessage.remove();
        console.error("Query failed:", error);
        addMessage(
            "Sorry, something went wrong.",
            "incoming"
        );
    }
});

function addMessage(text, type) {
    const message = document.createElement("div");
    message.classList.add("message", type);
    message.textContent = text;
    chatMessages.appendChild(message);
    chatMessages.scrollTop = chatMessages.scrollHeight;
}

function displayRetrieval(chunks, distances) {
    const retrievalTable = document.querySelector(".retrieval-table");
    retrievalTable.innerHTML = "";
    chunks.forEach((chunk, index) => {
        const card = document.createElement("div");
        card.classList.add("retrieval-card");
        card.innerHTML = `
            <div class="retrieval-card-header">
                <strong>Chunk ${index + 1}</strong>
                <span>Distance: ${distances[index].toFixed(4)}</span>
            </div>
            <div class="retrieval-card-content">
                ${chunk}
            </div>
        `;
        retrievalTable.appendChild(card);
    });
}

function clearRetrieval() {
    const retrievalTable =
        document.querySelector(".retrieval-table");
    retrievalTable.innerHTML = "";
}

function addThinkingMessage() {
    const message = document.createElement("div");
    message.classList.add(
        "message",
        "incoming",
        "thinking"
    );

    message.textContent = "Thinking...";
    chatMessages.appendChild(message);
    chatMessages.scrollTop = chatMessages.scrollHeight;

    return message;
}