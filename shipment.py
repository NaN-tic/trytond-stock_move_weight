# This file is part of the stock_move_weight module for Tryton.
# The COPYRIGHT file at the top level of this repository contains the full
# copyright notices and license terms.
from trytond.pool import PoolMeta
from trytond.model import fields

__all__ = ['Configuration']


class Configuration:
    __metaclass__ = PoolMeta
    __name__ = 'stock.configuration'
    weight_uom = fields.Many2One('product.uom', 'Default Weight Uom',
        states={
            'required': True,
            })
