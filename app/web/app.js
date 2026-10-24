// LinguaStyle Studio Frontend JavaScript
document.addEventListener("DOMContentLoaded", () => {
  const API_BASE = "";

  // Elements
  const tabBtns = document.querySelectorAll(".tab-btn");
  const tabPanes = document.querySelectorAll(".tab-pane");
  const statTm = document.getElementById("stat-tm");
  const statGlossary = document.getElementById("stat-glossary");
  const btnSeed = document.getElementById("btn-seed");

  // Studio Elements
  const studioInput = document.getElementById("studio-input");
  const studioOutput = document.getElementById("studio-output");
  const studioBad = document.getElementById("studio-bad");
  const studioLang = document.getElementById("studio-lang");
  const studioThreshold = document.getElementById("studio-threshold");
  const thresholdVal = document.getElementById("threshold-val");
  const btnTranslate = document.getElementById("btn-translate");
  const btnApproveTm = document.getElementById("btn-approve-tm");
  const inspectorTmList = document.getElementById("inspector-tm-list");
  const inspectorGlossaryList = document.getElementById("inspector-glossary-list");
  const promptPreviewCode = document.getElementById("prompt-preview-code");
  const providerBadge = document.getElementById("provider-badge");

  // TM Elements
  const tmSearch = document.getElementById("tm-search");
  const tmTableBody = document.getElementById("tm-table-body");
  const btnAddTmModal = document.getElementById("btn-add-tm-modal");
  const tmFormCard = document.getElementById("tm-form-card");
  const btnSaveTm = document.getElementById("btn-save-tm");
  const btnCancelTm = document.getElementById("btn-cancel-tm");
  const tmInputSource = document.getElementById("tm-input-source");
  const tmInputTarget = document.getElementById("tm-input-target");
  const tmInputBad = document.getElementById("tm-input-bad");
  const tmInputCategory = document.getElementById("tm-input-category");
  const tmInputNotes = document.getElementById("tm-input-notes");

  // Glossary Elements
  const glossaryCards = document.getElementById("glossary-cards-container");
  const btnAddGlossaryModal = document.getElementById("btn-add-glossary-modal");
  const glossaryFormCard = document.getElementById("glossary-form-card");
  const btnSaveGlossary = document.getElementById("btn-save-glossary");
  const btnCancelGlossary = document.getElementById("btn-cancel-glossary");
  const glTerm = document.getElementById("gl-term");
  const glPreferred = document.getElementById("gl-preferred");
  const glAvoid = document.getElementById("gl-avoid");
  const glContext = document.getElementById("gl-context");

  // Document Elements
  const docRawText = document.getElementById("doc-raw-text");
  const btnSegment = document.getElementById("btn-segment");
  const docSegmentedResults = document.getElementById("doc-segmented-results");
  const segmentedList = document.getElementById("segmented-list");
  const sentenceCount = document.getElementById("sentence-count");

  // LoRA Elements
  const btnExportLora = document.getElementById("btn-export-lora");
  const loraFormat = document.getElementById("lora-format");
  const loraValSplit = document.getElementById("lora-val-split");
  const valSplitVal = document.getElementById("val-split-val");
  const loraStatSegments = document.getElementById("lora-stat-segments");
  const loraExportStatus = document.getElementById("lora-export-status");

  // --- TAB NAVIGATION ---
  tabBtns.forEach(btn => {
    btn.addEventListener("click", () => {
      const target = btn.dataset.tab;
      tabBtns.forEach(b => b.classList.remove("active"));
      tabPanes.forEach(p => p.classList.remove("active"));
      btn.classList.add("active");
      document.getElementById(`tab-${target}`).classList.add("active");
    });
  });

  // Threshold slider display
  studioThreshold.addEventListener("input", (e) => {
    thresholdVal.textContent = e.target.value;
  });
  loraValSplit.addEventListener("input", (e) => {
    valSplitVal.textContent = `${Math.round(e.target.value * 100)}% Validation`;
  });

  // --- API CALLS ---
  async function fetchStatus() {
    try {
      const res = await fetch(`${API_BASE}/api/status`);
      const data = await res.json();
      statTm.textContent = data.tm_segments_count;
      statGlossary.textContent = data.glossary_terms_count;
      loraStatSegments.textContent = data.tm_segments_count;
    } catch (e) {
      console.error("Status fetch failed:", e);
    }
  }

  async function loadTm(search = "") {
    try {
      const res = await fetch(`${API_BASE}/api/tm?q=${encodeURIComponent(search)}`);
      const data = await res.json();
      renderTmTable(data);
    } catch (e) {
      tmTableBody.innerHTML = `<tr><td colspan="4" class="text-center">Error loading TM</td></tr>`;
    }
  }

  function renderTmTable(items) {
    if (!items || items.length === 0) {
      tmTableBody.innerHTML = `<tr><td colspan="4" class="text-center" style="color:var(--text-muted); padding:30px;">No translation memory pairs found. Click "+ Add New Pair" or "Load Demo Data".</td></tr>`;
      return;
    }
    tmTableBody.innerHTML = items.map(item => `
      <tr>
        <td><strong>${escapeHtml(item.source)}</strong></td>
        <td style="color:#38bdf8;">${escapeHtml(item.target)}</td>
        <td style="color:var(--accent-red); font-size:12px;">${item.bad_literal ? escapeHtml(item.bad_literal) : '<span style="color:var(--text-muted)">—</span>'}</td>
        <td>
          <button class="btn btn-sm btn-secondary" onclick="useInStudio('${escapeJs(item.source)}')">Use</button>
          <button class="btn btn-sm btn-danger" onclick="deleteTm('${item.id}')">Delete</button>
        </td>
      </tr>
    `).join("");
  }

  async function loadGlossary() {
    try {
      const res = await fetch(`${API_BASE}/api/glossary`);
      const data = await res.json();
      renderGlossary(data);
    } catch (e) {
      glossaryCards.innerHTML = `<p>Error loading glossary</p>`;
    }
  }

  function renderGlossary(items) {
    if (!items || items.length === 0) {
      glossaryCards.innerHTML = `<p style="grid-column: 1/-1; text-align:center; color:var(--text-muted); padding:40px;">No glossary terms registered. Click "+ Add New Term" to define vocabulary rules.</p>`;
      return;
    }
    glossaryCards.innerHTML = items.map(item => `
      <div class="glossary-card">
        <div>
          <div class="gl-title">${escapeHtml(item.term)}</div>
          <div class="gl-pref">➔ ${escapeHtml(item.preferred)}</div>
          ${item.avoid_terms && item.avoid_terms.length ? `<div class="gl-avoid">🚫 Avoid: ${escapeHtml(item.avoid_terms.join(", "))}</div>` : ""}
          ${item.context_notes ? `<div class="gl-context">💡 ${escapeHtml(item.context_notes)}</div>` : ""}
        </div>
        <div style="margin-top:12px; display:flex; justify-content:flex-end;">
          <button class="btn btn-sm btn-danger" onclick="deleteGlossary('${escapeJs(item.term)}')">Delete</button>
        </div>
      </div>
    `).join("");
  }

  // --- TRANSLATION STUDIO & RAG ---
  btnTranslate.addEventListener("click", async () => {
    const text = studioInput.value.trim();
    if (!text) return alert("Please enter text to translate.");

    btnTranslate.disabled = true;
    btnTranslate.textContent = "🔍 Retrieving Style Memory & Translating...";

    try {
      const res = await fetch(`${API_BASE}/api/translate/preview`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: jsonBody({
          source_text: text,
          target_language: studioLang.value,
          threshold: parseFloat(studioThreshold.value),
          top_k: 3
        })
      });
      const data = await res.json();

      // Display Translation
      studioOutput.value = data.translation_result.translation;
      providerBadge.textContent = `${data.translation_result.provider} (${data.translation_result.model})`;

      // Render RAG TM Matches
      if (data.tm_matches && data.tm_matches.length > 0) {
        inspectorTmList.innerHTML = data.tm_matches.map(m => `
          <div class="mini-item">
            <div><strong>[Match ${Math.round(m.similarity * 100)}%]</strong> "${escapeHtml(m.source)}"</div>
            <div style="color:#38bdf8; margin-top:2px;">➔ "${escapeHtml(m.target)}"</div>
            ${m.bad_literal ? `<div style="color:var(--accent-red); font-size:11px;">Avoid: "${escapeHtml(m.bad_literal)}"</div>` : ""}
          </div>
        `).join("");
      } else {
        inspectorTmList.innerHTML = `<p class="placeholder-text">No similar TM segments above threshold (${studioThreshold.value}). Translating with general style guidelines.</p>`;
      }

      // Render Glossary Matches
      if (data.glossary_matches && data.glossary_matches.length > 0) {
        inspectorGlossaryList.innerHTML = data.glossary_matches.map(g => `
          <div class="mini-item glossary">
            <div><strong>"${escapeHtml(g.term)}"</strong> ➔ <span style="color:var(--accent-green);">${escapeHtml(g.preferred)}</span></div>
            ${g.avoid_terms && g.avoid_terms.length ? `<div style="color:var(--accent-red); font-size:11px;">Forbidden: ${escapeHtml(g.avoid_terms.join(", "))}</div>` : ""}
            ${g.context_notes ? `<div style="color:var(--text-muted); font-size:11px;">Guidance: ${escapeHtml(g.context_notes)}</div>` : ""}
          </div>
        `).join("");
      } else {
        inspectorGlossaryList.innerHTML = `<p class="placeholder-text">No registered glossary terms found in this sentence.</p>`;
      }

      // Render Prompt Inspector
      promptPreviewCode.textContent = data.assembled_prompt.combined_prompt;

    } catch (e) {
      alert("Translation preview failed: " + e.message);
    } finally {
      btnTranslate.disabled = false;
      btnTranslate.textContent = "⚡ Translate with Your Style & RAG";
    }
  });

  // Approve & Save to TM
  btnApproveTm.addEventListener("click", async () => {
    const source = studioInput.value.trim();
    const target = studioOutput.value.trim();
    const badLiteral = studioBad.value.trim();
    if (!source || !target) return alert("Source and target translation are required.");

    try {
      const res = await fetch(`${API_BASE}/api/tm`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: jsonBody({
          source,
          target,
          bad_literal: badLiteral || null,
          category: "approved_studio"
        })
      });
      const data = await res.json();
      if (data.success) {
        alert("✅ Successfully added to Translation Memory with contrastive rules!");
        studioBad.value = "";
        fetchStatus();
        loadTm();
      }
    } catch (e) {
      alert("Failed to save to TM: " + e.message);
    }
  });

  // --- DOCUMENT SEGMENTATION ---
  btnSegment.addEventListener("click", async () => {
    const text = docRawText.value.trim();
    if (!text) return alert("Please paste text to segment.");

    try {
      const res = await fetch(`${API_BASE}/api/document/segment`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: jsonBody({ text })
      });
      const data = await res.json();
      sentenceCount.textContent = data.count;
      docSegmentedResults.classList.remove("hidden");

      segmentedList.innerHTML = data.sentences.map((s, idx) => `
        <div class="sentence-item">
          <span><strong>#${idx + 1}</strong> ${escapeHtml(s)}</span>
          <button class="btn btn-sm btn-primary" onclick="loadSentenceToStudio('${escapeJs(s)}')">Translate in Studio</button>
        </div>
      `).join("");
    } catch (e) {
      alert("Segmentation failed: " + e.message);
    }
  });

  // --- LORA EXPORT ---
  btnExportLora.addEventListener("click", async () => {
    btnExportLora.disabled = true;
    btnExportLora.textContent = "Generating Datasets...";
    try {
      const res = await fetch(`${API_BASE}/api/export/lora`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: jsonBody({
          format: loraFormat.value,
          val_split: parseFloat(loraValSplit.value)
        })
      });
      const data = await res.json();
      if (data.success) {
        const exp = data.export;
        loraExportStatus.classList.remove("hidden");
        loraExportStatus.innerHTML = `
          <strong>🎉 Datasets Successfully Generated!</strong><br>
          • Train file: <code>${exp.train_file}</code> (${exp.train_count} pairs)<br>
          • Validation file: <code>${exp.val_file}</code> (${exp.val_count} pairs)<br>
          • Training script: <code>${exp.training_script}</code><br>
          • Total Words: ${exp.stats.total_english_words} EN / ${exp.stats.total_hindi_words} HI (~${exp.stats.estimated_tokens} tokens)
        `;
      } else {
        alert(data.error || "Export failed");
      }
    } catch (e) {
      alert("Export failed: " + e.message);
    } finally {
      btnExportLora.disabled = false;
      btnExportLora.textContent = "🚀 Generate Fine-Tuning Datasets";
    }
  });

  // --- SEED DEMO DATA ---
  btnSeed.addEventListener("click", async () => {
    if (!confirm("Preload sample political economy translation memory pairs and glossary entries?")) return;
    try {
      const res = await fetch(`${API_BASE}/api/seed`, { method: "POST" });
      const data = await res.json();
      if (data.success) {
        alert(`Loaded ${data.tm_count} TM pairs and ${data.glossary_count} Glossary entries!`);
        fetchStatus();
        loadTm();
        loadGlossary();
      }
    } catch (e) {
      alert("Failed to seed: " + e.message);
    }
  });

  // --- MODALS / INLINE FORMS ---
  btnAddTmModal.addEventListener("click", () => tmFormCard.classList.toggle("hidden"));
  btnCancelTm.addEventListener("click", () => tmFormCard.classList.add("hidden"));
  btnSaveTm.addEventListener("click", async () => {
    const source = tmInputSource.value.trim();
    const target = tmInputTarget.value.trim();
    if (!source || !target) return alert("Source and target are required.");

    await fetch(`${API_BASE}/api/tm`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: jsonBody({
        source, target,
        bad_literal: tmInputBad.value.trim(),
        category: tmInputCategory.value.trim(),
        notes: tmInputNotes.value.trim()
      })
    });
    tmFormCard.classList.add("hidden");
    tmInputSource.value = "";
    tmInputTarget.value = "";
    tmInputBad.value = "";
    loadTm();
    fetchStatus();
  });

  btnAddGlossaryModal.addEventListener("click", () => glossaryFormCard.classList.toggle("hidden"));
  btnCancelGlossary.addEventListener("click", () => glossaryFormCard.classList.add("hidden"));
  btnSaveGlossary.addEventListener("click", async () => {
    const term = glTerm.value.trim();
    const preferred = glPreferred.value.trim();
    if (!term || !preferred) return alert("Term and preferred translation required.");

    const avoidTerms = glAvoid.value.split(",").map(s => s.trim()).filter(Boolean);
    await fetch(`${API_BASE}/api/glossary`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: jsonBody({
        term, preferred,
        avoid_terms: avoidTerms,
        context_notes: glContext.value.trim()
      })
    });
    glossaryFormCard.classList.add("hidden");
    glTerm.value = "";
    glPreferred.value = "";
    glAvoid.value = "";
    glContext.value = "";
    loadGlossary();
    fetchStatus();
  });

  tmSearch.addEventListener("input", (e) => loadTm(e.target.value));

  // --- GLOBAL HELPERS ---
  window.useInStudio = (src) => {
    studioInput.value = src;
    document.querySelector('[data-tab="studio"]').click();
  };
  window.loadSentenceToStudio = (src) => {
    studioInput.value = src;
    document.querySelector('[data-tab="studio"]').click();
    btnTranslate.click();
  };
  window.deleteTm = async (id) => {
    if (!confirm("Delete this translation memory pair?")) return;
    await fetch(`${API_BASE}/api/tm?id=${id}`, { method: "DELETE" });
    loadTm(tmSearch.value);
    fetchStatus();
  };
  window.deleteGlossary = async (term) => {
    if (!confirm(`Delete glossary term "${term}"?`)) return;
    await fetch(`${API_BASE}/api/glossary?term=${encodeURIComponent(term)}`, { method: "DELETE" });
    loadGlossary();
    fetchStatus();
  };

  function escapeHtml(str) {
    if (!str) return "";
    return str.replace(/&/g, "&amp;").replace(/</g, "&lt;").replace(/>/g, "&gt;").replace(/"/g, "&quot;");
  }
  function escapeJs(str) {
    if (!str) return "";
    return str.replace(/\\/g, "\\\\").replace(/'/g, "\\'").replace(/"/g, '\\"').replace(/\n/g, "\\n");
  }
  function jsonBody(obj) {
    return JSON.stringify(obj);
  }

  // Initial Load
  fetchStatus();
  loadTm();
  loadGlossary();
});
