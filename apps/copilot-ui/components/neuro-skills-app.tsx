"use client";

import {
  CopilotKit,
  useCopilotAction,
  useCopilotAdditionalInstructions,
  useCopilotReadable,
} from "@copilotkit/react-core";
import {
  CopilotPopup,
  CopilotSidebar,
} from "@copilotkit/react-core/v2";
import { startTransition, useMemo, useState } from "react";

import { analyzeBriefingText } from "@/lib/briefing";
import {
  DEFAULT_ACCOUNTS,
  DEFAULT_ANALYTICS,
  DEFAULT_AUTOMATIONS,
  DEFAULT_CAMPAIGNS,
  DEFAULT_CLIENTS,
  DEFAULT_SECTION,
  DEFAULT_VERTICAL,
  VERTICAL_LABELS,
} from "@/lib/default-state";
import type {
  AnalyticsSnapshot,
  AppSection,
  AutomationJob,
  BriefingAnalysis,
  CampaignDraft,
  ClientRecord,
  CreativeAnalysis,
  MetaAccountRecord,
  UploadedAsset,
  VerticalKey,
} from "@/types/app";

type PendingAsset = UploadedAsset & { base64?: string };

export function NeuroSkillsApp() {
  return (
    <CopilotKit runtimeUrl="/api/copilotkit" showDevConsole>
      <NeuroSkillsWorkspace />
    </CopilotKit>
  );
}

function NeuroSkillsWorkspace() {
  useCopilotAdditionalInstructions(
    {
      instructions:
        "Você é o copiloto principal do Neuro Skills. Ajude o usuário a navegar pela aplicação, estruturar briefings, criar campanhas, configurar automações e analisar criativos com foco em performance.",
    },
    [],
  );

  const [section, setSection] = useState<AppSection>(DEFAULT_SECTION);
  const [vertical, setVertical] = useState<VerticalKey>(DEFAULT_VERTICAL);
  const [clients, setClients] = useState<ClientRecord[]>(DEFAULT_CLIENTS);
  const [accounts, setAccounts] = useState<MetaAccountRecord[]>(DEFAULT_ACCOUNTS);
  const [briefing, setBriefing] = useState("");
  const [briefingAnalysis, setBriefingAnalysis] = useState<BriefingAnalysis | null>(null);
  const [assets, setAssets] = useState<PendingAsset[]>([]);
  const [campaigns, setCampaigns] = useState<CampaignDraft[]>(DEFAULT_CAMPAIGNS);
  const [automations, setAutomations] = useState<AutomationJob[]>(DEFAULT_AUTOMATIONS);
  const [analytics] = useState<AnalyticsSnapshot>(DEFAULT_ANALYTICS);
  const [isBusy, setIsBusy] = useState(false);

  const activeVertical = VERTICAL_LABELS[vertical];
  const metrics = useMemo(
    () => [
      { label: "Spend", value: `R$ ${analytics.spend.toLocaleString("pt-BR")}` },
      { label: "CTR", value: `${analytics.ctr.toFixed(2)}%` },
      { label: "CPC", value: `R$ ${analytics.cpc.toFixed(2)}` },
      { label: "ROAS", value: `${analytics.roas.toFixed(2)}x` },
    ],
    [analytics],
  );

  useCopilotReadable({ description: "Seção atual da aplicação", value: section });
  useCopilotReadable({ description: "Vertical ativa da operação", value: JSON.stringify(activeVertical) });
  useCopilotReadable({ description: "Clientes cadastrados", value: JSON.stringify(clients) });
  useCopilotReadable({ description: "Contas Meta configuradas", value: JSON.stringify(accounts) });
  useCopilotReadable({ description: "Análise atual do briefing", value: JSON.stringify(briefingAnalysis) });
  useCopilotReadable({ description: "Criativos enviados e análises", value: JSON.stringify(assets.map(stripBase64)) });
  useCopilotReadable({ description: "Campanhas em rascunho ou prontas", value: JSON.stringify(campaigns) });
  useCopilotReadable({ description: "Automações configuradas", value: JSON.stringify(automations) });
  useCopilotReadable({ description: "Snapshot de analytics da conta", value: JSON.stringify(analytics) });

  useCopilotAction({
    name: "navigateSection",
    description: "Navega para uma seção da aplicação",
    parameters: [{ name: "section", type: "string", required: true }],
    handler: ({ section: nextSection }) => {
      startTransition(() => setSection((nextSection as AppSection) || "overview"));
    },
  });

  useCopilotAction({
    name: "setVertical",
    description: "Define a vertical principal da operação",
    parameters: [{ name: "vertical", type: "string", required: true }],
    handler: ({ vertical: nextVertical }) => {
      const safe = (nextVertical as VerticalKey) || DEFAULT_VERTICAL;
      if (safe in VERTICAL_LABELS) setVertical(safe);
    },
  });

  useCopilotAction({
    name: "createClient",
    description: "Cria um novo cliente na operação",
    parameters: [
      { name: "name", type: "string", required: true },
      { name: "industry", type: "string", required: true },
      { name: "vertical", type: "string", required: true },
      { name: "monthlyBudget", type: "number", required: true },
    ],
    handler: ({ name, industry, vertical: nextVertical, monthlyBudget }) => {
      const newClient: ClientRecord = {
        id: crypto.randomUUID(),
        name,
        industry,
        vertical: (nextVertical as VerticalKey) || DEFAULT_VERTICAL,
        monthlyBudget: Number(monthlyBudget || 0),
        locations: ["Brasil"],
      };
      setClients((current) => [newClient, ...current]);
      setSection("settings");
    },
    render: ({ args }) => (
      <ActionPreview
        title="Cliente criado"
        lines={[
          String(args.name || ""),
          String(args.industry || ""),
          `Budget: R$ ${String(args.monthlyBudget || 0)}`,
        ]}
      />
    ),
  });

  useCopilotAction({
    name: "configureMetaAccount",
    description: "Configura ou adiciona uma conta Meta Ads",
    parameters: [
      { name: "name", type: "string", required: true },
      { name: "adAccountId", type: "string", required: true },
      { name: "pageId", type: "string", required: false },
      { name: "pixelId", type: "string", required: false },
    ],
    handler: ({ name, adAccountId, pageId, pixelId }) => {
      const newAccount: MetaAccountRecord = {
        id: crypto.randomUUID(),
        name,
        adAccountId,
        pageId,
        pixelId,
      };
      setAccounts((current) => [newAccount, ...current]);
      setSection("settings");
    },
  });

  useCopilotAction({
    name: "saveBriefing",
    description: "Salva e analisa o briefing atual da campanha",
    parameters: [{ name: "text", type: "string", required: true }],
    handler: ({ text }) => {
      setBriefing(text);
      setBriefingAnalysis(analyzeBriefingText(text));
      setSection("briefing");
    },
    render: ({ args }) => {
      const analysis = analyzeBriefingText(String(args.text || ""));
      return (
        <ActionPreview
          title="Briefing analisado"
          lines={[
            `Cliente: ${analysis.client || "não identificado"}`,
            `Produto: ${analysis.product || "não identificado"}`,
            `Objetivo: ${analysis.objective || "não identificado"}`,
          ]}
        />
      );
    },
  });

  useCopilotAction({
    name: "createCampaignDraft",
    description: "Cria um rascunho de campanha dentro da aplicação",
    parameters: [
      { name: "name", type: "string", required: true },
      { name: "objective", type: "string", required: true },
      { name: "budget", type: "number", required: true },
      { name: "copyAngle", type: "string", required: true },
    ],
    handler: ({ name, objective, budget, copyAngle }) => {
      const draft: CampaignDraft = {
        id: crypto.randomUUID(),
        name,
        objective,
        budget: Number(budget),
        status: "draft",
        copyAngle,
      };
      setCampaigns((current) => [draft, ...current]);
      setSection("campaigns");
    },
    render: ({ args }) => (
      <ActionPreview
        title="Rascunho de campanha"
        lines={[
          String(args.name || ""),
          String(args.objective || ""),
          `Budget: R$ ${String(args.budget || 0)}`,
        ]}
      />
    ),
  });

  useCopilotAction({
    name: "scheduleAutomation",
    description: "Agenda uma nova automação operacional",
    parameters: [
      { name: "name", type: "string", required: true },
      { name: "type", type: "string", required: true },
      { name: "schedule", type: "string", required: true },
    ],
    handler: ({ name, type, schedule }) => {
      const job: AutomationJob = {
        id: crypto.randomUUID(),
        name,
        type,
        schedule,
        enabled: true,
      };
      setAutomations((current) => [job, ...current]);
      setSection("automations");
    },
  });

  useCopilotAction({
    name: "analyzeUploadedCreative",
    description: "Analisa um criativo já enviado usando Gemini multimodal",
    parameters: [
      { name: "assetId", type: "string", required: true },
      { name: "prompt", type: "string", required: false },
    ],
    handler: async ({ assetId, prompt }) => {
      const target = assets.find((asset) => asset.id === assetId);
      if (!target?.base64 || target.kind !== "image") return;
      setAssets((current) => current.map((asset) => (asset.id === assetId ? { ...asset, status: "analyzing" } : asset)));

      const response = await fetch("/api/gemini/creative-analysis", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          imageBase64: target.base64,
          mimeType: target.mimeType || "image/png",
          prompt,
          context: { vertical },
        }),
      });

      const payload = (await response.json()) as { analysis?: CreativeAnalysis; error?: string };
      if (payload.analysis) {
        setAssets((current) =>
          current.map((asset) =>
            asset.id === assetId ? { ...asset, status: "analyzed", analysis: payload.analysis } : asset,
          ),
        );
      } else {
        setAssets((current) => current.map((asset) => (asset.id === assetId ? { ...asset, status: "uploaded" } : asset)));
      }
      setSection("creatives");
    },
  });

  async function handleFiles(files: FileList | null) {
    if (!files?.length) return;
    const prepared = await Promise.all(Array.from(files).map(fileToAsset));
    setAssets((current) => [...prepared, ...current]);
    setSection("creatives");
  }

  async function analyzeAsset(assetId: string) {
    const target = assets.find((asset) => asset.id === assetId);
    if (!target?.base64 || target.kind !== "image") return;
    setIsBusy(true);
    try {
      const response = await fetch("/api/gemini/creative-analysis", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          imageBase64: target.base64,
          mimeType: target.mimeType || "image/png",
          context: { vertical },
        }),
      });
      const payload = (await response.json()) as { analysis?: CreativeAnalysis };
      if (payload.analysis) {
        setAssets((current) =>
          current.map((asset) =>
            asset.id === assetId ? { ...asset, status: "analyzed", analysis: payload.analysis } : asset,
          ),
        );
      }
    } finally {
      setIsBusy(false);
    }
  }

  return (
    <div className="app-shell">
      <aside className="left-rail">
        <div className="brand-block">
          <div className="brand-mark">N</div>
          <div>
            <h1>Neuro Skills</h1>
            <p>Copilot application</p>
          </div>
        </div>
        <nav className="nav-list">
          {([
            ["overview", "Overview"],
            ["briefing", "Briefing"],
            ["creatives", "Creatives"],
            ["campaigns", "Campaigns"],
            ["analytics", "Analytics"],
            ["automations", "Automations"],
            ["settings", "Settings"],
          ] as [AppSection, string][]).map(([key, label]) => (
            <button key={key} className={section === key ? "nav-item active" : "nav-item"} onClick={() => setSection(key)}>
              {label}
            </button>
          ))}
        </nav>
        <div className="vertical-card">
          <span className="eyebrow">Vertical ativa</span>
          <strong>{activeVertical.title}</strong>
          <p>{activeVertical.description}</p>
          <select value={vertical} onChange={(event) => setVertical(event.target.value as VerticalKey)}>
            {Object.entries(VERTICAL_LABELS).map(([key, data]) => (
              <option key={key} value={key}>
                {data.title}
              </option>
            ))}
          </select>
        </div>
      </aside>

      <main className="main-area">
        <header className="hero-card">
          <div>
            <span className="eyebrow">Aplicação completa</span>
            <h2>Meta Ads + briefing + uploads + analytics + automações</h2>
            <p>
              Port da aplicação para uma interface web agent-native com CopilotKit no centro da experiência e
              Gemini multimodal para analisar criativos.
            </p>
          </div>
          <div className="hero-actions">
            <label className="upload-button">
              Enviar criativo
              <input type="file" accept="image/*,video/*" multiple onChange={(event) => handleFiles(event.target.files)} />
            </label>
          </div>
        </header>

        <section className="metrics-grid">
          {metrics.map((metric) => (
            <article key={metric.label} className="metric-card">
              <span>{metric.label}</span>
              <strong>{metric.value}</strong>
            </article>
          ))}
        </section>

        {section === "overview" && (
          <section className="panel-grid">
            <Panel title="Clientes">
              {clients.map((client) => (
                <RecordRow key={client.id} title={client.name} subtitle={`${client.industry} · ${VERTICAL_LABELS[client.vertical].title}`} />
              ))}
            </Panel>
            <Panel title="Contas Meta">
              {accounts.map((account) => (
                <RecordRow key={account.id} title={account.name} subtitle={account.adAccountId} />
              ))}
            </Panel>
            <Panel title="Campanhas">
              {campaigns.map((campaign) => (
                <RecordRow key={campaign.id} title={campaign.name} subtitle={`${campaign.objective} · ${campaign.status}`} />
              ))}
            </Panel>
            <Panel title="Automações">
              {automations.map((job) => (
                <RecordRow key={job.id} title={job.name} subtitle={`${job.type} · ${job.schedule}`} />
              ))}
            </Panel>
          </section>
        )}

        {section === "briefing" && (
          <section className="panel-grid single">
            <Panel title="Analisador de briefing">
              <textarea
                className="briefing-box"
                placeholder="Cole o briefing completo aqui..."
                value={briefing}
                onChange={(event) => setBriefing(event.target.value)}
              />
              <div className="button-row">
                <button className="primary" onClick={() => setBriefingAnalysis(analyzeBriefingText(briefing))}>
                  Analisar briefing
                </button>
              </div>
              {briefingAnalysis && (
                <div className="analysis-grid">
                  <RecordRow title={`Cliente: ${briefingAnalysis.client || "N/A"}`} subtitle={`Produto: ${briefingAnalysis.product || "N/A"}`} />
                  <RecordRow title={`Objetivo: ${briefingAnalysis.objective || "N/A"}`} subtitle={`Budget: ${briefingAnalysis.budget ? `R$ ${briefingAnalysis.budget}` : "N/A"}`} />
                  <RecordRow title={`CPA: ${briefingAnalysis.targetCpa || "N/A"}`} subtitle={`ROAS: ${briefingAnalysis.targetRoas || "N/A"}`} />
                  <RecordRow title="Pendências" subtitle={briefingAnalysis.missingInfo.join(", ") || "Nenhuma"} />
                </div>
              )}
            </Panel>
          </section>
        )}

        {section === "creatives" && (
          <section className="panel-grid single">
            <Panel title="Criativos e análise multimodal">
              <p className="panel-copy">
                Faça upload de imagens ou vídeos. Para imagens, a análise roda via Gemini multimodal e devolve
                hooks, leitura visual, melhorias e score.
              </p>
              <div className="asset-grid">
                {assets.length === 0 && <p className="empty-state">Nenhum criativo enviado ainda.</p>}
                {assets.map((asset) => (
                  <article key={asset.id} className="asset-card">
                    <div>
                      <strong>{asset.name}</strong>
                      <p>{asset.kind} · {asset.status}</p>
                    </div>
                    {asset.kind === "image" && (
                      <button className="secondary" disabled={isBusy} onClick={() => analyzeAsset(asset.id)}>
                        {asset.status === "analyzed" ? "Reanalisar" : "Analisar com Gemini"}
                      </button>
                    )}
                    {asset.analysis && (
                      <div className="analysis-block">
                        <p><strong>Resumo:</strong> {asset.analysis.summary}</p>
                        <p><strong>Hooks:</strong> {asset.analysis.hooks.join(" · ")}</p>
                        <p><strong>Visual:</strong> {asset.analysis.visualNotes.join(" · ")}</p>
                        <p><strong>Melhorias:</strong> {asset.analysis.improvementIdeas.join(" · ")}</p>
                        <p><strong>Score:</strong> {asset.analysis.score}/10</p>
                      </div>
                    )}
                  </article>
                ))}
              </div>
            </Panel>
          </section>
        )}

        {section === "campaigns" && (
          <section className="panel-grid single">
            <Panel title="Campaign workspace">
              <div className="campaign-grid">
                {campaigns.map((campaign) => (
                  <article key={campaign.id} className="record-card">
                    <strong>{campaign.name}</strong>
                    <p>{campaign.objective}</p>
                    <p>Budget: R$ {campaign.budget.toLocaleString("pt-BR")}</p>
                    <p>Angle: {campaign.copyAngle}</p>
                    <span className={`status-pill ${campaign.status}`}>{campaign.status}</span>
                  </article>
                ))}
              </div>
            </Panel>
          </section>
        )}

        {section === "analytics" && (
          <section className="panel-grid two">
            <Panel title="Resumo da conta">
              <RecordRow title={`Impressions: ${analytics.impressions.toLocaleString("pt-BR")}`} subtitle={`Clicks: ${analytics.clicks.toLocaleString("pt-BR")}`} />
              <RecordRow title={`CTR: ${analytics.ctr.toFixed(2)}%`} subtitle={`CPC: R$ ${analytics.cpc.toFixed(2)}`} />
              <RecordRow title={`Spend: R$ ${analytics.spend.toLocaleString("pt-BR")}`} subtitle={`ROAS: ${analytics.roas.toFixed(2)}x`} />
            </Panel>
            <Panel title="Leituras rápidas">
              <ul className="bullet-list">
                <li>CTR acima de 2% em campanhas principais.</li>
                <li>ROAS saudável para operação de topo + fundo.</li>
                <li>Melhor janela para testes: 12h e 19h.</li>
              </ul>
            </Panel>
          </section>
        )}

        {section === "automations" && (
          <section className="panel-grid single">
            <Panel title="Automações">
              {automations.map((job) => (
                <article key={job.id} className="record-card inline">
                  <div>
                    <strong>{job.name}</strong>
                    <p>{job.type} · {job.schedule}</p>
                  </div>
                  <span className={`status-pill ${job.enabled ? "ready" : "paused"}`}>{job.enabled ? "ativo" : "pausado"}</span>
                </article>
              ))}
            </Panel>
          </section>
        )}

        {section === "settings" && (
          <section className="panel-grid two">
            <Panel title="Clientes">
              {clients.map((client) => (
                <RecordRow key={client.id} title={client.name} subtitle={`R$ ${client.monthlyBudget.toLocaleString("pt-BR")}/mês`} />
              ))}
            </Panel>
            <Panel title="Contas Meta">
              {accounts.map((account) => (
                <RecordRow key={account.id} title={account.name} subtitle={account.adAccountId} />
              ))}
            </Panel>
          </section>
        )}
      </main>

      <CopilotSidebar defaultOpen width="420px" />
      <CopilotPopup defaultOpen={false} />
    </div>
  );
}

function Panel({ title, children }: { title: string; children: React.ReactNode }) {
  return (
    <section className="panel">
      <div className="panel-header">
        <h3>{title}</h3>
      </div>
      {children}
    </section>
  );
}

function RecordRow({ title, subtitle }: { title: string; subtitle: string }) {
  return (
    <article className="record-card">
      <strong>{title}</strong>
      <p>{subtitle}</p>
    </article>
  );
}

function ActionPreview({ title, lines }: { title: string; lines: string[] }) {
  return (
    <div className="action-preview">
      <strong>{title}</strong>
      {lines.map((line) => (
        <p key={line}>{line}</p>
      ))}
    </div>
  );
}

function stripBase64(asset: PendingAsset) {
  const { base64, ...rest } = asset;
  return rest;
}

async function fileToAsset(file: File): Promise<PendingAsset> {
  const base64 = await fileToBase64(file);
  return {
    id: crypto.randomUUID(),
    name: file.name,
    kind: file.type.startsWith("video/") ? "video" : "image",
    status: "uploaded",
    mimeType: file.type,
    base64,
  };
}

function fileToBase64(file: File): Promise<string> {
  return new Promise((resolve, reject) => {
    const reader = new FileReader();
    reader.onload = () => {
      const result = String(reader.result || "");
      resolve(result.includes(",") ? result.split(",")[1] : result);
    };
    reader.onerror = reject;
    reader.readAsDataURL(file);
  });
}
