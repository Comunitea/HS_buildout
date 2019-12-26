from odoo import fields, models


class SaleOrder(models.Model):

    _inherit = "sale.order"

    x_discount_str = fields.Char("Info descuento")


class SaleOrderType(models.Model):

    _inherit = "sale.order.type"

    logo = fields.Binary("Logo", attachment=True)
