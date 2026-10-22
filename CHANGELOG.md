# Changelog / 更新日志

## Unreleased — 2026-10-22

### Changed / 调整

- Map all thirteen reproduction Skills' existing underscore names to their public `SKILL.md` names through an explicit `skill_name` field. Existing Python directory and import paths remain usable.
- 为计算复现包的 13 个 Skill 明确名称映射：下划线名称和公开连字符名称均可查询，保留现有 Python 目录及导入路径。
- Add direct Skill selection and dependency queries with `python3 -m skills.registry`. MATLAB queries include the external `matlab-runner`, its `0.1.8-verymath-review` version, and its source.
- 名称查询同时展示内部依赖，以及 MATLAB 执行所需的外部 Runner、版本和来源。版本要求不表示该 Runner 已正式发布。

### Validation / 验证

- All thirteen name mappings, paths, and dependency references passed local checks. Seven existing invariant-computation package checks passed.
- 13 组名称及路径检查通过，现有 invariant-computation 包检查 7 项通过。旧 JSON Schema 检查因缺少其依赖未通过运行，本次没有新增该依赖。

### Release status / 发布状态

- This update covers Skill names, dependency queries, and their documentation. It does not add a CI workflow or claim a new scientific reproduction or MATLAB execution result.
- 本次更新包含名称映射、依赖查询及相关说明，不包含新增 CI 工作流，也不声明完成了新的科学项目复现或 MATLAB 执行验收。
