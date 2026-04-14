/* ── i18n ──────────────────────────────────────────────────────────────────── */
const I18N = {
  en: {
    logoSub:              "Editorial Screening Decision Support System",
    uploadTitle:          "Submit Manuscript for Screening",
    uploadSubtitle:       "Upload a PDF manuscript to start the automated editorial screening process.",
    dropHere:             "Drop your manuscript here",
    dropOr:               "or click to select a PDF file",
    processingNote:       "This may take several minutes depending on the model configuration.",
    stepPreprocessing:    "Preprocessing",
    stepPreprocessingDesc:"Extracting text, tables, and figures from the manuscript PDF.",
    stepCriteria:         "Criterion Analysis",
    stepCriteriaDesc:     "Running six evaluation agents in sequence.",
    stepReport:           "Report Generation",
    stepReportDesc:       "Synthesising all agent results into a final editorial decision.",
    decisionLabel:        "Decision",
    verdictAccept:        "Accepted for Peer Review",
    verdictReject:        "Desk Reject",
    metricDuration:       "Total Duration",
    metricTokensIn:       "Input Tokens",
    metricTokensOut:      "Output Tokens",
    finalReport:          "Final Report",
    agentDetails:         "Agent Details",
    newSubmission:        "New Submission",
    noReport:             "No report was generated.",
    errorPrefix:          "An error occurred:",
    // Agent display names
    preprocessing_agent:  "Preprocessing",
    format_agent:         "Format & Structure",
    innovation_agent:     "Innovation",
    method_agent:         "Methodology",
    plagiarism_agent:     "Plagiarism",
    quality_agent:        "Quality",
    scopefit_agent:       "Scope Fit",
    report_agent:         "Report Generation",
    // Accordion metrics
    labelDuration:        "Duration",
    labelInputTokens:     "Input tokens",
    labelOutputTokens:    "Output tokens",
    labelRetries:         "Retries",
    // Agent-specific data labels
    labelTables:          "Tables extracted",
    labelImages:          "Images extracted",
    labelTitle:           "Manuscript title",
    labelTitleSim:        "Title similarity",
    labelAbstractSim:     "Abstract similarity",
    // Score badge
    labelScore:           "Score",
    // Format agent
    labelSections:        "Sections",
    labelFormattingDetails: "Formatting Details",
    secIntroduction:      "Introduction",
    secMethods:           "Methods",
    secResults:           "Results",
    secDiscussion:        "Discussion",
    secConclusion:        "Conclusion",
    secReferences:        "References",
    // Innovation agent
    labelInnovationStatement: "Innovation Statement",
    labelSearchQueries:   "Search Queries",
    labelRelatedPapers:   "Related Papers Found",
    labelSemanticScholar: "Semantic Scholar",
    labelArxiv:           "arXiv",
    // Method agent
    labelResearchQuestion: "Research Question",
    // Quality agent
    labelSharpImages:     "Sharp images",
    labelBlurryImages:    "Blurry images",
    labelImageQuality:    "Image Quality",
    labelReadabilityScores: "Readability Scores",
    labelFleschEase:      "Flesch Reading Ease",
    labelFKGrade:         "Flesch-Kincaid Grade",
    labelGunningFog:      "Gunning Fog",
    labelSMOG:            "SMOG Index",
    labelARI:             "Auto. Readability",
    labelColemanLiau:     "Coleman-Liau",
    // Scopefit agent
    labelNeighborPapers:  "Similar Journal Papers",
    // Plagiarism
    notImplemented:       "not yet implemented",
    // Quality — extra readability scores
    labelLinsear:         "Linsear Write",
    labelDaleChall:       "Dale-Chall",
    labelMcAlpine:        "McAlpine EFLAW",
    // Preprocessing — file links
    labelManuscriptFiles: "Manuscript Files",
    labelPreprocessedPdf: "Preprocessed PDF",
    labelManuscriptMd:    "Manuscript Markdown",
    labelExtractedImages: "Extracted Tables & Images",
    // Navigation
    backToOverview:       "Back to Overview",
    // Previous submissions
    previousTitle:        "Previous Submissions",
    previousEmpty:        "No previous submissions found.",
    previousAccept:       "Accept",
    previousReject:       "Reject",
    previousPending:      "Unknown",
    previousLoad:         "Load Results",
  },
  de: {
    logoSub:              "Editorial Screening Decision Support System",
    uploadTitle:          "Manuskript zur Prüfung einreichen",
    uploadSubtitle:       "Laden Sie ein PDF-Manuskript hoch, um den automatisierten redaktionellen Screening-Prozess zu starten.",
    dropHere:             "Manuskript hier ablegen",
    dropOr:               "oder klicken Sie, um eine PDF-Datei auszuwählen",
    processingNote:       "Dies kann je nach Modellkonfiguration mehrere Minuten dauern.",
    stepPreprocessing:    "Vorverarbeitung",
    stepPreprocessingDesc:"Text, Tabellen und Abbildungen aus dem Manuskript-PDF extrahieren.",
    stepCriteria:         "Kriterienanalyse",
    stepCriteriaDesc:     "Sechs Bewertungsagenten werden nacheinander ausgeführt.",
    stepReport:           "Berichterstellung",
    stepReportDesc:       "Agentenergebnisse werden zu einer finalen redaktionellen Entscheidung zusammengefasst.",
    decisionLabel:        "Entscheidung",
    verdictAccept:        "Zur Peer-Review-Weitergabe akzeptiert",
    verdictReject:        "Desk Reject",
    metricDuration:       "Gesamtdauer",
    metricTokensIn:       "Eingabe-Token",
    metricTokensOut:      "Ausgabe-Token",
    finalReport:          "Abschlussbericht",
    agentDetails:         "Agentendetails",
    newSubmission:        "Neue Einreichung",
    noReport:             "Kein Bericht wurde erstellt.",
    errorPrefix:          "Ein Fehler ist aufgetreten:",
    // Agent display names
    preprocessing_agent:  "Vorverarbeitung",
    format_agent:         "Format & Struktur",
    innovation_agent:     "Innovation",
    method_agent:         "Methodik",
    plagiarism_agent:     "Plagiat",
    quality_agent:        "Qualität",
    scopefit_agent:       "Themenbereich",
    report_agent:         "Berichterstellung",
    // Accordion metrics
    labelDuration:        "Dauer",
    labelInputTokens:     "Eingabe-Token",
    labelOutputTokens:    "Ausgabe-Token",
    labelRetries:         "Wiederholungen",
    // Agent-specific data labels
    labelTables:          "Extrahierte Tabellen",
    labelImages:          "Extrahierte Abbildungen",
    labelTitle:           "Manuskripttitel",
    labelTitleSim:        "Titelähnlichkeit",
    labelAbstractSim:     "Abstractähnlichkeit",
    // Score badge
    labelScore:           "Punktzahl",
    // Format agent
    labelSections:        "Abschnitte",
    labelFormattingDetails: "Formatierungsdetails",
    secIntroduction:      "Einleitung",
    secMethods:           "Methoden",
    secResults:           "Ergebnisse",
    secDiscussion:        "Diskussion",
    secConclusion:        "Fazit",
    secReferences:        "Literatur",
    // Innovation agent
    labelInnovationStatement: "Innovationsaussage",
    labelSearchQueries:   "Suchanfragen",
    labelRelatedPapers:   "Gefundene verwandte Arbeiten",
    labelSemanticScholar: "Semantic Scholar",
    labelArxiv:           "arXiv",
    // Method agent
    labelResearchQuestion: "Forschungsfrage",
    // Quality agent
    labelSharpImages:     "Scharfe Bilder",
    labelBlurryImages:    "Unscharfe Bilder",
    labelImageQuality:    "Bildqualität",
    labelReadabilityScores: "Lesbarkeitsscores",
    labelFleschEase:      "Flesch-Lesbarkeit",
    labelFKGrade:         "Flesch-Kincaid-Klassenstufe",
    labelGunningFog:      "Gunning Fog Index",
    labelSMOG:            "SMOG Index",
    labelARI:             "Auto. Lesbarkeitsindex",
    labelColemanLiau:     "Coleman-Liau",
    // Scopefit agent
    labelNeighborPapers:  "Ähnliche Journalarbeiten",
    // Plagiarism
    notImplemented:       "noch nicht implementiert",
    // Quality — extra readability scores
    labelLinsear:         "Linsear Write",
    labelDaleChall:       "Dale-Chall",
    labelMcAlpine:        "McAlpine EFLAW",
    // Preprocessing — file links
    labelManuscriptFiles: "Manuskript-Dateien",
    labelPreprocessedPdf: "Vorverarbeitetes PDF",
    labelManuscriptMd:    "Manuskript Markdown",
    labelExtractedImages: "Extrahierte Tabellen & Bilder",
    // Navigation
    backToOverview:       "Zur Übersicht",
    // Previous submissions
    previousTitle:        "Vorherige Einreichungen",
    previousEmpty:        "Keine vorherigen Einreichungen gefunden.",
    previousAccept:       "Akzeptiert",
    previousReject:       "Abgelehnt",
    previousPending:      "Unbekannt",
    previousLoad:         "Ergebnisse laden",
  },
};

/* ── Agent configuration ───────────────────────────────────────────────────── */
const CRITERION_AGENTS = [
  "scopefit_agent", "method_agent", "innovation_agent",
  "format_agent",   "quality_agent", "plagiarism_agent",
];
const ALL_AGENTS = ["preprocessing_agent", ...CRITERION_AGENTS, "report_agent"];

/* ── App state ─────────────────────────────────────────────────────────────── */
let lang      = "en";
let jobId     = null;
let es        = null;  // EventSource
let startTime = null;

// Per-agent runtime data
const agentData = {};
ALL_AGENTS.forEach(a => {
  agentData[a] = {
    status:       "pending",
    data:         null,
    duration:     0,
    inputTokens:  0,
    outputTokens: 0,
    retries:      0,
    errors:       [],
  };
});

let finalReport           = null;
let deskreject            = null;
let currentManuscriptName = null;
let manuscriptPaths       = { preprocessed: null, md: null, images: [] };

/* ── i18n helpers ──────────────────────────────────────────────────────────── */
function t(key) {
  return (I18N[lang] && I18N[lang][key] !== undefined) ? I18N[lang][key] : key;
}

function applyTranslations() {
  document.querySelectorAll("[data-i18n]").forEach(el => {
    const key = el.dataset.i18n;
    if (I18N[lang][key] !== undefined) el.textContent = I18N[lang][key];
  });
}

function setLang(newLang) {
  lang = newLang;
  document.getElementById("btn-en").classList.toggle("active", lang === "en");
  document.getElementById("btn-de").classList.toggle("active", lang === "de");
  applyTranslations();
  // Re-render dynamic sections that contain translated text
  renderAgentGrid();
  fetchPreviousManuscripts();
  if (deskreject !== null) renderResults();
}

/* ── Section navigation ────────────────────────────────────────────────────── */
function showSection(name) {
  ["upload", "processing", "results"].forEach(s => {
    const el = document.getElementById(`sec-${s}`);
    if (el) {
      el.classList.toggle("hidden", s !== name);
      if (s === name) {
        // Re-trigger animation
        el.style.animation = "none";
        el.offsetHeight;
        el.style.animation = "";
      }
    }
  });
}

/* ── Dropzone setup ────────────────────────────────────────────────────────── */
const dropzone = document.getElementById("dropzone");
const fileInput = document.getElementById("file-input");

dropzone.addEventListener("click", () => fileInput.click());

dropzone.addEventListener("dragover", e => {
  e.preventDefault();
  dropzone.classList.add("drag-over");
});
dropzone.addEventListener("dragleave", () => dropzone.classList.remove("drag-over"));
dropzone.addEventListener("drop", e => {
  e.preventDefault();
  dropzone.classList.remove("drag-over");
  const file = e.dataTransfer.files[0];
  if (file) handleFile(file);
});
fileInput.addEventListener("change", () => {
  if (fileInput.files[0]) handleFile(fileInput.files[0]);
});

function setUploadError(msg) {
  const el = document.getElementById("upload-error");
  el.textContent = msg;
  el.classList.toggle("hidden", !msg);
}

/* ── Upload & job start ────────────────────────────────────────────────────── */
async function handleFile(file) {
  setUploadError("");
  if (!file.name.toLowerCase().endsWith(".pdf")) {
    setUploadError("Only PDF files are accepted.");
    return;
  }

  // Switch to processing view immediately
  currentManuscriptName = file.name.replace(/\.pdf$/i, "");
  document.getElementById("proc-filename").textContent = file.name;
  showSection("processing");
  resetSteps();
  renderAgentGrid();

  const fd = new FormData();
  fd.append("file", file);

  try {
    const resp = await fetch("/api/upload", { method: "POST", body: fd });
    if (!resp.ok) {
      const err = await resp.json().catch(() => ({ detail: "Upload failed." }));
      throw new Error(err.detail || "Upload failed.");
    }
    const payload = await resp.json();
    jobId = payload.job_id;
    connectSSE(jobId);
  } catch (err) {
    showSection("upload");
    setUploadError(err.message);
  }
}

/* ── SSE connection ────────────────────────────────────────────────────────── */
function connectSSE(id) {
  es = new EventSource(`/api/stream/${id}`);
  es.onmessage = e => {
    try {
      handleEvent(JSON.parse(e.data));
    } catch (_) { /* ignore malformed frames */ }
  };
  es.onerror = () => {
    es.close();
    if (deskreject === null) {
      showProcError("Connection to server lost. Please check the terminal and try again.");
    }
  };
}

/* ── Event dispatcher ──────────────────────────────────────────────────────── */
function handleEvent(event) {
  switch (event.type) {
    case "started":
      startTime = Date.now();
      break;
    case "node_update":
      handleNodeUpdate(event.node, event.data);
      break;
    case "complete":
      es.close();
      onWorkflowComplete();
      break;
    case "error":
      es.close();
      showProcError(`${t("errorPrefix")} ${event.message}`);
      break;
  }
}

/* ── Node update handling ──────────────────────────────────────────────────── */
function handleNodeUpdate(node, data) {
  // 1. Extract AgentResult for this node (key matches node name in state)
  if (data[node] && typeof data[node] === "object" && data[node].status) {
    const r = data[node];
    agentData[node] = {
      status:       r.status       ?? "pending",
      data:         r.data         ?? null,
      duration:     r.duration     ?? 0,
      inputTokens:  r.input_tokens ?? 0,
      outputTokens: r.output_tokens?? 0,
      retries:      r.retries      ?? 0,
      errors:       r.error        ?? [],
    };
  }

  // 2. Capture global state fields (set by report_agent or orchestrator)
  if (data.deskreject   !== undefined && data.deskreject   !== null) deskreject  = data.deskreject;
  if (data.final_report !== undefined && data.final_report !== null) finalReport = data.final_report;

  // 3. Capture manuscript file paths (emitted by preprocessing_agent node)
  if (data.preprocessed_manuscript_path) manuscriptPaths.preprocessed = data.preprocessed_manuscript_path;
  if (data.md_manuscript_path)           manuscriptPaths.md            = data.md_manuscript_path;
  if (Array.isArray(data.images))        manuscriptPaths.images        = data.images;

  // 3. Drive the stepper via orchestrator workflow_step transitions
  if (node === "orchestrator") {
    const step = data.workflow_step;
    if (step === 1) {
      // Preprocessing starting
      setStepStatus("preprocessing", "running");
      agentData["preprocessing_agent"].status = "running";
    } else if (step === 2) {
      // Preprocessing done → criterion agents starting
      setStepStatus("preprocessing", "success");
      agentData["preprocessing_agent"].status = "success";
      setStepStatus("criteria", "running");
      CRITERION_AGENTS.forEach(a => {
        if (agentData[a].status === "pending") agentData[a].status = "running";
      });
    } else if (step === 3) {
      // All criterion agents done → report starting
      CRITERION_AGENTS.forEach(a => {
        if (!["success", "failed"].includes(agentData[a].status)) agentData[a].status = "success";
      });
      const anyFailed = CRITERION_AGENTS.some(a => agentData[a].status === "failed");
      setStepStatus("criteria", anyFailed ? "failed" : "success");
      setStepStatus("report", "running");
      agentData["report_agent"].status = "running";
    } else if (step >= 4) {
      setStepStatus("report", "success");
    }
  }

  // 4. Individual agent node completions
  if (node === "preprocessing_agent") {
    const s = agentData[node].status;
    setStepStatus("preprocessing", s === "success" ? "success" : s === "failed" ? "failed" : "running");
    const dur = agentData[node].duration;
    if (dur) setText("dur-preprocessing", formatDuration(dur));
  }

  if (CRITERION_AGENTS.includes(node)) {
    const allDone = CRITERION_AGENTS.every(a => ["success", "failed"].includes(agentData[a].status));
    if (allDone) {
      const anyFailed = CRITERION_AGENTS.some(a => agentData[a].status === "failed");
      setStepStatus("criteria", anyFailed ? "failed" : "success");
    }
  }

  if (node === "report_agent") {
    const s = agentData[node].status;
    if (s === "success") setStepStatus("report", "success");
    const dur = agentData[node].duration;
    if (dur) setText("dur-report", formatDuration(dur));
  }

  renderAgentGrid();
}

/* ── Workflow complete ─────────────────────────────────────────────────────── */
function onWorkflowComplete() {
  // Ensure all steps look finished
  setStepStatus("preprocessing", "success");
  const critFailed = CRITERION_AGENTS.some(a => agentData[a].status === "failed");
  setStepStatus("criteria", critFailed ? "failed" : "success");
  setStepStatus("report", agentData["report_agent"].status === "success" ? "success" : "failed");

  renderAgentGrid();

  // Compute total duration from client-side timer
  const elapsedSec = startTime ? (Date.now() - startTime) / 1000 : null;
  if (elapsedSec) setText("metric-duration", formatDuration(elapsedSec));

  // Sum tokens across all agents
  const totalIn  = ALL_AGENTS.reduce((s, a) => s + (agentData[a].inputTokens  || 0), 0);
  const totalOut = ALL_AGENTS.reduce((s, a) => s + (agentData[a].outputTokens || 0), 0);
  setText("metric-tokens-in",  totalIn.toLocaleString());
  setText("metric-tokens-out", totalOut.toLocaleString());

  renderResults();

  // Brief pause so the user sees the completed stepper before the results jump in
  setTimeout(() => showSection("results"), 600);
}

/* ── Step status helpers ───────────────────────────────────────────────────── */
function setStepStatus(stepId, status) {
  const el = document.getElementById(`step-${stepId}`);
  if (el) el.dataset.status = status;
}

/* ── Agent grid renderer ───────────────────────────────────────────────────── */
function renderAgentGrid() {
  const grid = document.getElementById("agent-grid");
  if (!grid) return;

  grid.innerHTML = CRITERION_AGENTS.map(a => {
    const s   = agentData[a].status;
    const dur = agentData[a].duration ? formatDuration(agentData[a].duration) : "";
    const iconHtml =
      s === "running" ? `<div class="agent-card-spinner"></div>` :
      s === "success" ? "✓" :
      s === "failed"  ? "✗" : "";

    return `
      <div class="agent-card" data-status="${s}">
        <div class="agent-card-icon">${iconHtml}</div>
        <div>
          <div class="agent-card-name">${t(a)}</div>
          ${dur ? `<div class="agent-card-dur">${dur}</div>` : ""}
        </div>
      </div>`;
  }).join("");
}

/* ── Results renderer ──────────────────────────────────────────────────────── */
function renderResults() {
  // Manuscript name heading
  setText("result-manuscript-name", currentManuscriptName || "");

  // Decision banner
  const banner  = document.getElementById("decision-banner");
  const iconEl  = document.getElementById("decision-icon");
  const verdict = document.getElementById("decision-verdict");

  if (deskreject === true) {
    banner.className        = "decision-banner reject";
    iconEl.textContent      = "✗";
    verdict.textContent     = t("verdictReject");
  } else if (deskreject === false) {
    banner.className        = "decision-banner accept";
    iconEl.textContent      = "✓";
    verdict.textContent     = t("verdictAccept");
  }

  // Final report text
  setText("final-report-text", finalReport || t("noReport"));

  // Build accordion
  const acc = document.getElementById("accordion");
  if (!acc) return;
  acc.innerHTML = ALL_AGENTS.map(buildAccordionItem).join("");

  // Wire up toggles
  acc.querySelectorAll(".accordion-trigger").forEach(btn => {
    btn.addEventListener("click", () => {
      btn.closest(".accordion-item").classList.toggle("open");
    });
  });
}

/* ── Accordion item builder ────────────────────────────────────────────────── */
function buildAccordionItem(agentName) {
  const d       = agentData[agentName];
  const status  = d.status;
  const dur     = d.duration ? formatDuration(d.duration) : "—";
  const inTok   = d.inputTokens  ? d.inputTokens.toLocaleString()  : null;
  const outTok  = d.outputTokens ? d.outputTokens.toLocaleString() : null;
  const baseName = t(agentName);
  const name = agentName === "plagiarism_agent"
    ? `${baseName} <span class="acc-not-impl">(${t("notImplemented")})</span>`
    : baseName;

  // Meta line shown next to the chevron
  const metaParts = [dur];
  if (inTok)          metaParts.push(`${inTok} / ${outTok} tok`);
  if (d.retries > 0)  metaParts.push(`${d.retries}× retry`);
  const meta = metaParts.join(" · ");

  // Score badge (criterion agents expose a numeric score 0–10)
  const score = d.data?.score;
  const scoreBadgeHtml = (score !== undefined && score !== null)
    ? `<span class="acc-score-badge ${score >= 8 ? 'good' : score >= 6 ? 'mid' : 'low'}">${score}/10</span>`
    : "";

  // Metrics block
  const metricsHtml = `
    <div class="acc-metrics">
      <span class="acc-metric-item"><strong>${dur}</strong> ${t("labelDuration")}</span>
      ${inTok  ? `<span class="acc-metric-item"><strong>${inTok}</strong>  ${t("labelInputTokens")}</span>`  : ""}
      ${outTok ? `<span class="acc-metric-item"><strong>${outTok}</strong> ${t("labelOutputTokens")}</span>` : ""}
      ${d.retries > 0 ? `<span class="acc-metric-item"><strong>${d.retries}</strong> ${t("labelRetries")}</span>` : ""}
    </div>`;

  // Report text (most agents store it under data.report)
  const report    = d.data?.report ?? "";
  const reportHtml = report
    ? `<div class="acc-report">${escapeHtml(report)}</div>`
    : "";

  // Agent-specific extra data
  const extraHtml = buildExtraData(agentName, d.data);

  // Error messages
  const errorsHtml = d.errors && d.errors.length
    ? `<div class="acc-errors">${d.errors.map(e =>
        `<div class="acc-error-item">${escapeHtml(String(e))}</div>`
      ).join("")}</div>`
    : "";

  return `
    <div class="accordion-item">
      <button class="accordion-trigger">
        <div class="acc-left">
          <span class="acc-dot ${status}"></span>
          <span class="acc-name">${name}</span>
        </div>
        <div class="acc-right">
          ${scoreBadgeHtml}
          <span class="acc-meta">${meta}</span>
          <span class="acc-chevron">▶</span>
        </div>
      </button>
      <div class="accordion-body">
        ${metricsHtml}
        ${reportHtml}
        ${extraHtml}
        ${errorsHtml}
      </div>
    </div>`;
}

/* ── Agent-specific extra data ─────────────────────────────────────────────── */
function buildExtraData(agentName, data) {
  if (!data) return "";
  const sections = [];

  // ── preprocessing_agent ──────────────────────────────────────────────────
  if (agentName === "preprocessing_agent") {
    // Stats
    const items = [];
    if (data.number_of_tables   !== undefined) items.push([t("labelTables"),  data.number_of_tables]);
    if (data.number_of_pictures !== undefined) items.push([t("labelImages"),  data.number_of_pictures]);
    if (items.length) sections.push(dataGridHtml(items));

    // File links
    const fileLinks = [];
    if (manuscriptPaths.preprocessed)
      fileLinks.push({ label: t("labelPreprocessedPdf"), url: pathToUrl(manuscriptPaths.preprocessed) });
    if (manuscriptPaths.md)
      fileLinks.push({ label: t("labelManuscriptMd"),    url: pathToUrl(manuscriptPaths.md) });
    if (fileLinks.length) {
      const linksHtml = fileLinks.map(f =>
        `<a class="acc-file-link" href="${f.url}" target="_blank" rel="noopener">${escapeHtml(f.label)}</a>`
      ).join("");
      sections.push(`
        <div class="acc-subsection">
          <div class="acc-subsection-title">${t("labelManuscriptFiles")}</div>
          <div class="acc-file-links">${linksHtml}</div>
        </div>`);
    }

    // Image / table thumbnails
    if (manuscriptPaths.images && manuscriptPaths.images.length) {
      const thumbs = manuscriptPaths.images.map(imgPath => {
        const url  = pathToUrl(imgPath);
        const name = imgPath.split("/").pop();
        return `<a class="acc-image-thumb" href="${url}" target="_blank" rel="noopener" title="${escapeHtml(name)}">
          <img src="${url}" alt="${escapeHtml(name)}" loading="lazy" />
          <span class="acc-image-label">${escapeHtml(name)}</span>
        </a>`;
      }).join("");
      sections.push(`
        <div class="acc-subsection">
          <div class="acc-subsection-title">${t("labelExtractedImages")}</div>
          <div class="acc-images-grid">${thumbs}</div>
        </div>`);
    }
  }

  // ── format_agent ─────────────────────────────────────────────────────────
  if (agentName === "format_agent") {
    const sc = data.section_check;
    if (sc) {
      const sectionKeys   = ["introduction","methods","results","discussion","conclusion","references"];
      const sectionLabels = ["Introduction","Methods","Results","Discussion","Conclusion","References"];
      const checks = sectionKeys.map((k, i) => {
        const ok = sc[k] === true;
        return `<div class="acc-check-item ${ok ? "present" : "absent"}">
          <span class="acc-check-icon">${ok ? "✓" : "✗"}</span>
          <span class="acc-check-label">${sectionLabels[i]}</span>
        </div>`;
      }).join("");
      const noteHtml = sc.section_report
        ? `<div class="acc-note">${escapeHtml(sc.section_report)}</div>` : "";
      sections.push(`
        <div class="acc-subsection">
          <div class="acc-subsection-title">${t("labelSections")}</div>
          <div class="acc-checklist">${checks}</div>
          ${noteHtml}
        </div>`);
    }
    if (data.formatting_check) {
      sections.push(`
        <div class="acc-subsection">
          <div class="acc-subsection-title">${t("labelFormattingDetails")}</div>
          <div class="acc-preblock">${escapeHtml(data.formatting_check)}</div>
        </div>`);
    }
  }

  // ── innovation_agent ──────────────────────────────────────────────────────
  if (agentName === "innovation_agent") {
    if (data.innovation_statement) {
      sections.push(`
        <div class="acc-subsection">
          <div class="acc-subsection-title">${t("labelInnovationStatement")}</div>
          <div class="acc-text-block">${escapeHtml(data.innovation_statement)}</div>
        </div>`);
    }
    if (data.search_queries?.length) {
      const pills = data.search_queries
        .map(q => `<span class="acc-pill">${escapeHtml(q)}</span>`).join("");
      sections.push(`
        <div class="acc-subsection">
          <div class="acc-subsection-title">${t("labelSearchQueries")}</div>
          <div class="acc-pill-row">${pills}</div>
        </div>`);
    }
    const ssResults = data.semantic_scholar_results ?? [];
    const axResults = data.arxiv_results ?? [];
    if (ssResults.length || axResults.length) {
      const renderPapers = (list) =>
        list.map(p => `<div class="acc-paper-item">${escapeHtml(p.title ?? "—")}</div>`).join("");
      let papersHtml = "";
      if (ssResults.length)
        papersHtml += `<div class="acc-papers-source">${t("labelSemanticScholar")} (${ssResults.length})</div>
          <div class="acc-papers-list">${renderPapers(ssResults)}</div>`;
      if (axResults.length)
        papersHtml += `<div class="acc-papers-source">${t("labelArxiv")} (${axResults.length})</div>
          <div class="acc-papers-list">${renderPapers(axResults)}</div>`;
      sections.push(`
        <div class="acc-subsection">
          <div class="acc-subsection-title">${t("labelRelatedPapers")}</div>
          ${papersHtml}
        </div>`);
    }
  }

  // ── method_agent ──────────────────────────────────────────────────────────
  if (agentName === "method_agent") {
    if (data.researchquestion) {
      sections.push(`
        <div class="acc-subsection">
          <div class="acc-subsection-title">${t("labelResearchQuestion")}</div>
          <div class="acc-text-block">${escapeHtml(data.researchquestion)}</div>
        </div>`);
    }
  }

  // ── quality_agent ─────────────────────────────────────────────────────────
  if (agentName === "quality_agent") {
    if (data.imagequality) {
      const m = data.imagequality.match(/(\d+) sharp images? and (\d+) blurry/);
      if (m) {
        sections.push(`
          <div class="acc-subsection">
            <div class="acc-subsection-title">${t("labelImageQuality")}</div>
            ${dataGridHtml([
              [t("labelSharpImages"),  parseInt(m[1])],
              [t("labelBlurryImages"), parseInt(m[2])],
            ])}
          </div>`);
      }
    }
    const tq = data.textquality;
    if (tq) {
      const flesch = tq.flesch_reading_ease;
      const fleschCls = flesch >= 60 ? "score-good" : flesch >= 30 ? "score-mid" : "score-low";
      const scores = [
        [t("labelFleschEase"), flesch,                             fleschCls],
        [t("labelFKGrade"),    tq.flesch_kincaid_grade,            ""],
        [t("labelGunningFog"), tq.gunning_fog,                     ""],
        [t("labelSMOG"),       tq.smog_index,                      ""],
        [t("labelARI"),        tq.automated_readability_index,     ""],
        [t("labelColemanLiau"),tq.coleman_liau_index,              ""],
        [t("labelLinsear"),    tq.linsear_write_formula,           ""],
        [t("labelDaleChall"),  tq.dale_chall_readability_score,    ""],
        [t("labelMcAlpine"),   tq.mcalpine_eflaw,                  ""],
      ].filter(([, v]) => v !== undefined && v !== null);

      const grid = scores.map(([label, value, cls]) => `
        <div class="acc-readability-item ${cls}">
          <div class="acc-data-label">${label}</div>
          <div class="acc-data-value">${Number(value).toFixed(1)}</div>
        </div>`).join("");
      sections.push(`
        <div class="acc-subsection">
          <div class="acc-subsection-title">${t("labelReadabilityScores")}</div>
          <div class="acc-readability-grid">${grid}</div>
        </div>`);
    }
  }

  // ── scopefit_agent ────────────────────────────────────────────────────────
  if (agentName === "scopefit_agent") {
    const simItems = [];
    const title = data.manuscript_data?.title;
    if (title) simItems.push([t("labelTitle"), title]);
    if (data.title_cs_median    !== undefined)
      simItems.push([t("labelTitleSim"),    `${(data.title_cs_median    * 100).toFixed(1)} %`]);
    if (data.abstract_cs_median !== undefined)
      simItems.push([t("labelAbstractSim"), `${(data.abstract_cs_median * 100).toFixed(1)} %`]);
    if (simItems.length) sections.push(dataGridHtml(simItems));

    if (data.neighbor_info) {
      const neighbors = data.neighbor_info.trim().split("\n")
        .map(line => { const m = line.match(/^(.*?)\s*-\s*Score=([\d.]+)$/); return m ? { title: m[1].trim(), score: parseFloat(m[2]) } : null; })
        .filter(Boolean);
      if (neighbors.length) {
        const items = neighbors.map(n => `
          <div class="acc-neighbor-item">
            <span class="acc-neighbor-title">${escapeHtml(n.title)}</span>
            <span class="acc-neighbor-score">${(n.score * 100).toFixed(0)}%</span>
          </div>`).join("");
        sections.push(`
          <div class="acc-subsection">
            <div class="acc-subsection-title">${t("labelNeighborPapers")}</div>
            <div class="acc-neighbors-list">${items}</div>
          </div>`);
      }
    }
  }

  return sections.join("");
}

/* ── Path → URL helper ─────────────────────────────────────────────────────── */
function pathToUrl(filePath) {
  if (!filePath) return "#";
  // "data/some folder/file.png" → "/data/some%20folder/file.png"
  return "/" + filePath.split("/").map(encodeURIComponent).join("/");
}

/* ── data-grid helper ──────────────────────────────────────────────────────── */
function dataGridHtml(items) {
  return `<div class="acc-data-grid">${items.map(([label, value]) => `
    <div class="acc-data-item">
      <div class="acc-data-label">${label}</div>
      <div class="acc-data-value">${escapeHtml(String(value))}</div>
    </div>`).join("")}</div>`;
}

/* ── Error display ─────────────────────────────────────────────────────────── */
function showProcError(msg) {
  const el = document.getElementById("proc-error");
  if (!el) return;
  el.textContent = msg;
  el.classList.remove("hidden");
}

/* ── Reset ─────────────────────────────────────────────────────────────────── */
function resetSteps() {
  ["preprocessing", "criteria", "report"].forEach(id => setStepStatus(id, "pending"));
  setText("dur-preprocessing", "");
  setText("dur-report", "");
  document.getElementById("proc-error")?.classList.add("hidden");
}

function resetToUpload() {
  // Close any open SSE connection
  if (es) { es.close(); es = null; }

  // Clear state
  jobId                 = null;
  startTime             = null;
  finalReport           = null;
  deskreject            = null;
  currentManuscriptName = null;
  manuscriptPaths       = { preprocessed: null, md: null, images: [] };
  ALL_AGENTS.forEach(a => {
    agentData[a] = { status: "pending", data: null, duration: 0,
                     inputTokens: 0, outputTokens: 0, retries: 0, errors: [] };
  });

  // Reset file input so the same file can be re-selected
  document.getElementById("file-input").value = "";
  setUploadError("");
  resetSteps();
  fetchPreviousManuscripts();

  showSection("upload");
}

/* ── Utilities ─────────────────────────────────────────────────────────────── */
function formatDuration(seconds) {
  if (seconds < 60) return `${seconds.toFixed(1)}s`;
  const m = Math.floor(seconds / 60);
  const s = Math.round(seconds % 60);
  return `${m}m ${s}s`;
}

function setText(id, text) {
  const el = document.getElementById(id);
  if (el) el.textContent = text;
}

function escapeHtml(str) {
  return str
    .replace(/&/g, "&amp;")
    .replace(/</g, "&lt;")
    .replace(/>/g, "&gt;")
    .replace(/"/g, "&quot;");
}

/* ── Previous submissions ──────────────────────────────────────────────────── */
async function fetchPreviousManuscripts() {
  try {
    const resp = await fetch("/api/manuscripts");
    if (!resp.ok) return;
    const list = await resp.json();
    renderPreviousManuscripts(list);
  } catch (_) { /* silently ignore — not critical */ }
}

function renderPreviousManuscripts(list) {
  const section = document.getElementById("previous-section");
  const container = document.getElementById("previous-list");
  if (!section || !container) return;

  if (!list.length) {
    section.classList.add("hidden");
    return;
  }

  section.classList.remove("hidden");

  // Also update the section title (for language switching)
  const titleEl = section.querySelector(".previous-title");
  if (titleEl) titleEl.textContent = t("previousTitle");

  container.innerHTML = list.map(item => {
    const name = item.m_id;
    const dr   = item.deskreject;
    const decisionClass = dr === true ? "reject" : dr === false ? "accept" : "pending";
    const decisionLabel = dr === true ? t("previousReject") : dr === false ? t("previousAccept") : t("previousPending");

    // Derive a human-readable short name from the original path or m_id
    const displayName = item.original_path
      ? decodeURIComponent(item.original_path.split("/").pop().replace(/\.pdf$/i, ""))
      : name;

    return `
      <div class="prev-item">
        <div class="prev-item-icon">
          <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor"
               stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
            <path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z"/>
            <polyline points="14 2 14 8 20 8"/>
          </svg>
        </div>
        <span class="prev-item-name" title="${escapeHtml(displayName)}">${escapeHtml(displayName)}</span>
        <span class="prev-decision-badge ${decisionClass}">${decisionLabel}</span>
        <button class="prev-load-btn" data-mid="${escapeHtml(name)}">${t("previousLoad")} →</button>
      </div>`;
  }).join("");

  // Wire up load buttons (avoids inline-onclick quoting issues with special chars)
  container.querySelectorAll(".prev-load-btn").forEach(btn => {
    btn.addEventListener("click", () => loadPreviousManuscript(btn.dataset.mid));
  });
}

async function loadPreviousManuscript(mId) {
  setUploadError("");
  try {
    const resp = await fetch(`/api/manuscripts/${encodeURIComponent(mId)}`);
    if (!resp.ok) throw new Error(`Could not load results for "${mId}".`);
    const state = await resp.json();

    // Reset agent data then populate from stored state
    ALL_AGENTS.forEach(a => {
      agentData[a] = { status: "pending", data: null, duration: 0,
                       inputTokens: 0, outputTokens: 0, retries: 0, errors: [] };
    });

    ALL_AGENTS.forEach(a => {
      const r = state[a];
      if (!r) return;
      agentData[a] = {
        status:       r.status        ?? "pending",
        data:         r.data          ?? null,
        duration:     r.duration      ?? 0,
        inputTokens:  r.input_tokens  ?? 0,
        outputTokens: r.output_tokens ?? 0,
        retries:      r.retries       ?? 0,
        errors:       r.error         ?? [],
      };
    });

    finalReport           = state.final_report ?? null;
    deskreject            = state.deskreject   ?? null;
    currentManuscriptName = mId;
    manuscriptPaths = {
      preprocessed: state.preprocessed_manuscript_path ?? null,
      md:           state.md_manuscript_path           ?? null,
      images:       state.images                       ?? [],
    };

    // Compute metrics from stored per-agent values
    const totalIn  = ALL_AGENTS.reduce((s, a) => s + (agentData[a].inputTokens  || 0), 0);
    const totalOut = ALL_AGENTS.reduce((s, a) => s + (agentData[a].outputTokens || 0), 0);
    const totalDur = ALL_AGENTS.reduce((s, a) => s + (agentData[a].duration     || 0), 0);

    setText("metric-duration",   totalDur > 0 ? formatDuration(totalDur) : "—");
    setText("metric-tokens-in",  totalIn  > 0 ? totalIn.toLocaleString()  : "—");
    setText("metric-tokens-out", totalOut > 0 ? totalOut.toLocaleString() : "—");

    renderResults();
    showSection("results");
  } catch (err) {
    setUploadError(err.message);
  }
}

/* ── Init ──────────────────────────────────────────────────────────────────── */
document.addEventListener("DOMContentLoaded", () => {
  applyTranslations();
  renderAgentGrid();
  fetchPreviousManuscripts();
});
