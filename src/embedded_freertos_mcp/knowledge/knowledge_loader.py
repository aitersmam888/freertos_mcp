#!/usr/bin/env python3
"""知识库加载器 - 用于读取芯片规格书和SDK"""

import json
from pathlib import Path
from typing import Dict, List, Optional
import logging

# 可选导入yaml，如果不存在则使用json替代
try:
    import yaml
    YAML_AVAILABLE = True
except ImportError:
    YAML_AVAILABLE = False
    import json as yaml

logger = logging.getLogger(__name__)

class KnowledgeLoader:
    """知识库加载器类"""
    
    def __init__(self, knowledge_base_path: str = "./knowledge_base"):
        self.knowledge_base_path = Path(knowledge_base_path)
    
    def load_chip_config(self, chip_family: str) -> Optional[Dict]:
        """加载芯片配置文件"""
        try:
            config_path = self.knowledge_base_path / ".." / "config" / "mcu_configs" / f"{chip_family}.yaml"
            if not config_path.exists():
                # 尝试在知识库中查找
                config_path = self.knowledge_base_path / "datasheets" / chip_family / f"{chip_family}_config.yaml"
            
            if config_path.exists():
                with open(config_path, 'r', encoding='utf-8') as f:
                    if YAML_AVAILABLE:
                        return yaml.safe_load(f)
                    else:
                        # 使用json作为备选
                        import json
                        return json.load(f)
            return None
        except Exception as e:
            logger.error(f"加载芯片配置失败: {e}")
            return None
    
    def load_datasheet_info(self, chip_family: str) -> Optional[Dict]:
        """加载芯片规格书信息"""
        try:
            datasheet_dir = self.knowledge_base_path / "datasheets" / chip_family
            if not datasheet_dir.exists():
                return None
            
            # 查找规格书文件
            datasheet_files = list(datasheet_dir.glob("*.pdf")) + list(datasheet_dir.glob("*.txt"))
            
            info = {
                "chip_family": chip_family,
                "datasheet_files": [f.name for f in datasheet_files],
                "summary": self._extract_datasheet_summary(datasheet_dir)
            }
            
            return info
        except Exception as e:
            logger.error(f"加载规格书信息失败: {e}")
            return None
    
    def _extract_datasheet_summary(self, datasheet_dir: Path) -> Dict:
        """提取规格书摘要信息"""
        summary = {}
        
        # 查找摘要文件
        summary_file = datasheet_dir / "summary.txt"
        if summary_file.exists():
            with open(summary_file, 'r', encoding='utf-8') as f:
                summary["text"] = f.read()
        
        # 查找关键参数文件
        params_file = datasheet_dir / "parameters.yaml"
        if params_file.exists():
            with open(params_file, 'r', encoding='utf-8') as f:
                if YAML_AVAILABLE:
                    summary["parameters"] = yaml.safe_load(f)
                else:
                    # 使用json作为备选
                    import json
                    summary["parameters"] = json.load(f)
        
        return summary
    
    def load_sdk_info(self, chip_family: str) -> Optional[Dict]:
        """加载SDK信息"""
        try:
            sdk_dir = self.knowledge_base_path / "sdks" / f"{chip_family}_sdk"
            if not sdk_dir.exists():
                return None
            
            sdk_info = {
                "chip_family": chip_family,
                "sdk_path": str(sdk_dir),
                "available_drivers": self._scan_sdk_drivers(sdk_dir),
                "examples": self._scan_sdk_examples(sdk_dir),
                "build_system": self._scan_build_system(sdk_dir)
            }
            
            return sdk_info
        except Exception as e:
            logger.error(f"加载SDK信息失败: {e}")
            return None
    
    def _scan_sdk_drivers(self, sdk_dir: Path) -> List[str]:
        """扫描SDK中的驱动"""
        drivers = []
        driver_dir = sdk_dir / "drivers"
        
        if driver_dir.exists():
            for item in driver_dir.iterdir():
                if item.is_dir():
                    drivers.append(item.name)
        
        return drivers
    
    def _scan_sdk_examples(self, sdk_dir: Path) -> List[str]:
        """扫描SDK中的示例"""
        examples = []
        example_dir = sdk_dir / "examples"
        
        if example_dir.exists():
            for item in example_dir.iterdir():
                if item.is_dir():
                    examples.append(item.name)
        
        return examples
    
    def _scan_build_system(self, sdk_dir: Path) -> Dict:
        """扫描构建系统"""
        build_info = {}
        
        # 查找Makefile
        makefile = sdk_dir / "Makefile"
        if makefile.exists():
            build_info["makefile"] = True
        
        # 查找CMakeLists.txt
        cmakefile = sdk_dir / "CMakeLists.txt"
        if cmakefile.exists():
            build_info["cmake"] = True
        
        return build_info
    
    def load_requirements(self) -> Optional[Dict]:
        """加载项目需求文档"""
        try:
            req_dir = self.knowledge_base_path / "requirements"
            requirements = {}
            
            # 加载项目需求
            project_req = req_dir / "项目需求.txt"
            if project_req.exists():
                with open(project_req, 'r', encoding='utf-8') as f:
                    requirements["project"] = f.read()
            
            # 加载功能文档
            func_doc = req_dir / "functional_docs" / "功能文档.txt"
            if func_doc.exists():
                with open(func_doc, 'r', encoding='utf-8') as f:
                    requirements["functional"] = f.read()
            
            return requirements
        except Exception as e:
            logger.error(f"加载需求文档失败: {e}")
            return None
    
    def get_available_chips(self) -> List[str]:
        """获取可用的芯片列表"""
        chips = []
        
        # 从配置目录查找
        config_dir = self.knowledge_base_path / ".." / "config" / "mcu_configs"
        if config_dir.exists():
            for yaml_file in config_dir.glob("*.yaml"):
                chips.append(yaml_file.stem)
        
        # 从知识库目录查找
        datasheet_dir = self.knowledge_base_path / "datasheets"
        if datasheet_dir.exists():
            for chip_dir in datasheet_dir.iterdir():
                if chip_dir.is_dir() and chip_dir.name not in chips:
                    chips.append(chip_dir.name)
        
        return sorted(chips)