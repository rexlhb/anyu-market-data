// 动态加载市场数据并更新页面
class MarketDataLoader {
    constructor() {
        this.data = null;
        this.githubRawUrl = 'https://raw.githubusercontent.com/rexlhb/anyu-market-data/main/market.json';
        this.storageUrl = 'https://coze-coding-project.tos.coze.site/coze_storage_7592784756627144744/anyu-market/market.json';
    }

    // 尝试从多个数据源加载数据
    async loadData() {
        const sources = [
            this.githubRawUrl,
            this.storageUrl,
            './market.json' // 本地文件作为最后备选
        ];

        for (const source of sources) {
            try {
                console.log(`尝试从 ${source} 加载数据...`);
                const response = await fetch(source);

                if (!response.ok) {
                    throw new Error(`HTTP error! status: ${response.status}`);
                }

                this.data = await response.json();
                console.log('数据加载成功！', this.data);
                return this.data;
            } catch (error) {
                console.warn(`从 ${source} 加载数据失败:`, error.message);
                continue;
            }
        }

        console.error('所有数据源均加载失败，使用备用数据');
        return this.getBackupData();
    }

    // 备用数据（当所有数据源都无法访问时使用）
    getBackupData() {
        return {
            update_date: new Date().toISOString().split('T')[0],
            update_time: "09:00",
            products: {
                pig: {
                    name: "生猪",
                    unit: "元/公斤",
                    national_price: 12.73,
                    national_change: 0.23,
                    national_change_ratio: 1.84,
                    regions: {
                        "河北": {"price": 12.40, "change": -0.11},
                        "山东": {"price": 12.72, "change": 0.09},
                        "河南": {"price": 12.65, "change": -0.05},
                        "湖北": {"price": 12.78, "change": 0.33},
                        "四川": {"price": 13.03, "change": 0.23},
                        "黑龙江": {"price": 12.18, "change": -0.00},
                        "陕西": {"price": 12.53, "change": -0.07},
                        "甘肃": {"price": 12.33, "change": -0.20},
                        "广西": {"price": 13.13, "change": 0.28},
                        "广东": {"price": 13.33, "change": 0.31},
                        "江西": {"price": 12.88, "change": -0.05},
                        "福建": {"price": 13.08, "change": 0.35}
                    }
                },
                piglet: {
                    name: "仔猪",
                    unit: "元/公斤",
                    national_price: 21.33,
                    national_change: 0.97,
                    national_change_ratio: 4.76,
                    regions: {
                        "河北": {"price": 20.82, "change": 1.09},
                        "山东": {"price": 21.42, "change": 1.02},
                        "河南": {"price": 21.07, "change": 0.96},
                        "湖北": {"price": 21.71, "change": 1.35},
                        "四川": {"price": 22.02, "change": 0.84},
                        "黑龙江": {"price": 20.47, "change": 1.14},
                        "陕西": {"price": 21.17, "change": 0.99},
                        "甘肃": {"price": 20.92, "change": 1.06},
                        "广西": {"price": 21.87, "change": 0.92},
                        "广东": {"price": 22.17, "change": 0.79},
                        "江西": {"price": 21.62, "change": 0.94},
                        "福建": {"price": 21.82, "change": 1.01}
                    }
                },
                soybean: {
                    name: "豆粕",
                    unit: "元/吨",
                    national_price: 3080,
                    national_change: -165,
                    national_change_ratio: -5.08,
                    regions: {
                        "河北": {"price": 3075, "change": -155},
                        "山东": {"price": 3090, "change": -140},
                        "河南": {"price": 3085, "change": -145},
                        "湖北": {"price": 3100, "change": -130},
                        "四川": {"price": 3105, "change": -125},
                        "黑龙江": {"price": 3070, "change": -160},
                        "陕西": {"price": 3065, "change": -170},
                        "甘肃": {"price": 3060, "change": -175},
                        "广西": {"price": 3110, "change": -120},
                        "广东": {"price": 3120, "change": -115},
                        "江西": {"price": 3095, "change": -135},
                        "福建": {"price": 3115, "change": -110}
                    }
                }
            }
        };
    }

    // 格式化价格显示
    formatPrice(value, productKey) {
        if (productKey === 'corn' || productKey === 'soybean') {
            return value.toString(); // 整数显示
        }
        return value.toFixed(2); // 保留2位小数
    }

    // 格式化涨跌显示
    formatChange(change) {
        const sign = change >= 0 ? '+' : '';
        return sign + change;
    }

    // 格式化涨跌幅显示
    formatChangeRatio(ratio) {
        const sign = ratio >= 0 ? '+' : '';
        return `(${sign}${ratio.toFixed(2)}%)`;
    }

    // 获取涨跌样式类名
    getChangeClass(change) {
        if (change > 0) return 'up';
        if (change < 0) return 'down';
        return 'flat';
    }

    // 更新页面显示
    updatePage() {
        if (!this.data) {
            console.error('没有数据可以更新');
            return;
        }

        // 更新日期和时间
        this.updateDateTime();

        // 更新所有产品模块
        this.updateProductModule('pig', 'pig');
        this.updateProductModule('piglet', 'piglet');
        this.updateProductModule('egg', 'egg');
        this.updateProductModule('hen', 'hen');
        this.updateProductModule('corn', 'corn');
        this.updateProductModule('soybean', 'soybean');
    }

    // 更新日期和时间
    updateDateTime() {
        const dateEl = document.querySelector('.date-text');
        if (dateEl && this.data.update_date) {
            dateEl.textContent = this.data.update_date;
        }
    }

    // 更新单个产品模块
    updateProductModule(productKey, moduleName) {
        const product = this.data.products[productKey];
        if (!product) {
            console.warn(`找不到产品数据: ${productKey}`);
            return;
        }

        // 更新产品名称和单位
        const productNameEl = document.querySelector(`.${moduleName} .product-name`);
        const unitEl = document.querySelector(`.${moduleName} .unit`);
        if (productNameEl) productNameEl.textContent = product.name;
        if (unitEl) unitEl.textContent = product.unit;

        // 更新全国均价
        const nationalPriceEl = document.querySelector(`.${moduleName} .national-price`);
        const nationalChangeEl = document.querySelector(`.${moduleName} .national-change`);
        const nationalRatioEl = document.querySelector(`.${moduleName} .national-ratio`);

        if (nationalPriceEl) {
            nationalPriceEl.textContent = this.formatPrice(product.national_price, productKey);
        }
        if (nationalChangeEl) {
            nationalChangeEl.textContent = this.formatChange(product.national_change);
            nationalChangeEl.className = `national-change ${this.getChangeClass(product.national_change)}`;
        }
        if (nationalRatioEl) {
            nationalRatioEl.textContent = this.formatChangeRatio(product.national_change_ratio);
            nationalRatioEl.className = `national-ratio ${this.getChangeClass(product.national_change)}`;
        }

        // 更新区域数据
        const regionItems = document.querySelectorAll(`.${moduleName} .region-item`);
        if (regionItems.length > 0 && product.regions) {
            const regionNames = Object.keys(product.regions);
            regionItems.forEach((item, index) => {
                if (index < regionNames.length) {
                    const regionName = regionNames[index];
                    const regionData = product.regions[regionName];

                    const nameEl = item.querySelector('.region-name');
                    const priceEl = item.querySelector('.region-price');
                    const changeEl = item.querySelector('.region-change');

                    if (nameEl) nameEl.textContent = regionName;
                    if (priceEl) priceEl.textContent = this.formatPrice(regionData.price, productKey);
                    if (changeEl) {
                        changeEl.textContent = this.formatChange(regionData.change);
                        changeEl.className = `region-change ${this.getChangeClass(regionData.change)}`;
                    }
                }
            });
        }
    }

    // 初始化加载
    async init() {
        console.log('开始加载市场数据...');
        await this.loadData();
        this.updatePage();
        console.log('页面更新完成！');
    }
}

// 页面加载完成后自动执行
document.addEventListener('DOMContentLoaded', async () => {
    const loader = new MarketDataLoader();
    await loader.init();
});
