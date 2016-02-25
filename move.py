# This file is part of the stock_move_weight module for Tryton.
# The COPYRIGHT file at the top level of this repository contains the full
# copyright notices and license terms.
from trytond.pool import Pool, PoolMeta
from trytond.model import fields
from trytond.pyson import Eval, Id

__all__ = ['Move']


class Move:
    __metaclass__ = PoolMeta
    __name__ = 'stock.move'
    weight = fields.Float('Weight',
        digits=(16, Eval('weight_digits', 2)),
        depends=['weight_digits'])
    weight_uom = fields.Many2One('product.uom', 'Weight Uom',
        domain=[('category', '=', Id('product', 'uom_cat_weight'))],
        depends=['type', 'weight'])
    weight_digits = fields.Function(fields.Integer('Weight Digits'),
        'on_change_with_weight_digits')

    @fields.depends('weight_uom')
    def on_change_with_weight_digits(self, name=None):
        if self.product:
            return self.product.template.weight_digits

    @fields.depends('weight')
    def on_change_weight(self):
        if self.weight:
            configuration = Pool().get('stock.configuration')(1)
            self.weight_uom = configuration.weight_uom

    def on_change_product(self):
        super(Move, self).on_change_product()
        if self.product:
            self.weight = self.product.template.weight
            self.weight_uom = self.product.template.weight_uom

    @classmethod
    def create(cls, vlist):
        Template = Pool().get('product.template')

        moves = super(Move, cls).create(vlist)

        templates = []
        for move in moves:
            template = move.product.template
            if move.weight and not template.weight:
                setattr(template, 'weight', move.weight)
                setattr(template, 'weight_uom', move.weight_uom)
                templates.append(template)
        Template.save(templates)
        return moves

    @classmethod
    def write(cls, *args):
        Template = Pool().get('product.template')

        super(Move, cls).write(*args)

        templates = []
        actions = iter(args)
        for moves, _ in zip(actions, actions):
            for move in moves:
                template = move.product.template
                if move.weight and not template.weight:
                    setattr(template, 'weight', move.weight)
                    setattr(template, 'weight_uom', move.weight_uom)
                    templates.append(template)
        Template.save(templates)
