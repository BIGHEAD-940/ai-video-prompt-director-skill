# AI Video Prompt Director

[简体中文](#简体中文) | [English](#english)

## 简体中文

一个面向 Codex 的中文优先 AI 视频导演 Skill，帮助把创作意图整理为可执行的镜头计划和模型提示词，并检查表演、摄影机、连续性、声音与画面文字。

本项目由社区维护，与 OpenAI、抖音及来源作者均无隶属关系，也不保证特定模型一定按提示词生成。

### 能力范围

- 提取用户确认的剧情、对白、参考素材、模型与交付约束。
- 先明确镜头目的，再写可观察的表演和动作。
- 用路径、方向、速度和落点说明摄影机运动。
- 检查空间、视线、道具、声音与镜头衔接。
- 按目标模型当前官方文档适配语法；未知时保留待适配项。
- 复审提示词，避免静默改动或增加用户未提供的信息。

### 安装与使用

Codex 支持项目级和用户级 Skill。将 `skills/ai-video-prompt-director` 复制到：

- 项目级：`.codex/skills/ai-video-prompt-director`
- 用户级：`~/.codex/skills/ai-video-prompt-director`

之后要求 Codex 编写、整理或审阅 AI 视频镜头提示词。详见 [OpenAI Codex 技能评测指南](https://developers.openai.com/blog/eval-skills)。

本项目不调用生成接口，也不要求 API 密钥。是否提交提示词给视频模型由使用者决定。

### 开发检查

需要 Python 3.10+，无第三方依赖。

```powershell
python -m unittest discover -s tests -v
python scripts/validate_repo.py .
```

`evals/prompts.csv` 提供触发范围和行为检查用例。目前没有伪造模型运行结果；要比较版本，请手动在 Codex 中运行用例并记录模型、版本、Skill 提交号和评分。

### 许可

Markdown 文档、方法、模板和示例按 CC BY 4.0 发布，见 [LICENSE](LICENSE)。代码按 MIT 发布，见 [LICENSE-CODE](LICENSE-CODE)。第三方来源归属见 [SOURCES.md](SOURCES.md)。

## English

A Chinese-first AI video directing skill for Codex. It turns creative intent into clear shot plans and prompts, then reviews visible performance, camera movement, continuity, sound, and on-screen text.

This is an independent community project. It is not affiliated with OpenAI, Douyin, or the credited authors. Install the `skills/ai-video-prompt-director` directory under a project-level `.codex/skills/` or user-level `~/.codex/skills/` directory. The skill does not call generation APIs or require API credentials.
