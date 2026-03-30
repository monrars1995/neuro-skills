#!/bin/bash

# Instalação para Cursor
# Uso: curl -fsSL https://goldneuron.io/install-cursor.sh | bash

set -e

echo "🖥️ Instalando Neuro Skills para Cursor..."

# Instalar via npm
npm install -g @goldneuronio/neuro-skills

# Criar diretório doCursor
mkdir -p ~/.cursor/skills

# Criar symlinks
ln -sf ~/.neuro-skills/skills/meta-ads-manager ~/.cursor/skills/
ln -sf ~/.neuro-skills/skills/traffic-strategist ~/.cursor/skills/
ln -sf ~/.neuro-skills/skills/ad-copywriter ~/.cursor/skills/
ln -sf ~/.neuro-skills/skills/neuro-ads-manager ~/.cursor/skills/
ln -sf ~/.neuro-skills/skills/concessionarias ~/.cursor/skills/
ln -sf ~/.neuro-skills/skills/imobiliarias ~/.cursor/skills/
ln -sf ~/.neuro-skills/skills/ecommerce ~/.cursor/skills/
ln -sf ~/.neuro-skills/skills/educacao ~/.cursor/skills/
ln -sf ~/.neuro-skills/skills/saude ~/.cursor/skills/

echo ""
echo "✅ Instalação concluída!"
echo ""
echo "Os skills são carregados automaticamente quando estão em ~/.cursor/skills/"
echo ""
echo "📚 Documentação: https://goldneuron.io/"