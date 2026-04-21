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

      const bibtexEl = node.querySelector(".paper-bibtex");
      bibtexEl.textContent = buildBibtex(paper);
      const citeBtn = node.querySelector(".paper-cite");
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
