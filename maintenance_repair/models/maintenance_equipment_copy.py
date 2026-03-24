# -*- coding: utf-8 -*-
from odoo import api, fields, models

class MaintenanceEquipmentCopy(models.Model):
    _name = 'maintenance.equipment.copy'
    _description = 'Copy Log for Equipment'
    _order = 'date desc'

    name = fields.Char(compute='_compute_equipment_log_name', store=True)
    date = fields.Date(default=fields.Date.context_today)
    value = fields.Integer('Number of Copies', aggregator="max")
    copies_added = fields.Integer('Copies Made', readonly=True, help="Number of copies made since the last log")
    equipment_id = fields.Many2one('maintenance.equipment', 'Equipment', required=True)

    @api.model_create_multi
    def create(self, vals_list):
        records = super().create(vals_list)
        records._recalculate_copies_added()
        return records

    def write(self, vals):
        res = super().write(vals)
        if 'value' in vals or 'date' in vals or 'equipment_id' in vals:
            self._recalculate_copies_added()
        return res

    def _recalculate_copies_added(self):
        for equipment in self.mapped('equipment_id'):
            logs = self.env['maintenance.equipment.copy'].search([
                ('equipment_id', '=', equipment.id)
            ], order='date asc, id asc')
            prev_val = min(logs.mapped('value')) if logs else 0
            for log in logs:
                new_added = log.value - prev_val
                if log.copies_added != new_added:
                    log.write({'copies_added': new_added})
                prev_val = log.value

    @api.depends('equipment_id', 'date')
    def _compute_equipment_log_name(self):
        for record in self:
            name = record.equipment_id.display_name
            if not name:
                name = str(record.date)
            elif record.date:
                name += ' / ' + str(record.date)
            record.name = name
