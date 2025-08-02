#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
四面开敞公路收费站屋面风压计算示例
Example usage of wind coefficient calculator for highway toll station roofs
"""

from wind_coefficients_calculator import WindCoefficientCalculator

def example_flat_roof():
    """平屋面计算示例"""
    print("=" * 60)
    print("示例1: 平屋面收费站")
    print("=" * 60)
    
    calculator = WindCoefficientCalculator()
    
    # 计算参数
    result = calculator.calculate_wind_pressure(
        wind_speed=30.0,      # 设计风速 30 m/s
        roof_type="flat_roof", # 平屋面
        roof_height=8.0,      # 屋面高度 8m
        roof_length=30.0,     # 屋面长度 30m
        roof_width=20.0,      # 屋面宽度 20m
        wind_direction="normal", # 正风向
        altitude=200,         # 海拔高度 200m
        temperature=20        # 温度 20°C
    )
    
    # 计算风荷载
    load_result = calculator.calculate_wind_load(result)
    
    # 显示结果
    print(f"基本风压: {result['basic_wind_pressure']:.3f} kN/m²")
    print(f"高度修正系数: {result['height_correction']:.2f}")
    print(f"开敞修正系数: {result['open_correction']:.2f}")
    print()
    
    print("各区域风压:")
    for position, data in result["pressures"].items():
        print(f"  {position}: {data['pressure']:.3f} kN/m² (体型系数: {data['shape_coefficient']:.2f})")
    
    print(f"\n总风荷载: {load_result['total_wind_load']:.1f} kN")
    
    # 生成图表
    calculator.generate_pressure_distribution_plot(result, "flat_roof_pressure.png")
    
    return result, load_result

def example_gable_roof():
    """坡屋面计算示例"""
    print("\n" + "=" * 60)
    print("示例2: 坡屋面收费站")
    print("=" * 60)
    
    calculator = WindCoefficientCalculator()
    
    # 计算参数
    result = calculator.calculate_wind_pressure(
        wind_speed=25.0,       # 设计风速 25 m/s
        roof_type="gable_roof", # 坡屋面
        roof_height=6.0,       # 屋面高度 6m
        roof_length=25.0,      # 屋面长度 25m
        roof_width=15.0,       # 屋面宽度 15m
        wind_direction="oblique", # 斜风向
        altitude=100,          # 海拔高度 100m
        temperature=15         # 温度 15°C
    )
    
    # 计算风荷载
    load_result = calculator.calculate_wind_load(result)
    
    # 显示结果
    print(f"基本风压: {result['basic_wind_pressure']:.3f} kN/m²")
    print(f"高度修正系数: {result['height_correction']:.2f}")
    print(f"开敞修正系数: {result['open_correction']:.2f}")
    print()
    
    print("各区域风压:")
    for position, data in result["pressures"].items():
        print(f"  {position}: {data['pressure']:.3f} kN/m² (体型系数: {data['shape_coefficient']:.2f})")
    
    print(f"\n总风荷载: {load_result['total_wind_load']:.1f} kN")
    
    # 生成图表
    calculator.generate_pressure_distribution_plot(result, "gable_roof_pressure.png")
    
    return result, load_result

def example_arch_roof():
    """拱形屋面计算示例"""
    print("\n" + "=" * 60)
    print("示例3: 拱形屋面收费站")
    print("=" * 60)
    
    calculator = WindCoefficientCalculator()
    
    # 计算参数
    result = calculator.calculate_wind_pressure(
        wind_speed=35.0,      # 设计风速 35 m/s
        roof_type="arch_roof", # 拱形屋面
        roof_height=12.0,     # 屋面高度 12m
        roof_length=40.0,     # 屋面长度 40m
        roof_width=25.0,      # 屋面宽度 25m
        wind_direction="diagonal", # 对角风向
        altitude=500,         # 海拔高度 500m
        temperature=10        # 温度 10°C
    )
    
    # 计算风荷载
    load_result = calculator.calculate_wind_load(result)
    
    # 显示结果
    print(f"基本风压: {result['basic_wind_pressure']:.3f} kN/m²")
    print(f"高度修正系数: {result['height_correction']:.2f}")
    print(f"开敞修正系数: {result['open_correction']:.2f}")
    print()
    
    print("各区域风压:")
    for position, data in result["pressures"].items():
        print(f"  {position}: {data['pressure']:.3f} kN/m² (体型系数: {data['shape_coefficient']:.2f})")
    
    print(f"\n总风荷载: {load_result['total_wind_load']:.1f} kN")
    
    # 生成图表
    calculator.generate_pressure_distribution_plot(result, "arch_roof_pressure.png")
    
    return result, load_result

def compare_different_wind_speeds():
    """不同风速下的对比分析"""
    print("\n" + "=" * 60)
    print("示例4: 不同风速下的风压对比")
    print("=" * 60)
    
    calculator = WindCoefficientCalculator()
    wind_speeds = [20, 25, 30, 35, 40]  # m/s
    
    print("风速\t基本风压\t最大正压\t最大负压\t总风荷载")
    print("-" * 60)
    
    for wind_speed in wind_speeds:
        result = calculator.calculate_wind_pressure(
            wind_speed=wind_speed,
            roof_type="flat_roof",
            roof_height=6.0,
            roof_length=25.0,
            roof_width=18.0
        )
        
        load_result = calculator.calculate_wind_load(result)
        
        pressures = [data['pressure'] for data in result["pressures"].values()]
        max_positive = max(pressures)
        max_negative = min(pressures)
        
        print(f"{wind_speed}\t{result['basic_wind_pressure']:.3f}\t{max_positive:.3f}\t{max_negative:.3f}\t{load_result['total_wind_load']:.1f}")

def main():
    """主函数"""
    print("四面开敞公路收费站屋面风压计算示例")
    print("基于GB50009-2012建筑结构荷载规范")
    
    # 运行各种示例
    example_flat_roof()
    example_gable_roof()
    example_arch_roof()
    compare_different_wind_speeds()
    
    print("\n" + "=" * 60)
    print("计算完成！图表已保存为PNG文件。")
    print("详细结果请查看生成的JSON文件。")

if __name__ == "__main__":
    main()