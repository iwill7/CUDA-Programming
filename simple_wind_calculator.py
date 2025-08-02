#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
四面开敞的公路收费站屋面风压风吸体型系数计算工具（简化版）
Simplified Wind Pressure and Wind Suction Shape Coefficients Calculator for Highway Toll Station Roofs

本工具基于中国建筑荷载规范GB50009-2012和工程实践经验，
计算四面开敞的公路收费站屋面的风压风吸体型系数。
"""

import math
import json
from typing import Dict, Optional

class SimpleWindCoefficientCalculator:
    """四面开敞公路收费站屋面风压风吸体型系数计算器（简化版）"""
    
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
    
    def print_pressure_table(self, wind_pressure_result: Dict):
        """
        打印风压分布表
        
        Args:
            wind_pressure_result: 风压计算结果
        """
        params = wind_pressure_result["parameters"]
        pressures = wind_pressure_result["pressures"]
        
        print("\n" + "="*80)
        print(f"风压分布表 - {params['roof_type']} 屋面")
        print("="*80)
        print(f"设计风速: {params['wind_speed']} m/s")
        print(f"屋面尺寸: {params['roof_length']} m × {params['roof_width']} m")
        print(f"屋面高度: {params['roof_height']} m")
        print(f"基本风压: {wind_pressure_result['basic_wind_pressure']:.3f} kN/m²")
        print("-"*80)
        print(f"{'位置':<15} {'体型系数':<10} {'风压(kN/m²)':<12} {'风压(kPa)':<10}")
        print("-"*80)
        
        for position, data in pressures.items():
            print(f"{position:<15} {data['shape_coefficient']:<10.2f} {data['pressure']:<12.3f} {data['pressure_kpa']:<10.3f}")
        
        print("="*80)
    
    def print_load_table(self, wind_load_result: Dict):
        """
        打印风荷载分布表
        
        Args:
            wind_load_result: 风荷载计算结果
        """
        loads = wind_load_result["loads"]
        
        print("\n" + "="*80)
        print("风荷载分布表")
        print("="*80)
        print(f"屋面总面积: {wind_load_result['total_roof_area']:.1f} m²")
        print(f"总风荷载: {wind_load_result['total_wind_load']:.1f} kN")
        print("-"*80)
        print(f"{'位置':<15} {'面积(m²)':<10} {'风荷载(kN)':<12} {'荷载方向':<10}")
        print("-"*80)
        
        for position, data in loads.items():
            direction = "向下" if data['load'] > 0 else "向上"
            print(f"{position:<15} {data['area']:<10.1f} {data['load']:<12.1f} {direction:<10}")
        
        print("="*80)
    
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
        
        print(f"\n结果已导出到: {filename}")

def main():
    """主函数 - 演示计算器使用"""
    print("四面开敞的公路收费站屋面风压风吸体型系数计算工具（简化版）")
    print("=" * 80)
    
    # 创建计算器实例
    calculator = SimpleWindCoefficientCalculator()
    
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
    print(f"  海拔高度: 100 m")
    print(f"  温度: 15°C")
    
    # 计算风压
    wind_pressure_result = calculator.calculate_wind_pressure(
        wind_speed=wind_speed,
        roof_type=roof_type,
        roof_height=roof_height,
        roof_length=roof_length,
        roof_width=roof_width,
        altitude=100,
        temperature=15
    )
    
    # 计算风荷载
    wind_load_result = calculator.calculate_wind_load(wind_pressure_result)
    
    # 显示结果
    print("\n风压计算结果:")
    print("-" * 40)
    print(f"基本风压: {wind_pressure_result['basic_wind_pressure']:.3f} kN/m²")
    print(f"高度修正系数: {wind_pressure_result['height_correction']:.2f}")
    print(f"开敞修正系数: {wind_pressure_result['open_correction']:.2f}")
    
    # 打印详细表格
    calculator.print_pressure_table(wind_pressure_result)
    calculator.print_load_table(wind_load_result)
    
    # 导出结果
    calculator.export_results(wind_pressure_result, wind_load_result)
    
    # 总结
    print("\n" + "="*80)
    print("计算总结")
    print("="*80)
    print(f"最大风压: {max([abs(p['pressure']) for p in wind_pressure_result['pressures'].values()]):.3f} kN/m²")
    print(f"最小风压: {min([p['pressure'] for p in wind_pressure_result['pressures'].values()]):.3f} kN/m²")
    print(f"总风荷载: {wind_load_result['total_wind_load']:.1f} kN")
    print(f"屋面面积: {wind_load_result['total_roof_area']:.1f} m²")
    
    # 设计建议
    print("\n设计建议:")
    print("1. 重点关注负压区域（角部、边缘）的抗拉设计")
    print("2. 建议采用1.4的安全系数")
    print("3. 注意屋面系统的整体性和连接节点的设计")
    print("4. 必要时进行风洞试验验证")

if __name__ == "__main__":
    main()