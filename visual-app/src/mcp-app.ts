import { App } from "@modelcontextprotocol/ext-apps";

type Obj = Record<string, any>;
const app = new App({ name: "Meu Artigo Visual", version: "0.1.0" });
let state: Obj | null = null;
let tab = "overview";
let loading = false;

const $ = (id: string): HTMLElement => document.getElementById(id)!;
function el(tag: string, className = "", text = ""): HTMLElement {
  const node = document.createElement(tag);
  if (className) node.className = className;
  if (text) node.textContent = text;
  return node;
}
function add(parent: HTMLElement, tag: string, className = "", text = ""): HTMLElement {
  const child = el(tag, className, text);
  parent.append(child);
  return child;
}
function val(x: unknown): string { return x === null || x === undefined || x === "" ? "—" : String(x); }
function panel(heading: string): HTMLElement {
  const box = el("section", "panel");
  add(box, "h2", "", heading);
  return box;
}
function item(box: HTMLElement, title: string, subtitle: string, status?: string): void {
  const row = add(box, "div", "item");
  const head = add(row, "div", "item-head");
  add(head, "strong", "", title);
  if (status) add(head, "span", "badge", status);
  if (subtitle) add(row, "div", "small muted", subtitle);
}
function kpi(box: HTMLElement, number: unknown, label: string): void {
  const c = add(box, "div", "kpi");
  add(c, "div", "number", val(number));
  add(c, "div", "label", label);
}
function empty(box: HTMLElement, text: string): void { add(box, "div", "empty", text); }
function render(): void {
  const content = $("content");
  content.replaceChildren();
  $("project-title").textContent = state?.project?.title ?? "Painel científico";
  $("context").textContent = state ? "Modo " + state.mode + " · Armazenamento declarado: " + val(state.project.storage_state) : "Dados do projeto autorizado";
  if (!state) { empty(content, "Nenhum dado carregado. Abra pelo comando Acompanhar Meu Artigo."); return; }
  const o = state.operational, s = state.scientific;
  if (tab === "overview") {
    const metrics = add(content, "div", "grid");
    kpi(metrics, o.tasks_done_reported === null ? null : String(o.tasks_done_reported) + "/" + val(o.tasks_total), "Tarefas concluídas (registro)");
    kpi(metrics, o.tasks_blocked, "Bloqueadas");
    kpi(metrics, o.tasks_overdue, "Com prazo vencido");
    kpi(metrics, s.gates_approved_documented === null ? null : String(s.gates_approved_documented) + "/" + val(s.gates_total), "Validações documentadas");
    const next = panel("Sua próxima ação");
    const wrapper = add(next, "div", "next");
    if (o.next_action) {
      add(wrapper, "div", "eyebrow", val(o.next_action.id));
      add(wrapper, "div", "title", val(o.next_action.action));
      add(wrapper, "div", "meta", "Responsável: " + val(o.next_action.owner) + " · Prazo: " + val(o.next_action.deadline));
    } else empty(wrapper, "Nenhuma tarefa executável identificada nos registros.");
    content.append(next);
    const science = panel("Próxima decisão científica");
    const gate = s.next_ready_gate;
    if (gate) item(science, val(gate.name), val(gate.id) + " · Requer decisão real do pesquisador", val(gate.status));
    else empty(science, "Nenhuma validação está marcada como READY. Isso não significa aprovação.");
    content.append(science);
    const progress = panel("Andamento operacional");
    if (o.completion_percent === null) empty(progress, "Sem tarefas suficientes para calcular o percentual.");
    else {
      add(progress, "div", "title", String(o.completion_percent) + "% das tarefas registradas");
      const track = add(progress, "div", "progress");
      track.setAttribute("role", "progressbar");
      track.setAttribute("aria-valuenow", String(o.completion_percent));
      track.setAttribute("aria-valuemin", "0");
      track.setAttribute("aria-valuemax", "100");
      const fill = add(track, "div");
      fill.style.width = String(Math.min(100, Math.max(0, Number(o.completion_percent)))) + "%";
    }
    add(progress, "p", "note", "Este indicador não mede qualidade, validade ou originalidade científica.");
    content.append(progress);
  } else if (tab === "tasks") {
    const box = panel("Quadro C.A.D.A. — tarefas ativas");
    if (state.mode === "MINIMAL") add(box, "p", "small muted", "O modo MINIMAL mostra a próxima ação. Para listar as tarefas, escolha ver detalhes.");
    const tasks = o.tasks ?? [];
    if (!tasks.length) empty(box, "Nenhuma lista de tarefas disponível neste modo.");
    else tasks.forEach((task: Obj) => item(box, val(task.title || task.action), val(task.id) + " · " + val(task.owner) + " · Prazo: " + val(task.deadline), val(task.status)));
    content.append(box);
  } else if (tab === "gates") {
    const box = panel("Validações humanas — não equivalem a tarefas");
    if (!s.gates?.length) empty(box, "Nenhum gate encontrado nos registros.");
    else s.gates.forEach((gate: Obj) => {
      const sourceConcern = gate.approval_with_open_source_controls === true;
      const label = sourceConcern
        ? " · aprovação registrada, mas controles das fontes apresentam problemas"
        : gate.documented_approval ? " · aprovação documentada (não é certificação científica)"
          : " · aprovação não comprovada pelos campos exigidos";
      item(box, val(gate.name), val(gate.id) + label, sourceConcern ? "Revisar fontes" : val(gate.status));
    });
    content.append(box);
  } else if (tab === "sources") {
    const metrics = add(content, "div", "grid");
    kpi(metrics, s.searches_logged, "Buscas registradas");
    kpi(metrics, s.screening_records_registered, "Registros em triagem");
    kpi(metrics, s.evidence_rows_registered, "Linhas de evidência");
    kpi(metrics, s.claims_registered, "Claims registrados");
    const quality = s.source_verification || {};
    const health = panel("Estado das verificações de fontes");
    const descriptions: Record<string, string> = {
      MISSING: "Relatório não encontrado",
      STALE: "Relatório desatualizado; os arquivos ou registros mudaram",
      BLOCKED: "Divergências objetivas impedem a aprovação",
      REVIEW_REQUIRED: "Pendências precisam de avaliação humana específica",
      REVIEWED_LIMITATIONS: "Limitações com manifestação humana registrada; fontes não estão automaticamente verificadas",
      RECORDED_CLEAR: "Checagens registradas sem pendências detectadas; interpretação científica ainda exige revisão",
    };
    add(health, "div", "title", descriptions[quality.status] || "Estado de verificação desconhecido");
    const healthMetrics = add(health, "div", "grid");
    kpi(healthMetrics, quality.checked, "Verificações realizadas");
    kpi(healthMetrics, quality.pending_review, "Pendências de revisão");
    kpi(healthMetrics, quality.blocked, "Divergências bloqueantes");
    kpi(healthMetrics, quality.reviewed_limitations, "Limitações documentadas");
    if (quality.report_missing) add(health, "p", "note", "O relatório de verificação ainda não existe.");
    else if (quality.report_stale) add(health, "p", "note", "O relatório não corresponde aos registros e arquivos atuais; é necessário gerar nova verificação.");
    if (s.gates_approved_with_source_conflicts) add(health, "p", "note", "Há aprovação humana registrada, porém os controles de fonte impedem considerá-la regular.");
    content.append(health);
    const editorial = panel("Avisos editoriais e disponibilidade");
    item(editorial, "Retratações sinalizadas", val(quality.editorial_retraction_alerts), quality.editorial_retraction_alerts ? "Revisar" : undefined);
    item(editorial, "Correções sinalizadas", val(quality.editorial_correction_alerts), quality.editorial_correction_alerts ? "Revisar" : undefined);
    item(editorial, "Atualizações editoriais sinalizadas", val(quality.editorial_updates));
    item(editorial, "Alertas de serviços bibliográficos", val(quality.provider_warnings));
    add(editorial, "p", "note", "Avisos editoriais exigem análise do contexto. Um alerta ou exceção humana não altera automaticamente o estado de uma fonte.");
    content.append(editorial);
    const box = panel("Integridade das fontes e afirmações");
    item(box, "Afirmações que requerem revisão", val(s.claims_needing_review) + " registradas com pendências de robustez ou validação");
    item(box, "Usos substantivos de IA pendentes", val(s.substantive_ai_uses_pending_review) + " registros");
    add(box, "p", "note", "Registro bibliográfico não comprova leitura integral nem sustentação semântica. [L], [I] e [P] mantêm seus critérios originais.");
    content.append(box);
  } else if (tab === "history") {
    const box = panel("Linha do tempo registrada");
    const events = state.traceability.latest_events ?? [];
    if (state.mode === "MINIMAL") empty(box, "Mude para FULL para ver os últimos eventos.");
    else if (!events.length) empty(box, "Nenhum evento encontrado.");
    else events.forEach((event: Obj) => item(box, val(event.summary), val(event.id) + " · " + val(event.when), val(event.status)));
    content.append(box);
    const sync = panel("Sincronização e armazenamento");
    item(sync, "Armazenamento declarado", val(state.project.storage_mode) + " / " + val(state.project.storage_state));
    item(sync, "Conflitos de espelhamento registrados", val(state.synchronization.conflicts_registered));
    add(sync, "p", "note", "O painel não verificou Drive ou provedores externos em tempo real.");
    content.append(sync);
  }
  const detail = add(content, "div", "meta");
  if (state.mode === "MINIMAL") {
    const btn = add(detail, "button", "", "Ver detalhes (FULL)") as HTMLButtonElement;
    btn.addEventListener("click", () => refresh("FULL"));
  } else {
    const btn = add(detail, "button", "", "Visão simples (MINIMAL)") as HTMLButtonElement;
    btn.addEventListener("click", () => refresh("MINIMAL"));
  }
}

async function refresh(mode?: "MINIMAL" | "FULL"): Promise<void> {
  if (loading) return;
  loading = true;
  ($("refresh") as HTMLButtonElement).disabled = true;
  $("notice").textContent = "Consultando os registros canônicos…";
  try {
    const result = await app.callServerTool({ name: "meu_artigo_dashboard", arguments: mode ? { mode } : {} });
    loadResult(result);
  } catch {
    $("notice").textContent = "Não foi possível atualizar. Nenhuma alteração foi realizada.";
    $("notice").className = "small error";
  } finally {
    loading = false;
    ($("refresh") as HTMLButtonElement).disabled = false;
  }
}
function loadResult(result: any): void {
  const dashboard = result?.structuredContent?.dashboard;
  if (result?.isError || !dashboard || dashboard.schema !== "meu-artigo-visual/v1") {
    $("notice").textContent = "Painel indisponível: confirme que há um projeto canônico autorizado.";
    $("notice").className = "small error";
    return;
  }
  state = dashboard;
  $("notice").textContent = "Leitura dos registros concluída · Sem alterações no projeto";
  $("notice").className = "small muted";
  render();
}
document.querySelectorAll<HTMLButtonElement>("[data-tab]").forEach(btn => {
  btn.addEventListener("click", () => {
    tab = btn.dataset.tab || "overview";
    document.querySelectorAll("[data-tab]").forEach(b => b.setAttribute("aria-selected", String(b === btn)));
    render();
  });
});
$("refresh").addEventListener("click", () => refresh(state?.mode));
app.ontoolresult = loadResult;
render();
app.connect().catch(() => {
  $("notice").textContent = "Abra este painel em um cliente compatível com MCP Apps.";
  $("notice").className = "small muted";
});
