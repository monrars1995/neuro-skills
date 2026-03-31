from __future__ import annotations

from typing import Any, Dict, List, Literal, Optional

from pydantic import BaseModel, Field


class A2UIStatItem(BaseModel):
    label: str
    value: str
    tone: Literal["neutral", "success", "warning", "danger"] = "neutral"


class A2UICheckItem(BaseModel):
    label: str
    status: Literal["done", "active", "pending"] = "pending"


class A2UITableRow(BaseModel):
    label: str
    value: str
    meta: Optional[str] = None


class A2UIBlock(BaseModel):
    id: str
    type: Literal["hero", "metric_grid", "checklist", "table", "insight"]
    title: str
    description: Optional[str] = None
    stats: List[A2UIStatItem] = Field(default_factory=list)
    items: List[A2UICheckItem] = Field(default_factory=list)
    rows: List[A2UITableRow] = Field(default_factory=list)
    accent: Optional[str] = None


class AgentEvent(BaseModel):
    id: str
    type: str
    label: str
    detail: Optional[str] = None
    timestamp: str


class AgentRunRequest(BaseModel):
    agentId: str
    prompt: str
    vertical: str
    briefing: Optional[str] = None
    context: Dict[str, Any] = Field(default_factory=dict)


class AgentRunOutput(BaseModel):
    summary: str
    response_text: str
    events: List[AgentEvent] = Field(default_factory=list)
    widgets: List[A2UIBlock] = Field(default_factory=list)
    state: Dict[str, Any] = Field(default_factory=dict)


class AgentRunResponse(BaseModel):
    runId: str
    agentId: str
    agentName: str
    summary: str
    responseText: str
    events: List[AgentEvent]
    widgets: List[A2UIBlock]
    state: Dict[str, Any]


class AgentDescriptor(BaseModel):
    id: str
    name: str
    role: str
    description: str
    icon: str
    starterPrompts: List[str]
