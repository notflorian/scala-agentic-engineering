"use strict";

function adaptDisclosure(id, onExpand) {
  const disclosure = document.getElementById(id);
  if (!disclosure) return;

  const viewport = matchMedia(disclosure.dataset.wide);
  function adapt() {
    disclosure.open = viewport.matches;
    if (viewport.matches) onExpand?.(disclosure);
  }
  adapt();
  viewport.addEventListener("change", adapt);
}

function setupNavigation() {
  adaptDisclosure("chapter-disclosure", (sidebar) => {
    const active = sidebar.querySelector('[aria-current="page"]');
    const nav = document.getElementById("chapter-nav");
    if (active && active.getBoundingClientRect().bottom > nav.getBoundingClientRect().bottom) {
      nav.scrollTop += active.getBoundingClientRect().top - nav.getBoundingClientRect().top;
    }
  });
  adaptDisclosure("toc-disclosure");

  const picker = document.getElementById("language-picker");
  if (!picker) return;

  const links = picker.querySelectorAll("a[hreflang]");
  function updateLocaleLinks() {
    const { hash } = location;
    const anchor = /^#(?:s-\d+|chapter|guide)$/.test(hash) && document.getElementById(hash.slice(1)) ? hash : "";
    for (const link of links) {
      const target = new URL(link.href);
      target.hash = anchor;
      link.href = target.href;
    }
  }
  updateLocaleLinks();
  window.addEventListener("hashchange", updateLocaleLinks);

  picker.addEventListener("keydown", (event) => {
    if (event.key !== "Escape" || !picker.open) return;
    event.preventDefault();
    picker.open = false;
    picker.querySelector("summary").focus();
  });
  document.addEventListener("click", (event) => {
    if (!picker.contains(event.target)) picker.open = false;
  });
}

function setupContents() {
  const toc = document.querySelector(".guide-toc nav");
  if (!toc) return;

  const header = document.querySelector(".docs-header");
  const links = [...toc.querySelectorAll("a")];
  const headings = links.map((link) => document.getElementById(link.hash.slice(1)));
  let current;
  let frame;
  let observer;

  function update() {
    frame = undefined;
    const readingLine = header.getBoundingClientRect().bottom + 48;
    const end = document.documentElement.scrollHeight - innerHeight;
    let index = 0;
    if (end > 1 && scrollY >= end - 1) {
      index = headings.length - 1;
    } else {
      // Heading offsets are ordered. Check only the ones needed to find the reading position.
      let low = 0;
      let high = headings.length;
      while (low < high) {
        const mid = (low + high) >>> 1;
        if (headings[mid].getBoundingClientRect().top <= readingLine) low = mid + 1;
        else high = mid;
      }
      index = Math.max(0, low - 1);
    }
    const active = links[index];
    if (active === current) return;
    current?.removeAttribute("aria-current");
    current = active;
    active.setAttribute("aria-current", "location");
    if (matchMedia("(min-width: 80rem)").matches) {
      const rail = toc.getBoundingClientRect();
      const row = active.getBoundingClientRect();
      if (row.bottom > rail.bottom) toc.scrollTop += row.bottom - rail.bottom;
      if (row.top < rail.top) toc.scrollTop += row.top - rail.top;
    }
  }

  function schedule() {
    if (frame === undefined) frame = requestAnimationFrame(update);
  }

  function observe() {
    observer?.disconnect();
    if ("IntersectionObserver" in window) {
      const line = Math.min(innerHeight - 1, header.offsetHeight + 48);
      observer = new IntersectionObserver(schedule, { rootMargin: `-${line}px 0px 0px 0px` });
      headings.forEach((heading) => observer.observe(heading));
    }
    schedule();
  }
  observe();
  window.addEventListener("resize", observe);
  window.addEventListener("hashchange", schedule);
  window.addEventListener("pageshow", schedule);

  // Scroll completion also covers large jumps between headings that never intersect the viewport.
  if (observer && "onscrollend" in document) {
    document.addEventListener("scrollend", schedule);
  } else {
    window.addEventListener("scroll", schedule, { passive: true });
  }
}

const codeNames = {
  bash: "Bash", console: "Shell", javascript: "JavaScript", js: "JavaScript",
  json: "JSON", markdown: "Markdown", ruby: "Ruby", scala: "Scala",
  sh: "Shell", sql: "SQL", toml: "TOML", xml: "XML", yaml: "YAML", yml: "YAML"
};

function setupArticle() {
  const article = document.getElementById("guide-text");
  if (!article) return;

  const icon = document.getElementById("permalink-icon");
  for (const heading of article.querySelectorAll(":is(h1, h2, h3, h4, h5, h6)[id]")) {
    const link = document.createElement("a");
    link.className = "heading-permalink";
    link.href = "#" + heading.id;
    link.setAttribute("aria-label", article.dataset.permalink);
    link.append(icon.content.cloneNode(true));
    heading.append(link);
  }

  const scrollRegions = new Map();
  for (const block of article.querySelectorAll("pre")) {
    const code = block.querySelector("code");
    if (!code) continue;
    const source = block.closest(".highlighter-rouge") || block;
    const language = [...source.classList, ...code.classList].find((name) => name.startsWith("language-"))?.slice(9);
    const label = language === "plaintext" || language === "text"
      ? article.dataset.text
      : (Object.hasOwn(codeNames, language) ? codeNames[language] : language) || article.dataset.code;

    const wrapper = document.createElement("div");
    wrapper.className = "code-block";
    const header = document.createElement("div");
    header.className = "code-header";
    const name = document.createElement("span");
    name.className = "code-language";
    name.textContent = label;
    header.append(name);
    source.before(wrapper);
    wrapper.append(header, source);
    scrollRegions.set(block, label);

    if (!navigator.clipboard?.writeText) continue;
    const message = document.createElement("span");
    message.className = "copy-status";
    message.setAttribute("role", "status");
    const button = document.createElement("button");
    button.type = "button";
    button.className = "copy-button";
    button.textContent = article.dataset.copy;
    header.append(message, button);
    let reset;
    button.addEventListener("click", async () => {
      clearTimeout(reset);
      try {
        await navigator.clipboard.writeText(code.textContent);
        message.textContent = article.dataset.copied;
      } catch {
        message.textContent = article.dataset.copyError;
      }
      reset = setTimeout(() => { message.textContent = ""; }, 3000);
    });
  }

  for (const table of article.querySelectorAll(".table-wrapper")) {
    scrollRegions.set(table, article.dataset.table);
  }

  function updateRegion(element) {
    if (element.scrollWidth > element.clientWidth + 1) {
      element.tabIndex = 0;
      element.setAttribute("role", "region");
      element.setAttribute("aria-label", scrollRegions.get(element));
    } else {
      element.removeAttribute("tabindex");
      element.removeAttribute("role");
      element.removeAttribute("aria-label");
    }
  }
  const observer = "ResizeObserver" in window
    ? new ResizeObserver((entries) => entries.forEach(({ target }) => updateRegion(target)))
    : undefined;
  for (const element of scrollRegions.keys()) {
    updateRegion(element);
    observer?.observe(element);
  }
  if (!observer && scrollRegions.size) {
    window.addEventListener("resize", () => scrollRegions.forEach((_, element) => updateRegion(element)));
  }
}

function setupSearch() {
  const search = document.getElementById("local-search");
  if (!search?.showModal || typeof searchGuide !== "function") return;

  const trigger = document.getElementById("search-trigger");
  const input = document.getElementById("search-query");
  const results = document.getElementById("search-results");
  const status = document.getElementById("search-status");
  const lang = document.documentElement.lang;
  const number = new Intl.NumberFormat(lang);
  const mac = /Mac|iPhone|iPad/.test(navigator.platform);
  trigger.querySelector("kbd").textContent = mac ? "⌘ K" : "Ctrl K";
  trigger.hidden = false;

  let pending;
  let revision = 0;
  let delay;
  let opener;

  function loadIndex() {
    if (!pending) {
      pending = fetch(search.dataset.index).then((response) => {
        if (!response.ok) throw new Error("Search index unavailable");
        return response.json();
      }).catch((error) => {
        pending = undefined;
        throw error;
      });
    }
    return pending;
  }

  function paintResult(item, excerpt, url) {
    const li = document.createElement("li");
    const link = document.createElement("a");
    link.href = url;
    const separator = item.title.indexOf(" · ");
    const title = document.createElement("strong");
    title.textContent = separator < 0 ? item.title : item.title.slice(separator + 3);
    link.append(title);
    if (separator >= 0) {
      const context = document.createElement("span");
      context.className = "search-context";
      context.textContent = item.title.slice(0, separator);
      link.append(context);
    }
    if (excerpt) {
      const preview = document.createElement("span");
      preview.className = "search-preview";
      preview.textContent = excerpt;
      link.append(preview);
    }
    li.append(link);
    return li;
  }

  async function updateSearch(query, id) {
    try {
      const entries = await loadIndex();
      if (id !== revision) return;
      const found = document.createDocumentFragment();
      const local = `/${lang}/`;
      const seen = new Set();
      for (const { item, excerpt } of searchGuide(entries, query, lang)) {
        if (!item.url.startsWith(local)) continue;
        const url = new URL(search.dataset.prefix + item.url.slice(local.length), location.origin);
        if (url.origin !== location.origin || !url.pathname.startsWith(search.dataset.prefix) || seen.has(url.href)) continue;
        seen.add(url.href);
        found.append(paintResult(item, excerpt, url));
      }
      results.replaceChildren(found);
      status.textContent = seen.size ? search.dataset.count.replace("{count}", number.format(seen.size)) : search.dataset.noResults;
    } catch {
      if (id === revision) status.textContent = search.dataset.error;
    }
  }

  function open() {
    if (search.open) return;
    opener = document.activeElement;
    search.showModal();
    input.focus();
  }

  trigger.addEventListener("click", open);
  document.addEventListener("keydown", (event) => {
    if (event.key.toLowerCase() === "k" && (mac ? event.metaKey : event.ctrlKey) && !event.altKey) {
      event.preventDefault();
      open();
    }
  });
  search.addEventListener("close", () => {
    revision += 1;
    clearTimeout(delay);
    input.value = "";
    status.textContent = "";
    results.replaceChildren();
    (opener instanceof HTMLElement && opener !== document.body ? opener : trigger).focus();
  });
  search.addEventListener("click", (event) => {
    if (event.target !== search) return;
    const bounds = search.getBoundingClientRect();
    if (event.clientX < bounds.left || event.clientX > bounds.right || event.clientY < bounds.top || event.clientY > bounds.bottom) {
      search.close();
    }
  });
  search.addEventListener("keydown", (event) => {
    if (event.key === "Escape") {
      event.preventDefault();
      search.close();
      return;
    }
    const links = [...results.querySelectorAll("a")];
    const index = links.indexOf(document.activeElement);
    const inResults = document.activeElement === input || index >= 0;
    if (!links.length || !inResults) return;

    if (event.key === "ArrowDown" || event.key === "ArrowUp") {
      event.preventDefault();
      const next = event.key === "ArrowDown" ? Math.min(index + 1, links.length - 1) : index - 1;
      (index < 0 && event.key === "ArrowUp" ? links.at(-1) : links[next] || input).focus();
    } else if (event.key === "Enter" && document.activeElement === input) {
      event.preventDefault();
      links[0].click();
    }
  });
  input.addEventListener("input", () => {
    const id = ++revision;
    const query = input.value.trim();
    clearTimeout(delay);
    results.replaceChildren();
    status.textContent = query ? search.dataset.loading : "";
    if (query) delay = setTimeout(() => updateSearch(query, id), 150);
  });
}

function localizeNotFound() {
  const main = document.getElementById("not-found");
  if (!main) return;

  const path = location.pathname.slice(main.dataset.baseurl.length);
  const lang = path.split("/")[1];
  const template = document.getElementById("not-found-" + lang);
  if (!template) return;

  document.documentElement.lang = lang;
  document.getElementById("not-found-copy").replaceChildren(template.content.cloneNode(true));
  document.title = document.title.replace(document.getElementById("not-found-en").content.querySelector("h1").textContent,
    template.content.querySelector("h1").textContent);
}

setupNavigation();
setupArticle();
setupContents();
setupSearch();
localizeNotFound();
