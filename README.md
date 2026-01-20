# 安佑预混料每日行情系统

## 系统概述

这是一个自动化采集畜牧饲料原料市场行情数据的系统，每天自动从指定网站采集最新价格数据并更新到前端页面。

## 功能特性

✅ **自动数据采集** - 每天上午9:00自动从博亚和讯、猪好多网、玄田数据采集价格
✅ **完全免费** - 使用GitHub Actions免费额度（每月2000分钟）
✅ **24小时在线** - 部署在云端，不需要本地电脑开机
✅ **多数据源** - 覆盖6大品类：生猪、仔猪、鸡蛋、淘汰鸡、玉米、豆粕
✅ **定时生成周报** - 每周自动生成Excel和TXT格式周报

## 数据来源

| 品类 | 数据来源 |
|-----|---------|
| 生猪 | 博亚和讯 |
| 仔猪 | 博亚和讯 |
| 鸡蛋 | 生意社 |
| 淘汰鸡 | 鸡病专业网 |
| 玉米 | 港口价格 |
| 豆粕 | 博亚和讯 |

## 系统架构

```
GitHub (代码仓库)
  ↓
GitHub Actions (定时任务，每天9:00运行)
  ↓
数据采集脚本 (data_collector.py)
  ↓
市场数据文件 (market_data.json)
  ↓
前端更新脚本 (update_frontend.py)
  ↓
Netlify (自动部署)
  ↓
用户访问网站
```

## 使用方法

### 方式一：自动运行（推荐）

系统每天上午9:00自动采集数据并更新网站，无需任何操作。

### 方式二：手动触发

1. 访问GitHub仓库的Actions页面
2. 选择 "Daily Data Collection" 工作流
3. 点击 "Run workflow" 按钮

### 方式三：本地运行

```bash
# 进入后端目录
cd clean-deploy/backend

# 运行数据采集
python data_collector.py

# 运行前端更新
python update_frontend.py
```

## 项目结构

```
clean-deploy/
├── backend/
│   ├── data_collector.py          # 数据采集脚本
│   ├── update_frontend.py         # 前端更新脚本
│   ├── download_server.py         # 下载服务器
│   ├── generate_weekly_documents.py  # 周报生成脚本
│   ├── scheduler.py               # 定时任务调度器
│   └── market_data.json           # 市场数据（自动生成）
├── anyu-netlify-deploy/          # 前端文件
│   ├── index.html                 # 每日行情页面
│   ├── weekly-report.html         # 每周周报页面
│   └── profile.html               # 我的页面
└── .github/
    └── workflows/
        └── daily-data-collection.yml  # GitHub Actions工作流
```

## 网站访问

- **每日行情**: https://quiet-hotteok-0d7431.netlify.app/
- **每周周报**: https://quiet-hotteok-0d7431.netlify.app/weekly-report.html
- **我的**: https://quiet-hotteok-0d7431.netlify.app/profile.html

## 技术栈

- **前端**: HTML5 + CSS3 + JavaScript
- **后端**: Python 3.11
- **数据采集**: Coze Coding AI 搜索SDK
- **自动化**: GitHub Actions
- **部署**: Netlify

## 免费额度说明

| 服务 | 免费额度 | 实际使用 | 是否够用 |
|-----|---------|---------|---------|
| GitHub Actions | 2000分钟/月 | 约30分钟/月 | ✅ 完全够用 |
| Netlify | 100GB带宽/月 | 约1GB/月 | ✅ 完全够用 |
| Coze Search | 每日限额 | 约30次/天 | ✅ 完全够用 |

## 成本预估

**实际月成本**: 0元

所有服务都在免费额度内，无需付费。

## 维护说明

系统配置完成后，基本免维护：

1. **无需干预** - 每天自动采集数据
2. **自动部署** - 数据更新后自动部署到Netlify
3. **长期稳定** - 依赖GitHub和Netlify的稳定服务

如需修改数据来源或调整采集规则，编辑 `backend/data_collector.py` 文件即可。

## 更新日志

### 2026-01-16
- ✅ 完成数据采集功能开发
- ✅ 集成3个数据源（博亚和讯、猪好多网、玄田数据）
- ✅ 配置GitHub Actions定时任务
- ✅ 实现自动前端更新
- ✅ 部署到Netlify

## 联系方式

如有问题，请通过以下方式联系：
- GitHub Issues
- 项目维护者

---

**注意**: 本系统仅供内部使用，数据仅供参考，实际交易请以当地市场为准。
