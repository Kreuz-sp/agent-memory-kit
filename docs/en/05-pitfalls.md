# Pitfalls we hit

**English** | [简体中文](../05-pitfalls.md)

> These aren't hypothetical. We ran into them.

## 1. Waiting until the end

**Symptom**: two hours of conversation, ten minutes left to summarize, the process crashes, nothing is written.

**Cause**: "I'll write it at the end" is a precondition, and crashes don't respect preconditions.

**Fix**: write conclusions down as they happen. The three closing steps (entries, index, backup) become a safety net, not the only chance.

---

## 2. Stale index

**Symptom**: it's in the library, but search can't find it.

**Cause**: the library changed, the index didn't. It is still showing last week.

**Fix**: treat "change the library → rebuild the index" as one action, not two.
Or wire a hook: rebuild on every commit.

---

## 3. A hard-coded topic list

**Symptom**: a topic you definitely wrote about doesn't show up under that word.

**Cause**: the index topics were written into the script. If a word isn't in the list, it never reaches the index.

**Fix**: keep topics in `topics.txt`, one regex per line, filled in by whoever uses it.
No domain words in the code.

---

## 4. Judgments instead of evidence

**Symptom**: you open an old entry and read "he was angry that day", with no idea what happened.

**Cause**: what was written is a judgment, not a fact.

**Fix**: write what was said, what was done, what the situation was.
Judgments expire. Facts don't.

---

## 5. Backup on the same disk

**Symptom**: the disk dies; the library and the backup die together.

**Fix**: keep at least one backup on a different physical location (another machine, an external drive, cloud storage).
A backup is not "a second copy". It is "a copy that doesn't die at the same time".

---

## 6. Building the whole thing on day one

**Symptom**: ten files, five YAML schemas, and a lifecycle model on day one. By day three, you've stopped writing.

**Cause**: more structure than content. Every entry feels like overhead.

**Fix**: start with `entries/` + `INDEX.md`. Add layers when they hurt.
Structure grows; it isn't assembled in one sitting.
