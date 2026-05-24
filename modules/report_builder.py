# modules/report_builder.py

from sqlalchemy import desc
from modules.database import get_db_session
from modules.models import ProcessedMetrics


DISPLAY_CATEGORY_ORDER = [
    "Global Indices",
    "US Sectors",
    "India Sectors",
    "Commodities",
    "Crypto",
    "Macro Market Signals",
]

REGION_ORDER = [
    "United States",
    "Europe",
    "Japan",
    "China",
    "India",
]


def build_structured_snapshot():

    session = get_db_session()

    latest_date = session.query(
        ProcessedMetrics.week_timestamp
    ).order_by(desc(ProcessedMetrics.week_timestamp)).first()

    if not latest_date:
        return None, None

    week_date = latest_date[0]

    rows = session.query(ProcessedMetrics).filter(
        ProcessedMetrics.week_timestamp == week_date
    ).all()

    snapshot = {}

    for row in rows:

        category = row.category
        region = row.region

        if category not in snapshot:
            snapshot[category] = {}

        if region not in snapshot[category]:
            snapshot[category][region] = []

        snapshot[category][region].append({
            "name": row.ticker,
            "close": row.latest_close,
            "pct_10d": row.pct_change_10d,
            "vol": row.volatility_10d
        })

    session.close()

    return week_date, snapshot


def generate_table_html(assets):

    html = """
    <table border="1" cellpadding="6" cellspacing="0" width="100%"
    style="border-collapse:collapse; font-family:Arial; font-size:13px; margin-bottom:20px;">
        <thead>
            <tr style="background-color:#f0f0f0;">
                <th align="left">Asset</th>
                <th align="right">Close</th>
                <th align="right">10D %</th>
                <th align="right">Volatility</th>
            </tr>
        </thead>
        <tbody>
    """

    for a in assets:

        color = "#0a8a0a" if a["pct_10d"] >= 0 else "#c0392b"
        sign = "+" if a["pct_10d"] >= 0 else ""

        html += f"""
        <tr>
            <td><b>{a['name']}</b></td>
            <td align="right">{a['close']:,.2f}</td>
            <td align="right" style="color:{color};"><b>{sign}{a['pct_10d']:.2f}%</b></td>
            <td align="right">{a['vol']:.2f}%</td>
        </tr>
        """

    html += "</tbody></table>"

    return html


def generate_html_table(snapshot, week_date):

    # Bloomberg-style header
    html = f"""
    <div style="font-family:Arial, Helvetica, sans-serif; font-size:14px;">

        <div style="font-size:40px; font-weight:800; color:#000; line-height:1.1; margin-bottom:6px;">
            WEEKLY MACRO SNAPSHOT
        </div>

        <div style="font-size:18px; color:#333; margin-bottom:14px;">
            Global Markets Dashboard — {week_date}
        </div>

        <hr style="border:none; border-top:1px solid #dcdcdc; margin-bottom:25px;">
    """

    for category in DISPLAY_CATEGORY_ORDER:

        if category not in snapshot:
            continue

        html += f"""
        <h2 style="
        margin-top:30px;
        margin-bottom:10px;
        font-size:22px;
        font-weight:700;
        ">
        {category}
        </h2>
        """

        # Global indices have regions
        if category == "Global Indices":

            for region in REGION_ORDER:

                if region not in snapshot[category]:
                    continue

                html += f"""
                <h3 style="
                margin-top:15px;
                margin-bottom:5px;
                font-size:16px;
                font-weight:600;
                color:#333;
                ">
                {region}
                </h3>
                """

                html += generate_table_html(snapshot[category][region])

        else:

            region_dict = snapshot[category]
            assets = region_dict.get(None)

            if assets:
                html += generate_table_html(assets)

        html += "<hr style='margin:30px 0; border:none; border-top:1px solid #e5e5e5;'>"

    html += "</div>"

    return html