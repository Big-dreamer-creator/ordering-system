// 前端自检脚本：校验所有 JSON 能否解析、所有 JS 语法是否正确
// 运行：bun run check
import { readdirSync, readFileSync } from "node:fs";
import { extname, join } from "node:path";

const ROOT = join(import.meta.dir, "..");
const IGNORE = new Set(["node_modules", ".git"]);

function walk(dir) {
  const files = [];
  for (const entry of readdirSync(dir, { withFileTypes: true })) {
    if (entry.name.startsWith(".") || IGNORE.has(entry.name)) {
      continue;
    }
    const full = join(dir, entry.name);
    if (entry.isDirectory()) {
      files.push(...walk(full));
    } else {
      files.push(full);
    }
  }
  return files;
}

const files = walk(ROOT);
const transpiler = new Bun.Transpiler({ loader: "js" });
let failed = 0;

for (const file of files.filter((f) => extname(f) === ".json")) {
  try {
    JSON.parse(readFileSync(file, "utf8"));
  } catch (err) {
    failed++;
    console.error("JSON 解析失败:", file, "->", err.message);
  }
}

for (const file of files.filter((f) => extname(f) === ".js")) {
  try {
    // 只编译不执行，用来检查语法（同时支持 CommonJS 和 ESM）
    transpiler.transformSync(readFileSync(file, "utf8"));
  } catch (err) {
    failed++;
    console.error("JS 语法错误:", file, "->", err.message);
  }
}

if (failed > 0) {
  console.error(`检查失败：${failed} 个文件有问题`);
  process.exit(1);
}

console.log(`检查通过：共 ${files.length} 个文件`);
