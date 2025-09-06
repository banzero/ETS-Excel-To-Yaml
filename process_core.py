import io
import xml.etree.ElementTree as ET
import pandas as pd
import yaml
import openpyxl


def process_excel_xml(excel_content: bytes, xml_content: bytes):
    """
    使用 Excel 内容更新 XML 的 GroupAddress Name。

    参数:
    - excel_content: Excel 文件二进制内容（.xlsx）
    - xml_content: XML 文件二进制内容

    返回:
    - updated_xml_bytes: 修改后的 XML 二进制内容
    - updated_count: 更新的条目数
    - skipped_count: 跳过的条目数
    """

    # 读取 Excel
    excel_buf = io.BytesIO(excel_content)
    df = pd.read_excel(excel_buf)

    if 'Address' not in df.columns or 'Name' not in df.columns:
        raise ValueError('Excel 必须包含 Address 和 Name 两列')

    df['Address'] = df['Address'].astype(str).str.strip()
    address_to_name = dict(zip(df['Address'], df['Name']))

    # 解析 XML
    xml_buf = io.BytesIO(xml_content)
    tree = ET.parse(xml_buf)
    root = tree.getroot()

    namespace = {'ns': 'http://knx.org/xml/ga-export/01'}
    updated_count = 0
    skipped_count = 0

    for group_address in root.findall('.//ns:GroupAddress', namespace):
        address = group_address.get('Address')
        if not address:
            skipped_count += 1
            continue
        address = str(address).strip()

        if address in address_to_name:
            name_value = str(address_to_name[address])
            group_address.set('Name', name_value)
            updated_count += 1
        else:
            skipped_count += 1

    # 写回 XML
    ET.register_namespace('', 'http://knx.org/xml/ga-export/01')
    out_buf = io.BytesIO()
    tree.write(out_buf, encoding='utf-8', xml_declaration=True)
    return out_buf.getvalue(), updated_count, skipped_count


def process_excel_to_yaml(excel_content: bytes, field_mapping: dict = None):
    """
    将 Excel 文件转换为 YAML 格式。
    
    参数:
    - excel_content: Excel 文件二进制内容（.xlsx）
    - field_mapping: 字段映射字典，格式为 {原字段名: 新字段名}
    
    返回:
    - yaml_content: YAML 格式的字符串内容
    - row_count: 转换的行数
    """
    
    # 读取 Excel
    excel_buf = io.BytesIO(excel_content)
    wb = openpyxl.load_workbook(excel_buf)
    sheet = wb.active
    
    # 获取表头
    headers = [cell.value for cell in sheet[1]]
    
    # 处理字段映射
    if field_mapping is None:
        field_mapping = {}
    
    # 构建字段映射字典
    fields = {}
    for header in headers:
        if header in field_mapping:
            fields[header] = field_mapping[header]
        else:
            fields[header] = header
    
    # 转换为YAML数据
    data = []
    for row in sheet.iter_rows(min_row=2, values_only=True):
        row_data = {}
        for header, value in zip(headers, row):
            field_name = fields[header]
            # 处理值：数字保持原样，字符串确保有引号
            if value is None:
                row_data[field_name] = None
            elif isinstance(value, (int, float)):
                row_data[field_name] = value
            else:
                # 字符串值，确保有引号
                row_data[field_name] = str(value)
        data.append(row_data)
    
    # 生成YAML内容，使用自定义的字符串表示器
    class QuotedString(str):
        pass
    
    def quoted_string_representer(dumper, data):
        return dumper.represent_scalar('tag:yaml.org,2002:str', data, style='"')
    
    yaml.add_representer(QuotedString, quoted_string_representer)
    
    # 将字符串值转换为QuotedString
    for item in data:
        for key, value in item.items():
            if isinstance(value, str):
                item[key] = QuotedString(value)
    
    yaml_content = yaml.dump(
        data, 
        allow_unicode=True, 
        default_flow_style=False, 
        sort_keys=False
    )
    
    return yaml_content, len(data)


