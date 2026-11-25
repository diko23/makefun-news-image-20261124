import { mkdirSync, readFileSync, writeFileSync } from "node:fs";
import { dirname, join } from "node:path";
import { fileURLToPath } from "node:url";

const MAX_BYTES = 1_048_576;
const MAX_DIMENSION = 1024;
const PNG_MAGIC = Buffer.from([0x89, 0x50, 0x4e, 0x47, 0x0d, 0x0a, 0x1a, 0x0a]);
const PNG_IEND = Buffer.from([0x49, 0x45, 0x4e, 0x44, 0xae, 0x42, 0x60, 0x82]);

function validateImage(data: Buffer): void {
  if (data.length === 0 || data.length > MAX_BYTES) {
    throw new Error(`Invalid entry.png size: ${data.length} bytes (limit ${MAX_BYTES})`);
  }

  const isPng = data.length >= 33 && data.subarray(0, 8).equals(PNG_MAGIC);
  if (isPng) {
    const ihdrType = data.subarray(12, 16).toString("ascii");
    if (ihdrType !== "IHDR") {
      throw new Error("Malformed PNG: missing IHDR chunk");
    }
    const width = data.readUInt32BE(16);
    const height = data.readUInt32BE(20);
    if (width < 1 || height < 1 || width > MAX_DIMENSION || height > MAX_DIMENSION) {
      throw new Error(`PNG dimensions ${width}x${height} exceed ${MAX_DIMENSION}x${MAX_DIMENSION}`);
    }
    if (!data.subarray(data.length - 8).equals(PNG_IEND)) {
      throw new Error("Malformed PNG: missing trailing IEND chunk");
    }
    return;
  }

  const isJpeg =
    data.length >= 4 &&
    data[0] === 0xff &&
    data[1] === 0xd8 &&
    data[2] === 0xff &&
    data[data.length - 2] === 0xff &&
    data[data.length - 1] === 0xd9;
  if (!isJpeg) {
    throw new Error("entry.png is neither a complete PNG nor a complete JPEG");
  }
}

function main(): void {
  const repoDir = dirname(fileURLToPath(import.meta.url));
  const sourceImage = join(repoDir, "entry.png");
  const rawOutputDir = process.env.MAKEFUN_OUTPUT_DIR;
  const outputDir = rawOutputDir && rawOutputDir.trim().length > 0 ? rawOutputDir.trim() : "/output";
  const targetImage = join(outputDir, "entry.png");

  const payload = readFileSync(sourceImage);
  validateImage(payload);

  mkdirSync(outputDir, { recursive: true });
  writeFileSync(targetImage, payload);
}

try {
  main();
} catch (err) {
  const message = err instanceof Error ? err.message : String(err);
  process.stderr.write(`main.ts failed: ${message}\n`);
  process.exit(1);
}
