#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
文档下载服务器
提供Excel和TXT文档的HTTP下载服务
"""

from http.server import HTTPServer, SimpleHTTPRequestHandler
import os
import mimetypes
from datetime import datetime
import json
from urllib.parse import unquote

class DownloadHandler(SimpleHTTPRequestHandler):
    """自定义请求处理器"""

    def do_GET(self):
        """处理GET请求"""
        if self.path == '/api/documents':
            self.handle_documents_list()
        elif self.path.startswith('/download/'):
            self.handle_download()
        else:
            super().do_GET()

    def handle_documents_list(self):
        """返回文档列表"""
        documents = []

        # 查找Excel文件
        for filename in os.listdir('.'):
            if filename.startswith('本周行情数据_') and filename.endswith('.xlsx'):
                filepath = os.path.join('.', filename)
                size = os.path.getsize(filepath)
                documents.append({
                    'type': 'excel',
                    'name': filename,
                    'title': '本周行情数据',
                    'description': '本周六大品类（生猪、仔猪、鸡蛋、淘汰鸡、玉米、豆粕）行情数据',
                    'size': size,
                    'download_url': f'/download/{filename}'
                })

        # 查找TXT文件
        for filename in os.listdir('.'):
            if filename.startswith('每周周报_') and filename.endswith('.txt'):
                filepath = os.path.join('.', filename)
                size = os.path.getsize(filepath)
                documents.append({
                    'type': 'txt',
                    'name': filename,
                    'title': '每周周报',
                    'description': '本周行情分析及下周市场预测',
                    'size': size,
                    'download_url': f'/download/{filename}'
                })

        # 返回JSON响应
        self.send_response(200)
        self.send_header('Content-Type', 'application/json')
        self.send_header('Access-Control-Allow-Origin', '*')
        self.end_headers()

        response = {
            'success': True,
            'timestamp': datetime.now().isoformat(),
            'documents': documents
        }
        self.wfile.write(json.dumps(response, ensure_ascii=False).encode('utf-8'))

    def handle_download(self):
        """处理文件下载"""
        # 从URL中提取文件名，并解码URL编码
        filename = unquote(self.path.replace('/download/', '').strip('/'))

        # 安全检查：防止路径遍历攻击
        if '..' in filename or filename.startswith('/'):
            self.send_error(403, 'Forbidden')
            return

        # 检查文件是否存在
        if not os.path.exists(filename):
            self.send_error(404, 'File not found')
            return

        # 检查文件类型（只允许下载Excel和TXT文件）
        if not (filename.endswith('.xlsx') or filename.endswith('.txt')):
            self.send_error(403, 'File type not allowed')
            return

        # 获取文件大小和MIME类型
        file_size = os.path.getsize(filename)
        mime_type, _ = mimetypes.guess_type(filename)

        # 设置响应头
        self.send_response(200)
        self.send_header('Content-Type', mime_type or 'application/octet-stream')
        self.send_header('Content-Length', str(file_size))
        # 使用RFC 2231编码处理中文文件名
        from urllib.parse import quote
        encoded_filename = quote(filename, safe='')
        self.send_header('Content-Disposition', f"attachment; filename*=UTF-8''{encoded_filename}")
        self.send_header('Access-Control-Allow-Origin', '*')
        self.end_headers()

        # 发送文件内容
        with open(filename, 'rb') as f:
            self.wfile.write(f.read())

    def log_message(self, format, *args):
        """自定义日志格式"""
        timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        print(f"[{timestamp}] {format % args}")

def main():
    """启动下载服务器"""
    server_address = ('', 5001)  # 使用5001端口
    httpd = HTTPServer(server_address, DownloadHandler)

    print("=" * 60)
    print("文档下载服务器已启动")
    print("=" * 60)
    print(f"服务地址: http://localhost:5001")
    print(f"启动时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print()
    print("可用接口:")
    print("  - GET /api/documents          获取文档列表")
    print("  - GET /download/<filename>    下载文档")
    print()
    print("按 Ctrl+C 停止服务器")
    print("=" * 60)
    print()

    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        print("\n服务器已停止")
        httpd.server_close()

if __name__ == "__main__":
    main()
