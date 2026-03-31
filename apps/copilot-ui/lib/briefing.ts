import type { BriefingAnalysis } from "@/types/app";

export function analyzeBriefingText(briefingText: string): BriefingAnalysis {
  const lines = briefingText.split("\n");
  const result: BriefingAnalysis = {
    missingInfo: [],
  };

  for (const rawLine of lines) {
    const line = rawLine.trim();
    if (!line) continue;

    if (includesAny(line, ["cliente:", "client:"])) {
      result.client = valueAfterColon(line);
    } else if (includesAny(line, ["produto:", "product:", "serviço:"])) {
      result.product = valueAfterColon(line);
    } else if (includesAny(line, ["objetivo:", "objective:"])) {
      result.objective = normalizeObjective(valueAfterColon(line));
    } else if (includesAny(line, ["orçamento:", "budget:", "investimento:"])) {
      const value = onlyNumber(valueAfterColon(line));
      if (value) result.budget = Number(value);
    } else if (includesAny(line, ["cpa:", "cpa alvo:"])) {
      const value = onlyDecimal(valueAfterColon(line));
      if (value) result.targetCpa = Number(value);
    } else if (includesAny(line, ["roas:", "roas alvo:"])) {
      const value = onlyDecimal(valueAfterColon(line));
      if (value) result.targetRoas = Number(value);
    }
  }

  if (!result.client) result.missingInfo.push("Nome do cliente");
  if (!result.product) result.missingInfo.push("Produto/Serviço");
  if (!result.objective) result.missingInfo.push("Objetivo");
  if (!result.budget) result.missingInfo.push("Orçamento");

  return result;
}

function includesAny(value: string, needles: string[]) {
  const lower = value.toLowerCase();
  return needles.some((needle) => lower.includes(needle));
}

function valueAfterColon(value: string) {
  return value.split(":").slice(1).join(":").trim();
}

function onlyNumber(value: string) {
  return value.replace(/[^\d]/g, "");
}

function onlyDecimal(value: string) {
  return value.replace(/[^\d.]/g, "");
}

function normalizeObjective(value: string) {
  const lower = value.toLowerCase();
  if (lower.includes("venda") || lower.includes("sales") || lower.includes("convers")) {
    return "CONVERSIONS";
  }
  if (lower.includes("tráfego") || lower.includes("traffic")) {
    return "TRAFFIC";
  }
  if (lower.includes("lead")) {
    return "LEAD_GENERATION";
  }
  if (lower.includes("awareness") || lower.includes("reconhecimento")) {
    return "AWARENESS";
  }
  return value || "CONVERSIONS";
}
