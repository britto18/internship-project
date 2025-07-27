from tkinter import *
from tkinter import filedialog, messagebox
from PIL import Image
import os

# Function to encode text into image
def encode_text():
    file_path = filedialog.askopenfilename(title="Select Image", filetypes=[("Image Files", "*.png *.bmp")])
    if not file_path:
        return

    message = text_entry.get("1.0", END).strip()
    if not message:
        messagebox.showerror("Error", "No message to hide!")
        return

    image = Image.open(file_path)
    encoded_image = image.copy()
    width, height = image.size
    binary_message = ''.join(format(ord(char), '08b') for char in message) + '1111111111111110'  # EOF marker

    pixels = encoded_image.load()
    idx = 0

    for y in range(height):
        for x in range(width):
            if idx < len(binary_message):
                r, g, b, *rest = pixels[x, y]
                r = (r & ~1) | int(binary_message[idx])
                idx += 1
                if idx < len(binary_message):
                    g = (g & ~1) | int(binary_message[idx])
                    idx += 1
                if idx < len(binary_message):
                    b = (b & ~1) | int(binary_message[idx])
                    idx += 1
                pixels[x, y] = (r, g, b)

    save_path = filedialog.asksaveasfilename(defaultextension=".png", filetypes=[("PNG Image", "*.png")])
    if save_path:
        encoded_image.save(save_path)
        messagebox.showinfo("Success", f"Message hidden and saved to:\n{save_path}")

# Function to decode text from image
def decode_text():
    file_path = filedialog.askopenfilename(title="Select Image", filetypes=[("Image Files", "*.png *.bmp")])
    if not file_path:
        return

    image = Image.open(file_path)
    pixels = image.load()
    width, height = image.size
    binary_data = ""
    for y in range(height):
        for x in range(width):
            r, g, b, *rest = pixels[x, y]
            binary_data += str(r & 1)
            binary_data += str(g & 1)
            binary_data += str(b & 1)

    # Split binary into 8-bit chunks and convert to characters
    chars = []
    for i in range(0, len(binary_data), 8):
        byte = binary_data[i:i+8]
        if byte == '11111111':  # EOF marker
            break
        chars.append(chr(int(byte, 2)))

    hidden_message = ''.join(chars)
    if hidden_message:
        text_entry.delete("1.0", END)
        text_entry.insert(END, hidden_message)
        messagebox.showinfo("Decoded", "Hidden message extracted successfully!")
    else:
        messagebox.showwarning("Warning", "No hidden message found.")

# GUI Setup
root = Tk()
root.title("Steganography Tool - LSB")
root.geometry("500x400")

Label(root, text="Steganography Tool", font=("Arial", 16, "bold")).pack(pady=10)

text_entry = Text(root, wrap=WORD, width=60, height=10)
text_entry.pack(pady=10)

Button(root, text="Hide Message in Image", command=encode_text, bg="green", fg="white").pack(pady=5)
Button(root, text="Extract Message from Image", command=decode_text, bg="blue", fg="white").pack(pady=5)

root.mainloop()
