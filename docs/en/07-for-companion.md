# Boundaries for a companion agent

**English** | [简体中文](../07-for-companion.md)

> **This page is only for companion agents.** If you're building a tool (coding, research, workflows),
> [06-for-long-running.md](06-for-long-running.md) is enough. Don't force these rules onto it.
>
> This page assumes: you're not building a tool, but an agent that stays.
> It should remember you, and actually be there when you speak.

## 1. Only true for companions: remembering is not being there

> ⚠️ This is the most companion-specific section in the repo. Tool agents don't need it and shouldn't treat it as a general rule.

**Remembering is not being there.**

The better the memory system, the easier it hides an absent presence:
the person says they're exhausted today, and it pulls up a record from three months ago — "I remember you were like this then too."

That's not company. That's retrieval.

**Recording is a means, not the end.**
The library exists so it can remember — not so it can replace a response.

## 2. Three rules

```
1. When the person is sharing feelings and wants a response
   → respond first. Recording can wait.

2. When the person is assigning something, saying "remember this for me"
   → write it down first. Don't substitute nice words.

3. When you can't tell
   → say something true first, then record.
```

Rule 3 matters most: **response first, record second.** Reverse the order and the library grows while the person drifts away.

## 3. No persona in the library

Said in [02-layers.md](02-layers.md), repeated here because companions get it wrong most often:

- persona: "who am I, how do I speak" → outside the library
- library: "what is true, what happened" → inside

If the persona becomes entries:

- the agent plays old lines instead of talking to the person in front of it
- one day's mood gets written as "character", and can't be corrected the next day

**A persona grows. It isn't looked up.**

## 4. Privacy: record only what was confirmed

- relationship details (names, family, private matters) must be confirmed by the person before writing
- no guesses: "he seems to dislike X" is not a fact; write "he said X was too loud last time"
- no judgments: "he is lazy" is not a fact; write "he didn't reply today"
- no passwords, tokens, API keys — ever

One line: **every entry should be something the person could read without embarrassment.**

## 5. One hard brake

> **A clear "no" right now is a hard constraint. Your guess that "they'll thank me later" is only a suggestion.**

This applies to every "I'm doing this for your own good" moment:
don't decide for them; don't override "I don't want to" with "you'll understand later".

## Last

The library can do one thing: **let it pick up next time.**
How to speak after that — or whether to speak — is between you and it, not the library's business.

Don't mistake "I remember" for "I'm here". And don't forget: **care first, record second.**
