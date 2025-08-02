# 四面开敞公路收费站屋面风压风吸体型系数计算工具

## 概述

本工具用于计算四面开敞的公路收费站屋面的风压风吸体型系数，基于中国建筑荷载规范GB50009-2012和工程实践经验开发。

## 功能特点

- 支持平屋面、坡屋面、拱形屋面三种屋面类型
- 考虑四面开敞结构的特殊性
- 自动计算各区域风压和风荷载
- 生成可视化图表
- 导出详细计算结果

## 安装依赖

```bash
pip install -r requirements.txt
```

## 使用方法

### 基本使用

```python
from wind_coefficients_calculator import WindCoefficientCalculator

# 创建计算器实例
calculator = WindCoefficientCalculator()

# 计算风压
result = calculator.calculate_wind_pressure(
    wind_speed=25.0,      # 设计风速 (m/s)
    roof_type="flat_roof", # 屋面类型
    roof_height=6.0,      # 屋面高度 (m)
    roof_length=25.0,     # 屋面长度 (m)
    roof_width=18.0,      # 屋面宽度 (m)
    wind_direction="normal", # 风向
    altitude=100,         # 海拔高度 (m)
    temperature=15        # 温度 (°C)
)

# 计算风荷载
load_result = calculator.calculate_wind_load(result)

# 生成图表
calculator.generate_pressure_distribution_plot(result)

# 导出结果
calculator.export_results(result, load_result)
```

### 运行示例

```bash
# 运行基本示例
python wind_coefficients_calculator.py

# 运行详细示例
python example_usage.py
```

## 支持的屋面类型

### 1. 平屋面 (flat_roof)
- 迎风边缘 (windward_edge)
- 背风边缘 (leeward_edge)
- 侧边边缘 (side_edge)
- 中心区域 (center)
- 角部区域 (corner)

### 2. 坡屋面 (gable_roof)
- 迎风坡面 (windward_slope)
- 背风坡面 (leeward_slope)
- 屋脊 (ridge)
- 屋檐 (eave)

### 3. 拱形屋面 (arch_roof)
- 迎风弧面 (windward_arc)
- 背风弧面 (leeward_arc)
- 顶部 (top)
- 底部 (base)

## 体型系数参考值

### 平屋面体型系数
| 位置 | 体型系数 | 说明 |
|------|----------|------|
| 迎风边缘 | +0.8 | 正压区，风直接冲击 |
| 背风边缘 | -0.5 | 负压区，风分离产生吸力 |
| 侧边边缘 | -0.7 | 负压区，侧向风作用 |
| 中心区域 | -0.2 | 轻微负压，内部风压影响 |
| 角部区域 | -1.0 | 最大负压，涡流效应 |

### 修正系数
- **高度修正系数**：根据屋面高度自动调整
- **开敞修正系数**：考虑四面开敞的影响
- **风向修正系数**：考虑风向角度的影响

## 输出结果

### 1. 控制台输出
- 基本风压
- 各区域风压和体型系数
- 总风荷载
- 各区域风荷载

### 2. 图表输出
- 风压分布图
- 体型系数分布图

### 3. JSON文件
- 详细的计算参数
- 完整的计算结果
- 汇总信息

## 技术依据

- GB50009-2012《建筑结构荷载规范》
- GB50017-2017《钢结构设计标准》
- JGJ/T 338-2014《建筑工程风洞试验规程》

## 注意事项

1. **计算精度**：体型系数取值有一定经验性，建议进行风洞试验验证
2. **安全系数**：建议采用1.4的安全系数
3. **结构设计**：重点关注负压区域的设计
4. **施工要求**：确保屋面系统的整体性和抗风性能

## 文件说明

- `wind_coefficients_calculator.py` - 主计算器类
- `example_usage.py` - 使用示例
- `wind_coefficients_technical_guide.md` - 技术指南
- `requirements.txt` - 依赖包列表
- `README_wind_calculator.md` - 本说明文件

## 示例输出

```
四面开敞的公路收费站屋面风压风吸体型系数计算工具
============================================================
计算参数:
  设计风速: 25.0 m/s
  屋面类型: flat_roof
  屋面高度: 6.0 m
  屋面尺寸: 25.0 m × 18.0 m

风压计算结果:
----------------------------------------
基本风压: 0.379 kN/m²
高度修正系数: 1.10
开敞修正系数: 1.00

各区域风压:
  windward_edge: 0.334 kN/m² (体型系数: 0.80)
  leeward_edge: -0.208 kN/m² (体型系数: -0.50)
  side_edge: -0.292 kN/m² (体型系数: -0.70)
  center: -0.083 kN/m² (体型系数: -0.20)
  corner: -0.417 kN/m² (体型系数: -1.00)

风荷载计算结果:
----------------------------------------
屋面总面积: 450.0 m²
总风荷载: -45.0 kN

各区域风荷载:
  windward_edge: 30.1 kN (面积: 90.0 m²)
  leeward_edge: -18.7 kN (面积: 90.0 m²)
  side_edge: -39.4 kN (面积: 135.0 m²)
  center: -9.4 kN (面积: 112.5 m²)
  corner: -9.4 kN (面积: 22.5 m²)
```

## 联系方式

如有问题或建议，请联系开发团队。