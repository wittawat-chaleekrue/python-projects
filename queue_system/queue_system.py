# โปรแกรมระบบบัตรคิวร้านค้า/คลินิกในชุมชน (Queue System)
# ผู้พัฒนา: วิทวัส ชาลีเครือ

import tkinter as tk
from tkinter import messagebox

MINUTES_PER_PERSON = 5   # เวลาบริการเฉลี่ยต่อ 1 คน (นาที)

waiting = []       # รายการเลขคิวที่กำลังรอ (คนแรกอยู่หน้าสุด)
next_number = 1    # เลขคิวที่จะออกให้คนถัดไป


# ---------- ฟังก์ชันที่ทำงานเมื่อกดปุ่ม ----------

def take_ticket():
    global next_number

    waiting.append(next_number)   # ต่อท้ายแถว
    messagebox.showinfo("บัตรคิว", f"คุณได้คิวที่ {next_number}")
    next_number = next_number + 1
    update_screen()


def call_next():
    if len(waiting) == 0:
        messagebox.showinfo("แจ้งเตือน", "ไม่มีคิวรออยู่")
        return

    number = waiting.pop(0)       # ดึงคนหน้าสุดออกจากแถว
    label_now.config(text=f"เชิญคิวที่ {number}")
    update_screen()


def reset_queue():
    global next_number

    sure = messagebox.askyesno("ยืนยัน", "ต้องการล้างคิวทั้งหมด เริ่มใหม่ที่คิว 1 ใช่ไหม?")
    if sure:
        waiting.clear()
        next_number = 1
        label_now.config(text="ยังไม่มีการเรียกคิว")
        update_screen()


def update_screen():
    # ล้างรายการเดิม แล้ววาดใหม่ทั้งหมด
    listbox.delete(0, tk.END)

    position = 1
    for number in waiting:
        wait_time = position * MINUTES_PER_PERSON
        listbox.insert(tk.END, f"ลำดับที่ {position}: คิว {number}  (รอประมาณ {wait_time} นาที)")
        position = position + 1

    total_wait = len(waiting) * MINUTES_PER_PERSON
    label_waiting.config(text=f"รออยู่ {len(waiting)} คิว | คนสุดท้ายรอประมาณ {total_wait} นาที")


# ---------- สร้างหน้าต่างโปรแกรม ----------

window = tk.Tk()
window.title("Queue System - ระบบบัตรคิว")
window.geometry("450x480")

label_now = tk.Label(window, text="ยังไม่มีการเรียกคิว", font=("Arial", 26, "bold"), fg="blue")
label_now.pack(pady=20)

frame_buttons = tk.Frame(window)
frame_buttons.pack()
tk.Button(frame_buttons, text="ออกบัตรคิว", width=15, command=take_ticket).pack(side="left", padx=5)
tk.Button(frame_buttons, text="เรียกคิวถัดไป", width=15, command=call_next).pack(side="left", padx=5)

label_waiting = tk.Label(window, text="รออยู่ 0 คิว | คนสุดท้ายรอประมาณ 0 นาที")
label_waiting.pack(pady=10)

listbox = tk.Listbox(window, height=12)
listbox.pack(fill="both", expand=True, padx=10)

tk.Button(window, text="ล้างคิวทั้งหมด", command=reset_queue).pack(pady=10)

window.mainloop()
