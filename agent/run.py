#!/usr/bin/env python3
"""
Neuro Skills Agent - Entry Point
Autor: Monrars (@monrars)
"""

import sys
from pathlib import Path


def check_dependencies():
    """Verifica se todas as dependências estão instaladas"""
    missing = []

    try:
        import streamlit
    except ImportError:
        missing.append("streamlit")

    try:
        import requests
    except ImportError:
        missing.append("requests")

    try:
        from PIL import Image
    except ImportError:
        missing.append("Pillow")

    if missing:
        print("❌ Dependências faltando:")
        for dep in missing:
            print(f"   - {dep}")
        print("\nInstale com:")
        print(f"   pip install {' '.join(missing)}")
        return False

    return True


def main():
    """Ponto de entrada principal"""
    print("🧠 Neuro Skills Agent v2.0.0-beta")
    print("=" * 40)

    if not check_dependencies():
        sys.exit(1)

    print("\n✅ Todas as dependências instaladas")
    print("\n🚀 Iniciando interface...")
    print("\n📱 Siga @monrars no Instagram")
    print("🔗 github.com/monrars1995/neuro-skills")
    print("\n" + "=" * 40)

    # Inicializar memória
    from core.memory import MemoryManager
    from core.config import NEURO_DIR

    memory = MemoryManager(NEURO_DIR)

    print(f"📁 Memória: {NEURO_DIR}")

    # Executar Streamlit
    import os
    import streamlit.web.cli as stcli

    # Caminho para o app
    app_path = Path(__file__).parent / "ui" / "app.py"

    # Argumentos do Streamlit
    sys.argv = [
        "streamlit",
        "run",
        str(app_path),
        "--server.headless=true",
        "--server.port=8501",
        "--browser.gatherUsageStats=false",
    ]

    sys.exit(stcli.main())


if __name__ == "__main__":
    main()
