# -*- coding: utf-8 -*-

from odoo import models, fields, api

class MaintenanceEquipment(models.Model):
    _inherit = 'maintenance.equipment'

    repair_ids = fields.One2many(
        'repair.order', 'equipment_id', string='Repairs',
        help="Repair orders associated with this equipment."
    )
    repair_count = fields.Integer(
        string='Repair Count', compute='_compute_repair_count'
    )
    product_id = fields.Many2one(
        'product.product', string='Product',
        help="Product associated with this equipment."
    )
    copy_ids = fields.One2many(
        'maintenance.equipment.copy', 'equipment_id', string='Copy Logs',
        help="Copy logs associated with this equipment."
    )
    copy_count = fields.Integer(
        string='Copy Count', compute='_compute_copy_count'
    )
    copy_value = fields.Integer(
        compute='_get_copy_value', inverse='_set_copy_value', string='Last Copy Count',
        help='Latest copy count of the equipment'
    )

    def _get_copy_value(self):
        EquipmentCopy = self.env['maintenance.equipment.copy']
        for record in self:
            copy_log = EquipmentCopy.search([('equipment_id', 'in', record.ids)], limit=1, order='value desc')
            if copy_log:
                record.copy_value = copy_log.value
            else:
                record.copy_value = 0

    def _set_copy_value(self):
        for equipment in self:
            if equipment.copy_value:
                self.env['maintenance.equipment.copy'].create({
                    'value': equipment.copy_value,
                    'date': fields.Date.context_today(equipment),
                    'equipment_id': equipment.id
                })

    @api.depends('repair_ids')
    def _compute_repair_count(self):
        for equipment in self:
            equipment.repair_count = len(equipment.repair_ids)

    @api.depends('copy_ids')
    def _compute_copy_count(self):
        for equipment in self:
            equipment.copy_count = len(equipment.copy_ids)

    def action_view_copies(self):
        self.ensure_one()
        action = self.env["ir.actions.actions"]._for_xml_id("maintenance_repair.maintenance_equipment_copy_action")
        action['domain'] = [('equipment_id', '=', self.id)]
        action['context'] = {
            'default_equipment_id': self.id,
        }
        return action

    def action_view_repairs(self):
        self.ensure_one()
        action = self.env["ir.actions.actions"]._for_xml_id("repair.action_repair_order_tree")
        action['domain'] = [('equipment_id', '=', self.id)]
        action['context'] = {
            'default_equipment_id': self.id,
            'default_company_id': self.company_id.id,
        }
        return action
