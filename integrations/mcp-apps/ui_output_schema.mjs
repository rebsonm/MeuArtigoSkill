/**
 * Public per-call MCP output contract. This describes the already normalized
 * display-only response; no scientific verification or Drive access here.
 */
import {z} from "zod";
const nullableText=(max=120)=>z.string().max(max).nullable();
const task=z.object({
  id:z.string().min(1).max(120),
  task:nullableText(600),execution_owner:nullableText(120),
  deadline:nullableText(120)
}).strict();
const gate=z.object({
  id:z.string().regex(/^GATE-000[1-7]$/),
  approval_documented:z.boolean()
}).strict();
const scientificDiagnostic=z.object({
  schema:z.literal("MEU_ARTIGO_SCIENTIFIC_ADVISORY_PANEL_V1"),
  status:z.enum(["RECORDED_UNASSESSED","INPUTS_UNAVAILABLE"]),
  verdict:z.enum(["CORRECAO_REQUERIDA","REVISAO_CIENTIFICA_PENDENTE"]).nullable(),
  objective_blockers:z.number().int().min(0).max(1_000_000).nullable(),
  review_occurrences:z.number().int().min(0).max(1_000_000).nullable(),
  advisory_occurrences:z.number().int().min(0).max(1_000_000).nullable(),
  strict_required_occurrences:z.number().int().min(0).max(1_000_000).nullable(),
  priority_codes:z.array(z.string().regex(/^[A-Z][A-Z0-9_]{0,63}$/)).max(6),
  human_review_required:z.literal(true),
  semantic_support_proven:z.literal(false),
  scientific_quality_validated:z.literal(false),
  scientific_gate_approved:z.literal(false),
  reports_written:z.literal(false),
  drive_sync_verified:z.literal(false)
}).strict();
// No-snapshot calls are legitimate connectivity checks, never research data.
const disconnected=z.object({
  schema:z.literal("MEU_ARTIGO_SITE_V1"),
  kind:z.literal("HOST_NOT_CONNECTED"),
  locale:z.enum(["pt","en","es","fr"]),
  status:z.literal("NO_SNAPSHOT_PROVIDED"),
  project_loaded:z.literal(false),
  drive_sync_verified:z.literal(false),
  scientific_approval_verified:z.literal(false)
}).strict();

const authorized=z.object({
    schema:z.literal("MEU_ARTIGO_SITE_V1"),
    kind:z.literal("HOST_AUTHORIZED_SNAPSHOT"),
    active_route:nullableText(120),
    documented_gate_count:z.number().int().min(0).max(7),
    gate_view_partial:z.boolean(),
    registered_gate_total:z.number().int().min(0).max(7).nullable(),
    tasks:z.array(task).max(200),
    gates:z.array(gate).max(7),
    next_action:z.object({
      code:nullableText(120),
      explanation:nullableText(600),
      responsible:nullableText(120)
    }).strict(),
    scientific_diagnostic:scientificDiagnostic.nullable(),
    canonical_drive_sync_verified:z.literal(false),
    automatic_scientific_approval:z.literal(false),
    canonical_writes_allowed:z.literal(false)
  }).strict();

export const uiOutputSchema={site:z.union([disconnected,authorized])};
