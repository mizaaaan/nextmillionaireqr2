#!/usr/bin/env node
/**
 * Quick HTML balance check - counts ALL <div and </div> accurately.
 * Usage: node scripts/check-divs.js
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

for (const page of PAGES) {
  const filePath = path.join(__dirname, "..", page);
  if (!fs.existsSync(filePath)) continue;
  const html = fs.readFileSync(filePath, "utf-8");
  const openDivs = (html.match(/<div[\s>]/g) || []).length;
  const closeDivs = (html.match(/<\/div>/g) || []).length;
  const openSec = (html.match(/<section[\s>]/g) || []).length;
  const closeSec = (html.match(/<\/section>/g) || []).length;
  const openA = (html.match(/<a[\s>]/g) || []).length;
  const closeA = (html.match(/<\/a>/g) || []).length;
  
  const status = (openDivs === closeDivs && openSec === closeSec && openA === closeA) ? "✅" : "⚠️";
  console.log(`${status} ${page}: divs ${openDivs}/${closeDivs}, sections ${openSec}/${closeSec}, anchors ${openA}/${closeA}`);
}
