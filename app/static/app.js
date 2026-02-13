document.addEventListener("DOMContentLoaded", () => {
    const dropZone = document.getElementById("drop-zone");
    const fileInput = document.getElementById("file-input");
    const statusContainer = document.getElementById("status-container");
    const resultContainer = document.getElementById("result-container");
    const progressBar = document.getElementById("progress-bar");
    const statusText = document.getElementById("status-text");
    const downloadBtn = document.getElementById("download-btn");
    const resetBtn = document.getElementById("reset-btn");

    // Standard Drag & Drop logic
    dropZone.addEventListener("click", () => fileInput.click());

    fileInput.addEventListener("change", (e) => {
        if (fileInput.files.length) {
            handleUpload(fileInput.files[0]);
        }
    });

    ["dragover", "dragleave", "drop"].forEach(event => {
        dropZone.addEventListener(event, (e) => {
            e.preventDefault();
            if (event === "dragover") dropZone.classList.add("drop-zone--over");
            else dropZone.classList.remove("drop-zone--over");
        });
    });

    dropZone.addEventListener("drop", (e) => {
        const file = e.dataTransfer.files[0];
        if (file && file.type === "application/pdf") {
            handleUpload(file);
        } else {
            alert("Please upload a PDF file.");
        }
    });

    async function handleUpload(file) {
        if (file.size > 100 * 1024 * 1024) {
            alert("File is too large (max 100MB).");
            return;
        }

        // UI Reset
        dropZone.classList.add("hidden");
        statusContainer.classList.remove("hidden");
        progressBar.style.width = "10%";
        statusText.innerText = "Uploading...";

        const formData = new FormData();
        formData.append("file", file);

        try {
            const response = await fetch("/upload", {
                method: "POST",
                body: formData
            });

            if (!response.ok) throw new Error("Upload failed");

            const data = await response.json();
            const fileId = data.file_id;

            progressBar.style.width = "30%";
            statusText.innerText = "Analyzing & Converting...";

            startPolling(fileId);
        } catch (err) {
            alert("An error occurred during upload.");
            resetUI();
        }
    }

    function startPolling(fileId) {
        let attempts = 0;
        const interval = setInterval(async () => {
            attempts++;
            try {
                const response = await fetch(`/download/${fileId}`, { method: "HEAD" });

                if (response.ok) {
                    clearInterval(interval);
                    showSuccess(fileId);
                } else {
                    // Gradual progress simulation for UX
                    let p = 30 + (attempts * 5);
                    if (p > 95) p = 95;
                    progressBar.style.width = p + "%";
                }
            } catch (e) {
                // Ignore silent errors during polling
            }

            if (attempts > 60) { // 2 minute timeout
                clearInterval(interval);
                alert("Conversion is taking longer than expected. Please check back later.");
                resetUI();
            }
        }, 2000);
    }

    function showSuccess(fileId) {
        statusContainer.classList.add("hidden");
        resultContainer.classList.remove("hidden");
        downloadBtn.href = `/download/${fileId}`;
    }

    resetBtn.addEventListener("click", resetUI);

    function resetUI() {
        dropZone.classList.remove("hidden");
        statusContainer.classList.add("hidden");
        resultContainer.classList.add("hidden");
        fileInput.value = "";
    }
});
