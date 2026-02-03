import tkinter as tk
from tkinter import ttk, messagebox
import json
import re

class MAX7219PatternEditor:
    def __init__(self, root):
        self.root = root
        self.root.title("8x8 MAX7219 Pattern Editor - Draw OR Paste Code ↔ Grid")
        self.root.geometry("540x820")
        self.root.resizable(False, False)

        self.grid = [[0] * 8 for _ in range(8)]
        self.cell_size = 50

        # =============== CANVAS GRID ===============
        self.canvas = tk.Canvas(root, width=400, height=400, bg="white", highlightthickness=2, highlightbackground="black")
        self.canvas.pack(pady=20)

        self.cells = []
        for row in range(8):
            row_cells = []
            for col in range(8):
                x1, y1 = col * self.cell_size, row * self.cell_size
                x2, y2 = x1 + self.cell_size, y1 + self.cell_size
                rect = self.canvas.create_rectangle(x1, y1, x2, y2, fill="white", outline="#ddd")
                text = self.canvas.create_text((x1+x2)//2, (y1+y2)//2, text="", font=("Arial", 16))
                self.canvas.tag_bind(rect, "<Button-1>", lambda e, r=row, c=col: self.toggle(r, c))
                self.canvas.tag_bind(text, "<Button-1>", lambda e, r=row, c=col: self.toggle(r, c))
                row_cells.append((rect, text))
            self.cells.append(row_cells)

        # =============== OUTPUT TEXT ===============
        out_frame = ttk.Frame(root)
        out_frame.pack(pady=10, fill="x", padx=20)
        ttk.Label(out_frame, text="Arduino code (short format):", font=("Courier", 10, "bold")).pack(anchor="w")
        self.output_text = tk.Text(out_frame, height=3, font=("Courier", 11), wrap="none")
        self.output_text.pack(fill="x", pady=5)

        # =============== INPUT BOX (NEW!) ===============
        in_frame = ttk.LabelFrame(root, text="Paste Arduino pattern here to load into grid")
        in_frame.pack(pady=10, fill="x", padx=20)
        self.input_text = tk.Text(in_frame, height=3, font=("Courier", 11), wrap="word")
        self.input_text.pack(fill="x", padx=10, pady=5)
        ttk.Button(in_frame, text="Load from Code → Grid", command=self.load_from_code).pack(pady=5)

        # =============== BUTTONS ===============
        btn_frame = ttk.Frame(root)
        btn_frame.pack(pady=10)
        ttk.Button(btn_frame, text="Copy Code", command=self.copy_code).grid(row=0, column=0, padx=5)
        ttk.Button(btn_frame, text="Clear", command=self.clear_all).grid(row=0, column=1, padx=5)
        ttk.Button(btn_frame, text="Invert", command=self.invert).grid(row=0, column=2, padx=5)
        ttk.Button(btn_frame, text="Save .pat", command=self.save_pattern).grid(row=0, column=3, padx=5)
        ttk.Button(btn_frame, text="Load .pat", command=self.load_pattern).grid(row=0, column=4, padx=5)

        self.update_output()

    def toggle(self, row, col):
        self.grid[row][col] = 1 - self.grid[row][col]
        color = "#ffff00" if self.grid[row][col] else "white"
        self.canvas.itemconfig(self.cells[row][col][0], fill=color)
        self.canvas.itemconfig(self.cells[row][col][1], text="●" if self.grid[row][col] else "")
        self.update_output()

    def update_output(self):
        bytes_list = []
        for row in range(8):
            byte = sum(1 << (7 - col) for col in range(8) if self.grid[row][col])
            bytes_list.append(f"0x{byte:02X}")

        # Trim trailing zeros (exactly like your real sketches)
        while len(bytes_list) > 1 and bytes_list[-1] == "0x00":
            bytes_list.pop()

        code = "{" + ", ".join(bytes_list) + "}"
        self.output_text.delete(1.0, tk.END)
        self.output_text.insert(tk.END, code)

    def load_from_code(self):
        raw = self.input_text.get(1.0, tk.END).strip()
        # Extract hex values with regex
        hex_vals = re.findall(r'0x([0-9A-Fa-f]{2})', raw)
        if not hex_vals:
            messagebox.showerror("Error", "No valid 0x?? values found!")
            return

        self.clear_all()
        for row in range(min(8, len(hex_vals))):
            byte = int(hex_vals[row], 16)
            for col in range(8):
                if byte & (1 << (7 - col)):
                    self.grid[row][col] = 1
                    self.canvas.itemconfig(self.cells[row][col][0], fill="#ffff00")
                    self.canvas.itemconfig(self.cells[row][col][1], text="●")
        self.update_output()
        messagebox.showinfo("Loaded!", "Pattern loaded into grid!")

    def copy_code(self):
        self.root.clipboard_clear()
        self.root.clipboard_append(self.output_text.get(1.0, tk.END).strip())
        messagebox.showinfo("Copied!", "Code copied to clipboard!")

    def clear_all(self):
        self.grid = [[0] * 8 for _ in range(8)]
        for row in range(8):
            for col in range(8):
                self.canvas.itemconfig(self.cells[row][col][0], fill="white")
                self.canvas.itemconfig(self.cells[row][col][1], text="")
        self.update_output()

    def invert(self):
        for r in range(8):
            for c in range(8):
                self.toggle(r, c)

    def save_pattern(self):
        file = tk.filedialog.asksaveasfilename(defaultextension=".pat")
        if file:
            json.dump({"grid": self.grid}, open(file, "w"))
            messagebox.showinfo("Saved", "Pattern saved!")

    def load_pattern(self):
        file = tk.filedialog.askopenfilename()
        if file:
            self.grid = json.load(open(file))["grid"]
            self.clear_all()
            for r in range(8):
                for c in range(8):
                    if self.grid[r][c]:
                        self.toggle(r, c)
            self.update_output()

if __name__ == "__main__":
    root = tk.Tk()
    app = MAX7219PatternEditor(root)
    root.mainloop()