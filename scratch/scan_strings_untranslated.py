#!/usr/bin/env python3
import os
import re

# ==================== 配置 ====================
BACKUP_DIR = "/Users/steve/Documents/翻译项目/AWifesPhoneEP1/AWifesPhone_CN_Backup/game/tl/zh_Hans"

# 正则表达式
pattern_old = re.compile(r'^\s*old\s*"((?:[^"\\]|\\.)*)"\s*$')
pattern_new = re.compile(r'^\s*new\s*"((?:[^"\\]|\\.)*)"\s*$')

def main():
    print("开始扫描第一部汉化文件中 strings 块下未翻译的 old/new 对...")
    untranslated_count = 0
    
    rpy_files = []
    for root, dirs, files in os.walk(BACKUP_DIR):
        for f in files:
            if f.endswith(".rpy"):
                rpy_files.append(os.path.join(root, f))
                
    for fp in rpy_files:
        with open(fp, 'r', encoding='utf-8') as f:
            lines = f.readlines()
            
        file_printed = False
        in_strings = False
        
        idx = 0
        while idx < len(lines):
            line = lines[idx]
            if "translate zh_Hans strings:" in line:
                in_strings = True
                idx += 1
                continue
                
            if in_strings:
                # 如果遇到了其它的 translate 语句，说明 strings 块结束了
                if line.strip().startswith("translate zh_Hans") and "strings:" not in line:
                    in_strings = False
                    idx += 1
                    continue
                    
                m_old = pattern_old.match(line)
                if m_old:
                    old_val = m_old.group(1)
                    # 寻找下一行是不是 new
                    if idx + 1 < len(lines):
                        next_line = lines[idx+1]
                        m_new = pattern_new.match(next_line)
                        if m_new:
                            new_val = m_new.group(1)
                            # 如果 old 包含英文字母且与 new 完全一样
                            if old_val.strip() == new_val.strip() and any(c.isalpha() for c in old_val):
                                if not file_printed:
                                    print(f"\n[文件] {os.path.relpath(fp, BACKUP_DIR)}")
                                    file_printed = True
                                print(f"  行号 {idx+1}: old \"{old_val}\" -> new \"{new_val}\"")
                                untranslated_count += 1
                            idx += 2
                            continue
            idx += 1
                        
    print(f"\n共发现 {untranslated_count} 处未翻译的 strings 选项。")

if __name__ == "__main__":
    main()
