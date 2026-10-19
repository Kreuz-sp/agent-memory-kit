# Why files

**English** | [简体中文](../01-why.md)

## Context is not memory

A model's context window is a workbench, not a warehouse.
Close the window and the bench is cleared — the next session sees only what you paste back in.

So "it remembers me" was never a property of the model.
It is whether you put things where it can find them next time.

## Four reasons to use files

| Benefit | What it means |
|---|---|
| Readable | Open it. No tooling required. |
| Diffable | Every change is visible: who changed what. |
| Portable | Swap the model, framework, or machine — the library follows. |
| Auditable | Every entry has a source. No source, no truth. |

## When files are the wrong choice

- Tens of thousands of entries: you can't browse that anymore — you need retrieval.
- Semantic similarity ("find things like this"): you need embeddings.
- Many concurrent writers: you need a database with locking.

**Files first, retrieval later.** Most personal agents never reach "tens of thousands of entries"; starting with a vector store is usually inventing work.

## Files and vector stores

Files are the source. Vectors are a cache.

Don't reverse the order: write the files first, build an index from them when needed.
The other way around (vector store first, files written casually) has two failure modes: you edit a fact and the vector goes stale; you want to check the original and it isn't there.

## One line

**Memory + LLM = your own personal agent.** The model supplies intelligence; the library supplies acquaintance.

**Memory is not what the model remembers. It is what you put where it can find it next time.**
