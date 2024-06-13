from odoo import models, fields, api, _
from odoo.exceptions import ValidationError
from PyPDF2 import PdfFileMerger, PdfFileReader, PdfFileWriter
import tempfile
import subprocess
import os
import base64

class ProjectProject(models.Model):

    _inherit = 'project.project'

    project_ref = fields.Char(string="Ref", readonly=False, copy=False)


    pure_silent = fields.Boolean(string="PureSilent")
    pure_silent_attic = fields.Boolean(string="PureSilent Attic")

    #CONFIGURACIÓN DE VIVIENDA

    n_floors = fields.Integer(string="Floors Number")
    surface_area = fields.Float(string="Surface Area per Floor(m2)")
    n_bedrooms = fields.Integer(string="Bedrooms Number")
    independent_kitchen = fields.Boolean(string="Independent Kitchen")

    other_spaces = fields.Char(string="Other Spaces conneceted to the house")
    n_occupants = fields.Integer(string="Number of Occupants")
    pets = fields.Integer(string="Pets")
    #BAÑOS?
    n_bathrooms = fields.Integer(string="Bathrooms Number")
    with_windows = fields.Boolean(string="With Windows")
    with_extractor = fields.Boolean(string="With Extractor")
    with_shunt = fields.Boolean(string="With Shunt(static ventilation)")

    #ZONA DE SECADO
    drying_area = fields.Boolean(string="Clothes Drying Area")
    inside = fields.Boolean(string="Inside")
    outside = fields.Boolean(string="Outside")
    closed_terrace = fields.Boolean(string="Closed Terrace")
    others = fields.Boolean(string="Others")

    #TIPOLOGÍA DE FACHADA
    finish_facade = fields.Char(string="Exterior Finish Facade")
    normal_wall_thickness = fields.Float(string="Normal Wall Thickness")
    wall_thickness = fields.Float(string="Wall Thickness > 40cm")

    #VENTANAS

    n_aluminum = fields.Boolean(string="Of Aluminum")
    n_wood = fields.Boolean(string="Of Wood")
    n_pvc = fields.Boolean(string="Of PVC")
    n_with_shutter_box = fields.Boolean(string="With Shutter Box")
    n_with_shutter = fields.Boolean(string="With Shutter")
    n_sliding_type = fields.Boolean(string="Sliding Type")
    n_tilt_and_turn_type = fields.Boolean(string="Tilt and Turn Type")
    n_casement_type = fields.Boolean(string="Casement Type")
    n_with_termal_break = fields.Boolean(string="With Termal Break")
    other_windows= fields.Boolean(string="Others")

    #TIPO DE CALEFACCIÓN
    water_radiators = fields.Boolean(string="Water Radiators")
    electric_radiators = fields.Boolean(string="Electric Radiators")
    wood_pellet_fireplace = fields.Boolean(string="Wood Fireplace")
    heat_pump = fields.Boolean(string="Heat Pump")
    stoves = fields.Boolean(string="Stoves")

    #Patologías

    #MOHO
    molds = fields.Boolean(string="Molds?")
    mold_living_room = fields.Boolean(string="Living Room")
    mold_bedroom = fields.Boolean(string="Bedrooms")
    mold_bathroom = fields.Boolean(string="Bathroom/s")
    mold_kitchen = fields.Boolean(string="Kitchen")
    mold_other = fields.Char(string="Others")

    #VAHOS EN VENTANAS
    steam_windows = fields.Boolean(string="Steam in Windows?")
    steam_living_room = fields.Boolean(string="Living Room")
    steam_bedroom = fields.Boolean(string="Bedrooms")
    steam_bathroom = fields.Boolean(string="Bathroom/s")
    steam_kitchen = fields.Boolean(string="Kitchen")
    steam_other = fields.Char(string="Others")

    musty_smell = fields.Boolean(string="Musty Smell?")
    humidity_in_enviroment = fields.Boolean(string="Humidity in Enviroment?")

    #EN CASO DE PURESILET ÁTICO

    independent_attic = fields.Boolean(string="Independent Attic?")
    with_access = fields.Boolean(string="With Access?")
    without_access = fields.Boolean(string="Without Access?")
    has_ventilation = fields.Boolean(string="Has outside air intake / ventilation")
    current_usage = fields.Char(string="Current Usage")

    observation = fields.Text(string="Observation")

    #Hoja de obra
    worksheet_img = fields.Binary(string="Work Sheet Image", attachment=True, copy=False)
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
    worksheet_signature = fields.Binary(
        string='Worksheet acceptance', copy=False
    )
    worksheet_signature_date = fields.Date(string="Work Sheet Signature Date", copy=False)

    contract_type_id = fields.Many2one(comodel_name='project.contract.type', string="Contract Type", required=True, copy=False)
    contracted_distance = fields.Float(string="Contracted Distance(m)")

    #RADÓN
    #Configuracion de vivienda
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

    rcs_signature = fields.Binary( string='RCS acceptance', copy=False)

    rcs_signature_date = fields.Date(string="RCS Signature Date", copy=False)

    is_rcs = fields.Boolean(string="Is RCS?" , compute='_compute_is_rcs')

    with_guarantee = fields.Boolean(string="With Guarantee")

    guarantee_type = fields.Selection(string="Guarantee Type",
                                      selection=[('cap', 'CAP'), ('misc_deck', 'MISC Deck'), ('enc', 'ENC'),('misc_facade','MISC Facade'),('misc_terrace','MISC Terrace'),('ps','PS')])
    guarantee_start_date = fields.Date(string="Guarantee Start Date")

    manual_contract = fields.Boolean(string="Manual Contract")

    @api.depends('contract_type_id')
    def _compute_is_rcs(self):
        for record in self:
            if record.contract_type_id.contract_type == 'rcs':
                record.is_rcs = True
            else:
                record.is_rcs = False

    @api.onchange('with_guarantee')
    def _onchange_with_guarantee(self):
        for record in self:
            if not record.with_guarantee:
                record.guarantee_type = ''
                record.guarantee_start_date = False

    @api.model
    def create(self, vals):
        if not vals.get('manual_contract',False) and  vals.get('contract_type_id', False):
            contract_type = self.env['project.contract.type'].browse(vals['contract_type_id'])
            vals['project_ref'] = self._change_project_ref(contract_type)
            vals['name'] = self._change_project_name(vals['project_ref'], vals.get('name', False))
        project = super(ProjectProject, self).create(vals)
        if project.worksheet_signature:
            values = {'worksheet_signature': project.worksheet_signature}
            project._track_signature(vals, 'worksheet_signature')
        if project.rcs_signature:
            values = {'rcs_signature': project.rcs_signature}
            project._track_signature(vals, 'rcs_signature')
        return project

    @api.multi
    def write(self, values):
        self._track_signature(values, 'worksheet_signature')
        self._track_signature(values, 'rcs_signature')
        res = super(ProjectProject, self).write(values)
        if values.get('contract_type_id', False) and not values.get('manual_contract', False):
            contract_type = self.env['project.contract.type'].browse(values['contract_type_id'])
            for project in self.filtered(lambda x: not x.manual_contract):
                vals={}
                vals['project_ref'] = self._change_project_ref(contract_type)
                vals['name'] = self._change_project_name(vals['project_ref'], project.name)
                project.write(vals)
        return res

    def _change_project_ref(self, contract_type):
        if not contract_type:
            return False
        project_ref = '/'
        if contract_type.contract_type == 'mps':
            project_ref = self.env['ir.sequence'].next_by_code('project.project.mps')
        elif contract_type.contract_type == 'ps':
            project_ref = self.env['ir.sequence'].next_by_code('project.project.ps')
        elif contract_type.contract_type == 'misc':
            project_ref = self.env['ir.sequence'].next_by_code('project.project.misc')
        elif contract_type.contract_type == 'enc':
            project_ref = self.env['ir.sequence'].next_by_code('project.project.enc')
        elif contract_type.contract_type == 'cap':
            project_ref = self.env['ir.sequence'].next_by_code('project.project.cap')
        elif contract_type.contract_type == 'rcs':
            project_ref = self.env['ir.sequence'].next_by_code('project.project.rcs')
        return project_ref

    def _change_project_name(self,project_ref, name):
        if not project_ref or project_ref == '/':
            return name
        if not name:
            return project_ref
        split_name = name.split(' - ')
        if len(split_name) > 1:
            split_name[0] = project_ref
            return ' - '.join(split_name)
        else:
            return project_ref + ' - ' + name

    def action_show_worksheet_signatures(self):
        return {'type': 'ir.actions.act_window',
                'name': ('Worksheet Signatures'),
                'res_model': 'worksheet.signature.wizard',
                'target': 'new',
                'view_id': self.env.ref('hs_custom_documents.view_worksheet_signature_wzd').id,
                'view_mode': 'form',
                }

    @api.onchange('has_radiators')
    def _onchange_has_radiators(self):
        for record in self:
            if not record.has_radiators:
                record.radiators_qty = 0

    @api.onchange('has_toilet')
    def _onchange_has_toilet(self):
        for record in self:
            if not record.has_toilet:
                record.toilet_qty = 0

    @api.onchange('has_fixed_furnitures')
    def _onchange_has_fixed_furnitures(self):
        for record in self:
            if not record.has_fixed_furnitures:
                record.fixed_furnitures_qty = 0

    @api.onchange('has_plasterboard')
    def _onchange_has_plasterboard(self):
        for record in self:
            if not record.has_plasterboard:
                record.plasterboard_qty = 0

    @api.onchange('has_boiler')
    def _onchange_has_boiler(self):
        for record in self:
            if not record.has_boiler:
                record.boiler_qty = 0

    @api.onchange('has_baseboard')
    def _onchange_has_baseboard(self):
        for record in self:
            if not record.has_baseboard:
                record.baseboard_qty = 0
                record.basboard_type = ''


    def action_print_contract(self):
        for project in self:
            return {
                'type': 'ir.actions.act_url',
                'url': '/project/report/'+str(project.id),
                'target': 'new',
            }


    @api.multi
    def action_contract_send(self):
        res = super(ProjectProject, self).action_contract_send()
        context = res['context']
        data = self.generate_project_report()
        attachments = []
        if data:
            pdf = data['pdf']
            filename = data['filename']
            contract = self.sudo().env['ir.attachment'].create({
                'name': filename,
                'type': 'binary',
                'datas': pdf,
                'res_model': 'project.project',
                'res_id': self.id,
                'mimetype': 'application/pdf',
            })
            attachments.append(contract.id)
        if self.x_iva_doc:
            report = self.env['ir.actions.report']._get_report_from_name('hs_custom_documents.reduced_iva_report')
            doc = report.render_qweb_pdf([self.id])[0]
            att_doc = self.sudo().env['ir.attachment'].create({
                'name': 'HG-IVA.pdf',
                'type': 'binary',
                'datas': base64.b64encode(doc),
                'res_model': 'project.project',
                'res_id': self.id,
                'mimetype': 'application/pdf',
            })
            attachments.append(att_doc.id)
        if self.is_rcs and self.rcs_signature:
            report = self.env['ir.actions.report']._get_report_from_name('hs_custom_documents.report_work_data_sheet_rcs')
            doc = report.render_qweb_pdf([self.id])[0]
            att_doc = self.sudo().env['ir.attachment'].create({
                'name': 'RCS-WorkDataSheet.pdf',
                'type': 'binary',
                'datas': base64.b64encode(doc),
                'res_model': 'project.project',
                'res_id': self.id,
                'mimetype': 'application/pdf',
            })
            attachments.append(rcs_worksheet.id)
        if self.worksheet_signature:
            report = self.env['ir.actions.report']._get_report_from_name('hs_custom_documents.worksheet_report')
            doc = report.render_qweb_pdf([self.id])[0]
            att_doc = self.sudo().env['ir.attachment'].create({
                'name': 'WorkSheet.pdf',
                'type': 'binary',
                'datas': base64.b64encode(doc),
                'res_model': 'project.project',
                'res_id': self.id,
                'mimetype': 'application/pdf',
            })
            attachments.append(att_doc.id)
        if self.contract_type_id and self.contract_type_id.contract_type == 'ps':
            report = self.env['ir.actions.report']._get_report_from_name('hs_custom_documents.report_work_data_sheet')
            doc = report.render_qweb_pdf([self.id])[0]
            att_doc = self.sudo().env['ir.attachment'].create({
                'name': 'WorkDataSheet.pdf',
                'type': 'binary',
                'datas': base64.b64encode(doc),
                'res_model': 'project.project',
                'res_id': self.id,
                'mimetype': 'application/pdf',
            })
            attachments.append(att_doc.id)
        context.update({
            'default_attachment_ids': [(6, 0, attachments)],
        })
        res['context'] = context
        return res


    def generate_project_report(self):
        self.ensure_one()
        report_name = ''
        if self and self.contract_type_id:
            if self.contract_type_id.contract_type == 'mps':
                report_name = 'hs_custom_documents.mant_puresilent_contract_report'
            elif self.contract_type_id.contract_type == 'ps':
                report_name = 'hs_custom_documents.puresilent_contract_report'
            elif self.contract_type_id.contract_type == 'misc':
                report_name = 'hs_custom_documents.misc_contract_report'
            elif self.contract_type_id.contract_type == 'enc':
                report_name = 'hs_custom_documents.enc_contract_report'
            elif self.contract_type_id.contract_type == 'cap':
                report_name = 'hs_custom_documents.cap_contract_report'
            elif self.contract_type_id.contract_type == 'rcs':
                report_name = 'hs_custom_documents.radon_contract_report'
            else:
                return False

            report = self.env['ir.actions.report']._get_report_from_name(report_name)
            report_output = report.render_qweb_pdf([self.id])[0]
            if self.contract_type_id.contract_conditions:
                pdf = self.pdf_merge([base64.b64encode(report_output), self.contract_type_id.contract_conditions])
            else:
                pdf = base64.b64encode(report_output)
            filename = report.print_report_name.replace("'","")+'-'+self.name
            return {'filename': filename, 'pdf': pdf}
        else:
            return False



    def pdf_merge(self, documents_pdf):
        temp_file = tempfile.NamedTemporaryFile()
        temp_file_name = temp_file.name
        merger = PdfFileMerger()
        rutas=[]
        for document_pdf in documents_pdf:
            ft = tempfile.NamedTemporaryFile()
            nft = ft.name
            fo = open(nft, "wb")
            fo.write(base64.b64decode(document_pdf))
            fo.close()
            fo = open(nft, "rb")
            merger.append(fo)
            rutas.append(fo)

        merger.write(temp_file_name)
        merger.close()
        for ruta in rutas:
            ruta.close()

        pdf = open(temp_file_name,'rb')
        result = base64.b64encode(pdf.read())
        pdf.close()
        return result




class ProjectContractType(models.Model):

    _name = 'project.contract.type'
    _description = 'Project Contract Type'

    name = fields.Char(string="Name", required=True)
    active = fields.Boolean(string="Active", default=True)
    contract_type = fields.Selection(
        string='Contract Type',
        selection=[('mps', 'MPS'),
                   ('ps', 'PS'),
                   ('misc','MISC'),
                   ('enc','ENC'),
                   ('cap','CAP'),
                   ('rcs', 'RCS')],
        required=True
    )
    contract_conditions = fields.Binary(string="Contract Conditions", attachment=True)
