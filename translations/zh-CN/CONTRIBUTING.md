# 贡献

本仓库组织为博客系列和可运行的笔记本示例。

## 提交拉取请求之前

运行本地验证脚本：

```powershell
python scripts\verify_notebooks.py
```

对于实现或笔记本更改，运行本地安全笔记本执行：

```powershell
python scripts\verify_notebooks.py --execute
```

## 笔记本指南

- 保持笔记本可读且专注于相关文章。
- 不要提交保存的笔记本输出或执行计数。
- 除非文章需要特定的外部资源，否则使用 `sample_data/` 中的小样本数据。
- 行为变化时，在相关文章中记录验证结果。

## 秘密和凭据

- 不要提交 API 密钥、令牌、密码、私有端点或 `.env` 文件。
- `.env.example` 仅用于占位符值。
- 使用环境变量进行可选的本地 Ollama 实验。

## 文档

- 保持文章导航链接更新。
- 添加新文章、笔记本、依赖文件或样本数据文件时，更新 `README.md`。
- 在发布可见仓库更新前，更新 `CHANGELOG.md`。

## 验证

GitHub Actions 工作流运行：

```powershell
python scripts\verify_notebooks.py
python scripts\verify_notebooks.py --execute
```

`drafts/` 下的草稿材料在准备公开索引之前不会被仓库验证执行。

## 问题

对于文章纠正使用文章反馈模板，对于笔记本执行问题使用笔记本问题模板。

---

<!-- CO-OP TRANSLATOR DISCLAIMER START -->
**免责声明**：
本文件由 AI 翻译服务 [Co-op Translator](https://github.com/Azure/co-op-translator) 翻译完成。尽管我们力求准确，但请注意，自动翻译可能包含错误或不准确之处。原始语言版文件应视为权威来源。对于重要信息，建议使用专业人工翻译。我们对因使用本翻译而产生的任何误解或误释不承担责任。
<!-- CO-OP TRANSLATOR DISCLAIMER END -->