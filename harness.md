## Harness

- CLAUDE.md 项目说明，每次自动加载
- Hooks 在特定时机自动执行的事件触发器
- Skills 专业技能包，按需加载
- Plugins Skills + Hooks + MCP打包分发
- LSP IDE级代码导航
- MCP 连接外部工具和数据源
- SubAgent 独立上下文并行执行

模型选择

```bash
# 启动时指定
claude  --model sonnet/opus/haiku
# 在运行过程中切换
/model sonnet

# 在配置文件中指定
.claude/settings.json
```

```bash
/init
/compact
/clear
/context
/memory
/status
# 查看当前会话费用
/cost
# 项目代码审查
/review
/plan
# 回滚修改
/rewind
/resume
# 顺便问一句
/btw
/skill
/agent
/plugin
# 从质量/性能和复用性优化
/simplify
```

## 工作流

1. explore 探索
2. plan 规划
3. implement 实现
4. commit 提交


2. 任务颗粒度要小且聚焦
3. 频繁重置上下文
4. 复杂任务从plan开始
5. 使用skill和subagent卸载长任务
6. 接入MCP/LSP