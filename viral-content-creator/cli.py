#!/usr/bin/env python3
"""
Viral Content Creator CLI

Usage:
    python -m viral_content_creator analyze-profile @username instagram
    python -m viral_content_creator analyze-post https://instagram.com/p/abc123
    python -m viral_content_creator create-model concessionaria_viral
    python -m viral_content_creator generate concessionaria_viral "financiamento"
    python -m viral_content_creator dashboard

Author: @monrars
Site: https://goldneuron.io/
"""

import argparse
import json
import sys
from datetime import datetime
from pathlib import Path


ROOT = Path(__file__).resolve().parent
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))


def main():
    parser = argparse.ArgumentParser(
        description="Viral Content Creator - Crie conteúdo viral baseado em análise de perfis",
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )

    subparsers = parser.add_subparsers(dest="command", help="Comandos disponíveis")

    # Analyze Profile
    profile_parser = subparsers.add_parser(
        "analyze-profile",
        aliases=["cv-analyze"],
        help="Analisa um perfil de rede social",
    )
    profile_parser.add_argument("username", help="@username ou URL do perfil")
    profile_parser.add_argument(
        "plataforma",
        choices=["instagram", "tiktok", "twitter", "linkedin", "youtube"],
        help="Plataforma do perfil",
    )
    profile_parser.add_argument(
        "--posts-limit", type=int, default=50, help="Número de posts para analisar"
    )
    profile_parser.add_argument("--output", "-o", help="Arquivo de saída (JSON)")

    # Analyze Post
    post_parser = subparsers.add_parser(
        "analyze-post", aliases=["cv-post"], help="Analisa um post específico"
    )
    post_parser.add_argument("url", help="URL do post")
    post_parser.add_argument(
        "--analyze-visual", action="store_true", help="Incluir análise visual"
    )
    post_parser.add_argument("--output", "-o", help="Arquivo de saída (JSON)")

    # Analyze Image
    image_parser = subparsers.add_parser(
        "analyze-image", aliases=["cv-image"], help="Analisa uma imagem"
    )
    image_parser.add_argument("source", help="URL ou arquivo da imagem")
    image_parser.add_argument("--output", "-o", help="Arquivo de saída (JSON)")

    # Create Model
    model_parser = subparsers.add_parser(
        "create-model", aliases=["cv-model"], help="Cria um modelo de estilo"
    )
    model_parser.add_argument("nome", help="Nome do modelo (ex: concessionaria_viral)")
    model_parser.add_argument("--descricao", "-d", help="Descrição do modelo")
    model_parser.add_argument(
        "--analises", nargs="+", help="IDs de análises de referência"
    )
    model_parser.add_argument("--output", "-o", help="Arquivo de saída (JSON)")

    # List Models
    list_parser = subparsers.add_parser(
        "list-models", aliases=["cv-list"], help="Lista modelos disponíveis"
    )
    list_parser.add_argument("--vertical", help="Filtrar por vertical")
    list_parser.add_argument(
        "--ordenar", choices=["data", "nome", "score"], default="data"
    )

    # Generate Content
    gen_parser = subparsers.add_parser(
        "generate", aliases=["cv-generate"], help="Gera conteúdo baseado em modelo"
    )
    gen_parser.add_argument("modelo", help="Nome do modelo")
    gen_parser.add_argument("tema", help="Tema do conteúdo")
    gen_parser.add_argument(
        "--formato", choices=["carousel", "reels", "static"], default="carousel"
    )
    gen_parser.add_argument(
        "--slides", type=int, default=7, help="Número de slides (para carousel)"
    )
    gen_parser.add_argument(
        "--ab-test", action="store_true", help="Gerar variações A/B"
    )
    gen_parser.add_argument("--output", "-o", help="Arquivo de saída (JSON)")

    # Dashboard
    dash_parser = subparsers.add_parser(
        "dashboard", aliases=["cv-dashboard"], help="Mostra dashboard de estatísticas"
    )
    dash_parser.add_argument("--periodo", default="30d", help="Período de análise")
    dash_parser.add_argument("--formato", choices=["json", "markdown"], default="json")

    # Setup
    setup_parser = subparsers.add_parser("setup", help="Configura o sistema")
    setup_parser.add_argument("--vertical", help="Vertical padrão")

    args = parser.parse_args()

    if args.command is None:
        parser.print_help()
        sys.exit(0)

    # Run command
    result = run_command(args)

    # Output result
    if args.output:
        with open(args.output, "w", encoding="utf-8") as f:
            json.dump(result, f, ensure_ascii=False, indent=2)
        print(f"✓ Resultado salvo em {args.output}")
    else:
        print(json.dumps(result, ensure_ascii=False, indent=2))


def run_command(args):
    """Executa o comando solicitado."""

    if args.command in ["analyze-profile", "cv-analyze"]:
        from analyzer.profile_analyzer import ProfileAnalyzer

        analyzer = ProfileAnalyzer()
        return analyzer.analyze(
            args.username, args.plataforma, {"posts_limit": args.posts_limit}
        )

    elif args.command in ["analyze-post", "cv-post"]:
        from analyzer.post_analyzer import PostAnalyzer

        analyzer = PostAnalyzer()
        return analyzer.analyze(args.url, {"analyze_visual": args.analyze_visual})

    elif args.command in ["analyze-image", "cv-image"]:
        from analyzer.image_analyzer import ImageAnalyzer

        analyzer = ImageAnalyzer()
        return analyzer.analyze(args.source)

    elif args.command in ["create-model", "cv-model"]:
        from models.style_model import StyleModeler

        modeler = StyleModeler()
        return modeler.create_model(
            args.nome, args.descricao or f"Modelo {args.nome}", args.analises or []
        )

    elif args.command in ["list-models", "cv-list"]:
        from models.style_model import StyleModeler

        modeler = StyleModeler()
        return modeler.list_models(
            {"vertical": args.vertical, "ordenar_por": args.ordenar}
        )

    elif args.command in ["generate", "cv-generate"]:
        from generator.content_generator import ContentGenerator

        generator = ContentGenerator()
        return generator.generate(
            args.modelo,
            args.tema,
            {"formato": args.formato, "slides": args.slides, "ab_test": args.ab_test},
        )

    elif args.command in ["dashboard", "cv-dashboard"]:
        from utils.dashboard import Dashboard

        dashboard = Dashboard()
        if args.formato == "markdown":
            return {"markdown": dashboard.export_stats("markdown")}
        return dashboard.get_full_dashboard(args.periodo)

    elif args.command == "setup":
        return setup_system(args.vertical)

    else:
        return {"error": f"Comando desconhecido: {args.command}"}


def setup_system(vertical: str = None):
    """Configura o sistema inicial."""
    from pathlib import Path
    import os

    # Criar diretórios
    base_dir = Path.home() / ".neuro-skills" / "viral-content-creator"
    dirs = ["cache", "models", "generated"]

    for d in dirs:
        (base_dir / d).mkdir(parents=True, exist_ok=True)

    # Criar config
    config = {
        "default_vertical": vertical or "concessionarias",
        "analytics_enabled": True,
        "cache_duration_days": 30,
        "created_at": datetime.now().isoformat(),
    }

    config_path = base_dir / "config.json"
    with open(config_path, "w", encoding="utf-8") as f:
        json.dump(config, f, ensure_ascii=False, indent=2)

    return {
        "status": "success",
        "message": "Sistema configurado com sucesso",
        "config_path": str(config_path),
        "config": config,
    }


if __name__ == "__main__":
    main()
