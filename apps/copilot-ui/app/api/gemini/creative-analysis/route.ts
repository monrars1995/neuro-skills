import { NextRequest, NextResponse } from "next/server";

type GeminiResponse = {
  candidates?: Array<{
    content?: {
      parts?: Array<{ text?: string }>;
    };
  }>;
};

export async function POST(request: NextRequest) {
  const body = await request.json();
  const imageBase64 = body.imageBase64 as string | undefined;
  const mimeType = body.mimeType as string | undefined;
  const prompt = (body.prompt as string | undefined) ||
    "Analise este criativo para Meta Ads e devolva resumo, hooks, leitura visual, ideias de melhoria e score.";
  const vertical = body.context?.vertical as string | undefined;

  if (!imageBase64 || !mimeType) {
    return NextResponse.json({ error: "imageBase64 e mimeType são obrigatórios." }, { status: 400 });
  }

  const apiKey = process.env.GOOGLE_API_KEY;
  const model = process.env.GOOGLE_MODEL?.replace("google/", "") || "gemini-2.5-pro";

  if (!apiKey) {
    return NextResponse.json(
      {
        analysis: {
          summary: `Fallback local: configure GOOGLE_API_KEY para análise multimodal real.${vertical ? ` Vertical: ${vertical}.` : ""}`,
          hooks: ["Destaque o benefício na primeira linha", "Use contraste forte na capa"],
          visualNotes: ["Paleta escura com acento dourado", "Composição com foco central"],
          improvementIdeas: ["Adicionar CTA mais explícito", "Testar variação com número grande"],
          score: 7.8,
        },
      },
      { status: 200 },
    );
  }

  const instruction = `
Você é um diretor criativo e estrategista de performance para Meta Ads.
Contexto da vertical: ${vertical || "não informado"}.

Analise a imagem enviada e responda APENAS em JSON válido com esta estrutura:
{
  "summary": "...",
  "hooks": ["...", "..."],
  "visualNotes": ["...", "..."],
  "improvementIdeas": ["...", "..."],
  "score": 0
}

Critérios:
- summary: 1 frase objetiva
- hooks: 2 a 4 hooks sugeridos
- visualNotes: 2 a 4 leituras visuais
- improvementIdeas: 2 a 4 melhorias práticas
- score: nota de 0 a 10

Prompt adicional do usuário: ${prompt}
`;

  const response = await fetch(
    `https://generativelanguage.googleapis.com/v1beta/models/${model}:generateContent?key=${apiKey}`,
    {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({
        contents: [
          {
            parts: [
              { text: instruction },
              {
                inlineData: {
                  mimeType,
                  data: imageBase64,
                },
              },
            ],
          },
        ],
      }),
    },
  );

  if (!response.ok) {
    const errorText = await response.text();
    return NextResponse.json({ error: errorText }, { status: 500 });
  }

  const payload = (await response.json()) as GeminiResponse;
  const text = payload.candidates?.[0]?.content?.parts?.map((part) => part.text || "").join("\n") || "{}";
  const normalized = extractJson(text);

  return NextResponse.json({ analysis: normalized });
}

function extractJson(text: string) {
  const fenced = text.match(/```json\s*([\s\S]*?)```/i);
  const raw = fenced?.[1] || text;
  try {
    return JSON.parse(raw);
  } catch {
    const first = raw.indexOf("{");
    const last = raw.lastIndexOf("}");
    if (first >= 0 && last > first) {
      return JSON.parse(raw.slice(first, last + 1));
    }
    throw new Error("Gemini não retornou JSON válido.");
  }
}
