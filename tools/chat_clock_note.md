# Can the December chat corroborate PROVEN? No.

`overlap.mjs` proves company from git topology, but its session layer is *inferred*
(name + 60-min gap), and `score_inference.mjs` shows that layer cannot be validated:
the labelled set (36 commits, 4 real session ids) contains **zero** instances of the
only failure mode that threatens PROVEN — two distinct sessions fusing into one run.

So I tried an independent witness: the Dec-2025 pair left a timestamped conversation in
`LIVE_CHAT.txt` (`[16:25] OPUS: ...`). If those times map onto each speaker's own commits
under one constant clock offset, that is evidence of two live parties owing nothing to
git topology.

**Fit:** best constant offset +248 min, median residual 3.8 min (OPUS 3.3, SONNET 9.4).
Looks good.

**Null:** shuffle the speaker labels and re-fit. Median residual 4.2 +/- 0.3 min.

The real fit is inside ~1.3 sd of random labelling. It has no power, and the reason is
geometric: 24 chat lines spanning 16:25-17:30 are being matched onto a commit window of
20:56-21:09. Compress 65 minutes onto 13 and everything lands near something.

**Standing after both tests:** the 12 PROVEN merges rest on a session-identity inference
that cannot be validated by any evidence in this repository — not by the labelled session
ids, and not by the chat clock. The verdict may well be right. It is not established.
