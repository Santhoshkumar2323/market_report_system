from modules.fred_fetcher import fetch_fred_series
from datetime import timedelta

COUNTRY_YIELD_SERIES = {
    "United States": {
        "role": "Global Anchor",
        "10Y": "DGS10",
        "2Y": "DGS2",
    },
    "Japan": {
        "role": "Liquidity Source",
        "10Y": "IRLTLT01JPM156N",
        "2Y": "IR3TIB01JPM156N",
    },
    "Germany": {
        "role": "EU Core",
        "10Y": "IRLTLT01DEM156N",
        "2Y": "IR3TIB01DEM156N",
    },
    "Canada": {
        "role": "Energy Proxy",
        "10Y": "IRLTLT01CAM156N",
        "2Y": "IR3TIB01CAM156N",
    },
    "Australia": {
        "role": "Commodity Proxy",
        "10Y": "IRLTLT01AUM156N",
        "2Y": "IR3TIB01AUM156N",
    },
    "India": {
        "role": "High Growth EM",
        "10Y": "INDIRLTLT01STM",
        "2Y": None,  # no FRED short rate
    },
}

def compute_delta(df, months):

    if df is None or df.empty:
        return None

    try:
        latest_date = df["date"].iloc[-1]
        latest_value = df["value"].iloc[-1]

        target_date = latest_date - timedelta(days=30 * months)

        past_rows = df[df["date"] <= target_date]

        if past_rows.empty:
            return None

        past_value = past_rows.iloc[-1]["value"]

        return latest_value - past_value

    except Exception:
        return None


def classify_curve(spread):

    if spread is None:
        return None

    if spread < 0:
        return "Inverted"

    if spread > 1:
        return "Steep"

    return "Normal"


def build_yield_table():

    rows = []

    for country, data in COUNTRY_YIELD_SERIES.items():

        role = data["role"]

        df10 = fetch_fred_series(data["10Y"], days=400)
        df2 = fetch_fred_series(data["2Y"], days=400) if data["2Y"] else None

        if df10 is None or df10.empty:
            continue

        try:
            y10 = df10["value"].iloc[-1]
        except Exception:
            continue

        y10_3m = compute_delta(df10, 3)
        y10_6m = compute_delta(df10, 6)

        if df2 is not None and not df2.empty:
            y2 = df2["value"].iloc[-1]
            y2_3m = compute_delta(df2, 3)
            y2_6m = compute_delta(df2, 6)
        else:
            y2 = y2_3m = y2_6m = None

        spread = None
        curve_label = None

        if y2 is not None:
            spread = y10 - y2
            curve_label = classify_curve(spread)

        rows.append({
            "country": country,
            "role": role,
            "y10": y10,
            "y10_3m": y10_3m,
            "y10_6m": y10_6m,
            "y2": y2,
            "y2_3m": y2_3m,
            "y2_6m": y2_6m,
            "spread": spread,
            "curve": curve_label,
        })

    return rows


def fmt_value(value):
    if value is None:
        return "—"
    return f"{value:.2f}%"


def fmt_delta(value):

    if value is None:
        return "—"

    color = "#0a8a0a" if value >= 0 else "#c0392b"
    sign = "+" if value >= 0 else ""

    return f'<span style="color:{color};"><b>{sign}{value:.2f}%</b></span>'


def fmt_curve(spread, label):

    if spread is None:
        return "—"

    bps = spread * 100
    return f"{bps:.0f} bps ({label})"


def generate_yield_html():

    rows = build_yield_table()

    html = """
    <h2>Global Bond Market</h2>

    <table border="1" cellpadding="6" cellspacing="0" width="100%"
    style="border-collapse:collapse;font-family:Arial;font-size:13px;margin-bottom:20px;">

    <thead>
    <tr style="background-color:#f0f0f0;">
        <th align="left">Country (Role)</th>
        <th align="right">10Y Yield</th>
        <th align="right">10Y: 3M Δ</th>
        <th align="right">10Y: 6M Δ</th>
        <th align="right">2Y Yield</th>
        <th align="right">2Y: 3M Δ</th>
        <th align="right">2Y: 6M Δ</th>
        <th align="right">Yield Curve</th>
    </tr>
    </thead>

    <tbody>
    """

    for r in rows:

        html += f"""
        <tr>
            <td><b>{r['country']}</b> ({r['role']})</td>
            <td align="right">{fmt_value(r['y10'])}</td>
            <td align="right">{fmt_delta(r['y10_3m'])}</td>
            <td align="right">{fmt_delta(r['y10_6m'])}</td>
            <td align="right">{fmt_value(r['y2'])}</td>
            <td align="right">{fmt_delta(r['y2_3m'])}</td>
            <td align="right">{fmt_delta(r['y2_6m'])}</td>
            <td align="right">{fmt_curve(r['spread'], r['curve'])}</td>
        </tr>
        """

    html += "</tbody></table>"

    return html