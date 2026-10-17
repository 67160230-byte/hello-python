# Python CI/CD Lab

ภูริพัฒน์ ตานน้อย · รหัสนิสิต 67160230

- Website: https://67160230-byte.github.io/hello-python/
- Repository: https://github.com/67160230-byte/hello-python
- Actions: https://github.com/67160230-byte/hello-python/actions

โปรเจกต์หมวด 1–4 จากคู่มือ GitHub Actions ภาค 2 อ่านคะแนนตัวอย่างจาก CSV คำนวณเกรดและค่าเฉลี่ย แล้วสร้างเว็บ Static ด้วย Python ข้อมูลบนเว็บเป็นข้อมูลสมมติสำหรับแลป ไม่ใช่ผลการเรียนจริง

## โครงสร้าง

- `grades.py`: แปลงคะแนนเป็นเกรด A–F และคำนวณค่าเฉลี่ย
- `build_site.py`: อ่าน CSV, escape ข้อความ HTML และสร้าง `_site/index.html`
- `data/scores.csv`: คะแนนตัวอย่าง
- `tests/`: ทดสอบค่าขอบ คะแนนผิด ค่าเฉลี่ย การอ่าน CSV การสร้างเว็บ และการ escape HTML
- `.github/workflows/ci.yml`: lint และ tests ก่อน build/deploy

## รันในเครื่อง

```sh
python -m venv .venv
# Windows: .venv\Scripts\activate
# macOS/Linux: source .venv/bin/activate
python -m pip install -r requirements-dev.txt
python -m ruff check .
python -m pytest --cov=grades --cov=build_site --cov-report=term-missing --cov-fail-under=80
python build_site.py
```

เปิด `_site/index.html` เพื่อดูผล ไม่ commit `_site/` หรือ `.venv/` เพราะสร้างใหม่ได้

## Workflow ทำงานอย่างไร

เมื่อ push เข้า main หรือกด Run workflow จะเริ่ม job `test` บน Python 3.13 ติดตั้งเครื่องมือตามเวอร์ชันใน requirements-dev.txt แล้วตรวจด้วย Ruff และ pytest โดยต้องมี coverage อย่างน้อย 80% ส่วน job `deploy` กำหนด `needs: test` จึงเริ่มได้เมื่อ test ผ่านเท่านั้น จากนั้นสร้างเว็บด้วย Python และส่งเฉพาะโฟลเดอร์ `_site` ไปยัง GitHub Pages

## ทำความเข้าใจผล

- CI: ตรวจโค้ดและข้อมูลทุกครั้งที่ push หากคำสั่งคืน exit code ที่ไม่ใช่ 0 จะล้มเหลว
- CD: เมื่อ CI ผ่าน จึงสร้างเว็บและเผยแพร่อัตโนมัติ
- ถ้า CSV มีคะแนน 850 test จะไม่ผ่าน และ deploy ถูกข้าม เว็บที่เผยแพร่สำเร็จครั้งก่อนยังอยู่
- ถ้าแก้ CSV เป็นคะแนนที่ถูกต้องแล้ว push ใหม่ ระบบจึงอัปเดตเว็บ
- เพิ่มไฟล์ `test_*.py` ภายใน tests ได้โดยไม่ต้องแก้ workflow เพราะ pytest ค้นหา tests ให้เอง

ผลตรวจในเครื่อง: 22 tests ผ่าน, coverage 97.30% (Python 3.12); GitHub Actions กำหนด Python 3.13 ตามคู่มือ
