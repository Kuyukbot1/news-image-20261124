// news-image-20261124: place the drawn Tuesday front page at the output dir.
// Node 22, standard library only. The artwork is pre-drawn by draw.py and
// committed as entry.png; this entrypoint never runs Python or touches the
// repo directory, it only copies the exact committed bytes to the output
// directory, so every run produces identical output with no network access.
import { createHash } from "node:crypto";
import { mkdirSync, readFileSync, writeFileSync } from "node:fs";
import { dirname, join } from "node:path";
import { fileURLToPath } from "node:url";

const outputDir = process.env.MAKEFUN_OUTPUT_DIR ?? "/output";
// The grader mounts the output volume: create it if needed, never remove it.
mkdirSync(outputDir, { recursive: true });

const entryDir = dirname(fileURLToPath(import.meta.url));
const pngBytes = readFileSync(join(entryDir, "entry.png"));

// Validate the PNG before reporting it: 8-byte signature, then the IHDR
// chunk must say 1024x1024, matching the front-page format.
const PNG_SIG = Buffer.from([0x89, 0x50, 0x4e, 0x47, 0x0d, 0x0a, 0x1a, 0x0a]);
if (pngBytes.length < 33 || !pngBytes.subarray(0, 8).equals(PNG_SIG)) {
  throw new Error("entry.png is not a PNG file");
}
const width = pngBytes.readUInt32BE(16);
const height = pngBytes.readUInt32BE(20);
if (width !== 1024 || height !== 1024) {
  throw new Error(`entry.png is ${width}x${height}, expected 1024x1024`);
}

const outPath = join(outputDir, "entry.png");
writeFileSync(outPath, pngBytes);

// Round-trip check: re-read the copy and confirm it is byte-identical to
// the committed image, so a partial or failed write can never pass silently.
const writtenBytes = readFileSync(outPath);
const sha = createHash("sha256").update(pngBytes).digest("hex");
const writtenSha = createHash("sha256").update(writtenBytes).digest("hex");
if (writtenSha !== sha || writtenBytes.length !== pngBytes.length) {
  throw new Error("output copy differs from the committed entry.png");
}
console.log(`wrote ${outPath} ${writtenBytes.length} bytes sha256=${writtenSha}`);
