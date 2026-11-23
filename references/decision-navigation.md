# Four-choice next-step guidance — native radio choices and an open response

## Purpose and trigger

When the researcher reaches a **meaningful next-step decision** (initial orientation, a methodological fork, a documented blocker, a research design trade-off, a consequential change, or a requested "next/continue"), orient the conversation toward **one currently valid decision or next action**. Ground it in the authorized, current canonical project state and the existing next-step router; do not infer completion, access or a pending scientific gate from chat history alone.

When a real choice is needed, present a concise, researcher-facing **A/B/C/D decision menu** in the researcher's conversational language. **In any host with native radio-group controls, render one actual clickable single-select radio button immediately before each option A, B, C and D**; do not substitute a decorative circle, plain alphabetical list, disabled demonstration field, checkbox or ordinary prose for interactive radio controls. Never preselect the recommendation. This is an interaction and explanation policy, not a new scientific route, scoring algorithm, register, UI installation or approval mechanism. Do not interrupt ordinary factual answers, safely authorized routine operations or simple progress reports with a contrived menu.

## Required four choices

1. **A, B, C — exactly three distinct, feasible proposals for the same pending decision.** For each give (i) a plain-language description; (ii) a concrete advantage (**Pros**); (iii) a concrete disadvantage, limitation or risk (**Cons**); and (iv) what happens next if it is chosen. Tailor these to the research question, evidence actually checked, available tools, permissions, effort and current stage. The third option is not automatically "do nothing"; it must be a genuine useful alternative, which may be a safe pause or verification step when necessary.
2. **One explicit recommendation.** Visibly mark exactly one of A/B/C as **Recommended**, explain *why* it best fits the verified context and what material trade-off remains. The recommendation is provisional advice, **never** a selection, researcher endorsement, scientific judgment, gate approval or empirical evidence. If the project or evidence is unverified, recommend an appropriate safe verification/reconciliation path, **not** an unsupported research method. Never assert an objective best method or rank unassessed catalogue cards as scientifically superior.
3. **D — Other / my own answer.** D is the **fourth radio option**, not a separate free-form choice without a selection control. When D is selected, reveal or enable its **real editable text field** directly beneath D; leave it blank for the researcher's own alternative and require meaningful text before submitting that alternative. Switching from D to A/B/C must prevent an inactive D draft from being submitted as the choice. Do not prefill the field or render it permanently disabled. If the host has radio inputs but lacks a conditional text control, retain the **D radio** and prompt the researcher to write their own answer in chat after choosing D.
4. **One-select semantics and follow-up.** Only one radio option can be selected at once, including D; **Recommended** is an explanatory badge, **not a default selection**. If the host supports a submit/continue action, it must submit the actively selected A/B/C choice or D plus its nonblank text, and never assume any option was clicked. A choice to explore/compare remains read-only until the existing governed researcher decision process is followed. Keep the language and length appropriate to MINIMAL/FULL and the actual research stage.
5. **Graceful fallback, not a fake widget.** When the host genuinely lacks native radio groups, explicitly offer `A`, `B`, `C` or `D: [researcher's own text]` as a plain-chat choice, without representing Markdown characters or static circles as live radio inputs. The Skill is instructions and does not install native UI controls. Explain this limitation without omitting the four options.

## Native presentation and honest fallback

- **Capable host:** Show a **radio-group** with four exclusive native radio inputs arranged vertically, radio on the **left**, label and pros/cons/next step beside each. Put the **recommended** indication alongside exactly one option, while the initially selected value remains empty. When D is active, display a text input/textarea immediately below it and allow the researcher to type freely.
- **Fallback host:** A plain A/B/C/D chat list is permitted **only when no functional radio widget is exposed**. Do not claim the user can click a Markdown circle, or promise that importing a Skill ZIP itself installs a widget. Conditional radio/textarea behavior is a real host-renderer responsibility.
- **Accessibility:** All radio labels and the D textarea need accessible descriptive text and keyboard-operable selection where native controls support it. Do not use color or the recommendation marker as the sole differentiation.
- **Submission:** A native Continue/Submit control is only a user-triggered step to express a proposed choice; it must not update DEC/GATE, write storage, approve an article or initiate external activity without separately satisfying governance and authorization.

## Scientific and operational safeguards

- Resolve **one** genuinely eligible pending decision using the existing continuity/router/C.A.D.A. records; these four responses are choices **about that decision**, not four independently authorized tasks or four new gates. Do not override an earlier unresolved gate, a storage-authorization blocker or existing dependencies just to show an attractive menu.
- Choosing an option to **explore or compare** is not adopting it; choosing an option in chat never **automatically** changes canonical scientific state. For a consequential research decision, obtain the researcher's own rationale and recognized limitation, and use the existing authorized DEC/GATE procedure only after the necessary explicit confirmation, provenance and review. Maintain every gate PENDING until its own actual requirements are satisfied.
- A choice involving storage fallback, publication, external sharing, manuscript submission, human subjects, permissions, purchases or sensitive data requires its own applicable explicit authorization and verification; menu selection cannot bypass those requirements.
- When only one course is permitted for scientific, ethical or access reasons, **do not invent unsafe alternatives**. Offer three distinct safe ways to address the *real* constraint (for example, verify access, inspect original records, or defer) and keep D open. If no real decision is pending, give the next step directly rather than manufacture three scientific paths.
- For a free-text D response, assess the proposed path on the same criteria (feasibility, evidence, scientific integrity and rights), explain consequences, and ask only for the additional information genuinely needed. Do not silently convert it into A/B/C.
- Record only **actual** researcher decisions and verified work in the authorized canonical workspace. If storage is unavailable or project records disagree, report that honestly; no menu, button, placeholder or draft is evidence of persistence, authentication, execution or Drive synchronization.
- Respect [automatic interaction language](language-policy.md), [scientific governance](scientific-governance.md), [canonical state](project-state.md) and [minimal/full presentation](../docs/MODO-NUCLEO-MINIMO.md).

## Illustrative researcher-facing format (translate naturally)

**Next decision:** [one grounded decision, with the current evidence or blocker]

[Native radio: unselected] **A — [approach].** Pros: [specific gain]. Cons: [specific limitation]. Next: [next valid action].

[Native radio: unselected] **B — [approach].** Pros: [specific gain]. Cons: [specific limitation]. Next: [next valid action]. **Recommended** — [contextual, bounded reason].

[Native radio: unselected] **C — [approach].** Pros: [specific gain]. Cons: [specific limitation]. Next: [next valid action].

[Native radio: unselected] **D — Other:** [a native editable text field enabled **only after D is selected**; otherwise prompt for a D chat reply].

*Choose A, B, C, or describe your own path in D. No scientific gate is approved by this menu.*

The bracketed **Native radio** lines above are descriptive placeholders in the documentation, not actual interactive widgets. On a capable host, use real radio inputs. The example is not a source of actual project options, a default recommendation for every research problem, or proof that interactive inputs are supported on a specific host.
