import tkinter as tk
from tkinter import filedialog, messagebox
import xml.etree.ElementTree as ET
import pandas as pd

def process_files():
    try:
        # 读取 Excel 文件
        excel_path = filedialog.askopenfilename(title="选择 Excel 文件", filetypes=[("Excel 文件", "*.xlsx")])
        if not excel_path:
            messagebox.showerror("错误", "未选择 Excel 文件！")
            return
        df = pd.read_excel(excel_path)

        # 处理 Excel 数据，确保 Address 列格式统一
        df['Address'] = df['Address'].astype(str).str.strip()
        address_to_name = dict(zip(df['Address'], df['Name']))
        print(address_to_name)

        # 读取 XML 文件
        xml_path = filedialog.askopenfilename(title="选择 XML 文件", filetypes=[("XML 文件", "*.xml")])
        if not xml_path:
            messagebox.showerror("错误", "未选择 XML 文件！")
            return
        tree = ET.parse(xml_path)
        root = tree.getroot()

        # 更新 XML 数据
        namespace = {'ns': 'http://knx.org/xml/ga-export/01'}
        updated_count = 0
        skipped_count = 0

        for group_address in root.findall('.//ns:GroupAddress', namespace):
            address = group_address.get('Address')
            if not address:
                print("Error: Missing Address attribute!")
                continue
            address = address.strip()  # 清理 Address 的格式
            print(address)
            print(address_to_name)
            # 如果 Address 在 Excel 中有对应的 Name，则更新
            if address in address_to_name:
                name_value = str(address_to_name[address])
                group_address.set('Name', name_value)
                print(f"Updated: {address} -> {name_value}")
                updated_count += 1
            else:
                print(f"Skipping Address: {address} (Not found in Excel) ")
                skipped_count += 1

        if updated_count == 0:
            messagebox.showwarning("警告", "没有更新任何记录！")
            return

        # 保存 XML 文件
        ET.register_namespace('', 'http://knx.org/xml/ga-export/01')
        save_path = filedialog.asksaveasfilename(title="保存修改后的 XML 文件", defaultextension=".xml",
                                                 filetypes=[("XML 文件", "*.xml")])
        if not save_path:
            messagebox.showerror("错误", "未选择保存路径！")
            return
        tree.write(save_path, encoding='utf-8', xml_declaration=True)

        messagebox.showinfo("成功", f"文件已成功更新 {updated_count} 条记录，跳过 {skipped_count} 条，并保存到：\n{save_path}")

    except Exception as e:
        messagebox.showerror("错误", f"处理文件时发生错误：\n{str(e)}")

# 创建 GUI
root = tk.Tk()
root.title("XML 更新工具")

label = tk.Label(root, text="通过 Excel 更新 XML 中的 GroupAddress Name", font=("Arial", 14))
label.pack(pady=10)

btn = tk.Button(root, text="选择文件并更新", command=process_files, font=("Arial", 12), bg="purple", fg="white")
btn.pack(pady=20)

root.geometry("400x200")
root.mainloop()
