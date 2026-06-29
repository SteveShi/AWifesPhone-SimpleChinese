#!/usr/bin/env python3
import os

# ==================== 配置 ====================
FILES_TO_FIX = {
    # 第一部
    "map_events_1": {
        "path": "/Users/steve/Documents/翻译项目/AWifesPhoneEP1/AWifesPhone_CN_Backup/game/tl/zh_Hans/map_events_1.rpy",
        "line_idx": 552, # 0-indexed 的 552 就是第 553 行
        "correct_content": '    "{color=#000}嗯……这代表 \\"是\\" 是吗？嗯..."\n'
    },
    "part_2": {
        "path": "/Users/steve/Documents/翻译项目/AWifesPhoneEP1/AWifesPhone_CN_Backup/game/tl/zh_Hans/new_main_phone_0_2_part_2.rpy",
        "line_idx": 368076,
        "correct_content": '    nvljenna "别忘了练习[stepsis_name_is]教你的 {image=wink_emoji.png}"\n'
    },
    "wife_phone": {
        "path": "/Users/steve/Documents/翻译项目/AWifesPhoneEP1/AWifesPhone_CN_Backup/game/tl/zh_Hans/new_main_wife_phone_0_2.rpy",
        "line_idx": 28530,
        "correct_content": '    "{color=#000}[wife_name_is]: {color=#e21978}啊啊啊！啊！别……别停……啊啊啊！"\n'
    },
    # 第二部
    "talay_mc": {
        "path": "/Users/steve/Documents/翻译项目/AWifesPhoneEP1/AWifesPhone2_CN_Backup/game/tl/zh_Hans/scripts/dialogues/talay/talay_mc_storyline.rpy",
        "line_idx": 2462,
        "correct_content": '    nvltalay "醉酒的母马"\n'
    },
    "wife_coworker": {
        "path": "/Users/steve/Documents/翻译项目/AWifesPhoneEP1/AWifesPhone2_CN_Backup/game/tl/zh_Hans/scripts/dialogues/wife/wife_coworker_storyline.rpy",
        "line_idx": 2130,
        "correct_content": '    nvleric "我同意，但有一个条件。我们要在办公室里做，[wife_name_is]"\n'
    }
}

def main():
    print("开始执行强力物理修复报错行...")
    for key, info in FILES_TO_FIX.items():
        fp = info["path"]
        l_idx = info["line_idx"]
        correct = info["correct_content"]
        
        if not os.path.exists(fp):
            print(f"[跳过] 文件不存在: {fp}")
            continue
            
        with open(fp, 'r', encoding='utf-8') as f:
            lines = f.readlines()
            
        if l_idx < len(lines):
            print(f"正在修复 {os.path.basename(fp)} 第 {l_idx+1} 行:")
            print(f"  原内容: {repr(lines[l_idx])}")
            print(f"  改写为: {repr(correct)}")
            lines[l_idx] = correct
            
            with open(fp, 'w', encoding='utf-8') as f:
                f.writelines(lines)
            print("  [修复成功]")
        else:
            print(f"[错误] {os.path.basename(fp)} 行号 {l_idx+1} 超出了文件总行数 {len(lines)}")

if __name__ == "__main__":
    main()
