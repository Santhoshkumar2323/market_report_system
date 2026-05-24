from modules.yield_table_builder import generate_yield_html

html = generate_yield_html()

with open("yield_preview.html", "w", encoding="utf-8") as f:
    f.write(html)

print("HTML preview generated: yield_preview.html")