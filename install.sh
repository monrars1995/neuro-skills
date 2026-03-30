#!/bin/bash

# Neuro Skills - Instalação Rápida
# Uso: curl -fsSL https://goldneuron.io/install.sh | bash

set -e

echo ""
echo "🧠 Neuro Skills - Instalador"
echo ""

PLATFORMS=("claude-code" "opencode" "antigravity" "cursor" "gemini" "codex")
NEURO_DIR="$HOME/.neuro-skills"
SKILLS=("meta-ads-manager" "traffic-strategist" "ad-copywriter" "neuro-ads-manager" "concessionarias" "imobiliarias" "ecommerce" "educacao" "saude")

# Cores
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

check_npm() {
    if ! command -v npm &> /dev/null; then
        echo -e "${RED}❌ npm não encontrado. Instale o Node.js primeiro.${NC}"
        exit 1
    fi
}

install_via_npm() {
    echo -e "${GREEN}📦 Instalando via npm...${NC}"
    npm install -g @goldneuronio/neuro-skills
    echo -e "${GREEN}✅ Instalado em $NEURO_DIR${NC}"
}

get_platform_dir() {
    local platform=$1
    case $platform in
        "claude-code") echo "$HOME/.claude/skills" ;;
        "opencode") echo "$HOME/.opencode/skills" ;;
        "antigravity") echo "$HOME/.antigravity/skills" ;;
        "cursor") echo "$HOME/.cursor/skills" ;;
        "gemini") echo "$HOME/.gemini/skills" ;;
        "codex") echo "$HOME/.codex/skills" ;;
        *) echo "" ;;
    esac
}

install_to_platform() {
    local platform=$1
    local target_dir=$(get_platform_dir "$platform")
    
    if [ -z "$target_dir" ]; then
        echo -e "${RED}❌ Plataforma desconhecida: $platform${NC}"
        return 1
    fi
    
    echo -e "${GREEN}📁 Instalando em $target_dir${NC}"
    mkdir -p "$target_dir"
    
    for skill in "${SKILLS[@]}"; do
        if [ -d "$NEURO_DIR/skills/$skill" ]; then
            ln -sf "$NEURO_DIR/skills/$skill" "$target_dir/$skill" 2>/dev/null || true
            echo -e "  ${GREEN}✓${NC} $skill"
        fi
    done
    
    echo -e "${GREEN}✅ $platform configurado!${NC}"
}

install_all_platforms() {
    echo -e "${GREEN}🚀 Instalando em todas as plataformas...${NC}"
    
    for platform in "${PLATFORMS[@]}"; do
        install_to_platform "$platform"
    done
}

select_platforms() {
    echo -e "${YELLOW}Selecione as plataformas:${NC}"
    echo ""
    
    for i in "${!PLATFORMS[@]}"; do
        echo "  $((i+1))) ${PLATFORMS[$i]}"
    done
    echo "  0) Todas as plataformas"
    echo ""
    
    read -p "Escolha (0-6): " choice
    
    case $choice in
        0) install_all_platforms ;;
        1) install_to_platform "claude-code" ;;
        2) install_to_platform "opencode" ;;
        3) install_to_platform "antigravity" ;;
        4) install_to_platform "cursor" ;;
        5) install_to_platform "gemini" ;;
        6) install_to_platform "codex" ;;
        *) echo -e "${RED}Opção inválida${NC}" ;;
    esac
}

main() {
    check_npm
    install_via_npm
    echo ""
    select_platforms
    
    echo ""
    echo -e "${GREEN}✨ Instalação concluída!${NC}"
    echo ""
    echo "📚 Documentação: https://goldneuron.io/"
    echo "💬 Comunidade: https://goldneuron.io/drops"
    echo ""
    echo "Execute 'neuro-skills --help' para ver os comandos disponíveis."
}

main