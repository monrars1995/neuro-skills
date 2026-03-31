from __future__ import annotations

from fastapi import FastAPI
from fastapi.responses import JSONResponse, StreamingResponse

from agents import AGENT_DEFINITIONS, build_agents, build_run_output
from schemas import AgentDescriptor, AgentRunRequest, AgentRunResponse


app = FastAPI(title="Neuro Skills Agno OS", version="0.1.0")
agents = build_agents()


@app.get("/health")
def health():
    return {"ok": True, "service": "agno-os"}


@app.get("/api/agents")
def list_agents():
    return [descriptor.model_dump() for descriptor in AGENT_DEFINITIONS]


@app.post("/api/agents/run")
def run_agent(payload: AgentRunRequest):
    agent = agents.get(payload.agentId)
    if payload.agentId not in agents:
        return JSONResponse(
            {"error": f"Unknown agent: {payload.agentId}"}, status_code=404
        )

    prompt = build_prompt(payload)
    try:
        if agent is None:
            response_text = (
                "Agno agent disponível em modo fallback. Configure um provider compatível "
                "ou ajuste AGNO_MODEL para um backend instalado."
            )
        else:
            result = agent.run(prompt)
            response_text = extract_response_text(result)
    except Exception as exc:
        response_text = f"Fallback do serviço Agno: {exc}"

    structured = build_run_output(
        payload.agentId, payload.prompt, payload.vertical, response_text
    )
    response = AgentRunResponse(
        runId=structured.events[0].id,
        agentId=payload.agentId,
        agentName=(agent.name if agent is not None else payload.agentId)
        or payload.agentId,
        summary=structured.summary,
        responseText=structured.response_text,
        events=structured.events,
        widgets=structured.widgets,
        state=structured.state,
    )
    return response.model_dump()


@app.post("/api/agui/stream")
def agui_stream(payload: AgentRunRequest):
    response = run_agent(payload)

    def gen():
        yield _event("run_started", {"agentId": payload.agentId})
        for item in response["events"]:
            yield _event(item["type"], item)
        for chunk in response["responseText"].split(". "):
            if chunk.strip():
                yield _event("text_delta", {"delta": chunk.strip() + "."})
        yield _event("a2ui", {"widgets": response["widgets"]})
        yield _event("run_finished", response)

    return StreamingResponse(gen(), media_type="text/event-stream")


def build_prompt(payload: AgentRunRequest) -> str:
    parts = [
        f"Vertical: {payload.vertical}",
        f"Prompt: {payload.prompt}",
    ]
    if payload.briefing:
        parts.append(f"Briefing:\n{payload.briefing}")
    if payload.context:
        parts.append(f"Context: {payload.context}")
    return "\n\n".join(parts)


def extract_response_text(result) -> str:
    if isinstance(result, str):
        return result
    for attribute in ("content", "response", "output", "text"):
        value = getattr(result, attribute, None)
        if isinstance(value, str) and value.strip():
            return value
    return str(result)


def _event(name: str, payload) -> str:
    import json

    return f"event: {name}\ndata: {json.dumps(payload)}\n\n"
