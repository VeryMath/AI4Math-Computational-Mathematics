# AI4Math 计算数学复现 Skills

一个面向 coding agent 的 **Skill-first workflow package（工作流包）**，用于计算数学科研代码复现、运行时部署、自动调参、可视化和报告生成。

## 这是什么

AI4Math Reproduction Skills 为 coding agent 提供一套可复用的计算数学科研代码工作流层。Agent 读取 Skills，检查目标仓库或本地路径，判断计算数学领域，写出紧凑运行计划，等待人工确认，只执行获批步骤，诊断失败，提出调参方案，在有价值时生成图表，并写出有证据支撑的总结。

本仓库不是 CLI-first package，不是全自动 pipeline，不是 benchmark platform，也不是复现案例库。正常使用方式是和 coding agent 对话。Scripts 只是可选辅助工具，**不是工作流驱动器**。

## 给谁用

这套 package 面向 Codex、Claude Code、Gemini、OpenCode 等 agentic coding 环境。它仍然是 Codex-native 的参考 operator profile，但真正对外共享的产品是 `skills/` 下的 Skill 层，而不是某个平台壳。

人类用户仍然是 checkpoint 的决策者。Agent 可以检查、推理、规划和运行获批命令，但关键执行、源码修改、依赖变更、长时间实验、调参和最终结论都需要人工 review。

## 快速开始

根据你的 coding agent 选择入口：

- Codex：阅读 `.codex/INSTALL.md`。
- Claude Code：阅读 `CLAUDE.md`。
- Gemini：阅读 `GEMINI.md`。
- OpenCode：阅读 `.opencode/INSTALL.md`。

然后用默认 Skill 启动端到端任务：

```text
Use computational_math_reproduction_workflow_skill.

Goal:
Inspect this computational math repository, classify the domain,
write plan.md, and wait for approval before executing anything.

Output policy:
- route through skills/registry.yaml;
- keep durable artifacts under outputs/{run_id}/;
- use scripts only as optional helpers, not the workflow driver;
- ask before execution, source edits, dependency changes, or tuning.
```

## 默认工作流

默认入口是 `skills/computational_math_reproduction_workflow_skill/SKILL.md`。

高层流程是：

1. 理解用户目标和目标源码。
2. 使用 `skills/registry.yaml` 路由到领域、运行时、环境、诊断、调参、可视化、review 和报告 Skills。
3. 在 `outputs/{run_id}/` 下写紧凑的 `plan.md`。
4. 请求人类 approve、revise、reject 或 skip 下一步关键操作。
5. 只执行获批步骤，并保存有边界的命令日志。
6. 只在有证据价值时写 `repair_plan.md`、`RUN_SUMMARY.md`、调参产物或图表。

## Skill 架构

每个 Skill 仍然以 `SKILL.md` 为主入口。配套的 `manifest.yaml` 和 `skills/registry.yaml` 让 agent 和维护者更容易检查 Skill 层：它们声明阶段、依赖、预期产物、风险等级和审批边界。

- `computational_math_reproduction_workflow_skill`：默认 workflow 入口。
- `computational_math_domain_skill`：计算数学大领域路由器。
- `continuous_optimization_skill`：成熟 specialist Skill，覆盖 ADMM、PPA、proximal、primal-dual 和 augmented Lagrangian 方法。
- `matlab_environment_setup_skill`：面向 Codex、Claude Code、Gemini、OpenCode 和 generic coding agent 的 MATLAB、Octave、MATLAB MCP 配置与验证。
- `matlab_runtime_skill`：可选 MATLAB/Octave 运行时后端检查、规划、toolbox 提示和获批执行边界。
- `repo_reproduction_skill`：仓库分析、运行计划、执行和证据收集。
- `environment_deployment_skill`：依赖和运行环境部署规划。
- `failure_diagnosis_skill`：失败分类和修复计划。
- `algorithm_discovery_skill`：外部算法和实现搜索。
- `auto_tuning_skill`：调参计划和有边界的搜索。
- `visualization_skill`：收敛曲线和调参图表。
- `human_review_skill`：审批 checkpoint 和可选日志。
- `report_generation_skill`：紧凑计划、总结和报告。

## 支持范围

连续优化是第一个成熟领域模块，尤其是 ADMM、proximal methods、primal-dual methods、PPA 和 augmented Lagrangian workflows。

其他计算数学方向先由 `computational_math_domain_skill` 的 reference cards 路由，等需要独立工作流时再拆成 specialist Skills：

- 数值线性代数；
- 微分方程；
- PDE/FEM；
- 随机模拟；
- 反问题。

Python 是当前主要自动执行目标。MATLAB 配置由 `matlab_environment_setup_skill` 以 agent-neutral 的方式处理，覆盖 Codex、Claude Code、Gemini、OpenCode 和 generic coding agent。MATLAB 运行时使用由 `matlab_runtime_skill` 处理：agent 可以检查 `.m`/`.mlx`/`.mat` 产物，推断入口和 toolbox 线索，检测本地 `matlab` 或 `octave` 可执行文件，并生成获批后使用的 `matlab -batch` 或 `octave --eval` 运行计划。MATLAB 不是 workflow controller。Julia、C++ 和 R 可以被检测和报告，等需要更深支持时再新增 runtime Skills。

## 平台入口

薄平台入口帮助不同 coding agent 加载同一套工作流，而不是复制工作流：

- `.codex/INSTALL.md`：Codex 本地 Skill 安装说明。
- `.opencode/INSTALL.md`：OpenCode 加载方式和插件壳说明。
- `CLAUDE.md`：Claude Code 仓库级说明。
- `GEMINI.md`：Gemini 入口，包含默认 workflow Skill 和 registry。

所有入口都指回 `skills/registry.yaml` 和 `computational_math_reproduction_workflow_skill`。平台文件应保持短小，不应变成另一套 workflow 定义。

## 案例

本仓库不是复现案例库，但 `example/` 保留了一些紧凑参考产物，用来展示一次完整 Skill-first workflow 长什么样。

- `example/boyd_admm_lasso_20260513/`：Stanford Boyd ADMM Lasso 的 MATLAB 复现案例，包含运行计划审批、`grabcode` 只打开未保存 buffer 的修复、收敛可视化，以及获批后的 `rho` / `alpha` 调参。基线复现对齐公开示例的 15 次迭代；调参后 `rho = 1.0`、`alpha = 1.2` 在保持目标函数接近的前提下把迭代数降到 13。
- `example/admm_bhushan23_20260511/`：基于当前 `ai4math` Python 环境，对 `bhushan23/ADMM` 做的最小 ADMM Lasso objective 复现。

## 输出产物

紧凑默认工作流把产物写到 `outputs/{run_id}/`：

- 执行前写 `plan.md`；
- 只有需要源码或依赖修改时才写 `repair_plan.md`；
- 结束时写 `RUN_SUMMARY.md`；
- 只有提出调参时才写 `tuning/tuning_plan.md`；
- 只有调参被批准后才写 `tuning/tuning_results.csv`、`tuning/best_parameters.json`、`tuning/tuning.log`、`tuning/tuning_figures/` 和 `tuning/TUNING_SUMMARY.md`。

`outputs/{run_id}/checkpoints/` 下的 checkpoint 文件和 `outputs/{run_id}/approvals/` 下的 approval log 仍可作为可选的持久 review 机制使用。

## 环境

使用共享 Conda 环境 `ai4math`。

```bash
conda create -y -n ai4math python=3.13 pip
conda run -n ai4math python -m pip install -e ".[dev]"
```

更多说明见 `docs/environment.md`。

## 维护者说明

运行测试：

```bash
conda run -n ai4math pytest
```

新增 Skill 时，需要同步更新对应的 `manifest.yaml`、`skills/registry.yaml` 和必要的 routing reference cards。平台入口保持薄壳，优先改共享 Skill 层。
