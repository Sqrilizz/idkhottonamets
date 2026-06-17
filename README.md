# 🇨🇳 People's Republic of China Super Calculator v1.0

**Codename: 红龙 (Red Dragon)** 🐉

---

## 🧮 About

A calculator with a fully Chinese-themed interface.  
Enter numbers using Chinese digits, and the program calculates and displays the result in Chinese digits too.

**Example:**

```
  一二三
+ 四五六
= 五七九
```

---

## 🚀 Quick Start

### Option 1 — Prebuilt binary

```bash
cd dist/
./习近平计算器.exe
```

### Option 2 — From source (Python 3 required)

```bash
pip install pillow pygame
python3 计算器.py
```

---

## 🎮 How to Use

### Buttons

| Button | Action |
|--------|--------|
| **七** **八** **九** … **零** | Enter Chinese digits |
| **＋** | Addition |
| **−** | Subtraction |
| **×** | Multiplication |
| **÷** | Division |
| **＝** | Calculate |
| **清除** | Clear everything |
| **←** | Delete last character |
| **．** | Decimal point |

### Keyboard Shortcuts

| Key | Action |
|---------|----------|
| `+` `-` `*` `/` | Operators |
| `一二三四五六七八九` | Enter Chinese digits directly |
| `Enter` | Calculate |
| `Backspace` | Delete last char |
| `Escape` | Clear everything |

### 主席模式 (Mao Mode)

Click the **主席** button — the interface turns fully red,
a portrait of Mao Zedong appears, and **"Red Sun in the Sky" (东方红)** starts playing.

---

## 📁 Project Structure

```
IDKtbh/
├── 计算器.py                              # Source code
├── leader.jpg                             # Background image
├── mao zedong propaganda music Red Sun in the Sky.mp3  # Mao mode music
├── dist/
│   └── 习近平计算器.exe                   # Prebuilt binary (59 MB)
└── README.md                              # This file
```

---

## 🔧 Technical Details

- **Language:** Python 3
- **GUI:** Tkinter
- **Build system:** PyInstaller (one-file mode)
- **Images:** Pillow (PIL)
- **Audio:** pygame / ffplay
- **Binary size:** ~59 MB
- **All variables in source code are named in Chinese**

### Requirements

- **Linux x86-64** (binary)
- **Python 3.8+** (to run from source)
- **pygame + Pillow** (optional, for music and background image)

---

## 📜 License

MIT — do whatever you want 🇨🇳🐉
