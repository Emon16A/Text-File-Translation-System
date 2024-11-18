document.addEventListener("DOMContentLoaded", async function () {
    const languageSelect = document.getElementById("language-select");
    const historyList = document.getElementById("history-list");
    const translatedText = document.getElementById("translated-text");
    const downloadBtn = document.getElementById("download-btn");
    const uploadBtn = document.getElementById("upload-btn");

    // Fetch supported languages
    let languages = {};
    try {
        const response = await fetch("/api/languages");
        languages = await response.json();
        for (const [code, name] of Object.entries(languages)) {
            const option = document.createElement("option");
            option.value = code;
            option.innerText = name;
            languageSelect.appendChild(option);
        }
    } catch (error) {
        console.error("Error fetching languages:", error);
    }

    // Fetch translation history
    async function fetchHistory() {
        try {
            const response = await fetch("/api/upload/history");
            const history = await response.json();
            historyList.innerHTML = ""; // Clear old history

            history.forEach(item => {
                const languageName = languages[item.language] || "Unknown Language";
                const listItem = document.createElement("li");
                listItem.innerHTML = `
                    <div>
                        <p><strong>Translated to ${languageName}:</strong> ${item.translated.substring(0, 50)}...</p>
                        <button class="download-history-btn" data-id="${item.id}">Download Translation</button>
                        <button class="delete-history-btn" data-id="${item.id}" style="margin-left: 10px;">Delete</button>
                    </div>
                `;
                listItem.classList.add("history-item");
                historyList.appendChild(listItem);
            });

            document.querySelectorAll(".download-history-btn").forEach(button => {
                button.addEventListener("click", async function () {
                    const id = this.getAttribute("data-id");
                    const response = await fetch(`/api/upload/download/${id}`);
                    const blob = await response.blob();
                    const link = document.createElement("a");
                    link.href = URL.createObjectURL(blob);
                    link.download = `translation_${id}.txt`;
                    link.click();
                });
            });

            document.querySelectorAll(".delete-history-btn").forEach(button => {
                button.addEventListener("click", async function () {
                    const id = this.getAttribute("data-id");
                    const response = await fetch(`/api/upload/delete/${id}`, { method: "DELETE" });
                    if (response.ok) {
                        alert("Deleted successfully!");
                        fetchHistory();
                    } else {
                        alert("Failed to delete.");
                    }
                });
            });
        } catch (error) {
            console.error("Error fetching history:", error);
        }
    }

    fetchHistory();

    document.getElementById("upload-form").addEventListener("submit", async function (event) {
        event.preventDefault();
        const formData = new FormData(this);
        uploadBtn.disabled = true;

        try {
            const response = await fetch("/api/upload/", { method: "POST", body: formData });
            if (response.ok) {
                const data = await response.json();
                translatedText.innerText = data.translated;
                downloadBtn.style.display = "block";
                downloadBtn.addEventListener("click", () => {
                    const link = document.createElement("a");
                    link.href = data.download_url;
                    link.download = "translated.txt";
                    link.click();
                });
                fetchHistory(); // Refresh history
            } else {
                alert("Failed to upload.");
            }
        } catch (error) {
            console.error("Error uploading file:", error);
        } finally {
            uploadBtn.disabled = false;
        }
    });
});
