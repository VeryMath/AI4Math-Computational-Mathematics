# 不变量计算 Skill

English guide: [README.md](README.md)

`invariant-computation` 帮助 coding agent 计算、路由和验证代数、拓扑、几何、TDA 以及可认证数值不变量。

## 适合什么任务

当任务涉及这些对象或目标时使用：

- homology、cohomology、Betti numbers、torsion、Euler characteristic 或 persistent homology；
- Alexander、Jones、HOMFLY-PT、signature、determinant、linking number 等 knot 或 manifold invariants；
- group homology、Hilbert series、Betti table、primary decomposition、dimension 或 degree；
- 把自然语言、LaTeX、代码、三角剖分、复形、filtration、群表示、理想、结图或数据整理成可审查的计算表示。

## 会产出什么

Agent 应产出 representation checkpoints、method/backend routes、command drafts、logs、invariant summaries、validation reports，以及关于“该计算不能证明什么”的明确 caveats。

## 安装

把下面这句话发给你的 coding agent：

```text
请帮我安装 `invariant-computation` skill，链接是：https://github.com/VeryMath/AI4Math-Computational-Mathematics.git，分支：codex/ai4math-invariant-computing-skill。请读取 `.agent.md`，安装其中声明的 Skill entrypoint，验证 `$invariant-computation` 可用，并告诉我是否需要重启 agent。
```

如果你已经有这个 skill 仓库的本地文件夹，把链接换成本地路径即可。clone、link、配置、reload/restart 检查和验证都交给 coding agent 处理。

## 快速开始

```text
Use this repository's invariant-computation workflow.

Read:
- AGENTS.md
- SKILL.md
- skills/invariant-computation/SKILL.md

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
  invariant-computation/
    SKILL.md
    agents/openai.yaml
    manifest.yaml
    references/
tests/
```

## 维护检查

运行：

```bash
python <path-to-skill-creator>/scripts/quick_validate.py skills/invariant-computation
python3 -m unittest discover -s tests -v
```

然后检查 adapter 文件是否都指向共享 Skill layer，且没有新增本地绝对路径或私有 token。

## 许可证

见 [LICENSE](LICENSE)。
