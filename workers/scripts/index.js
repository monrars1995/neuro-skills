// Cloudflare Worker - scripts.goldneuron.io
// Neuro Skills Installation Scripts Server

const SCRIPTS = {
  'install.sh': 'install.sh',
  'install-claude-code.sh': 'scripts/install-claude-code.sh',
  'install-opencode.sh': 'scripts/install-opencode.sh',
  'install-antigravity.sh': 'scripts/install-antigravity.sh',
  'install-cursor.sh': 'scripts/install-cursor.sh',
  'install-gemini.sh': 'scripts/install-gemini.sh',
  'install-codex.sh': 'scripts/install-codex.sh'
};

export default {
  async fetch(request, env, ctx) {
    const url = new URL(request.url);
    const path = url.pathname.slice(1);
    
    const corsHeaders = {
      'Access-Control-Allow-Origin': '*',
      'Access-Control-Allow-Methods': 'GET, OPTIONS',
      'Access-Control-Allow-Headers': 'Content-Type',
      'Access-Control-Max-Age': '86400'
    };
    
    if (request.method === 'OPTIONS') {
      return new Response(null, { headers: corsHeaders });
    }
    
    if (path === '' || path === '/') {
      return new Response(getIndexPage(), {
        headers: {
          'Content-Type': 'text/html; charset=utf-8',
          ...corsHeaders
        }
      });
    }
    
    if (path === 'api/npm') {
      const npmData = {
        name: '@goldneuronio/neuro-skills',
        version: '2.3.1',
        description: 'O bastidor técnico que o mercado não mostra - Framework de automação de Meta Ads',
        author: '@monrars',
        license: 'MIT',
        homepage: 'https://goldneuron.io/',
        repository: 'https://github.com/monrars1995/neuro-skills',
        install: 'npm install -g @goldneuronio/neuro-skills',
        npx: 'npx @goldneuronio/neuro-skills start'
      };
      
      return new Response(JSON.stringify(npmData, null, 2), {
        headers: {
          'Content-Type': 'application/json',
          ...corsHeaders
        }
      });
    }
    
    const scriptPath = SCRIPTS[path];
    if (!scriptPath) {
      return new Response('Not Found', { 
        status: 404,
        headers: { 'Content-Type': 'text/plain', ...corsHeaders }
      });
    }
    
    try {
      if (env.SCRIPTS_KV) {
        const cacheKey = `script:${path}`;
        const cached = await env.SCRIPTS_KV.get(cacheKey);
        
        if (cached) {
          return new Response(cached, {
            headers: {
              'Content-Type': 'text/x-shellscript; charset=utf-8',
              'Cache-Control': 'public, max-age=3600',
              ...corsHeaders
            }
          });
        }
      }
      
      const githubUrl = `https://raw.githubusercontent.com/monrars1995/neuro-skills/beta/${scriptPath}`;
      const response = await fetch(githubUrl);
      
      if (!response.ok) {
        throw new Error(`GitHub returned ${response.status}`);
      }
      
      const content = await response.text();
      
      if (env.SCRIPTS_KV) {
        const cacheKey = `script:${path}`;
        await env.SCRIPTS_KV.put(cacheKey, content, { expirationTtl: 3600 });
      }
      
      return new Response(content, {
        headers: {
          'Content-Type': 'text/x-shellscript; charset=utf-8',
          'Cache-Control': 'public, max-age=3600',
          ...corsHeaders
        }
      });
    } catch (error) {
      console.error('Error fetching script:', error);
      
      const fallback = getFallbackScript(path);
      return new Response(fallback, {
        headers: {
          'Content-Type': 'text/x-shellscript; charset=utf-8',
          ...corsHeaders
        }
      });
    }
  }
};

function getFallbackScript(scriptName) {
  return `#!/bin/bash
# Neuro Skills - ${scriptName}
# Fallback script - fetching from npm...

npm install -g @goldneuronio/neuro-skills

echo ""
echo "✅ Instalado! Execute: neuro-skills --help"
echo "📚 Documentação: https://goldneuron.io/"
`;
}

function getIndexPage() {
  return `<!DOCTYPE html>
<html lang="pt-BR">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Neuro Skills // Installation Scripts</title>
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link href="https://fonts.googleapis.com/css2?family=JetBrains+Mono:wght@400;500;600;700&family=Inter:wght@400;500;600;700&display=swap" rel="stylesheet">
  <style>
    :root {
      --bg-primary: #0a0a0f;
      --bg-secondary: #12121a;
      --bg-tertiary: #1a1a25;
      --gold-primary: #d4af37;
      --gold-secondary: #c9a227;
      --gold-light: #f4d03f;
      --gold-dark: #8b7355;
      --text-primary: #e8e8e8;
      --text-secondary: #9898a6;
      --text-muted: #5a5a6e;
      --border-color: #2a2a3a;
      --success: #4ade80;
      --terminal-green: #22c55e;
    }

    * {
      margin: 0;
      padding: 0;
      box-sizing: border-box;
    }

    body {
      font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
      background: var(--bg-primary);
      color: var(--text-primary);
      min-height: 100vh;
      overflow-x: hidden;
    }

    .terminal-container {
      max-width: 1200px;
      margin: 0 auto;
      padding: 2rem;
      min-height: 100vh;
      display: flex;
      flex-direction: column;
    }

    /* Header */
    .terminal-header {
      background: linear-gradient(135deg, var(--bg-secondary) 0%, var(--bg-tertiary) 100%);
      border: 1px solid var(--border-color);
      border-radius: 16px 16px 0 0;
      padding: 1.5rem 2rem;
      position: relative;
      overflow: hidden;
    }

    .terminal-header::before {
      content: '';
      position: absolute;
      top: 0;
      left: 0;
      right: 0;
      height: 3px;
      background: linear-gradient(90deg, var(--gold-primary), var(--gold-light), var(--gold-primary));
    }

    .window-controls {
      display: flex;
      gap: 8px;
      margin-bottom: 1rem;
    }

    .window-dot {
      width: 12px;
      height: 12px;
      border-radius: 50%;
      opacity: 0.8;
    }

    .window-dot.red { background: #ff5f56; }
    .window-dot.yellow { background: #ffbd2e; }
    .window-dot.green { background: var(--terminal-green); }

    .header-content {
      text-align: center;
    }

    .logo {
      font-family: 'JetBrains Mono', monospace;
      font-size: 2.5rem;
      font-weight: 700;
      background: linear-gradient(135deg, var(--gold-primary), var(--gold-light), var(--gold-secondary));
      -webkit-background-clip: text;
      -webkit-text-fill-color: transparent;
      background-clip: text;
      margin-bottom: 0.5rem;
    }

    .tagline {
      color: var(--text-secondary);
      font-size: 1rem;
      font-family: 'JetBrains Mono', monospace;
    }

    .tagline::before {
      content: '> ';
      color: var(--gold-primary);
    }

    .cursor {
      display: inline-block;
      width: 10px;
      height: 1.2em;
      background: var(--gold-primary);
      animation: blink 1s infinite;
      vertical-align: middle;
      margin-left: 2px;
    }

    @keyframes blink {
      0%, 50% { opacity: 1; }
      51%, 100% { opacity: 0; }
    }

    /* Main Content */
    .terminal-body {
      background: var(--bg-secondary);
      border: 1px solid var(--border-color);
      border-top: none;
      padding: 2rem;
    }

    /* Section Styles */
    .section {
      margin-bottom: 2rem;
    }

    .section-header {
      display: flex;
      align-items: center;
      gap: 0.75rem;
      margin-bottom: 1.5rem;
    }

    .section-icon {
      font-size: 1.25rem;
    }

    .section-title {
      font-family: 'JetBrains Mono', monospace;
      font-size: 1rem;
      color: var(--gold-primary);
      font-weight: 600;
    }

    /* Code Block */
    .code-block {
      background: var(--bg-primary);
      border: 1px solid var(--border-color);
      border-radius: 12px;
      overflow: hidden;
      margin-bottom: 1rem;
    }

    .code-header {
      background: var(--bg-tertiary);
      padding: 0.5rem 1rem;
      border-bottom: 1px solid var(--border-color);
      display: flex;
      align-items: center;
      gap: 0.5rem;
    }

    .code-header-text {
      font-family: 'JetBrains Mono', monospace;
      font-size: 0.75rem;
      color: var(--text-muted);
    }

    .code-content {
      padding: 1.25rem;
      font-family: 'JetBrains Mono', monospace;
      font-size: 0.9rem;
      color: var(--text-primary);
      line-height: 1.6;
      overflow-x: auto;
    }

    .prompt {
      color: var(--gold-primary);
      font-weight: 600;
    }

    .command {
      color: var(--text-primary);
    }

    /* Platform Grid */
    .platforms-grid {
      display: grid;
      grid-template-columns: repeat(auto-fit, minmax(340px, 1fr));
      gap: 1rem;
    }

    .platform-card {
      background: var(--bg-primary);
      border: 1px solid var(--border-color);
      border-radius: 12px;
      overflow: hidden;
      transition: all 0.3s ease;
    }

    .platform-card:hover {
      border-color: var(--gold-primary);
      box-shadow: 0 0 20px rgba(212, 175, 55, 0.1);
      transform: translateY(-2px);
    }

    .platform-header {
      background: var(--bg-tertiary);
      padding: 1rem;
      border-bottom: 1px solid var(--border-color);
      display: flex;
      align-items: center;
      gap: 0.75rem;
    }

    .platform-icon {
      font-size: 1.5rem;
    }

    .platform-name {
      font-family: 'JetBrains Mono', monospace;
      font-weight: 600;
      color: var(--gold-light);
    }

    .platform-code {
      padding: 1rem;
      font-family: 'JetBrains Mono', monospace;
      font-size: 0.8rem;
      color: var(--text-secondary);
      line-height: 1.5;
      overflow-x: auto;
    }

    .copy-hint {
      padding: 0.75rem 1rem;
      background: var(--bg-tertiary);
      border-top: 1px solid var(--border-color);
      font-size: 0.75rem;
      color: var(--text-muted);
      text-align: center;
      cursor: pointer;
      transition: all 0.2s ease;
    }

    .copy-hint:hover {
      background: var(--bg-secondary);
      color: var(--gold-primary);
    }

    /* Footer */
    .terminal-footer {
      background: var(--bg-tertiary);
      border: 1px solid var(--border-color);
      border-top: none;
      border-radius: 0 0 16px 16px;
      padding: 1.5rem 2rem;
      display: flex;
      justify-content: center;
      align-items: center;
      gap: 2rem;
      flex-wrap: wrap;
    }

    .footer-link {
      color: var(--text-secondary);
      text-decoration: none;
      font-family: 'JetBrains Mono', monospace;
      font-size: 0.85rem;
      transition: color 0.2s ease;
      display: flex;
      align-items: center;
      gap: 0.5rem;
    }

    .footer-link:hover {
      color: var(--gold-primary);
    }

    .footer-link::before {
      content: '$ ';
      color: var(--gold-primary);
      opacity: 0.5;
    }

    .creator {
      font-family: 'JetBrains Mono', monospace;
      color: var(--text-muted);
      font-size: 0.8rem;
      margin-top: 0.5rem;
      text-align: center;
      width: 100%;
    }

    .creator a {
      color: var(--gold-primary);
      text-decoration: none;
    }

    .creator a:hover {
      text-decoration: underline;
    }

    /* Animations */
    @keyframes slideIn {
      from {
        opacity: 0;
        transform: translateY(10px);
      }
      to {
        opacity: 1;
        transform: translateY(0);
      }
    }

    .platform-card {
      animation: slideIn 0.3s ease forwards;
    }

    .platform-card:nth-child(1) { animation-delay: 0.1s; }
    .platform-card:nth-child(2) { animation-delay: 0.15s; }
    .platform-card:nth-child(3) { animation-delay: 0.2s; }
    .platform-card:nth-child(4) { animation-delay: 0.25s; }
    .platform-card:nth-child(5) { animation-delay: 0.3s; }
    .platform-card:nth-child(6) { animation-delay: 0.35s; }

    /* Responsive */
    @media (max-width: 768px) {
      .terminal-container {
        padding: 1rem;
      }
      
      .logo {
        font-size: 1.75rem;
      }
      
      .platforms-grid {
        grid-template-columns: 1fr;
      }
      
      .code-content {
        font-size: 0.8rem;
      }
      
      .terminal-footer {
        flex-direction: column;
        gap: 1rem;
      }
    }

    /* Selection */
    ::selection {
      background: var(--gold-primary);
      color: var(--bg-primary);
    }
  </style>
</head>
<body>
  <div class="terminal-container">
    <header class="terminal-header">
      <div class="window-controls">
        <span class="window-dot red"></span>
        <span class="window-dot yellow"></span>
        <span class="window-dot green"></span>
      </div>
      <div class="header-content">
        <h1 class="logo">neuro-skills</h1>
        <p class="tagline">O bastidor técnico que o mercado não mostra<span class="cursor"></span></p>
      </div>
    </header>

    <main class="terminal-body">
      <!-- NPM Section -->
      <section class="section">
        <div class="section-header">
          <span class="section-icon">📦</span>
          <h2 class="section-title">npm install</h2>
        </div>
        
        <div class="code-block">
          <div class="code-header">
            <span class="code-header-text">terminal</span>
          </div>
          <div class="code-content">
            <div><span class="prompt">$</span> <span class="command">npm install -g @goldneuronio/neuro-skills</span></div>
            <div style="margin-top: 0.5rem;"><span class="prompt">$</span> <span class="command">npx @goldneuronio/neuro-skills start</span></div>
          </div>
        </div>
      </section>

      <!-- Platforms Section -->
      <section class="section">
        <div class="section-header">
          <span class="section-icon">🤖</span>
          <h2 class="section-title">plataformas</h2>
        </div>

        <div class="platforms-grid">
          <div class="platform-card">
            <div class="platform-header">
              <span class="platform-icon">🧠</span>
              <span class="platform-name">Claude Code</span>
            </div>
            <div class="platform-code">
              <div><span class="prompt">$</span> curl -fsSL https://scripts.goldneuron.io/install-claude-code.sh | bash</div>
            </div>
            <div class="copy-hint" onclick="copyToClipboard('curl -fsSL https://scripts.goldneuron.io/install-claude-code.sh | bash')">📋 copiar comando</div>
          </div>

          <div class="platform-card">
            <div class="platform-header">
              <span class="platform-icon">⚡</span>
              <span class="platform-name">OpenCode</span>
            </div>
            <div class="platform-code">
              <div><span class="prompt">$</span> curl -fsSL https://scripts.goldneuron.io/install-opencode.sh | bash</div>
            </div>
            <div class="copy-hint" onclick="copyToClipboard('curl -fsSL https://scripts.goldneuron.io/install-opencode.sh | bash')">📋 copiar comando</div>
          </div>

          <div class="platform-card">
            <div class="platform-header">
              <span class="platform-icon">✨</span>
              <span class="platform-name">Cursor</span>
            </div>
            <div class="platform-code">
              <div><span class="prompt">$</span> curl -fsSL https://scripts.goldneuron.io/install-cursor.sh | bash</div>
            </div>
            <div class="copy-hint" onclick="copyToClipboard('curl -fsSL https://scripts.goldneuron.io/install-cursor.sh | bash')">📋 copiar comando</div>
          </div>

          <div class="platform-card">
            <div class="platform-header">
              <span class="platform-icon">💎</span>
              <span class="platform-name">Gemini CLI</span>
            </div>
            <div class="platform-code">
              <div><span class="prompt">$</span> curl -fsSL https://scripts.goldneuron.io/install-gemini.sh | bash</div>
            </div>
            <div class="copy-hint" onclick="copyToClipboard('curl -fsSL https://scripts.goldneuron.io/install-gemini.sh | bash')">📋 copiar comando</div>
          </div>

          <div class="platform-card">
            <div class="platform-header">
              <span class="platform-icon">🤖</span>
              <span class="platform-name">OpenAI Codex</span>
            </div>
            <div class="platform-code">
              <div><span class="prompt">$</span> curl -fsSL https://scripts.goldneuron.io/install-codex.sh | bash</div>
            </div>
            <div class="copy-hint" onclick="copyToClipboard('curl -fsSL https://scripts.goldneuron.io/install-codex.sh | bash')">📋 copiar comando</div>
          </div>

          <div class="platform-card">
            <div class="platform-header">
              <span class="platform-icon">🚀</span>
              <span class="platform-name">Antigravity</span>
            </div>
            <div class="platform-code">
              <div><span class="prompt">$</span> curl -fsSL https://scripts.goldneuron.io/install-antigravity.sh | bash</div>
            </div>
            <div class="copy-hint" onclick="copyToClipboard('curl -fsSL https://scripts.goldneuron.io/install-antigravity.sh | bash')">📋 copiar comando</div>
          </div>
        </div>
      </section>
    </main>

    <footer class="terminal-footer">
      <a href="https://goldneuron.io/" class="footer-link" target="_blank">🌐 site</a>
      <a href="https://goldneuron.io/drops" class="footer-link" target="_blank">📧 newsletter</a>
      <a href="https://github.com/monrars1995/neuro-skills" class="footer-link" target="_blank">📦 github</a>
      <a href="https://www.npmjs.com/package/@goldneuronio/neuro-skills" class="footer-link" target="_blank">⬡ npm</a>
      <a href="https://instagram.com/monrars" class="footer-link" target="_blank">📸 instagram</a>
      <p class="creator">feito com ❤️ por <a href="https://instagram.com/monrars" target="_blank">@monrars</a></p>
    </footer>
  </div>

  <script>
    function copyToClipboard(text) {
      navigator.clipboard.writeText(text).then(() => {
        // Show brief feedback
        const hints = document.querySelectorAll('.copy-hint');
        hints.forEach(hint => {
          if (hint.onclick.toString().includes(text)) {
            const original = hint.textContent;
            hint.textContent = '✓ copiado!';
            hint.style.color = '#4ade80';
            setTimeout(() => {
              hint.textContent = original;
              hint.style.color = '';
            }, 1500);
          }
        });
      });
    }
  </script>
</body>
</html>`;
}