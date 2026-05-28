# 发布检查清单

在提交或推送公共更新之前使用此清单。

## 安全性

- 确认没有将 API 密钥、令牌、密码或私有端点写入 Markdown 文件、笔记本、示例数据或脚本中。
- 将凭据保存在环境变量或托管身份中，不要写入已提交的文件。
- 不要提交 `.env` 文件或已执行的笔记本输出文件。
- 保持 `.env.example` 仅作占位符使用。

## 验证

运行仓库验证脚本：

```powershell
python scripts\verify_notebooks.py
```

在发布实现更改之前，运行完整的本地安全笔记本执行：

```powershell
python scripts\verify_notebooks.py --execute
```

预期检查：

- 本地 Markdown 链接通过
- 笔记本 JSON 验证通过
- 笔记本不包含保存的输出或执行计数
- 高风险秘密模式扫描通过
- 公开笔记本能够在本地执行
- 故意跳过 `drafts/` 下的草稿材料

## 审核

- 确认 README 文章链接指向预期文件。
- 确认每篇文章都有仓库导航和相关笔记本链接。
- 确认草稿不会从公共索引中链接，除非它们已准备好发布。
- 确认 GitHub issue 和 pull request 模板仍符合仓库工作流程。
- 确认文章中的验证结果与最新笔记本输出匹配。
- 确认 push 后预期会触发 GitHub Actions 工作流运行。
- 确认 `CHANGELOG.md` 反映正在发布的更新。
- 确认 `CONTRIBUTING.md` 仍符合仓库工作流程。

## Git

- 审查 `git status --short --branch`。
- 审查 `git diff --stat`。
- 仅在明确准备好时提交和推送。

---

<!-- CO-OP TRANSLATOR DISCLAIMER START -->
**免责声明**：
本文件由 AI 翻译服务 [Co-op Translator](https://github.com/Azure/co-op-translator) 翻译完成。尽管我们力求准确，但请注意，自动翻译可能包含错误或不准确之处。原始语言版文件应视为权威来源。对于重要信息，建议使用专业人工翻译。我们对因使用本翻译而产生的任何误解或误释不承担责任。
<!-- CO-OP TRANSLATOR DISCLAIMER END -->