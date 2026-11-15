// Minimal Python syntax highlighter -> HTML string (input is escaped first).
const KW = new Set(
  'and as assert async await break class continue def del elif else except False finally for from global if import in is lambda None nonlocal not or pass raise return True try while with yield'.split(' '),
)

function esc(s: string) {
  return s.replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;')
}

const TOKEN = /(#[^\n]*)|("""[\s\S]*?"""|'''[\s\S]*?'''|"(?:\\.|[^"\\\n])*"|'(?:\\.|[^'\\\n])*')|(\b\d+(?:\.\d+)?(?:e[+-]?\d+)?\b)|([A-Za-z_][A-Za-z0-9_]*)(?=\s*\()|([A-Za-z_][A-Za-z0-9_]*)/g

export function highlightPython(code: string): string {
  let out = ''
  let last = 0
  for (const m of code.matchAll(TOKEN)) {
    const i = m.index ?? 0
    out += esc(code.slice(last, i))
    const [tok, com, str, num, fn, word] = m
    if (com) out += `<span class="com">${esc(com)}</span>`
    else if (str) out += `<span class="str">${esc(str)}</span>`
    else if (num) out += `<span class="num">${esc(num)}</span>`
    else if (fn) out += KW.has(fn) ? `<span class="kw">${fn}</span>` : `<span class="fn">${fn}</span>`
    else if (word) out += KW.has(word) ? `<span class="kw">${word}</span>` : esc(word)
    else out += esc(tok)
    last = i + tok.length
  }
  out += esc(code.slice(last))
  return out
}
