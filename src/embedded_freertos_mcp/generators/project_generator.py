#!/usr/bin/env python3
"""项目生成器 - 根据芯片知识库自动生成完整的FreeRTOS项目"""

import os
import shutil
from pathlib import Path
from typing import Dict, List, Any
import logging
from ..knowledge.knowledge_loader import KnowledgeLoader
from ..memory.memory_manager import MemoryManager

logger = logging.getLogger(__name__)

class ProjectGenerator:
    """项目生成器类"""
    
    def __init__(self, knowledge_base_path: str, memory_db_path: str):
        self.knowledge_loader = KnowledgeLoader(knowledge_base_path)
        self.memory_manager = MemoryManager(memory_db_path)
    
    def generate_project(self, project_name: str, chip_family: str, output_dir: str) -> Dict[str, Any]:
        """生成完整的嵌入式FreeRTOS项目"""
        try:
            output_path = Path(output_dir) / project_name
            output_path.mkdir(parents=True, exist_ok=True)
            
            # 加载芯片知识
            chip_config = self.knowledge_loader.load_chip_config(chip_family)
            datasheet_info = self.knowledge_loader.load_datasheet_info(chip_family)
            sdk_info = self.knowledge_loader.load_sdk_info(chip_family)
            requirements = self.knowledge_loader.load_requirements()
            
            if not chip_config:
                raise ValueError(f"未找到芯片 {chip_family} 的配置")
            
            # 生成项目结构
            project_structure = self._create_project_structure(output_path)
            
            # 生成核心文件
            self._generate_main_file(output_path, chip_config, project_name)
            self._generate_freertos_config(output_path, chip_config)
            self._generate_makefile(output_path, chip_config)
            self._generate_linker_script(output_path, chip_config)
            self._generate_startup_file(output_path, chip_config)
            self._generate_system_config(output_path, chip_config)
            
            # 生成任务文件
            self._generate_basic_tasks(output_path, chip_config)
            
            # 保存项目配置到记忆库
            project_config = {
                "project_name": project_name,
                "chip_family": chip_family,
                "chip_config": chip_config,
                "project_structure": project_structure,
                "generated_files": self._get_generated_files(output_path)
            }
            
            self.memory_manager.save_project_config(project_name, chip_family, project_config)
            
            logger.info(f"项目生成成功: {project_name}")
            return {
                "success": True,
                "project_path": str(output_path),
                "chip_info": chip_config,
                "generated_files": project_config["generated_files"]
            }
            
        except Exception as e:
            logger.error(f"项目生成失败: {e}")
            return {"success": False, "error": str(e)}
    
    def _create_project_structure(self, project_path: Path) -> Dict[str, List[str]]:
        """创建项目目录结构"""
        structure = {
            "src": ["main.c", "system.c", "tasks"],
            "inc": ["system.h", "config.h"],
            "drivers": ["gpio", "uart", "spi", "i2c"],
            "freertos": ["Source", "Config"],
            "build": ["obj", "bin"],
            "docs": ["README.md", "config.md"]
        }
        
        for dir_name, files in structure.items():
            dir_path = project_path / dir_name
            dir_path.mkdir(exist_ok=True)
            
            # 创建子目录
            if dir_name == "tasks":
                (dir_path / "inc").mkdir(exist_ok=True)
                (dir_path / "src").mkdir(exist_ok=True)
            elif dir_name == "drivers":
                for driver_dir in files:
                    (dir_path / driver_dir).mkdir(exist_ok=True)
        
        return structure
    
    def _generate_main_file(self, project_path: Path, chip_config: Dict[str, Any], project_name: str):
        """生成主程序文件"""
        main_content = f'''#include "FreeRTOS.h"
#include "task.h"
#include "system.h"

/* 项目名称: {project_name} */
/* 芯片: {chip_config['chip']['name']} */

int main(void)
{{
    /* 系统初始化 */
    System_Init();
    
    /* 创建FreeRTOS任务 */
    xTaskCreate(vTask1, "Task1", 1024, NULL, 1, NULL);
    xTaskCreate(vTask2, "Task2", 1024, NULL, 1, NULL);
    
    /* 启动调度器 */
    vTaskStartScheduler();
    
    /* 程序不应执行到这里 */
    while(1);
}}

void vTask1(void *pvParameters)
{{
    for(;;)
    {{
        /* 任务1代码 */
        vTaskDelay(1000 / portTICK_PERIOD_MS);
    }}
}}

void vTask2(void *pvParameters)
{{
    for(;;)
    {{
        /* 任务2代码 */
        vTaskDelay(500 / portTICK_PERIOD_MS);
    }}
}}'''
        
        with open(project_path / "src" / "main.c", 'w', encoding='utf-8') as f:
            f.write(main_content)
    
    def _generate_freertos_config(self, project_path: Path, chip_config: Dict[str, Any]):
        """生成FreeRTOS配置文件"""
        config_content = f'''#ifndef FREERTOS_CONFIG_H
#define FREERTOS_CONFIG_H

/* 芯片配置: {chip_config['chip']['name']} */
#define configUSE_PREEMPTION                    1
#define configUSE_IDLE_HOOK                     0
#define configUSE_TICK_HOOK                     0
#define configCPU_CLOCK_HZ                      ({chip_config['freertos_config']['configCPU_CLOCK_HZ']})
#define configTICK_RATE_HZ                      (1000)
#define configMAX_PRIORITIES                    (5)
#define configMINIMAL_STACK_SIZE                ((unsigned short)128)
#define configTOTAL_HEAP_SIZE                   ((size_t)({chip_config['freertos_config']['configTOTAL_HEAP_SIZE']}))
#define configMAX_TASK_NAME_LEN                 (16)
#define configUSE_16_BIT_TICKS                  0
#define configIDLE_SHOULD_YIELD                 1
#define configUSE_MUTEXES                       1
#define configUSE_RECURSIVE_MUTEXES             1
#define configUSE_COUNTING_SEMAPHORES           1
#define configUSE_ALTERNATIVE_API               0
#define configCHECK_FOR_STACK_OVERFLOW          0
#define configUSE_TRACE_FACILITY                0

/* 内存分配方案 */
#define configSUPPORT_DYNAMIC_ALLOCATION        1
#define configSUPPORT_STATIC_ALLOCATION         0

#endif /* FREERTOS_CONFIG_H */'''
        
        config_dir = project_path / "freertos" / "Config"
        config_dir.mkdir(parents=True, exist_ok=True)
        
        with open(config_dir / "FreeRTOSConfig.h", 'w', encoding='utf-8') as f:
            f.write(config_content)
    
    def _generate_makefile(self, project_path: Path, chip_config: Dict[str, Any]):
        """生成Makefile"""
        makefile_content = f'''# BK7252 FreeRTOS项目Makefile
PROJECT_NAME = embedded_freertos_project
MCU = {chip_config['chip']['core'].lower()}

# 工具链配置
CC = arm-none-eabi-gcc
OBJCOPY = arm-none-eabi-objcopy
SIZE = arm-none-eabi-size

# 编译选项
CFLAGS = {''.join(f'\\n\t{flag}' for flag in chip_config['compiler']['flags'])}
CFLAGS += -I./inc -I./freertos/Config -I./freertos/Source/include
CFLAGS += -D{chip_config['chip']['family'].upper()}

# 源文件
SRCS = $(wildcard src/*.c) $(wildcard src/tasks/src/*.c) $(wildcard drivers/*/*.c)
SRCS += freertos/Source/tasks.c freertos/Source/queue.c freertos/Source/list.c
SRCS += freertos/Source/timers.c freertos/Source/event_groups.c
SRCS += freertos/Source/portable/GCC/ARM_CM4F/port.c
SRCS += freertos/Source/portable/MemMang/heap_4.c

# 目标文件
OBJS = $(SRCS:.c=.o)

# 默认目标
all: $(PROJECT_NAME).elf

$(PROJECT_NAME).elf: $(OBJS)
\t$(CC) $(CFLAGS) -T linker_script.ld -o $@ $^
\t$(SIZE) $@

%.o: %.c
\t$(CC) $(CFLAGS) -c -o $@ $<

clean:
\trm -f $(OBJS) $(PROJECT_NAME).elf

flash: $(PROJECT_NAME).elf
\t# 烧录命令

.PHONY: all clean flash'''
        
        with open(project_path / "Makefile", 'w', encoding='utf-8') as f:
            f.write(makefile_content)
    
    def _generate_linker_script(self, project_path: Path, chip_config: Dict[str, Any]):
        """生成链接脚本"""
        linker_content = f'''/* 链接器脚本 - {chip_config['chip']['name']} */
MEMORY
{{
    FLASH (rx) : ORIGIN = {chip_config['memory_map']['flash_start']}, LENGTH = {chip_config['chip']['flash_size']}
    RAM (rwx) : ORIGIN = {chip_config['memory_map']['ram_start']}, LENGTH = {chip_config['chip']['ram_size']}
}}

SECTIONS
{{
    .text :
    {{
        *(.text*)
    }} > FLASH
    
    .data :
    {{
        *(.data*)
    }} > RAM
    
    .bss :
    {{
        *(.bss*)
    }} > RAM
}}'''
        
        with open(project_path / "linker_script.ld", 'w', encoding='utf-8') as f:
            f.write(linker_content)
    
    def _generate_startup_file(self, project_path: Path, chip_config: Dict[str, Any]):
        """生成启动文件"""
        startup_content = f'''#include <stdint.h>

/* 中断向量表 */
extern void _estack(void);
extern void Reset_Handler(void);
extern void Default_Handler(void);

void NMI_Handler(void) __attribute__ ((weak, alias ("Default_Handler")));
void HardFault_Handler(void) __attribute__ ((weak, alias ("Default_Handler")));

/* 中断向量表 */
__attribute__ ((section(".isr_vector")))
void (* const g_pfnVectors[])(void) =
{{
    (void (*)(void))((uint32_t)&_estack),  /* 栈顶指针 */
    Reset_Handler,                         /* 复位处理 */
    NMI_Handler,                           /* NMI处理 */
    HardFault_Handler,                     /* 硬件错误处理 */
    /* 更多中断向量... */
}};

/* 默认中断处理 */
void Default_Handler(void)
{{
    while(1);
}}

/* 复位处理 */
void Reset_Handler(void)
{{
    /* 初始化.data段 */
    extern uint32_t _sdata, _edata, _sidata;
    uint32_t *pSrc = &_sidata;
    uint32_t *pDest = &_sdata;
    
    while(pDest < &_edata)
        *pDest++ = *pSrc++;
    
    /* 清零.bss段 */
    extern uint32_t _sbss, _ebss;
    pDest = &_sbss;
    while(pDest < &_ebss)
        *pDest++ = 0;
    
    /* 调用主函数 */
    extern int main(void);
    main();
}}'''
        
        with open(project_path / "src" / "startup.c", 'w', encoding='utf-8') as f:
            f.write(startup_content)
    
    def _generate_system_config(self, project_path: Path, chip_config: Dict[str, Any]):
        """生成系统配置文件"""
        system_h_content = f'''#ifndef SYSTEM_H
#define SYSTEM_H

#include <stdint.h>

/* 系统时钟配置 */
#define SYSTEM_CLOCK {chip_config['chip']['frequency']}

/* 外设基地址 */
#define PERIPH_BASE {chip_config['memory_map']['peripheral_base']}

/* 系统初始化函数 */
void System_Init(void);
void System_Clock_Config(void);

#endif /* SYSTEM_H */'''
        
        system_c_content = f'''#include "system.h"

void System_Init(void)
{{
    /* 系统时钟配置 */
    System_Clock_Config();
    
    /* 外设时钟使能 */
    // 根据芯片配置使能外设时钟
}}

void System_Clock_Config(void)
{{
    /* 配置系统时钟为 {chip_config['chip']['frequency']} */
    // 具体的时钟配置代码
}}'''
        
        inc_dir = project_path / "inc"
        inc_dir.mkdir(exist_ok=True)
        
        with open(inc_dir / "system.h", 'w', encoding='utf-8') as f:
            f.write(system_h_content)
        
        with open(project_path / "src" / "system.c", 'w', encoding='utf-8') as f:
            f.write(system_c_content)
    
    def _generate_basic_tasks(self, project_path: Path, chip_config: Dict[str, Any]):
        """生成基本任务文件"""
        tasks_inc_dir = project_path / "src" / "tasks" / "inc"
        tasks_src_dir = project_path / "src" / "tasks" / "src"
        tasks_inc_dir.mkdir(parents=True, exist_ok=True)
        tasks_src_dir.mkdir(parents=True, exist_ok=True)
        
        # 生成任务头文件
        tasks_h_content = '''#ifndef TASKS_H
#define TASKS_H

#include "FreeRTOS.h"
#include "task.h"

/* 任务函数声明 */
void vTask1(void *pvParameters);
void vTask2(void *pvParameters);
void vLEDTask(void *pvParameters);
void vUARTTask(void *pvParameters);

#endif /* TASKS_H */'''
        
        with open(tasks_inc_dir / "tasks.h", 'w', encoding='utf-8') as f:
            f.write(tasks_h_content)
    
    def _get_generated_files(self, project_path: Path) -> List[str]:
        """获取生成的文件列表"""
        files = []
        for file_path in project_path.rglob("*"):
            if file_path.is_file():
                files.append(str(file_path.relative_to(project_path)))
        return files