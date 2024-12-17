EMPLOYEE_FIELDS = [
    {"name": "kundennummer", "label": "Kundennummer", "type": "text", "required": True},
    {"name": "artikel", "label": "Artikel", "type": "text", "required": True},
    {"name": "modell", "label": "Modell", "type": "text", "required": True},  # NUEVO CAMPO
    {"name": "seriennummer", "label": "Seriennummer", "type": "text", "required": True},
    {"name": "fehlerangabe_kunde", "label": "Fehlerbeschreibung Kunde", "type": "textarea", "required": True},
    {"name": "vergeben_am", "label": "Vergeben am", "type": "date", "required": False},  # NUEVO CAMPO
    {"name": "trackingnummer", "label": "Trackingnummer", "type": "text", "required": False},
    {"name": "abgeschlossen_am", "label": "Abgeschlossen am", "type": "date", "required": False},
    {"name": "reparaturmassnahme", "label": "Reparaturmaßnahme", "type": "textarea", "required": True},
    {"name": "e_teile_nummer", "label": "E-Teile Nummer", "type": "text", "required": False},
    {"name": "reparaturkosten", "label": "Reparaturkosten (€)", "type": "number", "step": "0.01", "required": False},  # NUEVO CAMPO
    {"name": "kommentar", "label": "Kommentar", "type": "textarea", "required": False},
]
