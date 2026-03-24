# -*- coding: utf-8 -*-

from odoo import models, fields, api

class MaintenanceRequest(models.Model):
    _inherit = 'maintenance.request'

    repair_ids = fields.One2many(
        'repair.order', 'maintenance_id', string='Repairs',
        help="Repair orders associated with this maintenance request."
    )
    repair_count = fields.Integer(
        string='Repair Count', compute='_compute_repair_count'
    )
    copy_count = fields.Integer(
        related='equipment_id.copy_value', string='Copy Count', readonly=True
    )

    @api.depends('repair_ids')
    def _compute_repair_count(self):
        for request in self:
            request.repair_count = len(request.repair_ids)

    def action_view_repairs(self):
        self.ensure_one()
        action = self.env["ir.actions.actions"]._for_xml_id("repair.action_repair_order_tree")
        action['domain'] = [('maintenance_id', '=', self.id)]
        action['context'] = {
            'default_maintenance_id': self.id,
            'default_equipment_id': self.equipment_id.id if self.equipment_id else False,
            'default_company_id': self.company_id.id,
        }
        return action

    def action_create_repair_order(self):
        self.ensure_one()
        return {
            'type': 'ir.actions.act_window',
            'name': 'Create Repair Order',
            'res_model': 'repair.order',
            'view_mode': 'form',
            'target': 'current',
            'context': {
                'default_maintenance_id': self.id,
                'default_equipment_id': self.equipment_id.id if self.equipment_id else False,
                'default_product_id': self.equipment_id.product_id.id if self.equipment_id and getattr(self.equipment_id, 'product_id', False) else False,
                'default_company_id': self.company_id.id,
                'default_partner_id': self.equipment_id.owner_user_id.partner_id.id if self.equipment_id and getattr(self.equipment_id, 'owner_user_id', False) else False,
            }
        }
