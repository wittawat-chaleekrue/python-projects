# โปรแกรมแผนผังเครือญาติ (Tree + Recursion = ฟังก์ชันที่เรียกตัวเอง)
# ผู้พัฒนา: วิทวัส ชาลีเครือ
# แนวคิด: ครอบครัวเป็นโครงสร้างต้นไม้ คนหนึ่งมีลูกได้หลายคน ลูกก็มีลูกต่อไปได้อีก

import tkinter as tk
from tkinter import ttk, messagebox

ROOT = "ทวด"   # คนบนสุดของแผนผัง (ราก ของต้นไม้)

# dict: ชื่อ → [รายชื่อลูก]  (ทุกคนต้องมีชื่ออยู่ใน dict แม้ยังไม่มีลูก)
children = {
    "ทวด": ["ปู่", "ปู่รอง"],
    "ปู่": ["ลุง", "พ่อ", "อา"],
    "ปู่รอง": ["น้าแก้ว"],
    "ลุง": ["พี่ต้น", "พี่ฝน"],
    "พ่อ": ["ฉัน", "น้องมิว"],
    "อา": [],
    "น้าแก้ว": ["น้องเก่ง"],
    "พี่ต้น": [],
    "พี่ฝน": [],
    "ฉัน": [],
    "น้องมิว": [],
    "น้องเก่ง": [],
}


# ---------- ส่วนที่ 1: ฟังก์ชัน Recursion ทั้ง 3 ตัว ----------

def show_tree(name, parent_item):
    # ใส่ชื่อนี้ลงแผนผัง แล้ว "เรียกตัวเอง" ให้ใส่ลูกทุกคนต่อไว้ใต้ชื่อนี้
    item = tree.insert(parent_item, "end", text=name, open=True)
    for child in children[name]:
        show_tree(child, item)


def count_descendants(name):
    # นับลูกหลานทั้งหมด = ลูกแต่ละคน (1) + ลูกหลานของลูกคนนั้น
    total = 0
    for child in children[name]:
        total = total + 1 + count_descendants(child)
    return total            # ถ้าไม่มีลูก loop ไม่ทำงาน ได้ 0 = จุดหยุด


def find_parent(name):
    # หาว่าใครมีชื่อนี้อยู่ในรายชื่อลูก (ไม่ใช่ recursion เป็นตัวช่วย)
    for person in children:
        if name in children[person]:
            return person
    return None


def ancestors(name):
    # ไล่สายขึ้นไปหาบรรพบุรุษ: ฉัน → พ่อ → ปู่ → ทวด
    parent = find_parent(name)
    if parent is None:
        return [name]                      # จุดหยุด: ถึงคนบนสุดแล้ว
    return [name] + ancestors(parent)      # ตัวเอง + สายของพ่อ/แม่


# ---------- ส่วนที่ 2: ฟังก์ชันของปุ่ม ----------

def get_selected():
    item = tree.focus()          # แถวที่ถูกคลิกเลือกอยู่
    if item == "":
        messagebox.showwarning("แจ้งเตือน", "กรุณาคลิกเลือกชื่อในแผนผังก่อน")
        return None
    return tree.item(item, "text")


def refresh_tree():
    for item in tree.get_children():   # ลบแผนผังเก่าทั้งหมด
        tree.delete(item)
    show_tree(ROOT, "")                # "" = ใส่ไว้ชั้นบนสุด


def on_count():
    name = get_selected()
    if name is not None:
        n = count_descendants(name)
        label_result.config(text=f"👨‍👩‍👧 {name} มีลูกหลานทั้งหมด {n} คน")


def on_ancestors():
    name = get_selected()
    if name is not None:
        line = ancestors(name)
        label_result.config(text="🌳 สายบรรพบุรุษ:\n" + " → ".join(line))


def on_add_child():
    parent = get_selected()
    new_name = entry_name.get().strip()
    if parent is None:
        return
    if new_name == "":
        messagebox.showwarning("แจ้งเตือน", "กรุณาพิมพ์ชื่อลูกที่จะเพิ่ม")
        return
    if new_name in children:
        messagebox.showwarning("แจ้งเตือน", f"มีชื่อ {new_name} อยู่ในแผนผังแล้ว")
        return
    children[parent].append(new_name)   # เพิ่มเป็นลูกของคนที่เลือก
    children[new_name] = []             # คนใหม่ยังไม่มีลูก
    entry_name.delete(0, tk.END)
    refresh_tree()
    label_result.config(text=f"เพิ่ม {new_name} เป็นลูกของ {parent} แล้ว")


# ---------- ส่วนที่ 3: สร้างหน้าต่างโปรแกรม ----------

window = tk.Tk()
window.title("แผนผังเครือญาติ")
window.geometry("640x460")

tree = ttk.Treeview(window, show="tree")   # show="tree" = โชว์เฉพาะต้นไม้ ไม่มีหัวตาราง
tree.pack(side="left", fill="both", expand=True, padx=10, pady=10)

frame_right = tk.Frame(window, padx=10, pady=10)
frame_right.pack(side="left", fill="y")
tk.Label(frame_right, text="คลิกชื่อในแผนผังก่อน\nแล้วกดปุ่ม", fg="gray").pack(pady=5)
tk.Button(frame_right, text="นับลูกหลาน", width=18, command=on_count).pack(pady=3)
tk.Button(frame_right, text="ดูสายบรรพบุรุษ", width=18, command=on_ancestors).pack(pady=3)

tk.Label(frame_right, text="ชื่อลูกที่จะเพิ่ม").pack(anchor="w", pady=(20, 0))
entry_name = tk.Entry(frame_right, width=20)
entry_name.pack()
tk.Button(frame_right, text="➕ เพิ่มเป็นลูกของคนที่เลือก", command=on_add_child).pack(pady=5)

label_result = tk.Label(frame_right, text="", font=("Arial", 13), wraplength=220, justify="left")
label_result.pack(pady=20)

refresh_tree()
window.mainloop()
