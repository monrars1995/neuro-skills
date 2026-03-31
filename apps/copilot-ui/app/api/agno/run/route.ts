import { NextRequest, NextResponse } from "next/server";

import { buildFallbackAgentRun, type AgentRunInput } from "@/lib/agno-fallback";
import { DEFAULT_AGENTS } from "@/lib/default-state";

export async function POST(request: NextRequest) {
  const body = (await request.json()) as AgentRunInput;
  const target = DEFAULT_AGENTS.find((agent) => agent.id === body.agentId);
  const baseUrl = process.env.AGNO_BASE_URL;

  if (baseUrl) {
    try {
      const response = await fetch(`${baseUrl.replace(/\/$/, "")}/api/agents/run`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(body),
      });

      if (response.ok) {
        const payload = await response.json();
        return NextResponse.json(payload);
      }
    } catch {
      // Fallback below.
    }
  }

  return NextResponse.json(buildFallbackAgentRun(target, body));
}
