


import tkinter as tk
from tkinter import scrolledtext
import tkinter.ttk as ttk
from abvGenerate import *


def main():
    window = tk.Tk()
    window.title("ABV 文件生成器")
    abv_info = AbvInfo([], [], [])
    window_parm = []

    # 输入口名称文本框
    tk.Label(window, text="输入口名称（用逗号分隔）：\n无输入使用默认构造").pack()
    input_name_var = tk.StringVar()

    input_name_entry = tk.Entry(window, textvariable=input_name_var, width=60)
    input_name_entry.pack(pady=5)
    input_name_entry.insert(0, generate_input_names(6))  # 默认值，可根据需要修改

    # 输入口数量选择
    tk.Label(window, text="选择输入口数量：").pack()
    input_options = list(range(1, 17))
    input_count = tk.IntVar(value=3)
    input_combo = ttk.Combobox(window, values=input_options, textvariable=input_count, state="readonly", width=5)
    input_combo.pack(pady=5)
    input_combo.current(input_options.index(3))

    # 输出口数量选择
    tk.Label(window, text="选择输出口数量：").pack()
    output_options = list(range(1, 9))
    output_count = tk.IntVar(value=1)
    output_combo = ttk.Combobox(window, values=output_options, textvariable=output_count, state="readonly", width=5)
    output_combo.pack(pady=5)
    output_combo.current(output_options.index(1))

    # 文本框
    output_box = scrolledtext.ScrolledText(window, width=60, height=20, font=("Courier", 10))
    output_box.pack(padx=10, pady=10)

    # 配置 BUS 按钮
    tk.Button(window, text="配置BUS", command=lambda: open_bus_config(abv_info)).pack(pady=5)

    # 生成 ABV 内容
    def on_generate(*args):
        # 获取用户输入的输入口名称
        raw_input_names = input_name_entry.get()
        input_names = [name.strip() for name in raw_input_names.split(",") if name.strip()]

        # 如果用户没有输入，则使用默认生成函数
        if not input_names:
            input_names = generate_input_names(input_count.get())

        abv_info.input_list = input_names
        abv_info.out_put = generate_output_names(output_count.get())
        abv_text = header_generate(abv_info)
        abv_text += vector_generate(abv_info)
        output_box.delete(1.0, tk.END)
        output_box.insert(tk.END, abv_text)

    tk.Button(window, text="生成 ABV 内容", command=on_generate).pack(pady=10)

    # 自动更新输入输出口列表并刷新文本框
    input_combo.bind("<<ComboboxSelected>>", lambda e: on_generate())
    output_combo.bind("<<ComboboxSelected>>", lambda e: on_generate())
    input_name_var.trace_add("write",on_generate)

    on_generate()

    window.mainloop()

if __name__ == "__main__":
    main()