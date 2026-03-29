#!/bin/bash

# setup-memory.sh - Inicializa o sistema de memória do Neuro Skills
# Versão: v2.0.0-beta
# Autor: Monrars (@monrars)

NEURO_DIR="$HOME/.neuro-skills"
VERSION="2.0.0-beta"

echo ""
echo "🧠 Neuro Skills - Sistema de Memória"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "Versão: $VERSION"
echo ""

# Verificar se já existe
if [ -d "$NEURO_DIR" ]; then
    echo "⚠️  Diretório já existe: $NEURO_DIR"
    echo ""
    read -p "Deseja sobrescrever? (s/N): " -n 1 -r
    echo ""
    if [[ ! $REPLY =~ ^[Ss]$ ]]; then
        echo "❌ Operação cancelada."
        exit 1
    fi
    echo ""
    echo "📦 Fazendo backup do diretório existente..."
    mv "$NEURO_DIR" "$NEURO_DIR.backup.$(date +%Y%m%d%H%M%S)"
fi

echo "📁 Criando estrutura de diretórios..."
echo ""

# Criar estrutura de diretórios
mkdir -p "$NEURO_DIR/clients"
mkdir -p "$NEURO_DIR/campaigns"
mkdir -p "$NEURO_DIR/sessions/meta-ads-manager/cache/insights"
mkdir -p "$NEURO_DIR/sessions/meta-ads-manager/cache/campaigns"
mkdir -p "$NEURO_DIR/sessions/meta-ads-manager/logs"
mkdir -p "$NEURO_DIR/sessions/traffic-strategist/cache/analyses"
mkdir -p "$NEURO_DIR/sessions/ad-copywriter/cache/copies"
mkdir -p "$NEURO_DIR/shared/templates"

echo "✅ Diretórios criados"
echo ""

# Criar arquivos iniciais
echo "📄 Criando arquivos de configuração..."
echo ""

# Índice de clientes
cat > "$NEURO_DIR/clients/index.json" << 'EOF'
{
  "version": "2.0",
  "updated_at": null,
  "clients": {},
  "active_client": null,
  "recent_clients": []
}
EOF

# Contas Meta
cat > "$NEURO_DIR/shared/accounts.json" << 'EOF'
{
  "version": "2.0",
  "accounts": {},
  "active_account": null
}
EOF

# Aprendizados globais
cat > "$NEURO_DIR/shared/learnings.json" << 'EOF'
{
  "version": "1.0",
  "updated_at": null,
  "industry_benchmarks": {},
  "platform_insights": {},
  "audience_patterns": {},
  "copy_patterns": {}
}
EOF

# Benchmarks do mercado
cat > "$NEURO_DIR/shared/benchmarks.json" << 'EOF'
{
  "version": "1.0",
  "updated_at": null,
  "industries": {}
}
EOF

echo "✅ Arquivos de configuração criados"
echo ""

# Criar templates
echo "📝 Criando templates..."
echo ""

# Template de briefing
cat > "$NEURO_DIR/shared/templates/briefing_template.md" << 'EOF'
# Briefing: {nome_da_campanha}

## Informações do Cliente
- **Cliente:** {nome}
- **Produto/Serviço:** {produto}
- **Indústria:** {industria}
- **Voz da Marca:** {tom}

## Objetivos da Campanha
- **Objetivo Principal:** [Vendas/Leads/Tráfego/Awareness]
- **Objetivos Secundários:** [Brand reach, Email capture]
- **CPA Alvo:** R$ XX,XX
- **ROAS Alvo:** X.Xx
- **Orçamento:** R$ X.XXX/mês

## Público-Alvo
- **Idade:** XX a XX anos
- **Gênero:** [Todos/Masculino/Feminino]
- **Localização:** [Países, Cidades]
- **Interesses:** [Lista de interesses]
- **Comportamentos:** [Comportamentos de compra]
- **Dores:** [Problemas que o produto resolve]
- **Desejos:** [O que o público quer]

## Proposta de Valor (USPs)
1. {USP 1}
2. {USP 2}
3. {USP 3}

## Criativos
- **Formatos:** [Imagem, Vídeo, Carrossel]
- **Posicionamentos:** [Feed, Stories, Reels]
- **CTA Principal:** [Shop Now, Learn More]

## Landing Page
- **URL:** {url}
- **Tipo:** [Product page, Landing page]

## Período da Campanha
- **Início:** {data_inicio}
- **Fim:** {data_fim}

## Observações
{observações_adicionais}
EOF

# Template de checklist
cat > "$NEURO_DIR/shared/templates/checklist_template.md" << 'EOF'
# Checklist: {nome_da_campanha}

## Briefing
- [ ] Objetivo definido
- [ ] Público-alvo definido
- [ ] Orçamento definido
- [ ] Período definido

## Criativos
- [ ] Criativos criados
- [ ] Criativos validados
- [ ] Nomenclatura correta
- [ ] Formatos adequados

## Copy
- [ ] Copy para Feed
- [ ] Copy para Stories
- [ ] Copy para Reels
- [ ] Variações A/B

## Targeting
- [ ] Interesses definidos
- [ ] Localização definida
- [ ] Idade definida
- [ ] Gênero definido

## Técnico
- [ ] Pixel configurado
- [ ] Página conectada
- [ ] Conversions API (opcional)
- [ ] UTM configurado
EOF

echo "✅ Templates criados"
echo ""

# Criar script de gerenciamento
echo "🔧 Criando script de gerenciamento..."
echo ""

cat > "$NEURO_DIR/neuro-memory.sh" << 'SCRIPT'
#!/bin/bash

NEURO_DIR="$HOME/.neuro-skills"

show_help() {
    echo ""
    echo "🧠 Neuro Skills - Gerenciador de Memória"
    echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
    echo ""
    echo "Uso: neuro-memory <comando> [opções]"
    echo ""
    echo "Comandos:"
    echo "  status              Mostrar status do sistema"
    echo "  clients list        Listar clientes"
    echo "  client active       Mostrar cliente ativo"
    echo "  client use <id>     Definir cliente ativo"
    echo "  cache clear         Limpar cache"
    echo "  backup              Criar backup"
    echo "  help                Mostrar esta ajuda"
    echo ""
}

show_status() {
    echo ""
    echo "📊 Status do Sistema"
    echo "━━━━━━━━━━━━━━━━━━━"
    echo ""
    
    if [ -f "$NEURO_DIR/clients/index.json" ]; then
        clients=$(cat "$NEURO_DIR/clients/index.json")
        echo "📁 Diretório: $NEURO_DIR"
        echo ""
        echo "Clientes:"
        echo "$clients" | grep -o '"[^"]*":' | head -20
    else
        echo "❌ Sistema não inicializado. Execute: ./setup-memory.sh"
    fi
    echo ""
}

list_clients() {
    echo ""
    echo "👥 Clientes"
    echo "━━━━━━━━━━━━━━"
    echo ""
    
    if [ -f "$NEURO_DIR/clients/index.json" ]; then
        cat "$NEURO_DIR/clients/index.json" | python3 -c "import sys, json; data=json.load(sys.stdin); [print(f'  {k}: {v.get(\"name\", \"N/A\")}') for k,v in data.get('clients',{}).items()]"2>/dev/null || cat "$NEURO_DIR/clients/index.json"
    else
        echo "❌ Nenhum cliente cadastrado"
    fi
    echo ""
}

clear_cache() {
    echo ""
    echo "🗑️ Limpando cache..."
    rm -rf "$NEURO_DIR/sessions/*/cache/*" 2>/dev/null
    echo "✅ Cache limpo"
    echo ""
}

create_backup() {
    backup_file="$HOME/neuro-skills_backup_$(date +%Y%m%d_%H%M%S).tar.gz"
    tar -czvf "$backup_file" -C "$NEURO_DIR" . 2>/dev/null
    echo ""
    echo "✅ Backup criado: $backup_file"
    echo ""
}

case "$1" in
    "status") show_status ;;
    "clients"|"clients list") list_clients ;;
    "client active") echo "Cliente ativo: $(grep -o '"active_client":"[^"]*"' "$NEURO_DIR/clients/index.json" 2>/dev/null | cut -d'"' -f4)" ;;
    "client use") echo "Funcionalidade em desenvolvimento" ;;
    "cache clear") clear_cache ;;
    "backup") create_backup ;;
    "help"|"-h"|"--help") show_help ;;
    *) show_help ;;
esac
SCRIPT

chmod +x "$NEURO_DIR/neuro-memory.sh"

echo "✅ Script de gerenciamento criado"
echo ""

# Resumo final
echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "✅ Sistema de memória inicializado!"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""
echo "📁 Estrutura criada em: $NEURO_DIR"
echo ""
echo "📂 Diretórios:"
echo "   ├── clients/         (dados de clientes)"
echo "   ├── campaigns/       (campanhas ativas)"
echo "   ├── sessions/        (sessões por skill)"
echo "   └── shared/          (memória compartilhada)"
echo ""
echo "📝 Arquivos criados:"
echo "   ├── clients/index.json"
echo "   ├── shared/accounts.json"
echo "   ├── shared/learnings.json"
echo "   ├── shared/benchmarks.json"
echo "   └── shared/templates/"
echo ""
echo "🔧 Comando de gerenciamento:"
echo "   $NEURO_DIR/neuro-memory.sh help"
echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "🚀 Próximos passos:"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""
echo "1. Configure suas contas Meta Ads:"
echo "   /meta-ads setup"
echo ""
echo "2. Adicione clientes:"
echo "   mkdir -p ~/.neuro-skills/clients/{client_id}"
echo ""
echo "3. Use os skills normalmente"
echo ""
echo "📱 Siga @monrars no Instagram"
echo "🔗 github.com/monrars1995/neuro-skills"
echo ""