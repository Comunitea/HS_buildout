from odoo import _, api, fields, models

from passlib.context import CryptContext
import binascii
import os

API_KEY_SIZE = 20 # in bytes


class ResCompany(models.Model):

    _inherit = "res.company"

    google_ads_key = fields.Char(string="Google Ads Key", required=False)

    def generate_google_ads_key(self):
        self.ensure_one()
        k = binascii.hexlify(os.urandom(API_KEY_SIZE)).decode()
        self.google_ads_key = k
