/** Minimal markdown -> HTML for Guide tab (no extra dependency). */

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

export function renderMarkdown(md) {
  const lines = String(md || '').replace(/\r\n/g, '\n').split('\n');
  const out = [];
  let i = 0;
  let inCode = false;
  let codeBuf = [];
  let inTable = false;
  let tableBuf = [];

  function flushTable() {
    if (!tableBuf.length) return;
    const rows = tableBuf.filter((r) => !/^\s*\|?\s*-/.test(r));
    out.push('<table>');
    rows.forEach((row, idx) => {
      const cells = row.replace(/^\|/, '').replace(/\|$/, '').split('|').map((c) => c.trim());
      const tag = idx === 0 ? 'th' : 'td';
      out.push('<tr>' + cells.map((c) => `<${tag}>${inlineFormat(c)}</${tag}>`).join('') + '</tr>');
    });
    out.push('</table>');
    tableBuf = [];
    inTable = false;
  }

  while (i < lines.length) {
    const line = lines[i];
    if (line.startsWith('```')) {
      if (inCode) {
        out.push(`<pre><code>${escapeHtml(codeBuf.join('\n'))}</code></pre>`);
        codeBuf = [];
        inCode = false;
      } else {
        if (inTable) flushTable();
        inCode = true;
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

    if (/^### /.test(line)) out.push(`<h3>${inlineFormat(line.slice(4))}</h3>`);
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
    } else if (line.trim() === '') out.push('');
    else out.push(`<p>${inlineFormat(line)}</p>`);
    i += 1;
  }
  if (inCode) out.push(`<pre><code>${escapeHtml(codeBuf.join('\n'))}</code></pre>`);
  if (inTable) flushTable();
  return out.join('\n');
}
