import tkinter as tk
from itertools import product

def line(text=""):
    return text + ";\n"

class AbvInfo :
    def __init__(self,input_list,bus_list,out_put,window,module_name = "untitled",with_clock = False):
        self.module_name = module_name
        self.input_list = input_list
        self.bus_list = bus_list
        self.out_put = out_put
        self.with_clock = with_clock
        self.window = window

class BusInfo :
    def __init__(self,name,pins):
        self.name = name
        self.pins = pins


def header_generate(abv_info):
    res = ""
    res += line("module " + abv_info.module_name)

    # 所有引脚：普通输入 + 输出
    pin_list = abv_info.input_list + abv_info.out_put
    if abv_info.with_clock:
        res += line("CLK,"+",".join(pin_list) + " PIN")
    else:
        res += line(",".join(pin_list) + " PIN")

    # 自动声明 Bus
    for bus in abv_info.bus_list:
        res += line(f"{bus.name} = [{','.join(bus.pins)}]")

    # 其他符号定义（可选）
    res += line("x = .x.")
    return res


def vector_generate(abv_info):
    res = "test_vectors\n"

    # 构建 Bus 映射：{bus_name: [pin1, pin2, ...]}
    bus_map = {bus.name: bus.pins for bus in abv_info.bus_list}
    bus_names = list(bus_map.keys())
    bus_pins = [pin for pins in bus_map.values() for pin in pins]

    # 获取非 Bus 的普通输入口
    regular_inputs = [pin for pin in abv_info.input_list if pin not in bus_pins]

    # 构建输入输出映射行
    input_display = regular_inputs + bus_names
    output_display = abv_info.out_put
    if abv_info.with_clock:
        res += f"([CLK,{','.join(input_display)}]->[{','.join(output_display)}])\n"
    else:
        res += f"([{','.join(input_display)}]->[{','.join(output_display)}])\n"

    # 构建组合空间：普通输入是 0/1，Bus 是整数范围
    regular_combos = list(product([0, 1], repeat=len(regular_inputs)))
    bus_ranges = [range(2 ** len(bus_map[name])) for name in bus_names]
    bus_combos = list(product(*bus_ranges))

    # 组合拼接
    for r_vals in regular_combos:
        for b_vals in bus_combos:
            input_str = ",".join(str(v) for v in r_vals + b_vals)
            output_str = ",".join(["x"] * len(output_display))  # 默认输出为 x
            if abv_info.with_clock:
                res += f"[.c.,{input_str}]->[{output_str}];\n"
            else:
                res += f"[{input_str}]->[{output_str}];\n"
#TODO 这个时钟需要考虑
    res += "END\n"
    return res

def generate_output_names(n):
    return [f"OUT{chr(ord('A') + i)}" for i in range(n)]


def generate_input_names(n):
    # 生成 A, B, C, D... 最多支持 26 个输入口
    return [f"{chr(ord('A') + i)}" for i in range(n)]



def open_bus_config(abvinfo):
    bus_window = tk.Toplevel()
    bus_window.title("配置 Bus")

    # Bus 名称输入
    tk.Label(bus_window, text="Bus 名称：").grid(row=0, column=0, padx=10, pady=5, sticky="e")
    bus_name_entry = tk.Entry(bus_window)
    bus_name_entry.grid(row=0, column=1, padx=10, pady=5)

    # 输入口选择区
    tk.Label(bus_window, text="选择输入口组成 Bus：").grid(row=2, column=0, columnspan=2, pady=5)
    check_vars = {}
    for i, pin in enumerate(abvinfo.input_list):
        var = tk.BooleanVar()
        chk = tk.Checkbutton(bus_window, text=pin, variable=var)
        chk.grid(row=3 + i // 4, column=i % 4, padx=5, pady=2)
        check_vars[pin] = var

    # 确认按钮
    def confirm_bus():
        name = bus_name_entry.get().strip()
        selected_pins = [pin for pin, var in check_vars.items() if var.get()]
        if not selected_pins:
            print("⚠️ 至少选择一个引脚")
            return
        if name == "":
            name = f"BUS{len(abvinfo.bus_list) + 1}"
        abvinfo.bus_list.append(BusInfo(name, selected_pins))
        print(f"✅ 添加 Bus：{name}，引脚：{selected_pins}")

        bus_window.destroy()

    tk.Button(bus_window, text="确认", command=confirm_bus).grid(row=20, column=0, columnspan=4, pady=10)

'''
if __name__ == "__main__":
    print(header_generate(AbvInfo(["A"],["B"],["C"],"test")))
'''



