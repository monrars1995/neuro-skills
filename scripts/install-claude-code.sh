#!/bin/bash

# Instalação para Claude Code (Anthropic)
# Uso: curl -fsSL https://goldneuron.io/install-claude-code.sh | bash

set -e

echo "🤖 Instalando Neuro Skills para Claude Code..."

# Instalar via npm
npm install -g @goldneuronio/neuro-skills

# Criar diretório doClaude Code
mkdir -p ~/.claude/skills

# Criar symlinks
ln -sf ~/.neuro-skills/skills/meta-ads-manager ~/.claude/skills/
ln -sf ~/.neuro-skills/skills/traffic-strategist ~/.claude/skills/
ln -sf ~/.neuro-skills/skills/ad-copywriter ~/.claude/skills/
ln -sf ~/.neuro-skills/skills/neuro-ads-manager ~/.claude/skills/
ln -sf ~/.neuro-skills/skills/concessionarias ~/.claude/skills/
ln -sf ~/.neuro-skills/skills/imobiliarias ~/.claude/skills/
ln -sf ~/.neuro-skills/skills/ecommerce ~/.claude/skills/
ln -sf ~/.neuro-skills/skills/educacao ~/.claude/skills/
ln -sf ~/.neuro-skills/skills/saude ~/.claude/skills/

echo ""
echo "✅ Instalação concluída!"
echo ""
echo "Uso:"
echo "  Load skill: meta-ads-manager"
echo "  /meta-ads setup"
echo ""
echo "📚 Documentação: https://goldneuron.io/"