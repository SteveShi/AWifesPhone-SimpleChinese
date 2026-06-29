#!/usr/bin/env python3
import os
import re

# ==================== 配置 ====================
BACKUP_DIR = "/Users/steve/Documents/翻译项目/AWifesPhoneEP1/AWifesPhone_CN_Backup/game/tl/zh_Hans"

# 正则表达式
pattern_spk_id = re.compile(r'^(\s*)([a-zA-Z0-9_]+)\s*"((?:[^"\\]|\\.)*)"\s*$')
pattern_no_spk = re.compile(r'^(\s*)"((?:[^"\\]|\\.)*)"\s*$')

def parse_line(line):
    m = pattern_spk_id.match(line)
    if m: return m.group(1), m.group(2), m.group(3)
    m = pattern_no_spk.match(line)
    if m: return m.group(1), None, m.group(2)
    return None, None, None

def is_pure_english(text):
    # 去除 Ren'Py 标签和插值
    clean = re.sub(r'\[[^\]]+\]|\{[^\}]+\}', '', text).strip()
    if not clean:
        return False
    # 判断是否只包含英文字母、数字、空格和标点
    return all(ord(c) < 128 for c in clean)

def main():
    print("开始扫描第一部汉化文件中，翻译行与英文注释完全一致且为纯英文的行...")
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
        for idx in range(1, len(lines)):
            line = lines[idx]
            if line.strip() and not line.strip().startswith("#"):
                indent, spk, zh = parse_line(line)
                if zh is not None and is_pure_english(zh):
                    # 往前寻找它的英文注释行
                    found_en = None
                    for offset in range(1, 6):
                        prev_idx = idx - offset
                        if prev_idx < 0: break
                        prev_line = lines[prev_idx]
                        if prev_line.strip() and not prev_line.strip().startswith("#"):
                            prev_indent, prev_spk, prev_zh = parse_line(prev_line)
                            if prev_zh is not None: break
                        if prev_line.strip().startswith("#"):
                            comment_content = prev_line.strip().lstrip("#").strip()
                            c_indent, spk_en, en = parse_line("    " + comment_content)
                            if en is not None and spk_en == spk:
                                found_en = en
                                break
                                
                    if found_en is not None and zh.strip() == found_en.strip():
                        # 检查上一行是不是 "menu:" 相关的对白或者是选项提示
                        # 在 Ren'Py 中，translate 语句上方的注释里通常会有原始文件路径和行号，如：
                        # # game/script.rpy:123
                        # 我们打印出它的上下文
                        if not file_printed:
                            print(f"\n[文件] {os.path.relpath(fp, BACKUP_DIR)}")
                            file_printed = True
                        print(f"  行号 {idx+1}: {line.strip()} (英文注释: {found_en})")
                        untranslated_count += 1
                        
    print(f"\n共发现 {untranslated_count} 处未翻译的英文行。")

if __name__ == "__main__":
    main()
