// news-image-20261124: deterministic runner for the Tuesday front page.
// The artwork itself is drawn by draw.py (Pillow, fixed content, no clock,
// no network, no randomness). This file only drives it: run the script,
// confirm the PNG it produces, and place a copy at /output/entry.png so
// the grader finds it. Node 22, standard library only.
import { execFileSync } from "node:child_process";
import { createHash } from "node:crypto";
import {
  copyFileSync,
  existsSync,
  mkdirSync,
  readFileSync,
} from "node:fs";
import { dirname, join } from "node:path";
import { fileURLToPath } from "node:url";

const HERE = dirname(fileURLToPath(import.meta.url));
const DRAW_PY = join(HERE, "draw.py");
const LOCAL_PNG = join(HERE, "entry.png");
const OUTPUT_DIR = "/output";
const OUTPUT_PNG = join(OUTPUT_DIR, "entry.png");

// Guard: fail early with a clear message instead of a bare spawn error.
if (!existsSync(DRAW_PY)) {
  throw new Error("missing drawing script: " + DRAW_PY);
}

function sha256Of(path) {
  return createHash("sha256").update(readFileSync(path)).digest("hex");
}

function checkPng(path) {
  const data = readFileSync(path);
  const signature = Buffer.from([0x89, 0x50, 0x4e, 0x47, 0x0d, 0x0a, 0x1a, 0x0a]);
  if (data.length < 33 || !data.subarray(0, 8).equals(signature)) {
    throw new Error(path + " is not a PNG file");
  }
  const w = data.readUInt32BE(16);
  const h = data.readUInt32BE(20);
  if (w !== 1024 || h !== 1024) {
    throw new Error(`${path} is ${w}x${h}, expected 1024x1024`);
  }
  return data.length;
}

// draw.py writes entry.png next to itself; it takes no arguments.
execFileSync("python3", [DRAW_PY], { cwd: HERE, stdio: "inherit" });
if (!existsSync(LOCAL_PNG)) {
  throw new Error("draw.py finished without producing " + LOCAL_PNG);
}
const localBytes = checkPng(LOCAL_PNG);
const localHash = sha256Of(LOCAL_PNG);

mkdirSync(OUTPUT_DIR, { recursive: true });
copyFileSync(LOCAL_PNG, OUTPUT_PNG);
const outBytes = checkPng(OUTPUT_PNG);
const outHash = sha256Of(OUTPUT_PNG);
if (outHash !== localHash || outBytes !== localBytes) {
  throw new Error("output copy differs from the drawn entry.png");
}
console.log(`wrote ${OUTPUT_PNG} ${outBytes} bytes sha256=${outHash}`);
