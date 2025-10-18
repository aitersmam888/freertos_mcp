from typing import Dict, List, Any
import yaml
from pathlib import Path
from ..models.chip_analysis import ChipCapabilities, ProjectRequirements

class ChipAnalyzer:
    def __init__(self, knowledge_manager):
        self.knowledge_manager = knowledge_manager
        self.supported_chips = self._load_supported_chips()
    
    def _load_supported_chips(self) -> Dict[str, Any]:
        """加载支持的芯片列表"""
        chips = {}
        config_path = Path("config/mcu_configs")
        for config_file in config_path.glob("*.yaml"):
            with open(config_file, 'r') as f:
                chip_config = yaml.safe_load(f)
                chips[chip_config['mcu_family']] = chip_config
        return chips
    
    async def analyze_requirements(self, user_input: str) -> ProjectRequirements:
        """分析用户需求并生成项目规划"""
        # 提取关键信息
        requirements = self._extract_requirements(user_input)
        
        # 验证芯片支持
        chip_info = await self._validate_chip_support(requirements.chip_family)
        
        # 生成开发计划
        development_plan = await self._generate_development_plan(requirements, chip_info)
        
        return development_plan
    
    def _extract_requirements(self, user_input: str) -> ProjectRequirements:
        """从用户输入提取需求"""
        # 使用关键词识别技术需求
        requirements = {
            "wifi": "WiFi" in user_input or "无线" in user_input,
            "bluetooth": "Bluetooth" in user_input or "蓝牙" in user_input,
            "low_power": "低功耗" in user_input or "low power" in user_input,
            "peripherals": self._extract_peripherals(user_input),
            "application_type": self._detect_application_type(user_input)
        }
        return ProjectRequirements(**requirements)
    
    def _extract_peripherals(self, user_input: str) -> List[str]:
        """提取外设需求"""
        peripherals = []
        peripheral_keywords = {
            "UART": ["串口", "UART", "串行"],
            "SPI": ["SPI", "串行外设"],
            "I2C": ["I2C", "I²C", "IIC"],
            "ADC": ["ADC", "模数转换"],
            "PWM": ["PWM", "脉宽调制"]
        }
        
        for peripheral, keywords in peripheral_keywords.items():
            if any(keyword in user_input for keyword in keywords):
                peripherals.append(peripheral)
        
        return peripherals
    
    def _detect_application_type(self, user_input: str) -> str:
        """检测应用类型"""
        if any(word in user_input for word in ["智能家居", "智能设备", "smart home"]):
            return "smart_device"
        elif any(word in user_input for word in ["网关", "gateway", "集中器"]):
            return "iot_gateway"
        elif any(word in user_input for word in ["数据采集", "采集器", "sensor"]):
            return "data_acquisition"
        else:
            return "basic_demo"
    
    async def _validate_chip_support(self, chip_family: str) -> Dict[str, Any]:
        """验证芯片支持情况"""
        if chip_family not in self.supported_chips:
            raise ValueError(f"芯片 {chip_family} 暂不支持")
        
        # 从知识库获取更多芯片信息
        chip_info = self.supported_chips[chip_family]
        additional_info = await self.knowledge_manager.get_chip_details(chip_family)
        chip_info.update(additional_info)
        
        return chip_info
    
    async def _generate_development_plan(self, requirements: ProjectRequirements, 
                                       chip_info: Dict[str, Any]) -> ProjectRequirements:
        """生成开发计划"""
        plan = {
            "chip_family": requirements.chip_family,
            "application_type": requirements.application_type,
            "phases": [],
            "estimated_tasks": [],
            "potential_issues": []
        }
        
        # 根据应用类型生成阶段计划
        if requirements.application_type == "smart_device":
            plan["phases"] = [
                "基础系统初始化",
                "WiFi连接配置", 
                "外设驱动开发",
                "业务逻辑实现",
                "功耗优化"
            ]
        elif requirements.application_type == "iot_gateway":
            plan["phases"] = [
                "多任务架构设计",
                "网络协议栈集成",
                "数据转发逻辑",
                "安全认证实现",
                "性能调优"
            ]
        
        # 估算任务数量
        plan["estimated_tasks"] = self._estimate_tasks(requirements, chip_info)
        
        # 识别潜在问题
        plan["potential_issues"] = await self._identify_potential_issues(requirements, chip_info)
        
        return ProjectRequirements(**plan)
    
    def _estimate_tasks(self, requirements: ProjectRequirements, chip_info: Dict[str, Any]) -> List[str]:
        """估算需要实现的任务"""
        tasks = ["系统初始化", "FreeRTOS配置", "主任务框架"]
        
        if requirements.wifi:
            tasks.extend(["WiFi驱动初始化", "网络连接管理"])
        if requirements.bluetooth:
            tasks.extend(["蓝牙协议栈", "BLE服务配置"])
        
        tasks.extend([f"{peripheral}驱动配置" for peripheral in requirements.peripherals])
        tasks.append("应用业务逻辑")
        
        return tasks
    
    async def _identify_potential_issues(self, requirements: ProjectRequirements, 
                                       chip_info: Dict[str, Any]) -> List[str]:
        """识别潜在问题"""
        issues = []
        
        # 检查内存限制
        if chip_info['ram_size'] < 128:  # KB
            issues.append("内存资源紧张，需优化任务堆栈")
        
        # 检查外设冲突
        if "UART" in requirements.peripherals and "SPI" in requirements.peripherals:
            # 从知识库检查引脚冲突
            conflicts = await self.knowledge_manager.check_pin_conflicts(
                requirements.chip_family, ["UART", "SPI"])
            if conflicts:
                issues.append(f"检测到外设引脚冲突: {conflicts}")
        
        return issues