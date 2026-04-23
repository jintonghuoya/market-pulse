# Research Project — Multi-Source Data Analysis

投资研究数据分析平台，从多个数据源（CoStar、Wind 等）采集数据，进行分析并生成研究报告。

## 项目结构

```
data/
  costar/          # CoStar 导出数据（Excel/CSV）
  wind/            # Wind 数据（待建）
src/
  costar/          # CoStar 数据加载与分析
  wind/            # Wind 数据模块（待建）
reports/           # 生成的研究报告
templates/         # 报告模板
```

## 快速开始

```bash
# 安装依赖
pip install -r requirements.txt

# 使用 Python
from src.costar.loader import load, list_files
from src.costar.analysis import summary_stats, trend

# 列出可用数据
list_files()

# 加载所有文件
data = load()

# 加载单个文件
df = load("market_data.xlsx")
```

## 添加新数据源

1. 在 `data/` 下创建数据目录
2. 在 `src/` 下创建对应模块（loader.py + analysis.py）
3. 遵循 CoStar 模块的结构约定

## Beads Issue Tracker

This project uses **bd (beads)** for issue tracking. Run `bd prime` to see full workflow context and commands.
