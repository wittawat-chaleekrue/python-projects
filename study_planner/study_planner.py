# โปรแกรมวางแผนอ่านหนังสือสอบ (Study Planner)
# ผู้พัฒนา: วิทวัส ชาลีเครือ

import tkinter as tk
from tkinter import messagebox
from datetime import date, datetime
import json
import os

FILE_NAME = "plans.json"   # ชื่อไฟล์ที่ใช้เก็บแผนการอ่าน


# ---------- ส่วนที่ 1: อ่าน/บันทึกไฟล์ ----------

def load_plans():
    if os.path.exists(FILE_NAME):
        with open(FILE_NAME, "r", encoding="utf-8") as f:
            return json.load(f)
    return []


def save_plans():
    with open(FILE_NAME, "w", encoding="utf-8") as f:
        json.dump(plans, f, ensure_ascii=False, indent=2)


plans = load_plans()   # รายการแผนการอ่านทั้งหมด


# ---------- ส่วนที่ 2: คำนวณวันที่ ----------

def days_left(exam_date_text):
    # แปลงข้อความ "2026-11-20" ให้เป็นวันที่ แล้วลบกับวันนี้
    exam_date = datetime.strptime(exam_date_text, "%Y-%m-%d").date()
    return (exam_date - date.today()).days


# ---------- ส่วนที่ 3: ฟังก์ชันที่ทำงานเมื่อกดปุ่ม ----------

def add_plan():
    subject = entry_subject.get().strip()
    exam_text = entry_date.get().strip()
    chapters_text = entry_chapters.get().strip()

    if subject == "":
        messagebox.showwarning("แจ้งเตือน", "กรุณากรอกชื่อวิชา")
        return

    try:
        chapters = int(chapters_text)
    except ValueError:
        messagebox.showwarning("แจ้งเตือน", "จำนวนบทต้องเป็นตัวเลข เช่น 8")
        return

    try:
        left = days_left(exam_text)
    except ValueError:
        messagebox.showwarning("แจ้งเตือน", "วันที่ต้องเขียนแบบ ปี-เดือน-วัน เช่น 2026-11-20")
        return

    if left < 0:
        messagebox.showwarning("แจ้งเตือน", "วันสอบผ่านไปแล้ว")
        return

    new_plan = {"subject": subject, "exam_date": exam_text, "chapters": chapters, "done_days": []}
    plans.append(new_plan)
    save_plans()

    entry_subject.delete(0, tk.END)
    entry_date.delete(0, tk.END)
    entry_chapters.delete(0, tk.END)
    refresh_list()


def refresh_list():
    listbox.delete(0, tk.END)
    today = str(date.today())

    for plan in plans:
        left = days_left(plan["exam_date"])

        if left > 0:
            per_day = round(plan["chapters"] / left, 1)
            text = f"{plan['subject']} | สอบอีก {left} วัน | ควรอ่านวันละ {per_day} บท"
        elif left == 0:
            text = f"{plan['subject']} | สอบวันนี้! สู้ๆ"
        else:
            text = f"{plan['subject']} | สอบไปแล้ว"

        text = text + f" | อ่านแล้ว {len(plan['done_days'])} วัน"
        if today in plan["done_days"]:
            text = text + " ✓"

        listbox.insert(tk.END, text)


def mark_done():
    selected = listbox.curselection()
    if len(selected) == 0:
        messagebox.showwarning("แจ้งเตือน", "กรุณาคลิกเลือกวิชาในรายการก่อน")
        return

    index = selected[0]
    plan = plans[index]
    today = str(date.today())

    if today in plan["done_days"]:
        messagebox.showinfo("แจ้งเตือน", "วันนี้ติ๊กวิชานี้ไปแล้ว")
        return

    plan["done_days"].append(today)
    save_plans()
    refresh_list()


def delete_plan():
    selected = listbox.curselection()
    if len(selected) == 0:
        messagebox.showwarning("แจ้งเตือน", "กรุณาคลิกเลือกวิชาในรายการก่อน")
        return

    index = selected[0]
    sure = messagebox.askyesno("ยืนยัน", f"ลบวิชา {plans[index]['subject']} ใช่ไหม?")
    if sure:
        plans.pop(index)
        save_plans()
        refresh_list()


# ---------- ส่วนที่ 4: สร้างหน้าต่างโปรแกรม ----------

window = tk.Tk()
window.title("Study Planner - วางแผนอ่านหนังสือ")
window.geometry("520x520")

frame_add = tk.LabelFrame(window, text="เพิ่มวิชาที่จะสอบ", padx=10, pady=10)
frame_add.pack(fill="x", padx=10, pady=10)

tk.Label(frame_add, text="ชื่อวิชา").pack(anchor="w")
entry_subject = tk.Entry(frame_add)
entry_subject.pack(fill="x")

tk.Label(frame_add, text="วันสอบ (ปี-เดือน-วัน เช่น 2026-11-20)").pack(anchor="w")
entry_date = tk.Entry(frame_add)
entry_date.pack(fill="x")

tk.Label(frame_add, text="จำนวนบทที่ต้องอ่าน").pack(anchor="w")
entry_chapters = tk.Entry(frame_add)
entry_chapters.pack(fill="x")

tk.Button(frame_add, text="เพิ่มวิชา", command=add_plan).pack(pady=5)

listbox = tk.Listbox(window, height=10)
listbox.pack(fill="both", expand=True, padx=10)

frame_buttons = tk.Frame(window)
frame_buttons.pack(pady=10)
tk.Button(frame_buttons, text="วันนี้อ่านแล้ว ✓", command=mark_done).pack(side="left", padx=5)
tk.Button(frame_buttons, text="ลบวิชา", command=delete_plan).pack(side="left", padx=5)

refresh_list()   # แสดงแผนที่เคยบันทึกไว้ตอนเปิดโปรแกรม
window.mainloop()
