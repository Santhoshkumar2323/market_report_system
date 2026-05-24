from modules.yield_table_builder import build_yield_table

rows = build_yield_table()

print("\nGLOBAL BOND MARKET\n")

for r in rows:

    spread_text = ""
    if r["spread"] is not None:
        bps = r["spread"] * 100
        spread_text = f"{bps:.0f} bps ({r['curve']})"

    print(
        f"{r['country']} ({r['role']}) | "
        f"10Y: {r['y10']:.2f}% | "
        f"3MΔ: {'' if r['y10_3m'] is None else f'{r['y10_3m']:.2f}%'} | "
        f"6MΔ: {'' if r['y10_6m'] is None else f'{r['y10_6m']:.2f}%'} | "
        f"2Y: {'' if r['y2'] is None else f'{r['y2']:.2f}%'} | "
        f"Curve: {spread_text}"
    )