# modules/signal_engine.py

import statistics


def compute_average(values):
    return sum(values) / len(values) if values else 0


def classify_volatility(avg_vol):
    if avg_vol > 3.5:
        return "Elevated"
    elif avg_vol > 2:
        return "Normal"
    else:
        return "Calm"


def compute_signals(snapshot):

    signals = {}

    # --------------------------
    # Global Region Strength
    # --------------------------
    regions = {}
    if "Global Indices" in snapshot:
        for region, assets in snapshot["Global Indices"].items():
            avg_return = compute_average([a["pct_10d"] for a in assets])
            regions[region] = avg_return

    if regions:
        strongest_region = max(regions, key=regions.get)
        weakest_region = min(regions, key=regions.get)

        signals["strongest_region"] = strongest_region
        signals["weakest_region"] = weakest_region

        positive_regions = sum(1 for r in regions.values() if r > 0)
        signals["market_structure"] = (
            "Moving together" if positive_regions == len(regions)
            else "Mixed across regions"
        )

    # --------------------------
    # US Sector Leadership
    # --------------------------
    if "US Sectors" in snapshot:
        sectors = snapshot["US Sectors"].get(None, [])
        if sectors:
            strongest_sector = max(sectors, key=lambda x: x["pct_10d"])
            weakest_sector = min(sectors, key=lambda x: x["pct_10d"])

            signals["strongest_us_sector"] = strongest_sector["name"]
            signals["weakest_us_sector"] = weakest_sector["name"]

    # --------------------------
    # Commodities
    # --------------------------
    if "Commodities" in snapshot:
        commodities = snapshot["Commodities"].get(None, [])

        gold = next((a for a in commodities if "Gold" in a["name"]), None)
        oil = next((a for a in commodities if "Crude" in a["name"]), None)
        copper = next((a for a in commodities if "Copper" in a["name"]), None)

        if gold and oil:
            if gold["pct_10d"] > 0 and oil["pct_10d"] > 0:
                signals["commodity_signal"] = "Gold and oil rising together"
            else:
                signals["commodity_signal"] = "Commodities mixed"

        if copper and copper["pct_10d"] < 0:
            signals["commodity_note"] = "Copper showing weakness"

    # --------------------------
    # Crypto
    # --------------------------
    if "Crypto" in snapshot:
        crypto_assets = snapshot["Crypto"].get(None, [])
        if crypto_assets:
            avg_crypto = compute_average([a["pct_10d"] for a in crypto_assets])
            if abs(avg_crypto) < 1:
                signals["crypto_signal"] = "Neutral risk appetite"
            elif avg_crypto > 0:
                signals["crypto_signal"] = "Risk appetite positive"
            else:
                signals["crypto_signal"] = "Risk appetite cautious"

    # --------------------------
    # Volatility
    # --------------------------
    all_vol = []
    for category in snapshot:
        for region in snapshot[category]:
            for asset in snapshot[category][region]:
                all_vol.append(asset["vol"])

    avg_vol = compute_average(all_vol)
    signals["volatility_state"] = classify_volatility(avg_vol)

    return signals