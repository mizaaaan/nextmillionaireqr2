#!/usr/bin/env node
/**
 * Validate that all nav.* translation keys exist in every page's
 * window.translations object for all three languages (en/bn/ar).
 *
 * Usage: node scripts/check-nav-translations.js
 */

const fs = require("fs");
const path = require("path");

const PAGES = [
  "index.html",
  "about.html",
  "gallery.html",
  "contact.html",
  "team.html",
  "fleet.html",
  "portal.html",
];

// Keys that each page SHOULD have based on its HTML nav links
const REQUIRED_NAV_KEYS = {
  index:   ["nav.about", "nav.gallery", "nav.fleet", "nav.contact", "nav.portal"],
  about:   ["nav.about", "nav.gallery", "nav.fleet", "nav.contact", "nav.portal"],
  gallery: ["nav.about", "nav.gallery", "nav.fleet", "nav.contact", "nav.portal"],
  contact: ["nav.about", "nav.gallery", "nav.fleet", "nav.contact", "nav.portal"],
  team:    ["nav.about", "nav.gallery", "nav.fleet", "nav.contact", "nav.portal"],
  fleet:   ["nav.about", "nav.gallery", "nav.fleet", "nav.contact", "nav.portal"],
  portal:  ["nav.home",  "nav.about",   "nav.gallery", "nav.fleet", "nav.contact", "nav.portal"],
};

const LANGUAGES = ["en", "bn", "ar"];

function extractTranslations(text) {
  // Find window.translations = { ... };
  const match = text.match(/window\.translations\s*=\s*(\{[\s\S]*?\});\s*\n?\s*<\/script>/);
  if (!match) {
    console.error("  ✗ Could not find window.translations");
    return null;
  }
  try {
    // Use eval to parse since JSON5-style unquoted keys and trailing commas
    // are common. Safe because we control the source.
    const obj = eval("(" + match[1] + ")");
    return obj;
  } catch (e) {
    console.error("  ✗ Failed to parse translations:", e.message);
    return null;
  }
}

let allPassed = true;
let totalChecks = 0;
let passedChecks = 0;
let failedChecks = [];

for (const page of PAGES) {
  const pageName = path.basename(page, ".html");
  const filePath = path.join(__dirname, "..", page);
  const html = fs.readFileSync(filePath, "utf-8");
  const requiredKeys = REQUIRED_NAV_KEYS[pageName] || [];
  const translations = extractTranslations(html);

  if (!translations) {
    allPassed = false;
    continue;
  }

  console.log(`\n=== ${page} ===`);

  for (const lang of LANGUAGES) {
    const dict = translations[lang];
    if (!dict) {
      console.log(`  ${lang}: ✗ Language section missing`);
      allPassed = false;
      failedChecks.push({ page, lang, key: "(all)", status: "missing language section" });
      continue;
    }

    for (const key of requiredKeys) {
      totalChecks++;
      if (dict[key] !== undefined && dict[key] !== null && dict[key] !== "") {
        console.log(`  ${lang}.${key}: ✅ "${dict[key]}"`);
        passedChecks++;
      } else {
        console.log(`  ${lang}.${key}: ❌ MISSING`);
        allPassed = false;
        failedChecks.push({ page, lang, key, status: "missing" });
      }
    }
  }
}

console.log("\n" + "=".repeat(50));
console.log(`Results: ${passedChecks}/${totalChecks} checks passed`);
if (failedChecks.length > 0) {
  console.log("\nFailed checks:");
  for (const f of failedChecks) {
    console.log(`  ${f.page} — ${f.lang}.${f.key}: ${f.status}`);
  }
}
console.log(allPassed ? "\n✅ ALL CHECKS PASSED!" : "\n❌ SOME CHECKS FAILED!");
