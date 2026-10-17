import csv
import html
import os
from pathlib import Path

from grades import average, grade

OUTPUT_DIR = Path("_site")


def load_scores(csv_path):
    with open(csv_path, encoding="utf-8") as file:
        return [(row["name"], int(row["score"])) for row in csv.DictReader(file)]


def render_html(rows, title):
    table_rows = "\n".join(
        f'<tr><td>{html.escape(name)}</td><td>{score}</td>'
        f'<td><span class="grade">{grade(score)}</span></td></tr>'
        for name, score in rows
    )
    avg = average([score for _, score in rows])
    return f'''<!doctype html>
<html lang="th"><head><meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>{html.escape(title)}</title>
<style>
*{{box-sizing:border-box}}body{{margin:0;background:#f5f7f3;color:#213a2e;font-family:system-ui,sans-serif;line-height:1.7}}
main{{width:min(850px,90%);margin:60px auto}}.eyebrow{{font-size:12px;letter-spacing:2px;color:#537457}}
h1{{font-size:clamp(28px,5vw,42px);margin:12px 0}}.muted{{color:#68756b}}
.summary{{display:flex;gap:45px;padding:25px 0;margin:25px 0;border-top:1px solid #d9e1d5;border-bottom:1px solid #d9e1d5}}
.summary strong{{display:block;font-size:30px}}.summary span{{font-size:13px;color:#68756b}}
.table-wrap{{overflow-x:auto;border:1px solid #d9e1d5;border-radius:12px;background:white}}
table{{width:100%;border-collapse:collapse;text-align:left}}th,td{{padding:16px 22px;border-bottom:1px solid #e5e9e1}}th{{background:#eaf0e4;font-size:13px}}tr:last-child td{{border:0}}
.grade{{display:inline-block;background:#e6eedc;color:#356140;border-radius:5px;padding:2px 14px;font-weight:700}}
footer{{margin-top:28px;font-size:12px;color:#68756b}}a{{color:#356140}}@media(max-width:500px){{main{{margin:30px auto}}th,td{{padding:12px}}.summary{{gap:25px}}}}
</style></head><body><main>
<p class="eyebrow">PYTHON / CI / CD LAB</p><h1>{html.escape(title)}</h1>
<p class="muted">ภูริพัฒน์ ตานน้อย · 67160230</p>
<p>ข้อมูลตัวอย่างสำหรับฝึกคำนวณเกรดและเผยแพร่เว็บอัตโนมัติ ไม่ใช่ผลการเรียนจริง</p>
<div class="summary"><div><strong>{len(rows)}</strong><span>รายการคะแนน</span></div><div><strong>{avg:.2f}</strong><span>คะแนนเฉลี่ย</span></div></div>
<div class="table-wrap"><table><caption style="text-align:left;padding:16px 22px">ตารางผลคะแนนตัวอย่าง</caption><thead><tr><th scope="col">ชื่อ</th><th scope="col">คะแนน</th><th scope="col">เกรด</th></tr></thead><tbody>{table_rows}</tbody></table></div>
<p>ค่าเฉลี่ย: {avg}</p><p class="muted">เกณฑ์: A ≥ 80 · B ≥ 70 · C ≥ 60 · D ≥ 50 · F &lt; 50</p>
<footer>CSV → Python → Tests → GitHub Pages · <a href="https://github.com/67160230-byte/hello-python">ดูซอร์สโค้ดและ Workflow ↗</a></footer>
</main></body></html>'''


def main():
    title = os.environ.get("SITE_TITLE") or "ผลคะแนนวิชา CI/CD"
    rows = load_scores("data/scores.csv")
    OUTPUT_DIR.mkdir(exist_ok=True)
    (OUTPUT_DIR / "index.html").write_text(render_html(rows, title), encoding="utf-8")
    print(f"Built {OUTPUT_DIR / 'index.html'} ({len(rows)} students)")


if __name__ == "__main__":
    main()
