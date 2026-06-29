# AWifesPhone EP1 简体中文火辣汉化包备份手册

本备份包由 Antigravity 自动生成，包含《A Wife's Phone EP1》100% 汉化与 R-18 润色成果。

---

## 汉化概况

| 项目 | 内容 |
|------|------|
| 汉化方式 | Ren'Py 官方 `translate zh_Hans` 对白块，原生语言包形式 |
| 翻译来源 | Gemini 2.5 Flash API 并发批量重译 + 手工润色 |
| 润色风格 | R-18 日式视觉小说火辣本土化，女性视角精修 |
| 质检 | 已完成双向性别用语质检（女角→男词 / 男角→女词） |
| 完成日期 | 2026-06-29 |

---

## 目录文件说明

| 文件/目录 | 作用 |
|-----------|------|
| `AWifesPhone.po` | 最完整、可追溯的英文-中文对齐翻译数据库 |
| `game/tl/zh_Hans/` | 全剧情对话与系统 UI 汉化文件（Ren'Py strings 格式） |
| `game/screens.rpy` | 修改了 Preferences 界面，含 English / 简体中文双语切换按钮 |
| `game/chinese_font.rpy` | 语言切换为中文时自动热替换字体为中文字体 |
| `game/gui/chinese.ttf` | 高精度中文字体（Arial Unicode），彻底消灭豆腐块乱码 |

---

## 性别用语质检修正记录（2026-06-29）

以下对白在汉化时被大模型误译为性别错位用语，已全部修正：

| 文件 | 角色 | 错误译文（节选） | 修正为 |
|------|------|----------------|--------|
| `new_main_phone_0_2_part_1.rpy` | nvlwife | 你满足不了我的鸡巴 | 你满足不了我的欲望 |
| `new_main_phone_0_2_part_2.rpy` | nvlhelsa | 我有多想把我的鸡巴插进你的下面 | 反正我最近也不能过去，所以没怎么多想（原文被 AI 完全篡改，已还原） |
| `new_main_wife_phone_0_2.rpy` | nvlwife | 看她玩弄我的鸡巴 | 看她玩弄我的假阳具 |
| `new_main_wife_phone_0_2.rpy` | nvlwife | 你的宝贝现在正忙着我的鸡巴呢 | 你的宝贝现在正忙着我的假阳具呢 |

> **注意**：`nvlsteph`、`nvljohn`（fem_withoutapp 线）、`nvlpaul`（paula 线）等角色在特定剧情线中使用跨性别用语，属于游戏本身的剧情设计，未做修改。

---

## 如何手动还原/移植到游戏本体

如果您重新下载了游戏，只需：

1. 将本备份包中 `game/` 文件夹下的所有内容，**直接拷贝覆盖**到游戏的 `game/` 根目录下
2. **删除** `game/` 目录下所有 `.rpyc` 缓存文件（可用命令 `find . -name "*.rpyc" -delete`）
3. 重新打开游戏，在 Preferences（设置）→ Language 中点击 **简体中文** 即可

---

## 关于语言切换

第一部需要在游戏内 **Preferences → Language → 简体中文** 手动切换一次。
切换后游戏会自动记住语言偏好，之后无需再次选择。
