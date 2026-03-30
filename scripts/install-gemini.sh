#!/bin/bash

# Instalação para Gemini CLI (Google)
# Uso: curl -fsSL https://goldneuron.io/install-gemini.sh | bash

set -e

echo "✨ Instalando Neuro Skills para Gemini CLI..."

# Instalar via npm
npm install -g @goldneuronio/neuro-skills

# Criar diretório doGemini
mkdir -p ~/.gemini/skills

# Criar symlinks
ln -sf ~/.neuro-skills/skills/meta-ads-manager ~/.gemini/skills/
ln -sf ~/.neuro-skills/skills/traffic-strategist ~/.gemini/skills/
ln -sf ~/.neuro-skills/skills/ad-copywriter ~/.gemini/skills/
ln -sf ~/.neuro-skills/skills/neuro-ads-manager ~/.gemini/skills/
ln -sf ~/.neuro-skills/skills/concessionarias ~/.gemini/skills/
ln -sf ~/.neuro-skills/skills/imobiliarias ~/.gemini/skills/
ln -sf ~/.neuro-skills/skills/ecommerce ~/.gemini/skills/
ln -sf ~/.neuro-skills/skills/educacao ~/.gemini/skills/
ln -sf ~/.neuro-skills/skills/saude ~/.gemini/skills/

echo ""
echo "✅ Instalação concluída!"
echo ""
echo "Uso:"
echo "  Load skill: meta-ads-manager"
echo "  /meta-ads setup"
echo ""
echo "📚 Documentação: https://goldneuron.io/"