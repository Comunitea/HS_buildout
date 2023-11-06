from odoo import api, fields, models, _

class WorksheetSignatureWizard(models.TransientModel):
    _name='worksheet.signature.wizard'
    _description = 'Worksheet Signature Wizard'

    worksheet_signature = fields.Binary(
        string='Worksheet acceptance',
    )
    worksheet_id = fields.Many2one(comodel_name='project.project', string='Worksheet')

    name = fields.Char('Name')
    x_vendedor = fields.Char('Vendedor')
    worksheet_img = fields.Binary(string="Worksheet Image", attachment=True)
    has_radiators = fields.Boolean(string="Radiators")
    radiators_qty = fields.Integer(string="Radiators Quantity")
    has_toilet = fields.Boolean(string="Toilet")
    toilet_qty = fields.Integer(string="Toilets Quantity")
    has_fixed_furnitures = fields.Boolean(string="Fixed Furnitures")
    fixed_furnitures_qty = fields.Integer(string="Fixed Furnitures Quantity")
    has_plasterboard = fields.Boolean(string="Plasterboard")
    plasterboard_qty = fields.Integer(string="Plasterboard Quantity")
    has_boiler = fields.Boolean(string="Boiler")
    boiler_qty = fields.Integer(string="Booiler Quantity")
    worksheet_other = fields.Char(string="Other")
    has_baseboard = fields.Boolean(string="Baseboard")
    baseboard_qty = fields.Integer(string="Baseboard Quantity")
    basboard_type = fields.Char(string="Type")
    worksheet_wall_thickness = fields.Float(string="Wall Thickness")
    worksheet_wall_type = fields.Char(string="Type")
    exceptional_conditions = fields.Text(string="Exceptional Conditions")
    partner_id = fields.Many2one(comodel_name='res.partner', string='Customer')

    @api.model
    def default_get(self, fields):
        res = super(WorksheetSignatureWizard, self).default_get(fields)
        worksheet = self.env['project.project'].browse(self._context.get('active_id'))
        res.update({
            'worksheet_id': worksheet.id,
            'worksheet_signature': worksheet.worksheet_signature,
            'x_vendedor': worksheet.x_vendedor,
            'worksheet_img': worksheet.worksheet_img,
            'has_radiators': worksheet.has_radiators,
            'radiators_qty': worksheet.radiators_qty,
            'has_toilet': worksheet.has_toilet,
            'toilet_qty': worksheet.toilet_qty,
            'has_fixed_furnitures': worksheet.has_fixed_furnitures,
            'fixed_furnitures_qty': worksheet.fixed_furnitures_qty,
            'has_plasterboard': worksheet.has_plasterboard,
            'plasterboard_qty': worksheet.plasterboard_qty,
            'has_boiler': worksheet.has_boiler,
            'boiler_qty': worksheet.boiler_qty,
            'worksheet_other': worksheet.worksheet_other,
            'has_baseboard': worksheet.has_baseboard,
            'baseboard_qty': worksheet.baseboard_qty,
            'basboard_type': worksheet.basboard_type,
            'worksheet_wall_thickness': worksheet.worksheet_wall_thickness,
            'worksheet_wall_type': worksheet.worksheet_wall_type,
            'exceptional_conditions': worksheet.exceptional_conditions,
            'partner_id': worksheet.partner_id.id,
        })
        return res

    def action_update_worksheet_signature(self):
        if self.worksheet_signature and self.worksheet_id.worksheet_signature != self.worksheet_signature:
            self.worksheet_id.write({
                'worksheet_signature': self.worksheet_signature,
                'worksheet_signature_date': fields.Date.today()
            })
        return True
