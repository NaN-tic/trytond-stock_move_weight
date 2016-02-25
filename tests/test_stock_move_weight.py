# This file is part of the stock_move_weight module for Tryton.
# The COPYRIGHT file at the top level of this repository contains the full
# copyright notices and license terms.
from trytond.tests.test_tryton import ModuleTestCase
from trytond.tests.test_tryton import suite as test_suite
import unittest


class StockMoveWeighTestCase(ModuleTestCase):
    'Test Stock Move Weigh module'
    module = 'stock_move_weight'


def suite():
    suite = test_suite()
    suite.addTests(unittest.TestLoader().loadTestsFromTestCase(
            StockMoveWeighTestCase))
    return suite
