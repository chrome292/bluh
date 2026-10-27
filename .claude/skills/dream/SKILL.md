---
name: dream
description: Out-of-band memory review. Reads recent sessions, finds repeated mistakes and stale memory, and drafts changes for a human to approve. Run weekly, or when the agent keeps making the same mistake.
---
# Dream

A batch review of memory, done outside any working session: like a head teacher reading every
student's work to fix the curriculum, rather than one student taking notes mid-exam.

1. Collect: `python3 scripts/collect_transcripts.py --days 7` (pass a different `--days` if the user asked).
   If it reports 0 digests, stop and say there's nothing to review.
2. Split the digests in `.dream/inbox/` into batches of about 10 and run one `dream-analyst`
   subagent per batch, in parallel. Give each one its file list.
3. Merge their findings. Keep a pattern only if it showed up in **at least 2 sessions**, or if it's
   a single factual error in memory that's clearly wrong.
4. Write `memory/proposals/<YYYY-MM-DD>.md` (via `scripts/memwrite.py write ... --expect new`).
   Write one section per proposed change, containing:
   - **Change:** add / edit / delete, the target file, and the exact new text
   - **Why:** the pattern, with prevalence ("seen in 4 of 12 sessions")
   - **Evidence:** the session IDs and quoted lines
   - **Decision:** `[ ] accept  [ ] reject`, left for the human
5. Also suggest deletions: memory nothing used, or memory the sessions contradict.
6. Don't apply any change yourself. Tell the user where the proposal file is and give a summary
   of each change in one line. After they tick boxes, apply only the accepted ones (with
   `memwrite.py`; changes to `org/` are for the human to make by hand).
