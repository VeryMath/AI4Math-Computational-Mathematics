# 科学计算复现 Skill

[English README](README.md)

`scientific-computing-reproduction` 是一套 **给 coding agent 使用的 Skill 层**，也是一个
computational math workflow package。它帮助 agent 做计算数学科研代码复现、运行环境部署、
失败诊断、参数调优、可视化和证据化报告。

这个仓库是 Skill-first、agent-native、conversation-first 的。它不是 CLI-first package，也不是全自动 pipeline：用户把 Skills 安装或加载到 coding agent 里，然后用自然语言交互；agent 读取 Skills、检查目标仓库、写紧凑 review 产物，并在关键操作前等待人工批准。脚本只是共享 Skill 层背后的可选辅助工具。

## 这个 Skill 做什么

这个独立 Skill 帮助 coding agent 复现和检查计算数学科研代码。当你有本地仓库、远程仓库、压缩包、
论文代码指针或算法实现，希望 agent 先检查源码、制定有边界的运行计划、部署或诊断环境、只执行获批步骤、
在证据支持时调参、生成图表并写 evidence-backed summary 时，可以直接使用它。

日志、指标、图表和 best programs 都是计算证据；这个 README 的目标是让新用户能单独安装和使用本 Skill。

## 你安装的是什么

本仓库真正交付给用户的是 `skills/` 下的共享 Skill 层。

Skill 是给 coding agent 阅读的工作流说明。每个 `SKILL.md` 会告诉 agent：什么时候使用这个工作流、要检查哪些证据、要写哪些产物、哪些风险需要人工审批，以及哪些脚本可以作为可选辅助工具调用。

默认入口是：

```text
skills/computational_math_reproduction_workflow_skill/SKILL.md
```

Skill 注册表是：

```text
skills/registry.yaml
```

注册表把默认工作流路由到领域分类、仓库复现、环境部署、MATLAB 配置、MATLAB 运行时规划、失败诊断、调参、可视化、人工 review 和报告生成等 specialist Skills。

用户提供的是：

- 自然语言目标；
- 可选的本地路径、远程仓库、压缩包或论文代码目标；
- `approve`、`revise`、`reject`、`skip` 这类 checkpoint 决策。

Agent 在有价值时产出：

- `outputs/{run_id}/` 下的紧凑 review 产物；
- 获批运行的命令日志；
- 有证据时生成的图表和调参总结；
- 对发现、限制和不确定性的简洁对话说明。

## 安装 / 加载

### 一句话安装

把下面这句话发给你的 coding agent：

```text
请帮我安装 `scientific-computing-reproduction` skill，链接是：https://github.com/VeryMath/AI4Math-Computational-Mathematics.git，分支：kn。请读取 `.agent.md`，安装其中声明的 Skill entrypoint，验证 `$scientific-computing-reproduction` 可用，并告诉我是否需要重启 agent。
```

如果你已经有这个 skill 仓库的本地文件夹，把链接换成本地路径即可。clone、link、配置、reload/restart 检查和验证都交给 coding agent 处理。

## 快速开始

当 coding agent 能看到这些 Skills 后，可以这样启动：

```text
Use computational_math_reproduction_workflow_skill.

Goal:
Inspect this computational math repository, classify the domain,
write plan.md, and wait for approval before executing anything.

Target:
<local path, repository URL, archive path, or paper-code pointer>

Output policy:
- route through skills/registry.yaml;
- keep durable artifacts under outputs/{run_id}/;
- use scripts only as optional helpers, not the workflow driver;
- ask before execution, source edits, dependency changes, long runs, tuning, or final conclusions.
```

如果要配置 MATLAB 访问，先让 agent 使用 `matlab_environment_setup_skill`。只有在 MATLAB、Octave 或 MATLAB MCP 能力被验证之后，再使用 `matlab_runtime_skill`。

## 如何交互使用

推荐使用 checkpoint 循环：

```text
科研代码目标 -> 检查 -> 计划 -> approve / revise / reject / skip
             -> 获批运行、修复、调参或报告
             -> 证据总结 -> 下一轮 checkpoint
```

`approve` 表示执行下一步，`revise` 表示先修改计划，`reject` 表示停止当前路线，
`skip` 表示跳过当前阶段。执行命令、源码修改、依赖变化、长时间任务、调参和最终结论前都应先问用户。

## Skill 地图

- `computational_math_reproduction_workflow_skill`：默认端到端 workflow 入口。
- `computational_math_domain_skill`：计算数学大领域路由器。
- `continuous_optimization_skill`：成熟 specialist Skill，覆盖 ADMM、PPA、proximal gradient、primal-dual methods 和 augmented Lagrangian methods。
- `matlab_environment_setup_skill`：agent-neutral 的 MATLAB、Octave 和 MATLAB MCP 配置与验证。
- `matlab_runtime_skill`：可选 MATLAB/Octave 运行时后端检查、规划、toolbox 提示和获批执行边界。
- `repo_reproduction_skill`：仓库分析、运行计划、获批执行和证据收集。
- `environment_deployment_skill`：依赖和运行环境部署规划。
- `failure_diagnosis_skill`：失败分类和修复计划。
- `algorithm_discovery_skill`：外部算法和实现发现。
- `auto_tuning_skill`：获批调参计划和有边界搜索。
- `visualization_skill`：收敛曲线和调参图表。
- `human_review_skill`：审批 checkpoint 和可选 approval logs。
- `report_generation_skill`：紧凑计划、总结和报告。

## 支持范围

Phase 1 聚焦连续优化科研代码，尤其是：

- ADMM；
- PPA；
- proximal gradient methods；
- primal-dual methods；
- augmented Lagrangian methods。

Python 项目是当前主要自动执行目标。MATLAB 仓库可以通过 MATLAB Skills 被检查和规划；只有在 MATLAB、Octave 或 MATLAB MCP 可用且获得批准后才运行。Julia、C++ 和 R 在 MVP 中会被检测和报告，但默认不自动运行。

其他计算数学方向先由 reference cards 路由，等需要时再拆成 specialist Skills：

- 数值线性代数；
- 微分方程；
- PDE/FEM；
- 随机模拟；
- 反问题。

## 输出契约

默认工作流只写紧凑的持久产物：

- 执行前写 `outputs/{run_id}/plan.md`；
- 只有需要源码、依赖、adapter、入口或数据变更时才写 `outputs/{run_id}/repair_plan.md`；
- 复现工作结束后写 `outputs/{run_id}/RUN_SUMMARY.md`；
- 只有提出调参时才写 `outputs/{run_id}/tuning/tuning_plan.md`；
- 只有调参被批准后才写 tuning results、tuning logs、tuning figures 和 `tuning/TUNING_SUMMARY.md`。

Legacy checkpoint 文件和 approval logs 仍然可以作为可选的持久 review 机制使用，但它们不是默认工作流驱动器。

## 示例和维护者材料

本仓库不是复现案例库。`example/` 目录只保留紧凑参考产物，帮助维护者和读者理解一次完整 Skill-first workflow 长什么样。

测试、fixtures 和 helper-script 开发属于维护者范围。用户通过 coding agent 使用 Skill 层时不需要它们。

维护者工作使用共享 Conda 环境：

```bash
conda run -n ai4math pytest
```

更多维护者细节见 `docs/environment.md`、`docs/interaction_protocol.md` 和 `docs/testing.md`。

新增或修改 Skill 时，需要同步更新对应的 `manifest.yaml`、`skills/registry.yaml` 和必要的 routing reference cards。平台入口保持薄壳，优先改共享 Skill 层。
