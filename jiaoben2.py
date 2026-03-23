import tkinter as tk
from tkinter import filedialog, messagebox
from PIL import Image
import os
import hashlib

# 结束标记
END_MARK = b"<<<END>>>"

# ===== 密码处理（生成固定长度密钥） =====
def derive_key(password: str) -> bytes:
    return hashlib.sha256(password.encode('utf-8')).digest()

# ===== 简单对称加密（XOR） =====
def xor_encrypt(data: bytes, key: bytes) -> bytes:
    return bytes([data[i] ^ key[i % len(key)] for i in range(len(data))])

# ===== 编码 =====
def text_to_bits(text: str, password: str) -> str:
    raw = text.encode('utf-8') + END_MARK
    key = derive_key(password)
    encrypted = xor_encrypt(raw, key)
    return ''.join(f'{b:08b}' for b in encrypted)

# ===== 解码 =====
def bits_to_text(bits: str, password: str) -> str:
    data = bytearray()

    for i in range(0, len(bits), 8):
        byte = bits[i:i+8]
        if len(byte) < 8:
            break
        data.append(int(byte, 2))

    key = derive_key(password)
    decrypted = xor_encrypt(bytes(data), key)

    if END_MARK in decrypted:
        content = decrypted.split(END_MARK)[0]
        try:
            return content.decode('utf-8')
        except:
            return content.decode('utf-8', errors='ignore')
    else:
        return "密码错误或无隐藏数据"

# ===== 自动转PNG =====
def convert_to_png(input_path):
    img = Image.open(input_path)
    img = img.convert('RGB')
    base, _ = os.path.splitext(input_path)
    temp_path = base + "_temp.png"
    img.save(temp_path)
    return temp_path

# ===== 容量 =====
def capacity_bytes(img):
    w, h = img.size
    return (w * h * 3) // 8

# ===== 加密 =====
def encode_image(input_path, text, password, output_path):
    if not input_path.lower().endswith('.png'):
        input_path = convert_to_png(input_path)

    img = Image.open(input_path).convert('RGB')

    bitstream = text_to_bits(text, password)

    if (len(bitstream) // 8) > capacity_bytes(img):
        raise ValueError("图片太小，装不下这么多内容！")

    data = list(img.getdata())
    new_data = []
    bit_idx = 0

    for (r, g, b) in data:
        if bit_idx < len(bitstream):
            r = (r & ~1) | int(bitstream[bit_idx]); bit_idx += 1
        if bit_idx < len(bitstream):
            g = (g & ~1) | int(bitstream[bit_idx]); bit_idx += 1
        if bit_idx < len(bitstream):
            b = (b & ~1) | int(bitstream[bit_idx]); bit_idx += 1
        new_data.append((r, g, b))

    img.putdata(new_data)

    if not output_path.lower().endswith('.png'):
        output_path += '.png'

    img.save(output_path)

# ===== 解密 =====
def decode_image(image_path, password):
    if not image_path.lower().endswith('.png'):
        image_path = convert_to_png(image_path)

    img = Image.open(image_path).convert('RGB')
    data = list(img.getdata())

    bits = []
    for (r, g, b) in data:
        bits.append(str(r & 1))
        bits.append(str(g & 1))
        bits.append(str(b & 1))

    bitstream = ''.join(bits)
    return bits_to_text(bitstream, password)

# ===== GUI =====

def select_input():
    path = filedialog.askopenfilename()
    input_entry.delete(0, tk.END)
    input_entry.insert(0, path)


def select_output():
    path = filedialog.asksaveasfilename(defaultextension='.png')
    output_entry.delete(0, tk.END)
    output_entry.insert(0, path)


def encode_action():
    try:
        encode_image(input_entry.get(), text_entry.get(), pwd_entry.get(), output_entry.get())
        messagebox.showinfo('成功', '加密完成（需密码解密）')
    except Exception as e:
        messagebox.showerror('错误', str(e))


def decode_action():
    try:
        result = decode_image(input_entry.get(), pwd_entry.get())
        messagebox.showinfo('解密结果', result)
    except Exception as e:
        messagebox.showerror('错误', str(e))


root = tk.Tk()
root.title('LSB隐写工具（密码版）')
root.geometry('520x360')

# 输入

tk.Label(root, text='输入图片:').pack()
input_entry = tk.Entry(root, width=60)
input_entry.pack()
tk.Button(root, text='选择图片', command=select_input).pack()

# 输出

tk.Label(root, text='输出图片:').pack()
output_entry = tk.Entry(root, width=60)
output_entry.pack()
tk.Button(root, text='保存路径', command=select_output).pack()

# 文本

tk.Label(root, text='隐藏内容:').pack()
text_entry = tk.Entry(root, width=60)
text_entry.pack()

# 密码

tk.Label(root, text='密码:').pack()
pwd_entry = tk.Entry(root, width=60, show='*')
pwd_entry.pack()

# 按钮

tk.Button(root, text='加密（需密码）', command=encode_action).pack(pady=6)
tk.Button(root, text='解密（需密码）', command=decode_action).pack(pady=6)

# ===== 批量处理 =====
def batch_encode_action():
    try:
        files = filedialog.askopenfilenames(title='选择多张图片')
        if not files:
            return
        out_dir = filedialog.askdirectory(title='选择输出文件夹')
        if not out_dir:
            return
        text = text_entry.get()
        pwd = pwd_entry.get()
        count = 0
        for path in files:
            name = os.path.splitext(os.path.basename(path))[0]
            out_path = os.path.join(out_dir, f"{name}_encoded.png")
            encode_image(path, text, pwd, out_path)
            count += 1
        messagebox.showinfo('完成', f'批量处理完成，共处理 {count} 张图片')
    except Exception as e:
        messagebox.showerror('错误', str(e))

# 批量按钮

tk.Button(root, text='批量加密（多图）', command=batch_encode_action).pack(pady=6)

root.mainloop()
