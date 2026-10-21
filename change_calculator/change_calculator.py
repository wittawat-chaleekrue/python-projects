# ==========================================================
# โปรแกรมคิดเงินทอนร้านค้า (Change Calculator)
# ผู้พัฒนา: วิทวัส ชาลีเครือ
# ภาษา: Python + tkinter
# ==========================================================

import tkinter as tk      # เครื่องมือสร้างหน้าต่างโปรแกรม (GUI)

# ---------- ข้อมูลตั้งต้น ----------

# ธนบัตรและเหรียญของไทย ต้องเรียงจาก "มากไปน้อย" เท่านั้น
MONEY_TYPES = [1000, 500, 100, 50, 20, 10, 5, 2, 1]


# ---------- ส่วนที่ 1: ตรรกะ (สมองของโปรแกรม) ----------

def calculate_change(change):
    """รับยอดเงินทอน แล้วคืนค่าเป็น list ของ (ชนิดเงิน, จำนวนใบ)"""
    result = []
    for money in MONEY_TYPES:
        count = change // money     # ใช้เงินชนิดนี้ได้กี่ใบ
        change = change % money     # เหลือเงินที่ต้องทอนต่ออีกเท่าไร
        if count > 0:
            result.append((money, count))
    return result


def money_name(money):
    """แปลงตัวเลขเป็นชื่อเรียก เช่น 100 -> 'แบงก์ 100 บาท'"""
    if money >= 20:
        return f"แบงก์ {money} บาท"
    else:
        return f"เหรียญ {money} บาท"


# ---------- ส่วนที่ 2: ฟังก์ชันที่ทำงานเมื่อผู้ใช้กดปุ่ม ----------

def show_message(text, color):
    """แสดงข้อความในกล่องผลลัพธ์ พร้อมสีที่กำหนด"""
    result_label.config(text=text, fg=color)


def on_calculate(event=None):
    """กดปุ่ม 'คิดเงินทอน' (หรือกด Enter)"""
    price_text = price_entry.get().strip()
    paid_text = paid_entry.get().strip()

    # ตรวจว่ากรอกเป็นตัวเลขจริงไหม
    if not price_text.isdigit() or not paid_text.isdigit():
        show_message("กรุณากรอกเป็นตัวเลขจำนวนเต็มเท่านั้น", "red")
        return

    price = int(price_text)
    paid = int(paid_text)

    if paid < price:
        show_message(f"เงินไม่พอ ขาดอีก {price - paid} บาท", "red")
        return

    change = paid - price
    if change == 0:
        show_message("จ่ายพอดี ไม่ต้องทอนเงิน ✔", "green")
        return

    text = f"ต้องทอนทั้งหมด {change} บาท\n\n"
    for money, count in calculate_change(change):
        text = text + f"{money_name(money)}   x {count}\n"
    show_message(text, "black")


def on_clear():
    """กดปุ่ม 'ล้าง' เพื่อเริ่มลูกค้าคนใหม่"""
    price_entry.delete(0, tk.END)
    paid_entry.delete(0, tk.END)
    show_message("", "black")
    price_entry.focus()


# ---------- ส่วนที่ 3: สร้างหน้าต่าง (GUI) ----------

root = tk.Tk()
root.title("คิดเงินทอนร้านค้า")
root.geometry("380x480")
root.resizable(False, False)

tk.Label(root, text="💵 คิดเงินทอนร้านค้า",
         font=("Helvetica", 18, "bold")).pack(pady=15)

tk.Label(root, text="ราคาสินค้า (บาท):").pack()
price_entry = tk.Entry(root, width=15, font=("Helvetica", 16), justify="center")
price_entry.pack(pady=5)

tk.Label(root, text="ลูกค้าจ่ายมา (บาท):").pack()
paid_entry = tk.Entry(root, width=15, font=("Helvetica", 16), justify="center")
paid_entry.pack(pady=5)

button_frame = tk.Frame(root)
button_frame.pack(pady=10)
tk.Button(button_frame, text="คิดเงินทอน",
          command=on_calculate).pack(side="left", padx=5)
tk.Button(button_frame, text="ล้าง", command=on_clear).pack(side="left", padx=5)

result_label = tk.Label(root, text="", font=("Helvetica", 14), justify="left")
result_label.pack(pady=10)

root.bind("<Return>", on_calculate)   # กด Enter = กดปุ่มคิดเงินทอน
price_entry.focus()                   # ให้เคอร์เซอร์อยู่ช่องแรกตั้งแต่เปิด

root.mainloop()
