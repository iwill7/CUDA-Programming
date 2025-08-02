#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
四面开敞的公路收费站屋面风压风吸体型系数计算工具
Wind Pressure and Wind Suction Shape Coefficients Calculator for Highway Toll Station Roofs

本工具基于中国建筑荷载规范GB50009-2012和工程实践经验，
计算四面开敞的公路收费站屋面的风压风吸体型系数。
"""

import math
import numpy as np
import matplotlib.pyplot as plt
from typing import Dict, List, Tuple, Optional
import json

class WindCoefficientCalculator:
    """四面开敞公路收费站屋面风压风吸体型系数计算器"""
    
    def __init__(self):
        """初始化计算器"""
        # 基本参数
        self.g = 9.81  # 重力加速度 m/s²
        
        # 风压体型系数参考值（基于GB50009-2012和工程经验）
        self.shape_coefficients = {
            "flat_roof": {
                "windward_edge": 0.8,      # 迎风边缘
                "leeward_edge": -0.5,      # 背风边缘
                "side_edge": -0.7,         # 侧边边缘
                "center": -0.2,            # 中心区域
                "corner": -1.0             # 角部区域
            },
            "gable_roof": {
                "windward_slope": 0.3,     # 迎风坡面
                "leeward_slope": -0.6,     # 背风坡面
                "ridge": -0.8,             # 屋脊
                "eave": -0.5               # 屋檐
            },
            "arch_roof": {
                "windward_arc": 0.2,       # 迎风弧面
                "leeward_arc": -0.6,       # 背风弧面
                "top": -0.4,               # 顶部
                "base": -0.3               # 底部
            }
        }
        
        # 四面开敞修正系数
        self.open_correction = {
            "windward_open": 1.2,          # 迎风面开敞
            "leeward_open": 0.8,           # 背风面开敞
            "side_open": 0.9,              # 侧面开敞
            "all_open": 1.0                # 四面开敞
        }
        
        # 高度修正系数
        self.height_correction = {
            "ground_level": 1.0,           # 地面层
            "elevated": 1.1,               # 架空层
            "high_elevated": 1.2           # 高架层
        }
        
    def calculate_basic_wind_pressure(self, wind_speed: float, 
                                    altitude: float = 0, 
                                    temperature: float = 15) -> float:
        """
        计算基本风压
        
        Args:
            wind_speed: 设计风速 (m/s)
            altitude: 海拔高度 (m)
            temperature: 温度 (°C)
            
        Returns:
            基本风压 (kN/m²)
        """
        # 空气密度计算 (kg/m³)
        # 考虑海拔和温度影响
        rho_0 = 1.225  # 标准大气压下空气密度
        pressure_ratio = math.exp(-altitude / 8000)  # 压力随高度变化
        temp_ratio = (273.15 + 15) / (273.15 + temperature)  # 温度修正
        rho = rho_0 * pressure_ratio * temp_ratio
        
        # 基本风压计算
        q0 = 0.5 * rho * wind_speed**2 / 1000  # 转换为 kN/m²
        
        return q0
    
    def get_shape_coefficient(self, roof_type: str, position: str, 
                            wind_direction: str = "normal") -> float:
        """
        获取体型系数
        
        Args:
            roof_type: 屋面类型 ("flat_roof", "gable_roof", "arch_roof")
            position: 位置 ("windward_edge", "leeward_edge", "center", etc.)
            wind_direction: 风向 ("normal", "oblique", "diagonal")
            
        Returns:
            体型系数
        """
        base_coefficient = self.shape_coefficients[roof_type][position]
        
        # 风向修正
        if wind_direction == "oblique":
            base_coefficient *= 0.9
        elif wind_direction == "diagonal":
            base_coefficient *= 0.8
            
        return base_coefficient
    
    def calculate_wind_pressure(self, wind_speed: float, roof_type: str,
                              roof_height: float = 5.0, roof_length: float = 20.0,
                              roof_width: float = 15.0, wind_direction: str = "normal",
                              altitude: float = 0, temperature: float = 15) -> Dict:
        """
        计算屋面各区域的风压
        
        Args:
            wind_speed: 设计风速 (m/s)
            roof_type: 屋面类型
            roof_height: 屋面高度 (m)
            roof_length: 屋面长度 (m)
            roof_width: 屋面宽度 (m)
            wind_direction: 风向
            altitude: 海拔高度 (m)
            temperature: 温度 (°C)
            
        Returns:
            包含各区域风压的字典
        """
        # 基本风压
        q0 = self.calculate_basic_wind_pressure(wind_speed, altitude, temperature)
        
        # 高度修正系数
        if roof_height <= 3:
            height_corr = self.height_correction["ground_level"]
        elif roof_height <= 10:
            height_corr = self.height_correction["elevated"]
        else:
            height_corr = self.height_correction["high_elevated"]
        
        # 四面开敞修正
        open_corr = self.open_correction["all_open"]
        
        # 计算各区域风压
        pressures = {}
        
        if roof_type == "flat_roof":
            positions = ["windward_edge", "leeward_edge", "side_edge", "center", "corner"]
        elif roof_type == "gable_roof":
            positions = ["windward_slope", "leeward_slope", "ridge", "eave"]
        elif roof_type == "arch_roof":
            positions = ["windward_arc", "leeward_arc", "top", "base"]
        else:
            raise ValueError(f"不支持的屋面类型: {roof_type}")
        
        for position in positions:
            shape_coeff = self.get_shape_coefficient(roof_type, position, wind_direction)
            pressure = q0 * shape_coeff * height_corr * open_corr
            pressures[position] = {
                "shape_coefficient": shape_coeff,
                "pressure": pressure,
                "pressure_kpa": abs(pressure)
            }
        
        return {
            "basic_wind_pressure": q0,
            "height_correction": height_corr,
            "open_correction": open_corr,
            "pressures": pressures,
            "parameters": {
                "wind_speed": wind_speed,
                "roof_type": roof_type,
                "roof_height": roof_height,
                "roof_length": roof_length,
                "roof_width": roof_width,
                "wind_direction": wind_direction,
                "altitude": altitude,
                "temperature": temperature
            }
        }
    
    def calculate_wind_load(self, wind_pressure_result: Dict) -> Dict:
        """
        计算风荷载
        
        Args:
            wind_pressure_result: 风压计算结果
            
        Returns:
            风荷载计算结果
        """
        params = wind_pressure_result["parameters"]
        roof_area = params["roof_length"] * params["roof_width"]
        
        loads = {}
        total_load = 0
        
        for position, pressure_data in wind_pressure_result["pressures"].items():
            # 根据位置确定面积分配
            if position in ["windward_edge", "leeward_edge"]:
                area_ratio = 0.2  # 边缘区域占20%
            elif position in ["side_edge"]:
                area_ratio = 0.3  # 侧边区域占30%
            elif position in ["center"]:
                area_ratio = 0.25  # 中心区域占25%
            elif position in ["corner"]:
                area_ratio = 0.05  # 角部区域占5%
            else:
                area_ratio = 0.25  # 其他区域平均分配
            
            area = roof_area * area_ratio
            load = pressure_data["pressure"] * area
            
            loads[position] = {
                "area": area,
                "load": load,
                "load_kn": abs(load)
            }
            
            total_load += load
        
        return {
            "total_roof_area": roof_area,
            "total_wind_load": total_load,
            "loads": loads
        }
    
    def generate_pressure_distribution_plot(self, wind_pressure_result: Dict, 
                                          save_path: Optional[str] = None):
        """
        生成风压分布图
        
        Args:
            wind_pressure_result: 风压计算结果
            save_path: 保存路径
        """
        params = wind_pressure_result["parameters"]
        pressures = wind_pressure_result["pressures"]
        
        # 创建图形
        fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(15, 6))
        
        # 左图：风压分布
        positions = list(pressures.keys())
        pressure_values = [pressures[pos]["pressure"] for pos in positions]
        colors = ['red' if p < 0 else 'blue' for p in pressure_values]
        
        bars1 = ax1.bar(positions, pressure_values, color=colors, alpha=0.7)
        ax1.set_title(f'屋面风压分布图\n{params["roof_type"]} - 风速: {params["wind_speed"]} m/s')
        ax1.set_ylabel('风压 (kN/m²)')
        ax1.set_xlabel('位置')
        ax1.grid(True, alpha=0.3)
        
        # 添加数值标签
        for bar, value in zip(bars1, pressure_values):
            height = bar.get_height()
            ax1.text(bar.get_x() + bar.get_width()/2., height + (0.01 if height > 0 else -0.01),
                    f'{value:.3f}', ha='center', va='bottom' if height > 0 else 'top')
        
        # 右图：体型系数
        shape_coeffs = [pressures[pos]["shape_coefficient"] for pos in positions]
        bars2 = ax2.bar(positions, shape_coeffs, color='green', alpha=0.7)
        ax2.set_title('体型系数分布')
        ax2.set_ylabel('体型系数')
        ax2.set_xlabel('位置')
        ax2.grid(True, alpha=0.3)
        
        # 添加数值标签
        for bar, value in zip(bars2, shape_coeffs):
            height = bar.get_height()
            ax2.text(bar.get_x() + bar.get_width()/2., height + (0.01 if height > 0 else -0.01),
                    f'{value:.2f}', ha='center', va='bottom' if height > 0 else 'top')
        
        plt.tight_layout()
        
        if save_path:
            plt.savefig(save_path, dpi=300, bbox_inches='tight')
        
        plt.show()
    
    def export_results(self, wind_pressure_result: Dict, wind_load_result: Dict,
                      filename: str = "wind_analysis_results.json"):
        """
        导出计算结果到JSON文件
        
        Args:
            wind_pressure_result: 风压计算结果
            wind_load_result: 风荷载计算结果
            filename: 文件名
        """
        export_data = {
            "wind_pressure_analysis": wind_pressure_result,
            "wind_load_analysis": wind_load_result,
            "summary": {
                "max_pressure": max([abs(p["pressure"]) for p in wind_pressure_result["pressures"].values()]),
                "min_pressure": min([p["pressure"] for p in wind_pressure_result["pressures"].values()]),
                "total_load": wind_load_result["total_wind_load"],
                "roof_area": wind_load_result["total_roof_area"]
            }
        }
        
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(export_data, f, ensure_ascii=False, indent=2)
        
        print(f"结果已导出到: {filename}")

def main():
    """主函数 - 演示计算器使用"""
    print("四面开敞的公路收费站屋面风压风吸体型系数计算工具")
    print("=" * 60)
    
    # 创建计算器实例
    calculator = WindCoefficientCalculator()
    
    # 示例参数
    wind_speed = 25.0  # m/s
    roof_type = "flat_roof"
    roof_height = 6.0  # m
    roof_length = 25.0  # m
    roof_width = 18.0  # m
    
    print(f"计算参数:")
    print(f"  设计风速: {wind_speed} m/s")
    print(f"  屋面类型: {roof_type}")
    print(f"  屋面高度: {roof_height} m")
    print(f"  屋面尺寸: {roof_length} m × {roof_width} m")
    print()
    
    # 计算风压
    wind_pressure_result = calculator.calculate_wind_pressure(
        wind_speed=wind_speed,
        roof_type=roof_type,
        roof_height=roof_height,
        roof_length=roof_length,
        roof_width=roof_width
    )
    
    # 计算风荷载
    wind_load_result = calculator.calculate_wind_load(wind_pressure_result)
    
    # 显示结果
    print("风压计算结果:")
    print("-" * 40)
    print(f"基本风压: {wind_pressure_result['basic_wind_pressure']:.3f} kN/m²")
    print(f"高度修正系数: {wind_pressure_result['height_correction']:.2f}")
    print(f"开敞修正系数: {wind_pressure_result['open_correction']:.2f}")
    print()
    
    print("各区域风压:")
    for position, data in wind_pressure_result["pressures"].items():
        print(f"  {position}: {data['pressure']:.3f} kN/m² (体型系数: {data['shape_coefficient']:.2f})")
    
    print()
    print("风荷载计算结果:")
    print("-" * 40)
    print(f"屋面总面积: {wind_load_result['total_roof_area']:.1f} m²")
    print(f"总风荷载: {wind_load_result['total_wind_load']:.1f} kN")
    print()
    
    print("各区域风荷载:")
    for position, data in wind_load_result["loads"].items():
        print(f"  {position}: {data['load']:.1f} kN (面积: {data['area']:.1f} m²)")
    
    # 生成图表
    calculator.generate_pressure_distribution_plot(wind_pressure_result)
    
    # 导出结果
    calculator.export_results(wind_pressure_result, wind_load_result)

if __name__ == "__main__":
    main()