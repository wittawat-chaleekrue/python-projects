# โปรแกรมจับเวลาอ่านหนังสือแบบ Pomodoro
# ผู้พัฒนา: วิทวัส ชาลีเครือ
# แนวคิด: อ่าน 25 นาที พัก 5 นาที สลับกันไปเรื่อย ๆ

import tkinter as tk
from tkinter import messagebox

WORK_MINUTES = 25    # เวลาอ่านหนังสือ (นาที)  ** ตอนทดสอบเปลี่ยนเป็น 1 ได้ **
BREAK_MINUTES = 5    # เวลาพัก (นาที)

seconds_left = WORK_MINUTES * 60   # วินาทีที่เหลือ (25 นาที = 1500 วินาที)
is_running = False                 # นาฬิกากำลังเดินอยู่ไหม
is_work_time = True                # True = ช่วงอ่าน, False = ช่วงพัก
rounds_done = 0                    # วันนี้อ่านครบไปกี่รอบแล้ว
timer_id = None                    # เลขบัตรคิวที่ after() ให้มา (เอาไว้ยกเลิก)


# ---------- ส่วนที่ 1: แสดงผลบนหน้าจอ ----------

def show_time():
    minutes = seconds_left // 60   # หารปัดเศษทิ้ง = ได้กี่นาทีเต็ม
    seconds = seconds_left % 60    # หารเอาเศษ = เหลือกี่วินาที
    label_time.config(text=f"{minutes:02d}:{seconds:02d}")

    if is_work_time:
        label_mode.config(text="📖 ช่วงอ่านหนังสือ", fg="red")
    else:
        label_mode.config(text="☕ ช่วงพัก", fg="green")

    label_rounds.config(text=f"วันนี้อ่านครบ {rounds_done} รอบ ({rounds_done * WORK_MINUTES} นาที)")


# ---------- ส่วนที่ 2: หัวใจของโปรแกรม (นับถอยหลังทีละ 1 วินาที) ----------

def tick():
    global seconds_left, is_work_time, rounds_done, timer_id

    if seconds_left > 0:
        seconds_left = seconds_left - 1
    else:
        # หมดเวลาแล้ว → สลับช่วง อ่าน ↔ พัก
        window.bell()   # เสียงเตือน
        if is_work_time:
            rounds_done = rounds_done + 1
            is_work_time = False
            seconds_left = BREAK_MINUTES * 60
            messagebox.showinfo("หมดเวลาอ่าน", "เก่งมาก! ลุกไปพักสายตา 5 นาทีนะ")
        else:
            is_work_time = True
            seconds_left = WORK_MINUTES * 60
            messagebox.showinfo("หมดเวลาพัก", "กลับมาอ่านต่อกันเถอะ สู้ ๆ")

    show_time()
    # ฝากงานไว้: อีก 1000 มิลลิวินาที (= 1 วินาที) ให้เรียก tick อีกครั้ง
    timer_id = window.after(1000, tick)


# ---------- ส่วนที่ 3: ฟังก์ชันของปุ่ม ----------

def start():
    global is_running, timer_id
    if is_running:
        return   # กันกดซ้ำ ถ้ากด 2 ครั้งนาฬิกาจะเดินเร็วขึ้น 2 เท่า
    is_running = True
    timer_id = window.after(1000, tick)


def pause():
    global is_running
    if is_running:
        window.after_cancel(timer_id)   # ยกเลิกงานที่ฝากไว้ นาฬิกาจึงหยุด
        is_running = False


def reset():
    global seconds_left, is_work_time
    pause()
    is_work_time = True
    seconds_left = WORK_MINUTES * 60
    show_time()


# ---------- ส่วนที่ 4: สร้างหน้าต่างโปรแกรม ----------

window = tk.Tk()
window.title("Pomodoro - จับเวลาอ่านหนังสือ")
window.geometry("380x320")

label_mode = tk.Label(window, font=("Arial", 18))
label_mode.pack(pady=10)

label_time = tk.Label(window, font=("Arial", 64, "bold"))
label_time.pack()

label_rounds = tk.Label(window, font=("Arial", 14))
label_rounds.pack(pady=10)

frame_buttons = tk.Frame(window)
frame_buttons.pack(pady=10)
tk.Button(frame_buttons, text="▶ เริ่ม", width=8, command=start).pack(side="left", padx=5)
tk.Button(frame_buttons, text="⏸ หยุด", width=8, command=pause).pack(side="left", padx=5)
tk.Button(frame_buttons, text="↺ เริ่มใหม่", width=8, command=reset).pack(side="left", padx=5)

show_time()        # แสดง 25:00 ตั้งแต่เปิดโปรแกรม
window.mainloop()  # วงรอบรอเหตุการณ์ (event loop) เริ่มทำงานตรงนี้
