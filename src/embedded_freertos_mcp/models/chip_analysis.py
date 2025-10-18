from typing import Dict, List, Any, Optional
from dataclasses import dataclass, field
from enum import Enum

class ApplicationType(Enum):
    SMART_DEVICE = "smart_device"
    IOT_GATEWAY = "iot_gateway"
    DATA_ACQUISITION = "data_acquisition"
    BASIC_DEMO = "basic_demo"

@dataclass
class ChipCapabilities:
    """芯片能力模型"""
    chip_family: str
    core: str
    frequency: int
    flash_size: int
    ram_size: int
    peripherals: List[str]
    wifi_support: bool = False
    bluetooth_support: bool = False
    low_power_modes: List[str] = field(default_factory=lambda: ["sleep", "deep_sleep"])

@dataclass
class ProjectRequirements:
    """项目需求模型"""
    chip_family: str
    application_type: ApplicationType
    wifi_required: bool = False
    bluetooth_required: bool = False
    low_power_required: bool = False
    peripherals_required: List[str] = field(default_factory=list)
    estimated_tasks: List[str] = field(default_factory=list)
    potential_issues: List[str] = field(default_factory=list)
    phases: List[str] = field(default_factory=list)
    
    def to_dict(self) -> Dict[str, Any]:
        """转换为字典格式"""
        return {
            "chip_family": self.chip_family,
            "application_type": self.application_type.value,
            "wifi_required": self.wifi_required,
            "bluetooth_required": self.bluetooth_required,
            "low_power_required": self.low_power_required,
            "peripherals_required": self.peripherals_required,
            "estimated_tasks": self.estimated_tasks,
            "potential_issues": self.potential_issues,
            "phases": self.phases
        }
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'ProjectRequirements':
        """从字典创建实例"""
        return cls(
            chip_family=data.get("chip_family", ""),
            application_type=ApplicationType(data.get("application_type", "basic_demo")),
            wifi_required=data.get("wifi_required", False),
            bluetooth_required=data.get("bluetooth_required", False),
            low_power_required=data.get("low_power_required", False),
            peripherals_required=data.get("peripherals_required", []),
            estimated_tasks=data.get("estimated_tasks", []),
            potential_issues=data.get("potential_issues", []),
            phases=data.get("phases", [])
        )