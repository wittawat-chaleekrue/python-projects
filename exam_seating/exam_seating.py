# โปรแกรมจัดผังที่นั่งสอบ (2D List = ลิสต์ซ้อนลิสต์ แบบตาราง)
# ผู้พัฒนา: วิทวัส ชาลีเครือ
# แนวคิด: ห้องสอบคือตาราง แถว x คอลัมน์ → เก็บเป็น seats[แถว][คอลัมน์]

import tkinter as tk
from tkinter import messagebox
import random

# รายชื่อตัวอย่าง (ชื่อเล่นสมมติ) ผู้ใช้ลบแล้วพิมพ์ชื่อจริงแทนได้ บรรทัดละ 1 คน
sample_names = ["กร", "ขวัญ", "คิม", "งามตา", "จูน", "ชาย", "ญาญ่า", "ดาว",
                "ต้นกล้า", "ทิว", "นิว", "บีม", "ปาล์ม", "ฝน", "พลอย", "ฟ้า"]

seats = []          # ผังที่นั่ง 2D: seats[r][c] = ชื่อคนที่นั่งตรงนั้น
CELL_W = 90         # ความกว้าง 1 โต๊ะบนจอ
CELL_H = 50         # ความสูง 1 โต๊ะบนจอ
TOP = 45            # เว้นที่ด้านบนไว้วาดกระดาน


# ---------- ส่วนที่ 1: สร้างผังที่นั่ง ----------

def is_usable(r, c):
    # โหมดหมากรุก: นั่งเว้นโต๊ะสลับกัน (กันลอกข้อสอบ) ใช้ได้เฉพาะช่องที่ (แถว+คอลัมน์) เป็นเลขคู่
    if checker.get() == 1:
        return (r + c) % 2 == 0
    return True


def make_seats():
    global seats
    rows = int(spin_rows.get())
    cols = int(spin_cols.get())

    # อ่านชื่อจากกล่องข้อความ แยกทีละบรรทัด และตัดบรรทัดว่างทิ้ง
    names = []
    for line in text_names.get("1.0", tk.END).split("\n"):
        if line.strip() != "":
            names.append(line.strip())

    # นับว่ามีโต๊ะที่นั่งได้กี่ตัว
    capacity = 0
    for r in range(rows):
        for c in range(cols):
            if is_usable(r, c):
                capacity = capacity + 1
    if len(names) > capacity:
        messagebox.showwarning("ที่นั่งไม่พอ",
                               f"มีนักเรียน {len(names)} คน แต่มีโต๊ะแค่ {capacity} ตัว")
        return

    random.shuffle(names)   # สลับลำดับรายชื่อแบบสุ่ม

    # สร้างลิสต์ซ้อนลิสต์: วนทีละแถว ในแต่ละแถววนทีละคอลัมน์
    seats = []
    index = 0
    for r in range(rows):
        row = []
        for c in range(cols):
            if is_usable(r, c) and index < len(names):
                row.append(names[index])
                index = index + 1
            elif is_usable(r, c):
                row.append("(ว่าง)")
            else:
                row.append("")        # โต๊ะที่เว้นไว้ ไม่มีคนนั่ง
        seats.append(row)

    draw_seats(-1, -1)
    label_info.config(text=f"จัดแล้ว {len(names)} คน ในห้อง {rows} แถว x {cols} คอลัมน์")


# ---------- ส่วนที่ 2: วาดผัง + ค้นหาที่นั่ง ----------

def draw_seats(find_r, find_c):
    canvas.delete("all")
    canvas.create_rectangle(150, 8, 400, 33, fill="#2c3e50")
    canvas.create_text(275, 20, text="กระดาน / โต๊ะกรรมการคุมสอบ", fill="white")

    for r in range(len(seats)):
        for c in range(len(seats[r])):
            x = 10 + c * CELL_W
            y = TOP + r * CELL_H
            name = seats[r][c]
            if name == "":
                color = "#dddddd"        # โต๊ะที่เว้น สีเทา
            elif r == find_r and c == find_c:
                color = "#f1c40f"        # คนที่ค้นหา สีเหลือง
            else:
                color = "#d6eaf8"
            canvas.create_rectangle(x, y, x + CELL_W - 6, y + CELL_H - 6, fill=color)
            canvas.create_text(x + 42, y + 12, text=f"{r + 1}-{c + 1}", font=("Arial", 9))
            canvas.create_text(x + 42, y + 30, text=name, font=("Arial", 12))


def find_student():
    name = entry_find.get().strip()
    # ค้นหาในตาราง 2 มิติ ต้องใช้ loop ซ้อน loop
    for r in range(len(seats)):
        for c in range(len(seats[r])):
            if seats[r][c] == name:
                draw_seats(r, c)
                label_info.config(text=f"📍 {name} นั่งแถวที่ {r + 1} คอลัมน์ที่ {c + 1}")
                return
    messagebox.showinfo("ไม่พบ", f"ไม่มีชื่อ \"{name}\" ในผังที่นั่ง")


# ---------- ส่วนที่ 3: สร้างหน้าต่างโปรแกรม ----------

window = tk.Tk()
window.title("จัดผังที่นั่งสอบ")
window.geometry("760x520")

frame_left = tk.Frame(window, padx=10, pady=10)
frame_left.pack(side="left", fill="y")
tk.Label(frame_left, text="รายชื่อ (บรรทัดละ 1 คน)").pack(anchor="w")
text_names = tk.Text(frame_left, width=16, height=12, font=("Arial", 12))
text_names.pack()
text_names.insert("1.0", "\n".join(sample_names))

tk.Label(frame_left, text="จำนวนแถว").pack(anchor="w")
spin_rows = tk.Spinbox(frame_left, from_=1, to=8, width=5)
spin_rows.pack(anchor="w")
spin_rows.delete(0, tk.END)
spin_rows.insert(0, "5")
tk.Label(frame_left, text="จำนวนคอลัมน์").pack(anchor="w")
spin_cols = tk.Spinbox(frame_left, from_=1, to=6, width=5)
spin_cols.pack(anchor="w")
spin_cols.delete(0, tk.END)
spin_cols.insert(0, "4")

checker = tk.IntVar(value=0)   # 1 = ติ๊กถูก, 0 = ไม่ติ๊ก
tk.Checkbutton(frame_left, text="นั่งเว้นแบบหมากรุก", variable=checker).pack(anchor="w")
tk.Button(frame_left, text="🎲 สุ่มจัดที่นั่ง", command=make_seats).pack(pady=5, fill="x")

tk.Label(frame_left, text="ค้นหาที่นั่งของ").pack(anchor="w")
entry_find = tk.Entry(frame_left, width=16)
entry_find.pack()
tk.Button(frame_left, text="🔍 ค้นหา", command=find_student).pack(pady=5, fill="x")

frame_right = tk.Frame(window, pady=10)
frame_right.pack(side="left", fill="both", expand=True)
canvas = tk.Canvas(frame_right, width=550, height=450, bg="white")
canvas.pack()
label_info = tk.Label(frame_right, text="กด \"สุ่มจัดที่นั่ง\" เพื่อเริ่ม", font=("Arial", 13))
label_info.pack()

window.mainloop()
