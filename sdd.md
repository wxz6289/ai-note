# Spec-Driven Development (SDD)：详解、实操流程与最佳实践

## 一、什么是 SDD

### 1.1 定义

**Spec-Driven Development（规格驱动开发，SDD）** 是一种以**结构化规格说明（Specification）** 为权威来源、以代码为实现细节的软件开发方法论。

核心原则：

> **代码是规格的实现细节，而非反过来。规格声明意图，代码实现意图。**

在 AI 编程时代，SDD 是对 **Vibe Coding** 失效模式的直接回应：AI 擅长模式补全，但不擅长读心。模糊 Prompt 导致 AI 做出大量未声明的假设；SDD 通过**明确、可验证的规格**，把 AI 从「猜需求」变成「执行合同」。

**对比示例**：

| 方式 | Prompt / 输入 | AI 的行为 |
|---|---|---|
| Vibe Coding | "给 app 加照片分享" | 猜测格式、权限、存储、压缩…… |
| SDD | "用户可上传 JPEG/PNG，最大 10MB；存 S3，key 前缀 user-id；仅上传者可删除；上传时缩放到 1024px" | 按合同实现，假设空间被消除 |

### 1.2 历史脉络

SDD 并非全新概念，而是旧思想在 AI 时代的新复兴：

| 前身 | 关系 |
|---|---|
| **TDD** | 测试即规格，Red-Green-Refactor |
| **BDD** | Gherkin Given/When/Then，可执行的业务规格 |
| **API-First / Design-First** | OpenAPI 定义契约，再生成代码 |
| **Model-Based Design** | Simulink 模型 → 生成嵌入式 C 代码 |
| **Design by Contract** | 前置/后置条件作为规格 |

AI 编程助手（2023–2025）让 SDD 从「理想实践」变成「刚需」——GitHub Spec Kit、AWS Kiro、Cursor Plan Mode 等工具都围绕 Spec → Plan → Tasks → Implement 构建工作流。

### 1.3 在 AI 编程光谱中的位置

```
Vibe Coding  ←——  SDD  ——→  AI 辅助工程
  无规格、Accept All    规格先行、分阶段审查    严格 CR + TDD + CI
  周末原型              功能开发 / MVP 升级       生产级长期维护
```

SDD 是 **Vibe Coding 与 AI 辅助工程之间的桥梁**：保留 AI 的速度，补上 Vibe 缺失的结构与问责链。

---

## 二、规格权威光谱（三个级别）

根据 arXiv 论文 *Spec-Driven Development: From Code to Contract*，SDD 有三个严格程度递增的级别：

```
Code-First → Spec-First → Spec-Anchored → Spec-as-Source
  代码为王      规格引导初建     规格与代码同步      规格即源码
```

### 2.1 Spec-First（规格先行）

- **做法**：编码前先写 Spec，指导初始实现；实现完成后 Spec 可丢弃或允许漂移
- **价值**：防止 AI 猜需求，显著提升首次生成质量
- **适用**：新功能开发、AI 辅助初建、原型验证
- **局限**：不防长期 drift

### 2.2 Spec-Anchored（规格锚定）⭐ 生产系统 sweet spot

- **做法**：Spec 与代码**全生命周期同步**；行为变更时先改 Spec 再改代码
- ** enforcement**：BDD 场景、契约测试、CI 校验 Spec 与实现一致
- **适用**：生产系统、多维护者、API 集成、企业功能
- **代表工具**：Cucumber、OpenAPI + Specmatic、GitHub Spec Kit

### 2.3 Spec-as-Source（规格即源码）

- **做法**：人类**只编辑 Spec**，代码完全由 Spec 生成，禁止手改
- **适用**：OpenAPI 生成 Server Stub、Simulink 生成车载 C 代码、Tessl
- **要求**：生成工具成熟且可信；目前通用软件开发中仍较激进

### 2.4 选择决策树

```
新功能 / 新系统？
  ├─ 用 AI 辅助？→ 至少 Spec-First
  ├─ 长期维护？多维护者？→ Spec-Anchored
  └─ 代码生成工具成熟可信？→ Spec-as-Source

一次性原型 / 探索性编码？→ 不必 SDD，直接 Vibe
简单 CRUD、需求无歧义？→ 最小 Spec 即可
```

**黄金法则**：使用**能消除当前上下文歧义的最小规格严格度**。

---

## 三、SDD 核心工作流（四阶段）

```
Specify（定什么）→ Plan（怎么做）→ Implement（建出来）→ Validate（验对错）
      ↓                ↓                  ↓                  ↓
   功能规格          技术方案            代码实现            测试验证
   人工审查          人工审查            人工审查            自动 + 人工
```

每个阶段产出**约束下一阶段的 Artifact**，形成从意图到实现的问责链。

---

## 四、实操流程（完整 SOP）

### Phase 0：Constitution First（项目宪法，一次性）

**在任何 Spec 之前**，先建立项目级持久规则。

**创建 `AGENTS.md` 或 `.specify/memory/constitution.md`**：

```markdown
# Project Constitution

## Tech Stack
- Language: Python 3.12
- Framework: FastAPI
- Database: PostgreSQL + SQLAlchemy
- Test: pytest

## Rules
- Never add runtime dependencies without an ADR
- All API endpoints require authentication except /health
- Use type hints on all public functions
- No hardcoded secrets; use environment variables

## Commands
- Install: `pip install -e ".[dev]"`
- Test: `pytest -v`
- Lint: `ruff check .`
- Type check: `mypy src/`

## Never / Ask / Always
- NEVER: commit .env, delete existing tests, use eval()
- ASK: before changing database schema, adding new service
- ALWAYS: run tests before marking task complete
```

**目录结构（GitHub Spec Kit 风格）**：

```
project/
├── AGENTS.md                    # 项目宪法
├── specs/
│   └── 001-user-auth/
│       ├── spec.md              # 功能规格
│       ├── plan.md              # 技术方案
│       ├── tasks.md             # 任务分解
│       └── checklists/          # 验证清单
├── src/
└── tests/
```

---

### Phase 1：Specify（写功能规格）

**目标**：回答「软件应该做什么」，**不涉及怎么做**。

#### Step 1.1：从一句话需求出发

```
原始想法："用户可以用邮箱 magic link 登录"
```

#### Step 1.2：让 AI 生成初稿 Spec（Self-Spec）

在 Cursor Plan Mode 或 Spec Kit 中：

```
/speckit.specify

用户可以用邮箱 magic link 登录。
```

或手动 Prompt：

```
根据以下需求，生成一份功能规格（spec.md），包含：
1. 用户故事
2. EARS 格式的验收标准
3. In Scope / Out of Scope
4. 边界 case 和错误条件

需求：用户可以用邮箱 magic link 登录
约束：参考 @AGENTS.md
```

#### Step 1.3：Spec 模板

```markdown
# Feature: Magic Link Authentication

## User Stories
- As a user, I want to log in via email magic link, so that I don't need to remember a password.

## Acceptance Criteria (EARS)

### Event-driven
- When the user submits a valid email on the login page, the system shall send a magic link within 30 seconds.
- When the user clicks a valid magic link within 15 minutes, the system shall create a session and redirect to /dashboard.

### Unwanted behavior
- If the email is not registered, then the system shall show the same success message (prevent enumeration).
- If the magic link is expired (>15 min), then the system shall show "Link expired, request a new one."
- If the magic link is already used, then the system shall reject it.

### State-driven
- While the user has an active session, the system shall persist login across page refreshes.

## In Scope
- Email input + submit on /login
- Magic link generation, email delivery (SMTP)
- Token validation + session creation
- Logout

## Out of Scope
- OAuth / social login
- Password-based login
- Two-factor authentication
- Rate limiting (Phase 2)

## Edge Cases
- Invalid email format → inline validation error
- SMTP failure → log error, show generic "try again later"
- Concurrent login from same link → first click wins

## Non-Functional
- Magic link token: cryptographically random, 256-bit
- Session: HttpOnly cookie, 7-day expiry
```

#### Step 1.4：Clarify  pass（消除歧义）

```
/speckit.clarify

Review spec.md and list all ambiguous requirements.
Ask me questions before proceeding to plan.
```

**人工审查 Checklist**：
- [ ] 每个需求可被不同读者一致理解？
- [ ] Out of Scope 是否明确关闭 AI 会「自作主张」的方向？
- [ ] 边界 case 和错误条件是否覆盖？
- [ ] 验收标准是否可测试（不是「好用」而是「30 秒内发送」）？

**⛔ 阶段门禁**：Spec 未经人工确认，**禁止进入 Plan**。

---

### Phase 2：Plan（写技术方案）

**目标**：回答「怎么做」，在 Spec 约束下做架构决策。

#### Step 2.1：生成 Plan

```
/speckit.plan

Based on @specs/001-user-auth/spec.md and @AGENTS.md,
create a technical plan.
```

#### Step 2.2：Plan 模板

```markdown
# Technical Plan: Magic Link Authentication

## Architecture
- Auth module: `src/auth/` (router, service, models)
- Session: JWT in HttpOnly cookie (not localStorage)
- Email: async via background task (FastAPI BackgroundTasks)

## Data Model
```sql
magic_links (
  id UUID PK,
  user_id UUID FK → users.id,
  token_hash VARCHAR(64),  -- store hash, not plaintext
  expires_at TIMESTAMP,
  used_at TIMESTAMP NULL,
  created_at TIMESTAMP
)
```

## API Endpoints
| Method | Path | Description |
|--------|------|-------------|
| POST | /auth/magic-link | Request magic link |
| GET | /auth/verify?token= | Verify token, create session |
| POST | /auth/logout | Clear session |

## Dependencies
- python-jose (JWT)
- aiosmtplib (async email)
- No new DB beyond magic_links table

## Security Decisions
- Token: secrets.token_urlsafe(32), store SHA-256 hash
- Email enumeration: same response for registered/unregistered
- HTTPS only for magic link URLs

## File Changes
- NEW: src/auth/router.py, service.py, models.py
- NEW: src/auth/email_templates/magic_link.html
- MODIFY: src/main.py (include auth router)
- NEW: tests/test_auth_magic_link.py
```

#### Step 2.3：人工审查 Plan

- [ ] 架构是否符合项目既有模式？
- [ ] 依赖是否最小化？
- [ ] 安全决策是否 explicit？
- [ ] 与 Spec 有无矛盾？

**⛔ 阶段门禁**：Plan 未经确认，**禁止生成代码**。

---

### Phase 3：Tasks（任务分解）

**目标**：把 Plan 拆成**原子、可测试、可独立 review** 的小任务。

```
/speckit.tasks

Break @specs/001-user-auth/plan.md into implementation tasks.
Each task should be completable in one agent session.
Mark dependencies between tasks.
```

#### Tasks 示例

```markdown
# Tasks: Magic Link Authentication

## Phase 1: Foundation
- [ ] T1: Create magic_links SQLAlchemy model + migration
- [ ] T2: Create auth router skeleton with /health check

## Phase 2: Core Flow
- [ ] T3: Implement POST /auth/magic-link (depends: T1)
      - Validate email, generate token, store hash, queue email
- [ ] T4: Implement GET /auth/verify (depends: T1, T3)
      - Validate token, create JWT session, mark link used
- [ ] T5: Email template + async send (depends: T3)

## Phase 3: Session & Logout
- [ ] T6: JWT middleware + session persistence (depends: T4)
- [ ] T7: POST /auth/logout (depends: T6)

## Phase 4: Tests
- [ ] T8: Unit tests for token generation/validation (depends: T3, T4)
- [ ] T9: Integration test: full magic link flow (depends: T7)
- [ ] T10: Edge case tests: expired, reused, invalid email (depends: T9)
```

**原则**：
- 每个 Task 可在**一次 Agent 会话**内完成
- 有依赖关系的 Task 标注 depends
- 测试 Task 独立列出，不混在实现 Task 中

---

### Phase 4：Implement（逐 Task 实现）

**目标**：AI 在 Spec + Plan + Task 约束下生成代码，人类逐 Task 审查。

#### Step 4.1：单 Task 执行

```
/speckit.implement T3

Implement task T3 from @specs/001-user-auth/tasks.md.
Follow @specs/001-user-auth/spec.md and @specs/001-user-auth/plan.md.
Run tests after implementation.
Do NOT implement tasks beyond T3.
```

**Cursor 等价操作**：
1. 打开 Agent 模式
2. @ 引用 spec.md + plan.md + tasks.md
3. Prompt：「Implement T3 only. Run pytest when done.」

#### Step 4.2：每 Task 完成后

```bash
# 1. 运行测试
pytest tests/test_auth_magic_link.py -v

# 2. 人工 spot-check（即使 AI 说通过了）
#    - 代码是否符合 Plan 的文件结构？
#    - 有无 hardcoded secret？
#    - 是否引入了 Spec 中 Out of Scope 的功能？

# 3. Git commit（关联 Spec）
git add -A
git commit -m "feat(auth): implement magic link request endpoint, refs specs/001-user-auth"
```

#### Step 4.3：Task 失败处理

| 情况 | 行动 |
|---|---|
| 测试失败，AI 修 2 次仍失败 | 人工介入 debug |
| 实现偏离 Spec | **先改 Spec**（若 Spec 有误）或 **让 AI 重做**（若实现有误） |
| 发现 Spec 遗漏 | 回到 Phase 1 更新 Spec，再继续 |
| Task 太大完不成 | 拆成更小的 sub-task |

---

### Phase 5：Validate（验证）

**目标**：确认代码满足 Spec，关闭问责环。

#### Step 5.1：自动化验证

```bash
# 单元 + 集成测试
pytest -v --cov=src/auth

# Lint + 类型检查
ruff check . && mypy src/

# Spec Kit checklist（如有）
/speckit.checklist
```

#### Step 5.2：Checklist 模板

```markdown
# Validation Checklist: Magic Link Auth

## Functional (from Spec)
- [ ] Valid email → magic link sent within 30s
- [ ] Click valid link → session created, redirect to /dashboard
- [ ] Expired link → error message shown
- [ ] Reused link → rejected
- [ ] Unregistered email → same success message (no enumeration)

## Security
- [ ] Token stored as hash, not plaintext
- [ ] Session cookie: HttpOnly, Secure, SameSite=Lax
- [ ] No secrets in code or git history

## Non-Functional
- [ ] All tests pass
- [ ] No new undeclared dependencies
- [ ] Out of Scope items NOT implemented
```

#### Step 5.3：验证失败的处理

```
Spec 正确 + 代码不对 → 修代码
Spec 不对 + 代码符合 Spec → 修 Spec，再决定要不要改代码
Spec 和代码都不对 → 修 Spec，重新 Implement 受影响 Task
```

**⛔ 原则**：Spec 始终是 authority——但 Spec 本身也需要人工审查，不是银弹。

---

## 五、EARS 标注法（写 AI 可执行的验收标准）

**EARS**（Easy Approach to Requirements Syntax）提供 5 种模式，把模糊需求变成可测试、AI 可解析的语句：

| 模式 | 模板 | 示例 |
|---|---|---|
| **Ubiquitous**（普遍） | The `<system>` shall `<response>` | The system shall display the user's email on the profile page. |
| **Event-driven**（事件驱动） | When `<trigger>`, the `<system>` shall `<response>` | When the user clicks "Send Magic Link", the system shall send an email within 30 seconds. |
| **Unwanted**（异常行为） | If `<condition>`, then the `<system>` shall `<response>` | If the magic link is expired, then the system shall show "Link expired". |
| **State-driven**（状态驱动） | While `<state>`, the `<system>` shall `<response>` | While the user is authenticated, the system shall show the dashboard. |
| **Optional**（可选特性） | Where `<feature>`, the `<system>` shall `<response>` | Where dark mode is enabled, the system shall use dark theme colors. |

**对比模糊 vs EARS**：

```
❌ "登录要安全"
✅ If the login attempt fails 5 times within 10 minutes,
   then the system shall lock the account for 30 minutes.

❌ "支持上传图片"
✅ When the user uploads a file, the system shall accept JPEG or PNG up to 10MB.
   If the file exceeds 10MB, then the system shall reject with "File too large".
```

---

## 六、好 Spec 的六个要素

（Augment Code 总结，Leave any open → AI 替你回答，且答案你不满意）

| # | 要素 | 说明 |
|---|---|---|
| 1 | **Outcomes** | 完成时长什么样？不是「做 auth flow」，而是「用户能 signup、收验证邮件、login 无错、session 跨刷新持久」 |
| 2 | **Scope Boundaries** | In Scope + **Out of Scope**（同样重要） |
| 3 | **Constraints** | 技术栈、API 限制、性能要求；配合 AGENTS.md |
| 4 | **Prior Decisions** | 已选定的 schema、库、模式——否则 AI 会自己选 |
| 5 | **Task Breakdown** | 拆成可独立执行的小任务，避免一次要太多 |
| 6 | **Verification Criteria** | 什么测试通过、哪些 edge case 覆盖——Verifier Agent 的依据 |

---

## 七、最佳实践

### 7.1 十二条准则

#### 1. Constitution First
在写第一个 Spec 之前，先 commit `AGENTS.md`。项目级规则不应重复写在每个 Spec 里。

#### 2. 阶段门禁，绝不跳步
```
Spec 未确认 → 禁止 Plan
Plan 未确认 → 禁止 Implement
Task 未验证 → 禁止下一个 Task
```

#### 3. Spec 负面空间（Out of Scope）
明确写「不做什么」和「做什么」同样重要：
```
Out of Scope: OAuth, 2FA, rate limiting (Phase 2)
```

#### 4. 保持 Spec 简短（1–3 页）
过大 Spec 导致 context 退化。大功能拆成多个 Spec（`001-auth`、`002-profile`）。

#### 5. Spec 是活文档
需求变了 → **先改 Spec，再改代码**。不允许 silent drift。

#### 6. 用 EARS 写验收标准
每条 acceptance criteria 都应是可测试的 EARS 语句。

#### 7. 逐 Task 实现 + commit
```
feat(auth): magic link endpoint, refs specs/001-user-auth
```

#### 8. Clarify before Code
让 AI 在写代码前列出歧义点：
```
/speckit.clarify — 列出 Spec 中所有模糊之处，向我提问
```

#### 9. 对抗性验证（Adversarial Agent Pattern）
- **Implementor Agent**：按 Spec 写代码
- **Verifier Agent**：按 Spec 检查输出，找问题
- Implementor 对自己的 output 过于乐观；独立 Verifier 信号更干净

#### 10. 测试 Ratchet
Prompt 中明确：
```
It is unacceptable to remove or edit tests to make them pass.
Fix the implementation, not the tests.
```

#### 11. 何时写 Spec，何时跳过

| 写 Spec | 跳过 Spec |
|---|---|
| 跨多个 Agent 会话 | 探索性实验 |
| 多服务 / 多仓库 | 一个 Prompt 能出可用结果 |
| 误解需求代价高 | 5 分钟内可 review 完 |
| 合规 / 审计 | 一次性原型 |
| 组件逻辑 / 端到端流程 | 机械性小改动 |

**触发器**：如果你会因为 AI 理解错需求而恼火 → 写 Spec；一个 follow-up Prompt 能修 → 直接 Prompt。

#### 12. 从 Vibe 升级时先 Spec 再 Code
Vibe 产物验证了想法？不要继续在 vibe 上加功能——**freeze → 写 Spec → 按 SDD 重建或加固**。

---

### 7.2 常见陷阱

| 陷阱 | 表现 | 应对 |
|---|---|---|
| **Over-specification** | Spec 像伪代码，约束了「怎么做」 | Spec 只写「做什么」，Plan 写「怎么做」 |
| **Spec Rot** | Spec 与代码不同步 | 测试 enforce 对齐；变更先改 Spec |
| **Spec as Bureaucracy** | 填表式 Spec，无实际 clarity | 最小化：只消除歧义的部分 |
| **Tooling Complexity** |  drowning in 生成的 plan/tasks | 从简单 Spec 开始，按需加工具 |
| **False Confidence** | 测试通过 = 软件正确 | Spec 本身也可能错——Spec 也需要 review |
| **跳步** | 直接从想法到代码 | 阶段门禁 |

---

## 八、工具与实现方式

### 8.1 主流 SDD 工具

| 工具 | 类型 | 工作流 | 特点 |
|---|---|---|---|
| **GitHub Spec Kit** | CLI + Slash Commands | `/specify` → `/plan` → `/tasks` → `/implement` | 开源、模型无关、最 portable |
| **AWS Kiro** | IDE | Requirements → Design → Tasks → Code | VS Code 集成，结构化需求捕获 |
| **Cursor Plan Mode** | IDE | Plan → 确认 → Agent 实现 | IDE-first 团队最自然 |
| **Claude Code + cc-sdd** | CLI + Skills | Spec skills 驱动 | 终端工作流，低 friction |
| **OpenSpec / BMAD** | 框架 | 多种 SDD 变体 | 社区方法论 |
| **Tessl** | Platform | Spec-as-Source | 规格即源码，审计 trail |

### 8.2 不用专用工具时的「轻量 SDD」

在 Cursor / Claude Code 中手动操作：

```
1. 创建 specs/001-feature/spec.md（手写或用 AI 生成）
2. 人工 review spec.md
3. 创建 plan.md（AI 生成 + 人工改）
4. 创建 tasks.md（AI 拆分）
5. Agent 模式：@spec.md @plan.md @tasks.md "Implement T1 only"
6. 测试 → commit → 下一个 Task
```

### 8.3 多 Agent 协作模式

```
Coordinator（读 Spec，分配 Task）
    ├── Implementor A（Task 1, 3, 5）
    ├── Implementor B（Task 2, 4, 6）  ← 可并行
    └── Verifier（按 Spec 检查所有输出）
```

**长运行 Agent**（跨会话）的状态文件：
- `feature-list.json` — 所有功能及 pass/fail 状态
- `progress.txt` — 每 session 的进展日志
- `init.sh` — 新 session 的环境 bootstrap 脚本

---

## 九、SDD vs TDD vs BDD vs Vibe Coding

| 维度 | TDD | BDD | SDD | Vibe Coding |
|---|---|---|---|---|
| **权威来源** | 单元测试 | Gherkin 场景 | 结构化 Spec | 对话历史 |
| **粒度** | 函数级 | 功能级 | 功能 → 架构 → Task | 无结构 |
| **AI 协作** | AI 写测试/实现 | AI 写场景/步骤 | AI 按 Spec 全流程 | AI 猜需求 |
| **防 drift** | 测试 enforce | 场景 enforce | Spec + 测试 + 阶段门禁 | 无 |
| **适用** | 实现验证 | 跨职能对齐 | AI 时代的端到端开发 | 快速原型 |
| **关系** | SDD 包含 TDD 作为 Validate 手段 | SDD 吸收 BDD 的 Given/When/Then | 超集 | 对立面 |

---

## 十、从 Vibe 到 SDD 的升级路径

当你用 Vibe Coding 验证了想法，准备「认真做」时：

```
Step 1: Freeze — 不再 vibe 加新功能
Step 2: 让 AI 从现有代码反向生成 Spec（"Document current behavior as spec.md"）
Step 3: 审查 Spec — 修正 AI 的理解偏差
Step 4: 写 Plan — 标注哪些要保留、哪些要重写
Step 5: 按 SDD 流程逐 Task 加固或重建
Step 6: 补测试 — 从 Spec 的 EARS criteria 生成
Step 7: 建立 CI — spec check + test + lint
```

---

## 十一、总结

SDD 的本质：**把规格从「写完就丢的文档」变成「约束 AI 和执行验证的可执行合同」**。

**核心工作流**：
```
Constitution → Specify → Plan → Tasks → Implement (per task) → Validate
     ↑                                                              ↓
     └──────────── Spec 变更 ← 验证失败 ←──────────────────────────┘
```

**三条铁律**：

1. **Spec 是 authority** — 代码不对修代码，Spec 不对修 Spec；但 Spec 也需要 human review
2. **阶段门禁** — Never skip from spec to code
3. **最小严格度** — 用能消除歧义的最小 Spec，不过度规格化

SDD 不是 Vibe Coding 的对立面，而是其**成熟形态**——保留 AI 的速度，补上结构、问责和可维护性。在 AI 编程时代，**会写 Spec 的开发者 > 只会 Prompt 的开发者**。
