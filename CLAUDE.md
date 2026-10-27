# Working in this repo

## Memory protocol
@memory/MEMORY.md

1. **Read first.** Before starting a task, grep `memory/` for the topic. Check `memory/notes/ledger.md`
   so you don't repeat an attempt that's already marked DEAD END.
2. **Write last.** Before you summarize anything to the user, log what you tried in the ledger:
   `python3 scripts/memwrite.py append memory/notes/ledger.md --by <you> --why "<one line>"`
3. **Never edit memory files directly.** Use `scripts/memwrite.py`. For a full rewrite, run `hash`
   first, then `write --expect <hash>`. If it reports `conflict`, someone else changed the file:
   re-read it and redo your edit.
4. **`memory/org/` is human-only.** If you think it's wrong, write a proposal in `memory/proposals/`.
5. **`memory/scratch/`** is your own working space for the session. Write there freely; it isn't committed.
6. **Keep notes short.** Write one fact per bullet, include the evidence, and don't record anything
   you could re-derive from the code in seconds.

## Team rules
- The agent that produced a result never grades it. Send it to the `skeptic` subagent.
- Every attempt ends with exactly one verdict: **WORKS**, **TRADE-OFF** or **DEAD END**.
  A clean-looking result with no evidence counts as a DEAD END.
- A DEAD END is a result, not a failure. Log it, and don't retry it unless you have the
  new information its ledger entry asks for.
- Give each subagent one job. `worker` does, `skeptic` attacks, `librarian` searches memory.

## Learning between sessions
Run `/dream` every so often (weekly works). It reviews recent sessions, finds repeated mistakes,
and drafts memory changes for a human to accept or reject.
