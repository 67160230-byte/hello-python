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

@import url('https://fonts.googleapis.com/css2?family=Noto+Sans+Thai:wght@400;500;600;700&display=swap');
:root{{color-scheme:dark;--bg:#111412;--panel:#1a201b;--line:#354033;--text:#f2f5e9;--muted:#adb9a7;--lime:#d0f56b}}*{{box-sizing:border-box}}body{{margin:0;background:var(--bg);color:var(--text);font-family:'Noto Sans Thai',system-ui,sans-serif;line-height:1.8}}main{{width:min(1080px,90%);margin:0 auto;padding-bottom:30px}}a{{color:inherit;text-decoration:none}}.topbar{{display:flex;justify-content:space-between;align-items:center;gap:20px;padding:24px 0;border-bottom:1px solid var(--line);margin-bottom:55px}}.brand{{font:bold 33px system-ui;letter-spacing:-3px;color:var(--lime)}}.brand small{{font:10px system-ui;letter-spacing:2px;color:var(--muted);margin-left:20px}}.back{{font-size:12px;border:1px solid var(--line);border-radius:30px;padding:9px 16px}}.back:hover{{border-color:var(--lime);color:var(--lime)}}.eyebrow{{font:11px/1.7 system-ui;letter-spacing:2px;color:var(--lime);margin:0 0 15px}}.eyebrow::before{{content:'';display:inline-block;width:7px;height:7px;background:var(--lime);border-radius:50%;margin-right:10px}}h1{{font-size:clamp(30px,5vw,49px);letter-spacing:-1px;line-height:1.45;margin:15px 0}}.muted{{color:var(--muted)}}.owner{{font-size:14px}}.notice{{font-size:12px;color:var(--muted);max-width:700px}}.summary{{display:grid;grid-template-columns:1fr 1.35fr 1fr;gap:18px;margin:35px 0 45px}}.summary>div{{padding:25px 28px;border:1px solid var(--line);border-radius:12px;background:var(--panel);position:relative}}.summary>div:nth-child(2){{background:var(--lime);color:#192310;border-color:var(--lime)}}.summary strong{{display:block;font:600 clamp(32px,5vw,50px)/1.3 system-ui;letter-spacing:-2px;margin:20px 0 8px;font-variant-numeric:tabular-nums}}.summary span{{font-size:12px;color:var(--muted)}}.summary>div:nth-child(2) span{{color:#34471b}}.metric-label{{font:10px system-ui;letter-spacing:1.5px}}.metric-arrow{{position:absolute;right:22px;top:20px;font-size:20px}}.table-wrap{{overflow-x:auto;border:1px solid var(--line);border-radius:14px;background:var(--panel)}}table{{width:100%;border-collapse:collapse;text-align:left;font-variant-numeric:tabular-nums}}caption{{text-align:left;padding:23px 26px;font-size:19px;font-weight:600}}caption span{{font:10px system-ui;letter-spacing:1px;color:var(--muted);margin-left:15px}}th,td{{padding:18px 26px;border-bottom:1px solid var(--line)}}th{{background:#252e20;color:var(--muted);font-size:12px;font-weight:400}}td{{font-size:15px}}th:nth-child(2),td:nth-child(2){{text-align:right;width:24%}}th:nth-child(3),td:nth-child(3){{text-align:center;width:24%}}tbody tr:nth-child(even){{background:#1e261f}}tbody tr:hover{{background:#2b3625}}tr:last-child td{{border:0}}.grade{{display:inline-block;min-width:45px;text-align:center;background:#d0f56b;color:#192310;border-radius:6px;padding:3px 13px;font:700 14px/1.8 system-ui}}.legend{{display:flex;gap:8px;flex-wrap:wrap;margin:20px 0}}.legend span{{border:1px solid var(--line);border-radius:6px;padding:6px 12px;color:var(--muted);font-size:11px}}.average-note{{font-size:12px;color:var(--muted)}}footer{{display:flex;justify-content:space-between;gap:20px;flex-wrap:wrap;border-top:1px solid var(--line);padding-top:25px;margin-top:40px;font-size:11px;color:var(--muted)}}footer a{{color:var(--lime)}}:focus-visible{{outline:3px solid var(--lime);outline-offset:5px}}@media(max-width:650px){{.topbar{{margin-bottom:35px}}.brand small{{display:none}}.summary{{gap:10px;margin:25px 0}}.summary>div{{padding:18px 14px}}.summary strong{{font-size:32px}}.metric-label{{font-size:8px;letter-spacing:.5px}}.metric-arrow{{display:none}}.summary span{{font-size:10px}}th,td{{padding:15px}}caption{{font-size:16px;padding:20px 15px}}caption span{{display:block;margin:7px 0 0}}h1{{font-size:32px}}.back{{font-size:11px}}}}@media(max-width:360px){{.summary{{grid-template-columns:1fr}}.summary strong{{margin-top:10px}}}}
</style></head><body><main>
<header class="topbar"><a class="brand" href="https://67160230-byte.github.io/webdev-actions-lab/">pt.<small>LEARNING SPACE / SCOREBOARD</small></a><a class="back" href="https://67160230-byte.github.io/webdev-actions-lab/">← เว็บแนะนำตัว</a></header><p class="eyebrow">PYTHON / CI / CD LAB</p><h1>{html.escape(title)}</h1>
<p class="owner muted">ภูริพัฒน์ ตานน้อย · 67160230</p>
<p class="notice">89033167 Web Application Development<br>ข้อมูลตัวอย่างสำหรับฝึกคำนวณเกรดและเผยแพร่เว็บอัตโนมัติ ไม่ใช่ผลการเรียนจริง</p>
<div class="summary"><div><div class="metric-label">TOTAL STUDENTS</div><i class="metric-arrow">↗</i><strong>{len(rows):02d}</strong><span>รายการคะแนนตัวอย่าง</span></div><div><div class="metric-label">CLASS AVERAGE</div><i class="metric-arrow">✳</i><strong>{avg:.2f}</strong><span>คะแนนเฉลี่ย / 100</span></div><div><div class="metric-label">HIGHEST SCORE</div><i class="metric-arrow">↑</i><strong>{max(score for _, score in rows)}</strong><span>คะแนนสูงสุด / 100</span></div></div>
<div class="table-wrap"><table><caption>ตารางผลคะแนนตัวอย่าง <span>STUDENT PERFORMANCE / 2026</span></caption><thead><tr><th scope="col">ชื่อ</th><th scope="col">คะแนน</th><th scope="col">เกรด</th></tr></thead><tbody>{table_rows}</tbody></table></div>
<p class="average-note">ค่าเฉลี่ย: {avg}</p><div class="legend" aria-label="เกณฑ์การให้เกรด"><span>A · 80–100</span><span>B · 70–79</span><span>C · 60–69</span><span>D · 50–59</span><span>F · ต่ำกว่า 50</span></div>
<footer><span>CSV → Python → Tests → GitHub Pages</span><a href="https://github.com/67160230-byte/hello-python">ดูซอร์สโค้ดและ Workflow ↗</a></footer>
</main></body></html>'''


def main():
    title = os.environ.get("SITE_TITLE") or "ผลคะแนนวิชา CI/CD"
    rows = load_scores("data/scores.csv")
    OUTPUT_DIR.mkdir(exist_ok=True)
    (OUTPUT_DIR / "index.html").write_text(render_html(rows, title), encoding="utf-8")
    print(f"Built {OUTPUT_DIR / 'index.html'} ({len(rows)} students)")


if __name__ == "__main__":
    main()
