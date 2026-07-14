/* =========================================================================
   H. Vosteen Research — site renderer (academic redesign)
   Reads data/papers.json + data/goodies.json (same workflow as AGENTS.md),
   renders into the new schlank layout with:
     · SSRN featured section (top, oxblood accent)
     · Topic filter (live)
     · Year-grouped working papers & essays (sticky year headers)
     · Search (title + abstract + tags)
     · Click any entry to expand abstract + actions
     · BibTeX cite copy
     · Goodie lightbox
   ========================================================================= */

(() => {
  const state = {
    papers: [],
    filtered: [],
    activeTag: null,
    query: "",
    sort: "date-desc",
  };

  const els = {
    list: document.getElementById("paper-list"),
    ssrnList: document.getElementById("ssrn-list"),
    ssrnSection: document.getElementById("ssrn-section"),
    empty: document.getElementById("empty-state"),
    search: document.getElementById("search"),
    sort: document.getElementById("sort"),
    topics: document.getElementById("topics-filter"),
    paperTpl: document.getElementById("paper-template"),
    ssrnTpl: document.getElementById("ssrn-template"),
    yearTpl: document.getElementById("year-template"),
    goodiesGrid: document.getElementById("goodies-grid"),
    goodieTpl: document.getElementById("goodie-template"),
    year: document.getElementById("year"),
  };

  if (els.year) els.year.textContent = new Date().getFullYear();

  // ---------- formatters ----------

  const monthShort = (iso) => {
    if (!iso) return "";
    const d = new Date(iso);
    if (Number.isNaN(d.getTime())) return iso;
    return d.toLocaleDateString("en-US", { month: "short", day: "numeric" });
  };
  const fullDate = (iso) => {
    if (!iso) return "";
    const d = new Date(iso);
    if (Number.isNaN(d.getTime())) return iso;
    return d.toLocaleDateString("en-US", { year: "numeric", month: "short", day: "numeric" });
  };

  const kindLabel = (p) => {
    if (p.type === "ssrn") return "SSRN";
    if (p.type === "essay") return "Essay";
    return "Paper";
  };

  // ---------- BibTeX ----------

  const buildBibtex = (p) => {
    const key =
      p.bibkey ||
      `vosteen${(p.date || "").slice(0, 4)}${(p.slug || p.title || "")
        .toLowerCase()
        .replace(/[^a-z0-9]+/g, "")
        .slice(0, 12)}`;
    const authors = Array.isArray(p.authors)
      ? p.authors.join(" and ")
      : p.authors || "Vosteen, H.";
    const year = (p.date || "").slice(0, 4);
    const canonical = `https://hakvinv.github.io/H.Vosteen-Research-/concepts/${p.slug}/`;
    return [
      `@techreport{${key},`,
      `  title       = {${p.title || ""}},`,
      `  author      = {${authors}},`,
      `  year        = {${year}},`,
      `  institution = {H. Vosteen Research},`,
      `  url         = {${canonical}},`,
      `  note        = {${p.concept_id || "H. Vosteen Research"}; canonical record}`,
      `}`,
    ].filter(Boolean).join("\n");
  };

  // ---------- card builder ----------

  const buildCard = (paper, { featured = false } = {}) => {
    const tpl = featured ? els.ssrnTpl : els.paperTpl;
    const node = tpl.content.firstElementChild.cloneNode(true);
    if (featured) node.dataset.ssrn = "true";
    if (paper.slug) node.id = `paper-${paper.slug}`;
    if (paper.concept_id) node.dataset.conceptId = paper.concept_id;
    if (paper.provenance_token) node.dataset.provenanceToken = paper.provenance_token;

    // title
    const titleEl = node.querySelector(".paper-title");
    // remove existing kind/version/venue spans inside
    titleEl.querySelectorAll(".paper-kind, .paper-version, .paper-venue").forEach((el) => el.remove());

    // title text + appended labels
    const titleText = document.createTextNode((paper.title || "Untitled") + " ");
    titleEl.insertBefore(titleText, titleEl.firstChild);

    if (paper.type === "ssrn") {
      const venue = document.createElement("span");
      venue.className = "paper-venue";
      venue.textContent = "SSRN";
      titleEl.appendChild(venue);
    } else {
      const kind = document.createElement("span");
      kind.className = "paper-kind";
      kind.textContent = kindLabel(paper);
      titleEl.appendChild(kind);
    }
    if (paper.version) {
      const v = document.createElement("span");
      v.className = "paper-version";
      v.textContent = "v" + paper.version;
      titleEl.appendChild(v);
    }

    // date
    const dateEl = node.querySelector(".paper-date");
    dateEl.dateTime = paper.date || "";
    dateEl.textContent = featured ? fullDate(paper.date) : monthShort(paper.date);

    // authors
    const authorsEl = node.querySelector(".paper-authors");
    if (authorsEl) {
      authorsEl.textContent = Array.isArray(paper.authors)
        ? paper.authors.join(", ")
        : (paper.authors || "Hakvin Vosteen");
      if (paper.concept_id) {
        const concept = document.createElement("span");
        concept.className = "concept-id";
        concept.textContent = paper.concept_id;
        authorsEl.append(" · ", concept);
      }
    }

    // abstract
    const absEl = node.querySelector(".paper-abstract");
    if (absEl) {
      if (paper.abstract) absEl.textContent = paper.abstract;
      else absEl.remove();
    }

    // actions
    const actionsEl = node.querySelector(".paper-actions");
    if (actionsEl) {
      const actions = [];
      if (paper.slug) {
        actions.push({ label: "Canonical record", url: `concepts/${paper.slug}/` });
      }
      if (paper.file) {
        actions.push({ label: "Download PDF", url: paper.file, download: true });
        actions.push({ label: "View online",  url: paper.file, external: true });
      }
      (paper.links || []).forEach((link) => {
        if (link && link.url && link.label) actions.push({ label: link.label, url: link.url, external: true });
      });
      actionsEl.innerHTML = "";
      actions.forEach(({ label, url, download, external }) => {
        const a = document.createElement("a");
        a.href = url;
        if (download) a.setAttribute("download", "");
        if (external && !download) { a.target = "_blank"; a.rel = "noopener"; }
        a.textContent = label;
        actionsEl.appendChild(a);
      });
      // Cite button
      const cite = document.createElement("button");
      cite.type = "button";
      cite.className = "paper-cite";
      cite.textContent = "Cite";
      cite.style.cssText = "background:transparent;border:none;border-bottom:1px solid currentColor;color:inherit;font:inherit;cursor:pointer;padding:0;";
      actionsEl.appendChild(cite);

      cite.addEventListener("click", (e) => {
        e.preventDefault();
        const existing = node.querySelector(".paper-bibtex");
        if (existing) { existing.remove(); cite.textContent = "Cite"; return; }
        const pre = document.createElement("pre");
        pre.className = "paper-bibtex";
        pre.textContent = buildBibtex(paper);
        actionsEl.parentNode.appendChild(pre);
        cite.textContent = "Hide BibTeX";
        if (navigator.clipboard) navigator.clipboard.writeText(pre.textContent).catch(() => {});
      });
    }

    // tags
    const tagsEl = node.querySelector(".paper-tags");
    if (tagsEl) {
      tagsEl.innerHTML = "";
      (paper.tags || []).forEach((t) => {
        const li = document.createElement("li");
        li.textContent = t;
        tagsEl.appendChild(li);
      });
      if (!(paper.tags || []).length) tagsEl.remove();
    }

    return node;
  };

  // ---------- render ----------

  const groupByYear = (list) => {
    const groups = new Map();
    list.forEach((p) => {
      const y = (p.date || "").slice(0, 4) || "—";
      if (!groups.has(y)) groups.set(y, []);
      groups.get(y).push(p);
    });
    return [...groups.entries()].sort((a, b) => b[0].localeCompare(a[0]));
  };

  const renderTopics = () => {
    if (!els.topics) return;
    const counts = new Map();
    state.papers.forEach((p) => {
      if (p.draft) return;
      (p.tags || []).forEach((t) => counts.set(t, (counts.get(t) || 0) + 1));
    });
    const sorted = [...counts.entries()].sort((a, b) => b[1] - a[1]).slice(0, 8);

    // clear existing buttons (keep .lbl)
    els.topics.querySelectorAll("button.tag-chip").forEach((b) => b.remove());
    const search = els.topics.querySelector(".search");

    const make = (label, count, tag) => {
      const b = document.createElement("button");
      b.type = "button";
      b.className = "tag-chip" + (state.activeTag === tag ? " active" : "");
      b.innerHTML = `${label}${count != null ? `<span class="n">${count}</span>` : ""}`;
      b.addEventListener("click", () => {
        state.activeTag = state.activeTag === tag ? null : tag;
        renderTopics();
        applyFilters();
      });
      return b;
    };

    const totalActive = state.papers.filter((p) => !p.draft).length;
    const allBtn = make("all", totalActive, null);
    if (!state.activeTag) allBtn.classList.add("active");
    if (search) els.topics.insertBefore(allBtn, search); else els.topics.appendChild(allBtn);
    sorted.forEach(([tag, n]) => {
      const b = make(tag, n, tag);
      if (search) els.topics.insertBefore(b, search); else els.topics.appendChild(b);
    });
  };

  const render = () => {
    // SSRN featured
    const ssrn = state.filtered.filter((p) => p.type === "ssrn");
    if (els.ssrnList) {
      els.ssrnList.innerHTML = "";
      if (ssrn.length) {
        els.ssrnSection.hidden = false;
        ssrn.forEach((p) => els.ssrnList.appendChild(buildCard(p, { featured: true })));
      } else if (els.ssrnSection) {
        els.ssrnSection.hidden = true;
      }
    }

    // The rest by year
    const others = state.filtered.filter((p) => p.type !== "ssrn");
    els.list.innerHTML = "";

    if (!others.length && !ssrn.length) {
      els.empty.hidden = false;
      return;
    }
    els.empty.hidden = true;

    const groups = groupByYear(others);
    const frag = document.createDocumentFragment();
    for (const [year, papers] of groups) {
      const header = els.yearTpl.content.firstElementChild.cloneNode(true);
      header.querySelector("h3").textContent = year;
      header.querySelector(".ycount").textContent =
        `${papers.length} ${papers.length === 1 ? "entry" : "entries"}`;
      frag.appendChild(header);
      papers.forEach((p) => frag.appendChild(buildCard(p)));
    }
    els.list.appendChild(frag);
  };

  const applyFilters = () => {
    const q = state.query.trim().toLowerCase();
    let list = state.papers.filter((p) => {
      if (p.draft) return false;
      if (state.activeTag && !(p.tags || []).includes(state.activeTag)) return false;
      if (!q) return true;
      const hay = [
        p.title,
        p.abstract,
        Array.isArray(p.authors) ? p.authors.join(" ") : p.authors,
        (p.tags || []).join(" "),
      ].filter(Boolean).join(" ").toLowerCase();
      return hay.includes(q);
    });

    list.sort((a, b) => {
      switch (state.sort) {
        case "date-asc":  return (a.date || "").localeCompare(b.date || "");
        case "title-asc": return (a.title || "").localeCompare(b.title || "", "en");
        default:          return (b.date || "").localeCompare(a.date || "");
      }
    });

    state.filtered = list;
    render();
  };

  if (els.search) {
    els.search.addEventListener("input", (e) => { state.query = e.target.value; applyFilters(); });
  }
  if (els.sort) {
    els.sort.addEventListener("change", (e) => { state.sort = e.target.value; applyFilters(); });
  }

  // ---------- Goodies + lightbox ----------

  const lightbox = document.getElementById("lightbox");
  const lightboxImg = document.getElementById("lightbox-img");
  const lightboxClose = document.querySelector(".lightbox-close");

  const openLightbox = (src, alt) => {
    if (!lightbox) return;
    lightboxImg.src = src;
    lightboxImg.alt = alt || "";
    lightbox.hidden = false;
    document.body.style.overflow = "hidden";
  };
  const closeLightbox = () => {
    if (!lightbox) return;
    lightbox.hidden = true;
    lightboxImg.src = "";
    document.body.style.overflow = "";
  };
  if (lightbox) {
    lightbox.addEventListener("click", (e) => {
      if (e.target === lightbox || e.target === lightboxImg) closeLightbox();
    });
    if (lightboxClose) lightboxClose.addEventListener("click", closeLightbox);
    document.addEventListener("keydown", (e) => {
      if (e.key === "Escape" && !lightbox.hidden) closeLightbox();
    });
    lightboxImg.addEventListener("click", (e) => e.stopPropagation());
  }

  const renderGoodies = (items) => {
    if (!els.goodiesGrid || !els.goodieTpl) return;
    if (!items.length) {
      const sect = document.getElementById("goodies");
      if (sect) sect.hidden = true;
      return;
    }
    items.sort((a, b) => (b.date || "").localeCompare(a.date || ""));
    els.goodiesGrid.innerHTML = "";
    const frag = document.createDocumentFragment();
    items.forEach((g) => {
      const node = els.goodieTpl.content.firstElementChild.cloneNode(true);
      const img = node.querySelector("img");
      img.src = g.image || "";
      img.alt = g.title || "";
      node.querySelector(".goodie-title").textContent = g.title || "Untitled";
      const desc = node.querySelector(".goodie-description");
      if (g.description) {
        // strip to a single short line (the academic layout is tight)
        desc.textContent = g.description.length > 90 ? g.description.slice(0, 88).replace(/\s+\S*$/, "") + "…" : g.description;
      } else {
        desc.remove();
      }
      const tagsEl = node.querySelector(".goodie-tags");
      (g.tags || []).forEach((tag) => {
        const li = document.createElement("li");
        li.textContent = tag;
        tagsEl.appendChild(li);
      });
      const thumb = node.querySelector(".goodie-thumb");
      thumb.addEventListener("click", () => openLightbox(g.image, g.title));
      frag.appendChild(node);
    });
    els.goodiesGrid.appendChild(frag);
  };

  // ---------- fetch data ----------

  fetch("data/goodies.json", { cache: "no-cache" })
    .then((r) => (r.ok ? r.json() : []))
    .then((data) => renderGoodies(Array.isArray(data) ? data : data.goodies || []))
    .catch(() => {
      const sect = document.getElementById("goodies");
      if (sect) sect.hidden = true;
    });

  fetch("data/papers.json", { cache: "no-cache" })
    .then((r) => {
      if (!r.ok) throw new Error("HTTP " + r.status);
      return r.json();
    })
    .then((data) => {
      state.papers = Array.isArray(data) ? data : data.papers || [];
      renderTopics();
      applyFilters();
    })
    .catch((err) => {
      console.error(err);
      els.list.innerHTML =
        '<p class="empty-state" style="text-align:center;color:var(--ink-3);padding:2rem 0;">Could not load papers.json. Is the site being served over HTTP (e.g. GitHub Pages)?</p>';
    });
})();
