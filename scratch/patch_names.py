import os
import re
import json

# 目标替换的 4 个路径
TARGET_DIRS = [
    "/Users/steve/Documents/翻译项目/AWifesPhoneEP1/AWifesPhone_CN_Backup",
    "/Users/steve/Documents/翻译项目/AWifesPhoneEP1/AWifesPhone2_CN_Backup",
    "/Users/steve/Downloads/AWifesPhoneEP1.app/Contents/Resources/autorun/game/tl/zh_Hans",
    "/Users/steve/Downloads/AWifesPhone.app/Contents/Resources/autorun/game/tl/zh_Hans"
]

# 统计数据
stats = {
    "total_files_processed": 0,
    "total_files_modified": 0,
    "total_lines_replaced": 0,
    "rule1_sola": 0,       # 太阳/Sola -> 索拉
    "rule2_mark": 0,       # 标记 -> 马克
    "rule3_fem_mark": 0,   # 女星印记 -> 女性化马克
    "rule4_kirely_casey": 0, # Casey/Kacey as Kirely/Julia wrong -> 绮芮/[mc_name_is]
    "rule5_kirely1": 0,    # 凯瑞莉 -> 绮芮
    "rule6_kirely2": 0,    # 基雷莉 -> 绮芮
    "rule7_stepbrother": 0,# 继兄 -> 哥哥
    "rule8_stepsister": 0  # 继妹 -> 妹妹
}

# 太阳排除词
SUN_EXCLUDES = [
    "晒太阳", "太阳底下", "太阳升起", "太阳裙", "太阳眩光", 
    "太阳图标", "{#weekday_short}太阳", "小太阳", "太阳系", "太阳镜"
]

def replace_string(s, en_context=None, file_name=""):
    """
    对双引号内部的中文翻译字符串做高精度替换。
    """
    global stats
    modified = False
    
    # 规则 5: 凯瑞莉 -> 绮芮
    if "凯瑞莉" in s:
        s_new = s.replace("凯瑞莉", "绮芮")
        if s_new != s:
            stats["rule5_kirely1"] += s.count("凯瑞莉")
            s = s_new
            modified = True

    # 规则 6: 基雷莉 -> 绮芮
    if "基雷莉" in s:
        s_new = s.replace("基雷莉", "绮芮")
        if s_new != s:
            stats["rule6_kirely2"] += s.count("基雷莉")
            s = s_new
            modified = True

    # 规则 1: 太阳 -> 索拉 (Sola)
    # 剧情里所有独立的 Sola 英文单词都纠偏为 索拉
    s_new = re.sub(r'\b[Ss]ola\b', "索拉", s)
    if s_new != s:
        stats["rule1_sola"] += 1
        s = s_new
        modified = True
        
    # 如果中文里有 "太阳能内容"（Sola content 错译），换为 "索拉内容"
    if "太阳能内容" in s:
        s = s.replace("太阳能内容", "索拉内容")
        stats["rule1_sola"] += 1
        modified = True

    # 如果有 "太阳" 二字
    if "太阳" in s:
        # 检查是否包含任何太阳排除词
        has_exclude = any(ex in s for ex in SUN_EXCLUDES)
        # 如果没有排除词，或者就是单独的 "太阳"，则替换为 "索拉"
        if not has_exclude:
            # 只有当英文上下文是 Sola，或者没有英文上下文，或者是 JSON 键值对时
            if en_context is None or any(x in en_context.lower() for x in ["sola", "weekday_short"]):
                # 再次防护：如果含有 weekday_short 则不替换，因为那是星期天
                if en_context and "weekday_short" in en_context:
                    pass
                else:
                    s_new = s.replace("太阳", "索拉")
                    if s_new != s:
                        stats["rule1_sola"] += s.count("太阳")
                        s = s_new
                        modified = True

    # 规则 2: 标记 -> 马克
    # 只针对 Mark 人名被翻译成标记的纠错，不误伤动词“标记”
    # 在 strings.json 里 "Mark": "标记", "Mark-Wife Default Path": "标记妻子默认路径" 必定需要替换
    # 在对白中，如果完全是 "标记" 或者特定的 "标记 - 海伦卡..."
    if "标记" in s:
        # 如果是 strings.json 中的项
        if en_context and en_context == "Mark" and s == "标记":
            s = "马克"
            stats["rule2_mark"] += 1
            modified = True
        elif en_context and en_context == "Mark-Wife Default Path" and s == "标记妻子默认路径":
            s = "马克-妻子默认路径"
            stats["rule2_mark"] += 1
            modified = True
        elif s == "标记":
            s = "马克"
            stats["rule2_mark"] += 1
            modified = True
        elif "标记 - 海伦卡·德米多娃" in s:
            s = s.replace("标记 - 海伦卡·德米多娃", "马克 - 海伦卡·德米多娃")
            stats["rule2_mark"] += 1
            modified = True

    # 规则 3: 女星印记 -> 女性化马克 (Fem Mark)
    if "女星印记" in s:
        s_new = s.replace("女星印记", "女性化马克")
        if s_new != s:
            stats["rule3_fem_mark"] += s.count("女星印记")
            s = s_new
            modified = True

    # 规则 4: 凯茜、凯西在作为 Kirely 错译，或 Julia 误称男主时 -> [mc_name_is] 或是 绮芮
    # 4A. Kirely 的错译
    if en_context and any(k in en_context.lower() for k in ["kirely", "kirey", "kirley"]):
        for name in ["凯茜", "凯西"]:
            if name in s:
                s_new = s.replace(name, "绮芮")
                if s_new != s:
                    stats["rule4_kirely_casey"] += s.count(name)
                    s = s_new
                    modified = True
                    
    # 4B. 英文注释行包含插值变量，而中文包含 凯茜/凯西 (被硬编码的错译)
    if en_context:
        for var in ["[mc_name_is]", "[w_mc_name_is]", "[s_mc_name_is]", "[d_mc_name_is]"]:
            if var in en_context and not any(c in en_context.lower() for c in ["casey", "cacey"]):
                for name in ["凯茜", "凯西"]:
                    if name in s:
                        # 确保不误伤本身包含该变量的合理对白
                        s_new = s.replace(name, var)
                        if s_new != s:
                            stats["rule4_kirely_casey"] += s.count(name)
                            s = s_new
                            modified = True

    # 4C. Julia 误称男主为 凯茜/凯西（如“嘿，凯茜”、“你好，凯茜”、“谢谢你，凯茜”；以及 stepsis 说的 “我是说，凯茜”）
    # 我们根据常见句子或特定文件/说话人做更积极的映射
    is_julia_or_stepsis_file = "julia" in file_name.lower() or "stepsis" in file_name.lower()
    if is_julia_or_stepsis_file or (en_context and any(x in en_context.lower() for x in ["julia", "stepsis", "nvljulia", "nvlstepsis"])):
        # 嘿，凯茜/凯西
        for name in ["凯茜", "凯西"]:
            if f"嘿，{name}" in s:
                s = s.replace(f"嘿，{name}", "嘿，[mc_name_is]")
                stats["rule4_kirely_casey"] += 1
                modified = True
            if f"你好，{name}" in s:
                s = s.replace(f"你好，{name}", "你好，[mc_name_is]")
                stats["rule4_kirely_casey"] += 1
                modified = True
            if f"谢谢你，{name}" in s:
                s = s.replace(f"谢谢你，{name}", "谢谢你，[mc_name_is]")
                stats["rule4_kirely_casey"] += 1
                modified = True
            if f"我是说，{name}" in s:
                s = s.replace(f"我是说，{name}", "我是说，[w_mc_name_is]")
                stats["rule4_kirely_casey"] += 1
                modified = True

    # 规则 7: 继兄 -> 哥哥
    if "继兄" in s:
        s_new = s.replace("继兄", "哥哥")
        if s_new != s:
            stats["rule7_stepbrother"] += s.count("继兄")
            s = s_new
            modified = True

    # 规则 8: 继妹 -> 妹妹
    if "继妹" in s:
        s_new = s.replace("继妹", "妹妹")
        if s_new != s:
            stats["rule8_stepsister"] += s.count("继妹")
            s = s_new
            modified = True

    return s, modified

def process_rpy_or_po(file_path):
    """
    处理 .rpy 或 .po 文件，对所有双引号内的字符串执行高精度替换。
    """
    global stats
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            lines = f.readlines()
    except Exception as e:
        print(f"Error reading {file_path}: {e}")
        return False

    modified_file = False
    new_lines = []
    file_name = os.path.basename(file_path)

    for idx, line in enumerate(lines):
        # 寻找前一行的英文注释
        en_context = None
        if idx > 0 and lines[idx-1].strip().startswith("#"):
            en_context = lines[idx-1].strip()
        # 对于 po 文件，msgid 可以是 en_context
        elif idx > 0 and lines[idx-1].strip().startswith("msgid"):
            # 提取 msgid 后双引号内的内容
            m = re.match(r'msgid\s+"(.*)"', lines[idx-1].strip())
            if m:
                en_context = m.group(1)

        # 匹配双引号括起来的内容，同时处理可能的转义双引号 \"
        pattern = r'"((?:[^"\\]|\\.)*)"'
        
        line_replaced = False
        def quote_replacer(match):
            nonlocal line_replaced
            original_str = match.group(1)
            # 进行替换
            replaced_str, str_modified = replace_string(original_str, en_context, file_name)
            if str_modified:
                line_replaced = True
                return f'"{replaced_str}"'
            return match.group(0)

        # 只对非注释行进行替换
        # 但在 rpy 中，如果本身是 # 头的行，就不要做替换了，因为那是英文原文
        if not line.strip().startswith("#"):
            new_line = re.sub(pattern, quote_replacer, line)
            if line_replaced:
                line = new_line
                stats["total_lines_replaced"] += 1
                modified_file = True
        
        new_lines.append(line)

    if modified_file:
        try:
            with open(file_path, 'w', encoding='utf-8') as f:
                f.writelines(new_lines)
            stats["total_files_modified"] += 1
            return True
        except Exception as e:
            print(f"Error writing {file_path}: {e}")
    return False

def process_json(file_path):
    """
    处理 .json 文件，将其解析为字典并递归替换 value。
    """
    global stats
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
    except Exception as e:
        print(f"Error reading {file_path}: {e}")
        return False

    modified_file = False
    
    # 递归字典处理
    def recurse_replace(d):
        nonlocal modified_file
        if isinstance(d, dict):
            for k, v in d.items():
                if isinstance(v, str):
                    # 将 key 作为 en_context 传入
                    new_val, val_modified = replace_string(v, en_context=k, file_name=os.path.basename(file_path))
                    if val_modified:
                        d[k] = new_val
                        modified_file = True
                        stats["total_lines_replaced"] += 1
                else:
                    recurse_replace(v)
        elif isinstance(d, list):
            for idx, item in enumerate(d):
                if isinstance(item, str):
                    new_val, val_modified = replace_string(item, en_context=None, file_name=os.path.basename(file_path))
                    if val_modified:
                        d[idx] = new_val
                        modified_file = True
                        stats["total_lines_replaced"] += 1
                else:
                    recurse_replace(item)

    recurse_replace(data)

    if modified_file:
        try:
            with open(file_path, 'w', encoding='utf-8') as f:
                # 保持原样的缩进和确保不使用 ascii 转义中文
                json.dump(data, f, ensure_ascii=False, indent=2)
            stats["total_files_modified"] += 1
            return True
        except Exception as e:
            print(f"Error writing {file_path}: {e}")
    return False

def main():
    print("==================================================")
    print("开始运行 Ren'Py 高精度名字与汉化热补丁脚本...")
    print("==================================================")

    for directory in TARGET_DIRS:
        if not os.path.exists(directory):
            print(f"【跳过】目录不存在: {directory}")
            continue
        
        print(f"正在处理目录: {directory}")
        for root, _, files in os.walk(directory):
            for file in files:
                file_path = os.path.join(root, file)
                # 确认文件类型
                if file.endswith('.rpy') or file.endswith('.po'):
                    stats["total_files_processed"] += 1
                    process_rpy_or_po(file_path)
                elif file.endswith('.json'):
                    stats["total_files_processed"] += 1
                    process_json(file_path)

    print("\n================== 补丁处理完成统计 ==================")
    print(f"总共扫描处理文件数: {stats['total_files_processed']}")
    print(f"总共修改文件数:     {stats['total_files_modified']}")
    print(f"总共替换代码行数:   {stats['total_lines_replaced']}")
    print("--------------------------------------------------")
    print(f"规则1 (Sola/太阳 -> 索拉):        {stats['rule1_sola']} 次")
    print(f"规则2 (标记 -> 马克):             {stats['rule2_mark']} 次")
    print(f"规则3 (女星印记 -> 女性化马克):     {stats['rule3_fem_mark']} 次")
    print(f"规则4 (Kirely/Julia/插值变量错译): {stats['rule4_kirely_casey']} 次")
    print(f"规则5 (凯瑞莉 -> 绮芮):           {stats['rule5_kirely1']} 次")
    print(f"规则6 (基雷莉 -> 绮芮):           {stats['rule6_kirely2']} 次")
    print(f"规则7 (继兄 -> 哥哥):             {stats['rule7_stepbrother']} 次")
    print(f"规则8 (继妹 -> 妹妹):             {stats['rule8_stepsister']} 次")
    print("==================================================")

if __name__ == "__main__":
    main()
