"use strict";

const language = document.documentElement.lang;
const nav = document.getElementById("chapter-nav");
const toggle = document.getElementById("chapter-toggle");
const narrow = matchMedia("(max-width: 49.999rem)");

function showChapters(expand) {
  nav.dataset.collapsed = String(!expand && narrow.matches);
  toggle.setAttribute("aria-expanded", String(expand));
}
function adaptChapters() {
  toggle.hidden = !narrow.matches;
  showChapters(!narrow.matches);
}
adaptChapters();
narrow.addEventListener("change", adaptChapters);
toggle.addEventListener("click", () => showChapters(toggle.getAttribute("aria-expanded") !== "true"));

function updateLocaleLinks() {
  for (const link of document.querySelectorAll(".locale-nav a")) {
    const target = new URL(link.href);
    target.hash = /^#(?:s-\d+|chapter|guide)$/.test(location.hash) ? location.hash : "";
    link.href = target.href;
  }
}
updateLocaleLinks();
window.addEventListener("hashchange", updateLocaleLinks);

const article = document.getElementById("guide-text");
if (article && navigator.clipboard) {
  for (const block of article.querySelectorAll("pre")) {
    const code = block.querySelector("code");
    if (!code) continue;
    const button = document.createElement("button");
    button.type = "button";
    button.className = "btn copy-button";
    button.textContent = article.dataset.copy;
    const message = document.createElement("span");
    message.className = "sr-only";
    message.setAttribute("role", "status");
    const wrapper = block.closest(".highlighter-rouge") || block;
    wrapper.before(button, message);
    button.addEventListener("click", async () => {
      try {
        await navigator.clipboard.writeText(code.textContent);
        message.textContent = article.dataset.copied;
      } catch {
        message.textContent = article.dataset.copyError;
      }
    });
  }
}

const search = document.getElementById("local-search");
const input = document.getElementById("search-query");
const results = document.getElementById("search-results");
const status = document.getElementById("search-status");
let pending;
let revision = 0;
let delay;

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

async function updateSearch(query, id) {
  try {
    const entries = await loadIndex();
    if (id !== revision) return;
    const matches = searchGuide(entries, query, language);
    status.textContent = matches.length ? "" : search.dataset.noResults;
    for (const { item, excerpt } of matches) {
      const url = search.dataset.baseurl + item.url;
      if (!url.startsWith(search.dataset.baseurl + "/" + language + "/")) continue;
      const li = document.createElement("li");
      const link = document.createElement("a");
      link.href = url;
      link.textContent = item.title;
      const preview = document.createElement("span");
      preview.className = "search-preview";
      preview.textContent = excerpt;
      li.append(link, preview);
      results.append(li);
    }
  } catch {
    if (id === revision) status.textContent = search.dataset.error;
  }
}

search.hidden = false;
input.addEventListener("input", () => {
  revision += 1;
  const id = revision;
  const query = input.value.trim();
  clearTimeout(delay);
  results.replaceChildren();
  status.textContent = "";
  if (query) delay = setTimeout(() => updateSearch(query, id), 150);
});
