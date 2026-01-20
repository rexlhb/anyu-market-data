#!/usr/bin/env node
/**
 * 给HTML文件添加数据加载功能
 * 运行方法：node add-data-loading.js
 */

const fs = require('fs');
const path = require('path');

// 读取HTML文件
const htmlPath = path.join(__dirname, '../netlify-deploy/index.html');
let html = fs.readFileSync(htmlPath, 'utf-8');

// 在</body>标签前添加JavaScript代码
const scriptCode = `
    <!-- 自动加载数据的JavaScript代码 -->
    <script>
    (function() {
        // 配置：GitHub用户名（请修改为你的GitHub用户名）
        const GITHUB_USERNAME = 'YOUR_GITHUB_USERNAME';
        const REPO_NAME = 'anyu-market-data';

        // 产品价格映射（从JSON中的产品名到HTML中的数据属性）
        const productMap = {
            '生猪': { selector: '.product-name' },
            '仔猪': { selector: '.product-name' },
            '鸡蛋': { selector: '.product-name' },
            '淘汰鸡': { selector: '.product-name' },
            '玉米': { selector: '.product-name' },
            '豆粕': { selector: '.product-name' }
        };

        // 从GitHub加载JSON数据
        async function loadMarketData() {
            try {
                const url = \`https://raw.githubusercontent.com/\${GITHUB_USERNAME}/\${REPO_NAME}/main/backend/market_data.json\`;
                const response = await fetch(url);

                if (!response.ok) {
                    console.error('加载数据失败:', response.status);
                    return;
                }

                const data = await response.json();
                updatePrices(data);
                updateLastUpdated(data.date);

            } catch (error) {
                console.error('加载数据出错:', error);
            }
        }

        // 更新页面上的价格数据
        function updatePrices(data) {
            const products = data.products;

            // 遍历所有产品模块
            document.querySelectorAll('.module').forEach(module => {
                const productName = module.querySelector('.product-name')?.textContent.trim();

                if (productName && products[productName]) {
                    const price = products[productName].price;

                    if (price) {
                        // 更新全国价格
                        const priceElement = module.querySelector('.national-price');
                        if (priceElement) {
                            priceElement.textContent = formatPrice(productName, price);
                        }

                        // 添加数据来源提示
                        const sources = products[productName].sources || [];
                        if (sources.length > 0) {
                            const sourceNames = sources.map(s => s.source).join(', ');
                            addSourceTooltip(module, productName, price, sourceNames);
                        }
                    }
                }
            });
        }

        // 格式化价格（根据产品类型决定小数位数）
        function formatPrice(productName, price) {
            // 生猪、仔猪、鸡蛋、淘汰鸡保留2位小数
            // 玉米、豆粕保留整数
            const decimalProducts = ['生猪', '仔猪', '鸡蛋', '淘汰鸡'];
            const integerProducts = ['玉米', '豆粕'];

            if (decimalProducts.includes(productName)) {
                return price.toFixed(2);
            } else if (integerProducts.includes(productName)) {
                return Math.round(price).toString();
            } else {
                return price.toString();
            }
        }

        // 更新最后更新时间
        function updateLastUpdated(date) {
            const dateElements = document.querySelectorAll('.update-text');
            dateElements.forEach(el => {
                el.textContent = '最后更新: ' + date;
            });
        }

        // 添加数据来源提示
        function addSourceTooltip(module, productName, price, sources) {
            // 可以在这里添加更多交互功能，比如点击显示数据来源
            console.log(\`\${productName}: \${price} (来源: \${sources})\`);
        }

        // 页面加载完成后自动运行
        if (document.readyState === 'loading') {
            document.addEventListener('DOMContentLoaded', loadMarketData);
        } else {
            loadMarketData();
        }

        console.log('数据加载功能已启用');
    })();
    </script>
`;

// 在</body>前插入脚本代码
if (html.includes('</body>')) {
    html = html.replace('</body>', scriptCode + '</body>');
    fs.writeFileSync(htmlPath, html, 'utf-8');
    console.log('✅ 数据加载功能已添加到 index.html');
    console.log('⚠️  请将 GITHUB_USERNAME 修改为你的GitHub用户名！');
} else {
    console.error('❌ 未找到 </body> 标签');
}
