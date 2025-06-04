# Co-Working-Space-Management

### Project Idea: **Co-Working Space Management Suite**

A lightweight yet complete solution for running an independent co-working hub.
It is broken into **10 self-contained custom modules** that together cover the day-to-day operations.
Every single module can be built **using only**:

* Custom models & fields (incl. many2one / one2many)
* Model inheritance
* List, Form & Kanban views
* Menus + server actions
* `@api.onchange` methods
* `@api.depends` compute methods
* SQL constraints (`_sql_constraints`)

---

| #  | Module (technical name) | Purpose & Scope                                                      | Where the required concepts naturally show up                                                                                                                                          |
| -- | ----------------------- | -------------------------------------------------------------------- | -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| 1  | **member\_directory**   | Central person register (members, walk-ins, staff).                  | • Onchange: When `member_type` changes, default individual/company fields.<br>• Compute: Age from DOB, membership status from related subscription.<br>• SQL: Unique email per member. |
| 2  | **membership\_plan**    | Catalog of recurring plans (daily, weekly, monthly) + subscriptions. | • Onchange: Auto-fill price & duration when plan chosen.<br>• Compute: Next-billing date.<br>• SQL: Duration > 0, price ≥ 0.                                                           |
| 3  | **space\_booking**      | Reserve desks, meeting rooms or booths by time slot.                 | • Onchange: Filter available resources by date chosen.<br>• Compute: Booking duration (hours) & subtotal.<br>• SQL: Prevent overlapping bookings on same resource.                     |
| 4  | **event\_scheduler**    | Internal / public events calendar (workshops, meet-ups).             | • Onchange: Suggest end-time = start + default duration.<br>• Compute: Seats left (capacity − confirmed attendees).<br>• SQL: Start < End, unique name per day.                        |
| 5  | **maintenance\_ticket** | Report & track facility issues (AC fault, chair broken).             | • Onchange: When `priority` set to “High” auto-assign SLA date.<br>• Compute: Resolution time (hours)<br>• SQL: One open ticket per asset at a time.                                   |
| 6  | **inventory\_supplies** | Simple stock list for coffee beans, stationery, cleaning items.      | • Onchange: UoM change adjusts reorder qty.<br>• Compute: Current stock = opening + purchases − usage.<br>• SQL: Positive reorder qty.                                                 |
| 7  | **simple\_billing**     | Draft invoices for bookings, plans, events. (No account moves.)      | • Onchange: When client picked, pull outstanding bookings.<br>• Compute: Total = Σ line subtotals.<br>• SQL: One draft invoice per customer per day.                                   |
| 8  | **feedback\_review**    | Collect star ratings & comments from members after services.         | • Onchange: If rating ≤ 2 prompt for mandatory comment.<br>• Compute: Average rating per service/provider.<br>• SQL: Rating between 1–5 integer.                                       |
| 9  | **partner\_discount**   | Manage partner companies & discount codes.                           | • Onchange: Auto-set expiry = today + plan.duration.<br>• Compute: Times redeemed.<br>• SQL: Unique active code.                                                                       |
| 10 | **asset\_tracker**      | Log movable assets (chairs, monitors, routers) & assignments.        | • Onchange: When member picked, set state → “in-use”.<br>• Compute: Usage\_days since last assignment.<br>• SQL: Serial number unique & not null.                                      |

---

#### How the suite hangs together

* **Loose coupling** – each module has its own models but relates to others through many2one (e.g., bookings → members, invoices → bookings).
* **Progressive learning** – you can build them in order; every module adds just a bit more depth to the same concept set.
* **No advanced extras** – wizards, security groups, web controllers, reports, REST, etc., are deliberately left out so that **only** the items in your prerequisites list are needed.

#### Suggested development order

1. `member_directory` → foundation for relations
2. `membership_plan` → introduce computed dates
3. `space_booking` → practise overlapping-slot SQL constraint
4. `simple_billing` → pull data across modules
5. Add the remaining modules in any order; they repeat the same patterns with new business logic.

---

This project gives you **10 real-world mini-apps** that exercise *exactly* the skills you listed—nothing more, nothing less—while still ending up with a coherent, useful product you could demo or extend later.
