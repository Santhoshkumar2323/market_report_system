from modules.database import engine, get_db_session
from modules.models import Base, WeeklyReport
from modules.tickers import ASSET_STRUCTURE
from modules.data_fetcher import fetch_ticker_data
from modules.data_processor import process_and_store
from modules.report_builder import build_structured_snapshot, generate_html_table
from modules.gemini_client import generate_gemini_report
from modules.email_sender import send_email
from datetime import datetime, timezone
import json
from modules.signal_engine import compute_signals
from config.branding import PROXY_NAME, PROXY_URL, PROXY_BLOCK, ANALYTICAL_BLOCK
from modules.yield_table_builder import generate_yield_html
from modules.macro_liquidity_builder import generate_macro_html


def init_db():
    Base.metadata.create_all(bind=engine)


def run_data_pipeline():

    for category, value in ASSET_STRUCTURE.items():

        if isinstance(value, dict):
            for region, assets in value.items():

                for asset in assets:

                    df = fetch_ticker_data(asset["symbol"])

                    if not df.empty:
                        process_and_store(
                            display_name=asset["name"],
                            ticker_symbol=asset["symbol"],
                            category=category,
                            region=region,
                            df=df,
                        )

        else:

            for asset in value:

                df = fetch_ticker_data(asset["symbol"])

                if not df.empty:
                    process_and_store(
                        display_name=asset["name"],
                        ticker_symbol=asset["symbol"],
                        category=category,
                        region=None,
                        df=df,
                    )


def run_weekly_report():

    session = get_db_session()

    week_date, snapshot = build_structured_snapshot()

    if not snapshot:
        print("No snapshot data found.")
        session.close()
        return

    try:
        signals = compute_signals(snapshot)
    except Exception as e:
        print("Signal engine failed:", e)
        session.close()
        return


    try:
        gemini_text = generate_gemini_report(signals)
    except Exception as e:
        print("Gemini failed:", e)
        gemini_text = "Model commentary unavailable this week."


    report = WeeklyReport(
        report_timestamp=datetime.now(timezone.utc).date(),
        structured_input_json=json.dumps(snapshot),
        gemini_response_text=gemini_text,
        email_sent=False,
    )

    session.add(report)
    session.commit()

    report_id = report.id
    html_table = generate_html_table(snapshot, week_date)

    try:
        yield_table = generate_yield_html()
    except Exception as e:
        print("Yield table failed:", e)
        yield_table = ""

    try:
        macro_table = generate_macro_html()
    except Exception as e:
        print("Macro table failed:", e)
        macro_table = ""


    commentary_html = "<h2>Commentary</h2><ul>"

    for line in gemini_text.split("\n"):
        clean_line = line.strip()
        clean_line = clean_line.lstrip("*").lstrip("-").lstrip("•").strip()

        if clean_line:
            commentary_html += f"<li>{clean_line}</li>"

    commentary_html += "</ul><hr>"


    signal_html = "<h2>Summary</h2><ul>"

    for key, value in signals.items():

        label = key.replace("_", " ").title()

        signal_html += f"<li><b>{label}:</b> {value}</li>"

    signal_html += "</ul><hr>"


    analytical_html = f"""
<div style="font-size:13px;color:#444;margin-top:25px;line-height:1.6;">
{ANALYTICAL_BLOCK}
</div>
<hr style="margin:25px 0;">
"""

    proxy_content = PROXY_BLOCK.replace("{{PROXY_NAME}}", PROXY_NAME)
    proxy_content = proxy_content.replace("{{PROXY_URL}}", PROXY_URL)

    proxy_html = f"""
<div style="
background-color:#f4f6fa;
border-left:5px solid #000;
padding:20px;
margin-top:20px;
font-family:Arial;
">
<h3 style="margin-top:0;margin-bottom:12px;">Beyond the Snapshot</h3>
<div style="font-size:14px;line-height:1.6;">
{proxy_content}
</div>
</div>
"""


    full_email = (
        html_table
        + yield_table
        + macro_table
        + commentary_html
        + signal_html
        + analytical_html
        + proxy_html
    )

    try:
        send_email(
            subject=f"Weekly Macro Snapshot – {week_date} | {datetime.now().strftime('%H:%M')}",
            html_content=full_email,
            report_id=report_id,
        )
    except Exception as e:
        print("Email sending failed:", e)
        session.close()
        return

    report.email_sent = True
    session.commit()
    session.close()

    print("Weekly report sent.")


if __name__ == "__main__":

    print("Starting market report system...")

    init_db()
    run_data_pipeline()
    run_weekly_report()