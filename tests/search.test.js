const test = require("node:test");
const assert = require("node:assert/strict");
const { searchGuide } = require("../site/assets/js/search.js");

const data = [
  { lang: "fr", title: "Sélection du modèle", text: "Budget réservé aux tests", url: "/fr/ch-3/#s-2" },
  { lang: "fr", title: "Budget", text: "Modèle Scala", url: "/fr/ch-4/#chapter" },
  { lang: "en", title: "Selection du modele", text: "Budget selection", url: "/en/ch-3/#s-2" }
];

test("matches accented words and ranks a heading match ahead of a body match", () => {
  assert.deepEqual(searchGuide(data, "modele", "fr").map(({ item }) => item.url),
    ["/fr/ch-3/#s-2", "/fr/ch-4/#chapter"]);
});

test("excludes foreign results even when supplied a mixed index", () => {
  assert.deepEqual(searchGuide(data, "Selection", "fr").map(({ item }) => item.lang), ["fr"]);
  assert.deepEqual(searchGuide(data, "réservé tests", "en"), []);
});

test("matches every term and handles an empty query", () => {
  assert.equal(searchGuide(data, "budget tests", "fr").length, 1);
  assert.deepEqual(searchGuide(data, " ", "fr"), []);
});
