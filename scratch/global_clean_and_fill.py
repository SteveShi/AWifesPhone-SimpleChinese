#!/usr/bin/env python3
import os
import re

# ==================== 配置 ====================
BACKUP_DIRS = [
    "/Users/steve/Documents/翻译项目/AWifesPhoneEP1/AWifesPhone_CN_Backup/game/tl/zh_Hans",
    "/Users/steve/Documents/翻译项目/AWifesPhoneEP1/AWifesPhone2_CN_Backup/game/tl/zh_Hans"
]

# ==================== 正则与语法解析 ====================
pattern_spk_id = re.compile(r'^(\s*)([a-zA-Z0-9_]+)\s*"((?:[^"\\]|\\.)*)"\s*$')
pattern_no_spk = re.compile(r'^(\s*)"((?:[^"\\]|\\.)*)"\s*$')

def parse_line(line):
    m = pattern_spk_id.match(line)
    if m: return m.group(1), m.group(2), m.group(3)
    m = pattern_no_spk.match(line)
    if m: return m.group(1), None, m.group(2)
    return None, None, None

# ==================== 精准物理裁剪算法 ====================
def clean_mixed_text(zh_val, en_val):
    """
    如果 zh_val 里包含了 en_val，我们需要把尾部的英文裁剪掉，只保留中文部分。
    """
    zh_str = zh_val.strip()
    en_str = en_val.strip()
    
    if not en_str:
        return zh_val
        
    # 情况1：直接以 en_str 结尾
    if zh_str.endswith(en_str):
        cleaned = zh_str[:len(zh_str) - len(en_str)].rstrip()
        # 补回原有的首尾空格或转义
        return cleaned
        
    # 情况2：带标签的不规则拼接，例如：
    # "爸爸，您…… {image=love_emoji.png}Dad, you... {image=love_emoji.png}"
    # 我们用剔除标签后的纯英文文本进行右侧匹配
    # 提取 en 里的纯英文词（非标签部分）
    en_clean = re.sub(r'\[[^\]]+\]|\{[^\}]+\}', '', en_str).strip()
    if en_clean:
        # 如果 zh_str 结尾是这段纯英文
        if zh_str.endswith(en_clean):
            cleaned = zh_str[:len(zh_str) - len(en_clean)].rstrip()
            return cleaned
            
    # 情况3：如果 zh_str 里面确实包含 en_str
    if en_str in zh_str:
        # 找到最后一次出现的地方，如果接近右侧
        idx = zh_str.rfind(en_str)
        if idx > 0 and (len(zh_str) - idx - len(en_str)) < 5:
            return zh_str[:idx].rstrip()
            
    return zh_val

def determine_role_hint(file_path):
    fn = os.path.basename(file_path)
    parent = os.path.basename(os.path.dirname(file_path))
    if "son" in fn or parent == "son":
        return "Edwin_Son_Mickey"
    elif "mark" in fn:
        return "Mark_Brother"
    elif "fem_mc" in parent or "fem_mc" in fn:
        return "Fem_MC_Protagonist"
    elif "julia_romance" in fn or "niece" in fn:
        return "Julia_Romance_Uncle"
    elif "julia" in fn:
        return "Julia_BBC"
    return "generic"

# ==================== 主逻辑 ====================
def main():
    # 1. 扫描所有的 .rpy 文件
    rpy_files = []
    for d in BACKUP_DIRS:
        if not os.path.exists(d):
            continue
        for root, dirs, files in os.walk(d):
            if "blank_templates" in root:
                continue
            for f in files:
                if f.endswith(".rpy"):
                    rpy_files.append(os.path.join(root, f))
                    
    print(f"共发现 {len(rpy_files)} 个剧本文件。")

    # 2. 全局清洗覆写
    print("开始执行 100% 物理级汉化清洗与格式规范...")
    files_updated = 0
    lines_overwritten = 0

    for fp in rpy_files:
        with open(fp, 'r', encoding='utf-8') as f:
            lines = f.readlines()
            
        file_modified = False
        role_hint = determine_role_hint(fp)
        
        for idx in range(1, len(lines)):
            line = lines[idx]
            if line.strip() and not line.strip().startswith("#"):
                indent, spk, zh = parse_line(line)
                if zh is not None:
                    # 往前寻找注释行以获取纯英文原文
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
                                
                    if found_en is not None:
                        # 核心清洗1：剔除多余的中英文拼接
                        cleaned_zh = clean_mixed_text(zh, found_en)
                        
                        # 核心清洗2：将“您”全部纠偏替换为“你”
                        cleaned_zh = cleaned_zh.replace("您", "你")
                        
                        # 核心清洗3：侄女日常暧昧线含蓄化规范
                        if role_hint == "Julia_Romance_Uncle":
                            # 对日常叔侄暧昧路线中的敏感生理词汇进行去粗俗化优雅改写
                            cleaned_zh = cleaned_zh.replace("鸡巴", "坏家伙")
                            cleaned_zh = cleaned_zh.replace("肉棒", "坏家伙")
                            cleaned_zh = cleaned_zh.replace("骚穴", "身子")
                            cleaned_zh = cleaned_zh.replace("骚货", "坏丫头")
                            cleaned_zh = cleaned_zh.replace("小穴", "身子")
                            cleaned_zh = cleaned_zh.replace("湿了", "动情了")
                            cleaned_zh = cleaned_zh.replace("硬了", "兴奋了")
                            cleaned_zh = cleaned_zh.replace("勃起", "兴奋")
                            cleaned_zh = cleaned_zh.replace("操你", "要你")
                            cleaned_zh = cleaned_zh.replace("操我", "要我")
                            cleaned_zh = cleaned_zh.replace("射精", "爱液")
                        
                        # 精准双重转义：先还原已有转义为普通双引号，再重新进行单次精确转义，彻底消灭 \\\\" 和多重斜杠Bug
                        escaped_zh = cleaned_zh.replace('\\"', '"').replace('"', '\\"')
                        if spk:
                            new_line = f'{indent}{spk} "{escaped_zh}"\n'
                        else:
                            new_line = f'{indent}"{escaped_zh}"\n'
                        
                        if lines[idx] != new_line:
                            lines[idx] = new_line
                            file_modified = True
                            lines_overwritten += 1

        # 特别对 screens.rpy 里的特定二连发和管道符 Bug 进行物理清洗
        if fp.endswith("screens.rpy"):
            print(f"正在物理修复 {os.path.basename(fp)} 里的特殊 UI 选项翻译...")
            for l_idx, l_val in enumerate(lines):
                if 'new "{#auto_page}自动|{#auto_page}自动"' in l_val:
                    lines[l_idx] = l_val.replace('new "{#auto_page}自动|{#auto_page}自动"', 'new "{#auto_page}自动"')
                    file_modified = True
                    lines_overwritten += 1
                if 'new "{#quick_page}快速|{#quick_page}快速"' in l_val:
                    lines[l_idx] = l_val.replace('new "{#quick_page}快速|{#quick_page}快速"', 'new "{#quick_page}快速"')
                    file_modified = True
                    lines_overwritten += 1
                if 'new "{size=28}{#file_time}%B %d, %H:%M|{size=28}{#file_time}%B  %d， %H ：%M"' in l_val:
                    lines[l_idx] = l_val.replace('new "{size=28}{#file_time}%B %d, %H:%M|{size=28}{#file_time}%B  %d， %H ：%M"', 'new "{size=28}{#file_time}%B %d, %H:%M"')
                    file_modified = True
                    lines_overwritten += 1

        if file_modified:
            with open(fp, 'w', encoding='utf-8') as f:
                f.writelines(lines)
            files_updated += 1

    print(f"全局物理清洗与覆写成功结束！更新了 {files_updated} 个剧本文件，共完美清洗了 {lines_overwritten} 行剧本对白。")

if __name__ == "__main__":
    main()
