from odoo import api, fields, models, _


class ContractSignatureWizard(models.TransientModel):
    _inherit = 'contract.signature.wizard'

    worksheet_signature = fields.Binary(
        string='Worksheet acceptance',
    )
    worksheet_id = fields.Many2one(comodel_name='project.project', string='Worksheet')

    name = fields.Char('Name')
    x_vendedor = fields.Char('Vendedor')
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

    is_rcs = fields.Boolean(string="RCS")
    rcs_n_floors = fields.Integer(string="Floors Number")
    rcs_surface_area = fields.Float(string="Surface Area per Floor(m2)")
    rcs_underground_zone = fields.Boolean(string="Underground Zone")
    rcs_garage = fields.Boolean(string="Garage")
    rec_pantry = fields.Boolean(string="Pantry")
    rcs_play_area = fields.Boolean(string="Play Area")
    rcs_gym = fields.Boolean(string="Gym")
    rcs_laundry = fields.Boolean(string="Laundry")
    rcs_other_underground = fields.Char(string="Other Underground Zone Spaces")
    rcs_communication_facade = fields.Boolean(string="Communicaton with the facade")

    #Tipologia de fachada
    rcs_finish_facade = fields.Selection(string="Exterior Facade Finish",
                                         selection=[('standard', 'Standard'), ('grather_than_40cm', 'Grather than 40cm')])
    #Ventanas
    rcs_n_aluminum = fields.Boolean(string="Of Aluminum")
    rcs_n_wood = fields.Boolean(string="Of Wood")
    rcs_n_pvc = fields.Boolean(string="Of PVC")
    rcs_windows_other = fields.Char(string="Others")
    #Mediciones previas
    rcs_meter_type = fields.Selection(string="Meter Type",
                                      selection=[('airthings', 'Airthings'),('radoneye','RadonEye'),('other', 'Other')])
    rcs_average_values = fields.Float(string="Average Values")
    rcs_monthly = fields.Boolean(string="Monthly")
    rcs_quarterly = fields.Boolean(string="Quarterly")
    #imágenes
    rcs_potential_environment = fields.Boolean(string="Potential Environment")
    rcs_underground_zone_img = fields.Boolean(string="Underground Zone")
    rcs_facade = fields.Boolean(string="Facade")
    rcs_observation = fields.Text(string="Observation")
    rcs_signature = fields.Binary( string='RCS acceptance')

    @api.model
    def default_get(self, fields):
        res = super(ContractSignatureWizard, self).default_get(fields)
        worksheet = self.env['project.project'].browse(self._context.get('active_id'))
        res.update({
            'worksheet_id': worksheet.id,
            'worksheet_signature': worksheet.worksheet_signature,
            'x_vendedor': worksheet.x_vendedor,
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
            'is_rcs': worksheet.is_rcs,
            'rcs_n_floors': worksheet.rcs_n_floors,
            'rcs_surface_area': worksheet.rcs_surface_area,
            'rcs_underground_zone': worksheet.rcs_underground_zone,
            'rcs_garage': worksheet.rcs_garage,
            'rec_pantry': worksheet.rec_pantry,
            'rcs_play_area': worksheet.rcs_play_area,
            'rcs_gym': worksheet.rcs_gym,
            'rcs_laundry': worksheet.rcs_laundry,
            'rcs_other_underground': worksheet.rcs_other_underground,
            'rcs_communication_facade': worksheet.rcs_communication_facade,
            'rcs_finish_facade': worksheet.rcs_finish_facade,
            'rcs_n_aluminum': worksheet.rcs_n_aluminum,
            'rcs_n_wood': worksheet.rcs_n_wood,
            'rcs_n_pvc': worksheet.rcs_n_pvc,
            'rcs_windows_other': worksheet.rcs_windows_other,
            'rcs_meter_type': worksheet.rcs_meter_type,
            'rcs_average_values': worksheet.rcs_average_values,
            'rcs_monthly': worksheet.rcs_monthly,
            'rcs_quarterly': worksheet.rcs_quarterly,
            'rcs_potential_environment': worksheet.rcs_potential_environment,
            'rcs_underground_zone_img': worksheet.rcs_underground_zone_img,
            'rcs_facade': worksheet.rcs_facade,
            'rcs_observation': worksheet.rcs_observation,
            'rcs_signature': worksheet.rcs_signature,
        })
        return res

    def action_update_contract_signature(self):
        if self.worksheet_signature and self.worksheet_id.worksheet_signature != self.worksheet_signature:
            self.worksheet_id.sudo().write({
                'worksheet_signature': self.worksheet_signature,
                'worksheet_signature_date': fields.Date.today()
            })
        if self.is_rcs and self.rcs_signature and self.worksheet_id.rcs_signature != self.rcs_signature:
            self.worksheet_id.sudo().write({
                'rcs_signature': self.rcs_signature,
                'rcs_signature_date': fields.Date.today()
            })
        return super(ContractSignatureWizard, self).action_update_contract_signature()
