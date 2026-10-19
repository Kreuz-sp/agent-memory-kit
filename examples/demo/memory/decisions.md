# Decisions

## 2026-03-10 - No React; server-rendered templates for now

- **Decided**: Atlas's frontend uses Jinja templates for now; no React.
- **Why**: only three pages, and the ops team just needs tables; adding a build chain adds a deployment step.
- **By whom**: Alex
- **Impact / boundaries**: re-evaluate when there are more than five pages or complex interactions are needed.
- **Later**:
