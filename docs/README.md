# bctx Memory Integration Documentation

Complete blueprint for implementing CLAUDE.md pattern and memory system integration, extracted from work laptop screenshots.

---

## Start Here

New to this documentation? **Read in this order**:

1. **INDEX.md** - Overview of all documentation (you are here)
2. **MEMORY_INTEGRATION_SUMMARY.md** - High-level summary and key insights (10 min read)
3. **SYSTEM_ARCHITECTURE_DIAGRAM.md** - Visual diagrams and flow charts (15 min read)
4. **IMPLEMENTATION_GUIDE.md** - Step-by-step implementation (detailed)
5. **BLUEPRINT_CLAUDE_MD_PATTERN.md** - Complete pattern reference (comprehensive)
6. **SCREENSHOT_EXTRACTION.md** - Raw source material (reference only)

---

## Documentation Files

| File | Size | Purpose | When to Read |
|------|------|---------|--------------|
| **INDEX.md** | 14K | Navigation hub for all docs | First - overview of everything |
| **MEMORY_INTEGRATION_SUMMARY.md** | 13K | High-level overview | First - understand the big picture |
| **BLUEPRINT_CLAUDE_MD_PATTERN.md** | 16K | Complete pattern specification | Reference - detailed patterns |
| **SYSTEM_ARCHITECTURE_DIAGRAM.md** | 18K | Visual diagrams and flows | Understanding - see how it fits |
| **IMPLEMENTATION_GUIDE.md** | 20K | Step-by-step instructions | Implementing - actual work |
| **SCREENSHOT_EXTRACTION.md** | 12K | Raw text from screenshots | Reference - authoritative source |

**Total**: 93K of documentation covering complete memory integration blueprint

---

## Quick Links

### For Reading

- **[Start Reading →](INDEX.md)** - Complete documentation index
- **[Summary →](MEMORY_INTEGRATION_SUMMARY.md)** - Quick overview
- **[Diagrams →](SYSTEM_ARCHITECTURE_DIAGRAM.md)** - Visual reference

### For Implementing

- **[Implementation Guide →](IMPLEMENTATION_GUIDE.md)** - Step-by-step tasks
- **[Blueprint →](BLUEPRINT_CLAUDE_MD_PATTERN.md)** - Pattern reference
- **[Source Text →](SCREENSHOT_EXTRACTION.md)** - Original screenshots text

---

## What's Inside

### MEMORY_INTEGRATION_SUMMARY.md (13K)

High-level summary of complete extraction from work laptop screenshots.

**Key sections**:
- What was extracted (7 key elements)
- Documents created (6 files with summaries)
- Key insights (5 major patterns)
- Implementation path (immediate/short-term/medium-term)
- Critical patterns to follow
- Validation checklist
- Success metrics

**Read when**: You need a quick understanding or starting point

---

### BLUEPRINT_CLAUDE_MD_PATTERN.md (16K)

Comprehensive blueprint of CLAUDE.md pattern and memory system.

**Key sections**:
- Global CLAUDE.md structure and template
- Index.yaml pattern and schema
- Memory system organization
- Directory index pattern
- Agent orchestration rules
- Navigation instructions
- Key conventions (naming, timestamps, tags)
- Complete bay memory store example

**Read when**: You need detailed specifications for patterns

---

### SYSTEM_ARCHITECTURE_DIAGRAM.md (18K)

Visual diagrams showing complete system structure and data flows.

**Key diagrams**:
- Complete `~/.claude/` directory tree
- Bay ecosystem detail (bay-tui + bctx)
- Memory store pattern (index → entries)
- Agent discovery flow
- bctx context injection flow
- Navigator generation flow
- Cross-store references
- Tag-based discovery
- Data flow integration

**Read when**: You need to visualize how components fit together

---

### IMPLEMENTATION_GUIDE.md (20K)

Practical step-by-step implementation instructions with code examples.

**Phases covered**:
1. Create Bay Memory Store (templates provided)
2. Update Global CLAUDE.md (verification steps)
3. Implement Navigator Generation (auto-generation logic)
4. Schema Validation (validation script included)
5. Testing (manual + integration tests)
6. Documentation (README updates, installation)
7. Maintenance (auto-sync, timestamps, rebuilding)

Plus: Success criteria, troubleshooting guide

**Read when**: You're actually implementing the integration

---

### SCREENSHOT_EXTRACTION.md (12K)

Raw text extracted from work laptop screenshots for authoritative reference.

**Contents**:
- Line-by-line extraction from IMG_3495 (header, global rules)
- Line-by-line extraction from IMG_3496 (memory system)
- Line-by-line extraction from IMG_3497 (navigation, directory index)
- Key patterns extracted
- Formatting conventions
- Critical instructions
- Directory structure

**Read when**: You need exact wording from the source

---

### INDEX.md (14K)

Complete navigation hub for all documentation.

**Contents**:
- Quick start guide
- Detailed file descriptions
- Reading guide by task
- Key patterns reference
- Critical decisions documented
- Implementation phases
- Validation checklist
- Troubleshooting index

**Read when**: You need to find something specific

---

## Source Material

This documentation was extracted from three screenshots of the work laptop's `~/.claude/CLAUDE.md`:

- **IMG_3495.jpeg** - Header, global rules, navigation (lines 1-27)
- **IMG_3496.jpeg** - Memory system, directory index (lines 26-45)
- **IMG_3497.jpeg** - Project navigation, directory index (lines 32-62)

**Location**: `/Users/lasso/workspace/bctx/guidance/`

---

## Key Concepts

### Navigator Pattern

Hub-and-spoke navigation system:
- `~/.claude/CLAUDE.md` - Global navigation hub
- `~/.claude/memory/index.md` - Memory system docs
- `~/.claude/bayctx/CLAUDE.md` - bctx resource catalog (auto-generated)

### Index-First Discovery

Agents always read `index.yaml` before loading files:
```
Task → Check directory → Read index.yaml → Scan summaries → Load entries
```

### Two-Tier Memory

- **Store level** (index.yaml): Metadata + entry summaries
- **Entry level** (entries/*.yaml): Full content

### Scope-Based Context

- **Global**: Always injected (coding standards)
- **Repo-specific**: Only in that repo (API docs)

---

## Implementation Path

### Week 1: Memory Store
1. Create `~/.claude/memory/bay/` structure
2. Create index.yaml and overview.yaml
3. Update global CLAUDE.md

### Week 2-3: Navigator Generation
4. Implement `bctx sync` command
5. Auto-generate CLAUDE.md and index files
6. Add validation

### Month 1: Polish
7. Testing and documentation
8. Context budget enhancements
9. Maintenance tooling

**Detailed plan**: See IMPLEMENTATION_GUIDE.md

---

## Critical Patterns

### File Naming
- `index.yaml` (always `.yaml`, never `.yml`)
- `CLAUDE.md` (always uppercase)
- `entries/*.yaml` (always `.yaml`)

### Timestamps
```yaml
created: '2026-03-23T00:00:00.000000+00:00'
```
ISO 8601 with microseconds and timezone.

### Tags
**Store**: `project`, `ecosystem`, `<language>`, `<tool>`
**Entry**: `architecture`, `workflows`, `usecases`, `improvement`

### Summaries
```
<Component> <what it does> - <key features>
```

**Full details**: See BLUEPRINT_CLAUDE_MD_PATTERN.md

---

## Validation Checklist

Quick validation before considering integration complete:

**File Structure**
- [ ] `~/.claude/memory/bay/` exists with index.yaml
- [ ] `entries/overview.yaml` exists
- [ ] `~/.claude/bayctx/CLAUDE.md` auto-generates

**Schema**
- [ ] All files use `.yaml` extension
- [ ] Timestamps are ISO 8601
- [ ] Tags follow conventions

**Integration**
- [ ] Global CLAUDE.md includes bay
- [ ] Memory CLI works: `memory show bay`
- [ ] Agents can discover memory

**Full checklist**: See MEMORY_INTEGRATION_SUMMARY.md → "Validation Checklist"

---

## Success Metrics

Integration is complete when:

1. ✅ Memory CLI works: `memory show bay`
2. ✅ Navigator generates: `bctx sync` creates CLAUDE.md
3. ✅ Agents discover: Claude Code finds bay memory
4. ✅ Context injects: `bctx inject` respects budget
5. ✅ Validation passes: All schemas comply

**Full metrics**: See MEMORY_INTEGRATION_SUMMARY.md → "Success Metrics"

---

## Getting Started

### Step 1: Read the Summary
```bash
# Read high-level overview
cat MEMORY_INTEGRATION_SUMMARY.md
```

### Step 2: Understand the Architecture
```bash
# Review system diagrams
cat SYSTEM_ARCHITECTURE_DIAGRAM.md
```

### Step 3: Follow Implementation Guide
```bash
# Start with Phase 1
cat IMPLEMENTATION_GUIDE.md
```

### Step 4: Reference Blueprint as Needed
```bash
# Check pattern specifications
cat BLUEPRINT_CLAUDE_MD_PATTERN.md
```

---

## Troubleshooting

**Can't find what you need?**

1. Check **INDEX.md** → "Reading Guide by Task"
2. Search across all docs: `grep -r "pattern" docs/`
3. Check **SCREENSHOT_EXTRACTION.md** for original source

**Schema validation failing?**
→ See IMPLEMENTATION_GUIDE.md → "Troubleshooting"

**Navigator not generating?**
→ See IMPLEMENTATION_GUIDE.md → "Troubleshooting"

---

## Related Documentation

### Existing Memory Stores
- `~/.claude/memory/bay-tui/` - bay-tui session manager
- `~/.claude/memory/bctx/` - bctx context manager
- `~/.claude/memory/index.md` - Memory system docs

### Configuration Files
- `~/.claude/CLAUDE.md` - Global navigation hub
- `~/.claude/bayctx/config.yaml` - bctx configuration

---

## Document Stats

- **Total files**: 6 documentation files
- **Total size**: 93K
- **Total sections**: 50+ major sections
- **Diagrams**: 10+ ASCII diagrams
- **Code examples**: 30+ templates and scripts
- **Checklists**: 5+ validation and implementation checklists

---

## Next Steps

1. **Read** MEMORY_INTEGRATION_SUMMARY.md (10 min)
2. **Review** SYSTEM_ARCHITECTURE_DIAGRAM.md (15 min)
3. **Start** IMPLEMENTATION_GUIDE.md Phase 1 (hands-on)
4. **Reference** BLUEPRINT_CLAUDE_MD_PATTERN.md (as needed)
5. **Verify** against SCREENSHOT_EXTRACTION.md (when in doubt)

---

## Quick Reference

### Directory Locations
- Memory store: `~/.claude/memory/bay/`
- Navigator: `~/.claude/bayctx/CLAUDE.md`
- Type indexes: `~/.claude/bayctx/{rules,skills,agents,plugins}/index.yaml`

### Commands
- View store: `memory show bay`
- Get entry: `memory get bay overview`
- Sync navigator: `bctx sync`
- Validate: Use script in IMPLEMENTATION_GUIDE.md

### File Paths (all absolute)
- `/Users/lasso/workspace/bctx/docs/INDEX.md`
- `/Users/lasso/workspace/bctx/docs/MEMORY_INTEGRATION_SUMMARY.md`
- `/Users/lasso/workspace/bctx/docs/BLUEPRINT_CLAUDE_MD_PATTERN.md`
- `/Users/lasso/workspace/bctx/docs/SYSTEM_ARCHITECTURE_DIAGRAM.md`
- `/Users/lasso/workspace/bctx/docs/IMPLEMENTATION_GUIDE.md`
- `/Users/lasso/workspace/bctx/docs/SCREENSHOT_EXTRACTION.md`

---

**Last Updated**: 2026-05-16
**Source**: Work laptop screenshots (IMG_3495, IMG_3496, IMG_3497)
**Purpose**: Blueprint for bctx memory integration following established patterns
