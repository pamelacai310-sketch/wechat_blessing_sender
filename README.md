# 保险合同条款对比程序

这是一个基于 Python 的命令行工具，用于对比两版保险合同条款，输出：

- 新增条款
- 删除条款
- 修改条款（带 unified diff）

## 使用方式

```bash
python insurance_clause_compare.py old.txt new.txt
```

可选输出到文件：

```bash
python insurance_clause_compare.py old.txt new.txt -o result.txt
```

## 条款识别规则

程序会把以下常见格式识别为“条款标题”：

- `第1条 ...` / `第一条 ...`
- `一、...`
- `1. ...` / `1、...`

如果没有识别到条款标题，会把全文作为“总则”进行整体比较。
