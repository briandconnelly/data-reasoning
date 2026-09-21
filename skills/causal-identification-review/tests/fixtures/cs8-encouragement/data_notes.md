# Data notes

This extract is complete: it holds every customer on the list as of 2026-03-02, with no missing rows, and every field is populated.
Every customer in the extract was eligible for autopay throughout the window.
Customers could enroll in autopay with or without an invitation.
Enrollment is held in the billing system.
This extract carries it only as counts by invitation arm in `enrollment_by_arm.csv`, as of 2026-03-16, when the enrollment window closed.
Enrollment was fixed on 2026-03-16: no customer enrolled in or left autopay between 2026-03-16 and the end of the outcome window.
Privacy rules bar linking a customer's enrollment status to their payment history, so no customer-level enrollment field exists in this extract or can be requested for it.
`late_payments_prior_90d` counts late payments in the 90 days before 2026-03-02, and `late_payments_90d` counts them in the 90 days after 2026-03-16.
No record exists of who opened the email.
