# AGENTS.md

本项目（plane-det-2）基于飞机航迹（由多个点迹组成的序列）的特征，对飞机机型进行识别。这是一个时序/轨迹特征分类问题，不涉及图像或视觉模型。

## 启动流程

开始编码前：

1. **确认工作目录**：`pwd`
2. **完整阅读本文件**
3. **阅读项目文档（如存在）**：`docs/ARCHITECTURE.md`、`docs/PRODUCT.md`、README 等
4. **运行 `./init.ps1`** 验证环境是否正常
5. **阅读 `feature-list.json`** 查看当前功能状态
6. **查看最近提交**：`git log --oneline -5`

如果基线验证失败，先修复它，再添加新的功能范围。

## 工作规则

- **一次只做一个功能**：从 `feature-list.json` 中选择一个未完成的功能（当前列表为空，按用户要求不预先拆解，做了什么就记录什么）
- **必须验证**：不要在没有运行验证命令的情况下声称完成
- **更新记录**：会话结束前更新 `progress.md` 和 `feature-list.json`
- **保持范围**：不要修改与当前功能无关的文件
- **保持可启动状态**：下一次会话必须能够立即运行 `./init.ps1`

## 必需文件

- `feature-list.json` — 功能状态记录（事实来源，按实际完成情况追加，不预先规划）
- `progress.md` — 会话连续性记录
- `init.ps1` — 标准启动与验证脚本（PowerShell，适配当前 Windows 环境）
- `issues-log.md` — 问题记录，记录对话过程中遇到的坑和解决办法
- `architecture.md` — 项目架构说明，汇总各模块精简信息并指向模块详细说明文档
- `session-handoff.md` — 可选，用于较大的会话交接

## 完成的定义

一个功能只有在满足以下所有条件时才算完成：

- [ ] 目标行为已实现
- [ ] 已实际运行所需的验证（测试 / lint / 类型检查）
- [ ] 已在 `feature-list.json` 或 `progress.md` 中记录证据
- [ ] 仓库仍可从标准启动路径重新启动

## 会话结束时

结束会话前：

1. 更新 `progress.md` 记录当前状态
2. 更新 `feature-list.json` 记录新的功能状态
3. 记录任何未解决的风险或阻塞项
4. 在工作处于安全状态后，提交一次有描述性的 commit
5. 保持仓库整洁，使下一次会话可以立即运行 `./init.ps1`

## 验证命令

```powershell
# 完整验证（推荐）
powershell -ExecutionPolicy Bypass -File .\init.ps1
```

必须检查的内容：
- Python 解释器固定为 `E:\anaconda3\envs\imgforge\python.exe`（conda 环境 `imgforge`），不使用 `conda run` / `conda activate`
- 依赖安装：`pip install -r requirements.txt`
- 测试：如存在 `tests` 目录则运行 `pytest`

## 升级处理

遇到以下情况时：
- **架构决策**：参考项目架构文档（如存在），否则询问用户
- **需求不明确**：查看产品/需求文档（如存在），否则询问用户
- **重复的测试失败**：更新进度记录，提请人工复核
- **范围不清晰**：重新阅读 `feature-list.json` 中的完成定义
