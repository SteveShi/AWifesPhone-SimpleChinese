import os
import re
import json

TARGET_DIRS = [
    "/Users/steve/Documents/翻译项目/AWifesPhoneEP1/AWifesPhone_CN_Backup",
    "/Users/steve/Documents/翻译项目/AWifesPhoneEP1/AWifesPhone2_CN_Backup",
    "/Users/steve/Downloads/AWifesPhoneEP1.app/Contents/Resources/autorun/game/tl/zh_Hans",
    "/Users/steve/Downloads/AWifesPhone.app/Contents/Resources/autorun/game/tl/zh_Hans"
]

SUN_EXCLUDES = [
    "晒太阳", "太阳底下", "太阳升起", "太阳裙", "太阳眩光", 
    "太阳图标", "{#weekday_short}太阳", "小太阳", "太阳系", "太阳镜"
]

def check_string(s, en_context=None, file_name=""):
    """
    检查字符串中是否有违禁词或遗留词。
    返回错误信息列表。
    """
    errors = []
    
    # 1. 遗留 凯瑞莉
    if "凯瑞莉" in s:
        errors.append(f"发现遗留词 '凯瑞莉'")
        
    # 2. 遗留 基雷莉
    if "基雷莉" in s:
        errors.append(f"发现遗留词 '基雷莉'")
        
    # 3. 遗留 继兄
    if "继兄" in s:
        errors.append(f"发现遗留词 '继兄'")
        
    # 4. 遗留 继妹
    if "继妹" in s:
        errors.append(f"发现遗留词 '继妹'")
        
    # 5. 遗留 女星印记
    if "女星印记" in s:
        errors.append(f"发现遗留词 '女星印记'")

    # 6. 未替换的 Sola (对白中出现英文 Sola/sola)
    sola_matches = re.findall(r'\b[Ss]ola\b', s)
    if sola_matches:
        # 如果英文上下文本来就是 Sola，中文对白里不应该有 Sola
        errors.append(f"对白中发现未翻译/未纠偏的英文 'Sola': \"{s}\"")
        
    # 7. 太阳能内容 遗留
    if "太阳能内容" in s:
        errors.append(f"发现未替换的 '太阳能内容'")

    # 8. 不合法的 太阳
    if "太阳" in s:
        has_exclude = any(ex in s for ex in SUN_EXCLUDES)
        if not has_exclude:
            # 排除 weekday_short 的合法性
            if en_context and "weekday_short" in en_context:
                pass
            else:
                errors.append(f"发现疑似错译为 '太阳' (Sola) 的文本: \"{s}\"")

    # 9. 不合法的 标记
    if "标记" in s:
        if s == "标记" and en_context == "Mark":
            errors.append(f"发现遗留词 '标记' (对应英文 Mark)")
        elif s == "标记妻子默认路径":
            errors.append(f"发现遗留词 '标记妻子默认路径'")
            
    # 10. Kirely 的错译 Casey 遗留检测
    if en_context and any(k in en_context.lower() for k in ["kirely", "kirey", "kirley"]):
        if any(name in s for name in ["凯茜", "凯西"]):
            errors.append(f"英文为 Kirely，但中文中仍发现 '{s}' 包含 凯茜/凯西")

    # 11. Julia/stepsis 对男主错误称呼 凯茜/凯西 遗留检测
    is_julia_or_stepsis_file = "julia" in file_name.lower() or "stepsis" in file_name.lower()
    if is_julia_or_stepsis_file or (en_context and any(x in en_context.lower() for x in ["julia", "stepsis", "nvljulia", "nvlstepsis"])):
        for name in ["凯茜", "凯西"]:
            if f"嘿，{name}" in s or f"你好，{name}" in s or f"谢谢你，{name}" in s:
                errors.append(f"在 Julia/stepsis 语境中发现疑似对男主错误称呼: \"{s}\"")

    return errors

def main():
    print("==================================================")
    print("开始运行补丁验证脚本，检查遗留违禁词...")
    print("==================================================")
    
    all_errors = []
    checked_files = 0
    
    for directory in TARGET_DIRS:
        if not os.path.exists(directory):
            print(f"【忽略】目录不存在: {directory}")
            continue
            
        print(f"扫描目录: {directory}")
        for root, _, files in os.walk(directory):
            for file in files:
                file_path = os.path.join(root, file)
                checked_files += 1
                
                # 校验 .rpy 或 .po
                if file.endswith('.rpy') or file.endswith('.po'):
                    try:
                        with open(file_path, 'r', encoding='utf-8') as f:
                            lines = f.readlines()
                    except Exception as e:
                        print(f"Error reading {file_path}: {e}")
                        continue
                        
                    for idx, line in enumerate(lines):
                        if line.strip().startswith("#"):
                            continue
                            
                        # 查找英文上下文
                        en_context = None
                        if idx > 0 and lines[idx-1].strip().startswith("#"):
                            en_context = lines[idx-1].strip()
                        elif idx > 0 and lines[idx-1].strip().startswith("msgid"):
                            m = re.match(r'msgid\s+"(.*)"', lines[idx-1].strip())
                            if m:
                                en_context = m.group(1)
                                
                        # 查找双引号内容
                        pattern = r'"((?:[^"\\]|\\.)*)"'
                        matches = re.findall(pattern, line)
                        for match in matches:
                            errs = check_string(match, en_context, file)
                            for err in errs:
                                all_errors.append(f"{file}:{idx+1}: {err} -> ZH: \"{match}\"")
                                
                # 校验 .json
                elif file.endswith('.json'):
                    try:
                        with open(file_path, 'r', encoding='utf-8') as f:
                            data = json.load(f)
                    except Exception as e:
                        print(f"Error reading {file_path}: {e}")
                        continue
                        
                    def check_json_node(d):
                        if isinstance(d, dict):
                            for k, v in d.items():
                                if isinstance(v, str):
                                    errs = check_string(v, en_context=k, file_name=file)
                                    for err in errs:
                                        all_errors.append(f"{file} key '{k}': {err} -> ZH: \"{v}\"")
                                else:
                                    check_json_node(v)
                        elif isinstance(d, list):
                            for idx, item in enumerate(d):
                                if isinstance(item, str):
                                    errs = check_string(item, en_context=None, file_name=file)
                                    for err in errs:
                                        all_errors.append(f"{file} index {idx}: {err} -> ZH: \"{item}\"")
                                else:
                                    check_json_node(item)
                                    
                    check_json_node(data)

    print("\n================== 验证结果 ==================")
    print(f"已检查文件数: {checked_files}")
    if all_errors:
        print(f"❌ 验证未通过！共发现 {len(all_errors)} 处遗留/不合规问题：")
        for err in all_errors[:50]: # 打印前50个
            print(f"  - {err}")
        if len(all_errors) > 50:
            print(f"  ... 以及其余 {len(all_errors) - 50} 处。")
        exit(1)
    else:
        print("✅ 验证全部通过！无遗留违禁词，未发现任何不合规项。")
        exit(0)

if __name__ == "__main__":
    main()
