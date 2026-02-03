# Billing commands

`zpcli billing` — View account balance, transaction history, and aggregated summary; redeem credit codes (e.g. beta invite); or start a payment flow to add credits. Use these commands to understand what you’re charged for (storage, time-of-use) and to manage your balance.

**Authentication:** JWT or PAT. Billing endpoints require the `billing` scope if you use a PAT. See [Authentication](../../../../docs/authentication.md#scopes). For **claim**, you must be authenticated with **JWT** (username/password), not a PAT.

## Commands

- `zpcli billing balance` — Show current account balance in USD.
- `zpcli billing ledger` — Show billing transaction history with optional date range and limit.
- `zpcli billing summary` — Show aggregated billing summary for a period (storage charges, time-of-use charges, credits, totals).
- `zpcli billing claim <code>` — Redeem a credit code (beta invite, promotional credits, etc.). Requires JWT.
- `zpcli billing start <amount>` — Start a payment session to add credits (opens a URL to complete payment). Minimum amount $1.

---

## balance

```text
zpcli billing balance [--json]
```

Shows your current account balance in USD. Use this to confirm your balance before creating or modifying zpools.

**Output**

- **Default:** A single line: `Current Balance: $X.XX` (formatted with up to 6 decimal places as needed; trailing zeros are omitted).
- If balance information is unavailable, the CLI prints: *Balance information unavailable.*

**Options**

- `--json` — Output raw JSON instead of the formatted line.

**Examples**

```text
zpcli billing balance
zpcli billing balance --json
```

---

## ledger

```text
zpcli billing ledger [OPTIONS]
```

Shows billing transaction history: each row is a single transaction (credit add, storage charge, time-of-use charge, etc.). Entries are ordered **newest first**. Use this to audit what changed your balance and when.

**Options**

- `--limit <n>` — Maximum number of entries to return. Omit for the default limit.
- `--since <YYYY-MM-DD>` — Only include events that **occurred** on or after this date (inclusive). Filters by **event** time, not posted time.
- `--until <YYYY-MM-DD>` — Only include events that **occurred** on or before this date (inclusive). Filters by **event** time.
- `--json` — Output raw JSON instead of the table.
- `--local` — Show timestamps in local timezone instead of UTC.

**Date format:** Both `--since` and `--until` must be `YYYY-MM-DD`. Invalid format causes the CLI to report an error and exit.

**Output columns**

- **Event** — When the event occurred (e.g. when the charge was incurred).
- **Posted** — When the transaction was recorded in the ledger.
- **Event Type** — Type of transaction (e.g. credit, storage charge, time-of-use).
- **Source** — Source or category of the transaction.
- **Amount (USD)** — Amount in dollars: positive (e.g. `+$10.00`) for credits, negative (e.g. `-$0.05`) for charges. Formatted with trailing zeros stripped.
- **Note** — Optional note or description.

If there are no transactions in the range (or no transactions at all), the CLI prints *No transactions found.*

**Examples**

```text
zpcli billing ledger
zpcli billing ledger --limit 50
zpcli billing ledger --since 2025-01-01 --until 2025-01-31
zpcli billing ledger --since 2025-06-01 --local --json
```

---

## summary

```text
zpcli billing summary [OPTIONS]
```

Shows an **aggregated** billing summary for a date range: storage charges grouped by zpool and rate period, time-of-use charges (e.g. scrub jobs, egress), credits applied, and totals. Use this to see *what* you’re being charged for and how it adds up, rather than a raw list of transactions.

**Options**

- `--since <YYYY-MM-DD>` — Start of the period. Omit for “all time” .
- `--until <YYYY-MM-DD>` — End of the period. Omit for “present” .
- `--json` — Output raw JSON instead of the formatted tables and totals.
- `--local` — Show timestamps in local timezone instead of UTC.

**Date format:** `--since` and `--until` must be `YYYY-MM-DD`. Invalid format causes the CLI to report an error.

**Output structure**

1. **Period** — Header showing the date range (e.g. *Billing Summary (2025-01-01 to 2025-01-31)*).

2. **Storage Charges** (if any) — Table of storage charges by zpool and period:
   - **Zpool ID** — The zpool these charges apply to.
   - **Type** — Volume type (e.g. gp3, sc1).
   - **Size** — Size in GB (see [Storage units](../../../../docs/reference/storage-units.md) for GiB elsewhere).
   - **Hourly Rate** — Rate per hour in USD.
   - **Daily Rate** — Rate per day in USD.
   - **Hours** — Number of hours in this period.
   - **Total** — Total charge for this row in USD.
   - **Period** — Date range for this row (from → to).

3. **Time-of-Use Charges** (if any) — Table of one-off or usage-based charges (e.g. scrub jobs, egress):
   - **Time** — When the charge was posted.
   - **Source** — Source of the charge.
   - **Zpool ID** — Zpool this charge relates to (if applicable).
   - **Amount** — Charge in USD.
   - **Note** — Optional note.

4. **Credits** (if any) — Table of credits applied (e.g. from claim codes):
   - **Time** — When the credit was posted.
   - **Source** — Source of the credit.
   - **Amount** — Credit amount in USD (shown as positive).
   - **Note** — Optional note.

5. **Totals** — Summary lines:
   - **Storage Charges** — Total storage charges (shown as negative).
   - **Time-of-Use Charges** — Total time-of-use charges (negative).
   - **Credits Applied** — Total credits (positive).
   - **Period Net** — Net change over the period (USD).
   - **Ending Balance** — Balance at end of period (USD).

6. **Note** — Optional footer message (e.g. disclaimers or timing of balance updates).

If summary information is unavailable, the CLI prints *Summary information unavailable.*

**Examples**

```text
zpcli billing summary
zpcli billing summary --since 2025-01-01 --until 2025-01-31
zpcli billing summary --since 2025-06-01 --local --json
```

---

## claim

```text
zpcli billing claim <code> [--json]
```

Redeems a **credit code** (e.g. beta invite code, promotional credits). The code is applied to your account and your balance increases by the code’s value. Each code is typically one-time use.

**Authentication:** You must be authenticated with **JWT** (username/password). PAT authentication is not accepted for claim; use interactive login or `ZPOOL_USER` / `ZPOOL_PASSWORD` in the environment.

**Argument**

- **code** — The credit code to redeem (exact string as provided, e.g. from email or invite).

**Options**

- `--json` — Output raw JSON instead of the formatted success message.

**Success output**

On success (non-JSON), the CLI prints:

- A success message.
- **Added:** The amount added in USD (e.g. `Added: $10.00`).

The new balance is not shown; run `zpcli billing balance` to see your updated balance.

If the code is invalid, already used, or expired, the CLI reports an error.

**Examples**

```text
zpcli billing claim MY-BETA-CODE-123
zpcli billing claim MY-BETA-CODE-123 --json
```

---

## start

```text
zpcli billing start <amount> [--json]
```

Starts a **payment session** to add credits to your account. The CLI prints a **payment URL**; open it in a browser to complete payment (e.g. card or other methods offered by the provider). Used for onboarding or when you want to add funds.

**Argument**

- **amount** — Amount in **dollars** (integer) to add. **Minimum: $1.** If amount is less than 1, the CLI prints *Amount must be at least $1* and exits.

**Options**

- `--json` — Output raw JSON instead of the formatted message and URL.

**Success output**

On success (non-JSON), the CLI prints:

- A success message.
- *Please visit this URL to complete payment:*
- The **payment URL** (clickable in terminals that support links).

Open the URL in a browser and complete the payment flow; your balance will be updated after payment succeeds.

**Examples**

```text
zpcli billing start 10
zpcli billing start 25 --json
```

---

## See also

- [Command reference](commands.md)
- [Authentication](../../../../docs/authentication.md#scopes) — JWT vs PAT, billing scope, non-interactive use
- [Storage units](../../../../docs/reference/storage-units.md) — GiB vs GB; summary may show sizes in GB; zpool sizes elsewhere use GiB
