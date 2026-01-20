#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
更新前端HTML页面
从market_data.json读取数据，更新index.html中的价格数据
"""

import json
import re
from datetime import datetime


def load_market_data():
    """加载市场数据"""
    with open('market_data.json', 'r', encoding='utf-8') as f:
        return json.load(f)


def update_html_with_data(html_file, data):
    """
    更新HTML文件中的价格数据

    Args:
        html_file: HTML文件路径
        data: 市场数据
    """
    # 读取HTML文件
    with open(html_file, 'r', encoding='utf-8') as f:
        html_content = f.read()

    # 更新日期
    today = data.get('date', datetime.now().strftime('%Y-%m-%d'))
    html_content = re.sub(
        r'<p class="date-text">[^<]*</p>',
        f'<p class="date-text">{today}</p>',
        html_content
    )

    # 更新各个产品的价格
    products = data.get('products', {})

    # 生猪
    if '生猪' in products:
        price = products['生猪'].get('price', 0)
        html_content = re.sub(
            r'<span class="national-price">[0-9.]+</span>',
            f'<span class="national-price">{price}</span>',
            html_content,
            count=1
        )

    # 仔猪
    if '仔猪' in products:
        price = products['仔猪'].get('price', 0)
        html_content = re.sub(
            r'<span class="national-price">[0-9.]+</span>',
            f'<span class="national-price">{price}</span>',
            html_content,
            count=1
        )

    # 鸡蛋
    if '鸡蛋' in products:
        price = products['鸡蛋'].get('price', 0)
        html_content = re.sub(
            r'<span class="national-price">[0-9.]+</span>',
            f'<span class="national-price">{price}</span>',
            html_content,
            count=1
        )

    # 淘汰鸡
    if '淘汰鸡' in products:
        price = products['淘汰鸡'].get('price', 0)
        html_content = re.sub(
            r'<span class="national-price">[0-9.]+</span>',
            f'<span class="national-price">{price}</span>',
            html_content,
            count=1
        )

    # 玉米
    if '玉米' in products:
        price = products['玉米'].get('price', 0)
        html_content = re.sub(
            r'<span class="national-price">[0-9.]+</span>',
            f'<span class="national-price">{price}</span>',
            html_content,
            count=1
        )

    # 豆粕
    if '豆粕' in products:
        price = products['豆粕'].get('price', 0)
        html_content = re.sub(
            r'<span class="national-price">[0-9.]+</span>',
            f'<span class="national-price">{price}</span>',
            html_content,
            count=1
        )

    # 保存更新后的HTML文件
    with open(html_file, 'w', encoding='utf-8') as f:
        f.write(html_content)

    print(f"HTML文件已更新: {html_file}")


def main():
    """主函数"""
    print("=" * 60)
    print("开始更新前端HTML页面")
    print("=" * 60)

    # 加载数据
    data = load_market_data()
    print(f"数据日期: {data.get('date', '未知')}")

    # 更新index.html
    try:
        update_html_with_data('../anyu-netlify-deploy/index.html', data)
        print("✅ index.html 更新成功")
    except Exception as e:
        print(f"❌ index.html 更新失败: {e}")

    print("=" * 60)
    print("HTML更新完成！")
    print("=" * 60)


if __name__ == "__main__":
    main()
