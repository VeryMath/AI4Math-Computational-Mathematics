---
name: qr-decomposition
description: "Use when you need QR decomposition, orthogonal triangular factorization, least squares, orthogonal bases, solving over/under-determined systems, Gram-Schmidt, Householder reflections, or stable Python implementations."
---
# QR Decomposition Skill

## 适用场景
- 对任意矩阵做 $A = Q R$ 分解，$Q$ 正交/酉，$R$ 上三角
- 求解最小二乘问题（过定系统）、欠定系统
- 计算正交基、投影、Gram-Schmidt 正交化
- 处理列满秩的长方形矩阵
- QR 迭代用于特征值计算、Arnoldi 算法

## Quick Start
- [ ] 确认矩阵形状；QR 适用于方阵和长方形矩阵
- [ ] 判断任务是完整 QR、缩减 QR、求解还是求基
- [ ] 选择 `numpy.linalg.qr` 或 `scipy.linalg.qr`
- [ ] 区分 economic/ reduced 与 full/complete 模式
- [ ] 验证 $A \approx Q R$、正交性和残差
- [ ] 若矩阵秩亏，说明列线性相关性

## Selection Rules

- 适用场景：任意矩阵（方阵或长方形），尤其适合列满秩的长方形矩阵最小二乘。
- 优先级：当问题涉及最小二乘、正交化、求解线性系统时，QR 是推荐的首选（比 LU 对非方阵更自然）。
- 不适用或次选：矩阵明显秩亏或病态严重（推荐 SVD）；矩阵对称正定（推荐 Cholesky）。
- 当 QR 过程中发现列线性相关时，应主动说明并提供 SVD 或带列选主元的 QR 建议。

## 执行流程

### 路径 A：用户已给矩阵和具体目标
1. 确认矩阵形状（$m \times n$）和目标类型（分解、求解、正交化）。
2. 计算经济型 $Q R$ 或完整型 $Q R$。
3. 若求解线性系统，做 $R x = Q^T b$（上三角回代）。
4. 报告重构误差、残差、列相关性或正交性检验。
5. 若秩亏，提供秩信息并说明最小范数解方案。

### 路径 B：用户只说"做 QR"但没有明确目标
1. 先澄清是完整分解、求解最小二乘、还是求正交基。
2. 若是教学场景，可以顺带解释 Householder 反射与 Gram-Schmidt 的区别。
3. 若矩阵非列满秩，主动提示并提供带列选主元的 QR 或 SVD 方案。

## 输出模板
```markdown
### 问题重述
...

### 矩阵检查
- shape: ...
- 是否方阵: ...
- 是否列满秩: ...

### 分解结果
- Q: ...
- R: ...

### 验证
- reconstruction error ||A - QR||: ...
- 正交性 ||Q^T Q - I||: ...

### 求解结果（如适用）
- x: ...
- residual ||Ax - b||: ...

### 结果解释
...
```

## 歧义与澄清
- 需要 full QR 还是 reduced/economic QR？
- 只需要 $Q$ 或只需要 $R$，还是两者都要？
- 是否需要带列选主元的 QR（rank-revealing）？
- 是求解最小二乘，还是求正交基？
- 若矩阵秩亏，是否需要输出秩信息或最小范数解？
- 用户常混淆 QR 与 SVD；明确说明 QR 适合列满秩情况，SVD 通用。

## 范围与边界

- 本 skill 适用于任意形状矩阵，但对秩亏情况建议补充说明或切换到 SVD。
- QR 分解本身不直接适用于奇异/秩亏矩阵的可靠求解，但可作为中间步骤。
- 正交化、投影、最小二乘是 QR 的典型应用场景。

## Python 技术细节

- 生产场景优先使用 `numpy.linalg.qr` 或 `scipy.linalg.qr`
- `numpy.linalg.qr(A, mode='reduced')` 返回经济型 $Q R$（$Q$ 为 $m \times k$，$R$ 为 $k \times n$，$k = \min(m, n)$）
- `mode='complete'` 返回完整型 $Q$（$m \times m$ 方阵）
- 矩阵秩亏时，`scipy.linalg.qr` 可选 `pivoting=True` 做带列选主元的 QR
- Householder 反射是数值稳定的默认实现，Gram-Schmidt 用于教学
- 独立脚本见 [scripts/solve_qr.py](./scripts/solve_qr.py)

## 示例

需要示例时请阅读 [references/examples.md](./references/examples.md)。

## 病态处理工作流

- 触发条件：QR 分解过程中发现列线性相关、条件数过大、或残差异常。
- 补救动作（按序）：
  1. 启用带列选主元的 QR（`pivoting=True`）并重试；
  2. 若仍不稳健，尝试矩阵均衡化（row/col scaling）；
  3. 若上述仍失败，回退到 SVD 并说明原因；
  4. 在每一步中生成 `report`（包含 rank_estimate、tried、final_method、residual_norm 等）。