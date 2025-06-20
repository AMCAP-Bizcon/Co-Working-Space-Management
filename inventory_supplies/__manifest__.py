# -*- coding: utf-8 -*-
{
    'name': 'Inventory Supplies',
    'version': '1.0',
    'summary': ' ',
    'sequence': 10,
    'description': """
---

### **Module 6: `inventory_supplies`**

#### 📌 Purpose:

To maintain a lightweight inventory system for consumables and supplies used in the co-working space (e.g., coffee, markers, toilet paper).

---

### ✅ Functional Requirements:

#### 1. **Supply Item Model**

Fields:

* Item Name (char)
* Category (Selection: Beverage, Stationery, Cleaning, Others)
* Unit of Measure (Selection: units, kg, liters, packets)
* Current Stock (computed)
* Opening Stock (integer)
* Total Purchased (integer)
* Total Consumed (integer)
* Reorder Quantity (integer)
* Reorder Needed (computed boolean: if stock ≤ reorder quantity)
* Active (boolean)

SQL Constraints:

* Opening, purchased, consumed, and reorder quantity must be ≥ 0
* Unique item name

---

#### 2. **Supply Movement Model**

Tracks inward (purchases) and outward (usage) movement of items.

Fields:

* Item (many2one to supply item)
* Movement Type (Selection: Inward, Outward)
* Quantity (integer)
* Date
* Purpose / Note (char)

SQL Constraints:

* Quantity > 0
* Must not allow consumption beyond current stock (logic level check)

---

### 🔄 Behavior:

* `@api.onchange`:

  * When item is selected, show UoM and category
  * When movement type is Outward, check against available stock

* `@api.depends`:

  * `current_stock = opening_stock + Σ(inward) − Σ(outward)`
  * `reorder_needed = current_stock ≤ reorder_qty`

---

### 📊 Views Required:

* **Form View**: Add/edit items and movements
* **List View**:

  * Items list with current stock, reorder status
  * Movements list with item, type, qty, date
* **Kanban View**: Items grouped by category (optional)

---

### 🧭 Menu Structure:

```
Supplies
 Items
 Stock Movements
 Low Stock Alerts (filtered: reorder_needed = True)
```

---

    """,
    'category': 'Co working space',
    'website': 'https://www.mkce.ac.in',
    'depends': ['base'],
    'data': [
        'views/inventory.xml',
        'security/ir.model.access.csv',
        'views/supply_movement_views.xml'
        ],
    'demo':[
    ],
    'installable': True,
    'application': True,
    'license': 'LGPL-3',
}