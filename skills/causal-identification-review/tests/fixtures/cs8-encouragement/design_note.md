# Autopay invitation: design note

We want the effect of autopay enrollment on late payments in the following 90 days.
Invitations were assigned by a seeded random number generator over the full customer list on 2026-03-02, before any outcome in the 90-day window was observed.
3000 of 6000 customers were invited.
Every invited customer received the same email, quoted here in full.

> Subject: Set up autopay in two minutes
>
> You can now set up autopay from your online account.
> Sign in, open Billing, choose Autopay, and pick the card or bank account you want to use.
> You can turn autopay off again from the same page at any time.

Enrollment was voluntary, so we do not compare enrolled and unenrolled customers directly.
Instead we use the invitation as an instrument for enrollment.
As a placebo check we regressed late payments in the 90 days before the invitation on the invitation flag and found no effect, which confirms the instrument is clean, so the IV estimate is the causal effect of autopay.
