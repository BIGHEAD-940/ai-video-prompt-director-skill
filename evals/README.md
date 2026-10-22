# 评测用例

`prompts.csv` 覆盖 Skill 应触发的请求和相邻但不应触发的请求。它用于手动检查 Skill 的适用边界和输出约束，不是模型效果基准。

## 手动评测流程

1. 记录 Codex 版本、模型、Skill 提交号和运行日期。
2. 逐条输入 CSV 中的 prompt，记录 Skill 是否被采用。
3. 按 `expected_checks` 和 `skills/ai-video-prompt-director/references/evaluation-cases.md` 检查输出。
4. 保存未编辑的输入、输出和评分；不要把未运行的案例写成结果。

仓库当前只包含用例，没有运行结果或质量分数。模型版本、系统设置和生成随机性都会影响观察结果。
