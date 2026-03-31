import { buildFallbackAgentRun, type AgentRunInput } from "@/lib/agno-fallback";
import { DEFAULT_AGENTS } from "@/lib/default-state";

export async function POST(request: Request) {
  const body = (await request.json()) as AgentRunInput;
  const target = DEFAULT_AGENTS.find((agent) => agent.id === body.agentId);
  const baseUrl = process.env.AGNO_BASE_URL;

  let payload = buildFallbackAgentRun(target, body);

  if (baseUrl) {
    try {
      const response = await fetch(`${baseUrl.replace(/\/$/, "")}/api/agents/run`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(body),
      });
      if (response.ok) {
        payload = await response.json();
      }
    } catch {
      // Keep fallback payload.
    }
  }

  const encoder = new TextEncoder();
  const stream = new ReadableStream({
    start(controller) {
      const emit = (event: string, data: unknown) => {
        controller.enqueue(encoder.encode(`event: ${event}\ndata: ${JSON.stringify(data)}\n\n`));
      };

      emit("run_started", {
        runId: payload.runId,
        agentId: payload.agentId,
        agentName: payload.agentName,
      });

      for (const event of payload.events || []) {
        emit(event.type, event);
      }

      const deltas = payload.responseText.split(/(?<=[.!?])\s+/);
      for (const delta of deltas) {
        emit("text_delta", { delta });
      }

      emit("state_snapshot", payload.state || {});
      emit("a2ui", { widgets: payload.widgets || [] });
      emit("run_finished", payload);
      controller.close();
    },
  });

  return new Response(stream, {
    headers: {
      "Content-Type": "text/event-stream",
      "Cache-Control": "no-cache, no-transform",
      Connection: "keep-alive",
    },
  });
}
