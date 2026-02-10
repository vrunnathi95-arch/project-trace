function toggleFilters() {
    document.getElementById("filterPanel").classList.toggle("hidden");
}

async function semanticSearch() {
    const query = document.getElementById("query").value.trim();
    if (!query) return;

    const results = document.getElementById("results");
    const details = document.getElementById("documentDetails");

    details.innerHTML = "";
    results.innerHTML = `<div class="loading">● AI analyzing context...</div>`;

    const formData = new FormData();
    formData.append("query", query);

    const res = await fetch("http://127.0.0.1:8000/semantic-search", {
        method: "POST",
        body: formData
    });

    const data = await res.json();
    results.innerHTML = "";

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
}

async function loadDocumentDetails(recordId) {
    const res = await fetch(`http://127.0.0.1:8000/document/${recordId}`);
    const d = await res.json();

    document.getElementById("documentDetails").innerHTML = `
        <h2>${d.document_title}</h2>
        <p><b>Project ID:</b> ${d.project_id}</p>
        <p><b>API:</b> ${d.product_api_name}</p>
        <p><b>Technique:</b> ${d.technique}</p>
        <p><b>Version:</b> ${d.version}</p>
        <p><b>Keywords:</b> ${d.keywords}</p>
        <p><b>Summary:</b><br>${d.summary}</p>
        <p><b>OCR Text:</b><br>${d.ocr_text}</p>
    `;

    document.getElementById("documentDetails")
        .scrollIntoView({ behavior: "smooth" });
}
