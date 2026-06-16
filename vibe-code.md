# Vibe Coding：详解、实操流程与最佳实践

## 一、什么是 Vibe Coding

### 1.1 起源与定义

**Vibe Coding**（氛围编程 / 直觉编程）一词由前 Tesla AI 总监、OpenAI 联合创始人 **Andrej Karpathy** 于 **2025 年 2 月** 在 X（Twitter）上提出，迅速成为 AI 编程领域最具讨论度的概念之一。

Karpathy 的原话：

> "There's a new kind of coding I call 'vibe coding', where you fully give in to the vibes, embrace exponentials, and forget that the code even exists. [...] I 'Accept All' always, I don't read the diffs anymore. When I get error messages I just copy paste them in with no comment, usually that fixes it. The code grows beyond my usual comprehension, [...] but it's not really coding — I just see stuff, say stuff, run stuff, and copy paste stuff, and it mostly works."

**核心含义**：开发者不再逐行手写和细读代码，而是通过**自然语言**（口语或文字）向 AI Agent 描述意图，让 AI 生成、修改、调试代码；开发者以「看效果、说需求、跑程序、贴报错」的方式驱动开发，追求**速度、心流和快速迭代**，而非对每一行代码的完全掌控。

### 1.2 学术视角

剑桥大学与微软研究院 2025 年发表的论文 *Vibe coding: programming through conversation with artificial intelligence* 将其定义为：

> 开发者主要通过与代码生成型大语言模型交互来「写代码」，而非直接编写代码的一种新兴编程范式。

论文发现，Vibe Coding 并不消除编程 expertise 的需求，而是将其**重新分配**到：
- **上下文管理**（给 AI 什么信息）
- **快速代码评估**（扫一眼、跑一下判断是否 OK）
- **切换时机判断**（何时让 AI 做、何时自己上手改）

### 1.3 与 AI 编程、AI 辅助工程的关系

| 维度 | Vibe Coding | AI 辅助工程（AI-Assisted Engineering） |
|---|---|---|
| **心态** | 「忘记代码存在」，Accept All | 「AI 是结对伙伴」，逐行 review |
| **Prompt 风格** | 高层面、口语化、模糊 | 结构化、带约束、带上下文 |
| **代码审查** | 最小化或不审查 diff | 严格审查每一行 AI 输出 |
| **测试** | 跑起来能看就行 | TDD、CI、覆盖率要求 |
| **适用场景** | 原型、MVP、周末项目、学习 | 生产系统、团队协作、长期维护 |
| **风险容忍** | 高（快速试错） | 低（质量、安全优先） |

Addy Osmani 的总结：**Vibe Coding 和 AI 辅助工程不是一回事**。前者是创意沙盒，后者是在成熟工程流程中把 AI 当作 force multiplier。两者之间存在一条**光谱**——从纯 vibe 到 spec-driven 再到严格工程，可以根据项目阶段灵活切换。

```
纯 Vibe Coding ←—— 光谱 ——→ AI 辅助工程
  周末原型          Spec-driven         生产级系统
  Accept All        Plan → 实现 → 测试    设计文档 + CR + TDD
```

---

## 二、Vibe Coding 的核心特征

### 2.1 「Material Disengagement」（与代码物质层面的脱钩）

论文提出：Vibe Coding 是知识工作中 **material disengagement**（与材料脱钩）的首次大规模实践——开发者不再直接操作「代码」这一材料，而是通过 AI 中介来编排代码的生产与编辑。

### 2.2 迭代目标满足循环（Iterative Goal Satisfaction）

Vibe Coding 的工作流不是线性的「需求 → 设计 → 编码 → 测试」，而是循环的：

```
设定目标 → Prompt AI → 评估输出 → 接受/拒绝 → 运行测试
    ↑                                              ↓
    └──── 发现问题 → 贴报错 / 改 Prompt / 手动编辑 ←┘
```

### 2.3 Context Momentum（上下文动量）

早期 Prompt 和 AI 的解读会**锁定项目轨迹**——第一个「差不多能用」的实现会成为后续所有生成的基础。好处是可以快速探索；风险是错误方向会被放大，后期难以纠正。

**示例**：你让 AI 做「历史汇率查询」，AI 理解成「选单日」，你觉得也行就接受了；后面你要「日期范围查询」，AI 仍按单日模式生成——这就是 context momentum 的负面效应。

### 2.4 信任是动态的，而非 blanket acceptance

即使是 Karpathy 式的「Accept All」，实践中开发者仍会通过**运行结果**来验证——能跑、能看、符合预期就继续；不行就贴报错或换方向。信任是通过迭代验证建立的，而非盲目信任。

---

## 三、适用场景与不适用场景

### ✅ 适合 Vibe Coding

| 场景 | 说明 |
|---|---|
| **快速原型 / MVP** | 48 小时从想法到可演示的产品 |
| **周末项目 / Side Project** | Karpathy 所称的 "throwaway weekend projects" |
| **Hackathon / Demo** | 追求速度而非代码质量 |
| **个人工具 / 脚本** | 一次性或低频使用的自动化脚本 |
| **UI / 前端快速迭代** | 「按钮再红一点」「加个动画」 |
| **学习新技术** | 通过 vibe 快速体验框架，事后再读代码学习 |
| **胶水代码 / 迁移脚本** | Docker Compose → Terraform 等重复性转换 |
| **探索性项目** | 「看看 AI 能推到什么程度」 |

### ❌ 不适合 Vibe Coding（应切换到 AI 辅助工程）

| 场景 | 原因 |
|---|---|
| **生产级系统** | 安全、性能、可维护性要求高 |
| **支付 / 认证 / 权限** | AI 容易出 subtle bug（如 truthy 取反错误） |
| **高并发 / 大数据量** | AI 生成的查询可能在小数据集 OK、生产环境崩溃 |
| **团队协作的长期项目** | 无人理解的代码 = trust debt |
| **合规 / 审计要求** | 需要可追溯的设计决策和代码审查 |
| **核心算法 / 性能关键路径** | 需要人类深度理解和优化 |

---

## 四、实操流程（完整 SOP）

### Phase 0：准备（5–15 分钟）

**目标**：给 AI 一个干净的起点，减少幻觉和跑偏。

1. **选工具**
   - IDE Agent：Cursor（Agent/Composer）、Windsurf、Cline
   - 零代码平台：Bolt、Lovable、v0（纯 vibe，不写代码）
   - CLI Agent：Claude Code、Amazon Q CLI、Aider

2. **初始化项目**
   ```bash
   # 方式 A：从空目录开始（纯 vibe）
   mkdir my-project && cd my-project
   
   # 方式 B：用 Starter Template（推荐，减少 boilerplate 错误）
   npx create-next-app@latest my-app
   
   # 方式 C：在已有代码库上继续 vibe（需 @ 引用上下文）
   ```

3. **配置 AI 上下文**（可选但强烈推荐）
   - 创建 `.cursor/rules` 或 `AGENTS.md`，写入：
     - 技术栈（Next.js 15 + Tailwind + Prisma）
     - 编码风格（函数式、不用 class）
     - 禁止事项（不要用 jQuery、不要硬编码 API Key）
   - 配置 `.cursorignore` 排除 `node_modules`、`.env`

4. **写一份「够用的 Spec」**（即使 vibe 也不建议完全零规划）
   - 用 Excalidraw / 纸笔 / 甚至让 AI 帮你写：
     - 核心功能列表（3–5 条）
     - 用户流程（登录 → 上传 → 查看结果）
     - 技术选型
   - 工具辅助：CodeGuide.dev 可从需求生成项目计划和文档

### Phase 1：第一轮生成（「让它跑起来」）

**目标**：尽快得到一个可运行的 skeleton。

**Prompt 模板**：

```
我要做一个 [一句话描述产品]。

核心功能：
1. [功能 1]
2. [功能 2]
3. [功能 3]

技术栈：[框架/语言/数据库]
风格：[简洁/现代/暗色主题]

请先搭建项目结构，实现最核心的 [功能 1]，能跑起来就行。
不要一次性做全部功能。
```

**操作要点**：
- 一次只做一个 phase / 一个功能
- Agent 模式下让 AI 自动创建文件、装依赖、跑 dev server
- **不要读 diff**，等它跑完看浏览器效果

### Phase 2：迭代目标满足循环（核心阶段，占 70% 时间）

这是 Vibe Coding 的主战场。每一轮循环：

#### Step 1：看效果 → 形成下一个目标

打开浏览器 / 终端，看当前效果。用自然语言描述差距：

```
# 好的 vibe prompt（具体 + 感性）
"登录按钮太小了，放大一点，改成蓝色"
"列表加载太慢，加个 skeleton loading"
"这个弹窗太丑了，参考 Linear 的风格改"

# 不好的 prompt（太模糊）
"改好看一点"
"优化一下"
```

#### Step 2：Prompt AI → Accept

- Agent 模式：描述需求，等 AI 改完
- 小改动：Inline Edit（选中代码 + Cmd+K）
- **Karpathy 式**：Accept All，不读 diff

#### Step 3：运行验证

```bash
# 前端：看浏览器
npm run dev

# 后端：curl 或看 terminal 输出
curl localhost:3000/api/health

# 有报错？进入 Step 4
```

#### Step 4：调试（Vibe 式）

**Karpathy 调试三板斧**：

```
1. 复制完整报错信息
2. 粘贴到 AI 对话框
3. 不加任何解释，等 AI 修

# 示例
> TypeError: Cannot read properties of undefined (reading 'map')
  at UserList (src/components/UserList.tsx:12:24)
  
  [粘贴，不加 comment]
```

**进阶调试**（当三板斧不够时）：

| 策略 | 做法 |
|---|---|
| **截图** | 截 UI 问题发给 AI（需模型支持 vision） |
| **贴 DevTools** | 复制 Console / Network 错误 |
| **换模型** | Claude 搞不定的换 GPT，或反之 |
| **新开会话** | 开新 Composer 窗口，清除 context momentum |
| **关 tab 清上下文** | 关闭所有文件 tab 再 Prompt |
| **手动改** | 小改动（改个颜色、改个变量名）自己改比 Prompt 更快 |

#### Step 5：重复直到当前 sub-goal 满足

每个 sub-goal 完成后，再 Prompt 下一个功能：

```
"OK 登录功能可以了。现在做第二个功能：用户可以上传 PDF 简历"
```

### Phase 3：功能叠加（逐步扩展）

**按 phase 推进，不要一次要太多**：

```
Phase 1: 项目骨架 + 首页          ✅
Phase 2: 用户认证（先用 dummy data） ✅
Phase 3: 核心功能（简历上传）      ← 当前
Phase 4: 支付集成（Stripe）
Phase 5: 部署上线
```

**Scope Limitation Prompt**：

```
"不要集成 Stripe，先用 dummy data 做支付页面的 UI"
"只做后端 API，前端暂时用 hardcode 数据"
```

### Phase 4：收尾与决策（关键分叉点）

项目能 demo 了，你需要做一个**conscious decision**：

| 路径 | 做法 | 适用 |
|---|---|---|
| **A. 扔掉重写** | vibe 产物是 throwaway，用 spec 重新 AI 辅助工程 | 验证了想法，要上生产 |
| **B. 局部加固** | 保留 UI/结构，重写 auth/支付等关键模块 | MVP 基本可用 |
| **C. 直接上线** | 个人 side project、内部工具 | 低风险的场景 |
| **D. 继续 vibe** | 加功能、改 UI，不担心代码质量 | 还在探索阶段 |

---

## 五、Prompt 策略详解

### 5.1 粒度光谱：从「 dumb question」到「精确指令」

Cambridge 论文观察到的有效策略：**先用高层 Prompt，不行再加细节**。

```
# Level 1：高层（先试）
"创建一个 API 来新建对话"

# Level 2：AI 搞不定，加具体
"在 src/app/api/conversations/route.ts 中创建 POST endpoint，
 接收 { repo_id, title }，返回 { id, created_at }"

# Level 3：仍不行，给示例
"API 应该返回这样的 JSON：
 { \"id\": \"abc123\", \"title\": \"New Chat\", \"created_at\": \"2025-01-01T00:00:00Z\" }"
```

### 5.2 混合精确与模糊

Vibe Coding 的独特之处：**审美类需求故意模糊**，让 AI 发挥。

```
# 精确（布局、逻辑）
"箭头不要对角线，箭头尖指向方框中心"
"日期移到下方，用很小的字体"

# 模糊（审美、风格）
"整体风格参考 Linear，暗色主题"
"让页面看起来更 modern 一点"
"间距再 narrow 一些"
```

### 5.3 上下文管理技巧

| 技巧 | 说明 |
|---|---|
| **@ 引用文件** | `@src/auth.ts` 让 AI 看到现有代码 |
| **新开会话** | 切换功能模块时开新 Composer，避免 context 污染 |
| **关 tab** | 关闭无关文件 tab，减少 AI 误读 |
| **贴文档 URL** | "参考 https://tanstack.com/form 实现表单" |
| **贴错误信息** | 完整 stack trace，不要截断 |
| **Meta-Prompt** | 让 AI 先帮你写 Prompt，再执行 |
| **Phase 拆分** | "只做 Phase 1，不要动其他文件" |

### 5.4 输入模式

| 模式 | 适用 | 工具 |
|---|---|---|
| **文字** | 默认，最精确 | 所有 AI IDE |
| **语音** | 快速描述 UI 改动，Karpathy 推荐 | Cursor + Whisper / Mac 听写 |
| **截图** | UI 问题、设计参考 | Cursor（vision 模型） |
| **代码片段** | 指定修改范围 | Inline Edit / @ 引用 |

---

## 六、最佳实践

### 6.1 黄金法则

> **如果你不会 merge 一个初级开发者不 review 就提交的代码，那也不要 merge AI 不 review 的代码。**
> — Agentic Coding Handbook

### 6.2 十条实践准则

#### 1. 分阶段切换模式

```
探索期 → Vibe Coding（快、不审查）
验证期 → Spec-driven（写计划、分 phase）
生产期 → AI 辅助工程（review、测试、CI）
```

不要在同一个项目里混用两种心态——要么 vibe 到底（知道要扔），要么从第一天就 engineering。

#### 2. 小步、单目标 Prompt

- ❌ "做一个完整的电商网站，包含用户系统、购物车、支付、后台管理"
- ✅ "先做产品列表页，展示 dummy 数据，卡片式布局"

#### 3. 用 Git 做安全网

```bash
# 每完成一个 sub-goal 就 commit
git add -A && git commit -m "feat: login page with dummy auth"

# AI 改坏了？一键回滚
git checkout -- .
# 或
git reset --hard HEAD~1
```

Vibe Coding **必须**用版本控制——这是唯一的 undo 按钮。

#### 4. 定期「落地检查」

每 30–60 分钟暂停 vibe，做 5 分钟 reality check：

- [ ] 项目还能跑吗？（`npm run dev` / `npm test`）
- [ ] 有没有引入不必要的依赖？
- [ ] `.env` 里有没有误提交密钥？
- [ ] 代码量是否已超出你的理解范围？

#### 5. 知道何时从 Vibe 切换到 Manual

| 信号 | 行动 |
|---|---|
| 同一个 bug AI 修了 3 次还没好 | 自己看代码、手动修 |
| 改动只需 1–2 行 | 手动改比 Prompt 快 |
| 涉及核心业务逻辑 | 自己写或逐行 review |
| AI 加了不需要的功能 | 手动删除 + 加约束 Prompt |

#### 6. 限制 scope，延迟集成

```
"先别接 Stripe，用 dummy 数据"
"先别做移动端适配"
"先别加国际化"
```

AI 倾向于 over-engineer——你需要主动做减法。

#### 7. 安全底线（即使 vibe 也不能省）

- **绝不**把 API Key / 密码粘贴到 Prompt 中
- 涉及 auth / 支付时，至少让 AI 做一次 security check：
  ```
  "Review the auth module for common security issues:
   SQL injection, XSS, insecure session handling, missing input validation"
  ```
- 上线前检查：`.env` 在 `.gitignore` 中、HTTPS、CORS 配置

#### 8. 对抗 Context Momentum

- 新功能模块 → **新开会话**
- 感觉 AI 方向偏了 → 回滚 Git + 重新 Prompt
- 大功能用 **Spec 文档** 锚定方向，避免被 AI 带偏

#### 9. 记录 Intent，而非 Code

Vibe 产物可能看不懂，但你的 **意图** 应该被记录：

```markdown
# project-log.md
## 2025-06-10
- 决定用 Next.js App Router（AI 推荐的，可以接受）
- 认证先用 NextAuth，后续可能换 Clerk
- 支付还没做，Phase 4 再做
- AI 生成的 middleware 有问题，手动重写了 auth check
```

#### 10. 事后学习（Vibe → Understand）

Karpathy 自己也说代码会超出理解范围。项目完成后：

- 让 AI 解释关键模块："Explain how the auth flow works"
- 读一遍生成的代码，标记不理解的部分
- 这是 vibe coding 的 **learning dividend**——先跑起来，再理解

---

## 七、常见陷阱与应对

| 陷阱 | 表现 | 应对 |
|---|---|---|
| **Trust Debt** | 堆了 1000 行 AI 代码，没人懂 | 定期 review；关键模块手动写 |
| **Context Momentum** | 早期错误决策被放大 | 新会话 + Git 回滚 |
| **Over-engineering** | AI 加了 6 个用不到的 npm 包 | Scope limitation Prompt |
| **Security Blind Spot** | API Key 硬编码、SQL 注入 | 上线前 security review |
| **Performance Time Bomb** | 小数据集 OK，生产崩溃 | 关键查询手动 review |
| **Spaghetti Architecture** | middleware 散落 6 个文件 | 到 Phase 4 前做架构整理 |
| **False Confidence** | 测试通过 ≠ 生产可用 | 用真实数据量测试 |
| **Review 甩锅** | 自己不读 PR 就丢给同事 | 专业底线：自己的代码自己负责 |

---

## 八、工具推荐

### 8.1 按 Vibe 程度排序

| 工具 | Vibe 指数 | 说明 |
|---|---|---|
| **Bolt / Lovable / v0** | ⭐⭐⭐⭐⭐ | 零代码 vibe，浏览器里描述即可 |
| **Cursor Agent** | ⭐⭐⭐⭐ | Karpathy 用的，Accept All 友好 |
| **Windsurf Cascade** | ⭐⭐⭐⭐ | Agent 模式，自动执行 |
| **Claude Code (CLI)** | ⭐⭐⭐⭐ | 终端 vibe，适合后端/脚本 |
| **Cline** | ⭐⭐⭐ | 开源 Agent，自主性高 |
| **GitHub Copilot Chat** | ⭐⭐ | 更偏辅助，需更多手动 |
| **Continue** | ⭐⭐ | 轻量，灵活但自主性低 |

### 8.2 Vibe Coding 工具链

```
规划：Excalidraw / CodeGuide.dev / AI 写 Spec
  ↓
编码：Cursor / Windsurf / Claude Code
  ↓
预览：Browser / DevTools Console
  ↓
调试：贴报错 → AI / 换模型 / 手动
  ↓
版本：Git（commit 每个 sub-goal）
  ↓
部署：Vercel / Railway / AI 帮你 deploy
```

---

## 九、从 Vibe Coding 到 AI 辅助工程的升级路径

当你准备把 vibe 产物推向生产时，按以下步骤「升级」：

```
1. 冻结功能 → 不再 vibe 加新功能
2. 写/补 Spec → 让 AI 帮你生成架构文档
3. 安全审计 → 让 AI review auth/支付/输入验证
4. 补测试 → 让 AI 生成单元测试 + 集成测试
5. 重构关键路径 → 手动或 AI 辅助重写核心模块
6. 代码审查 → 逐文件 review，理解每一行
7. 建立 CI → lint + test + type check
8. 部署 →  staging 环境验证后再上生产
```

---

## 十、三种开发者人格（Addy Osmani）

| 人格 | 特征 | 结果 |
|---|---|---|
| **Vibe Coder** | 太多自由，Accept All，不 review | 快但 fragile |
| **Rodeo Cowboy** | 高风险的 cowboy coding + AI | 偶尔 spectacular，经常 disaster |
| **Prisoner** | 太多约束，拒绝 AI | 安全但无创新 |

**理想状态**：在 Vibe 和 Engineering 之间找到平衡——**足够的 rope 来创新，足够的 discipline 来不把自己吊死**。

---

## 十一、总结

Vibe Coding 是一种**以自然语言驱动、以效果验证为导向、以速度优先**的 AI 编程范式。它降低了编程门槛，让非专业开发者也能快速构建原型，让专业开发者以 10x 速度探索想法。

**核心公式**：

> **See → Say → Run → Paste → Repeat**

**三条铁律**：

1. **Know when to vibe, know when to engineer** — 原型 vibe，生产 engineer
2. **Git is your undo button** — 没有版本控制的 vibe 是裸奔
3. **Trust but verify through running** — 不读 diff 可以，但不跑就 accept 不行

Vibe Coding 不是软件工程的终点，而是**从想法到可运行原型最短路径**。它的真正价值在于压缩「验证想法」的时间成本——至于验证之后要不要、能不能上生产，那是另一个阶段的故事。
