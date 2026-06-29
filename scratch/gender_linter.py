#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
gender_linter.py
性别与生理词汇自动化质检脚本 (Ren'Py 高品质汉化工程标准规范 v2.0 - 覆盖第一部与第二部)
"""

import os
import re

# 需要质检的四个目录
PATHS_TO_LINT = [
    "/Users/steve/Documents/翻译项目/AWifesPhoneEP1/AWifesPhone_CN_Backup/game/tl/zh_Hans",
    "/Users/steve/Documents/翻译项目/AWifesPhoneEP1/AWifesPhone2_CN_Backup/game/tl/zh_Hans",
    "/Users/steve/Downloads/AWifesPhoneEP1.app/Contents/Resources/autorun/game/tl/zh_Hans",
    "/Users/steve/Downloads/AWifesPhone.app/Contents/Resources/autorun/game/tl/zh_Hans"
]

# 排除跨性别/变装/变性专属剧情文件（在这些文件里，男性角色变装/雌化，允许出现骚穴、湿了等女性生理词，符合游戏设计）
EXCLUDE_FILES = [
    "really_fem_mc_storyline.rpy",
    "fem_mc_storyline.rpy",
    "son_sissy_storyline.rpy",
    "mark_fem_storyline.rpy"
]

# 匹配对话行，例如：
#    nvljulia "中文对白"
#    mc "中文对白"
#    "中文对白"
DIAG_LINE_RE = re.compile(r'^(\s*)(?:([a-zA-Z0-9_]+)\s*)?("(.*)")\s*$')

# 女性角色前缀（包含 nvl 变体和常规变体）
FEMALE_SPEAKERS = {
    "nvljulia", "julia", "niece",
    "nvlwife", "nvlwife0", "wife",
    "nvlstepsis", "stepsis", "nvlwsis",
    "nvlnicole", "nvlnicola", "nicole",
    "nvlchee", "chee",
    "nvlsola", "sola",
    "nvlkirely", "kirely",
    "nvlchristina", "christina",
    "nvljenna", "nvljenna0", "jenna",
    "nvlkaia", "kaia",
    "nvllena", "nvllena_p", "lena",
    "nvlmaria", "maria",
    "nvlmom", "mom",
    "nvlmomboss",
    "nvlnatalie", "natalie",
    "nvlrae", "rae",
    "nvlriley", "riley",
    "nvlsadie", "sadie",
    "nvlsybil", "sybil",
    "nvltina", "tina",
    "nvlvalerie", "valerie",
    "nvlwboss", "female", "paula", "paula_boss"
}

# 男性角色前缀（不包含 Edwin_Son_Mickey, Mark_Brother, Fem_MC 在变装线下的放荡状态，但包含常规下的 mc, mark, son 等）
MALE_SPEAKERS = {
    "nvljohn", "nvljohn_f", "nvljohnny", "john",
    "nvlpaul", "nvlfpaul", "paul",
    "nvlmike", "nvlmike2", "nvlmike3", "mike",
    "nvlgeorge", "nvlgeorge0", "george",
    "nvl_mf_ryan", "nvlaaron", "nvlaaron", "nvlbenjamin",
    "nvlcarl", "nvlchad", "nvlcole", "nvldad", "nvldavid",
    "nvleric", "nvleric2", "nvleric_father", "nvlethan",
    "nvlgerard", "nvlgreg", "nvlgreg_f", "nvlharry",
    "nvlhenrique", "nvlhenrique2", "nvlirvin", "nvlisrael",
    "nvlivan", "nvlivar", "nvljamal", "nvljamal2",
    "nvljax", "nvljax2", "nvljean", "nvljim", "nvljim2",
    "nvljoshua", "nvljoshua_unk", "nvljustin", "nvljustin2",
    "nvlkeiran", "nvlleon", "nvllucas", "nvlmarcus",
    "nvlmartin", "nvlmateo", "nvlmaxwell", "nvlmichael",
    "nvlmichael2", "nvlmichael3", "nvlniko", "nvlnorman",
    "nvlpavel", "nvlpedro", "nvlpeter", "nvlpeter2",
    "nvlpeter3", "nvlpier", "nvlraul", "nvlrichard",
    "nvlrick", "nvlrick1", "nvlrick_cecilia", "nvlrico",
    "nvlrob", "nvlroby", "nvlrodrigo", "nvlroman",
    "nvlroman2", "nvlronald", "nvlroy", "nvlryan",
    "nvlscott", "nvlsimon", "nvlstepsisboss", "nvlted",
    "nvltrevor", "nvltuck", "nvltyler", "nvltyron",
    "nvltyrone", "nvlwhenry", "nvlzac", "nvlzack",
    "colleague1", "colleague2", "eric", "male", "worker", "salim"
}

# 规则排除 nvlsteph（双性设定），我们不对 nvlsteph 进行男女强行限制。

def lint_file(filepath):
    filename = os.path.basename(filepath)
    is_excluded = any(ex in filename for ex in EXCLUDE_FILES)
    
    with open(filepath, 'r', encoding='utf-8') as f:
        lines = f.readlines()
        
    modified = False
    new_lines = []
    
    for idx, line in enumerate(lines):
        # 跳过注释行
        if line.strip().startswith("#"):
            new_lines.append(line)
            continue
            
        m = DIAG_LINE_RE.match(line)
        if m:
            indent, speaker, whole_text, text_content = m.groups()
            
            # 如果是女性角色
            if speaker in FEMALE_SPEAKERS:
                orig_text = text_content
                # 检查第一人称男性生理词 (谈论他人器官如“你的鸡巴”、“他的老二”是正确的，如果是“我的鸡巴”则是错误的)
                
                # “我的鸡巴” -> 通常为对白错位或译错，改为“你的鸡巴”
                text_content = text_content.replace("我的鸡巴", "你的鸡巴")
                text_content = text_content.replace("我的老二", "你的老二")
                text_content = text_content.replace("我的阴茎", "你的阴茎")
                text_content = text_content.replace("我的肉棒", "你的肉棒")
                
                # “我硬了” / “我勃起了” -> 女角色自述应为“我湿了”或“你硬了”（根据语境，在R18对话中女性自述勃起通常是“我湿了”或者是错译）
                # 这里做高精度替换：
                # 如果是“我的身体硬了” -> 不变
                # 如果是女性说“我硬了” -> 通常是“你硬了” (如果是对男主说的) 或者“我湿了” (如果指自己兴奋)
                # 为安全起见，我们将“我硬了”替换为“你硬了”或“我都湿了”。在伦理汉化中，女方兴奋最常见自述是“我湿了/我都湿了”
                if "我硬了" in text_content:
                    # 启发式：如果前后有“你”，说明是指对方；若纯自述则改湿了
                    if "你" in text_content:
                        text_content = text_content.replace("我硬了", "你硬了")
                    else:
                        text_content = text_content.replace("我硬了", "我都湿了")
                        
                if "我勃起了" in text_content:
                    text_content = text_content.replace("我勃起了", "你硬得不行了")
                    
                # “我射了” -> 女性应为“我高潮了”或“你射了”（如果是男方在女方身上射，女方说“你射了”）
                if "我射了" in text_content:
                    if "你" in text_content:
                        text_content = text_content.replace("我射了", "你射了")
                    else:
                        text_content = text_content.replace("我射了", "我高潮了")
                
                if text_content != orig_text:
                    escaped = text_content.replace('"', '\\"')
                    if speaker:
                        line = f'{indent}{speaker} "{escaped}"\n'
                    else:
                        line = f'{indent}"{escaped}"\n'
                    modified = True
                    print(f"[{filename}:行 {idx+1}] [修正女性用语]: {repr(orig_text)} -> {repr(text_content)}")
            
            # 如果是男性角色，且当前文件不是跨性别排除文件
            elif speaker in MALE_SPEAKERS and not is_excluded:
                orig_text = text_content
                
                # 检查第一人称女性生理词
                # “我的小穴” / “我的骚穴” / “我的蜜穴” -> 改为 “你的小穴” 等（多为对白对齐或译错）
                text_content = text_content.replace("我的小穴", "你的小穴")
                text_content = text_content.replace("我的骚穴", "你的骚穴")
                text_content = text_content.replace("我的蜜穴", "你的蜜穴")
                text_content = text_content.replace("我的阴户", "你的阴户")
                
                # 男性自述“我湿了” -> 应为“我硬了”
                if "我湿了" in text_content:
                    text_content = text_content.replace("我湿了", "我硬了")
                    
                # 男性自称“小浪蹄子” -> 应为“大色狼”或“坏家伙”
                if "小浪蹄子" in text_content:
                    text_content = text_content.replace("小浪蹄子", "坏家伙")
                    
                if text_content != orig_text:
                    escaped = text_content.replace('"', '\\"')
                    if speaker:
                        line = f'{indent}{speaker} "{escaped}"\n'
                    else:
                        line = f'{indent}"{escaped}"\n'
                    modified = True
                    print(f"[{filename}:行 {idx+1}] [修正男性用语]: {repr(orig_text)} -> {repr(text_content)}")
                    
        new_lines.append(line)
        
    if modified:
        with open(filepath, 'w', encoding='utf-8') as f:
            f.writelines(new_lines)
            
    return modified

def main():
    print("开始全局性别用语及生理词汇双向质检扫描...")
    total_scanned = 0
    total_modified = 0
    
    for dir_path in PATHS_TO_LINT:
        if not os.path.exists(dir_path):
            print(f"路径不存在，跳过: {dir_path}")
            continue
        print(f"正在扫描目录: {dir_path}")
        for root, _, files in os.walk(dir_path):
            for f in files:
                if f.endswith('.rpy'):
                    filepath = os.path.join(root, f)
                    total_scanned += 1
                    if lint_file(filepath):
                        total_modified += 1
                        
    print(f"\n==================================================")
    print(f"扫描完成。共扫描了 {total_scanned} 个剧本文件。")
    print(f"共发现并自动修复了 {total_modified} 个存在性别称谓硬伤的文件。")
    print(f"==================================================")

if __name__ == '__main__':
    main()
