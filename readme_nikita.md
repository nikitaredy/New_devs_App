### 1 privacy leak
fix: add tenant isolation to revenue cache key

Cache key was using only property_id, allowing cross-tenant
cache hits. Ocean Rentals could see Sunset Properties data
on cache refresh.

Fix: prefix cache key with tenant_id
- Before: revenue:{property_id}
- After:  revenue:{tenant_id}:{property_id}"

### 2 Wrong Revenue Totals
"fix: enforce strict tenant context in dashboard API

getattr fallback to 'default_tenant' was silently merging
multiple clients under one tenant when auth context was missing.

Fix: raise HTTP 401 if tenant_id cannot be resolved"

### 3 — Rounding Errors
"fix: prevent float precision loss on revenue totals

Converting Decimal to float caused rounding errors e.g.
4975.50 becoming 4975.4999999. Finance team reported
discrepancies of a few cents across reports.

Fix: return total_revenue as string from Decimal directly


### 4- prop-001
fix: remove hardcoded property list from frontend dashboard

Dashboard.tsx had all 5 properties hardcoded as a static array,
showing ALL properties to ALL tenants regardless of who is logged in.
Ocean Rentals could see Sunset's properties in the dropdown and vice versa.

Root cause: PROPERTIES array in Dashboard.tsx was not fetched from the
backend — it was a static list with no tenant context at all.

Fix: identified that the dropdown needs to call GET /api/v1/properties
filtered by tenant_id from the authenticated user's token.
Flagged for full fix — requires a new backend endpoint + frontend rebuild.