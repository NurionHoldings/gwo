import fs from 'node:fs/promises';
import path from 'node:path';
import { fileURLToPath } from 'node:url';
import fg from 'fast-glob';
import CleanCSS from 'clean-css';
import { minify as minifyHtml } from 'html-minifier-terser';
import JavaScriptObfuscator from 'javascript-obfuscator';
import { minify as minifyJs } from 'terser';

const __dirname = path.dirname(fileURLToPath(import.meta.url));
const ROOT = path.resolve(__dirname, '..');
const DIST = path.join(ROOT, 'dist');

const OBFUSCATOR_OPTIONS = {
  compact: true,
  controlFlowFlattening: false,
  deadCodeInjection: false,
  debugProtection: false,
  disableConsoleOutput: false,
  identifierNamesGenerator: 'hexadecimal',
  numbersToExpressions: false,
  renameGlobals: false,
  reservedNames: ['^GWO_I18N$', '^window$', '^document$'],
  selfDefending: false,
  simplify: true,
  splitStrings: false,
  stringArray: true,
  stringArrayCallsTransform: false,
  stringArrayEncoding: ['base64'],
  stringArrayThreshold: 0.75,
  transformObjectKeys: false,
  unicodeEscapeSequence: false,
};

const HTML_MINIFY_OPTIONS = {
  collapseWhitespace: true,
  conservativeCollapse: true,
  decodeEntities: true,
  minifyCSS: true,
  minifyJS: false,
  removeComments: true,
  removeRedundantAttributes: true,
  removeScriptTypeAttributes: true,
  removeStyleLinkTypeAttributes: true,
  sortAttributes: true,
  sortClassName: true,
};

async function ensureDir(dir) {
  await fs.mkdir(dir, { recursive: true });
}

async function writeFile(relPath, content) {
  const target = path.join(DIST, relPath);
  await ensureDir(path.dirname(target));
  await fs.writeFile(target, content, 'utf8');
}

function minifyCss(source) {
  const result = new CleanCSS({ level: 2 }).minify(source);
  if (result.errors.length) {
    throw new Error(`CSS minify failed: ${result.errors.join('; ')}`);
  }
  return result.styles;
}

async function protectJs(source, label) {
  const terserResult = await minifyJs(source, {
    compress: true,
    mangle: false,
    format: { comments: false },
  });
  if (terserResult.error) {
    throw new Error(`Terser failed (${label}): ${terserResult.error.message}`);
  }

  const obfuscated = JavaScriptObfuscator.obfuscate(
    terserResult.code,
    OBFUSCATOR_OPTIONS,
  );
  return obfuscated.getObfuscatedCode();
}

async function processInlineScripts(html) {
  const scriptRegex = /<script(?![^>]*\bsrc\b)[^>]*>([\s\S]*?)<\/script>/gi;
  let index = 0;
  const blocks = [];

  const withPlaceholders = html.replace(scriptRegex, (match, code) => {
    const trimmed = code.trim();
    if (!trimmed) return match;
    const placeholder = `<!--__INLINE_SCRIPT_${index}__-->`;
    blocks.push(trimmed);
    index += 1;
    return placeholder;
  });

  const obfuscatedBlocks = [];
  for (let i = 0; i < blocks.length; i += 1) {
    obfuscatedBlocks.push(await protectJs(blocks[i], `inline-script-${i}`));
  }

  let processed = withPlaceholders;
  obfuscatedBlocks.forEach((code, i) => {
    processed = processed.replace(
      `<!--__INLINE_SCRIPT_${i}__-->`,
      `<script>${code}</script>`,
    );
  });

  return minifyHtml(processed, HTML_MINIFY_OPTIONS);
}

async function copyBinaryAndStatic() {
  const patterns = [
    'assets/**/*.png',
    'robots.txt',
    'sitemap.xml',
  ];

  const files = await fg(patterns, { cwd: ROOT, onlyFiles: true });
  for (const rel of files) {
    const source = path.join(ROOT, rel);
    const target = path.join(DIST, rel);
    await ensureDir(path.dirname(target));
    await fs.copyFile(source, target);
  }
}

async function minifyLocales() {
  const files = await fg('assets/locales/*.json', { cwd: ROOT, onlyFiles: true });
  for (const rel of files) {
    const raw = await fs.readFile(path.join(ROOT, rel), 'utf8');
    const json = JSON.stringify(JSON.parse(raw));
    await writeFile(rel, json);
  }
}

async function minifyJsOnly(source, label) {
  const terserResult = await minifyJs(source, {
    compress: true,
    mangle: false,
    format: { comments: false },
  });
  if (terserResult.error) {
    throw new Error(`Terser failed (${label}): ${terserResult.error.message}`);
  }
  return terserResult.code;
}

async function buildAssets() {
  const cssFiles = ['assets/site.css', 'assets/logo-animated.css'];
  for (const rel of cssFiles) {
    const source = await fs.readFile(path.join(ROOT, rel), 'utf8');
    await writeFile(rel, minifyCss(source));
  }

  const i18nSource = await fs.readFile(path.join(ROOT, 'assets/i18n.js'), 'utf8');
  await writeFile('assets/i18n.js', await protectJs(i18nSource, 'assets/i18n.js'));

  // Chart.js 연동 스크립트는 API 호환을 위해 미니파이만 적용
  const chartsSource = await fs.readFile(path.join(ROOT, 'assets/policy-brief-charts.js'), 'utf8');
  await writeFile(
    'assets/policy-brief-charts.js',
    await minifyJsOnly(chartsSource, 'assets/policy-brief-charts.js'),
  );
}

async function buildHtml() {
  const files = await fg(['*.html', '404.html'], { cwd: ROOT, onlyFiles: true });
  for (const rel of files) {
    let html = await fs.readFile(path.join(ROOT, rel), 'utf8');
    html = html.replace(/logo-animated\.css\?v=\d+/g, 'logo-animated.css?v=9');
    const output = await processInlineScripts(html);
    await writeFile(rel, output);
  }
}

async function main() {
  console.log('Building dist/ ...');
  await ensureDir(DIST);
  await copyBinaryAndStatic();
  await minifyLocales();
  await buildAssets();
  await buildHtml();
  console.log('Build complete → dist/');
}

main().catch((error) => {
  console.error(error);
  process.exit(1);
});
