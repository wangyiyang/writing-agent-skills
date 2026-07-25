#!/usr/bin/env node

const { spawn } = require("child_process");
const path = require("path");

const scriptPath = path.join(__dirname, "..", "rss-fetcher", "scripts", "fetch_rss.py");
const args = process.argv.slice(2);

const child = spawn("python3", [scriptPath, ...args], {
  stdio: "inherit",
  env: process.env,
});

child.on("error", (err) => {
  if (err.code === "ENOENT") {
    console.error("Error: python3 not found. Please install Python 3.8+.");
    process.exit(1);
  }
  console.error(err.message);
  process.exit(1);
});

child.on("close", (code) => {
  process.exit(code);
});
