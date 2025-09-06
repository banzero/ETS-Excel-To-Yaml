import openpyxl
import yaml
import codecs
import tkinter as tk
from tkinter import filedialog

def convert_excel_to_yaml():
    # 打开文件选择对话框
    root = tk.Tk()
    root.withdraw()
    file_path = filedialog.askopenfilename()

    # 打开Excel文件
    wb = openpyxl.load_workbook(file_path)
    sheet = wb.active

    # 获取表头
    headers = [cell.value for cell in sheet[1]]

    # 获取字段名并自定义
    fields = {}
    for header in headers:
        field_name = input(f"请输入'{header}'的字段名（留空表示使用原字段名）：")
        if field_name:
            fields[header] = field_name
        else:
            fields[header] = header

    # 转换为YAML
    data = []
    for row in sheet.iter_rows(min_row=2, values_only=True):
        row_data = {}
        for header, value in zip(headers, row):
            field_name = fields[header]
            if isinstance(value, str):
                value = f'"{value}"'
            row_data[field_name] = value
        data.append(row_data)

    yaml_data = yaml.dump(data, allow_unicode=True, default_flow_style=False,sort_keys=False)

    # 保存为YAML文件
    save_path = filedialog.asksaveasfilename(defaultextension=".yaml")
    with codecs.open(save_path, "w", encoding="utf-8") as file:
        file.write(yaml_data)

    print("转换完成！")

if __name__ == "__main__":
    convert_excel_to_yaml()
