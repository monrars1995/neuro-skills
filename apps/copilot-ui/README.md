# Copilot UI

Aplicação web completa do Neuro Skills usando:

- Next.js App Router
- CopilotKit
- Gemini multimodal para análise de criativos

## Rodar localmente

```bash
cd apps/copilot-ui
npm install
cp .env.example .env
npm run dev
```

## Variáveis

- `GOOGLE_API_KEY`: chave da Gemini API
- `GOOGLE_MODEL`: padrão `google/gemini-2.5-pro`
- `OPENAI_API_KEY`: fallback opcional para runtime
- `ANTHROPIC_API_KEY`: fallback opcional para runtime

## Escopo atual

- Overview da operação
- Briefing analyzer
- Workspace de criativos com análise multimodal
- Rascunhos de campanha
- Snapshot de analytics
- Jobs de automação
- Settings de clientes e contas

O copiloto atua sobre a aplicação inteira via ações de frontend expostas no CopilotKit.
