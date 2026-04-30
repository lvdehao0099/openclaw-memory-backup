# 办公软件配置

## LibreOffice 安装
**安装时间：** 2026-03-10
**版本：** LibreOffice 24.2.7.2
**组件：** Writer（文档）, Calc（表格）
**命令：** `libreoffice`, `soffice`

## 用途
- 编辑 .docx 报价单、合同
- 处理 .xlsx 表格数据
- 转换文档格式

## 常用命令
```bash
# 转换 docx 为其他格式
libreoffice --headless --convert-to pdf input.docx

# 编辑文档（后台处理）
soffice --headless --accept="socket,host=localhost,port=2002;urp;"
```
