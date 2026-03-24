# -*- coding: utf-8 -*-

from odoo import models, fields
from odoo.exceptions import ValidationError
from odoo.addons.maintenance_repair.models import maintenance_equipment

class RepairOrder(models.Model):
    _inherit = 'repair.order'

    maintenance_id = fields.Many2one(
        'maintenance.request', string='Maintenance Request',
        copy=False, check_company=True,
        help="Maintenance request leading to this repair."
    )
    equipment_id = fields.Many2one(
        'maintenance.equipment', string='Equipment to Repair',
        copy=False, check_company=True,
        help="Equipment associated with this repair."
    )
    copy_value = fields.Integer(
        string='Copy Value'
    )

    def action_repair_start(self):
        res = super(RepairOrder, self).action_repair_start()
        for repair in self:
            if repair.maintenance_id:
                # Find the "In Progress" stage
                # 'maintenance.stage_1' is the xml_id for In Progress from standard data
                in_progress_stage = self.env.ref('maintenance.stage_1', raise_if_not_found=False)
                if in_progress_stage:
                    repair.maintenance_id.stage_id = in_progress_stage.id
        return res

    def action_repair_end(self):
        for repair in self:
            if repair.equipment_id and repair.copy_value <= 0:
                raise ValidationError("Debe ingresar la cantidad de copias del equipo antes de finalizar la reparación.")
            
            if repair.equipment_id and repair.copy_value > 0:
                self.env['maintenance.equipment.copy'].create({
                    'value': repair.copy_value,
                    'date': fields.Date.context_today(repair),
                    'equipment_id': repair.equipment_id.id
                })

        res = super(RepairOrder, self).action_repair_end()
        for repair in self:
            if repair.maintenance_id:
                # Find the "Repaired" stage
                # 'maintenance.stage_3' is the xml_id for Repaired from standard data
                repaired_stage = self.env.ref('maintenance.stage_3', raise_if_not_found=False)
                if repaired_stage:
                    repair.maintenance_id.stage_id = repaired_stage.id
        return res
