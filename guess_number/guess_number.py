# ==========================================================
# เกมทายตัวเลข (Number Guessing Game)
# ผู้พัฒนา: วิทวัส ชาลีเครือ
# ภาษา: Python + tkinter
# ==========================================================

import tkinter as tk      # เครื่องมือสร้างหน้าต่างโปรแกรม (GUI)
import random             # เครื่องมือสุ่มตัวเลข

# ---------- ข้อมูลตั้งต้น ----------

MIN_NUMBER = 1
MAX_NUMBER = 100
MAX_TRIES = 7       # 7 ครั้งพอเสมอ ถ้าใช้วิธี "แบ่งครึ่ง" (ดู EXPLAIN.md)

# ตัวแปรที่เปลี่ยนไประหว่างเล่น (สถานะของเกม)
secret = 0          # เลขลับที่โปรแกรมสุ่มไว้
tries = 0           # ทายไปแล้วกี่ครั้ง
low = MIN_NUMBER    # ขอบล่างที่เป็นไปได้ตอนนี้
high = MAX_NUMBER   # ขอบบนที่เป็นไปได้ตอนนี้
game_over = False   # จบเกมหรือยัง


# ---------- ส่วนที่ 1: ตรรกะ (สมองของโปรแกรม) ----------

def check_guess(guess, answer):
    """เทียบเลขที่ทายกับคำตอบ แล้วบอกผล"""
    if guess < answer:
        return "น้อยไป"
    elif guess > answer:
        return "มากไป"
    else:
        return "ถูกต้อง"


# ---------- ส่วนที่ 2: ฟังก์ชันที่ทำงานเมื่อผู้ใช้กดปุ่ม ----------

def update_status():
    """อัปเดตข้อความช่วงตัวเลขและจำนวนครั้งที่เหลือ"""
    range_label.config(text=f"เลขลับอยู่ระหว่าง {low} – {high}")
    tries_label.config(text=f"เหลือโอกาส {MAX_TRIES - tries} ครั้ง")


def new_game():
    """เริ่มเกมใหม่: สุ่มเลขลับและรีเซ็ตทุกอย่าง"""
    global secret, tries, low, high, game_over
    secret = random.randint(MIN_NUMBER, MAX_NUMBER)
    tries = 0
    low = MIN_NUMBER
    high = MAX_NUMBER
    game_over = False

    history_listbox.delete(0, tk.END)
    message_label.config(text="ผมคิดเลขไว้แล้ว ลองทายดู!", fg="black")
    guess_entry.delete(0, tk.END)
    guess_entry.focus()
    update_status()


def on_guess(event=None):
    """กดปุ่ม 'ทาย' (หรือกด Enter)"""
    global tries, low, high, game_over
    if game_over:
        return

    text = guess_entry.get().strip()
    guess_entry.delete(0, tk.END)

    if not text.isdigit():
        message_label.config(text="กรุณาพิมพ์ตัวเลขเท่านั้น", fg="red")
        return

    guess = int(text)
    if guess < low or guess > high:
        message_label.config(text=f"ลองเลขระหว่าง {low} – {high} สิ (ไม่นับครั้งนี้)", fg="red")
        return

    tries = tries + 1
    result = check_guess(guess, secret)
    history_listbox.insert(tk.END, f"ครั้งที่ {tries}:  {guess}  →  {result}")

    if result == "ถูกต้อง":
        message_label.config(text=f"🎉 ถูกต้อง! เลขลับคือ {secret} ใช้ไป {tries} ครั้ง", fg="green")
        game_over = True
        return

    if result == "น้อยไป":
        low = guess + 1
    else:
        high = guess - 1

    if tries >= MAX_TRIES:
        message_label.config(text=f"😢 หมดโอกาสแล้ว เลขลับคือ {secret}", fg="red")
        game_over = True
    else:
        message_label.config(text=f"{guess} {result}", fg="orange")
    update_status()


# ---------- ส่วนที่ 3: สร้างหน้าต่าง (GUI) ----------

root = tk.Tk()
root.title("เกมทายตัวเลข")
root.geometry("380x520")
root.resizable(False, False)

tk.Label(root, text="🔢 เกมทายตัวเลข 1–100",
         font=("Helvetica", 18, "bold")).pack(pady=15)

range_label = tk.Label(root, text="", font=("Helvetica", 14))
range_label.pack()

tries_label = tk.Label(root, text="")
tries_label.pack()

guess_entry = tk.Entry(root, width=8, font=("Helvetica", 20), justify="center")
guess_entry.pack(pady=10)

button_frame = tk.Frame(root)
button_frame.pack()
tk.Button(button_frame, text="ทาย", command=on_guess).pack(side="left", padx=5)
tk.Button(button_frame, text="เล่นใหม่", command=new_game).pack(side="left", padx=5)

message_label = tk.Label(root, text="", font=("Helvetica", 14, "bold"))
message_label.pack(pady=10)

history_listbox = tk.Listbox(root, width=30, height=8)
history_listbox.pack(pady=5)

root.bind("<Return>", on_guess)
new_game()          # เริ่มเกมแรกทันทีที่เปิดโปรแกรม

root.mainloop()
