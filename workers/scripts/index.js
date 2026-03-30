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

const CONTENT_TYPES = {
  'sh': 'text/x-shellscript',
  'md': 'text/markdown',
  'json': 'application/json'
};

export default {
  async fetch(request, env, ctx) {
    const url = new URL(request.url);
    const path = url.pathname.slice(1);
    
    // CORS headers
    const corsHeaders = {
      'Access-Control-Allow-Origin': '*',
      'Access-Control-Allow-Methods': 'GET, OPTIONS',
      'Access-Control-Allow-Headers': 'Content-Type',
      'Access-Control-Max-Age': '86400'
    };
    
    // Handle OPTIONS for CORS
    if (request.method === 'OPTIONS') {
      return new Response(null, { headers: corsHeaders });
    }
    
    // Root path - show index
    if (path === '' || path === '/') {
      return new Response(getIndexPage(), {
        headers: {
          'Content-Type': 'text/html; charset=utf-8',
          ...corsHeaders
        }
      });
    }
    
    // API endpoint for npm info
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
    
    // Get script content from KV orGitHub
    const scriptPath = SCRIPTS[path];
    if (!scriptPath) {
      return new Response('Not Found', { 
        status: 404,
        headers: { 'Content-Type': 'text/plain', ...corsHeaders }
      });
    }
    
    try {
      // Try to get from KV cache first
      const cacheKey = `script:${path}`;
      const cached = await env.SCRIPTS_KV?.get(cacheKey);
      
      if (cached) {
        return new Response(cached, {
          headers: {
            'Content-Type': 'text/x-shellscript; charset=utf-8',
            'Cache-Control': 'public, max-age=3600',
            ...corsHeaders
          }
        });
      }
      
      // Fetch from GitHub
      const githubUrl = `https://raw.githubusercontent.com/monrars1995/neuro-skills/beta/${scriptPath}`;
      const response = await fetch(githubUrl);
      
      if (!response.ok) {
        throw new Error(`GitHub returned ${response.status}`);
      }
      
      const content = await response.text();
      
      // Cache in KV for 1 hour
      await env.SCRIPTS_KV?.put(cacheKey, content, { expirationTtl: 3600 });
      
      return new Response(content, {
        headers: {
          'Content-Type': 'text/x-shellscript; charset=utf-8',
          'Cache-Control': 'public, max-age=3600',
          ...corsHeaders
        }
      });
    } catch (error) {
      console.error('Error fetching script:', error);
      
      // Return fallback script
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
  <title>Neuro Skills - Installation Scripts</title>
  <style>
    * { margin: 0; padding: 0; box-sizing: border-box; }
    body {
      font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Oxygen, Ubuntu, sans-serif;
      background: linear-gradient(135deg, #0f0f23 0%, #1a1a3e 100%);
      color: #e0e0e0;
      min-height: 100vh;
      padding: 2rem;
    }
    .container {
      max-width: 900px;
      margin: 0 auto;
    }
    header {
      text-align: center;
      margin-bottom: 3rem;
    }
    h1 {
      font-size: 2.5rem;
      background: linear-gradient(135deg, #60a5fa, #a78bfa);
      -webkit-background-clip: text;
      -webkit-text-fill-color: transparent;
      margin-bottom: 0.5rem;
    }
    .subtitle {
      color: #888;
      font-size: 1.1rem;
    }
    .links {
      display: grid;
      grid-template-columns: repeat(auto-fit, minmax(280px, 1fr));
      gap: 1rem;
      margin-bottom: 2rem;
    }
    .link-card {
      background: rgba(255, 255, 255, 0.05);
      border: 1px solid rgba(255, 255, 255, 0.1);
      border-radius: 12px;
      padding: 1.5rem;
      transition: all 0.3s ease;
    }
    .link-card:hover {
      background: rgba(255, 255, 255, 0.1);
      border-color: #60a5fa;
      transform: translateY(-2px);
    }
    .link-card h3 {
      color: #60a5fa;
      margin-bottom: 0.5rem;
    }
    .link-card code {
      display: block;
      background: rgba(0, 0, 0, 0.3);
      padding: 0.75rem;
      border-radius: 6px;
      font-size: 0.85rem;
      overflow-x: auto;
      white-space: nowrap;
    }
    .npm-section {
      background: rgba(96, 165, 250, 0.1);
      border: 1px solid #60a5fa;
      border-radius: 12px;
      padding: 2rem;
      margin-bottom: 2rem;
    }
    .npm-section h2 {
      color: #60a5fa;
      margin-bottom: 1rem;
    }
    .npm-section code {
      display: block;
      background: rgba(0, 0, 0, 0.3);
      padding: 1rem;
      border-radius: 6px;
      margin-bottom: 1rem;
      font-size: 1rem;
    }
    footer {
      text-align: center;
      color: #666;
      margin-top: 3rem;
    }
    footer a {
      color: #60a5fa;
      text-decoration: none;
    }
    footer a:hover {
      text-decoration: underline;
    }
  </style>
</head>
<body>
  <div class="container">
    <header>
      <h1>🧠 Neuro Skills</h1>
      <p class="subtitle">O bastidor técnico que o mercado não mostra</p>
    </header>
    
    <div class="npm-section">
      <h2>📦 Instalação via npm</h2>
      <code>npm install -g @goldneuronio/neuro-skills</code>
      <code>npx @goldneuronio/neuro-skills start</code>
    </div>
    
    <h2 style="margin-bottom: 1rem; color: #60a5fa;">🤖 Instalação por Plataforma</h2>
    
    <div class="links">
      <div class="link-card">
        <h3>Claude Code</h3>
        <code>curl -fsSL https://scripts.goldneuron.io/install-claude-code.sh | bash</code>
      </div>
      
      <div class="link-card">
        <h3>OpenCode</h3>
        <code>curl -fsSL https://scripts.goldneuron.io/install-opencode.sh | bash</code>
      </div>
      
      <div class="link-card">
        <h3>Cursor</h3>
        <code>curl -fsSL https://scripts.goldneuron.io/install-cursor.sh | bash</code>
      </div>
      
      <div class="link-card">
        <h3>Gemini CLI</h3>
        <code>curl -fsSL https://scripts.goldneuron.io/install-gemini.sh | bash</code>
      </div>
      
      <div class="link-card">
        <h3>OpenAI Codex</h3>
        <code>curl -fsSL https://scripts.goldneuron.io/install-codex.sh | bash</code>
      </div>
      
      <div class="link-card">
        <h3>Antigravity</h3>
        <code>curl -fsSL https://scripts.goldneuron.io/install-antigravity.sh | bash</code>
      </div>
    </div>
    
    <footer>
      <p>
        <a href="https://goldneuron.io/">🌐 Site Oficial</a> • 
        <a href="https://goldneuron.io/drops">📧 Newsletter</a> • 
        <a href="https://github.com/monrars1995/neuro-skills">📦 GitHub</a> • 
        <a href="https://www.npmjs.com/package/@goldneuronio/neuro-skills">📦 npm</a>
      </p>
      <p style="margin-top: 1rem;">Made with ❤️ by <a href="https://instagram.com/monrars">@monrars</a></p>
    </footer>
  </div>
</body>
</html>`;
}