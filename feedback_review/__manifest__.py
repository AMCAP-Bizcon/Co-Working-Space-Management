# -*- coding: utf-8 -*-

{
    'name': 'Feedback Review',
    'version': '1.0',
    'summary': ' ',
    'sequence': 10,
    'description': """
---

### **Module 8: `feedback_review`**

#### 📌 Purpose:

To collect and analyze feedback from members regarding bookings, events, or services through star ratings and comments.

---

### ✅ Functional Requirements:

#### 1. **Feedback Model**

Fields:

* Member (many2one to `member_directory.member`)
* Feedback Type (Selection: Booking, Event, Service)
* Related Record (many2one – generic; could be limited to bookings, events, or services based on type)
* Rating (integer: 1 to 5 stars)
* Comment (text)
* Submitted On (datetime)
* Staff Response (text)
* Status (Selection: New, Reviewed, Closed)

SQL Constraints:

* Rating must be an integer between 1 and 5
* One feedback per member per related record (e.g., only one review per event)

---

### 🔄 Behavior:

* `@api.onchange`:

  * If Rating ≤ 2, make `Comment` required (client-side logic or field validation)
  * When Feedback Type is chosen, filter the Related Record dropdown accordingly

* `@api.depends`:

  * Compute average rating per service, event, or booking item (aggregated in related models if extended)

---

### 📊 Views Required:

* **Form View**: Create/edit feedback
* **List View**: Show feedback with rating, type, date, and status
* **Kanban View**: Group feedback cards by status (e.g., New, Reviewed)

---

### 🧭 Menu Structure:

```
Feedback
├── All Feedback
├── My Feedback (filtered by current user)
└── Low Ratings (filtered where rating ≤ 2)
```

---
    """,
    'category': 'co working space',
    'website': 'https://www.mkce.ac.in',
    'depends': ['base'],
    'data': [

    ],
    'demo': [

    ],
    'installable': True,
    'application': True,

    'license': 'LGPL-3',
}
