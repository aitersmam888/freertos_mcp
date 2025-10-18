import re
from typing import Dict, List, Tuple, Any
from pathlib import Path

class CodeValidator:
    def __init__(self):
        self.validation_rules = self._load_validation_rules()
    
    def _load_validation_rules(self) -> Dict[str, Any]:
        """加载验证规则"""
        rules = {}
        rules_path = Path("config/validation_rules")
        if rules_path.exists():
            for rule_file in rules_path.glob("*.yaml"):
                try:
                    with open(rule_file, 'r') as f:
                        rule_name = rule_file.stem
                        rules[rule_name] = yaml.safe_load(f)
                except Exception as e:
                    print(f"加载验证规则失败 {rule_file}: {e}")
        else:
            # 使用默认规则
            rules = {
                "memory": {
                    "max_stack_usage_percentage": 60,
                    "min_task_stack_size": 128
                }
            }
        return rules
    
    async def validate_generated_code(self, code: str, chip: str, 
                                    requirements: Dict[str, Any]) -> Dict[str, Any]:
        """验证生成的代码"""
        validation_result = {
            "passed": True,
            "warnings": [],
            "errors": [],
            "suggestions": []
        }
        
        # 内存使用验证
        memory_checks = await self._validate_memory_usage(code, chip, requirements)
        if "warnings" in memory_checks:
            validation_result["warnings"].extend(memory_checks["warnings"])
        
        # 外设配置验证
        peripheral_checks = await self._validate_peripheral_config(code, chip)
        if "errors" in peripheral_checks:
            validation_result["errors"].extend(peripheral_checks["errors"])
        
        # FreeRTOS最佳实践验证
        freertos_checks = self._validate_freertos_practices(code)
        if "suggestions" in freertos_checks:
            validation_result["suggestions"].extend(freertos_checks["suggestions"])
        
        # 更新通过状态
        if validation_result["errors"]:
            validation_result["passed"] = False
        
        return validation_result
    
    async def _validate_memory_usage(self, code: str, chip: str, 
                                   requirements: Dict[str, Any]) -> Dict[str, List[str]]:
        """验证内存使用"""
        warnings = []
        
        # 分析堆栈分配
        stack_allocations = self._extract_stack_allocations(code)
        total_stack = sum(stack_allocations.values())
        
        # 使用默认RAM大小（如果无法获取芯片信息）
        chip_ram = 128 * 1024  # 默认128KB
        if total_stack > chip_ram * 0.6:  # 使用超过60% RAM
            warnings.append(f"堆栈使用量({total_stack}字节)超过芯片RAM的60%，建议优化")
        
        # 检查任务堆栈大小
        for task, stack_size in stack_allocations.items():
            if stack_size < 128:  # 最小堆栈建议
                warnings.append(f"任务 {task} 堆栈大小({stack_size})可能不足")
        
        return {"warnings": warnings}
    
    def _extract_stack_allocations(self, code: str) -> Dict[str, int]:
        """提取堆栈分配信息"""
        stack_allocations = {}
        
        # 匹配 xTaskCreate 调用
        task_pattern = r'xTaskCreate\s*\(\s*\w+\s*,\s*"([^"]+)"\s*,\s*(\d+)'
        matches = re.findall(task_pattern, code)
        
        for task_name, stack_size in matches:
            stack_allocations[task_name] = int(stack_size)
        
        return stack_allocations
    
    async def _validate_peripheral_config(self, code: str, chip: str) -> Dict[str, List[str]]:
        """验证外设配置"""
        errors = []
        
        # 检查时钟配置
        if "RCC" in code and "SystemClock_Config" not in code:
            errors.append("缺少系统时钟配置函数")
        
        # 简单的外设初始化检查
        if "GPIO_Init" in code and "SystemClock_Config" not in code:
            errors.append("GPIO初始化前应先配置系统时钟")
        
        return {"errors": errors}
    
    def _validate_freertos_practices(self, code: str) -> Dict[str, List[str]]:
        """验证FreeRTOS最佳实践"""
        suggestions = []
        
        # 检查任务延迟使用
        if "vTaskDelay(1)" in code:
            suggestions.append("建议使用 pdMS_TO_TICKS() 宏进行延时转换")
        
        # 检查队列使用
        if "xQueueSend" in code and "portMAX_DELAY" not in code:
            suggestions.append("队列发送建议指定超时时间，避免死锁")
        
        # 检查错误处理
        if "xTaskCreate" in code and "NULL" in code:
            suggestions.append("建议检查任务创建返回值，处理创建失败情况")
        
        return {"suggestions": suggestions}