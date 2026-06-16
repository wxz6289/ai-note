# 部署笔记仓库

将 AI 笔记的变更提交并推送到远程仓库。

## 步骤

1. 先检查仓库状态，确认有需要提交的变更：

```bash
cd /Users/dreamerking/ai-note
git status
```

1. 如果没有变更，提前告知用户并退出。

1. 如果有变更，用用户上次提交时使用的约定格式生成提交信息：

- 前缀参考: `docs(ai):` / `chore:` / `feat:` / `fix:` / `refactor:`
- 使用中文描述变更内容
- 尽量简洁（50 字以内）

可以参考最近的提交历史来决定前缀和风格：

```bash
git log --oneline -5
```

1. 用生成的信息提交所有变更：

```bash
git add -A
git commit -m "<提交信息>"
```

1. 推送到远程：

```bash
git push
```

1. 输出推送结果给用户。
