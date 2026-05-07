## Bug Fixes — Property Revenue Dashboard

**Loom:** https://www.loom.com/share/e3699a7a32a94e0ea9d3154add6841e8

---

### Bug 1 — Cache key had no tenant isolation
`backend/app/services/cache.py`

Cache was keyed on property_id only. Two tenants querying the 
same property_id would share cached results — Ocean could see 
Sunset's revenue on refresh.

Before: `revenue:{property_id}`  
After: `revenue:{tenant_id}:{property_id}`

---

### Bug 2 — Silent tenant fallback returning wrong data
`backend/app/api/v1/dashboard.py` + `backend/app/services/reservations.py`

dashboard.py had a getattr fallback to "default_tenant" when 
auth context was missing — no error, just wrong data silently.

Also found: when the DB pool fails, reservations.py falls back 
to hardcoded mock_data keyed only by property_id. No tenant 
check at all — any tenant gets the same numbers.

Fix: raise 401 if tenant_id is missing. Mock fallback flagged 
for removal.

---

### Bug 3 — Float precision dropping cents
`backend/app/api/v1/dashboard.py`

Decimal was being cast to float before returning. Caused values 
like 4975.50 to come back as 4975.4999999. Finance team noticed 
the discrepancy.

Fix: return the Decimal as string directly, skip the float cast.

---

### Bug 4 — Property dropdown hardcoded, no tenant filtering
`frontend/src/components/Dashboard.tsx`

PROPERTIES array was static — all 5 properties from both tenants 
hardcoded in the frontend. Ocean could select and query Sunset's 
properties directly.

Not fully fixed — needs a new GET /api/v1/properties endpoint 
filtered by tenant_id and frontend to fetch on mount instead 
of using a static list. Flagged for next sprint.