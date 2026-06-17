#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
中国超级计算器 v1.0
代号: 红龙
"""

import math
import os
import subprocess
import tkinter as tk
from tkinter import font, messagebox

from PIL import Image, ImageTk

# ============================================================
# 全局配置
# ============================================================
金色 = "#FFD700"
暗红 = "#8B0000"
深红 = "#4A0000"
深红黑 = "#1A0000"
白 = "#FFFFFF"
黑 = "#000000"

# ============================================================
# 中文数字字典
# ============================================================
中数字_到_阿拉伯 = {
    "零": 0,
    "一": 1,
    "二": 2,
    "三": 3,
    "四": 4,
    "五": 5,
    "六": 6,
    "七": 7,
    "八": 8,
    "九": 9,
}

阿拉伯_到_中数字 = {v: k for k, v in 中数字_到_阿拉伯.items()}

中文运算符映射 = {
    "+": "+",
    "-": "-",
    "*": "*",
    "/": "/",
}


def 中文转阿拉伯(中文文本: str) -> int:
    """将中文数字字符串转换为整数。"""
    if not 中文文本:
        return 0
    结果 = 0
    for 字符 in 中文文本:
        if 字符 in 中数字_到_阿拉伯:
            结果 = 结果 * 10 + 中数字_到_阿拉伯[字符]
        else:
            raise ValueError(f"无效的中文数字字符: {字符}")
    return 结果


def 阿拉伯转中文(数字: int) -> str:
    """将整数转换为中文数字字符串。"""
    if 数字 == 0:
        return "零"
    符号 = ""
    if 数字 < 0:
        符号 = "负"
        数字 = -数字
    结果 = ""
    for 字符 in str(数字):
        结果 += 阿拉伯_到_中数字[int(字符)]
    return 符号 + 结果


def 阿拉伯浮点转中文(数字: float) -> str:
    """将浮点数转换为中文数字字符串（支持小数）。"""
    if 数字 == 0:
        return "零"
    if 数字 == int(数字):
        return 阿拉伯转中文(int(数字))
    符号 = ""
    if 数字 < 0:
        符号 = "负"
        数字 = -数字
    整数部分 = int(math.floor(数字))
    小数部分 = 数字 - 整数部分
    结果 = 阿拉伯转中文(整数部分)
    结果 += "点"
    小数文本 = f"{小数部分:.10f}".rstrip("0").lstrip("0.")
    for 字符 in 小数文本:
        结果 += 阿拉伯_到_中数字[int(字符)]
    return 符号 + 结果


# ============================================================
# MP3 плеер для режима Мао
# ============================================================
class 音频:
    def __init__(self):
        self.进程 = None
        self.路径 = self._找到MP3()

    def _找到MP3(self):
        папка = os.path.dirname(os.path.abspath(__file__))
        for файл in os.listdir(папка):
            if файл.endswith(".mp3"):
                return os.path.join(папка, файл)
        return None

    def 播放(self):
        if not self.路径:
            return
        self.停止()
        try:
            import pygame

            pygame.mixer.init()
            pygame.mixer.music.load(self.路径)
            pygame.mixer.music.set_volume(0.5)
            pygame.mixer.music.play(-1)
            self.进程 = "pygame"
        except Exception:
            try:
                self.进程 = subprocess.Popen(
                    ["ffplay", "-nodisp", "-loop", "0", self.路径],
                    stdout=subprocess.DEVNULL,
                    stderr=subprocess.DEVNULL,
                )
            except Exception:
                self.进程 = None

    def 停止(self):
        if self.进程 == "pygame":
            try:
                import pygame

                pygame.mixer.music.stop()
                pygame.mixer.music.unload()
            except Exception:
                pass
        elif self.进程:
            try:
                self.进程.terminate()
                self.进程.wait(timeout=2)
            except Exception:
                try:
                    self.进程.kill()
                except Exception:
                    pass
        self.进程 = None


# ============================================================
# 主计算器类
# ============================================================
class 计算器:
    """中华人民共和国超级计算器 — как настоящий калькулятор"""

    def __init__(self):
        self.窗口 = tk.Tk()
        self.窗口.title("中华人民共和国超级计算器 v1.0")
        self.窗口.geometry("420x620")
        self.窗口.configure(bg=暗红)
        self.窗口.resizable(False, False)

        # 状态变量
        self.数字一 = ""
        self.数字二 = ""
        self.运算符 = ""
        self.结果 = ""
        self.显示文本 = ""
        self.总计算次数 = 0
        self.主席模式激活 = False
        self.输入开始 = True

        # 音频 (только для режима Мао)
        self.音频 = 音频()

        # 加载背景图片
        self.背景图 = None
        папка = os.path.dirname(os.path.abspath(__file__))
        путь = os.path.join(папка, "leader.jpg")
        if os.path.exists(путь):
            try:
                пил = Image.open(путь).resize((420, 620), Image.LANCZOS)
                self.背景图 = ImageTk.PhotoImage(пил)
            except Exception:
                self.背景图 = None

        # 设置样式
        self.设置字体()
        self.构建界面()
        self.播放欢迎()

        self.窗口.protocol("WM_DELETE_WINDOW", self.退出)

    def 设置字体(self):
        """初始化字体"""
        self.字体标题 = font.Font(family="SimSun", size=16, weight="bold")
        self.字体按钮大 = font.Font(family="SimSun", size=18, weight="bold")
        self.字体按钮 = font.Font(family="SimSun", size=14, weight="bold")
        self.字体数字 = font.Font(family="SimSun", size=22, weight="bold")
        self.字体显示 = font.Font(family="SimSun", size=26, weight="bold")
        self.字体状态 = font.Font(family="SimSun", size=10)

    # ───────────── Сборка интерфейса ─────────────

    def 构建界面(self):
        """Собрать калькулятор"""
        # === Фоновая картинка ===
        if self.背景图:
            bg = tk.Label(self.窗口, image=self.背景图, bg=暗红)
            bg.place(x=0, y=0, relwidth=1, relheight=1)
            bg.lower()

        # === Верхняя панель ===
        顶部 = tk.Frame(self.窗口, bg=暗红)
        顶部.pack(fill=tk.X, pady=(8, 2))

        国旗 = tk.Label(
            顶部,
            text="★ ★ ★ ★ ★",
            font=font.Font(family="SimSun", size=12),
            fg=金色,
            bg=暗红,
        )
        国旗.pack()

        标题 = tk.Label(
            顶部, text="中华人民共和国超级计算器", font=self.字体标题, fg=金色, bg=暗红
        )
        标题.pack()

        版本 = tk.Label(
            顶部, text="v1.0 | 代号: 红龙 🐉", font=self.字体状态, fg=金色, bg=暗红
        )
        版本.pack()

        # === Дисплей ===
        显示框架 = tk.Frame(self.窗口, bg=深红, relief=tk.RIDGE, bd=4)
        显示框架.pack(pady=(8, 5), padx=15, fill=tk.X)

        # нижний дисплей — вводимое число / результат
        self.显示标签 = tk.Label(
            显示框架,
            text="",
            font=self.字体显示,
            fg=金色,
            bg=深红,
            height=2,
            anchor=tk.E,
            padx=12,
        )
        self.显示标签.pack(fill=tk.X)

        # === Кнопочная сетка ===
        сетка = tk.Frame(self.窗口, bg=暗红)
        сетка.pack(pady=5, padx=15, fill=tk.BOTH, expand=True)

        # Стили кнопок
        стиль_число = {
            "font": self.字体按钮大,
            "fg": 金色,
            "bg": "#3D0000",
            "activeforeground": 金色,
            "activebackground": "#5C0000",
            "relief": tk.RAISED,
            "bd": 3,
            "cursor": "hand2",
            "width": 3,
            "height": 1,
        }
        стиль_операция = {
            "font": self.字体按钮大,
            "fg": 暗红,
            "bg": 金色,
            "activeforeground": 暗红,
            "activebackground": "#E6BE00",
            "relief": tk.RAISED,
            "bd": 3,
            "cursor": "hand2",
            "width": 3,
            "height": 1,
        }
        стиль_равно = {
            "font": self.字体按钮大,
            "fg": 白,
            "bg": "#B22222",
            "activeforeground": 白,
            "activebackground": "#DC143C",
            "relief": tk.RAISED,
            "bd": 3,
            "cursor": "hand2",
            "width": 3,
            "height": 1,
        }
        стиль_очистка = {
            "font": self.字体按钮,
            "fg": 白,
            "bg": "#4A0000",
            "activeforeground": 白,
            "activebackground": "#6B0000",
            "relief": tk.RAISED,
            "bd": 3,
            "cursor": "hand2",
            "width": 3,
            "height": 1,
        }
        стиль_стереть = {
            "font": font.Font(family="SimSun", size=14, weight="bold"),
            "fg": 金色,
            "bg": "#3D0000",
            "activeforeground": 金色,
            "activebackground": "#5C0000",
            "relief": tk.RAISED,
            "bd": 3,
            "cursor": "hand2",
            "width": 3,
            "height": 1,
        }

        # Раскладка кнопок (4 колонки, 6 рядов)
        кнопки = [
            # (текст, стиль, команда, colspan)
            ("七", стиль_число, lambda t="七": self.数字输入(t), 1),
            ("八", стиль_число, lambda t="八": self.数字输入(t), 1),
            ("九", стиль_число, lambda t="九": self.数字输入(t), 1),
            ("÷", стиль_операция, lambda: self.操作输入("/"), 1),
            ("四", стиль_число, lambda t="四": self.数字输入(t), 1),
            ("五", стиль_число, lambda t="五": self.数字输入(t), 1),
            ("六", стиль_число, lambda t="六": self.数字输入(t), 1),
            ("×", стиль_операция, lambda: self.操作输入("*"), 1),
            ("一", стиль_число, lambda t="一": self.数字输入(t), 1),
            ("二", стиль_число, lambda t="二": self.数字输入(t), 1),
            ("三", стиль_число, lambda t="三": self.数字输入(t), 1),
            ("−", стиль_операция, lambda: self.操作输入("-"), 1),
            ("零", стиль_число, lambda t="零": self.数字输入(t), 1),
            (".", стиль_число, lambda t=".": self.数字输入(t), 1),
            ("＝", стиль_равно, self.执行计算, 1),
            ("＋", стиль_операция, lambda: self.操作输入("+"), 1),
            ("清除", стиль_очистка, self.执行清除, 2),
            ("←", стиль_стереть, self.删除, 1),
            ("主席", стиль_очистка, self.切换主席模式, 1),
        ]

        # Создаём кнопки в grid
        ряд = 0
        колонка = 0
        for текст, стиль, команда, colspan in кнопки:
            btn = tk.Button(сетка, text=текст, command=команда, **стиль)
            btn.grid(
                row=ряд,
                column=колонка,
                columnspan=colspan,
                padx=3,
                pady=3,
                sticky="nsew",
            )
            колонка += colspan
            if колонка >= 4:
                колонка = 0
                ряд += 1

        # Настройка растяжения колонок/рядов
        for i in range(4):
            сетка.columnconfigure(i, weight=1, uniform="btn")
        for i in range(5):
            сетка.rowconfigure(i, weight=1, uniform="btn")

        # === Нижняя панель: статистика ===
        底部 = tk.Frame(self.窗口, bg=暗红)
        底部.pack(fill=tk.X, padx=15, pady=(5, 8))

        self.统计标签 = tk.Label(
            底部, text="总计算次数: 0", font=self.字体状态, fg=金色, bg=暗红
        )
        self.统计标签.pack(side=tk.LEFT)

        # === Скрытый портрет Мао ===
        self.主席画像标签 = tk.Label(
            self.窗口,
            text="""
         ╔══════════════╗
         ║   毛泽东     ║
         ║  (1893-1976) ║
         ║              ║
         ║   🚩 东方红  ║
         ╚══════════════╝
            """,
            font=font.Font(family="SimSun", size=10),
            fg=金色,
            bg=暗红,
            justify=tk.CENTER,
        )

        # Клавиатурные сокращения
        self.窗口.bind("<Return>", lambda e: self.执行计算())
        self.窗口.bind("<Escape>", lambda e: self.执行清除())
        self.窗口.bind("<BackSpace>", lambda e: self.删除())
        self.窗口.bind("<Key>", self.键盘输入)

    # ───────────── Логика калькулятора ─────────────

    def 数字输入(self, цифра):
        """Нажата цифровая кнопка"""
        if self.输入开始:
            # После оператора или = начинаем новое число
            self.显示文本 = ""
            self.输入开始 = False
        if цифра == ".":
            if "." in self.显示文本:
                return  # уже есть точка
            if self.显示文本 == "":
                self.显示文本 = "零"
            self.显示文本 += "点"
        else:
            self.显示文本 += цифра
        self.刷新显示()

    def 操作输入(self, операция):
        """Нажат оператор (+ − × ÷)"""
        if not self.显示文本 and self.数字一 == "":
            return  # нет числа — игнорируем

        if self.显示文本:
            # Сохраняем первое число
            self.数字一 = self.显示文本

        self.运算符 = операция
        self.输入开始 = True
        self.刷新显示(операция)

    def 执行计算(self):
        """Нажата ＝ — вычислить"""
        # Если нет оператора, но есть результат — повторяем операцию
        if not self.运算符 and self.结果:
            # Повтор последней операции с новым числом
            pass

        if not self.运算符 or not self.数字一:
            return

        # Второе число — текущий ввод
        if self.显示文本:
            self.数字二 = self.显示文本
        elif self.数字二:
            pass  # используем предыдущее число
        else:
            return

        try:
            数一 = 中文转阿拉伯(self.数字一)
            数二 = 中文转阿拉伯(self.数字二)

            if self.运算符 == "+":
                运算结果 = 数一 + 数二
            elif self.运算符 == "-":
                运算结果 = 数一 - 数二
            elif self.运算符 == "*":
                运算结果 = 数一 * 数二
            elif self.运算符 == "/":
                if 数二 == 0:
                    raise ZeroDivisionError("除以零错误！")
                运算结果 = 数一 / 数二
            else:
                raise ValueError(f"不支持的运算符: {self.运算符}")

            if isinstance(运算结果, float) and 运算结果 != int(运算结果):
                self.结果 = 阿拉伯浮点转中文(运算结果)
            else:
                self.结果 = 阿拉伯转中文(int(运算结果))

            # Показываем выражение и результат
            выражение = f"{self.数字一} {self.运算符} {self.数字二}"
            self.显示文本 = self.结果
            self.刷新显示()

            self.总计算次数 += 1
            self.统计标签.config(text=f"总计算次数: {self.总计算次数}")

            # Результат становится первым числом для цепочки
            self.数字一 = self.结果
            self.数字二 = ""
            # оставляем оператор — можно нажать снова =
            self.输入开始 = True

        except ValueError as e:
            self.显示文本 = "错误"
            self.刷新显示()
            messagebox.showerror("错误", str(e))
        except ZeroDivisionError as e:
            self.显示文本 = "错误"
            self.刷新显示()
            messagebox.showerror("错误", str(e))

    def 删除(self):
        """← стереть последний символ"""
        if self.输入开始 or not self.显示文本:
            return
        # Удаляем последнюю цифру или "点"
        if self.显示文本.endswith("点"):
            self.显示文本 = self.显示文本[:-1]
        elif self.显示文本:
            self.显示文本 = self.显示文本[:-1]
        self.刷新显示()

    def 执行清除(self):
        """Полная очистка"""
        self.数字一 = ""
        self.数字二 = ""
        self.运算符 = ""
        self.结果 = ""
        self.显示文本 = ""
        self.输入开始 = True
        self.显示标签.config(text="")

    def 刷新显示(self, оператор_префикс=""):
        """Обновить текст на дисплее"""
        if оператор_префикс and self.数字一:
            self.显示标签.config(text=f"{self.数字一} {оператор_префикс}")
        elif self.显示文本:
            self.显示标签.config(text=self.显示文本)
        else:
            self.显示标签.config(text="")

    def 键盘输入(self, event):
        """Обработка нажатий с клавиатуры"""
        символ = event.char
        if символ in "零一二三四五六七八九":
            self.数字输入(символ)
        elif символ == "+":
            self.操作输入("+")
        elif символ == "-":
            self.操作输入("-")
        elif символ == "*":
            self.操作输入("*")
        elif символ == "/":
            self.操作输入("/")
        elif символ == "=" or символ == "\r":
            self.执行计算()
        elif символ in ".点":
            self.数字输入(".")

    # ───────────── Мао-режим ─────────────

    def 切换主席模式(self):
        """切换主席模式"""
        self.主席模式激活 = not self.主席模式激活

        if self.主席模式激活:
            红 = "#FF0000"

            self.窗口.configure(bg=红)
            self.递归改变背景(self.窗口, 红)
            self.主席画像标签.pack(pady=5)
            self.显示标签.config(text="毛主席万岁！")
            self.音频.播放()
        else:
            self.窗口.configure(bg=暗红)
            self.递归改变背景(self.窗口, 暗红)
            self.主席画像标签.pack_forget()
            self.显示标签.config(text="欢迎使用")
            self.音频.停止()

    def 递归改变背景(self, 父组件, 颜色):
        """递归改变所有子组件的背景色"""
        for 子 in 父组件.winfo_children():
            try:
                子.configure(bg=颜色)
            except tk.TclError:
                pass
            if 子.winfo_children():
                self.递归改变背景(子, 颜色)

    def 播放欢迎(self):
        """播放欢迎消息"""
        self.显示标签.config(text="欢迎使用超级计算器")
        self.窗口.after(2500, lambda: self.显示标签.config(text=""))

    def 退出(self):
        """Выход"""
        if hasattr(self, "音频"):
            self.音频.停止()
        self.窗口.destroy()


# ============================================================
# 程序入口
# ============================================================
if __name__ == "__main__":
    计算器实例 = 计算器()
    计算器实例.窗口.mainloop()
