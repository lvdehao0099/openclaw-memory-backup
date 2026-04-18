#!/usr/bin/env python3
"""
飞书文档表格写入工具 - 合并方案
结合了：
1. 规范文档的 Block 构造方法
2. 飞书 API 的分步创建机制（Table → Cells → 更新内容）

核心逻辑：
1. 创建 Table Block（只传行列数，飞书自动创建 Cells）
2. 读取 Table Block 获取所有 Cell IDs
3. 更新每个 Cell 里的 Text Block 内容
"""

import requests
import json

FEISHU_APP_ID = "cli_a92780ca08b89bb6"
FEISHU_APP_SECRET = "6gzhCcNYlHc7vOnGCCdvpbik27O85uz0"

class FeishuDocTableWriter:
    def __init__(self):
        self.token = self._get_token()
        self.headers = {
            'Authorization': f'Bearer {self.token}',
            'Content-Type': 'application/json'
        }
    
    def _get_token(self):
        """获取 tenant_access_token"""
        url = 'https://open.feishu.cn/open-apis/auth/v3/tenant_access_token/internal'
        res = requests.post(url, json={
            'app_id': FEISHU_APP_ID,
            'app_secret': FEISHU_APP_SECRET
        })
        return res.json()['tenant_access_token']
    
    def create_document(self, title, folder_token=None):
        """创建空白文档"""
        url = 'https://open.feishu.cn/open-apis/docx/v1/documents'
        payload = {'title': title}
        if folder_token:
            payload['folder_token'] = folder_token
        
        res = requests.post(url, headers=self.headers, json=payload)
        data = res.json()
        if data['code'] != 0:
            raise Exception(f"创建文档失败: {data['msg']}")
        
        doc_id = data['data']['document']['document_id']
        url = f"https://feishu.cn/docx/{doc_id}"
        return doc_id, url
    
    def write_table(self, doc_id, table_data, header_row=True):
        """
        写入表格到文档
        
        Args:
            doc_id: 文档ID
            table_data: 二维数组，如 [["列1", "列2"], ["值1", "值2"]]
            header_row: 是否有表头
        
        Returns:
            table_block_id: 表格block的ID
        """
        row_size = len(table_data)
        column_size = len(table_data[0]) if table_data else 0
        
        # 步骤1: 创建 Table Block（只传行列数）
        url = f'https://open.feishu.cn/open-apis/docx/v1/documents/{doc_id}/blocks/{doc_id}/children'
        table_block = {
            "block_type": 31,
            "table": {
                "property": {
                    "row_size": row_size,
                    "column_size": column_size,
                    "header_row": header_row
                }
            }
        }
        
        res = requests.post(url, headers=self.headers, json={"children": [table_block]})
        data = res.json()
        if data['code'] != 0:
            raise Exception(f"创建表格失败: {data['msg']}")
        
        table_block_id = data['data']['children'][0]['block_id']
        cell_ids = data['data']['children'][0]['table']['cells']
        
        print(f"表格创建成功，Block ID: {table_block_id}")
        print(f"自动生成 {len(cell_ids)} 个单元格")
        
        # 步骤2: 更新每个 Cell 的内容
        for i, cell_id in enumerate(cell_ids):
            row = i // column_size
            col = i % column_size
            cell_text = str(table_data[row][col]).strip()
            
            # 获取 cell 里的 text block ID
            cell_url = f'https://open.feishu.cn/open-apis/docx/v1/documents/{doc_id}/blocks/{cell_id}/children'
            res = requests.get(cell_url, headers=self.headers)
            cell_data = res.json()
            
            if cell_data['code'] == 0 and cell_data['data']['items']:
                text_block_id = cell_data['data']['items'][0]['block_id']
                
                # 更新 text block 内容
                update_url = f'https://open.feishu.cn/open-apis/docx/v1/documents/{doc_id}/blocks/{text_block_id}'
                update_payload = {
                    "block_type": 2,
                    "text": {
                        "elements": [{"text_run": {"content": cell_text}}]
                    }
                }
                res = requests.patch(update_url, headers=self.headers, json=update_payload)
                if res.json()['code'] != 0:
                    print(f"  ⚠️ 更新单元格 [{row},{col}] 失败: {res.json()['msg']}")
                else:
                    print(f"  ✅ 单元格 [{row},{col}] = '{cell_text[:20]}...'")
        
        return table_block_id
    
    def write_content(self, doc_id, blocks):
        """
        写入其他内容（标题、文本、列表等）
        
        Args:
            doc_id: 文档ID
            blocks: Block 数组
        """
        url = f'https://open.feishu.cn/open-apis/docx/v1/documents/{doc_id}/blocks/{doc_id}/children'
        res = requests.post(url, headers=self.headers, json={"children": blocks})
        data = res.json()
        if data['code'] != 0:
            raise Exception(f"写入内容失败: {data['msg']}")
        return data


# ============ Block 构造函数（从规范文档提取）============

def create_heading1(text):
    return {"block_type": 3, "heading1": {"elements": [{"text_run": {"content": text}}]}}

def create_heading2(text):
    return {"block_type": 4, "heading2": {"elements": [{"text_run": {"content": text}}]}}

def create_text(text):
    return {"block_type": 2, "text": {"elements": [{"text_run": {"content": text}}]}}

def create_bullet(text):
    return {"block_type": 12, "bulleted_list": {"elements": [{"text_run": {"content": text}}]}}

def create_numbered(text):
    return {"block_type": 13, "numbered_list": {"elements": [{"text_run": {"content": text}}]}}

def create_divider():
    return {"block_type": 22, "divider": {}}


# ============ 主函数 ============

if __name__ == "__main__":
    writer = FeishuDocTableWriter()
    
    # 创建测试文档
    doc_id, url = writer.create_document("表格测试-合并方案", folder_token="Thhrfa3QglB5amdIMpEcY2tAndd")
    print(f"\n📄 文档创建: {url}\n")
    
    # 写入标题
    writer.write_content(doc_id, [
        create_heading1("🎯 两会AI政策速览"),
        create_text("数据来源：两会官方文件整理"),
        create_divider()
    ])
    
    # 写入表格1：三大关键信号
    print("\n写入表格1：三大关键信号")
    writer.write_table(doc_id, [
        ["关键词", "政策内容"],
        ["人工智能+", "与制造业、医疗、教育等实体行业深度融合"],
        ["场景驱动", "优先支持有实际应用场景的AI项目，避免空转"],
        ["普惠AI", "降低中小企业使用AI的门槛，避免技术垄断"]
    ], header_row=True)
    
    # 写入分隔
    writer.write_content(doc_id, [create_divider()])
    
    # 写入表格2：3大机会
    print("\n写入表格2：3大机会")
    writer.write_table(doc_id, [
        ["机会方向", "门槛", "收益", "说明"],
        ["行业AI解决方案", "★★★", "★★★★★", "有特定行业经验，把大模型和行业痛点结合"],
        ["AI应用层创业", "★★★★", "★★★★★", "做垂直场景AI应用，类似移动互联网时代的APP"],
        ["AI技能培训", "★★", "★★★★", "教别人怎么用AI，门槛低，市场需求大"]
    ], header_row=True)
    
    print(f"\n✅ 全部完成！文档链接: {url}")
