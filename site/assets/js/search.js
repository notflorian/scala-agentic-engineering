"use strict";

function fold(text, language) {
  return text.toLocaleLowerCase(language).normalize("NFKD").replace(/\p{M}/gu, "").replace(/ß/g, "ss");
}

function searchGuide(entries, query, language) {
  const terms = fold(query.trim(), language).match(/[\p{L}\p{N}][\p{L}\p{N}+#.-]*/gu) || [];
  if (!terms.length) return [];
  return entries
    .filter((item) => item.lang === language)
    .map((item) => {
      const title = fold(item.title, language);
      const body = fold(item.text, language);
      let score = 0;
      for (const term of terms) {
        if (title.includes(term)) score += 5;
        else if (body.includes(term)) score += 1;
        else return null;
      }
      const match = body.indexOf(terms[0]);
      const start = Math.max(match - 35, 0);
      const excerpt = item.text.slice(start, start + 155).trim();
      return { item, score, excerpt: (start ? "…" : "") + excerpt + (start + 155 < item.text.length ? "…" : "") };
    })
    .filter(Boolean)
    .sort((left, right) => right.score - left.score)
    .slice(0, 20);
}

if (typeof module === "object") module.exports = { searchGuide };
