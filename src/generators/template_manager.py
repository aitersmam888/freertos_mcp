from typing import Dict, Any
import jinja2
from pathlib import Path

class TemplateManager:
    def __init__(self):
        # 修正模板路径为正确的相对路径
        self.template_path = Path("src/embedded_freertos_mcp/templates")
        self.env = jinja2.Environment(
            loader=jinja2.FileSystemLoader(self.template_path),
            trim_blocks=True,
            lstrip_blocks=True
        )
    
    def get_application_template(self, chip: str, app_type: str) -> Dict[str, Any]:
        """获取应用模板"""
        template_mapping = {
            "BK7252N": {
                "iot_gateway": "bk7252n_iot_gateway",
                "smart_device": "bk7252n_smart_device", 
                "basic_demo": "bk7252n_basic_demo"
            },
            "STM32F4": {
                "iot_gateway": "stm32_iot_gateway",
                "data_acquisition": "stm32_data_acq"
            }
        }
        
        chip_templates = template_mapping.get(chip, {})
        template_name = chip_templates.get(app_type, "generic_template")
        
        return self._load_template(template_name)
    
    def _load_template(self, template_name: str) -> Dict[str, Any]:
        """加载模板"""
        template_files = {
            "main_c": f"projects/{template_name}/main.c.j2",
            "header": f"projects/{template_name}/config.h.j2",
            "makefile": f"projects/{template_name}/Makefile.j2",
            "tasks": f"projects/{template_name}/tasks.c.j2"
        }
        
        templates = {}
        for key, template_path in template_files.items():
            try:
                templates[key] = self.env.get_template(template_path)
            except jinja2.TemplateNotFound:
                # 使用通用模板
                templates[key] = self.env.get_template(f"projects/generic_template/{key}.j2")
        
        return templates
    
    def render_project(self, template_set: Dict[str, Any], context: Dict[str, Any]) -> Dict[str, str]:
        """渲染项目文件"""
        rendered_files = {}
        
        for file_type, template in template_set.items():
            rendered_files[file_type] = template.render(**context)
        
        return rendered_files