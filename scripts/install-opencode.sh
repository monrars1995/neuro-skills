#!/bin/bash

# Instalação para OpenCode
# Uso: curl -fsSL https://goldneuron.io/install-opencode.sh | bash

set -e

echo "🤖 Instalando Neuro Skills para OpenCode..."

# Instalar via npm
npm install -g @goldneuronio/neuro-skills

# Criar diretório doOpenCode
mkdir -p ~/.opencode/skills

# Criar symlinks
ln -sf ~/.neuro-skills/skills/meta-ads-manager ~/.opencode/skills/
ln -sf ~/.neuro-skills/skills/traffic-strategist ~/.opencode/skills/
ln -sf ~/.neuro-skills/skills/ad-copywriter ~/.opencode/skills/
ln -sf ~/.neuro-skills/skills/neuro-ads-manager ~/.opencode/skills/
ln -sf ~/.neuro-skills/skills/concessionarias ~/.opencode/skills/
ln -sf ~/.neuro-skills/skills/imobiliarias ~/.opencode/skills/
ln -sf ~/.neuro-skills/skills/ecommerce ~/.opencode/skills/
ln -sf ~/.neuro-skills/skills/educacao ~/.opencode/skills/
ln -sf ~/.neuro-skills/skills/saude ~/.opencode/skills/

echo ""
echo "✅ Instalação concluída!"
echo ""
echo "Uso:"
echo "  Load skill: meta-ads-manager"
echo "  /meta-ads setup"
echo ""
echo "📚 Documentação: https://goldneuron.io/"