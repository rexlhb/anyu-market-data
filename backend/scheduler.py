#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
定时任务调度器
每周日中午12:00自动生成文档
"""

import schedule
import time
import logging
from datetime import datetime
from generate_weekly_documents import generate_excel_document, generate_txt_document

# 配置日志
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('scheduler.log', encoding='utf-8'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

def generate_documents():
    """生成文档的任务函数"""
    logger.info("=" * 60)
    logger.info("开始执行定时任务：生成文档")
    logger.info("=" * 60)

    try:
        # 生成Excel文档
        logger.info("正在生成Excel文档...")
        excel_filename = generate_excel_document()
        logger.info(f"✅ Excel文档已生成: {excel_filename}")

        # 生成TXT文档
        logger.info("正在生成TXT文档...")
        txt_filename = generate_txt_document()
        logger.info(f"✅ TXT文档已生成: {txt_filename}")

        logger.info("=" * 60)
        logger.info("✅ 定时任务执行完成")
        logger.info("=" * 60)

    except Exception as e:
        logger.error(f"❌ 定时任务执行失败: {str(e)}")
        raise

def run_scheduler():
    """运行定时任务调度器"""
    logger.info("=" * 60)
    logger.info("定时任务调度器已启动")
    logger.info("=" * 60)
    logger.info(f"启动时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    logger.info()

    # 配置定时任务：每周日中午12:00执行
    schedule.every().sunday.at("12:00").do(generate_documents)

    logger.info("定时任务已配置:")
    logger.info("  - 执行时间: 每周日中午12:00")
    logger.info("  - 任务内容: 生成Excel和TXT文档")
    logger.info()

    # 立即执行一次（用于测试）
    logger.info("首次启动，立即执行一次文档生成...")
    generate_documents()
    logger.info()

    # 启动调度器循环
    logger.info("调度器运行中，等待下次执行...")
    logger.info("按 Ctrl+C 停止调度器")
    logger.info("=" * 60)
    logger.info()

    try:
        while True:
            schedule.run_pending()
            time.sleep(60)  # 每分钟检查一次
    except KeyboardInterrupt:
        logger.info()
        logger.info("=" * 60)
        logger.info("调度器已停止")
        logger.info("=" * 60)

if __name__ == "__main__":
    run_scheduler()
