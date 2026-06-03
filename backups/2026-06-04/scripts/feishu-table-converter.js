/**
 * 飞书文档表格转换器
 * 将 Markdown 表格转换为飞书真正的 Table Block
 */

const { getToken, fetchWithAuth } = require('/root/.openclaw/extensions/feishu/feishu-common/index.js');

// 解析 Markdown 表格
function parseMarkdownTable(lines) {
    const rows = [];
    let i = 0;
    
    while (i < lines.length) {
        const line = lines[i].trim();
        if (line.startsWith('|') && line.endsWith('|')) {
            const cells = line.slice(1, -1).split('|').map(c => c.trim());
            // 跳过分隔行 (|---|---|)
            if (!cells.every(c => /^[-:]+$/.test(c))) {
                rows.push(cells);
            }
            i++;
        } else {
            break;
        }
    }
    
    return { rows, consumed: i };
}

// 创建表格块并填充内容
async function createTableBlock(docToken, rows) {
    if (rows.length === 0) return null;
    
    const colCount = rows[0].length;
    const rowCount = rows.length;
    
    // 1. 创建空表格
    const tableBlock = {
        block_type: 31, // Table
        table: {
            property: {
                row_size: rowCount,
                column_size: colCount,
                column_width: Array(colCount).fill(100)
            }
        }
    };
    
    const createRes = await fetchWithAuth(
        `https://open.feishu.cn/open-apis/docx/v1/documents/${docToken}/blocks/${docToken}/children`,
        {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ children: [tableBlock] })
        }
    );
    const createData = await createRes.json();
    
    if (createData.code !== 0) {
        console.error('创建表格失败:', createData.msg);
        return null;
    }
    
    const tableBlockId = createData.data.children[0].block_id;
    const cellIds = createData.data.children[0].table.cells;
    
    // 2. 填充单元格内容
    for (let r = 0; r < rowCount; r++) {
        for (let c = 0; c < colCount; c++) {
            const cellIndex = r * colCount + c;
            const cellId = cellIds[cellIndex];
            const content = rows[r][c] || '';
            
            if (content) {
                const textBlock = {
                    block_type: 2, // Text
                    text: {
                        elements: [{
                            text_run: { content: content }
                        }],
                        style: {}
                    }
                };
                
                await fetchWithAuth(
                    `https://open.feishu.cn/open-apis/docx/v1/documents/${docToken}/blocks/${cellId}/children`,
                    {
                        method: 'POST',
                        headers: { 'Content-Type': 'application/json' },
                        body: JSON.stringify({ children: [textBlock] })
                    }
                );
                
                // 避免请求过快
                await new Promise(resolve => setTimeout(resolve, 50));
            }
        }
    }
    
    console.log(`✓ 创建表格: ${rowCount}行 x ${colCount}列`);
    return tableBlockId;
}

// 创建文本块
async function createTextBlock(docToken, content, blockType = 2) {
    const block = {
        block_type: blockType,
        text: {
            elements: [{
                text_run: { content: content }
            }],
            style: {}
        }
    };
    
    // 根据内容判断块类型
    if (content.startsWith('### ')) {
        block.block_type = 5; // Heading3
        block.heading3 = { elements: [{ text_run: { content: content.slice(4) } }], style: {} };
        delete block.text;
    } else if (content.startsWith('## ')) {
        block.block_type = 4; // Heading2
        block.heading2 = { elements: [{ text_run: { content: content.slice(3) } }], style: {} };
        delete block.text;
    } else if (content.startsWith('# ')) {
        block.block_type = 3; // Heading1
        block.heading1 = { elements: [{ text_run: { content: content.slice(2) } }], style: {} };
        delete block.text;
    } else if (content.startsWith('- ')) {
        block.block_type = 12; // Bullet
        block.bullet = { elements: [{ text_run: { content: content.slice(2) } }], style: {} };
        delete block.text;
    } else if (content.startsWith('```')) {
        block.block_type = 14; // Code
        block.code = { elements: [{ text_run: { content: '' } }], style: { language: 1, wrap: false } };
        delete block.text;
    }
    
    const res = await fetchWithAuth(
        `https://open.feishu.cn/open-apis/docx/v1/documents/${docToken}/blocks/${docToken}/children`,
        {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ children: [block] })
        }
    );
    
    return res.json();
}

// 清空文档
async function clearDocument(docToken) {
    // 获取所有子块
    const res = await fetchWithAuth(
        `https://open.feishu.cn/open-apis/docx/v1/documents/${docToken}/blocks/${docToken}/children`,
        { method: 'GET' }
    );
    const data = await res.json();
    
    if (data.code === 0 && data.data?.items) {
        const blockIds = data.data.items.map(item => item.block_id);
        console.log(`找到 ${blockIds.length} 个块需要删除`);
        
        // 飞书不支持批量删除，只能逐个删除
        // 但可以通过重写文档来实现清空效果
        // 这里我们选择创建新文档
    }
    
    return data.data?.items?.length || 0;
}

module.exports = {
    parseMarkdownTable,
    createTableBlock,
    createTextBlock,
    clearDocument
};
