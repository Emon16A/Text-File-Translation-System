document.addEventListener("DOMContentLoaded", async function () {
    const languageSelect = document.getElementById("language-select");
    const historyList = document.getElementById("history-list");
    const translatedText = document.getElementById("translated-text");
    const translationResult = document.getElementById("translation-result");
    const downloadBtn = document.getElementById("download-btn");
    const downloadHistoryBtn = document.getElementById("download-history-btn");
    const languageResponse = await fetch("/api/languages");
    const languages = await languageResponse.json();

    // Fetch supported languages
    try {
        const response = await fetch("/api/languages");
        const languages = await response.json();
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
                const listItem = document.createElement("li");
                const languageName = languages[item.language] || item.language;
                listItem.innerHTML = `
                    <div>
                        <p><strong>Translated to ${languageName}:</strong> ${item.translated.substring(0, 50)}...</p>
                        <button class="download-history-btn" data-id="${item.id}">Download Translation</button>
                    </div>
                    <hr>
                `;
                listItem.classList.add("history-item");
                historyList.appendChild(listItem);
            });

            // Add event listeners to each download button
            const downloadButtons = document.querySelectorAll(".download-history-btn");
            downloadButtons.forEach(button => {
                button.addEventListener("click", async function () {
                    const itemId = this.getAttribute("data-id");
                    const response = await fetch(`/api/upload/download/${itemId}`);
                    const data = await response.blob();
                    const link = document.createElement("a");
                    link.href = URL.createObjectURL(data);
                    link.download = `translated_${itemId}.txt`;
                    link.click();
                });
            });
        } catch (error) {
            console.error("Error fetching history:", error);
        }
    }
    fetchHistory();

    // Handle file upload and translation
    document.getElementById("upload-form").addEventListener("submit", async function (event) {
        event.preventDefault();
        const formData = new FormData(this);
        const statusDiv = document.getElementById("status");

        try {
            statusDiv.innerText = "Uploading and translating...";
            const response = await fetch("/api/upload/", { method: "POST", body: formData });
            if (response.ok) {
                const data = await response.json();
                translatedText.innerText = data.translated;
                translationResult.style.display = "block";
                statusDiv.innerText = "Translation completed.";
                fetchHistory(); // Update history

                // Enable download button and set the correct link
                downloadBtn.style.display = "inline-block";
                downloadBtn.onclick = function () {
                    const downloadUrl = `/api/upload/download/${data.id}`;
                    const a = document.createElement("a");
                    a.href = downloadUrl;
                    a.download = `translated_${data.id}.txt`;
                    a.click();
                };
            } else {
                statusDiv.innerText = "Failed to translate.";
            }
        } catch (error) {
            console.error("Error:", error);
            statusDiv.innerText = "An error occurred.";
        }
    });

    // Handle history download
    downloadHistoryBtn.addEventListener("click", async function () {
        try {
            const response = await fetch("/api/upload/history");
            const history = await response.json();

            let historyContent = "Translation History:\n\n";
            history.forEach(item => {
                const languageName = languages[item.language] || item.language;
                historyContent += `Translated to ${languageName}: ${item.translated.substring(0, 50)}...\n`;
            });

            const blob = new Blob([historyContent], { type: 'text/plain' });
            const a = document.createElement("a");
            a.href = URL.createObjectURL(blob);
            a.download = "translation_history.txt";
            a.click();
        } catch (error) {
            console.error("Error downloading history:", error);
        }
    });
});
