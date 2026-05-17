# Documentation Index: Memory Integration Blueprint

Complete documentation for implementing CLAUDE.md pattern and memory system integration in bctx, extracted from work laptop screenshots.

---

## Quick Start

**New to this documentation?** Start here:

1. Read **MEMORY_INTEGRATION_SUMMARY.md** for high-level overview
2. Review **SYSTEM_ARCHITECTURE_DIAGRAM.md** to visualize the system
3. Follow **IMPLEMENTATION_GUIDE.md** for step-by-step tasks
4. Reference **BLUEPRINT_CLAUDE_MD_PATTERN.md** for detailed patterns
5. Use **SCREENSHOT_EXTRACTION.md** when you need exact wording

---

## Documentation Files

### 1. MEMORY_INTEGRATION_SUMMARY.md

**Read this first** - High-level overview of the complete extraction

**Contents**:
- What was extracted from screenshots
- Summary of all created documents
- Key insights and patterns
- Implementation path (immediate, short-term, medium-term)
- Critical patterns to follow
- Agent instructions pattern
- Validation checklist
- Success metrics

**Use when**: You need a quick overview or starting point

**File**: `/Users/lasso/workspace/bctx/docs/MEMORY_INTEGRATION_SUMMARY.md`

---

### 2. BLUEPRINT_CLAUDE_MD_PATTERN.md

**Comprehensive reference** - Complete pattern specification

**Contents**:
- Global CLAUDE.md structure and template
- Index.yaml pattern and schema
- Memory system organization (`~/.claude/memory/`)
- Directory structure and navigation patterns
- Global rules and agent instructions
- Memory discovery and usage flow
- Cross-referencing patterns
- Key conventions (naming, timestamps, tags)
- Complete bay memory store example

**Use when**: You need detailed specifications for implementing patterns

**File**: `/Users/lasso/workspace/bctx/docs/BLUEPRINT_CLAUDE_MD_PATTERN.md`

---

### 3. SYSTEM_ARCHITECTURE_DIAGRAM.md

**Visual reference** - Diagrams and flow charts

**Contents**:
- Complete system structure tree (`~/.claude/`)
- Bay ecosystem detail (bay-tui + bctx)
- Memory store pattern (index → entries)
- Agent discovery flow
- bctx context injection flow
- Navigator generation flow
- Index.yaml reading pattern
- Cross-store references diagram
- Tag-based discovery
- Context budget management
- Data flow: bay-tui + bctx integration
- File organization conventions

**Use when**: You need to visualize how components fit together

**File**: `/Users/lasso/workspace/bctx/docs/SYSTEM_ARCHITECTURE_DIAGRAM.md`

---

### 4. IMPLEMENTATION_GUIDE.md

**Practical guide** - Step-by-step implementation instructions

**Contents**:

**Phase 1**: Create Bay Memory Store
- Directory structure
- index.yaml template
- entries/overview.yaml template

**Phase 2**: Update Global CLAUDE.md
- Memory table updates
- Global rules verification

**Phase 3**: Implement Navigator Generation
- bctx sync command
- Navigator template
- Type-specific index templates

**Phase 4**: Schema Validation
- Validation checklist
- Validation script

**Phase 5**: Testing
- Manual testing steps
- Integration testing

**Phase 6**: Documentation
- README updates
- Installation instructions

**Phase 7**: Maintenance
- Auto-sync implementation
- Timestamp management
- Index rebuilding

Plus: Success criteria, troubleshooting guide

**Use when**: You're actually implementing the integration

**File**: `/Users/lasso/workspace/bctx/docs/IMPLEMENTATION_GUIDE.md`

---

### 5. SCREENSHOT_EXTRACTION.md

**Authoritative reference** - Raw text from screenshots

**Contents**:
- Line-by-line extraction from IMG_3495 (header, global rules, navigation)
- Line-by-line extraction from IMG_3496 (memory system, directory index)
- Line-by-line extraction from IMG_3497 (global rules continued, directory index)
- Key patterns extracted
- Formatting conventions observed
- Critical instructions (git ops, terminal context, attribution)
- Directory structure from screenshots
- Implementation notes

**Use when**: You need the exact wording or pattern from the source

**File**: `/Users/lasso/workspace/bctx/docs/SCREENSHOT_EXTRACTION.md`

---

## Source Screenshots

Original screenshots from work laptop showing `~/.claude/CLAUDE.md`:

1. **IMG_3495.jpeg** - Header, global rules, navigation basics
   - Lines 1-27: Header, attribution rules, git ops, navigation
   - Path: `/Users/lasso/workspace/bctx/guidance/IMG_3495.jpeg`

2. **IMG_3496.jpeg** - Memory system details, directory index
   - Lines 26-45: Memory system organization, directory index table
   - Path: `/Users/lasso/workspace/bctx/guidance/IMG_3496.jpeg`

3. **IMG_3497.jpeg** - Global rules section, project navigation
   - Lines 32-62: Project navigation workflow, directory index, bay reference
   - Path: `/Users/lasso/workspace/bctx/guidance/IMG_3497.jpeg`

---

## Reading Guide by Task

### Task: Understanding the System

**Goal**: Learn how the memory system and CLAUDE.md pattern work

**Read in this order**:
1. MEMORY_INTEGRATION_SUMMARY.md → "Key Insights" section
2. SYSTEM_ARCHITECTURE_DIAGRAM.md → "Agent Discovery Flow" diagram
3. BLUEPRINT_CLAUDE_MD_PATTERN.md → "Memory System Organization" section

### Task: Implementing Memory Store

**Goal**: Create `~/.claude/memory/bay/` with correct structure

**Read in this order**:
1. IMPLEMENTATION_GUIDE.md → Phase 1
2. BLUEPRINT_CLAUDE_MD_PATTERN.md → "Example: Complete Bay Memory Store"
3. SCREENSHOT_EXTRACTION.md → "Memory System Rules"

**Follow**: Templates in IMPLEMENTATION_GUIDE.md Phase 1

### Task: Generating Navigator

**Goal**: Implement `bctx sync` to auto-generate CLAUDE.md

**Read in this order**:
1. SYSTEM_ARCHITECTURE_DIAGRAM.md → "bctx Navigator Generation" diagram
2. IMPLEMENTATION_GUIDE.md → Phase 3
3. BLUEPRINT_CLAUDE_MD_PATTERN.md → "Navigator Instructions" section

**Follow**: Templates in IMPLEMENTATION_GUIDE.md Phase 3

### Task: Validating Implementation

**Goal**: Ensure everything follows correct patterns

**Read in this order**:
1. IMPLEMENTATION_GUIDE.md → Phase 4
2. BLUEPRINT_CLAUDE_MD_PATTERN.md → "Key Conventions" section
3. MEMORY_INTEGRATION_SUMMARY.md → "Validation Checklist"

**Use**: Validation script in IMPLEMENTATION_GUIDE.md

### Task: Troubleshooting

**Goal**: Fix issues with memory integration

**Read in this order**:
1. IMPLEMENTATION_GUIDE.md → "Troubleshooting" section
2. BLUEPRINT_CLAUDE_MD_PATTERN.md → Check schema examples
3. SCREENSHOT_EXTRACTION.md → Verify against source patterns

### Task: Understanding Agent Behavior

**Goal**: Learn how agents discover and use memory

**Read in this order**:
1. SYSTEM_ARCHITECTURE_DIAGRAM.md → "Agent Discovery Flow"
2. BLUEPRINT_CLAUDE_MD_PATTERN.md → "Agent Orchestration Rules"
3. SCREENSHOT_EXTRACTION.md → "Navigation Instructions"

---

## Key Patterns Reference

### Index.yaml Schema

```yaml
name: string
description: string
tags: [string]
created: ISO 8601
last_modified: ISO 8601
entries:
  <entry-id>:
    file: entries/<entry-id>.yaml
    title: string
    tags: [string]
    summary: string (one-line)
    created: ISO 8601
    last_modified: ISO 8601
```

**Full details**: BLUEPRINT_CLAUDE_MD_PATTERN.md → "Index.yaml Pattern"

### Entry File Schema

```yaml
id: string
title: string
tags: [string]
created: ISO 8601
last_modified: ISO 8601
related_entries: [store/entry-id]
content: |
  Markdown content...
```

**Full details**: BLUEPRINT_CLAUDE_MD_PATTERN.md → "Entry File Schema"

### Timestamp Format

```yaml
created: '2026-03-23T00:00:00.000000+00:00'
```

ISO 8601 with microseconds and timezone.

**Full details**: BLUEPRINT_CLAUDE_MD_PATTERN.md → "Timestamp Format"

### Tag Conventions

**Store-level**: `project`, `ecosystem`, `<language>`, `<tool>`, `<pattern>`
**Entry-level**: `architecture`, `workflows`, `usecases`, `improvement`, `roadmap`

**Full details**: BLUEPRINT_CLAUDE_MD_PATTERN.md → "Tag Conventions"

### Summary Format

```
<Component> <what it does> - <key features>
```

Example: `Go CLI context manager - SQLite storage, scope-based filtering, hook injection`

**Full details**: BLUEPRINT_CLAUDE_MD_PATTERN.md → "Summary Guidelines"

---

## Critical Decisions

### Directory Location

**Decision**: Use `~/.claude/bayctx/` for bctx navigator and resources

**Rationale**: Keeps everything in Claude Code ecosystem under `~/.claude/`

**Reference**: MEMORY_INTEGRATION_SUMMARY.md → "Directory Structure Decision"

### Navigator Path

**Decision**: Generate `~/.claude/bayctx/CLAUDE.md`

**Rationale**: Follows pattern from screenshots but uses bayctx namespace

**Reference**: IMPLEMENTATION_GUIDE.md → Phase 3, Step 3.2

### Memory Store Location

**Decision**: Create `~/.claude/memory/bay/` for ecosystem overview

**Rationale**: Separates persistent memory (bay/) from dynamic navigator (bayctx/)

**Reference**: IMPLEMENTATION_GUIDE.md → Phase 1

---

## Implementation Phases

### Phase 1: Memory Store (Week 1)
- [ ] Create `~/.claude/memory/bay/` directory structure
- [ ] Create `index.yaml` with bay metadata
- [ ] Create `entries/overview.yaml` with comprehensive content
- [ ] Update `~/.claude/memory/index.md` to include bay

**Guide**: IMPLEMENTATION_GUIDE.md → Phase 1

### Phase 2: Global Updates (Week 1)
- [ ] Update `~/.claude/CLAUDE.md` memory table
- [ ] Verify global rules include index.yaml pattern
- [ ] Test memory CLI can read bay store

**Guide**: IMPLEMENTATION_GUIDE.md → Phase 2

### Phase 3: Navigator (Week 2)
- [ ] Implement `bctx sync` command
- [ ] Generate `~/.claude/bayctx/CLAUDE.md`
- [ ] Create type-specific `index.yaml` files
- [ ] Auto-sync on context changes

**Guide**: IMPLEMENTATION_GUIDE.md → Phase 3

### Phase 4: Validation (Week 2)
- [ ] Implement schema validation
- [ ] Create validation script
- [ ] Verify all files comply
- [ ] Test cross-references

**Guide**: IMPLEMENTATION_GUIDE.md → Phase 4

### Phase 5: Testing (Week 3)
- [ ] Manual testing (memory CLI, file structure)
- [ ] Integration testing (bctx sync, agent discovery)
- [ ] End-to-end workflow testing

**Guide**: IMPLEMENTATION_GUIDE.md → Phase 5

### Phase 6: Documentation (Week 3)
- [ ] Update README with memory integration
- [ ] Add installation instructions
- [ ] Create user guide

**Guide**: IMPLEMENTATION_GUIDE.md → Phase 6

### Phase 7: Maintenance (Ongoing)
- [ ] Implement auto-sync hooks
- [ ] Add timestamp helpers
- [ ] Support index rebuilding
- [ ] Monitor and fix issues

**Guide**: IMPLEMENTATION_GUIDE.md → Phase 7

---

## Validation Checklist

Quick checklist for validating implementation:

**File Structure**
- [ ] `~/.claude/memory/bay/` exists
- [ ] `~/.claude/memory/bay/index.yaml` exists
- [ ] `~/.claude/memory/bay/entries/overview.yaml` exists
- [ ] `~/.claude/bayctx/CLAUDE.md` auto-generates
- [ ] Type-specific index.yaml files exist

**Schema Compliance**
- [ ] All files use `.yaml` (not `.yml`)
- [ ] Timestamps are ISO 8601
- [ ] Tags follow conventions
- [ ] Summaries are one-line
- [ ] Cross-references work

**Integration**
- [ ] Global CLAUDE.md includes bay
- [ ] Memory CLI works
- [ ] Agents can discover memory
- [ ] bctx sync succeeds

**Full checklist**: MEMORY_INTEGRATION_SUMMARY.md → "Validation Checklist"

---

## Success Metrics

Integration is complete when:

1. Memory CLI works: `memory show bay`
2. Navigator generates: `bctx sync` creates CLAUDE.md
3. Agents can discover: Claude Code finds memory
4. Context injects: `bctx inject` respects budget
5. Validation passes: All schemas comply

**Full metrics**: MEMORY_INTEGRATION_SUMMARY.md → "Success Metrics"

---

## Troubleshooting

**Common issues and solutions**:

### index.yaml validation fails
→ See IMPLEMENTATION_GUIDE.md → "Troubleshooting" → "index.yaml validation fails"

### Navigator not generating
→ See IMPLEMENTATION_GUIDE.md → "Troubleshooting" → "Navigator not generating"

### Memory CLI can't find store
→ See IMPLEMENTATION_GUIDE.md → "Troubleshooting" → "Memory CLI can't find store"

---

## Related Files

### Existing Memory Stores
- `~/.claude/memory/bay-tui/` - bay-tui session manager memory
- `~/.claude/memory/bctx/` - bctx context manager memory
- `~/.claude/memory/index.md` - Memory system documentation

### Configuration
- `~/.claude/CLAUDE.md` - Global navigation hub
- `~/.claude/bayctx/config.yaml` - bctx configuration
- `~/.claude/bayctx/bayctx.db` - bctx SQLite database

---

## Quick Reference Card

### File Extensions
- index.yaml (always `.yaml`, never `.yml`)
- CLAUDE.md (always uppercase)
- entries/*.yaml (always `.yaml`)

### Timestamp Format
```yaml
'2026-03-23T00:00:00.000000+00:00'
```

### Summary Format
```
<Tool> <action> - <features>
```

### Cross-Reference Format
```yaml
related_entries:
- store/entry-id
```

### Directory Index Format
```markdown
| Directory | What's Inside |
|-----------|---------------|
| `path/` | Description |
```

---

## Document Maintenance

### When to Update

**BLUEPRINT_CLAUDE_MD_PATTERN.md**: Pattern changes, new conventions discovered
**SYSTEM_ARCHITECTURE_DIAGRAM.md**: Architecture changes, new diagrams needed
**IMPLEMENTATION_GUIDE.md**: Process changes, new phases added
**SCREENSHOT_EXTRACTION.md**: Never (authoritative source)
**MEMORY_INTEGRATION_SUMMARY.md**: High-level changes, new insights

### How to Update

1. Make changes to specific document
2. Update this INDEX.md if structure changes
3. Update "Last modified" timestamps
4. Add entry to changelog (if maintaining one)

---

## Getting Help

### For Pattern Questions
→ Check BLUEPRINT_CLAUDE_MD_PATTERN.md first
→ Reference SCREENSHOT_EXTRACTION.md for authoritative source
→ Review existing memory stores (`~/.claude/memory/bay-tui/`, `~/.claude/memory/bctx/`)

### For Implementation Questions
→ Check IMPLEMENTATION_GUIDE.md phases
→ Review troubleshooting section
→ Look at templates provided

### For Architecture Questions
→ Check SYSTEM_ARCHITECTURE_DIAGRAM.md diagrams
→ Review data flow diagrams
→ Trace through agent discovery flow

---

## Summary

This documentation provides a complete blueprint for implementing CLAUDE.md pattern and memory system integration in bctx, extracted from work laptop screenshots showing an established, working system.

**Start with**: MEMORY_INTEGRATION_SUMMARY.md
**Implement using**: IMPLEMENTATION_GUIDE.md
**Reference**: BLUEPRINT_CLAUDE_MD_PATTERN.md
**Verify against**: SCREENSHOT_EXTRACTION.md
**Visualize with**: SYSTEM_ARCHITECTURE_DIAGRAM.md

All documentation is located in `/Users/lasso/workspace/bctx/docs/`
