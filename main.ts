// news-18-nov: entry program for make.fun's "Sum up 18 November's world
// news in one image" bounty. The image itself (entry.png) was drawn by
// render.py and sits beside this file; this program copies it to the
// grader's output directory as /output/entry.png.
//
// Outside the grader, MAKEFUN_OUTPUT_DIR stands in for /output:
//   mkdir -p out && MAKEFUN_OUTPUT_DIR=out node main.ts

import { copyFileSync } from "node:fs";
import { join } from "node:path";

const outDir = process.env.MAKEFUN_OUTPUT_DIR ?? "/output";
const src = new URL("./entry.png", import.meta.url);
copyFileSync(src, join(outDir, "entry.png"));
