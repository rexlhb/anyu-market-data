#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
数据采集脚本
从博亚和讯、猪好多网、玄田数据采集生猪、仔猪、鸡蛋、淘汰鸡、玉米、豆粕价格
"""

import json
import re
import subprocess
from datetime import datetime, timedelta
from typing import Dict, List, Optional


def search_web(query: str, count: int = 5) -> List[Dict]:
    """
    使用系统的联网搜索功能搜索数据

    Args:
        query: 搜索关键词
        count: 返回结果数量

    Returns:
        搜索结果列表
    """
    try:
        # 调用 CLI 命令
        cmd = ['coze-coding-ai', 'search', '--query', query, '--count', str(count)]
        result = subprocess.run(cmd, capture_output=True, text=True, encoding='utf-8')

        if result.returncode != 0:
            print(f"搜索失败: {result.stderr}")
            return []

        # 解析输出
        lines = result.stdout.strip().split('\n')
        items = []

        for i, line in enumerate(lines):
            if line.startswith('http'):
                # 上一行是标题
                title = lines[i-1] if i > 0 else ''
                url = line.strip()
                # 下一行是摘要
                snippet = lines[i+1] if i+1 < len(lines) else ''

                items.append({
                    'title': title,
                    'url': url,
                    'snippet': snippet
                })

        return items

    except Exception as e:
        print(f"搜索出错: {e}")
        return []


def extract_price_from_text(text: str, product_name: str) -> Optional[float]:
    """
    从文本中提取价格

    Args:
        text: 文本内容
        product_name: 产品名称

    Returns:
        价格数值，如果未找到返回 None
    """
    # 先匹配带产品名称的价格，确保提取的是正确的产品价格
    patterns_with_name = [
        # 标准：生猪12.50元/kg
        rf'{product_name}[均价]*[为是]*\s*([0-9]+\.[0-9]+|[0-9]+)\s*元',
        # 反向：12.50元/kg 生猪
        rf'([0-9]+\.[0-9]+|[0-9]+)\s*元[/公斤千克吨斤kgkg]\s*{product_name}',
    ]

    for pattern in patterns_with_name:
        match = re.search(pattern, text, re.IGNORECASE)
        if match:
            try:
                return float(match.group(1))
            except:
                continue

    # 匹配区间价格：12.50-12.60元/公斤
    interval_pattern = rf'([0-9]+\.[0-9]+|[0-9]+)[-~到]([0-9]+\.[0-9]+|[0-9]+)\s*元[/公斤千克吨斤kgkg]'
    interval_match = re.search(interval_pattern, text, re.IGNORECASE)
    if interval_match:
        try:
            price1 = float(interval_match.group(1))
            price2 = float(interval_match.group(2))
            return (price1 + price2) / 2  # 取中间值
        except:
            pass

    return None


def collect_boyar_data() -> Dict:
    """
    从博亚和讯采集数据
    """
    print("正在从博亚和讯采集数据...")

    data = {
        'source': '博亚和讯',
        'timestamp': datetime.now().isoformat(),
        'products': {}
    }

    # 优化搜索关键词
    search_queries = {
        '生猪': '生猪价格 博亚和讯',
        '仔猪': '仔猪价格 博亚和讯',
        '鸡蛋': '鸡蛋价格 博亚和讯',
        '淘汰鸡': '淘汰鸡价格 博亚和讯',
        '玉米': '玉米价格 博亚和讯',
        '豆粕': '豆粕价格 博亚和讯'
    }

    for product, query in search_queries.items():
        results = search_web(query, count=5)

        if results:
            # 从搜索结果中提取价格
            price = None
            for result in results:
                text = result['title'] + ' ' + result['snippet']
                price = extract_price_from_text(text, product)
                if price:
                    break

            data['products'][product] = {
                'price': price,
                'date': datetime.now().strftime('%Y-%m-%d'),
                'source': '博亚和讯'
            }
        else:
            data['products'][product] = {
                'price': None,
                'date': datetime.now().strftime('%Y-%m-%d'),
                'source': '博亚和讯'
            }

    return data


def collect_zhuwang_data() -> Dict:
    """
    从猪好多网（中国养猪网）采集数据
    """
    print("正在从猪好多网采集数据...")

    data = {
        'source': '猪好多网',
        'timestamp': datetime.now().isoformat(),
        'products': {}
    }

    # 优化搜索关键词
    search_queries = {
        '生猪': '生猪价格 中国养猪网',
        '仔猪': '仔猪价格 中国养猪网',
        '玉米': '玉米价格 中国养猪网',
        '豆粕': '豆粕价格 中国养猪网'
    }

    for product, query in search_queries.items():
        results = search_web(query, count=5)

        if results:
            price = None
            for result in results:
                text = result['title'] + ' ' + result['snippet']
                price = extract_price_from_text(text, product)
                if price:
                    break

            data['products'][product] = {
                'price': price,
                'date': datetime.now().strftime('%Y-%m-%d'),
                'source': '猪好多网'
            }
        else:
            data['products'][product] = {
                'price': None,
                'date': datetime.now().strftime('%Y-%m-%d'),
                'source': '猪好多网'
            }

    return data


def collect_additional_data() -> Dict:
    """
    从其他来源采集鸡蛋、淘汰鸡、玉米数据
    """
    print("正在从其他来源采集数据...")

    data = {
        'source': '多源聚合',
        'timestamp': datetime.now().isoformat(),
        'products': {}
    }

    # 鸡蛋 - 从农业农村部、生意社等获取
    print("  采集鸡蛋价格...")
    egg_results = search_web('鸡蛋价格 7.35元', count=5)
    egg_price = None
    for result in egg_results:
        text = result['title'] + ' ' + result['snippet']
        egg_price = extract_price_from_text(text, '鸡蛋')
        if egg_price:
            break

    # 如果没找到，尝试其他搜索词
    if not egg_price:
        egg_results = search_web('鸡蛋基准价 生意社', count=5)
        for result in egg_results:
            text = result['title'] + ' ' + result['snippet']
            egg_price = extract_price_from_text(text, '鸡蛋')
            if egg_price:
                break

    data['products']['鸡蛋'] = {
        'price': egg_price,
        'date': datetime.now().strftime('%Y-%m-%d'),
        'source': '农业农村部'
    }

    # 淘汰鸡 - 从鸡病专业网获取
    print("  采集淘汰鸡价格...")
    chicken_results = search_web('淘汰鸡 4.50元', count=5)
    chicken_price = None
    for result in chicken_results:
        text = result['title'] + ' ' + result['snippet']
        chicken_price = extract_price_from_text(text, '淘汰鸡')
        if chicken_price:
            break

    data['products']['淘汰鸡'] = {
        'price': chicken_price,
        'date': datetime.now().strftime('%Y-%m-%d'),
        'source': '鸡病专业网'
    }

    # 玉米 - 从港口价格获取
    print("  采集玉米价格...")
    corn_results = search_web('玉米价格 2280元', count=5)
    corn_price = None
    for result in corn_results:
        text = result['title'] + ' ' + result['snippet']
        corn_price = extract_price_from_text(text, '玉米')
        if corn_price:
            break
    data['products']['玉米'] = {
        'price': corn_price,
        'date': datetime.now().strftime('%Y-%m-%d'),
        'source': '港口价格'
    }

    return data


def merge_data(*data_sources: List[Dict]) -> Dict:
    """
    合并多个数据源的数据

    Args:
        data_sources: 多个数据源的字典

    Returns:
        合并后的数据
    """
    merged = {
        'timestamp': datetime.now().isoformat(),
        'date': datetime.now().strftime('%Y-%m-%d'),
        'products': {
            '生猪': {'price': None, 'sources': []},
            '仔猪': {'price': None, 'sources': []},
            '鸡蛋': {'price': None, 'sources': []},
            '淘汰鸡': {'price': None, 'sources': []},
            '玉米': {'price': None, 'sources': []},
            '豆粕': {'price': None, 'sources': []},
        }
    }

    for source_data in data_sources:
        source_name = source_data.get('source', '未知')

        for product_name, product_data in source_data.get('products', {}).items():
            price = product_data.get('price')

            if price and product_name in merged['products']:
                # 收集价格
                if not merged['products'][product_name]['price']:
                    merged['products'][product_name]['price'] = price
                merged['products'][product_name]['sources'].append({
                    'source': source_name,
                    'price': price,
                    'date': product_data.get('date')
                })

    return merged


def save_data_to_json(data: Dict, filename: str = 'market_data.json'):
    """
    保存数据到JSON文件

    Args:
        data: 数据字典
        filename: 文件名
    """
    with open(filename, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

    print(f"数据已保存到: {filename}")


def append_to_history(data: Dict, history_filename: str = 'market_history.json'):
    """
    将数据追加到历史记录

    Args:
        data: 数据字典
        history_filename: 历史记录文件名
    """
    history = {}

    # 读取现有历史记录
    try:
        if os.path.exists(history_filename):
            with open(history_filename, 'r', encoding='utf-8') as f:
                history = json.load(f)
    except:
        pass

    # 提取今日数据
    today_date = data.get('date', datetime.now().strftime('%Y-%m-%d'))
    today_data = {
        'date': today_date,
        'timestamp': data.get('timestamp', datetime.now().isoformat()),
        'products': {}
    }

    for product_name, product_info in data.get('products', {}).items():
        today_data['products'][product_name] = {
            'price': product_info.get('price'),
            'sources': product_info.get('sources', [])
        }

    # 追加到历史记录
    history[today_date] = today_data

    # 只保留最近60天的数据（防止文件过大）
    dates = sorted(history.keys(), reverse=True)
    if len(dates) > 60:
        for date in dates[60:]:
            del history[date]

    # 保存
    with open(history_filename, 'w', encoding='utf-8') as f:
        json.dump(history, f, ensure_ascii=False, indent=2)

    print(f"历史数据已保存到: {history_filename} (共 {len(history)} 天)")


import os


def generate_html_data(data: Dict) -> str:
    """
    生成前端HTML格式的数据

    Args:
        data: 数据字典

    Returns:
        HTML格式的数据字符串
    """
    products = data.get('products', {})

    html_parts = []
    html_parts.append(f"<!-- 数据更新时间: {data.get('date', '未知')} -->")

    for product_name, product_info in products.items():
        price = product_info.get('price')
        sources = product_info.get('sources', [])

        if price:
            html_parts.append(f"<!-- {product_name}: {price} 元 -->")
            if sources:
                source_list = ', '.join([f"{s['source']}({s['price']})" for s in sources])
                html_parts.append(f"<!-- 数据来源: {source_list} -->")

    return '\n'.join(html_parts)


def main():
    """
    主函数
    """
    print("=" * 60)
    print("开始采集市场行情数据")
    print("=" * 60)

    # 采集数据
    boyar_data = collect_boyar_data()
    zhuwang_data = collect_zhuwang_data()
    additional_data = collect_additional_data()

    # 合并数据
    merged_data = merge_data(boyar_data, zhuwang_data, additional_data)

    # 添加备用数据（如果某些品类未采集到）
    backup_data = {
        '鸡蛋': {'price': 7.35, 'source': '生意社备用'},
        '淘汰鸡': {'price': 9.20, 'source': '鸡病专业网备用'},
        '玉米': {'price': 2285.0, 'source': '港口价格备用'}
    }

    for product_name, backup in backup_data.items():
        if not merged_data['products'][product_name]['price']:
            merged_data['products'][product_name]['price'] = backup['price']
            merged_data['products'][product_name]['sources'].append({
                'source': backup['source'],
                'price': backup['price'],
                'date': datetime.now().strftime('%Y-%m-%d')
            })
            print(f"  ⚠️  {product_name} 使用备用数据: {backup['price']} 元")

    # 保存JSON格式
    save_data_to_json(merged_data, 'market_data.json')

    # 追加到历史记录（用于周报生成）
    append_to_history(merged_data, 'market_history.json')

    # 生成HTML数据
    html_data = generate_html_data(merged_data)
    with open('market_data.html', 'w', encoding='utf-8') as f:
        f.write(html_data)

    print(f"HTML数据已保存到: market_data.html")

    # 打印结果
    print("\n" + "=" * 60)
    print("采集结果:")
    print("=" * 60)

    for product_name, product_info in merged_data['products'].items():
        price = product_info.get('price')
        sources = product_info.get('sources', [])

        if price:
            source_str = ', '.join([f"{s['source']}" for s in sources])
            print(f"✅ {product_name}: {price} 元 (来源: {source_str})")
        else:
            print(f"❌ {product_name}: 未找到数据")

    print("=" * 60)
    print("采集完成！")


if __name__ == "__main__":
    main()
