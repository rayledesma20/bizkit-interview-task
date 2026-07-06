# Notes

## Explain one fix

The double-booking bug was in `dates_overlap`, which only checked whether the **new booking's start date** fell inside an existing range. A request like Jan 5-12 could overlap an existing Jan 10-15 booking but was allowed because Jan 5 is before Jan 10. The fix uses full range overlap: `not (end_a < start_b or end_b < start_a)`.

## Show the failure

**2026-01-05 to 2026-01-12** for the Canon DSLR Camera - overlaps the existing Jan 10-15 booking; the original code wrongly allowed this.

## AI use

AI was used to review the README tasks, explain bugs, and suggest where maintenance rules needed backend enforcement. I verified each suggestion by running the Flask app, calling the API directly (e.g. overlapping dates, maintenance equipment), and checking that totals matched inclusive day-count rules before keeping any change.
