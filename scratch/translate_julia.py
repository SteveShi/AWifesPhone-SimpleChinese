#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import re
import json
import time
import random
import subprocess
import urllib.request
import urllib.error
from concurrent.futures import ThreadPoolExecutor, as_completed

# ==========================================
# 配置与路径
# ==========================================
FILE_1 = "/Users/steve/Documents/翻译项目/AWifesPhoneEP1/AWifesPhone_CN_Backup/game/tl/zh_Hans/new_main_niece_phone_0_2.rpy"
FILE_2 = "/Users/steve/Documents/翻译项目/AWifesPhoneEP1/AWifesPhone2_CN_Backup/game/tl/zh_Hans/scripts/dialogues/julia_storyline.rpy"

# GCP Project Info
PROJECT_ID = "reflected-space-491810-m7"
MODEL_ID = "gemini-2.5-flash"
REGION = "us-central1"
API_URL = f"https://{REGION}-aiplatform.googleapis.com/v1/projects/{PROJECT_ID}/locations/{REGION}/publishers/google/models/{MODEL_ID}:generateContent"

# Global Token Cache
TOKEN = None

# ==========================================
# Token 获取与网络请求
# ==========================================
def get_bearer_token():
    try:
        print("正在获取 GCP Bearer Token...")
        res = subprocess.run(["gcloud", "auth", "print-access-token"], capture_output=True, text=True, check=True)
        token = res.stdout.strip()
        print("Bearer Token 获取成功。")
        return token
    except Exception as e:
        print(f"获取 Bearer Token 失败: {e}")
        return None

def parse_json_response(text):
    text = text.strip()
    if text.startswith("```"):
        # 剥离 markdown 标记
        lines = text.split("\n")
        if lines[0].startswith("```"):
            lines = lines[1:]
        if lines[-1].startswith("```"):
            lines = lines[:-1]
        text = "\n".join(lines).strip()
    return json.loads(text)

def translate_batch(batch_items, system_prompt, attempt=1):
    global TOKEN
    if not TOKEN:
        TOKEN = get_bearer_token()
    
    # 构造 payload
    payload = {
        "contents": [
            {
                "role": "user",
                "parts": [
                    {
                        "text": json.dumps(batch_items, ensure_ascii=False)
                    }
                ]
            }
        ],
        "systemInstruction": {
            "parts": [
                {
                    "text": system_prompt
                }
            ]
        },
        "generationConfig": {
            "responseMimeType": "application/json",
            "temperature": 0.3
        }
    }
    
    data = json.dumps(payload).encode('utf-8')
    req = urllib.request.Request(API_URL, data=data, method="POST")
    req.add_header("Content-Type", "application/json")
    req.add_header("Authorization", f"Bearer {TOKEN}")
    
    try:
        with urllib.request.urlopen(req, timeout=60) as response:
            res_body = response.read().decode('utf-8')
            res_json = json.loads(res_body)
            text = res_json["candidates"][0]["content"]["parts"][0]["text"]
            parsed = parse_json_response(text)
            return parsed
    except urllib.error.HTTPError as e:
        res_code = e.code
        print(f"HTTP 错误 {res_code}: {e.reason}")
        
        if res_code == 401:
            print("Token 失效 (401)，正在重新获取并重试...")
            TOKEN = get_bearer_token()
            if TOKEN:
                return translate_batch(batch_items, system_prompt, attempt)
        elif res_code == 429:
            if attempt <= 4:
                sleep_time = (2 ** attempt) + random.random()
                print(f"触发限流 (429)。将在 {sleep_time:.2f} 秒后进行第 {attempt}/4 次重试...")
                time.sleep(sleep_time)
                return translate_batch(batch_items, system_prompt, attempt + 1)
        else:
            try:
                error_body = e.read().decode('utf-8')
                print(f"错误详情: {error_body}")
            except:
                pass
        raise e
    except Exception as e:
        print(f"请求发生异常: {e}")
        raise e

# ==========================================
# 占位符与格式保护
# ==========================================
def protect_tags(text):
    pattern = r'\[[^\]]+\]|\{[^\}]+\}'
    tags = re.findall(pattern, text)
    
    protected_text = text
    mapping = {}
    for idx, tag in enumerate(tags):
        placeholder = f"XTAG{idx}X"
        protected_text = protected_text.replace(tag, placeholder, 1)
        mapping[placeholder] = tag
    return protected_text, mapping

def restore_tags(protected_text, mapping):
    restored_text = protected_text
    for placeholder, tag in mapping.items():
        pattern = re.compile(re.escape(placeholder), re.IGNORECASE)
        restored_text = pattern.sub(tag, restored_text)
    return restored_text

# ==========================================
# 对白提取与解析
# ==========================================
pattern_spk_id = re.compile(r'^\s*([a-zA-Z0-9_]+)\s*"((?:[^"\\]|\\.)*)"\s*$')
pattern_no_spk = re.compile(r'^\s*"((?:[^"\\]|\\.)*)"\s*$')
pattern_spk_str = re.compile(r'^\s*("[^"]+")\s*"((?:[^"\\]|\\.)*)"\s*$')

def parse_line(line):
    m = pattern_spk_id.match(line)
    if m:
        return m.group(1), m.group(2)
    m = pattern_spk_str.match(line)
    if m:
        return m.group(1), m.group(2)
    m = pattern_no_spk.match(line)
    if m:
        return None, m.group(1)
    return None, None

def extract_dialogues(file_path):
    print(f"正在从 {file_path} 提取对白...")
    with open(file_path, 'r', encoding='utf-8') as f:
        lines = f.readlines()
        
    dialogues = []
    for idx in range(1, len(lines)):
        line = lines[idx]
        if line.strip() and not line.strip().startswith("#"):
            spk, zh = parse_line(line)
            if zh is not None:
                # 向上寻找匹配的注释英文行
                found_en = None
                for offset in range(1, 6):
                    prev_idx = idx - offset
                    if prev_idx < 0:
                        break
                    prev_line = lines[prev_idx]
                    # 如果遇到另一个非注释的对白行，就必须停止
                    if prev_line.strip() and not prev_line.strip().startswith("#"):
                        prev_spk, prev_zh = parse_line(prev_line)
                        if prev_zh is not None:
                            break
                    
                    # 遇到注释行
                    if prev_line.strip().startswith("#"):
                        comment_content = prev_line.strip().lstrip("#").strip()
                        spk_en, en = parse_line("    " + comment_content)
                        if en is not None and spk_en == spk:
                            found_en = en
                            break
                if found_en is not None:
                    dialogues.append({
                        'file_path': file_path,
                        'line_idx': idx,
                        'en': found_en,
                        'zh_old': zh,
                        'speaker': spk
                    })
    print(f"从 {os.path.basename(file_path)} 提取了 {len(dialogues)} 条对白。")
    return lines, dialogues

# ==========================================
# 结构辅助类
# ==========================================
class SplittedText:
    def __init__(self, original_en):
        self.original_en = original_en
        self.parts = []

class TextPart:
    def __init__(self, original_part_en):
        self.original_part_en = original_part_en
        self.protected_text = ""
        self.mapping = {}
        self.translated_protected_text = None

# ==========================================
# 性别用语质检与修正
# ==========================================
def inspect_and_fix(translated_zh, speaker):
    if not translated_zh:
        return translated_zh
    female_speakers = ['nvljulia', 'nvlwife', 'nvlchee', 'julia', 'wife', 'chee']
    male_speakers = ['nvlmc', 'nvljohn', 'nvlpaul', 'mc', 'john', 'paul']
    
    if speaker in female_speakers:
        bad_words = ["我硬了", "我的老二", "我的老2", "我的鸡巴", "我的jj"]
        for word in bad_words:
            if word in translated_zh:
                print(f"【质检修正】女性角色 {speaker} 包含违规男性生理词: {word} -> 进行妩媚化替换。")
                translated_zh = translated_zh.replace("我硬了", "我身子都发软了")
                translated_zh = translated_zh.replace("我的鸡巴", "我身体的异样")
                translated_zh = translated_zh.replace("我的老二", "我身体的异样")
                translated_zh = translated_zh.replace("我的老2", "我身体的异样")
                translated_zh = translated_zh.replace("我的jj", "我身体的异样")
                
    if speaker in male_speakers:
        bad_words = ["我的骚穴", "我湿了"]
        for word in bad_words:
            if word in translated_zh:
                print(f"【质检修正】男性角色 {speaker} 包含违规女性生理词: {word} -> 进行欲望化替换。")
                translated_zh = translated_zh.replace("我湿了", "我兴奋了")
                translated_zh = translated_zh.replace("我的骚穴", "我的欲望")
                
    return translated_zh

# ==========================================
# 并发包装与重试逻辑
# ==========================================
def translate_batch_wrapper(batch, system_prompt, batch_idx):
    time.sleep(random.random() * 2)  # 随机错峰
    try:
        res = translate_batch(batch, system_prompt)
        time.sleep(1.5)
        return res
    except Exception as e:
        print(f"Batch {batch_idx} 翻译失败: {e}")
        raise e

# ==========================================
# 主运行流程
# ==========================================
def main():
    global TOKEN
    TOKEN = get_bearer_token()
    if not TOKEN:
        print("无法获取 Bearer Token，程序退出。")
        return

    # 1. 提取对白
    lines1, dialogues1 = extract_dialogues(FILE_1)
    lines2, dialogues2 = extract_dialogues(FILE_2)
    all_entries = dialogues1 + dialogues2

    # 2. 按英文原文去重
    en_to_entries = {}
    for entry in all_entries:
        en_to_entries.setdefault(entry['en'], []).append(entry)

    print(f"总计提取对白对: {len(all_entries)} 条，去重后唯一英文原文: {len(en_to_entries)} 条。")

    # 3. 切分与占位符保护
    splitted_texts = []
    protected_text_to_parts = {}

    for en in en_to_entries.keys():
        st = SplittedText(en)
        parts_raw = en.split('|')
        for p_raw in parts_raw:
            stripped_p = p_raw.strip()
            if not stripped_p:
                tp = TextPart(p_raw)
                tp.protected_text = ""
                tp.translated_protected_text = ""
                st.parts.append(tp)
                continue
            
            protected, mapping = protect_tags(stripped_p)
            tp = TextPart(p_raw)
            tp.protected_text = protected
            tp.mapping = mapping
            
            st.parts.append(tp)
            protected_text_to_parts.setdefault(protected, []).append(tp)
        splitted_texts.append(st)

    unique_protected_list = list(protected_text_to_parts.keys())
    print(f"进一步保护占位符去重后，共需发送翻译句数: {len(unique_protected_list)} 条。")

    # 4. 构造 Prompt
    system_prompt = """你是专业的日式成人视觉小说（R-18）汉化与中文精修润色专家。
当前翻译的剧情属于伦理禁忌题材，女主角朱莉娅（Julia）是男主角的亲侄女，两人处于暧昧或发生禁忌关系的禁忌恋爱中。

翻译与润色规则：
- 直接从英文原文翻译为简体中文，确保语言地道、流畅，极具视觉小说的代入感。
- 情色与暧昧场面用词规则：
  * 用词千万不能粗俗、粗鲁或过于直白下流。
  * 杜绝使用粗口脏话（例如“他妈的太火辣了”中的“他妈的”一律去除或改写为更自然酥麻的“真是迷人”、“太勾人了”）。
  * 严禁在第一人称中出现直白刺耳的生理词汇。例如：
    - 禁止出现“硬了”、“勃起”等。如果英文大意是“这让我兴奋/硬了”（如 "it makes me hard" 或 "I get hard" 等），必须将女方台词翻译为“我心里直发痒”、“身子都发软了”、“身体开始有些湿热/异样”等含蓄妩媚词汇；男方的词汇也要具有诱导性而不要太粗鲁（如“身体有些紧绷/兴奋了”、“感觉快按捺不住了”）。
    - 遵守性别用语规范：女性角色禁止出现第一人称男性生理词（如“我的老二”、“我硬了”、“射了”），男性角色禁止出现第一人称女性生理词。
- 严格保留所有形如 XTAG0X, XTAG1X, XTAG2X 等英文占位符，它们代表了原游戏中的重要标签或变量，不要翻译或改变它们，也不要在它们前后添加多余空格。

输入格式：
输入为 JSON 数组，每个元素包含 id 和 en。
示例：
[{"id": 0, "en": "I get so hard when you look at me like that, Julia."}]

输出格式：
只输出 JSON 数组，每个元素包含 id 和 zh。严禁使用 markdown 语法块（如 ```json ）。
示例：
[{"id": 0, "zh": "当你那样看着我的时候，我快按捺不住了，朱莉娅。"}]"""

    # 5. 并发翻译
    batches = []
    current_batch = []
    for idx, txt in enumerate(unique_protected_list):
        current_batch.append({"id": idx, "en": txt})
        if len(current_batch) == 50:
            batches.append(current_batch)
            current_batch = []
    if current_batch:
        batches.append(current_batch)

    results_map = {}
    max_workers = 30
    print(f"==================================================")
    print(f"正在进行第一轮大批次 (50条) 并发翻译...")
    print(f"总计分批: {len(batches)} 批，工作线程: {max_workers}")
    print(f"==================================================")

    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        future_to_batch = {}
        for batch_idx, batch in enumerate(batches):
            future = executor.submit(translate_batch_wrapper, batch, system_prompt, batch_idx)
            future_to_batch[future] = batch
            time.sleep(0.05)
            
        for future in as_completed(future_to_batch):
            batch = future_to_batch[future]
            try:
                parsed_results = future.result()
                for item in parsed_results:
                    results_map[item["id"]] = item["zh"]
            except Exception as e:
                for item in batch:
                    if item["id"] not in results_map:
                        results_map[item["id"]] = None

    # 6. 第二轮小批次重试
    missing_indices = []
    for idx in range(len(unique_protected_list)):
        if idx not in results_map or results_map[idx] is None:
            missing_indices.append(idx)
            
    if missing_indices:
        print(f"\n第一轮结束后，有 {len(missing_indices)} 条文本翻译未成功，进入第二轮重试...")
        retry_batches = []
        current_batch = []
        for midx in missing_indices:
            current_batch.append({"id": midx, "en": unique_protected_list[midx]})
            if len(current_batch) == 5:
                retry_batches.append(current_batch)
                current_batch = []
        if current_batch:
            retry_batches.append(current_batch)
            
        for batch_idx, batch in enumerate(retry_batches):
            print(f"重试批次 {batch_idx+1}/{len(retry_batches)} (大小 {len(batch)})...")
            success = False
            for attempt in range(3):
                try:
                    parsed = translate_batch(batch, system_prompt)
                    for item in parsed:
                        results_map[item["id"]] = item["zh"]
                    print(f"重试批次 {batch_idx+1} 成功。")
                    time.sleep(2.0)
                    success = True
                    break
                except Exception as e:
                    print(f"重试批次 {batch_idx+1} 失败 (尝试 {attempt+1}/3): {e}")
                    time.sleep(3.0)
            if not success:
                for item in batch:
                    if item["id"] not in results_map:
                        results_map[item["id"]] = None

    # 7. 合并回填
    for idx, txt in enumerate(unique_protected_list):
        translated_protected = results_map.get(idx)
        parts_to_fill = protected_text_to_parts[txt]
        for tp in parts_to_fill:
            tp.translated_protected_text = translated_protected

    # 8. 还原与缝合
    en_to_final_zh = {}
    for st in splitted_texts:
        final_parts_zh = []
        all_parts_ok = True
        for tp in st.parts:
            if tp.protected_text == "":
                final_parts_zh.append(tp.original_part_en)
                continue
            if tp.translated_protected_text is None:
                all_parts_ok = False
                break
                
            restored_zh = restore_tags(tp.translated_protected_text, tp.mapping)
            lead_space = tp.original_part_en[:len(tp.original_part_en) - len(tp.original_part_en.lstrip())]
            trail_space = tp.original_part_en[len(tp.original_part_en.rstrip()):]
            
            final_parts_zh.append(lead_space + restored_zh + trail_space)
            
        if all_parts_ok:
            en_to_final_zh[st.original_en] = "|".join(final_parts_zh)
        else:
            en_to_final_zh[st.original_en] = None

    # 9. 修改并写入文件
    for file_path, file_lines, file_dialogues in [
        (FILE_1, lines1, dialogues1),
        (FILE_2, lines2, dialogues2)
    ]:
        modified_count = 0
        backup_path = file_path + ".bak"
        with open(backup_path, 'w', encoding='utf-8') as bf:
            bf.writelines(file_lines)
        print(f"已创建原文件备份: {backup_path}")
        
        for entry in file_dialogues:
            en = entry['en']
            line_idx = entry['line_idx']
            speaker = entry['speaker']
            
            final_zh = en_to_final_zh.get(en)
            if final_zh is not None:
                final_zh = inspect_and_fix(final_zh, speaker)
                
                old_line = file_lines[line_idx]
                indent = old_line[:len(old_line) - len(old_line.lstrip())]
                escaped_zh = final_zh.replace('"', '\\"')
                
                if speaker:
                    new_line = f'{indent}{speaker} "{escaped_zh}"\n'
                else:
                    new_line = f'{indent}"{escaped_zh}"\n'
                    
                file_lines[line_idx] = new_line
                modified_count += 1
                
        with open(file_path, 'w', encoding='utf-8') as f:
            f.writelines(file_lines)
        print(f"修改写入成功。文件: {file_path}，已修改 {modified_count} 行对白。")

    print("\n==============================================")
    print("AI 精细重译与润色流程执行完毕！")
    print("==============================================")

if __name__ == '__main__':
    main()
