"""Vorher: absichtlich mit Code-Smells versehene Rabattberechnung.

Diese Datei dient als Ausgangspunkt fuer die Refactoring-Demo in Block 4.
Nicht als Vorbild fuer produktiven Code verwenden.
"""


def calc(o):
    # lange Funktion, tiefe Verschachtelung, Magic Numbers, unklare Namen
    t = 0
    for i in o["items"]:
        if i["qty"] > 0:
            if i["price"] >= 0:
                t = t + i["qty"] * i["price"]
            else:
                t = t + 0
        else:
            t = t + 0
    if o.get("code") is not None:
        if o["code"] == "SAVE10":
            t = t - (t * 10 / 100)
        else:
            if o["code"] == "VIP20":
                if o.get("customer", "").startswith("VIP-"):
                    t = t - (t * 20 / 100)
                else:
                    pass
            else:
                pass
    if t < 5000:
        t = t + 499
    else:
        t = t + 0
    return t
