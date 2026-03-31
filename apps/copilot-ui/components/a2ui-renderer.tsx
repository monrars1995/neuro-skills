"use client";

import type { A2UIBlock } from "@/types/app";

export function A2UIRenderer({ blocks }: { blocks: A2UIBlock[] }) {
  if (!blocks.length) {
    return <p className="empty-state">Nenhum widget gerado ainda.</p>;
  }

  return (
    <div className="a2ui-grid">
      {blocks.map((block) => (
        <article key={block.id} className={`a2ui-card a2ui-${block.type}`}>
          <div className="a2ui-header">
            <span className="eyebrow">A2UI</span>
            <h4>{block.title}</h4>
            {block.description && <p>{block.description}</p>}
          </div>

          {block.type === "metric_grid" && block.stats && (
            <div className="a2ui-stats">
              {block.stats.map((stat) => (
                <div key={`${block.id}-${stat.label}`} className={`a2ui-stat ${stat.tone || "neutral"}`}>
                  <span>{stat.label}</span>
                  <strong>{stat.value}</strong>
                </div>
              ))}
            </div>
          )}

          {block.type === "checklist" && block.items && (
            <div className="a2ui-list">
              {block.items.map((item) => (
                <div key={`${block.id}-${item.label}`} className={`a2ui-list-item ${item.status || "pending"}`}>
                  <strong>{item.label}</strong>
                  <span>{item.status || "pending"}</span>
                </div>
              ))}
            </div>
          )}

          {block.type === "table" && block.rows && (
            <div className="a2ui-table">
              {block.rows.map((row) => (
                <div key={`${block.id}-${row.label}`} className="a2ui-row">
                  <div>
                    <strong>{row.label}</strong>
                    {row.meta && <p>{row.meta}</p>}
                  </div>
                  <span>{row.value}</span>
                </div>
              ))}
            </div>
          )}
        </article>
      ))}
    </div>
  );
}
