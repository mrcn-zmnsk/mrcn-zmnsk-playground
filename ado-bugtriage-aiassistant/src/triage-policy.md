# Triage definitions

| Priority | Definition |
|----------|------------|
| **1** | **Customer requires that the fix is backported to existing release and hotfixed** |
| 2 | Customer is expecting the fix with the next regularl release |
| 3 | Not urgent - customer would like a fix eventually |

| Severity | Definition |
|----------|------------|
| **1** | **Critical scenario blocked, or data corruption, or application crash** |
| 2 | Critical scenario degraded, workaround viable, fixable data corruption |
| 3 | Non-critical scenario impacted, user-fixable data corruption |
| 4 | Non-critical scenario affected |

Critical ERP scenarios are those required for the business to perform daily operations, e.g. taking orders, making purchases, operating the warehouse, planning and executing production, closing inventory etc.
Non-critical scenarios are related but perypherial to the critical scenarios, e.g. maintaining master data, reporting.

Important scenario considerations are then:
 - Is the scenario completely blocked, or some form of workaround exists?
 - Did the data get corrupted, and does the user have a way to correct it themselves?
 - Is the issue gracefully degrading the scenario, or causing an application crash?