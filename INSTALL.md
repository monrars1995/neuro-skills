# Instalação - Neuro Skills

Framework de automação de Meta Ads para AI Agents.

## 📦 Instalação via npm/npx

```bash
# Usar diretamente (recomendado)
npx @goldneuronio/neuro-skills start

# Instalar globalmente
npm install -g @goldneuronio/neuro-skills
neuro-skills start
```

---

## 🤖 Instalação por Plataforma

### Claude Code (Anthropic)

**Método 1: Diretório local**
```bash
# Clone o repositório
git clone https://github.com/monrars1995/neuro-skills.git
cd neuro-skills

# Instale os skills no Claude Code
cp -r meta-ads-manager ~/.claude/skills/
cp -r traffic-strategist ~/.claude/skills/
cp -r ad-copywriter ~/.claude/skills/
cp -r neuro-ads-manager ~/.claude/skills/

# Vertical agents
cp -r agents/concessionarias ~/.claude/skills/
cp -r agents/imobiliarias ~/.claude/skills/
cp -r agents/ecommerce ~/.claude/skills/
cp -r agents/educacao ~/.claude/skills/
cp -r agents/saude ~/.claude/skills/
```

**Método 2: Via npm**
```bash
# Instalar globalmente
npm install -g @goldneuronio/neuro-skills

# Os skills são instalados automaticamente em ~/.neuro-skills/skills/
# Crie symlinks para o Claude Code
ln -s ~/.neuro-skills/skills/* ~/.claude/skills/
```

**Uso:**
```
Load skill: meta-ads-manager
/meta-ads setup
```

---

### OpenCode

**Método 1: Diretório local**
```bash
# Clone o repositório
git clone https://github.com/monrars1995/neuro-skills.git
cd neuro-skills

# Instale os skills noOpenCode
cp -r meta-ads-manager ~/.opencode/skills/
cp -r traffic-strategist ~/.opencode/skills/
cp -r ad-copywriter ~/.opencode/skills/
cp -r neuro-ads-manager ~/.opencode/skills/

# Vertical agents
cp -r agents/concessionarias ~/.opencode/skills/
cp -r agents/imobiliarias ~/.opencode/skills/
cp -r agents/ecommerce ~/.opencode/skills/
cp -r agents/educacao ~/.opencode/skills/
cp -r agents/saude ~/.opencode/skills/
```

**Método 2: Via npm**
```bash
npm install -g @goldneuronio/neuro-skills
ln -s ~/.neuro-skills/skills/* ~/.opencode/skills/
```

**Uso:**
```
Load skill: meta-ads-manager
/meta-ads setup
```

---

### Antigravity

**Método 1: Diretório local**
```bash
git clone https://github.com/monrars1995/neuro-skills.git
cd neuro-skills

# Instale os skills no Antigravity
cp -r meta-ads-manager ~/.antigravity/skills/
cp -r traffic-strategist ~/.antigravity/skills/
cp -r ad-copywriter ~/.antigravity/skills/
cp -r neuro-ads-manager ~/.antigravity/skills/

# Vertical agents
cp -r agents/* ~/.antigravity/skills/
```

**Método 2: Via npm**
```bash
npm install -g @goldneuronio/neuro-skills
ln -s ~/.neuro-skills/skills/* ~/.antigravity/skills/
```

**Uso:**
```
Load skill: meta-ads-manager
/meta-ads setup
```

---

### Cursor

**Método 1: Diretório local**
```bash
git clone https://github.com/monrars1995/neuro-skills.git
cd neuro-skills

# Cursor usa o mesmo formato doVSCode
# Crie um arquivo .cursorrules na raiz do projeto

# Copie os skills para o projeto
cp -r meta-ads-manager .cursor/skills/
cp -r traffic-strategist .cursor/skills/
cp -r ad-copywriter .cursor/skills/
cp -r neuro-ads-manager .cursor/skills/

# Vertical agents
cp -r agents/concessionarias .cursor/skills/
cp -r agents/imobiliarias .cursor/skills/
cp -r agents/ecommerce .cursor/skills/
cp -r agents/educacao .cursor/skills/
cp -r agents/saude .cursor/skills/
```

**Método 2: Configuração global**
```bash
npm install -g @goldneuronio/neuro-skills

# Crie o diretório doCursor
mkdir -p ~/.cursor/skills

# Crie symlinks
ln -s ~/.neuro-skills/skills/meta-ads-manager ~/.cursor/skills/
ln -s ~/.neuro-skills/skills/traffic-strategist ~/.cursor/skills/
ln -s ~/.neuro-skills/skills/ad-copywriter ~/.cursor/skills/
ln -s ~/.neuro-skills/skills/neuro-ads-manager ~/.cursor/skills/
ln -s ~/.neuro-skills/skills/concessionarias ~/.cursor/skills/
ln -s ~/.neuro-skills/skills/imobiliarias ~/.cursor/skills/
ln -s ~/.neuro-skills/skills/ecommerce ~/.cursor/skills/
ln -s ~/.neuro-skills/skills/educacao ~/.cursor/skills/
ln -s ~/.neuro-skills/skills/saude ~/.cursor/skills/
```

**Uso:**
No Cursor,os skills são carregados automaticamente quando estão no diretório `.cursor/skills/`.

---

### Gemini CLI (Google)

**Método 1: Diretório local**
```bash
git clone https://github.com/monrars1995/neuro-skills.git
cd neuro-skills

# Instale os skills no Gemini CLI
cp -r meta-ads-manager ~/.gemini/skills/
cp -r traffic-strategist ~/.gemini/skills/
cp -r ad-copywriter ~/.gemini/skills/
cp -r neuro-ads-manager ~/.gemini/skills/

# Vertical agents
cp -r agents/concessionarias ~/.gemini/skills/
cp -r agents/imobiliarias ~/.gemini/skills/
cp -r agents/ecommerce ~/.gemini/skills/
cp -r agents/educacao ~/.gemini/skills/
cp -r agents/saude ~/.gemini/skills/
```

**Método 2: Via npm**
```bash
npm install -g @goldneuronio/neuro-skills
ln -s ~/.neuro-skills/skills/* ~/.gemini/skills/
```

**Uso:**
```
Load skill: meta-ads-manager
/meta-ads setup
```

---

### OpenAI Codex

**Método 1: Diretório local**
```bash
git clone https://github.com/monrars1995/neuro-skills.git
cd neuro-skills

# Instale os skills no Codex
cp -r meta-ads-manager ~/.codex/skills/
cp -r traffic-strategist ~/.codex/skills/
cp -r ad-copywriter ~/.codex/skills/
cp -r neuro-ads-manager ~/.codex/skills/

# Vertical agents
cp -r agents/concessionarias ~/.codex/skills/
cp -r agents/imobiliarias ~/.codex/skills/
cp -r agents/ecommerce ~/.codex/skills/
cp -r agents/educacao ~/.codex/skills/
cp -r agents/saude ~/.codex/skills/
```

**Método 2: Via npm**
```bash
npm install -g @goldneuronio/neuro-skills
ln -s ~/.neuro-skills/skills/* ~/.codex/skills/
```

**Uso:**
```
Load skill: meta-ads-manager
/meta-ads setup
```

---

## 🚀 Inicialização Rápida

### Criar novo projeto
```bash
neuro-skills init meu-projeto
cd meu-projento
```

### Configurar conta existente
```bash
neuro-skills setup
# Siga as instruções interativas
```

### Listar skills instalados
```bash
neuro-skills list
```

### Ver informações do sistema
```bash
neuro-skills info
```

---

## 📁 Estrutura de Skills

Após a instalação, os skills ficam em:

| Plataforma | Diretório |
|------------|-----------|
| Claude Code | `~/.claude/skills/` |
| OpenCode | `~/.opencode/skills/` |
| Antigravity | `~/.antigravity/skills/` |
| Cursor | `~/.cursor/skills/` |
| Gemini CLI | `~/.gemini/skills/` |
| Codex | `~/.codex/skills/` |
| npm global | `~/.neuro-skills/skills/` |

---

## 🎯 Skills Disponíveis

### Skills Core
- **meta-ads-manager** - Gerenciador completo de Meta Ads
- **traffic-strategist** - Preparação e validação de campanhas
- **ad-copywriter** - Copy on-brand para anúncios
- **neuro-ads-manager** -CRUD, Analytics e Automação

### Vertical Agents
- **concessionarias** - Automotivo (ciclo de venda 7-90 dias)
- **imobiliarias** - Imobiliário (alto ticket, geração de leads)
- **ecommerce** - E-commerce (ROAS, catálogo, funil)
- **educacao** - Educação (matrícula, sazonalidade)
- **saude** - Saúde (LGPD/HIPAA, agendamento)

---

## 📚 Documentação

- **Site**: https://goldneuron.io/
- **Comunidade**: https://goldneuron.io/drops
- **GitHub**: https://github.com/monrars1995/neuro-skills
- **npm**: https://www.npmjs.com/package/@goldneuronio/neuro-skills

---

## 🔗 Links

- Instagram: https://instagram.com/monrars
- Criador: @monrars

---

## 📄Licença

MIT - Veja [LICENSE](LICENSE) para mais detalhes.