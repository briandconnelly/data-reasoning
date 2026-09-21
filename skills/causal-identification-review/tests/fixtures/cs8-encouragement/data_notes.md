# Data notes

This extract is complete: it holds every customer on the list as of 2026-03-02, with no missing rows, and every field is populated.
Every customer in the extract was eligible for autopay throughout the window.
Customers could enroll in autopay with or without an invitation.
`enrolled_autopay` is enrollment status as of 2026-03-16, when the enrollment window closed: no customer enrolled in or left autopay between 2026-03-16 and the end of the outcome window.
`late_payments_prior_90d` counts late payments in the 90 days before 2026-03-02, and `late_payments_90d` counts them in the 90 days after 2026-03-16.
No record exists of who opened the email.
