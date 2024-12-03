EMPLOYEE_FIELDS = [
    {"name": "kundennummer", "type": "text", "placeholder": "Kundennummer", "required": True},
    {"name": "product", "type": "text", "placeholder": "Produktname", "required": True},
    {"name": "serial_number", "type": "text", "placeholder": "Seriennummer", "required": True},
    {"name": "customer", "type": "text", "placeholder": "Kundenname", "required": True},
    {"name": "adresse", "type": "text", "placeholder": "Adresse", "required": True},
    {"name": "plz", "type": "text", "placeholder": "Postleitzahl", "required": True},
    {"name": "telefon", "type": "text", "placeholder": "Telefonnummer", "required": True},
    {"name": "email", "type": "email", "placeholder": "E-Mail-Adresse", "required": True},
    {"name": "anmeldedatum", "type": "date", "placeholder": "Anmeldedatum", "required": True},
    {"name": "issue_description", "type": "textarea", "placeholder": "Problembeschreibung", "required": True},
    {"name": "repair_cost", "type": "number", "placeholder": "Reparaturkosten (€)", "step": "0.01", "required": False},
    {"name": "status", "type": "select", "options": ["Neu", "In Arbeit", "Abgeschlossen"], "placeholder": "Status", "required": True},
    {"name": "assigned_taller", "type": "text", "placeholder": "Zugewiesener Werkstatt", "required": False}
]
