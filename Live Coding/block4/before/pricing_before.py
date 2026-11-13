_SAVE10_CODE = "SAVE10"
_VIP20_CODE = "VIP20"
_VIP_CUSTOMER_PREFIX = "VIP-"
_SAVE10_DISCOUNT_PERCENT = 10
_VIP20_DISCOUNT_PERCENT = 20
_PERCENT_BASE = 100
_SURCHARGE_THRESHOLD = 5000
_SURCHARGE_AMOUNT = 499


def _calculate_subtotal(items):
    total = 0
    for item in items:
        if item["qty"] > 0 and item["price"] >= 0:
            total = total + item["qty"] * item["price"]

    return total


def _apply_discount(total, order):
    if order.get("code") is not None:
        if order["code"] == _SAVE10_CODE:
            total = total - (total * _SAVE10_DISCOUNT_PERCENT / _PERCENT_BASE)
        elif order["code"] == _VIP20_CODE and order.get("customer", "").startswith(_VIP_CUSTOMER_PREFIX):
            total = total - (total * _VIP20_DISCOUNT_PERCENT / _PERCENT_BASE)

    return total


def _apply_surcharge(total):
    if total < _SURCHARGE_THRESHOLD:
        total = total + _SURCHARGE_AMOUNT

    return total


def calc(o):
    total = _calculate_subtotal(o["items"])
    total = _apply_discount(total, o)
    total = _apply_surcharge(total)

    return total
