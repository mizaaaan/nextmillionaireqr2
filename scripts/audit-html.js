#!/usr/bin/env node
/**
 * Audit all HTML pages for structural issues after gallery changes.
 * Checks: unclosed divs, broken nav links, translation syntax, etc.
 *
 * Usage: node scripts/audit-html.js
 */
const fs = require("fs");
const path = require("path");

const PAGES = [
  "index.html",
  "about.html",
  "contact.html",
  "team.html",
  "fleet.html",
  "portal.html",
];

let allGood = true;

function auditNavLinks(html, file) {
  const issues = [];
  // Check desktop nav
  const navLinks = html.match(/<div class="nav-links">([\s\S]*?)<\/div>/);
  if (!navLinks) {
    issues.push("Missing nav-links section");
  } else {
    const linkCount = (navLinks[1].match(/data-i18n="nav\./g) || []).length;
    if (linkCount < 4) issues.push(`Only ${linkCount} nav links found (expected 5+)`);
  }

  // Check mobile menu
  const mobileMenu = html.match(/<div class="mobile-menu"[^>]*>([\s\S]*?)<\/div>/);
  if (!mobileMenu) {
    issues.push("Missing mobile-menu section");
  } else {
    const linkCount = (mobileMenu[1].match(/data-i18n="nav\./g) || []).length;
    if (linkCount < 4) issues.push(`Only ${linkCount} mobile nav links found (expected 5+)`);
  }

  return issues;
}

function checkDivBalance(html, file) {
  const issues = [];
  // Count opening and closing div tags (excluding self-closing)
  const openDivs = (html.match(/<div[\s>]/g) || []).length;
  const closeDivs = (html.match(/<\/div>/g) || []).length;
  // Count other prominent tags
  const openSections = (html.match(/<section[\s>]/g) || []).length;
  const closeSections = (html.match(/<\/section>/g) || []).length;

  if (openDivs !== closeDivs) {
    issues.push(`Div mismatch: ${openDivs} opening vs ${closeDivs} closing`);
  }
  if (openSections !== closeSections) {
    issues.push(`Section mismatch: ${openSections} opening vs ${closeSections} closing`);
  }
  return issues;
}

function checkTranslationsSyntax(html, file) {
  const issues = [];
  const transMatch = html.match(/window\.translations\s*=\s*(\{[\s\S]*?\});\s*\n?\s*<\/script>/);
  if (!transMatch) {
    issues.push("Could not find translations object");
    return issues;
  }
  
  const transText = transMatch[1];
  
  // Check for nav keys
  const navKeys = transText.match(/"nav\.[^"]+"/g) || [];
  if (navKeys.length === 0) {
    issues.push("No nav.* translation keys found");
  }
  
  // Check for double commas (syntax error)
  if (/,,\s*"/.test(transText)) {
    issues.push("Double comma found in translations");
  }
  
  // Check for missing commas between keys
  const lines = transText.split('\n');
  for (let i = 0; i < lines.length - 1; i++) {
    const currentLine = lines[i].trim();
    const nextLine = lines[i+1].trim();
    // If current line ends with a value but no comma, and next line starts with a key
    if (/"[^"]*"\s*$/.test(currentLine) && /^"/.test(nextLine)) {
      if (!currentLine.endsWith(',') && !currentLine.endsWith('{')) {
        if (currentLine.includes(':')) {
          issues.push(`Possible missing comma at line ${i+1}: "${currentLine}" -> "${nextLine}"`);
        }
      }
    }
  }

  return issues;
}

function checkAnchorBalance(html, file) {
  const issues = [];
  const openAs = (html.match(/<a\s/g) || []).length;
  const closeAs = (html.match(/<\/a>/g) || []).length;
  if (openAs !== closeAs) {
    issues.push(`Anchor mismatch: ${openAs} opening vs ${closeAs} closing`);
  }
  return issues;
}

function auditGallerySection(html, file) {
  if (file !== "index.html") return [];
  const issues = [];
  
  // Find gallery section
  const gallerySection = html.match(/<section[\s\S]*?id="gallery"[\s\S]*?<\/section>/);
  if (!gallerySection) {
    issues.push("Gallery section not found");
    return issues;
  }
  
  const secHtml = gallerySection[0];
  
  // Count gallery cards
  const cards = secHtml.match(/<div class="gallery-card">/g) || [];
  if (cards.length !== 6) {
    issues.push(`Expected 6 gallery cards, found ${cards.length}`);
  }
  
  // Check each card has proper closing
  const cardCloses = secHtml.match(/<\/div><\/div>/g) || [];
  if (cardCloses.length < 5) {
    issues.push(`Only ${cardCloses.length} properly closed gallery cards`);
  }
  
  return issues;
}

for (const page of PAGES) {
  const filePath = path.join(__dirname, "..", page);
  if (!fs.existsSync(filePath)) {
    console.log(`\n--- ${page} --- ⚠️ FILE NOT FOUND (was deleted)`);
    continue;
  }
  
  const html = fs.readFileSync(filePath, "utf-8");
  
  console.log(`\n--- ${page} ---`);
  
  const navIssues = auditNavLinks(html, page);
  const divIssues = checkDivBalance(html, page);
  const transIssues = checkTranslationsSyntax(html, page);
  const anchorIssues = checkAnchorBalance(html, page);
  const galleryIssues = auditGallerySection(html, page);
  
  const allIssues = [...navIssues, ...divIssues, ...transIssues, ...anchorIssues, ...galleryIssues];
  
  if (allIssues.length === 0) {
    console.log("  ✅ No issues found");
  } else {
    allGood = false;
    for (const issue of allIssues) {
      console.log(`  ⚠️  ${issue}`);
    }
  }
}

console.log("\n" + "=".repeat(50));
console.log(allGood ? "✅ ALL PAGES LOOK GOOD!" : "❌ Issues found (see above)");
