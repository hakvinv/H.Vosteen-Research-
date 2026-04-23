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
    empty: document.getElementById("empty-state"),
    search: document.getElementById("search"),
    sort: document.getElementById("sort"),
    tagFilter: document.getElementById("tag-filter"),
    template: document.getElementById("paper-card-template"),
    year: document.getElementById("year"),
  };

  els.year.textContent = new Date().getFullYear();

  const formatDate = (iso) => {
    if (!iso) return "";
    const d = new Date(iso);
    if (Number.isNaN(d.getTime())) return iso;
    return d.toLocaleDateString("en-US", {
      year: "numeric",
      month: "short",
      day: "numeric",
    });
  };

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
    return [
      `@techreport{${key},`,
      `  title   = {${p.title || ""}},`,
      `  author  = {${authors}},`,
      `  year    = {${year}},`,
      `  institution = {H. Vosteen Research},`,
      p.url ? `  url     = {${p.url}},` : null,
      `  note    = {Working Paper}`,
      `}`,
    ]
      .filter(Boolean)
      .join("\n");
  };

  const render = () => {
    els.list.innerHTML = "";
    const list = state.filtered;

    if (!list.length) {
      els.empty.hidden = false;
      return;
    }
    els.empty.hidden = true;

    const frag = document.createDocumentFragment();
    for (const paper of list) {
      const node = els.template.content.cloneNode(true);

      node.querySelector(".paper-title").textContent = paper.title || "Untitled";
      node.querySelector(".paper-authors").textContent = Array.isArray(paper.authors)
        ? paper.authors.join(", ")
        : paper.authors || "H. Vosteen";
      node.querySelector(".paper-abstract").textContent = paper.abstract || "";

      const dateEl = node.querySelector(".paper-date");
      dateEl.dateTime = paper.date || "";
      dateEl.textContent = formatDate(paper.date);

      const versionEl = node.querySelector(".paper-version");
      if (paper.version) {
        versionEl.textContent = `v${paper.version}`;
      } else {
        versionEl.remove();
      }

      const tagsEl = node.querySelector(".paper-tags");
      (paper.tags || []).forEach((tag) => {
        const li = document.createElement("li");
        li.textContent = tag;
        tagsEl.appendChild(li);
      });

      const dl = node.querySelector(".paper-download");
      const view = node.querySelector(".paper-view");
      if (paper.file) {
        dl.href = paper.file;
        view.href = paper.file;
      } else {
        dl.remove();
        view.remove();
      }

      const citeBtn = node.querySelector(".paper-cite");
      (paper.links || []).forEach((link) => {
        if (!link || !link.url || !link.label) return;
        const a = document.createElement("a");
        a.className = "btn btn-ghost paper-link";
        a.href = link.url;
        a.target = "_blank";
        a.rel = "noopener";
        const isGithub = /github\.com\//i.test(link.url);
        if (isGithub) {
          a.innerHTML =
            '<svg width="14" height="14" viewBox="0 0 16 16" fill="currentColor" aria-hidden="true">' +
            '<path d="M8 0C3.58 0 0 3.58 0 8c0 3.54 2.29 6.53 5.47 7.59.4.07.55-.17.55-.38 0-.19-.01-.82-.01-1.49-2.01.37-2.53-.49-2.69-.94-.09-.23-.48-.94-.82-1.13-.28-.15-.68-.52-.01-.53.63-.01 1.08.58 1.23.82.72 1.21 1.87.87 2.33.66.07-.52.28-.87.51-1.07-1.78-.2-3.64-.89-3.64-3.95 0-.87.31-1.59.82-2.15-.08-.2-.36-1.02.08-2.12 0 0 .67-.21 2.2.82.64-.18 1.32-.27 2-.27.68 0 1.36.09 2 .27 1.53-1.04 2.2-.82 2.2-.82.44 1.1.16 1.92.08 2.12.51.56.82 1.27.82 2.15 0 3.07-1.87 3.75-3.65 3.95.29.25.54.73.54 1.48 0 1.07-.01 1.93-.01 2.2 0 .21.15.46.55.38A8.012 8.012 0 0016 8c0-4.42-3.58-8-8-8z"/>' +
            '</svg>';
        }
        const span = document.createElement("span");
        span.textContent = link.label;
        a.appendChild(span);
        citeBtn.insertAdjacentElement("beforebegin", a);
      });

      const bibtexEl = node.querySelector(".paper-bibtex");
      bibtexEl.textContent = buildBibtex(paper);
      citeBtn.addEventListener("click", () => {
        const show = bibtexEl.hidden;
        bibtexEl.hidden = !show;
        citeBtn.textContent = show ? "Hide BibTeX" : "Cite";
        if (show && navigator.clipboard) {
          navigator.clipboard.writeText(bibtexEl.textContent).catch(() => {});
        }
      });

      frag.appendChild(node);
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
      ]
        .filter(Boolean)
        .join(" ")
        .toLowerCase();
      return hay.includes(q);
    });

    list.sort((a, b) => {
      switch (state.sort) {
        case "date-asc":
          return (a.date || "").localeCompare(b.date || "");
        case "title-asc":
          return (a.title || "").localeCompare(b.title || "", "en");
        case "date-desc":
        default:
          return (b.date || "").localeCompare(a.date || "");
      }
    });

    state.filtered = list;
    render();
  };

  const renderTagFilter = () => {
    const tagCount = new Map();
    state.papers.forEach((p) =>
      (p.tags || []).forEach((t) => tagCount.set(t, (tagCount.get(t) || 0) + 1)),
    );
    if (!tagCount.size) {
      els.tagFilter.hidden = true;
      return;
    }
    const tags = [...tagCount.entries()].sort((a, b) => b[1] - a[1]);
    els.tagFilter.innerHTML = "";

    const all = document.createElement("button");
    all.className = "tag-chip" + (state.activeTag ? "" : " active");
    all.textContent = "All";
    all.type = "button";
    all.addEventListener("click", () => {
      state.activeTag = null;
      renderTagFilter();
      applyFilters();
    });
    els.tagFilter.appendChild(all);

    tags.forEach(([tag, count]) => {
      const btn = document.createElement("button");
      btn.className = "tag-chip" + (state.activeTag === tag ? " active" : "");
      btn.textContent = `${tag} (${count})`;
      btn.type = "button";
      btn.addEventListener("click", () => {
        state.activeTag = state.activeTag === tag ? null : tag;
        renderTagFilter();
        applyFilters();
      });
      els.tagFilter.appendChild(btn);
    });
  };

  els.search.addEventListener("input", (e) => {
    state.query = e.target.value;
    applyFilters();
  });
  els.sort.addEventListener("change", (e) => {
    state.sort = e.target.value;
    applyFilters();
  });

  fetch("data/papers.json", { cache: "no-cache" })
    .then((r) => {
      if (!r.ok) throw new Error(`HTTP ${r.status}`);
      return r.json();
    })
    .then((data) => {
      state.papers = Array.isArray(data) ? data : data.papers || [];
      renderTagFilter();
      applyFilters();
    })
    .catch((err) => {
      console.error(err);
      els.list.innerHTML =
        '<p class="empty-state">Could not load papers.json. Is the site being served over HTTP (e.g. GitHub Pages)?</p>';
    });
})();
