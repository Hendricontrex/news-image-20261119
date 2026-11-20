// news-image-20261119 — "The day in five stories", Thursday 19 November 2026.
//
// The entry is a program that writes one image to /output/entry.png. The
// image itself (a newspaper front page: masthead with the date, then the
// five biggest stories of 19 Nov 2026, each with a headline, one factual
// subline and its dateline) lives in this repository as entry.png, and
// this program copies it to the output directory. No network is used, and
// both runs write the same bytes because the copy is byte-for-byte.
//
// Local check: mkdir -p out && MAKEFUN_OUTPUT_DIR=out node main.ts

import { mkdirSync, readFileSync, writeFileSync } from "node:fs";
import { dirname, join } from "node:path";
import { fileURLToPath } from "node:url";

const here = dirname(fileURLToPath(import.meta.url));
const outDir = process.env.MAKEFUN_OUTPUT_DIR ?? "/output";
const target = join(outDir, "entry.png");

mkdirSync(outDir, { recursive: true });
const bytes = readFileSync(join(here, "entry.png"));

// The gate takes a whole PNG of at most 1 MiB and 1024 by 1024 pixels.
// Fail loudly here instead of handing the grader a broken file.
const PNG_MAGIC = Buffer.from([0x89, 0x50, 0x4e, 0x47, 0x0d, 0x0a, 0x1a, 0x0a]);
if (!bytes.subarray(0, 8).equals(PNG_MAGIC)) {
  throw new Error("entry.png is not a PNG file");
}
if (bytes.length > 1048576) {
  throw new Error(`entry.png is ${bytes.length} bytes, over the 1 MiB limit`);
}
writeFileSync(target, bytes);
console.log(`wrote ${target} (${bytes.length} bytes)`);
