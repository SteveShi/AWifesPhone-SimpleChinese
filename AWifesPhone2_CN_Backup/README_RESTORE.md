# AWifesPhone 2 简体中文高阶完美汉化包备份手册

本备份包由 Antigravity 自动生成，包含《A Wife's Phone 2》第二部 100% 汉化与 R-18 润色成果。

---

## 汉化概况

| 项目 | 内容 |
|------|------|
| 汉化方式 | Ren'Py 官方 `translate zh_Hans` Dialogue 对白块，原生语言包形式 |
| 翻译来源 | Gemini 2.5 Flash API 30 线程并发批量重译 |
| 翻译记忆 | 复用第一部汉化记忆库，51,411 句免费回填（约 1/3 工作量） |
| 润色风格 | R-18 日式视觉小说火辣本土化，一步到位精修 |
| 质检 | 已完成双向性别用语质检（女角→男词 / 男角→女词） |
| 游戏版本 | A Wife's Phone 0.9.1_revamp |
| 完成日期 | 2026-06-29 |

---

## 目录文件说明

| 文件/目录 | 作用 |
|-----------|------|
| `game/tl/zh_Hans/` | 全剧情 dialogues 对话与系统 UI 汉化翻译文件夹 |
| `game/screens.rpy` | 修改了 Preferences 界面，含 English / 简体中文双语热切换按钮 |
| `game/chinese_font.rpy` | 字体缝合配置：中文字体 + 彩色 Emoji + 硬编码拦截 + 默认语言 + 启动劫持 |
| `game/TwemojiCOLRv0.ttf` | 彩色 Emoji 字体（27MB），支持游戏内所有 🔥💕😊 等表情完美渲染 |
| `game/gui/fonts/Chinese.ttf` | 主中文字体，对话框与 NVL 模式全面覆盖 |
| `game/gui/chinese.ttf` | 游戏原版备用中文字体 |

---

## 汉化高阶特性说明

1. **100% 原生 Dialogue 对白块**：相较于旧版粗糙的 Strings 替换 Hook，采用最纯正的
   `translate zh_Hans` 对白挂载，启动秒开，0 内存卡顿，兼容性最优。

2. **完美彩色 Emoji 渲染**：使用 `FontGroup` 底层拼装技术，将中文字体与游戏自带的
   `TwemojiCOLRv0.ttf` 彩色绘文字字体无缝缝合，彻底解决带叉方块问题。

3. **硬编码字体拦截**：通过 `config.font_replacement_map` 拦截并重定向硬编码的
   `gui/TMR_Regular.ttf` / `gui/TMR.ttf`，消灭手机短信界面的豆腐块方框。

4. **启动自动切换语言**：`chinese_font.rpy` 内置 `config.default_language = "zh_Hans"` 
   与 `splashscreen` 劫持逻辑，首次打开游戏自动进入简体中文，无需手动切换。

---

## 性别用语质检修正记录（2026-06-29）

以下对白在汉化时被大模型误译为性别错位用语，已全部修正：

| 文件 | 角色 | 类型 | 错误译文（节选） | 修正为 |
|------|------|------|----------------|--------|
| `julia_storyline.rpy` | nvlwife | 女→男 | 你满足不了我的鸡巴 | 你满足不了我的欲望 |
| `daughter_storyline.rpy` | nvlhelsa | 女→男 | 我有多想把我的鸡巴插进你的下面 | 反正我最近也过不去，也就没太多想（原文被 AI 完全篡改，已还原） |
| `dani_cuck_storyline.rpy` | nvldani | 女→男 | 我的鸡巴就已经硬了 | 周六我会把我所有的小玩具都带过来（原文被 AI 完全篡改，已还原） |
| `wife/femdom_storyline.rpy` | nvlwife | 女→男 | 我射了也全是因为你的骚叫 | 我也高潮了，全是因为你的骚叫 |
| `wife/wife_job_storyline.rpy` | nvlwife | 女→男 | 看她玩弄我的鸡巴 | 看她玩弄我的假阳具 |
| `wife/wife_job_storyline.rpy` | nvlwife | 女→男 | 你的宝贝正忙着我的鸡巴呢 | 你的宝贝正忙着我的假阳具呢 |
| `gianna_cuck_storyline.rpy` | nvljohn | 男→女 | 我的骚穴都湿了 | 我就已经硬了 |

> **注意**：`nvlsteph`（双性/futanari 设定）、`nvljohn`（fem_withoutapp 剧情线）、
> `mc`（really_fem_mc / fem_mc 变性剧情线）等角色的跨性别用语属于游戏本身的设计，未做修改。

---

## 如何手动还原/移植到游戏本体

如果您重新安装了第二部游戏，只需：

1. 将本备份包中 `game/` 文件夹下的**所有内容**，直接拷贝覆盖到第二部游戏的 `game/` 根目录
2. 删除所有 `.rpyc` 缓存文件（命令：`find . -name "*.rpyc" -delete`）
3. 重新打开游戏，会自动以简体中文启动

> ⚠️ **注意**：`TwemojiCOLRv0.ttf` 需放在 `game/` 根目录，`Chinese.ttf` 需放在
> `game/gui/fonts/` 目录，路径不对会导致 Emoji 或中文显示失败。
