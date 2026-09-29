// chat_clock.mjs — can the December chat timestamps independently corroborate PROVEN?
// Idea: the Dec-2025 pair left a timestamped conversation. If chat times map onto each
// speaker's own commits under ONE constant offset, that is evidence of two live parties
// that does not depend on git topology at all.
// Result: NO. Best offset +248 min gives median residual 3.8 min, but shuffling the
// speaker labels gives 4.2 +/- 0.3 — the fit is indistinguishable from random labelling.
// Cause: 24 chat lines spanning 65 min are being matched onto a 13-min commit window, so
// everything lands close no matter who said it. The test has no power here.
// Kept as a negative result. Python original in the commit that added this file.
console.log("See tools/chat_clock_note.md — this route was tested and does not work.");
