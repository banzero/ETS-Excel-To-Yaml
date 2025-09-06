from flask import Flask, render_template, request, send_file, flash, redirect, url_for, jsonify
import io
import os
import json
import openpyxl
from werkzeug.utils import secure_filename
from process_core import process_excel_xml, process_excel_to_yaml


app = Flask(__name__)
app.secret_key = os.environ.get('FLASK_SECRET_KEY', 'dev-secret-key')
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024 

@app.route('/', methods=['GET'])
def index():
    return render_template('index.html')


@app.route('/process-xml', methods=['POST'])
def process_xml():
    try:
        excel_file = request.files.get('excel')
        xml_file = request.files.get('xml')

        if not excel_file or not xml_file:
            flash('请同时选择 Excel 和 XML 文件')
            return redirect(url_for('index'))

        # 可选：校验扩展名
        excel_filename = secure_filename(excel_file.filename or '')
        xml_filename = secure_filename(xml_file.filename or '')
        if not excel_filename.lower().endswith('.xlsx'):
            flash('Excel 文件必须为 .xlsx')
            return redirect(url_for('index'))
        if not xml_filename.lower().endswith('.xml'):
            flash('XML 文件必须为 .xml')
            return redirect(url_for('index'))

        out_bytes, updated_count, skipped_count = process_excel_xml(
            excel_file.read(),
            xml_file.read()
        )

        # 生成下载文件名
        base_name = os.path.splitext(xml_filename)[0] or 'output'
        out_name = f"{base_name}_updated.xml"

        mem = io.BytesIO(out_bytes)
        mem.seek(0)
        return send_file(
            mem,
            mimetype='application/xml',
            as_attachment=True,
            download_name=out_name,
            etag=False
        )
    except Exception as e:
        flash(f'XML处理失败：{str(e)}')
        return redirect(url_for('index'))


@app.route('/process-yaml', methods=['POST'])
def process_yaml():
    try:
        excel_file = request.files.get('excel')
        field_mapping_json = request.form.get('field_mapping', '{}')

        if not excel_file:
            flash('请选择 Excel 文件')
            return redirect(url_for('index'))

        # 校验扩展名
        excel_filename = secure_filename(excel_file.filename or '')
        if not excel_filename.lower().endswith('.xlsx'):
            flash('Excel 文件必须为 .xlsx')
            return redirect(url_for('index'))

        # 解析字段映射
        try:
            field_mapping = json.loads(field_mapping_json) if field_mapping_json else {}
        except json.JSONDecodeError:
            field_mapping = {}

        yaml_content, row_count = process_excel_to_yaml(
            excel_file.read(),
            field_mapping
        )

        # 生成下载文件名
        base_name = os.path.splitext(excel_filename)[0] or 'output'
        out_name = f"{base_name}.yaml"

        mem = io.BytesIO(yaml_content.encode('utf-8'))
        mem.seek(0)
        return send_file(
            mem,
            mimetype='application/x-yaml',
            as_attachment=True,
            download_name=out_name,
            etag=False
        )
    except Exception as e:
        flash(f'YAML处理失败：{str(e)}')
        return redirect(url_for('index'))


@app.route('/get-excel-headers', methods=['POST'])
def get_excel_headers():
    """获取Excel文件的表头，用于字段映射"""
    try:
        excel_file = request.files.get('excel')
        if not excel_file:
            return jsonify({'error': '请选择Excel文件'}), 400

        # 读取Excel表头
        excel_buf = io.BytesIO(excel_file.read())
        wb = openpyxl.load_workbook(excel_buf)
        sheet = wb.active
        headers = [cell.value for cell in sheet[1] if cell.value]
        
        return jsonify({'headers': headers})
    except Exception as e:
        return jsonify({'error': f'读取Excel失败：{str(e)}'}), 500


if __name__ == '__main__':
    # 生产环境关闭debug模式
    debug_mode = os.environ.get('FLASK_ENV') != 'production'
    app.run(host='0.0.0.0', port=5678, debug=debug_mode)


