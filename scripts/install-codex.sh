#!/bin/bash

# Instalação para OpenAI Codex
# Uso: curl -fsSL https://goldneuron.io/install-codex.sh | bash

set -e

echo "🤖 Instalando Neuro Skills para OpenAI Codex..."

# Instalar via npm
npm install -g @goldneuronio/neuro-skills

# Criar diretório doCodex
mkdir -p ~/.codex/skills

# Criar symlinks
ln -sf ~/.neuro-skills/skills/meta-ads-manager ~/.codex/skills/
ln -sf ~/.neuro-skills/skills/traffic-strategist ~/.codex/skills/
ln -sf ~/.neuro-skills/skills/ad-copywriter ~/.codex/skills/
ln -sf ~/.neuro-skills/skills/neuro-ads-manager ~/.codex/skills/
ln -sf ~/.neuro-skills/skills/concessionarias ~/.codex/skills/
ln -sf ~/.neuro-skills/skills/imobiliarias ~/.codex/skills/
ln -sf ~/.neuro-skills/skills/ecommerce ~/.codex/skills/
ln -sf ~/.neuro-skills/skills/educacao ~/.codex/skills/
ln -sf ~/.neuro-skills/skills/saude ~/.codex/skills/

echo ""
echo "✅ Instalação concluída!"
echo ""
echo "Uso:"
echo "  Load skill: meta-ads-manager"
echo "  /meta-ads setup"
echo ""
echo "📚 Documentação: https://goldneuron.io/"