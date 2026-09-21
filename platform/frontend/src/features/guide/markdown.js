/** Minimal markdown -> HTML for Guide tab (no extra dependency except Mermaid). */

function escapeHtml(text) {
  return String(text)
    .replace(/&/g, '&amp;')
    .replace(/</g, '&lt;')
    .replace(/>/g, '&gt;')
    .replace(/"/g, '&quot;');
}

function inlineFormat(text) {
  let s = escapeHtml(text);
  s = s.replace(/`([^`]+)`/g, '<code>$1</code>');
  s = s.replace(/\*\*([^*]+)\*\*/g, '<strong>$1</strong>');
  s = s.replace(/\[([^\]]+)\]\(([^)]+)\)/g, '<a href="$2" rel="noopener">$1</a>');
  return s;
}

function slugify(text) {
  return String(text || '')
    .toLowerCase()
    .replace(/<[^>]+>/g, '')
    .replace(/&[a-z]+;/g, '')
    .replace(/[^a-z0-9]+/g, '-')
    .replace(/^-+|-+$/g, '')
    .slice(0, 80) || 'section';
}

function uniqueSlug(base, used) {
  let slug = base;
  let n = 2;
  while (used.has(slug)) {
    slug = `${base}-${n}`;
    n += 1;
  }
  used.add(slug);
  return slug;
}

/**
 * Turn flat block HTML into a readable page: title + lede, on-page TOC,
 * and one card per ## section (with optional ### subsections).
 */
function structureGuideHtml(blocks) {
  if (!blocks.length) return '';

  const usedSlugs = new Set();
  const pieces = [];
  let i = 0;

  // Title
  let titleHtml = '';
  if (blocks[i] && /^<h1[\s>]/.test(blocks[i])) {
    titleHtml = blocks[i];
    i += 1;
  }

  // Intro under the title (before first h2)
  const lede = [];
  while (i < blocks.length && !/^<h2[\s>]/.test(blocks[i])) {
    lede.push(blocks[i]);
    i += 1;
  }

  // Collect h2 sections for TOC + body
  const sections = [];
  while (i < blocks.length) {
    if (!/^<h2[\s>]/.test(blocks[i])) {
      // Orphan content after a section: attach to previous or lede
      if (sections.length) sections[sections.length - 1].raw.push(blocks[i]);
      else lede.push(blocks[i]);
      i += 1;
      continue;
    }
    const heading = blocks[i];
    const titleMatch = heading.match(/^<h2[^>]*>([\s\S]*)<\/h2>$/);
    const titleText = titleMatch ? titleMatch[1].replace(/<[^>]+>/g, '') : 'Section';
    const slug = uniqueSlug(slugify(titleText), usedSlugs);
    i += 1;
    const raw = [];
    while (i < blocks.length && !/^<h2[\s>]/.test(blocks[i])) {
      raw.push(blocks[i]);
      i += 1;
    }
    sections.push({ slug, titleText, heading, raw });
  }

  if (titleHtml || lede.length) {
    pieces.push('<header class="guide-md-header">');
    if (titleHtml) pieces.push(titleHtml);
    if (lede.length) {
      pieces.push(`<div class="guide-md-lede">${lede.join('\n')}</div>`);
    }
    pieces.push('</header>');
  }

  if (sections.length >= 2) {
    pieces.push('<nav class="guide-toc" aria-label="On this page">');
    pieces.push('<div class="guide-toc-label">On this page</div>');
    pieces.push('<ol class="guide-toc-list">');
    sections.forEach((sec, idx) => {
      pieces.push(
        `<li><a class="guide-toc-link" href="#${sec.slug}" data-guide-anchor="${sec.slug}">` +
          `<span class="guide-toc-index">${idx + 1}</span>` +
          `<span class="guide-toc-text">${escapeHtml(sec.titleText)}</span>` +
          `</a></li>`,
      );
    });
    pieces.push('</ol></nav>');
  }

  sections.forEach((sec, idx) => {
    pieces.push(
      `<section class="guide-section" id="${sec.slug}" data-guide-section="${sec.slug}">`,
    );
    pieces.push('<div class="guide-section-head">');
    pieces.push(`<span class="guide-section-index" aria-hidden="true">${idx + 1}</span>`);
    pieces.push(sec.heading.replace(/^<h2/, `<h2 id="${sec.slug}-title"`));
    pieces.push('</div>');
    pieces.push(`<div class="guide-section-body">${wrapSubsections(sec.raw, usedSlugs).join('\n')}</div>`);
    pieces.push('</section>');
  });

  return pieces.join('\n');
}

/** Group ### blocks into guide-subsection cards inside a section body. */
function wrapSubsections(blocks, usedSlugs) {
  if (!blocks.length) return [];
  const out = [];
  let i = 0;
  const preface = [];
  while (i < blocks.length && !/^<h3[\s>]/.test(blocks[i])) {
    preface.push(blocks[i]);
    i += 1;
  }
  if (preface.length) out.push(...preface);

  while (i < blocks.length) {
    if (!/^<h3[\s>]/.test(blocks[i])) {
      out.push(blocks[i]);
      i += 1;
      continue;
    }
    const heading = blocks[i];
    const titleMatch = heading.match(/^<h3[^>]*>([\s\S]*)<\/h3>$/);
    const titleText = titleMatch ? titleMatch[1].replace(/<[^>]+>/g, '') : 'Subsection';
    const slug = uniqueSlug(slugify(titleText), usedSlugs);
    i += 1;
    const body = [];
    while (i < blocks.length && !/^<h3[\s>]/.test(blocks[i])) {
      body.push(blocks[i]);
      i += 1;
    }
    out.push(`<div class="guide-subsection" id="${slug}">`);
    out.push(heading.replace(/^<h3/, `<h3 id="${slug}-title"`));
    if (body.length) out.push(`<div class="guide-subsection-body">${body.join('\n')}</div>`);
    out.push('</div>');
  }
  return out;
}

export function renderMarkdown(md) {
  const lines = String(md || '').replace(/\r\n/g, '\n').split('\n');
  const out = [];
  let i = 0;
  let inCode = false;
  let codeLang = '';
  let codeBuf = [];
  let inTable = false;
  let tableBuf = [];

  function flushTable() {
    if (!tableBuf.length) return;
    const rows = tableBuf.filter((r) => !/^\s*\|?\s*-/.test(r));
    out.push('<div class="guide-table-wrap"><table>');
    rows.forEach((row, idx) => {
      const cells = row.replace(/^\|/, '').replace(/\|$/, '').split('|').map((c) => c.trim());
      const tag = idx === 0 ? 'th' : 'td';
      out.push('<tr>' + cells.map((c) => `<${tag}>${inlineFormat(c)}</${tag}>`).join('') + '</tr>');
    });
    out.push('</table></div>');
    tableBuf = [];
    inTable = false;
  }

  function flushCode() {
    const body = codeBuf.join('\n');
    if (codeLang === 'mermaid') {
      out.push(
        `<div class="guide-mermaid"><pre class="mermaid">${escapeHtml(body)}</pre></div>`,
      );
    } else {
      out.push(`<pre><code>${escapeHtml(body)}</code></pre>`);
    }
    codeBuf = [];
    codeLang = '';
    inCode = false;
  }

  while (i < lines.length) {
    const line = lines[i];
    if (line.startsWith('```')) {
      if (inCode) {
        flushCode();
      } else {
        if (inTable) flushTable();
        inCode = true;
        codeLang = line.slice(3).trim().toLowerCase();
      }
      i += 1;
      continue;
    }
    if (inCode) {
      codeBuf.push(line);
      i += 1;
      continue;
    }
    if (line.trim().startsWith('|')) {
      inTable = true;
      tableBuf.push(line);
      i += 1;
      continue;
    }
    if (inTable) flushTable();

    if (/^#### /.test(line)) out.push(`<h4>${inlineFormat(line.slice(5))}</h4>`);
    else if (/^### /.test(line)) out.push(`<h3>${inlineFormat(line.slice(4))}</h3>`);
    else if (/^## /.test(line)) out.push(`<h2>${inlineFormat(line.slice(3))}</h2>`);
    else if (/^# /.test(line)) out.push(`<h1>${inlineFormat(line.slice(2))}</h1>`);
    else if (/^[-*] /.test(line)) {
      const items = [];
      while (i < lines.length && /^[-*] /.test(lines[i])) {
        items.push(`<li>${inlineFormat(lines[i].slice(2))}</li>`);
        i += 1;
      }
      out.push(`<ul>${items.join('')}</ul>`);
      continue;
    } else if (/^\d+\. /.test(line)) {
      const items = [];
      while (i < lines.length && /^\d+\. /.test(lines[i])) {
        items.push(`<li>${inlineFormat(lines[i].replace(/^\d+\. /, ''))}</li>`);
        i += 1;
      }
      out.push(`<ol>${items.join('')}</ol>`);
      continue;
    } else if (line.trim() === '') {
      // skip blank lines between blocks
    } else out.push(`<p>${inlineFormat(line)}</p>`);
    i += 1;
  }
  if (inCode) flushCode();
  if (inTable) flushTable();

  return structureGuideHtml(out.filter(Boolean));
}
