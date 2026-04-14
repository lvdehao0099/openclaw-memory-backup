#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
飞书表格管理器 (FeishuTableManager)
基于 v5.0 规范：创建空表 → 提取幽灵块 → 覆盖更新

作者：虾米 (CLO)
版本：5.0
更新日期：2026-03-13
"""

import requests
import json
from typing import List, Tuple, Dict, Any, Optional


class FeishuTableManager:
    """飞书文档表格管理器 - 基于 v5.0 规范"""
    
    def __init__(self, app_id: str, app_secret: str):
        """
        初始化
        
        Args:
            app_id: 飞书应用 ID
            app_secret: 飞书应用密钥
        """
        self.app_id = app_id
        self.app_secret = app_secret
        self.base_url = 'https://open.feishu.cn/open-apis'
        self.token = self._get_token()
        self.headers = {
            'Authorization': f'Bearer {self.token}',
            'Content-Type': 'application/json'
        }
    
    def _get_token(self) -> str:
        """获取 tenant_access_token"""
        url = f'{self.base_url}/auth/v3/tenant_access_token/internal'
        res = requests.post(url, json={
            'app_id': self.app_id,
            'app_secret': self.app_secret
        })
        return res.json()['tenant_access_token']
    
    def create_table(self, doc_id: str, rows: int, cols: int) -> str:
        """
        第一步：创建空表容器
        
        Args:
            doc_id: 文档 ID
            rows: 行数
            cols: 列数
        
        Returns:
            table_id: 表格 Block ID
        """
        url = f'{self.base_url}/docx/v1/documents/{doc_id}/blocks/{doc_id}/children'
        payload = {
            "children": [{
                "block_type": 31,
                "table": {
                    "property": {
                        "row_size": rows,
                        "column_size": cols
                    }
                }
            }]
        }
        
        res = requests.post(url, headers=self.headers, json=payload)
        if res.json()['code'] != 0:
            raise Exception(f"创建表格失败: {res.json()['msg']}")
        
        return res.json()['data']['children'][0]['block_id']
    
    def get_ghost_ids(self, doc_id: str, table_id: str) -> List[str]:
        """
        第二步：提取幽灵块 ID
        
        飞书创建空表时，会自动在每个单元格生成一个空的 text block。
        这些就是"幽灵块"，我们需要获取它们的 ID 来进行覆盖更新。
        
        Args:
            doc_id: 文档 ID
            table_id: 表格 Block ID
        
        Returns:
            ghost_text_ids: 幽灵块（text block）ID 列表，按单元格顺序排列
        """
        # 先获取表格下的所有单元格
        url = f'{self.base_url}/docx/v1/documents/{doc_id}/blocks/{table_id}/children'
        res = requests.get(url, headers=self.headers)
        
        if res.json()['code'] != 0:
            raise Exception(f"获取表格子块失败: {res.json()['msg']}")
        
        cells = res.json()['data']['items']
        ghost_text_ids = []
        
        # 遍历每个单元格，获取其中的第一个 text block ID
        for cell in cells:
            cell_id = cell['block_id']
            
            # 获取单元格下的子块
            url = f'{self.base_url}/docx/v1/documents/{doc_id}/blocks/{cell_id}/children'
            res = requests.get(url, headers=self.headers)
            
            if res.json()['code'] == 0 and res.json()['data']['items']:
                # 获取第一个子块（通常是飞书自动生成的空 text block）
                ghost_text_id = res.json()['data']['items'][0]['block_id']
                ghost_text_ids.append(ghost_text_id)
        
        return ghost_text_ids
    
    def update_cell(self, doc_id: str, ghost_id: str, content: str, 
                   bold: bool = False, italic: bool = False) -> bool:
        """
        第三步：覆盖更新单个单元格
        
        使用 PATCH + update_text_elements 覆盖幽灵块
        
        Args:
            doc_id: 文档 ID
            ghost_id: 幽灵块 ID
            content: 单元格内容
            bold: 是否加粗
            italic: 是否斜体
        
        Returns:
            success: 是否成功
        """
        url = f'{self.base_url}/docx/v1/documents/{doc_id}/blocks/{ghost_id}'
        
        # 核心：使用 update_text_elements 而不是 text
        payload = {
            "update_text_elements": {
                "elements": [{
                    "text_run": {
                        "content": str(content).strip().replace('\r', '').replace('\n', ''),
                        "text_element_style": {
                            "bold": bold,
                            "italic": italic
                        }
                    }
                }]
            }
        }
        
        res = requests.patch(url, headers=self.headers, json=payload)
        return res.status_code == 200 and res.json().get('code') == 0
    
    def batch_update_content(self, doc_id: str, data: List[List[str]], 
                           header_bold: bool = True) -> bool:
        """
        批量更新表格内容
        
        Args:
            doc_id: 文档 ID
            data: 二维数组，内容按行排列
            header_bold: 是否对第一行（表头）加粗
        
        Returns:
            success: 是否全部成功
        """
        if not data:
            return False
        
        rows = len(data)
        cols = len(data[0])
        
        # 第一步：创建空表
        table_id = self.create_table(doc_id, rows, cols)
        
        # 第二步：获取幽灵块 ID
        ghost_ids = self.get_ghost_ids(doc_id, table_id)
        
        if len(ghost_ids) != rows * cols:
            raise Exception(f"幽灵块数量不匹配: 期望 {rows*cols}, 实际 {len(ghost_ids)}")
        
        # 第三步：逐个覆盖更新
        flat_data = []
        for row in data:
            flat_data.extend(row)
        
        for i, ghost_id in enumerate(ghost_ids):
            content = flat_data[i]
            is_header = (i < cols) and header_bold
            
            success = self.update_cell(doc_id, ghost_id, content, bold=is_header)
            if not success:
                print(f"  ⚠️ 更新单元格 {i} 失败: {content}")
        
        return True
    
    def create_table_with_data(self, title: str, data: List[List[str]], 
                              folder_token: str = None,
                              header_bold: bool = True) -> Tuple[str, str]:
        """
        一键创建带内容的表格
        
        Args:
            title: 文档标题
            data: 二维数组，内容按行排列
            folder_token: 文件夹 token（可选）
            header_bold: 是否对第一行（表头）加粗
        
        Returns:
            (doc_id, url): 文档 ID 和链接
        """
        # 创建文档
        url = f'{self.base_url}/docx/v1/documents'
        payload = {"title": title}
        if folder_token:
            payload["folder_token"] = folder_token
        
        res = requests.post(url, headers=self.headers, json=payload)
        if res.json()['code'] != 0:
            raise Exception(f"创建文档失败: {res.json()['msg']}")
        
        doc_id = res.json()['data']['document']['document_id']
        
        # 批量更新内容
        self.batch_update_content(doc_id, data, header_bold)
        
        return doc_id, f"https://feishu.cn/docx/{doc_id}"


# ============ 便捷函数 ============

def create_table_simple(title: str, data: List[List[str]], 
                        folder_token: str = None) -> Tuple[str, str]:
    """
    便捷函数：一键创建带内容的表格
    
    Args:
        title: 文档标题
        data: 二维数组
        folder_token: 文件夹 token（可选）
    
    Returns:
        (doc_id, url)
    """
    app_id = "cli_a92780ca08b89bb6"
    app_secret = "6gzhCcNYlHc7vOnGCCdvpbik27O85uz0"
    
    manager = FeishuTableManager(app_id, app_secret)
    return manager.create_table_with_data(title, data, folder_token)


# ============ 测试 ============

if __name__ == "__main__":
    # 测试创建表格
    app_id = "cli_a92780ca08b89bb6"
    app_secret = "6gzhCcNYlHc7vOnGCCdvpbik27O85uz0"
    
    manager = FeishuTableManager(app_id, app_secret)
    
    # 测试数据
    data = [
        ["关键词", "政策内容"],
        ["人工智能+", "与制造业深度融合"],
        ["场景驱动", "优先支持实际应用"],
        ["普惠AI", "降低中小企业门槛"]
    ]
    
    # 创建文档和表格
    doc_id, url = manager.create_table_with_data(
        "测试表格-v5.0规范",
        data,
        folder_token="Thhrfa3QglB5amdIMpEcY2tAndd"
    )
    
    print(f"✅ 表格创建成功: {url}")
