from flask import url_for

routes_map = {
    # Rutas Compartidas
    'shared_index': lambda: url_for('shared.index'),
    'shared_login': lambda: url_for('shared.login'),
    'shared_logout': lambda: url_for('shared.logout'),

    # Rutas de Administración
    'admin_manage_employees': lambda: url_for('admin.manage_employees'),
    'admin_add_employee': lambda: url_for('admin.add_employee'),
    'admin_edit_employee': lambda employee_id: url_for('admin.edit_employee', employee_id=employee_id),
    'admin_delete_employee': lambda employee_id: url_for('admin.delete_employee', employee_id=employee_id),

    # Rutas de Clientes
    'client_consulta': lambda: url_for('client.consulta'),
    'client_register_rma': lambda: url_for('client.register_rma'),

    # Rutas de Empleados
    'employee_dashboard': lambda: url_for('employee.employee_dashboard'),
    'employee_new_requests': lambda: url_for('employee.new_requests'),
    'employee_edit_data': lambda rma_id: url_for('employee.edit_data', rma_id=rma_id),
    'employee_update_status': lambda: url_for('employee.update_status'),
    'employee_generate_report': lambda: url_for('employee.generate_report'),
    'create_report': lambda rma_id: url_for('employee.create_report', rma_id=rma_id),
    'view_reports': lambda rma_id: url_for('employee.view_reports', rma_id=rma_id),

    # Rutas de RMA
    'rma_submit_rma': lambda: url_for('rma.submit_rma'),
    'rma_new_rma': lambda: url_for('rma.new_rma'),
}
