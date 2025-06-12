{
    'name': 'Event Scheduler',
    'version': '1.0',
    'summary': ' ',
    'sequence': 10,
    'description': """
---

### **Module 4: `event_scheduler`**

#### 📌 Purpose:

To schedule and manage events held in the co-working space, such as workshops, talks, and networking sessions.

---

### ✅ Functional Requirements:

#### 1. **Event Model**

Fields:

* Event Name (char)
* Organizer (many2one to `member_directory.member`)
* Start Datetime
* End Datetime
* Location (char)
* Description (text)
* Max Attendees (integer)
* Seats Left (computed: max − confirmed attendees)
* Status (Selection: Draft, Published, Completed, Cancelled)

SQL Constraints:

* Max Attendees > 0
* Start < End
* Unique event name on the same date

#### 2. **Event Attendee Model**

Fields:

* Event (many2one to Event)
* Member (many2one to `member_directory.member`)
* RSVP Status (Selection: Interested, Confirmed, Cancelled)
* Joined At (datetime – auto-filled if status becomes Confirmed)

SQL Constraints:

* A member cannot register more than once per event
* Confirmed count must not exceed max attendees (handled in business logic)

---

### 🔄 Behavior:

* `@api.onchange`:

  * On choosing start time, auto-suggest end time based on a default duration (e.g., +2 hours)
  * When RSVP = Confirmed → auto-fill `joined_at` if empty

* `@api.depends`:

  * Compute `seats_left` from max_attendees − confirmed attendee count

---

### 📊 Views Required:

* **Form View**: Event and attendee forms
* **List View**:

  * Events list: show name, date, location, seats left
  * Attendees list: event name, member, RSVP status
* **Kanban View**: Group events by status

---

### 🧭 Menu Structure:

```
Events
 Events
 Event Attendees
 My RSVPs (filtered by current user if applicable)
```

---
    """,
    'category': 'co working space',
    'website': 'https://www.skpec.in',
    'depends': ['base'],
    'data': [

    ],
    'demo': [

    ],
    'installable': True,
    'application': True,

    'license': 'LGPL-3',
}
