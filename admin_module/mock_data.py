# Nuevos pedidos ingresados por los clientes
new_requests = [
    {"id": 1, "product": "Producto A", "customer": "Cliente 1", "status": "Nuevo", "date": "2024-12-01"},
    {"id": 2, "product": "Producto B", "customer": "Cliente 2", "status": "Nuevo", "date": "2024-12-02"},
]

# Pedidos en curso asignados a empleados
assigned_requests = [
    {"id": 3, "product": "Producto C", "employee": "Empleado 1", "status": "En Proceso", "date": "2024-12-01"},
]

# Funciones para obtener los datos
def get_new_requests():
    return new_requests

def get_assigned_requests():
    return assigned_requests
