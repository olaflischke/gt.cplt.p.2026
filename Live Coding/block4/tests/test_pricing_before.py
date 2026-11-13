"""Charakterisierungstests fuer das "Vorher"-Beispiel.

Diese Tests dokumentieren das bestehende Verhalten, bevor refaktoriert wird.
"""

import copy
import unittest

from block4.before.pricing_before import calc


class PricingBeforeCharacterizationTests(unittest.TestCase):
    def test_simple_order_without_discount(self):
        order = {"items": [{"qty": 2, "price": 1000}], "code": None, "customer": "C-1"}
        self.assertEqual(2499.0, calc(order))

    def test_save10_discount(self):
        order = {"items": [{"qty": 2, "price": 1000}], "code": "SAVE10", "customer": "C-1"}
        self.assertEqual(2299.0, calc(order))

    def test_vip20_discount_requires_vip_prefix(self):
        order = {"items": [{"qty": 1, "price": 1000}], "code": "VIP20", "customer": "VIP-7"}
        self.assertEqual(1299.0, calc(order))

    def test_negative_price_item_is_ignored(self):
        order = {"items": [{"qty": 1, "price": -500}], "code": None, "customer": "C-1"}
        self.assertEqual(499.0, calc(order))

    def test_nonpositive_quantities_are_ignored(self):
        for qty in (0, -2):
            with self.subTest(qty=qty):
                order = {"items": [{"qty": qty, "price": 1000}], "code": None}
                result = calc(order)
                self.assertEqual(499, result)
                self.assertIs(type(result), int)

    def test_nonpositive_quantity_does_not_require_price(self):
        order = {"items": [{"qty": 0}], "code": None}
        self.assertEqual(499, calc(order))

    def test_zero_price_item_adds_nothing(self):
        order = {"items": [{"qty": 3, "price": 0}], "code": None}
        result = calc(order)
        self.assertEqual(499, result)
        self.assertIs(type(result), int)

    def test_vip20_without_vip_prefix_does_not_discount(self):
        order = {"items": [{"qty": 1, "price": 1000}], "code": "VIP20", "customer": "C-1"}
        self.assertEqual(1499, calc(order))

    def test_vip20_without_customer_does_not_discount(self):
        order = {"items": [{"qty": 1, "price": 1000}], "code": "VIP20"}
        self.assertEqual(1499, calc(order))

    def test_missing_and_unknown_codes_do_not_discount(self):
        orders = (
            {"items": [{"qty": 1, "price": 1000}]},
            {"items": [{"qty": 1, "price": 1000}], "code": "UNKNOWN"},
        )
        for order in orders:
            with self.subTest(code=order.get("code")):
                self.assertEqual(1499, calc(order))

    def test_multiple_items_are_summed(self):
        order = {
            "items": [
                {"qty": 1, "price": 1000},
                {"qty": 2, "price": 1500},
            ],
            "code": None,
        }
        self.assertEqual(4499, calc(order))

    def test_surcharge_threshold_below_at_and_above_boundary(self):
        cases = ((4999, 5498), (5000, 5000), (5001, 5001))
        for subtotal, expected in cases:
            with self.subTest(subtotal=subtotal):
                order = {"items": [{"qty": 1, "price": subtotal}], "code": None}
                result = calc(order)
                self.assertEqual(expected, result)
                self.assertIs(type(result), int)

    def test_discount_can_move_subtotal_below_surcharge_threshold(self):
        order = {"items": [{"qty": 1, "price": 5500}], "code": "SAVE10"}
        result = calc(order)
        self.assertEqual(5449.0, result)
        self.assertIs(type(result), float)

    def test_order_is_not_mutated(self):
        order = {
            "items": [{"qty": 1, "price": 1000}],
            "code": "VIP20",
            "customer": "VIP-7",
        }
        original_order = copy.deepcopy(order)

        calc(order)

        self.assertEqual(original_order, order)


if __name__ == "__main__":
    unittest.main()
