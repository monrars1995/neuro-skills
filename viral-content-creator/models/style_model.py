"""
Style Modeler - Cria modelos de estilo reutilizáveis baseados em análises.

Author: @monrars
"""

import json
from typing import Dict, List, Optional, Any
from dataclasses import dataclass, field
from datetime import datetime
from pathlib import Path
import os


@dataclass
class VisualIdentity:
    paleta: Dict[str, str] = field(
        default_factory=lambda: {
            "primaria": "#000000",
            "secundaria": "#FFFFFF",
            "destaque": "#D4AF37",
            "fundo": "#0A0A0F",
        }
    )
    tipografia: Dict[str, Dict[str, Any]] = field(
        default_factory=lambda: {
            "headline": {"fonte": "Inter", "peso": 700, "tamanho": 48},
            "body": {"fonte": "Inter", "peso": 400, "tamanho": 24},
            "cta": {"fonte": "Inter", "peso": 600, "tamanho": 20},
        }
    )
    elementos: Dict[str, bool] = field(
        default_factory=lambda: {
            "badges": True,
            "setas": True,
            "icones": True,
            "numeros": True,
        }
    )
    composicao: Dict[str, int] = field(
        default_factory=lambda: {"margem": 40, "padding": 20, "espaco_entre_slides": 10}
    )


@dataclass
class CopyFramework:
    hooks: List[str] = field(default_factory=list)
    estruturas: List[str] = field(default_factory=list)
    ctas: List[str] = field(default_factory=list)


@dataclass
class HashtagsFramework:
    estrategia: str = "fita_infinita"
    quantidade_min: int = 5
    quantidade_max: int = 10
    categorias: List[Dict[str, str]] = field(default_factory=list)


@dataclass
class TimingConfig:
    dias_melhores: List[str] = field(
        default_factory=lambda: ["segunda", "quarta", "sexta"]
    )
    horarios_melhores: List[str] = field(
        default_factory=lambda: ["07:00", "12:00", "18:00", "21:00"]
    )
    duracao_ideal_segundos: Dict[str, Any] = field(
        default_factory=lambda: {"reels": 15, "carrossel": "scroll_natural"}
    )


@dataclass
class ViralityFactors:
    pesos: Dict[str, float] = field(
        default_factory=lambda: {
            "hook_strength": 0.25,
            "visual_appeal": 0.20,
            "value_proposition": 0.20,
            "cta_clarity": 0.15,
            "timing": 0.10,
            "hashtag_strategy": 0.10,
        }
    )
    threshold_viral: float = 7.5
    threshold_muito_viral: float = 9.0


class StyleModeler:
    """
    Cria modelos de estilo reutilizáveis baseados em análises de perfis e posts.

    Funcionalidades:
    - Criar modelos de estilo desde análises
    - Salvar/carregar modelos
    - Atualizar modelos com novas análises
    - Gerar templates baseados em modelos
    """

    VERTICAL_VARIABLES = {
        "concessionarias": {
            "{veiculo}": ["carro", "SUV", "sedan", "hatch", "pickup"],
            "{marca}": ["Toyota", "Honda", "VW", "Chevrolet", "Hyundai"],
            "{valor}": ["R$ 50.000", "R$ 80.000", "R$ 120.000"],
            "{problema}": ["juro alto", "entrada grande", "documentação"],
            "{solucao}": ["financiamento", "consórcio", "usado certificado"],
            "{prazo}": ["48 meses", "60 meses", "72 meses"],
            "{economia}": ["R$ 5.000", "R$ 10.000", "R$ 20.000"],
        },
        "imobiliarias": {
            "{imovel}": ["apartamento", "casa", "terreno", "cobertura"],
            "{bairro}": ["Centro", "Zona Sul", "Zona Norte"],
            "{quartos}": ["1 quarto", "2 quartos", "3 quartos", "4 quartos"],
            "{valor}": ["R$ 300.000", "R$ 500.000", "R$ 800.000"],
            "{vaga}": ["1 vaga", "2 vagas", "sem vaga"],
            "{diferencial}": ["varanda", "área de lazer", "próximo metrô"],
        },
        "ecommerce": {
            "{produto}": ["produto A", "produto B", "produto C"],
            "{categoria}": ["eletrônicos", "moda", "casa", "beleza"],
            "{desconto}": ["30%", "50%", "70%"],
            "{prazo}": ["1 dia", "3 dias", "7 dias"],
            "{beneficio}": ["frete grátis", "cashback", "brinde"],
            "{urgencia}": ["últimas unidades", "últimas horas", "último dia"],
        },
        "educacao": {
            "{curso}": ["curso A", "curso B", "curso C"],
            "{area}": ["tecnologia", "negócios", "saúde", "idiomas"],
            "{duracao}": ["3 meses", "6 meses", "1 ano"],
            "{certificacao}": ["certificado", "diploma", "bacharelado"],
            "{modalidade}": ["online", "presencial", "híbrido"],
        },
        "saude": {
            "{tratamento}": ["tratamento A", "tratamento B", "tratamento C"],
            "{especialidade}": ["dermatologia", "odontologia", "estética"],
            "{duracao}": ["1 sessão", "3 sessões", "pacote completo"],
            "{resultado}": ["imediato", "1 semana", "1 mês"],
            "{beneficio}": ["natural", "duradouro", "sem dor"],
        },
    }

    DEFAULT_HOOKS = [
        "Você sabia que {insight_surpreendente}?",
        "A maioria das {audiencia} não sabe que {problema}.",
        "{numero}% das pessoas erram ao {acao}.",
        "Por que {objeto} custa tão caro? A resposta vai te surpreender.",
        "O que ninguém te conta sobre {topico}.",
        "3 coisas que você PRECISA saber sobre {topico}.",
        "Esse {objeto} mudou minha vida. Explico por que.",
        "Pare de fazer isso com {objeto}. Sério.",
    ]

    DEFAULT_CTAS = [
        "Salva para ver depois 💾",
        "Comenta SIM se você faz isso ✅",
        "Envia para quem precisa saber 📤",
        "Segue para mais dicas assim 👆",
        "Comenta sua dúvida aqui 👇",
        "Compartilha com um amigo 🤝",
    ]

    def __init__(self, config: Optional[Dict] = None):
        self.config = config or {}
        self.models_dir = (
            Path.home() / ".neuro-skills" / "viral-content-creator" / "models"
        )
        self.models_dir.mkdir(parents=True, exist_ok=True)
        self.cache = {}

    def create_model(
        self,
        nome: str,
        descricao: str,
        analises_referencia: List[str],
        configuracoes: Optional[Dict] = None,
    ) -> Dict[str, Any]:
        """
        Cria um modelo de estilo a partir de análises.

        Args:
            nome: Nome do modelo (ex: "concessionaria_viral")
            descricao: Descrição do modelo
            analises_referencia: IDs das análises de referência
            configuracoes: Configurações customizadas

        Returns:
            Dict com modelo criado
        """
        configuracoes = configuracoes or {}

        model = {
            "modelo": {
                "id": f"model_{nome}_{datetime.now().strftime('%Y%m%d%H%M%S')}",
                "nome": nome,
                "versao": "1.0",
                "descricao": descricao,
                "criado_em": datetime.now().isoformat(),
                "estatisticas": {
                    "perfis_analisados": len(
                        [a for a in analises_referencia if "profile" in a]
                    ),
                    "posts_analisados": len(
                        [a for a in analises_referencia if "post" in a]
                    ),
                    "tempo_analise": "pendente",
                },
                "identidade_visual": self._build_visual_identity(configuracoes),
                "copy_framework": self._build_copy_framework(configuracoes),
                "hashtags_framework": self._build_hashtags_framework(configuracoes),
                "timing": self._build_timing_config(configuracoes),
                "viralidade_factors": self._build_virality_factors(configuracoes),
                "variaveis_dynamic": self._get_vertical_variables(nome),
                "templates": self._build_templates(configuracoes),
            }
        }

        self._save_model(model)
        self.cache[nome] = model

        return model

    def _build_visual_identity(self, config: Dict) -> Dict[str, Any]:
        """Constrói identidade visual do modelo."""
        paleta = config.get("paleta", {})

        return {
            "paleta": {
                "primaria": paleta.get("primaria", "#000000"),
                "secundaria": paleta.get("secundaria", "#FFFFFF"),
                "destaque": paleta.get("destaque", "#D4AF37"),
                "fundo": paleta.get("fundo", "#0A0A0F"),
            },
            "tipografia": config.get(
                "tipografia",
                {
                    "headline": {"fonte": "Inter", "peso": 700, "tamanho": 48},
                    "body": {"fonte": "Inter", "peso": 400, "tamanho": 24},
                    "cta": {"fonte": "Inter", "peso": 600, "tamanho": 20},
                },
            ),
            "elementos": config.get(
                "elementos",
                {"badges": True, "setas": True, "icones": True, "numeros": True},
            ),
            "composicao": config.get(
                "composicao", {"margem": 40, "padding": 20, "espaco_entre_slides": 10}
            ),
        }

    def _build_copy_framework(self, config: Dict) -> Dict[str, Any]:
        """Constrói framework de copy."""
        return {
            "hooks": config.get("hooks", self.DEFAULT_HOOKS),
            "estruturas": config.get(
                "estruturas",
                [
                    "HOOK → PROBLEMA → SOLUÇÃO → CTA",
                    "CONTRASTE → INFORMAÇÃO → BENEFÍCIO → CTA",
                    "DADO → CONTEXTO → APLICAÇÃO → CTA",
                ],
            ),
            "ctas": config.get("ctas", self.DEFAULT_CTAS),
        }

    def _build_hashtags_framework(self, config: Dict) -> Dict[str, Any]:
        """Constrói framework de hashtags."""
        return {
            "estrategia": config.get("estrategia", "fita_infinita"),
            "quantidade_min": config.get("quantidade_min", 5),
            "quantidade_max": config.get("quantidade_max", 10),
            "categorias": config.get(
                "categorias",
                [
                    {"branded": "#marca"},
                    {"行业标准": "#industria"},
                    {"nichada": "#niche"},
                    {"tendencia": "#trending"},
                ],
            ),
        }

    def _build_timing_config(self, config: Dict) -> Dict[str, Any]:
        """Constrói configuração de timing."""
        return {
            "dias_melhores": config.get(
                "dias_melhores", ["segunda", "quarta", "sexta"]
            ),
            "horarios_melhores": config.get(
                "horarios_melhores", ["07:00", "12:00", "18:00", "21:00"]
            ),
            "duracao_ideal_segundos": config.get(
                "duracao_ideal", {"reels": 15, "carrossel": "scroll_natural"}
            ),
        }

    def _build_virality_factors(self, config: Dict) -> Dict[str, Any]:
        """Constrói fatores de viralização."""
        return {
            "pesos": config.get(
                "pesos",
                {
                    "hook_strength": 0.25,
                    "visual_appeal": 0.20,
                    "value_proposition": 0.20,
                    "cta_clarity": 0.15,
                    "timing": 0.10,
                    "hashtag_strategy": 0.10,
                },
            ),
            "threshold_viral": config.get("threshold_viral", 7.5),
            "threshold_muito_viral": config.get("threshold_muito_viral", 9.0),
        }

    def _get_vertical_variables(self, nome: str) -> Dict[str, List[str]]:
        """Obtém variáveis dinâmicas por vertical."""
        for vertical, variaveis in self.VERTICAL_VARIABLES.items():
            if vertical in nome.lower():
                return variaveis
        return {}

    def _build_templates(self, config: Dict) -> Dict[str, Any]:
        """Constrói templates padrão."""
        return {
            "carousel_educativo": {
                "slides_padrao": 7,
                "estrutura": [
                    {"slide": 1, "tipo": "capa", "elementos": ["hook", "badge"]},
                    {"slide": 2, "tipo": "problema", "elementos": ["texto", "icone"]},
                    {
                        "slide": 3,
                        "tipo": "dado",
                        "elementos": ["numero_grande", "subtitulo"],
                    },
                    {
                        "slide": 4,
                        "tipo": "solucao",
                        "elementos": ["lista", "checkmarks"],
                    },
                    {
                        "slide": 5,
                        "tipo": "exemplo",
                        "elementos": ["caso_real", "resultado"],
                    },
                    {
                        "slide": 6,
                        "tipo": "value",
                        "elementos": ["conclusao", "beneficio"],
                    },
                    {"slide": 7, "tipo": "cta", "elementos": ["acao", "icones"]},
                ],
            },
            "reels_viral": {
                "duracao_segundos": [7, 15, 30],
                "estrutura": {
                    "0-3s": "Hook visual + textual",
                    "3-10s": "Desenvolvimento rápido",
                    "10-15s": "Climax / revelação",
                    "15-30s": "CTA + repete loop",
                },
            },
            "post_estatico": {
                "formato": ["1:1", "4:5"],
                "estrutura_visual": {
                    "zona_atencao": "33% superior",
                    "texto_principal": "centro",
                    "cta": "20% inferior",
                },
            },
        }

    def _save_model(self, model: Dict) -> None:
        """Salva modelo em arquivo."""
        nome = model["modelo"]["nome"]
        filepath = self.models_dir / f"{nome}.json"

        with open(filepath, "w", encoding="utf-8") as f:
            json.dump(model, f, ensure_ascii=False, indent=2)

    def load_model(self, nome: str) -> Optional[Dict[str, Any]]:
        """Carrega modelo salvo."""
        if nome in self.cache:
            return self.cache[nome]

        filepath = self.models_dir / f"{nome}.json"

        if filepath.exists():
            with open(filepath, "r", encoding="utf-8") as f:
                model = json.load(f)
                self.cache[nome] = model
                return model

        return None

    def list_models(self, filtro: Optional[Dict] = None) -> Dict[str, Any]:
        """Lista todos os modelos disponíveis."""
        models = []

        for filepath in self.models_dir.glob("*.json"):
            try:
                with open(filepath, "r", encoding="utf-8") as f:
                    model = json.load(f)
                    models.append(
                        {
                            "nome": model["modelo"]["nome"],
                            "versao": model["modelo"]["versao"],
                            "criado_em": model["modelo"]["criado_em"],
                            "estatisticas": model["modelo"]["estatisticas"],
                        }
                    )
            except Exception:
                continue

        # Apply filters
        if filtro:
            if filtro.get("vertical"):
                models = [m for m in models if filtro["vertical"] in m["nome"].lower()]

            if filtro.get("ordenar_por") == "data":
                models.sort(key=lambda x: x["criado_em"], reverse=True)
            elif filtro.get("ordenar_por") == "nome":
                models.sort(key=lambda x: x["nome"])

        return {"modelos": models, "total": len(models)}

    def update_model(
        self, model_id: str, novas_analises: List[str], recalcular: bool = True
    ) -> Dict[str, Any]:
        """Atualiza modelo existente com novas análises."""
        model = self.load_model(model_id)

        if not model:
            return {"error": f"Modelo {model_id} não encontrado"}

        # Add new analyses
        model["modelo"]["estatisticas"]["perfis_analisados"] += len(
            [a for a in novas_analises if "profile" in a]
        )
        model["modelo"]["estatisticas"]["posts_analisados"] += len(
            [a for a in novas_analises if "post" in a]
        )
        model["modelo"]["versao"] = self._increment_version(model["modelo"]["versao"])

        if recalcular:
            # Recalculate factors based on new data
            model["modelo"] = self._recalculate_factors(model["modelo"])

        self._save_model(model)
        return model

    def _increment_version(self, version: str) -> str:
        """Incrementa versão do modelo."""
        parts = version.split(".")
        if len(parts) == 2:
            return f"{parts[0]}.{int(parts[1]) + 1}"
        return "1.1"

    def _recalculate_factors(self, model: Dict) -> Dict:
        """Recalcula fatores de viralização."""
        # Placeholder - em produção, recorreria às análises
        return model

    def delete_model(self, model_id: str) -> Dict[str, Any]:
        """Remove modelo."""
        filepath = self.models_dir / f"{model_id}.json"

        if filepath.exists():
            filepath.unlink()
            if model_id in self.cache:
                del self.cache[model_id]
            return {"success": True, "message": f"Modelo {model_id} removido"}

        return {"success": False, "message": f"Modelo {model_id} não encontrado"}

    def get_default_models(self) -> Dict[str, Any]:
        """Retorna modelos padrão por vertical."""
        defaults = {}

        for vertical in [
            "concessionarias",
            "imobiliarias",
            "ecommerce",
            "educacao",
            "saude",
        ]:
            defaults[vertical] = {
                "nome": f"{vertical}_viral",
                "variaveis": self.VERTICAL_VARIABLES.get(vertical, {}),
                "hooks": self.DEFAULT_HOOKS,
                "ctas": self.DEFAULT_CTAS,
            }

        return defaults
