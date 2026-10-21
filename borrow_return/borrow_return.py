# ==========================================================
# ระบบยืม-คืนหนังสือ/อุปกรณ์ ของห้องเรียน
# ผู้พัฒนา: วิทวัส ชาลีเครือ
# ภาษา: Python + tkinter + SQLite
# ==========================================================

import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
import sqlite3
from datetime import date, timedelta

DB_FILE = "borrow.db"


# ---------- ส่วนที่ 1: ฐานข้อมูล ----------
# ตาราง items เก็บของ 1 ชิ้นต่อ 1 แถว
# ถ้า borrower ว่าง ("") แปลว่าของชิ้นนั้น "ว่าง" ยืมได้

conn = sqlite3.connect(DB_FILE)
cur = conn.cursor()
cur.execute("""
    CREATE TABLE IF NOT EXISTS items (
        id          INTEGER PRIMARY KEY AUTOINCREMENT,
        name        TEXT,
        borrower    TEXT DEFAULT '',
        borrow_date TEXT DEFAULT '',
        due_date    TEXT DEFAULT ''
    )
""")
conn.commit()


# ---------- ส่วนที่ 2: ตรรกะ ----------

def get_status(borrower, due_date):
    """ดูว่าของชิ้นนี้อยู่สถานะไหน: ว่าง / ถูกยืม / เลยกำหนด"""
    if borrower == "":
        return "ว่าง"
    today = str(date.today())          # เช่น "2026-10-17"
    if today > due_date:               # เทียบข้อความวันที่ได้ เพราะเรียง ปี-เดือน-วัน
        return "เลยกำหนด"
    return "ถูกยืม"


def get_selected():
    """คืนค่าข้อมูลแถวที่เลือก (id, ชื่อ, ผู้ยืม, ...) ถ้าไม่ได้เลือก คืนค่า None"""
    selected = table.selection()
    if len(selected) == 0:
        messagebox.showinfo("แจ้งเตือน", "กรุณาคลิกเลือกของในตารางก่อน")
        return None
    return table.item(selected[0], "values")


# ---------- ส่วนที่ 3: ฟังก์ชันหลัก ----------

def load_data():
    """อ่านข้อมูลจากฐานข้อมูลมาแสดงในตาราง (กรองตามคำค้นหา)"""
    for row in table.get_children():
        table.delete(row)

    keyword = search_entry.get().strip()
    cur.execute("SELECT * FROM items WHERE name LIKE ? OR borrower LIKE ? ORDER BY id",
                ("%" + keyword + "%", "%" + keyword + "%"))
    rows = cur.fetchall()

    count_free = 0
    count_borrowed = 0
    count_late = 0

    for r in rows:
        item_id, name, borrower, borrow_date, due_date = r
        status = get_status(borrower, due_date)
        table.insert("", tk.END,
                     values=(item_id, name, status, borrower, borrow_date, due_date),
                     tags=(status,))
        if status == "ว่าง":
            count_free = count_free + 1
        elif status == "ถูกยืม":
            count_borrowed = count_borrowed + 1
        else:
            count_late = count_late + 1

    summary_label.config(
        text=f"ว่าง {count_free} ชิ้น   |   ถูกยืม {count_borrowed} ชิ้น   |   เลยกำหนด {count_late} ชิ้น")


def add_item():
    """เพิ่มของชิ้นใหม่เข้าระบบ"""
    name = name_entry.get().strip()
    if name == "":
        messagebox.showwarning("ข้อมูลผิด", "กรุณากรอกชื่อของ")
        return
    cur.execute("INSERT INTO items (name) VALUES (?)", (name,))
    conn.commit()
    name_entry.delete(0, tk.END)
    load_data()


def delete_item():
    """ลบของออกจากระบบ (ห้ามลบถ้ายังถูกยืมอยู่)"""
    row = get_selected()
    if row is None:
        return
    item_id, name, status = row[0], row[1], row[2]
    if status != "ว่าง":
        messagebox.showwarning("ลบไม่ได้", f"'{name}' ยังถูกยืมอยู่ ต้องคืนก่อนจึงจะลบได้")
        return
    if messagebox.askyesno("ยืนยัน", f"ต้องการลบ '{name}' ใช่ไหม?"):
        cur.execute("DELETE FROM items WHERE id=?", (item_id,))
        conn.commit()
        load_data()


def borrow_item():
    """บันทึกการยืม: ใส่ชื่อผู้ยืม วันที่ยืม และวันกำหนดคืน"""
    row = get_selected()
    if row is None:
        return
    item_id, name, status = row[0], row[1], row[2]
    if status != "ว่าง":
        messagebox.showwarning("ยืมไม่ได้", f"'{name}' ถูกยืมไปแล้ว")
        return

    borrower = borrower_entry.get().strip()
    if borrower == "":
        messagebox.showwarning("ข้อมูลผิด", "กรุณากรอกชื่อผู้ยืม")
        return

    try:
        days = int(days_entry.get())
    except ValueError:
        messagebox.showwarning("ข้อมูลผิด", "จำนวนวันต้องเป็นตัวเลขจำนวนเต็ม")
        return
    if days < 1:
        messagebox.showwarning("ข้อมูลผิด", "จำนวนวันต้องอย่างน้อย 1 วัน")
        return

    today = date.today()
    due = today + timedelta(days=days)      # วันนี้ + จำนวนวันที่ให้ยืม

    cur.execute("UPDATE items SET borrower=?, borrow_date=?, due_date=? WHERE id=?",
                (borrower, str(today), str(due), item_id))
    conn.commit()
    borrower_entry.delete(0, tk.END)
    load_data()
    messagebox.showinfo("สำเร็จ", f"{borrower} ยืม '{name}'\nกำหนดคืน: {due}")


def return_item():
    """บันทึกการคืน: ล้างข้อมูลผู้ยืมออก ของกลับมาเป็น 'ว่าง'"""
    row = get_selected()
    if row is None:
        return
    item_id, name, status, borrower = row[0], row[1], row[2], row[3]
    if status == "ว่าง":
        messagebox.showinfo("แจ้งเตือน", f"'{name}' ไม่ได้ถูกยืมอยู่")
        return
    cur.execute("UPDATE items SET borrower='', borrow_date='', due_date='' WHERE id=?",
                (item_id,))
    conn.commit()
    load_data()
    messagebox.showinfo("สำเร็จ", f"{borrower} คืน '{name}' เรียบร้อย")


# ---------- ส่วนที่ 4: สร้างหน้าต่าง (GUI) ----------

root = tk.Tk()
root.title("ระบบยืม-คืน ของห้องเรียน")
root.geometry("800x600")

style = ttk.Style()
style.theme_use("clam")

tk.Label(root, text="📚 ระบบยืม-คืน หนังสือ/อุปกรณ์ ห้องเรียน",
         font=("Helvetica", 18, "bold")).pack(pady=10)

# --- กรอบเพิ่มของ ---
add_frame = tk.LabelFrame(root, text="เพิ่มของเข้าระบบ", padx=10, pady=8)
add_frame.pack(fill="x", padx=15)
tk.Label(add_frame, text="ชื่อของ:").pack(side="left")
name_entry = tk.Entry(add_frame, width=30)
name_entry.pack(side="left", padx=5)
tk.Button(add_frame, text="➕ เพิ่ม", command=add_item).pack(side="left", padx=5)
tk.Button(add_frame, text="🗑 ลบของที่เลือก", command=delete_item).pack(side="left", padx=5)

# --- กรอบยืม/คืน ---
borrow_frame = tk.LabelFrame(root, text="ยืม / คืน (เลือกของในตารางก่อน)", padx=10, pady=8)
borrow_frame.pack(fill="x", padx=15, pady=8)
tk.Label(borrow_frame, text="ชื่อผู้ยืม:").pack(side="left")
borrower_entry = tk.Entry(borrow_frame, width=20)
borrower_entry.pack(side="left", padx=5)
tk.Label(borrow_frame, text="ยืมกี่วัน:").pack(side="left")
days_entry = tk.Entry(borrow_frame, width=5)
days_entry.insert(0, "7")
days_entry.pack(side="left", padx=5)
tk.Button(borrow_frame, text="📤 ยืม", command=borrow_item).pack(side="left", padx=5)
tk.Button(borrow_frame, text="📥 คืน", command=return_item).pack(side="left", padx=5)

# --- ค้นหา ---
search_frame = tk.Frame(root)
search_frame.pack()
tk.Label(search_frame, text="🔍 ค้นหา (ชื่อของ/ผู้ยืม):").pack(side="left")
search_entry = tk.Entry(search_frame, width=25)
search_entry.pack(side="left", padx=5)
search_entry.bind("<KeyRelease>", lambda event: load_data())

# --- ตาราง ---
columns = ("id", "name", "status", "borrower", "borrow_date", "due_date")
table = ttk.Treeview(root, columns=columns, show="headings", height=12)
headings = ["รหัส", "ชื่อของ", "สถานะ", "ผู้ยืม", "วันที่ยืม", "กำหนดคืน"]
widths = [50, 220, 90, 140, 100, 100]
for i in range(len(columns)):
    table.heading(columns[i], text=headings[i])
    table.column(columns[i], width=widths[i], anchor="center")
table.tag_configure("ว่าง", background="#e3f6e3")       # เขียว
table.tag_configure("ถูกยืม", background="#fff5d6")     # เหลือง
table.tag_configure("เลยกำหนด", background="#fbd4d4")   # แดง
table.pack(fill="both", expand=True, padx=15, pady=8)

summary_label = tk.Label(root, text="", font=("Helvetica", 13, "bold"))
summary_label.pack(pady=5)

load_data()
root.mainloop()
conn.close()
