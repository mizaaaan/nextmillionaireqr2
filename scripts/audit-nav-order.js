#!/usr/bin/env node
/**
 * Audit navigation link order across all pages for site-wide consistency.
 *
 * Usage: node scripts/audit-nav-order.js
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

function extractNavLinks(html) {
  // Find nav-links sections (desktop nav)
  const navLinksMatch = html.match(/<div class="nav-links">([\s\S]*?)<\/div>/);
  // Find mobile-menu sections
  const mobileMenuMatch = html.match(/<div class="mobile-menu"[^>]*>([\s\S]*?)<\/div>/);

  function parseLinks(section) {
    if (!section) return [];
    const links = [];
    const regex = /<a\s[^>]*data-i18n="([^"]+)"[^>]*>([^<]+)<\/a>/g;
    let match;
    while ((match = regex.exec(section)) !== null) {
      links.push({ key: match[1], text: match[2].trim() });
    }
    return links;
  }

  return {
    desktop: parseLinks(navLinksMatch ? navLinksMatch[1] : null),
    mobile: parseLinks(mobileMenuMatch ? mobileMenuMatch[1] : null),
  };
}

console.log("=".repeat(80));
console.log("NAVIGATION LINK ORDER AUDIT");
console.log("=".repeat(80));

let allConsistent = true;
let referenceOrder = null;

for (const page of PAGES) {
  const filePath = path.join(__dirname, "..", page);
  const html = fs.readFileSync(filePath, "utf-8");
  const { desktop, mobile } = extractNavLinks(html);

  const dKeys = desktop.map((l) => l.key);
  const mKeys = mobile.map((l) => l.key);
  const dText = desktop.map((l) => `${l.key} ("${l.text}")`);
  const mText = mobile.map((l) => `${l.key} ("${l.text}")`);

  console.log(`\n--- ${page} ---`);
  console.log(`  Desktop nav-links: [${dKeys.join(" → ")}]`);
  console.log(`  Mobile menu:      [${mKeys.join(" → ")}]`);

  // Check desktop vs mobile consistency
  const desktopStr = JSON.stringify(dKeys);
  const mobileStr = JSON.stringify(mKeys);
  if (desktopStr !== mobileStr) {
    console.log(`  ⚠️  MISMATCH: Desktop and mobile orders differ!`);
    allConsistent = false;
  }

  // Check cross-page consistency
  if (referenceOrder === null) {
    referenceOrder = desktopStr;
  } else if (desktopStr !== referenceOrder) {
    console.log(`  ⚠️  INCONSISTENT with other pages! Expected: ${referenceOrder}`);
    allConsistent = false;
  }

  // Check for duplicate links
  if (new Set(dKeys).size !== dKeys.length) {
    console.log(`  ⚠️  DUPLICATE links in desktop nav!`);
    allConsistent = false;
  }
  if (new Set(mKeys).size !== mKeys.length) {
    console.log(`  ⚠️  DUPLICATE links in mobile menu!`);
    allConsistent = false;
  }
}

console.log("\n" + "=".repeat(80));
if (allConsistent) {
  console.log("✅ ALL PAGES have consistent nav link order!");
} else {
  console.log("❌ Some inconsistencies were found (see above).");
}
console.log("=".repeat(80));
