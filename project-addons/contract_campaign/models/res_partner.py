# -*- coding: utf-8 -*-
from odoo import models


class ResPartner(models.Model):

    _name = "res.partner"
    _inherit = ['res.partner', 'utm.mixin']
