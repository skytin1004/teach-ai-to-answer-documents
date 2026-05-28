# Scripts

此文件夹包含仓库验证脚本。

## `verify_notebooks.py`

验证本地 Markdown 链接、笔记本 JSON、笔记本输出清洁度以及高风险秘密模式：

```powershell
python scripts\verify_notebooks.py
```

执行所有公共的本地安全笔记本：

```powershell
python scripts\verify_notebooks.py --execute
```

GitHub Actions 工作流程使用相同的脚本。

未准备好公开索引的草稿材料位于 `drafts/` 下，会被跳过。

---

<!-- CO-OP TRANSLATOR DISCLAIMER START -->
**免责声明**：
本文件由 AI 翻译服务 [Co-op Translator](https://github.com/Azure/co-op-translator) 翻译完成。尽管我们力求准确，但请注意，自动翻译可能包含错误或不准确之处。原始语言版文件应视为权威来源。对于重要信息，建议使用专业人工翻译。我们对因使用本翻译而产生的任何误解或误释不承担责任。
<!-- CO-OP TRANSLATOR DISCLAIMER END -->