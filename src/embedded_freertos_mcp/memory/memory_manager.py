#!/usr/bin/env python3
"""记忆库管理器 - 用于存储和检索项目配置"""

import sqlite3
import json
from pathlib import Path
from typing import Dict, List, Optional
import logging

logger = logging.getLogger(__name__)

class MemoryManager:
    """记忆库管理类"""
    
    def __init__(self, db_path: str = "./memory/memory.db"):
        self.db_path = Path(db_path)
        self.db_path.parent.mkdir(parents=True, exist_ok=True)
        self._init_database()
    
    def _init_database(self):
        """初始化数据库"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # 创建项目记忆表
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS project_memory (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                project_name TEXT UNIQUE NOT NULL,
                chip_family TEXT NOT NULL,
                config_json TEXT NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        # 创建芯片知识表
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS chip_knowledge (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                chip_family TEXT NOT NULL,
                knowledge_type TEXT NOT NULL,
                content_json TEXT NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        conn.commit()
        conn.close()
    
    def save_project_config(self, project_name: str, chip_family: str, config: Dict) -> bool:
        """保存项目配置到记忆库"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            config_json = json.dumps(config, ensure_ascii=False)
            
            cursor.execute('''
                INSERT OR REPLACE INTO project_memory 
                (project_name, chip_family, config_json, updated_at)
                VALUES (?, ?, ?, CURRENT_TIMESTAMP)
            ''', (project_name, chip_family, config_json))
            
            conn.commit()
            conn.close()
            logger.info(f"项目配置已保存: {project_name}")
            return True
        except Exception as e:
            logger.error(f"保存项目配置失败: {e}")
            return False
    
    def load_project_config(self, project_name: str) -> Optional[Dict]:
        """从记忆库加载项目配置"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            cursor.execute('''
                SELECT config_json FROM project_memory 
                WHERE project_name = ?
            ''', (project_name,))
            
            result = cursor.fetchone()
            conn.close()
            
            if result:
                return json.loads(result[0])
            return None
        except Exception as e:
            logger.error(f"加载项目配置失败: {e}")
            return None
    
    def save_chip_knowledge(self, chip_family: str, knowledge_type: str, content: Dict) -> bool:
        """保存芯片知识到记忆库"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            content_json = json.dumps(content, ensure_ascii=False)
            
            cursor.execute('''
                INSERT INTO chip_knowledge 
                (chip_family, knowledge_type, content_json)
                VALUES (?, ?, ?)
            ''', (chip_family, knowledge_type, content_json))
            
            conn.commit()
            conn.close()
            logger.info(f"芯片知识已保存: {chip_family}/{knowledge_type}")
            return True
        except Exception as e:
            logger.error(f"保存芯片知识失败: {e}")
            return False
    
    def search_chip_knowledge(self, chip_family: str, knowledge_type: str = None) -> List[Dict]:
        """搜索芯片知识"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            if knowledge_type:
                cursor.execute('''
                    SELECT content_json FROM chip_knowledge 
                    WHERE chip_family = ? AND knowledge_type = ?
                    ORDER BY created_at DESC
                ''', (chip_family, knowledge_type))
            else:
                cursor.execute('''
                    SELECT content_json FROM chip_knowledge 
                    WHERE chip_family = ?
                    ORDER BY created_at DESC
                ''', (chip_family,))
            
            results = cursor.fetchall()
            conn.close()
            
            return [json.loads(result[0]) for result in results]
        except Exception as e:
            logger.error(f"搜索芯片知识失败: {e}")
            return []