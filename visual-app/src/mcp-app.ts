import { App } from "@modelcontextprotocol/ext-apps";

/** Read-only UI: status values come exclusively from the configured project. */
type Obj = Record<string, any>;
const app = new App({ name: "Meu Artigo Visual", version: "0.1.0" });
let state: Obj | null = null;
let tab = "overview";
let loading = false;
const tabs: [string, string][] = [
  ["overview", "Visão geral"], ["stages", "Etapas"], ["tasks", "Tarefas C.A.D.A."],
  ["searches", "Fontes e buscas"], ["evidence", "Evidências [L/I/P]"],
  ["gates", "Validações"], ["history", "Rastreabilidade"],
  ["submission", "Submissão"], ["sync", "Sincronização"], ["setup", "Primeiro uso"],
];
const $ = (id: string): HTMLElement => document.getElementById(id)!;
const val = (v: unknown): string => v === null || v === undefined || v === "" ? "Indisponível" : String(v);
const explicit = (value: unknown): boolean => value === true;
function tag(kind: string, className = "", content = ""): HTMLElement {
  const n = document.createElement(kind);
  n.className = className;
  n.textContent = content;
  return n;
}
function add(parent: HTMLElement, kind: string, className = "", content = ""): HTMLElement {
  const n = tag(kind, className, content);
  parent.append(n); return n;
}
function section(parent: HTMLElement, heading: string, klass = ""): HTMLElement {
  const el = add(parent, "section", "panel " + klass);
  add(el, "h2", "", heading);
  return el;
}
function note(parent: HTMLElement, text: string): void { add(parent, "p", "note", text); }
function empty(parent: HTMLElement, text: string): void { add(parent, "div", "empty", text); }
function badge(parent: HTMLElement, text: string, type = ""): void { add(parent, "span", "badge " + type, text); }
function metric(parent: HTMLElement, label: string, number: unknown): void {
  const card = add(parent, "div", "kpi");
  add(card, "div", "number", val(number)); add(card, "div", "label", label);
}
function metrics(parent: HTMLElement): HTMLElement { return add(parent, "div", "grid"); }
function item(parent: HTMLElement, title: string, details: string, status?: string, tone = ""): void {
  const row = add(parent, "div", "item"), head = add(row, "div", "item-head");
  add(head, "strong", "", title);
  if (status) badge(head, status, tone);
  if (details) add(row, "div", "note", details);
}
function action(parent: HTMLElement, label: string, onClick: () => void, primary = false): void {
  const b = add(parent, "button", primary ? "button-primary" : "", label) as HTMLButtonElement;
  b.type = "button";
  b.addEventListener("click", onClick);
}
function navigate(next: string): void {
  if (!tabs.some(([id]) => id === next) && next !== "action") return;
  tab = next;
  document.querySelectorAll<HTMLButtonElement>("[data-tab]").forEach(b => b.setAttribute("aria-selected", String(b.dataset.tab === next)));
  render();
  $("content").focus();
}
function header(label: string, title?: string, description?: string): void {
  $("page-label").textContent = label;
  $("project-title").textContent = title || state?.project?.title || "Meu Artigo";
  $("context").textContent = description || ("Modo " + val(state?.mode) + " · Dados canônicos do projeto autorizado");
}
function overview(root: HTMLElement): void {
  const o = state!.operational, s = state!.scientific;
  header("Panorama da pesquisa");
  const grid = metrics(root);
  metric(grid, "Tarefas concluídas (registro)", o.tasks_total === null ? null : val(o.tasks_done_reported) + "/" + val(o.tasks_total));
  metric(grid, "Gates documentados", s.gates_total === null ? null : val(s.gates_approved_documented) + "/" + val(s.gates_total));
  metric(grid, "Tarefas bloqueadas", o.tasks_blocked);
  metric(grid, "Verificações de fontes", s.source_verification?.checked);
  const cols = add(root, "div", "columns");
  const next = section(cols, "Próxima ação recomendada", "highlight");
  if (o.next_action) {
    add(next, "div", "title", val(o.next_action.action));
    add(next, "div", "muted", "Responsável: " + val(o.next_action.owner) + " · Prazo: " + val(o.next_action.deadline));
    const actions = add(next, "div", "buttons");
    action(actions, "Ver próximo passo →", () => navigate("action"), true);
  } else empty(next, "Nenhuma ação executável documentada. Consulte C.A.D.A. e as pendências.");
  const science = section(cols, "Estado científico");
  if (s.next_ready_gate) item(science, val(s.next_ready_gate.name), "Requer validação humana com evidências.", val(s.next_ready_gate.status), "warning");
  else empty(science, "Nenhum gate pronto documentado; isso não implica aprovação.");
  const bars = add(science, "div", "stages");
  for (const gate of (s.gates || []).slice(0, 7)) {
    const box = add(bars, "div", "stage");
    add(box, "strong", "", val(gate.id));
    badge(box, gate.documented_approval ? "Aprovação registrada" : val(gate.status), gate.documented_approval ? "success" : "");
  }
  const foot = section(root, "O que esses números significam?");
  note(foot, "Progresso administrativo é diferente de aprovação científica. Verificações de fontes são checagens registradas, não certificação de qualidade da pesquisa.");
}
function nextAction(root: HTMLElement): void {
  header("Orientação contextual", "Uma ação de cada vez", "A interface apresenta a providência documentada; não executa nem aprova automaticamente.");
  const o = state!.operational, s = state!.scientific;
  const p = section(root, "Próxima tarefa");
  if (o.next_action) {
    add(p, "div", "title", val(o.next_action.action));
    item(p, "Registro " + val(o.next_action.id), "Responsável: " + val(o.next_action.owner) + " · Prazo: " + val(o.next_action.deadline), val(o.next_action.status));
    if (o.next_action.blocker) item(p, "Bloqueio registrado", val(o.next_action.blocker), "Pendente", "warning");
  } else empty(p, "Não há tarefa executável nos registros atuais.");
  const g = section(root, "Próxima decisão científica");
  if (s.next_ready_gate) item(g, val(s.next_ready_gate.name), "É necessária manifestação real do pesquisador, registrada pelo fluxo de gates.", "Decisão humana", "warning");
  else empty(g, "Nenhum gate está marcado como pronto.");
  note(g, "Ver uma decisão não a aprova. A validação requer ator, justificativa e evidência atribuíveis no registro canônico.");
  const actions = add(root, "div", "buttons");
  action(actions, "Conferir validações →", () => navigate("gates"), true);
  action(actions, "Ver tarefas →", () => navigate("tasks"));
}
function stages(root: HTMLElement): void {
  header("Caminho científico", "Sete decisões que realmente importam", "Etapas científicas e aprovações documentadas não dependem da porcentagem de tarefas.");
  const s = state!.scientific;
  if (!s.gates?.length) { empty(root, "Mapa indisponível: não foram encontrados os registros de gates."); return; }
  const p = section(root, "Mapa dos gates");
  const grid = add(p, "div", "stages");
  for (const gate of s.gates.slice(0, 7)) {
    const card = add(grid, "div", "stage");
    add(card, "div", "eyebrow small", val(gate.id));
    add(card, "strong", "", val(gate.name));
    badge(card, gate.documented_approval ? "Aprovação registrada" : val(gate.status), gate.documented_approval ? "success" : "warning");
    if (gate.approval_with_open_source_controls) note(card, "Controles das fontes estão pendentes.");
  }
  const actions = add(p, "div", "buttons");
  action(actions, "Examinar decisões →", () => navigate("gates"), true);
  note(root, "O mapa usa os registros existentes. Não confirma identidade do avaliador, mérito científico, revisão humana independente ou conclusão de fases ausentes.");
}
function tasks(root: HTMLElement): void {
  header("Controle de atividades", "Seu quadro C.A.D.A.", "Tarefas por estado, sem alterações no projeto.");
  const o = state!.operational;
  const stats = metrics(root);
  metric(stats, "Ativas", o.tasks_active);
  metric(stats, "Concluídas (registro)", o.tasks_done_reported);
  metric(stats, "Bloqueadas", o.tasks_blocked);
  metric(stats, "Vencidas", o.tasks_overdue);
  if (state!.mode === "MINIMAL") {
    empty(root, "A lista está oculta no modo MINIMAL. Ver detalhes para visualizar o quadro.");
    action(root, "Ver detalhes (FULL)", () => refresh("FULL"), true);
    return;
  }
  if (!o.tasks?.length) { empty(root, "Nenhuma tarefa ativa disponível."); return; }
  const grid = add(root, "div", "kanban");
  const lanes: [string, string[]][] = [
    ["A fazer", ["CAPTURED","ASSIGNED","READY"]],
    ["Em andamento", ["IN_PROGRESS","WAITING"]],
    ["Bloqueadas", ["BLOCKED"]]
  ];
  for (const [title, statuses] of lanes) {
    const lane = add(grid, "section", "lane");
    add(lane, "h3", "", title);
    const entries = o.tasks.filter((t: Obj) => statuses.includes(String(t.status).toUpperCase()));
    if (!entries.length) empty(lane, "Nenhum registro.");
    for (const t of entries) {
      const card = add(lane, "div", "task");
      add(card, "strong", "", val(t.title === "" ? t.action : t.title));
      add(card, "small", "", val(t.id) + " · " + val(t.owner));
      add(card, "small", "", " · Prazo: " + val(t.deadline));
      badge(card, val(t.status), String(t.status).toUpperCase() === "BLOCKED" ? "danger" : "");
    }
  }
}
function searches(root: HTMLElement): void {
  header("Rastreabilidade bibliográfica", "Buscas e bases científicas", "Uma consulta planejada não é uma busca executada.");
  const s = state!.scientific;
  const grid = metrics(root);
  metric(grid, "Buscas registradas", s.searches_logged);
  metric(grid, "Concluídas segundo o registro", s.searches_marked_complete_in_register);
  metric(grid, "Registros em triagem", s.screening_records_registered);
  metric(grid, "Verificações documentadas", s.source_verification?.checked);
  const p = section(root, "Estados das buscas");
  if (state!.mode === "MINIMAL") {
    empty(p, "Detalhes disponíveis no modo FULL.");
    action(p, "Ver detalhes", () => refresh("FULL"), true);
  } else if (!s.searches?.length) empty(p, "Não há buscas individualizadas nos registros.");
  else s.searches.forEach((x: Obj) =>
    item(p, val(x.source), val(x.id) + " · " + val(x.date), val(x.status), /^(PLANNED|NOT_EXECUTED)$/i.test(String(x.status)) ? "warning" : ""));
  note(p, "STATUS concluído no CSV não substitui comprovante de execução da base. O painel não consulta Scopus, WoS, Consensus ou serviços externos.");
}
function evidence(root: HTMLElement): void {
  header("Classificação epistemológica", "De onde vêm as afirmações?", "Separação [L] literatura, [I] inferência e [P] proposição original.");
  const s = state!.scientific, labels = s.epistemic_counts;
  const grid = metrics(root);
  metric(grid, "[L] Literatura", labels?.L);
  metric(grid, "[I] Inferência", labels?.I);
  metric(grid, "[P] Proposição", labels?.P);
  metric(grid, "Sem classe reconhecida", s.epistemic_unclassified);
  const quality = section(root, "Integridade das fontes");
  item(quality, "Estado do relatório", "Não é parecer científico nem verificação semântica automática.", val(s.source_verification?.status));
  const g = metrics(quality);
  metric(g, "Revisões pendentes", s.source_verification?.pending_review);
  metric(g, "Divergências bloqueantes", s.source_verification?.blocked);
  metric(g, "Correções editoriais", s.source_verification?.editorial_correction_alerts);
  metric(g, "Retratações sinalizadas", s.source_verification?.editorial_retraction_alerts);
  const p = section(root, "Afirmações e revisão");
  item(p, "Claims em revisão", val(s.claims_needing_review) + " registrados com pendências.");
  item(p, "IA substantiva sem conclusão humana", val(s.substantive_ai_uses_pending_review));
  note(p, "Os contadores usam apenas linhas rotuladas nos registros. Quantidade de [L], [I] ou [P] não prova fundamentação ou originalidade.");
}
function gates(root: HTMLElement): void {
  header("Decisão humana", "Validação humana", "Registrar aprovação exige fluxo governado fora deste painel somente leitura.");
  const s = state!.scientific;
  if (!s.gates?.length) { empty(root, "Nenhum gate disponível para exibição."); return; }
  const p = section(root, "Gates e evidências");
  s.gates.forEach((g: Obj) => {
    const summary = g.documented_approval ? "Aprovação apenas registrada; identidade não autenticada" : "Pendente ou sem comprovação suficiente";
    item(p, val(g.id) + " · " + val(g.name), summary, g.approval_with_open_source_controls ? "Conflito nas fontes" : val(g.status), g.approval_with_open_source_controls ? "danger" : g.documented_approval ? "success" : "warning");
  });
  const noteBox = section(root, "Critério de governança", "highlight");
  note(noteBox, "Este painel não aceita, rejeita nem altera decisões. O pesquisador deve revisar as evidências e registrar autorização, método, data e justificativa nos artefatos canônicos.");
}
function history(root: HTMLElement): void {
  header("Rastreabilidade", "Como o artigo evoluiu", "Registros de eventos não são prova independente de execução externa.");
  const t = state!.traceability;
  metric(metrics(root), "Eventos registrados", t.events_registered);
  const p = section(root, "Linha do tempo");
  if (state!.mode === "MINIMAL") {
    empty(p, "Detalhamento da linha do tempo disponível no modo FULL.");
    action(p, "Ver eventos", () => refresh("FULL"), true);
  } else if (!t.latest_events?.length) empty(p, "Nenhum evento registrado.");
  else {
    const line = add(p, "div", "timeline");
    t.latest_events.forEach((event: Obj) =>
      item(line, val(event.summary), val(event.id) + " · " + val(event.when), val(event.status), /UNVERIFIED|PARTIAL|FAILED/i.test(String(event.status)) ? "warning" : ""));
  }
  note(p, "TRACE-IDs exibidos preservam seu status registrado; eventos UNVERIFIED não viram CONFIRMED pela visualização.");
}
function submission(root: HTMLElement): void {
  header("Prontidão editorial", "Antes de enviar à revista", "Checklist, política editorial, anonimização e Gate 7.");
  const ed = state!.scientific.editorial || {};
  const grid = metrics(root);
  metric(grid, "Itens do checklist", ed.checklist_count);
  metric(grid, "Itens ainda não resolvidos", ed.pending_checklist_items);
  metric(grid, "Normas da revista", ed.journal_status);
  metric(grid, "Anonimização", ed.anonymization_status);
  const p = section(root, "Controles para submissão");
  item(p, "Revista-alvo", val(ed.journal_name));
  item(p, "Normas oficiais", explicit(ed.journal_official_rules_verified) ? "Verificação declarada no perfil" : "Ainda não verificadas", explicit(ed.journal_official_rules_verified) ? "Registradas" : "Pendente");
  item(p, "Gate 7", explicit(ed.gate7_approval_recorded) ? "Aprovação documentada (não autenticada)" : "Sem aprovação documentada", explicit(ed.gate7_approval_recorded) ? "Registrado" : "Pendente");
  item(p, "Prontidão parcial", explicit(ed.ready_to_submit) ? "Critérios resumidos do painel atendidos; controles completos ainda precisam de auditoria" : "Pendente — não há autorização de envio", explicit(ed.ready_to_submit) ? "Revisar" : "Bloqueada", "warning");
  note(p, "A tela não envia artigos e não substitui auditoria final de disclosure, hash dos arquivos, regras da revista ou revisão pelo autor.");
}
function sync(root: HTMLElement): void {
  header("Armazenamento e continuidade", "Os dados estão mesmo salvos?", "Drive canônico somente quando o serviço autorizado o comprova.");
  const p = state!.project, s = state!.synchronization;
  const grid = metrics(root);
  metric(grid, "Registros de espelhamento", s.external_manager_links_registered);
  metric(grid, "Conflitos registrados", s.conflicts_registered);
  metric(grid, "Snapshots locais", s.snapshots_registered);
  metric(grid, "Sincronização Drive confirmada agora", "Não verificada");
  const panel = section(root, "Status de continuidade");
  item(panel, "Modo declarado", val(p.storage_mode), val(p.storage_state));
  if (s.last_recorded_snapshot) item(panel, "Último snapshot registrado", val(s.last_recorded_snapshot.id) + " · " + val(s.last_recorded_snapshot.when), val(s.last_recorded_snapshot.status));
  else empty(panel, "Nenhum snapshot foi encontrado.");
  note(panel, "A presença de registros locais não comprova upload ao Drive. O painel não contém um adaptador de sincronização ao vivo.");
}
function setup(root: HTMLElement): void {
  header("Primeiro uso", "Vamos organizar seu artigo", "Conferência de permissões, registros e fonte canônica antes de prosseguir.");
  const o = state!.onboarding;
  const p = section(root, "Verificações de configuração");
  item(p, "Projeto canônico", o.canonical_config_present ? "Configuração local presente" : "Configuração ausente", o.canonical_config_present ? "Registrada" : "Pendente");
  item(p, "Registros disponíveis", val(o.local_registers_present) + " de " + val(o.local_registers_expected) + " arquivos esperados", "Conferir");
  item(p, "Acesso ao Drive", "Não autenticado nem sincronizado por este painel", "Não verificado", "warning");
  note(p, "Configure a conexão por um fluxo autorizado. Não há criação automática de projeto, importação, upload ou restauração de decisões antigas por esta tela.");
  const btns = add(p, "div", "buttons");
  action(btns, "Ver estado da sincronização →", () => navigate("sync"), true);
}
function render(): void {
  const root = $("content");
  root.replaceChildren();
  $("integrity-badge").textContent = state ? "LEITURA LOCAL · DRIVE NÃO VERIFICADO" : "SEM DADOS DO PROJETO";
  if (!state) {
    header("Continuidade", "Nenhum projeto carregado", "Abra com a ferramenta do projeto autorizado. Dados fictícios não serão substituídos.");
    empty(root, "Nenhuma configuração canônica foi fornecida ou a leitura falhou.");
    return;
  }
  switch (tab) {
    case "overview": overview(root); break;
    case "action": nextAction(root); break;
    case "stages": stages(root); break;
    case "tasks": tasks(root); break;
    case "searches": searches(root); break;
    case "evidence": evidence(root); break;
    case "gates": gates(root); break;
    case "history": history(root); break;
    case "submission": submission(root); break;
    case "sync": sync(root); break;
    case "setup": setup(root); break;
    default: overview(root);
  }
}
function buildNav(): void {
  for (const [id, label] of tabs) for (const container of ["sidebar", "mobile-nav"]) {
    const b = add($(container), "button", "", label) as HTMLButtonElement;
    b.type = "button";
    b.dataset.tab = id;
    b.setAttribute("aria-selected", String(id === tab));
    b.addEventListener("click", () => navigate(id));
  }
}
function loadResult(result: any): void {
  const data = result?.structuredContent?.dashboard;
  if (result?.isError || !data || data.schema !== "meu-artigo-visual/v1") {
    state = null;
    $("notice").textContent = "Nenhum dado validamente carregado. Verifique projeto autorizado e permissões; nenhuma alteração foi realizada.";
    $("notice").className = "notice error";
    render();
    return;
  }
  state = data;
  $("notice").textContent = "Leitura dos registros concluída. Armazenamento remoto não verificado.";
  $("notice").className = "notice";
  render();
}
async function refresh(mode?: "FULL" | "MINIMAL"): Promise<void> {
  if (loading) return;
  loading = true;
  ($("refresh") as HTMLButtonElement).disabled = true;
  $("notice").textContent = "Lendo os registros do projeto autorizado…";
  try {
    const result = await app.callServerTool({ name: "meu_artigo_dashboard", arguments: mode ? { mode } : {} });
    loadResult(result);
  } catch {
    state = null;
    $("notice").textContent = "Leitura indisponível; o painel anterior foi limpo para evitar dados desatualizados.";
    $("notice").className = "notice error";
    render();
  } finally {
    loading = false;
    ($("refresh") as HTMLButtonElement).disabled = false;
  }
}
buildNav();
$("refresh").addEventListener("click", () => refresh(state?.mode));
$("mode-switch").addEventListener("click", () => refresh(state?.mode === "FULL" ? "MINIMAL" : "FULL"));
app.ontoolresult = loadResult;
render();
app.connect().catch(() => {
  $("notice").textContent = "Este painel necessita de um host compatível com MCP Apps e projeto autorizado.";
  $("notice").className = "notice error";
});
