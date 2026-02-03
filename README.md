# 🔲 DotMatrixer 8×8 (Archived)
### Visual pattern designer & code generator for MAX7219 LED matrices

**DotMatrixer 8×8** is a small desktop tool that lets you **design 8×8 LED dot-matrix patterns visually** and then **generate ready-to-paste Arduino code** for MAX7219-based displays.

This project exists because manually writing byte arrays is slow, error-prone, and frustrating.

---

## 🚀 What problem does this solve?

When working with 8×8 MAX7219 LED matrices, developers often need to:
- sketch patterns on paper
- manually convert pixels to bits
- debug inverted rows or columns
- repeat trial-and-error for every new design

DotMatrixer removes that friction entirely.

---

## ✨ What it does

- 🖱️ **Interactive 8×8 grid**
  - Click to toggle individual LEDs on/off
- 👁️ **Immediate visual feedback**
  - See exactly what the matrix will display
- 🧾 **Arduino code generation**
  - Outputs byte/array definitions you can paste directly into your sketch
- 🔁 **Fast iteration**
  - Design, tweak, and regenerate patterns in seconds

This tool focuses on *design → code*, nothing more, nothing less.

---

## 🧠 Why this is useful

This isn’t a demo or example sketch.

It’s a **workflow tool**:
- reduces mistakes
- speeds up development
- makes patterns reproducible
- removes guesswork from bit manipulation

If you use MAX7219 matrices even occasionally, this saves time immediately.

---

## 🗂️ Project contents

- `DotMatrixer8x8_v2.0.py` — desktop GUI application
- Visual editor + code export logic

(No external Arduino dependencies required.)

---

## ▶️ Usage

```bash
python DotMatrixer8x8_v2.0.py
```
1. Click cells to design your pattern
2. Copy the generated Arduino array/code
3. Paste it into your MAX7219 sketch

## ⚠️ Project status

Archived / Complete

- Feature-complete for its intended purpose
- No hardware connection required
- No active development planned

This tool does exactly what it was built to do — and does it well.

## 💡 If expanded in the future…

Possible extensions (not required):

- animation frame sequencing
- multiple matrix chaining
- export formats for different libraries
- save/load pattern files

The core idea already stands on its own.

## 🏷️ Status

Archived — small, practical, and still genuinely useful.
