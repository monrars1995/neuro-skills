#!/bin/bash

# Instalação para Antigravity
# Uso: curl -fsSL https://goldneuron.io/install-antigravity.sh | bash

set -e

echo "🚀 Instalando Neuro Skills para Antigravity..."

# Instalar via npm
npm install -g @goldneuronio/neuro-skills

# Criar diretório doAntigravity
mkdir -p ~/.antigravity/skills

# Criar symlinks
ln -sf ~/.neuro-skills/skills/meta-ads-manager ~/.antigravity/skills/
ln -sf ~/.neuro-skills/skills/traffic-strategist ~/.antigravity/skills/
ln -sf ~/.neuro-skills/skills/ad-copywriter ~/.antigravity/skills/
ln -sf ~/.neuro-skills/skills/neuro-ads-manager ~/.antigravity/skills/
ln -sf ~/.neuro-skills/skills/concessionarias ~/.antigravity/skills/
ln -sf ~/.neuro-skills/skills/imobiliarias ~/.antigravity/skills/
ln -sf ~/.neuro-skills/skills/ecommerce ~/.antigravity/skills/
ln -sf ~/.neuro-skills/skills/educacao ~/.antigravity/skills/
ln -sf ~/.neuro-skills/skills/saude ~/.antigravity/skills/

echo ""
echo "✅ Instalação concluída!"
echo ""
echo "Uso:"
echo "  Load skill: meta-ads-manager"
echo "  /meta-ads setup"
echo ""
echo "📚 Documentação: https://goldneuron.io/"