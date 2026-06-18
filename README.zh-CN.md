# AI4Math 不变量计算 Skill

English guide: [README.md](README.md)

`invariant-computation-skill` 是面向 coding agent 的 AI4Math Skill，用来计算、路由和验证拓扑、几何、代数不变量。

## AI4Math 角色

这个 Skill 是 AI4Math 体系里的不变量计算层。当研究问题需要代数、拓扑、几何或可认证数值证据，
再进入证明、猜想修正、优化或形式化之前，优先使用它。

## 交接

上游可能来自 `discover-math-problems`、`paper-to-skill`、Lean 形式化尝试或科学计算复现运行。
交接时应包含对象表示、系数/约定选择、方法路线、验证检查，以及该不变量不能证明什么。完成后把
validated summaries 作为证据交回猜想生成、定理证明或形式化 workflow，而不是把计算结果当成最终证明。

## 这是什么

当任务涉及下列目标时使用这个 Skill：

- 计算同调、上同调、Betti 数、torsion、Euler characteristic、持久同调、结或流形不变量、Alexander polynomial、Jones polynomial、HOMFLY-PT polynomial、signature、determinant、linking number、群同调、Hilbert series、Betti table、primary decomposition、dimension、degree 等不变量；
- 把自然语言、LaTeX、代码、三角剖分、复形、filtration、群表示、理想、结图或数据整理成可审查的计算表示；
- 在精确组合方法、符号代数方法、TDA、低维拓扑工具和可认证数值方法之间选择路线。

如果任务只是普通优化、论文筛选，或者没有不变量计算目标的形式化证明，不要使用这个 Skill。

## 安装 / 加载

从当前 checkout 使用时，让 coding agent 读取：

```text
AGENTS.md
SKILL.md
skills/invariant-computation-skill/SKILL.md
```

如果 agent 支持本地 Skill discovery，可以链接 concrete Skill 目录：

```bash
ln -s "$PWD/skills/invariant-computation-skill" ~/.codex/skills/invariant-computation-skill
```

如果目标 agent 需要重启或 reload，链接后再执行对应操作。

平台说明：

| Agent | 加载方式 |
| --- | --- |
| Codex | 读取 `.codex/INSTALL.md` |
| Claude Code | 读取 `CLAUDE.md` |
| Gemini | 读取 `GEMINI.md` |
| OpenCode | 读取 `.opencode/INSTALL.md` |

## 快速开始

```text
Use this repository's invariant-computation workflow.

Read:
- AGENTS.md
- SKILL.md
- skills/invariant-computation-skill/SKILL.md

Goal:
<你要计算的数学对象和不变量>

Target:
<本地路径、公式、三角剖分、filtration、群表示、理想、结图、数据或论文片段>

Constraints:
- inspect first;
- build a computation checkpoint before execution;
- ask before dependency changes, long runs, source edits, API calls, or final claims.
```

## 如何交互使用

正常使用方式是 checkpoint loop：

```text
数学对象和目标不变量
  -> 表示形式 checkpoint
  -> 方法与后端路线
  -> approve / revise / reject / skip
  -> 批准后的计算或命令草案
  -> 验证与证据报告
```

使用 `approve` 执行下一步，`revise` 修改路线，`reject` 停止当前路径，`skip` 跳过当前阶段，`stop` 结束会话并总结状态。

## 示例会话

```text
User:
Use this Skill to compute the homology of this simplicial complex.
Do not install packages yet. First inspect and propose the route.

Agent:
I will identify the object representation, coefficient ring, and candidate
backends, then write a computation checkpoint before running anything.

User:
approve the read-only route check.

Agent:
[reports closure checks, candidate tools, expected outputs, and next approval]
```

## 工作流与输出

需要保存证据时，优先使用：

```text
outputs/<run_id>/
├── input_summary.md
├── representation_checkpoint.md
├── route_plan.md
├── commands/
├── logs/
├── results/invariant_summary.json
├── validation_report.md
└── RUN_SUMMARY.md
```

只创建当前任务真正需要的文件。

## 安全与审查规则

- 安装数学软件包或修改环境前先询问。
- 长时间计算、昂贵枚举、源码修改前先询问。
- 记录系数环、定向、分次约定、变量顺序、filtration 方向和软件版本。
- 有限组合输入和符号输入优先使用精确方法。
- 数值几何结论优先使用可认证或区间方法。
- 除非有定理支持，不要声称不变量可以分类对象。

## 仓库结构

```text
AGENTS.md
SKILL.md
skills/
  invariant-computation-skill/
    SKILL.md
    agents/openai.yaml
    manifest.yaml
    references/
tests/
```

## 维护检查

运行：

```bash
python <path-to-skill-creator>/scripts/quick_validate.py skills/invariant-computation-skill
python3 -m unittest discover -s tests -v
```

然后检查 adapter 文件是否都指向共享 Skill layer，且没有新增本地绝对路径或私有 token。

## 许可证

见 [LICENSE](LICENSE)。
