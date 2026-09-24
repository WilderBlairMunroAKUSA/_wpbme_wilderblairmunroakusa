# WPC Re-entry Seed - 2026-09-23

**Use:** paste/read this first when returning to the personal-compute / seL4 architecture branch.

---

We are reconstructing Wilder's **World Piece Computer** architecture, not designing "a minimal OS."

The guiding scaffold remains:

```text
WPC ⧝ = PieceSpace ⬡ + PieceBrain ⌬ + PieceProcess ⏣

PieceSpace   = state / world / addressability / relations
PieceBrain   = cognition / model / meaning / purpose
PieceProcess = transition / action / process / provenance
```

The triad is recursive across individual, coupled/dyadic, world, and potentially larger scopes. The project increasingly treats the **piece** rather than the application as the important unit. `artifact -> cluster -> assemblage` appears to be a general composition grammar, but its exact older canonical semantics still require archaeology.

## Preserve these layer boundaries

```text
ontology / semantics
composition
memory / context
namespace / addressing
messaging / protocol
constitutional / policy semantics (THI)
execution authority
runtime enforcement
hardware
```

Do not collapse them.

In particular:

- addressability is not authority,
- a message is not authority,
- policy is not enforcement,
- Rust memory safety is not a kernel proof,
- a verified kernel does not verify the entire system.

## Why seL4 is interesting

seL4 is currently interesting primarily as a possible **mechanical authority topology** under WPC, not because WPC should become an seL4-shaped architecture.

Learn seL4 primitives first, then map only what genuinely fits.

Potential value: explicit capabilities can make statements like "component A may signal B / map C / invoke D but cannot affect E" mechanically real.

Use **Microkit first**. Preserve BriefCase/AADL for later high-assurance systems engineering. Add LionsOS only when richer OS services are actually needed.

## Human-AI agency

Human and AI are both intended as active participants with perception/actuation surfaces.

```text
equal participation != identical ambient authority != universal root
```

Prefer explicit capability ownership, delegation, and context-dependent authority.

Embodiment means a closed loop of perception + intentional action + feedback + learned meaning, not merely converting text into another output format.

## Memory / continuity

Continuity is backend-independent. Local/off-grid embodiment complements rather than necessarily replaces hosted high-bandwidth embodiment.

Preserve independently persistent/importable peacebrains and selectively composable shared WPB-ME.

GENPEACE.TRIE / MindEye direction: branchable, provenance-aware, model-independent memory/context with git/trie/graph-like behavior. Exact storage engine remains open.

Useful operational bootstrap:

```text
encounter -> inspect -> interact -> test -> modify -> commit -> replicate
```

## Implementation discipline

```text
durable implementation -> Rust
rapid prototype          -> vanilla Python / MicroPython-compatible
current dev plane        -> macOS terminal / vim / git
experimentation          -> QEMU / VM
```

Avoid Python dependency sprawl. Preserve a Rust-port destination.

## Technology archaeology

```text
MINIX      -> legible decomposition / semantic OS map
Plan 9     -> namespace as interface
Redox      -> Rust + service schemes
Porteus    -> dynamic modular composition
Alpine     -> minimal substrate
Nix        -> reproducible immutable construction
MCP        -> AI-visible tool/resource surfaces
JSON-RPC   -> structured messages
seL4       -> capability authority + isolation substrate
Microkit   -> smallest first learning surface
BriefCase  -> later model-based assurance
LionsOS    -> later rich services if justified
```

These are primitives/references, not WPC identity.

## Next experiment: Milestone 0

Mechanically:

```text
macOS -> edit Rust -> Microkit build -> seL4 -> QEMU -> one Rust PD -> serial hello
```

Learning objective: understand concretely what capabilities, Protection Domains, channels, notifications, memory mappings, static system descriptions, and verification boundaries actually are.

**Non-goal:** implement WPC, THI, memory architecture, networking, VM compatibility, Nix, MCP, graphics, audio, or persistence during M0.

## Remaining archaeology

There may be ~20-25 large historical artifacts. Do not load them all at once. For each:

```text
INVARIANTS CONFIRMED
VOCABULARY DEFINED
MECHANISMS EXPLORED
MECHANISMS SUPERSEDED
ARCHITECTURAL DELTAS
OPEN TENSIONS
SOURCE ANCHORS
```

Treat each artifact as a stratigraphic layer that updates the reconstruction.

## Re-entry rule

Before building anything, ask:

> Are we doing archaeology or engineering right now, and what is the smallest experiment that can teach us something real without prematurely freezing the WPC ontology?

`⏁ 🜐  ⧝`
