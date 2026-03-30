"""
Content Generator - Gera conteúdo viral baseado em modelos de estilo.

Author: @monrars
"""

import json
import random
from typing import Dict, List, Optional, Any
from dataclasses import dataclass, field
from datetime import datetime
from pathlib import Path
import re


class ContentGenerator:
    """
    Gera conteúdo viral baseado em modelos de estilo.

    Funcionalidades:
    - Gerar carrosséis educativos
    - Gerar reels virais
    - Gerar posts estáticos
    - Gerar variações A/B
    - Gerar conteúdo em lote
    """

    CONTENT_TYPES = ["carousel", "reels", "static", "story"]

    SLIDE_TYPES = {
        "capa": {"elementos": ["hook", "badge", "seta"], "score_weight": 0.25},
        "problema": {"elementos": ["texto", "icone", "numero"], "score_weight": 0.15},
        "dado": {
            "elementos": ["numero_grande", "subtitulo", "icone"],
            "score_weight": 0.20,
        },
        "solucao": {
            "elementos": ["lista", "checkmarks", "numero"],
            "score_weight": 0.15,
        },
        "exemplo": {
            "elementos": ["caso_real", "resultado", "antes_depois"],
            "score_weight": 0.10,
        },
        "value": {
            "elementos": ["conclusao", "beneficio", "destaque"],
            "score_weight": 0.10,
        },
        "cta": {"elementos": ["acao", "icones", "setas"], "score_weight": 0.05},
    }

    def __init__(self, config: Optional[Dict] = None):
        self.config = config or {}
        self.generated_dir = (
            Path.home() / ".neuro-skills" / "viral-content-creator" / "generated"
        )
        self.generated_dir.mkdir(parents=True, exist_ok=True)
        self.cache = {}

    def generate(
        self, modelo: str, tema: str, options: Optional[Dict] = None
    ) -> Dict[str, Any]:
        """
        Gera conteúdo baseado em modelo.

        Args:
            modelo: Nome do modelo (ex: "concessionaria_viral")
            tema: Tema do conteúdo (ex: "financiamento de carro")
            options: Opções de geração

        Returns:
            Dict com conteúdo gerado
        """
        options = options or {
            "formato": "carousel",
            "slides": 7,
            "variacao": 1,
            "ab_test": True,
            "include_copy_alternatives": True,
            "include_hashtags": True,
            "include_timing": True,
            "variaveis_custom": {},
        }

        # Load model (simplified - in production, load from file)
        model = self._load_model(modelo)

        if not model:
            return {"error": f"Modelo {modelo} não encontrado"}

        # Generate content based on format
        if options["formato"] == "carousel":
            content = self._generate_carousel(model, tema, options)
        elif options["formato"] == "reels":
            content = self._generate_reels(model, tema, options)
        elif options["formato"] == "static":
            content = self._generate_static(model, tema, options)
        else:
            content = self._generate_carousel(model, tema, options)

        # Add variants if requested
        if options.get("ab_test"):
            content["ab_test_variations"] = self._generate_ab_variations(content, model)

        # Add copy alternatives if requested
        if options.get("include_copy_alternatives"):
            content["copy_alternativas"] = self._generate_copy_alternatives(
                content, model
            )

        # Add hashtags if requested
        if options.get("include_hashtags"):
            content["hashtags"] = self._generate_hashtags(tema, model)

        # Add timing if requested
        if options.get("include_timing"):
            content["timing_recomendado"] = self._generate_timing(model)

        # Save generated content
        self._save_content(content)

        return content

    def _load_model(self, nome: str) -> Optional[Dict]:
        """Carrega modelo (simplificado)."""
        # In production, load from file
        models_dir = Path.home() / ".neuro-skills" / "viral-content-creator" / "models"
        filepath = models_dir / f"{nome}.json"

        if filepath.exists():
            with open(filepath, "r", encoding="utf-8") as f:
                return json.load(f)

        # Return default model structure
        return {
            "modelo": {
                "nome": nome,
                "identidade_visual": self._get_default_visual(),
                "copy_framework": self._get_default_copy(),
                "hashtags_framework": self._get_default_hashtags(),
                "variaveis_dynamic": self._get_default_variables(nome),
            }
        }

    def _get_default_visual(self) -> Dict:
        """Retorna identidade visual padrão."""
        return {
            "paleta": {
                "primaria": "#000000",
                "secundaria": "#FFFFFF",
                "destaque": "#D4AF37",
                "fundo": "#0A0A0F",
            },
            "tipografia": {
                "headline": {"fonte": "Inter", "peso": 700, "tamanho": 48},
                "body": {"fonte": "Inter", "peso": 400, "tamanho": 24},
                "cta": {"fonte": "Inter", "peso": 600, "tamanho": 20},
            },
        }

    def _get_default_copy(self) -> Dict:
        """Retorna framework de copy padrão."""
        return {
            "hooks": [
                "Você sabia que {insight}?",
                "{numero}% das pessoas erram ao {acao}.",
                "O que ninguém te conta sobre {topico}.",
            ],
            "estruturas": [
                "HOOK → PROBLEMA → SOLUÇÃO → CTA",
                "DADO → CONTEXTO → APLICAÇÃO → CTA",
            ],
            "ctas": [
                "Salva para ver depois 💾",
                "Comenta SIM se você faz isso ✅",
                "Envia para quem precisa saber 📤",
            ],
        }

    def _get_default_hashtags(self) -> Dict:
        """Retorna framework de hashtags padrão."""
        return {
            "estrategia": "fita_infinita",
            "quantidade_min": 5,
            "quantidade_max": 10,
            "categorias": ["nichada", "industria", "tendencia", "branded"],
        }

    def _get_default_variables(self, nome: str) -> Dict:
        """Retorna variáveis dinâmicas padrão."""
        return {
            "{tema}": nome.replace("_viral", ""),
            "{insight}": "algo surpreendente",
            "{numero}": "90",
            "{acao}": "fazer isso",
        }

    def _generate_carousel(
        self, model: Dict, tema: str, options: Dict
    ) -> Dict[str, Any]:
        """Gera conteúdo para carrossel."""
        num_slides = options.get("slides", 7)
        variaveis = self._merge_variables(
            model, tema, options.get("variaveis_custom", {})
        )

        slides = []
        score_total = 0

        # Define slide sequence
        slide_sequence = [
            "capa",
            "problema",
            "dado",
            "solucao",
            "exemplo",
            "value",
            "cta",
        ]

        for i, slide_tipo in enumerate(slide_sequence[:num_slides]):
            slide = self._generate_slide(slide_tipo, i + 1, model, variaveis, tema)
            slides.append(slide)
            score_total += (
                slide.get("score", 0) * self.SLIDE_TYPES[slide_tipo]["score_weight"]
            )

        return {
            "conteudos_gerados": [
                {
                    "id": f"content_{datetime.now().strftime('%Y%m%d%H%M%S')}",
                    "tipo": "carousel",
                    "modelo": model["modelo"]["nome"],
                    "tema": tema,
                    "slides": num_slides,
                    "slides_content": slides,
                    "viralidade_score": round(score_total, 1),
                }
            ]
        }

    def _generate_slide(
        self, slide_tipo: str, numero: int, model: Dict, variaveis: Dict, tema: str
    ) -> Dict[str, Any]:
        """Gera um slide específico."""
        templates = {
            "capa": self._generate_cover_slide,
            "problema": self._generate_problem_slide,
            "dado": self._generate_data_slide,
            "solucao": self._generate_solution_slide,
            "exemplo": self._generate_example_slide,
            "value": self._generate_value_slide,
            "cta": self._generate_cta_slide,
        }

        generator = templates.get(slide_tipo, self._generate_default_slide)
        slide = generator(numero, model, variaveis, tema)

        # Add visual specs
        slide["visual"] = self._get_visual_specs(slide_tipo, model)

        return slide

    def _generate_cover_slide(
        self, numero: int, model: Dict, variaveis: Dict, tema: str
    ) -> Dict[str, Any]:
        """Gera slide de capa."""
        hooks = model["modelo"]["copy_framework"]["hooks"]
        hook_template = random.choice(hooks)

        # Replace variables
        hook = self._replace_variables(hook_template, variaveis)

        return {
            "numero": numero,
            "tipo": "capa",
            "texto": hook,
            "score": 9.0,
            "elementos": ["badge_NOVO", "seta_baixo"],
        }

    def _generate_problem_slide(
        self, numero: int, model: Dict, variaveis: Dict, tema: str
    ) -> Dict[str, Any]:
        """Gera slide de problema."""
        return {
            "numero": numero,
            "tipo": "problema",
            "texto": f"Porque ninguém te conta que {tema} é diferente do que parece.",
            "score": 8.5,
            "elementos": ["texto_destaque", "icone_interrogacao"],
        }

    def _generate_data_slide(
        self, numero: int, model: Dict, variaveis: Dict, tema: str
    ) -> Dict[str, Any]:
        """Gera slide de dado."""
        return {
            "numero": numero,
            "tipo": "dado",
            "texto": f"Em média, você pode economizar 30% em {tema}.",
            "numero_grande": "30%",
            "subtexto": f"de economia em {tema}",
            "score": 8.0,
            "elementos": ["numero_grande", "icone_grafico"],
        }

    def _generate_solution_slide(
        self, numero: int, model: Dict, variaveis: Dict, tema: str
    ) -> Dict[str, Any]:
        """Gera slide de solução."""
        return {
            "numero": numero,
            "tipo": "solucao",
            "texto": f"3 passos para resolver seu problema com {tema}:",
            "items": [
                f"Pesquise sobre {tema}",
                "Compare opções disponíveis",
                "Tome uma decisão informada",
            ],
            "score": 8.0,
            "elementos": ["lista_checkmarks", "numeros"],
        }

    def _generate_example_slide(
        self, numero: int, model: Dict, variaveis: Dict, tema: str
    ) -> Dict[str, Any]:
        """Gera slide de exemplo."""
        return {
            "numero": numero,
            "tipo": "exemplo",
            "texto": f"João economizou R$ 12.000 fazendo isso com {tema}.",
            "before": "R$ 48.000",
            "after": "R$ 36.000",
            "economia": "R$ 12.000",
            "score": 7.5,
            "elementos": ["comparacao_visual", "icone_pessoa"],
        }

    def _generate_value_slide(
        self, numero: int, model: Dict, variaveis: Dict, tema: str
    ) -> Dict[str, Any]:
        """Gera slide de value."""
        return {
            "numero": numero,
            "tipo": "value",
            "texto": f"Agora você sabe o que 90% não sabia sobre {tema}.",
            "score": 8.0,
            "elementos": ["conclusao", "destaque"],
        }

    def _generate_cta_slide(
        self, numero: int, model: Dict, variaveis: Dict, tema: str
    ) -> Dict[str, Any]:
        """Gera slide de CTA."""
        ctas = model["modelo"]["copy_framework"]["ctas"]
        cta = random.choice(ctas)

        return {
            "numero": numero,
            "tipo": "cta",
            "texto": cta,
            "score": 9.2,
            "elementos": ["icones", "setas_para_cta"],
        }

    def _generate_default_slide(
        self, numero: int, model: Dict, variaveis: Dict, tema: str
    ) -> Dict[str, Any]:
        """Gera slide padrão."""
        return {
            "numero": numero,
            "tipo": "default",
            "texto": f"Informação sobre {tema}",
            "score": 7.0,
            "elementos": ["texto", "icone"],
        }

    def _get_visual_specs(self, slide_tipo: str, model: Dict) -> Dict[str, Any]:
        """Obtém especificações visuais para um slide."""
        visual = model["modelo"]["identidade_visual"]

        return {
            "background": visual["paleta"]["fundo"],
            "texto_cor": visual["paleta"]["secundaria"],
            "destaque_cor": visual["paleta"]["destaque"],
            "tipografia": visual["tipografia"],
            "elementos": self.SLIDE_TYPES[slide_tipo]["elementos"],
        }

    def _merge_variables(self, model: Dict, tema: str, custom: Dict) -> Dict[str, str]:
        """Mescla variáveis do modelo, tema e customizadas."""
        variaveis = model["modelo"].get("variaveis_dynamic", {})
        variaveis["{tema}"] = tema
        variaveis.update(custom)
        return variaveis

    def _replace_variables(self, template: str, variaveis: Dict) -> str:
        """Substitui variáveis no template."""
        result = template
        for var, valor in variaveis.items():
            result = result.replace(var, str(valor))
        return result

    def _generate_ab_variations(self, content: Dict, model: Dict) -> List[Dict]:
        """Gera variações A/B para o conteúdo."""
        return [
            {
                "id": "var_a",
                "hook": "Por que 90% cometem esse erro?",
                "tipo": "dado_chocante",
            },
            {
                "id": "var_b",
                "hook": "O que ninguém te conta sobre isso.",
                "tipo": "conspiracao",
            },
        ]

    def _generate_copy_alternatives(
        self, content: Dict, model: Dict
    ) -> Dict[str, List[str]]:
        """Gera alternativas de copy."""
        return {
            "hooks": [
                "Você já pagou mais do que deveria?",
                "O vendedor TE conta isso? Claro que não.",
                "A oferta que eles fazem é REAL ou é o máximo que você aceita?",
            ],
            "ctas": [
                "Salva agora antes de decidir 💾",
                "Envia pro amigo que precisa 📤",
                "Comenta DUVIDA que te explico ✅",
            ],
        }

    def _generate_hashtags(self, tema: str, model: Dict) -> List[str]:
        """Gera hashtags relevantes."""
        # Simplified - in production, would use trend analysis
        base_tags = [f"#{tema.replace(' ', '').lower()}"]

        trending = ["#dica", "#viral", "#aprenda", "#descomplica"]

        return base_tags + trending[:4]

    def _generate_timing(self, model: Dict) -> Dict[str, Any]:
        """Gera recomendação de timing."""
        timing = model["modelo"].get("timing", {})

        return {
            "melhor_dia": timing.get("dias_melhores", ["quarta"])[0]
            if timing.get("dias_melhores")
            else "quarta",
            "melhor_horario": timing.get("horarios_melhores", ["12:00"])[0]
            if timing.get("horarios_melhores")
            else "12:00",
            "razao": "horário de almoço, maior engajamento",
        }

    def _generate_reels(self, model: Dict, tema: str, options: Dict) -> Dict[str, Any]:
        """Gera conteúdo para Reels."""
        return {
            "conteudos_gerados": [
                {
                    "id": f"content_{datetime.now().strftime('%Y%m%d%H%M%S')}",
                    "tipo": "reels",
                    "modelo": model["modelo"]["nome"],
                    "tema": tema,
                    "duracao_segundos": 15,
                    "estrutura": {
                        "0-3s": "Hook visual + textual",
                        "3-10s": "Desenvolvimento rápido",
                        "10-15s": "CTA + repete loop",
                    },
                }
            ]
        }

    def _generate_static(self, model: Dict, tema: str, options: Dict) -> Dict[str, Any]:
        """Gera conteúdo para post estático."""
        return {
            "conteudos_gerados": [
                {
                    "id": f"content_{datetime.now().strftime('%Y%m%d%H%M%S')}",
                    "tipo": "static",
                    "modelo": model["modelo"]["nome"],
                    "tema": tema,
                    "formato": "4:5",
                    "estrutura_visual": {
                        "zona_atencao": "33% superior",
                        "texto_principal": "centro",
                        "cta": "20% inferior",
                    },
                }
            ]
        }

    def generate_batch(
        self,
        modelo: str,
        temas: List[str],
        por_tema: int = 3,
        formato: str = "carousel",
    ) -> Dict[str, Any]:
        """Gera múltiplos conteúdos em lote."""
        results = {}

        for tema in temas:
            variations = []
            for i in range(por_tema):
                content = self.generate(
                    modelo, tema, {"formato": formato, "variacao": i + 1}
                )
                variations.append(content)

            results[tema] = variations

        return {"batch": results, "total": len(temas) * por_tema}

    def regenerate(
        self, content_id: str, manter: List[str], alterar: List[str]
    ) -> Dict[str, Any]:
        """Regenera conteúdo mantendo ou alterando elementos."""
        # Load content from cache or file
        # Simplified - in production, load from storage
        return {
            "content_id": content_id,
            "status": "regenerated",
            "mantido": manter,
            "alterado": alterar,
        }

    def _save_content(self, content: Dict) -> None:
        """Salva conteúdo gerado."""
        content_id = content.get("conteudos_gerados", [{}])[0].get(
            "id", f"content_{datetime.now().strftime('%Y%m%d%H%M%S')}"
        )
        filepath = self.generated_dir / f"{content_id}.json"

        with open(filepath, "w", encoding="utf-8") as f:
            json.dump(content, f, ensure_ascii=False, indent=2)

        self.cache[content_id] = content
