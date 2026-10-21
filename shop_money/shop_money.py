# ==========================================================
# ระบบบันทึกรายรับ-รายจ่าย ร้านค้าเล็กในชุมชน
# ผู้พัฒนา: วิทวัส ชาลีเครือ
# ภาษา: Python + tkinter + SQLite
# ==========================================================

import tkinter as tk
from tkinter import ttk           # widget แบบใหม่ เช่น ตาราง (Treeview)
from tkinter import messagebox    # กล่องข้อความแจ้งเตือน
import sqlite3                    # ฐานข้อมูลแบบไฟล์เดียว
from datetime import date, datetime

DB_FILE = "shop.db"   # ชื่อไฟล์ฐานข้อมูล (จะถูกสร้างอัตโนมัติ)


# ---------- ส่วนที่ 1: ฐานข้อมูล ----------

conn = sqlite3.connect(DB_FILE)   # เปิด (หรือสร้าง) ไฟล์ฐานข้อมูล
cur = conn.cursor()               # ตัวสั่งงานฐานข้อมูล

cur.execute("""
    CREATE TABLE IF NOT EXISTS records (
        id      INTEGER PRIMARY KEY AUTOINCREMENT,
        date    TEXT,
        kind    TEXT,
        detail  TEXT,
        amount  REAL
    )
""")
conn.commit()


# ---------- ส่วนที่ 2: ฟังก์ชันช่วยเหลือ ----------

def read_form():
    """อ่านค่าจากช่องกรอก ตรวจความถูกต้อง
    ถ้าถูกต้อง คืนค่า (วันที่, ประเภท, รายละเอียด, จำนวนเงิน)
    ถ้าผิด แจ้งเตือนแล้วคืนค่า None"""
    date_text = date_entry.get().strip()
    kind = kind_var.get()
    detail = detail_entry.get().strip()
    amount_text = amount_entry.get().strip()

    # ตรวจรูปแบบวันที่ ต้องเป็น ปี-เดือน-วัน เช่น 2026-10-17
    try:
        datetime.strptime(date_text, "%Y-%m-%d")
    except ValueError:
        messagebox.showwarning("ข้อมูลผิด", "วันที่ต้องเป็นรูปแบบ ปปปป-ดด-วว เช่น 2026-10-17")
        return None

    if detail == "":
        messagebox.showwarning("ข้อมูลผิด", "กรุณากรอกรายละเอียด")
        return None

    # ตรวจจำนวนเงิน ต้องเป็นตัวเลขและมากกว่า 0
    try:
        amount = float(amount_text)
    except ValueError:
        messagebox.showwarning("ข้อมูลผิด", "จำนวนเงินต้องเป็นตัวเลข")
        return None
    if amount <= 0:
        messagebox.showwarning("ข้อมูลผิด", "จำนวนเงินต้องมากกว่า 0")
        return None

    return date_text, kind, detail, amount


def clear_form():
    """ล้างช่องกรอก และยกเลิกการเลือกแถวในตาราง"""
    date_entry.delete(0, tk.END)
    date_entry.insert(0, str(date.today()))
    kind_var.set("รายรับ")
    detail_entry.delete(0, tk.END)
    amount_entry.delete(0, tk.END)
    for row in table.selection():
        table.selection_remove(row)


def get_selected_id():
    """คืนค่า id ของแถวที่เลือกในตาราง ถ้าไม่ได้เลือก คืนค่า None"""
    selected = table.selection()
    if len(selected) == 0:
        messagebox.showinfo("แจ้งเตือน", "กรุณาคลิกเลือกรายการในตารางก่อน")
        return None
    values = table.item(selected[0], "values")
    return values[0]   # คอลัมน์แรกคือ id


# ---------- ส่วนที่ 3: CRUD (สร้าง อ่าน แก้ ลบ) ----------

def load_data():
    """R = Read: อ่านข้อมูลจากฐานข้อมูลมาแสดงในตาราง + คำนวณสรุป"""
    # ลบแถวเก่าในตารางออกให้หมดก่อน
    for row in table.get_children():
        table.delete(row)

    month = month_entry.get().strip()   # เช่น "2026-10" หรือว่าง
    if month == "":
        cur.execute("SELECT * FROM records ORDER BY date DESC")
    else:
        cur.execute("SELECT * FROM records WHERE date LIKE ? ORDER BY date DESC",
                    (month + "%",))
    rows = cur.fetchall()

    total_income = 0
    total_expense = 0

    for r in rows:
        record_id, d, kind, detail, amount = r
        table.insert("", tk.END, values=(record_id, d, kind, detail, f"{amount:,.2f}"),
                     tags=(kind,))
        if kind == "รายรับ":
            total_income = total_income + amount
        else:
            total_expense = total_expense + amount

    profit = total_income - total_expense

    income_label.config(text=f"รายรับรวม: {total_income:,.2f} บาท")
    expense_label.config(text=f"รายจ่ายรวม: {total_expense:,.2f} บาท")
    if profit >= 0:
        profit_label.config(text=f"กำไร: {profit:,.2f} บาท", fg="green")
    else:
        profit_label.config(text=f"ขาดทุน: {-profit:,.2f} บาท", fg="red")


def add_record():
    """C = Create: เพิ่มรายการใหม่"""
    data = read_form()
    if data is None:
        return
    cur.execute("INSERT INTO records (date, kind, detail, amount) VALUES (?, ?, ?, ?)",
                data)
    conn.commit()
    clear_form()
    load_data()


def update_record():
    """U = Update: แก้ไขรายการที่เลือก"""
    record_id = get_selected_id()
    if record_id is None:
        return
    data = read_form()
    if data is None:
        return
    d, kind, detail, amount = data
    cur.execute("UPDATE records SET date=?, kind=?, detail=?, amount=? WHERE id=?",
                (d, kind, detail, amount, record_id))
    conn.commit()
    clear_form()
    load_data()


def delete_record():
    """D = Delete: ลบรายการที่เลือก (ถามยืนยันก่อน)"""
    record_id = get_selected_id()
    if record_id is None:
        return
    if messagebox.askyesno("ยืนยัน", "ต้องการลบรายการนี้ใช่ไหม?"):
        cur.execute("DELETE FROM records WHERE id=?", (record_id,))
        conn.commit()
        clear_form()
        load_data()


def on_select(event):
    """เมื่อคลิกแถวในตาราง ให้นำข้อมูลมาใส่ช่องกรอก (เพื่อแก้ไข)"""
    selected = table.selection()
    if len(selected) == 0:
        return
    record_id, d, kind, detail, amount = table.item(selected[0], "values")
    date_entry.delete(0, tk.END)
    date_entry.insert(0, d)
    kind_var.set(kind)
    detail_entry.delete(0, tk.END)
    detail_entry.insert(0, detail)
    amount_entry.delete(0, tk.END)
    amount_entry.insert(0, amount.replace(",", ""))


def show_all():
    """ล้างตัวกรองเดือน แล้วแสดงทุกรายการ"""
    month_entry.delete(0, tk.END)
    load_data()


# ---------- ส่วนที่ 4: สร้างหน้าต่าง (GUI) ----------

root = tk.Tk()
root.title("ระบบรายรับ-รายจ่าย ร้านค้าชุมชน")
root.geometry("760x600")

style = ttk.Style()
style.theme_use("clam")   # ธีมนี้ทำให้ใส่สีแถวในตารางได้ทุกเครื่อง (รวมถึง Mac)

tk.Label(root, text="🏪 ระบบรายรับ-รายจ่าย ร้านค้าชุมชน",
         font=("Helvetica", 18, "bold")).pack(pady=10)

# --- กรอบช่องกรอกข้อมูล ---
form = tk.LabelFrame(root, text="ข้อมูลรายการ", padx=10, pady=10)
form.pack(fill="x", padx=15)

tk.Label(form, text="วันที่ (ปปปป-ดด-วว):").grid(row=0, column=0, sticky="w")
date_entry = tk.Entry(form, width=15)
date_entry.grid(row=0, column=1, sticky="w", pady=3)

tk.Label(form, text="ประเภท:").grid(row=0, column=2, sticky="w", padx=(20, 0))
kind_var = tk.StringVar(value="รายรับ")
tk.Radiobutton(form, text="รายรับ", variable=kind_var, value="รายรับ").grid(row=0, column=3)
tk.Radiobutton(form, text="รายจ่าย", variable=kind_var, value="รายจ่าย").grid(row=0, column=4)

tk.Label(form, text="รายละเอียด:").grid(row=1, column=0, sticky="w")
detail_entry = tk.Entry(form, width=40)
detail_entry.grid(row=1, column=1, columnspan=4, sticky="w", pady=3)

tk.Label(form, text="จำนวนเงิน (บาท):").grid(row=2, column=0, sticky="w")
amount_entry = tk.Entry(form, width=15)
amount_entry.grid(row=2, column=1, sticky="w", pady=3)

# --- ปุ่ม ---
buttons = tk.Frame(root)
buttons.pack(pady=8)
tk.Button(buttons, text="➕ เพิ่ม", width=10, command=add_record).pack(side="left", padx=4)
tk.Button(buttons, text="✏️ แก้ไข", width=10, command=update_record).pack(side="left", padx=4)
tk.Button(buttons, text="🗑 ลบ", width=10, command=delete_record).pack(side="left", padx=4)
tk.Button(buttons, text="ล้างช่อง", width=10, command=clear_form).pack(side="left", padx=4)

# --- ตัวกรองเดือน ---
filter_frame = tk.Frame(root)
filter_frame.pack()
tk.Label(filter_frame, text="ดูเฉพาะเดือน (ปปปป-ดด):").pack(side="left")
month_entry = tk.Entry(filter_frame, width=10)
month_entry.pack(side="left", padx=4)
tk.Button(filter_frame, text="แสดง", command=load_data).pack(side="left", padx=2)
tk.Button(filter_frame, text="ทั้งหมด", command=show_all).pack(side="left", padx=2)

# --- ตาราง ---
columns = ("id", "date", "kind", "detail", "amount")
table = ttk.Treeview(root, columns=columns, show="headings", height=10)
table.heading("id", text="ลำดับ")
table.heading("date", text="วันที่")
table.heading("kind", text="ประเภท")
table.heading("detail", text="รายละเอียด")
table.heading("amount", text="จำนวนเงิน")
table.column("id", width=50, anchor="center")
table.column("date", width=100, anchor="center")
table.column("kind", width=80, anchor="center")
table.column("detail", width=300)
table.column("amount", width=120, anchor="e")
table.tag_configure("รายรับ", background="#e3f6e3")
table.tag_configure("รายจ่าย", background="#fbe4e4")
table.pack(fill="both", expand=True, padx=15, pady=8)
table.bind("<<TreeviewSelect>>", on_select)

# --- สรุปยอด ---
summary = tk.Frame(root)
summary.pack(pady=5)
income_label = tk.Label(summary, text="", fg="green", font=("Helvetica", 13))
income_label.pack(side="left", padx=10)
expense_label = tk.Label(summary, text="", fg="red", font=("Helvetica", 13))
expense_label.pack(side="left", padx=10)
profit_label = tk.Label(summary, text="", font=("Helvetica", 14, "bold"))
profit_label.pack(side="left", padx=10)

# --- เริ่มทำงาน ---
clear_form()
load_data()
root.mainloop()
conn.close()   # ปิดฐานข้อมูลเมื่อปิดโปรแกรม
