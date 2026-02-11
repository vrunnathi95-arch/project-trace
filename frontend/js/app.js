/* =========================
   UI HELPERS
========================= */

function toggleFilters() {
    document.getElementById("filterPanel").classList.toggle("hidden");
}

/* Collapse hero after search (Google-style) */
function collapseHero() {
    const hero = document.querySelector(".hero");
    if (hero) {
        hero.style.height = "auto";
        hero.style.padding = "40px 0 20px";
    }
}

/* =========================
   SEMANTIC SEARCH
========================= */

async function semanticSearch() {
    const queryInput = document.getElementById("query");
    const query = queryInput.value.trim();

    if (!query) {
        queryInput.focus();
        return;
    }

    const results = document.getElementById("results");
    const details = document.getElementById("documentDetails");

    details.innerHTML = "";
    results.innerHTML = `<div class="loading">● AI analyzing context...</div>`;

    collapseHero();

    const formData = new FormData();
    formData.append("query", query);

    try {
        const res = await fetch("http://127.0.0.1:8000/semantic-search", {
            method: "POST",
            body: formData
        });

        if (!res.ok) throw new Error("Search failed");

        const data = await res.json();
        results.innerHTML = "";

        if (data.length === 0) {
            results.innerHTML = `<div class="loading">No relevant documents found.</div>`;
            return;
        }

        data.forEach(d => {
            const card = document.createElement("div");
            card.className = "result-card";

            card.innerHTML = `
                <div class="result-title" onclick="loadDocumentDetails('${d.record_id}')">
                    ${d.document_title}
                </div>
                <div class="tag">${d.technique}</div>
                <div class="score">Relevance: ${d.score.toFixed(3)}</div>
            `;

            results.appendChild(card);
        });

        results.scrollIntoView({ behavior: "smooth" });

    } catch (err) {
        results.innerHTML = `
            <div class="loading" style="color:red;">
                Search failed. Please check server connection.
            </div>
        `;
        console.error(err);
    }
}

/* =========================
   DOCUMENT DETAILS
========================= */

async function loadDocumentDetails(recordId) {
    const details = document.getElementById("documentDetails");
    details.innerHTML = `<div class="loading">Loading document...</div>`;

    try {
        const res = await fetch(`http://127.0.0.1:8000/document/${recordId}`);
        if (!res.ok) throw new Error("Document fetch failed");

        const d = await res.json();

        details.innerHTML = `
            <h2>${d.document_title}</h2>
            <p><b>Project ID:</b> ${d.project_id}</p>
            <p><b>API:</b> ${d.product_api_name}</p>
            <p><b>Technique:</b> ${d.technique}</p>
            <p><b>Version:</b> ${d.version}</p>
            <p><b>Keywords:</b> ${d.keywords}</p>
            <p><b>Summary:</b><br>${d.summary}</p>
            <p><b>OCR Text:</b><br>${d.ocr_text}</p>
        `;

        details.scrollIntoView({ behavior: "smooth" });

    } catch (err) {
        details.innerHTML = `
            <div class="loading" style="color:red;">
                Failed to load document details.
            </div>
        `;
        console.error(err);
    }
}

/* =========================
   FILE UPLOAD (IMPROVED)
========================= */

document.getElementById("uploadFile")?.addEventListener("change", async function () {
    const file = this.files[0];
    if (!file) return;

    const uploadText = document.getElementById("uploadText");

    uploadText.innerText = "⏳ Uploading...";
    uploadText.style.opacity = "0.7";

    const formData = new FormData();
    formData.append("file", file);

    try {
        const response = await fetch("http://127.0.0.1:8000/upload", {
            method: "POST",
            body: formData
        });

        if (!response.ok) throw new Error("Upload failed");

        const result = await response.json();

        alert(
            `Upload successful!\nInserted: ${result.inserted_rows}\nUpdated: ${result.updated_rows}`
        );

        // Reset UI
        document.getElementById("results").innerHTML = "";
        document.getElementById("documentDetails").innerHTML = "";
        document.getElementById("query").focus();

    } catch (err) {
        console.error(err);
        alert("Upload failed. Please check file format or server.");
    } finally {
        uploadText.innerText = "⬆ Upload Data";
        uploadText.style.opacity = "1";
        this.value = "";
    }
});

