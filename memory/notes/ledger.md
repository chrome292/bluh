# Ledger

Append-only. Newest at the bottom. Every attempt gets an entry *before* any summary to the user.

Format:

    ## YYYY-MM-DD: <short title>
    - Tried: <what was attempted>
    - Verdict: WORKS | TRADE-OFF | DEAD END
    - Why: <evidence: command output, test result, link>
    - Skeptic: <what the skeptic tried, and whether it broke>
    - Don't retry unless: <the new information that would justify another attempt>
