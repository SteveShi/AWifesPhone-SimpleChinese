#!/usr/bin/env python3
import json

CACHE_FILE = "/Users/steve/.gemini/antigravity/brain/691e26d2-a768-49c7-b653-dfedbdac50b9/scratch/translate_cache.json"

with open(CACHE_FILE, 'r', encoding='utf-8') as f:
    translate_cache = json.load(f)

# 模拟这一行的提取信息
line_idx = 75428
old_line = '    nvlsson "爸爸，您……人家不知道您是怎么做到的，可人家现在有女孩子的胸部了呢 {image=love_emoji.png}Dad, you... I don\'t know how you did, but I have a woman\'s breasts now {image=love_emoji.png}"\n'
en = "Dad, you... I don't know how you did, but I have a woman's breasts now {image=love_emoji.png}"
role_hint = "Edwin_Son_Mickey"
speaker = "nvlsson"

ck = f"{en}###{role_hint}"
cached_parts = translate_cache.get(ck)
print("Cache item found:", cached_parts is not None)

if cached_parts and isinstance(cached_parts, dict):
    parts = en.split('|')
    final_parts_zh = []
    all_parts_ok = True
    
    for p_idx, part in enumerate(parts):
        stripped = part.strip()
        print(f"part_idx={p_idx}, part={repr(part)}, stripped={repr(stripped)}")
        if not stripped:
            final_parts_zh.append(part)
            continue
        restored_zh = cached_parts.get(str(p_idx))
        print(f"restored_zh from cache: {repr(restored_zh)}")
        if restored_zh is None:
            all_parts_ok = False
            break
        lead_space = part[:len(part) - len(part.lstrip())]
        trail_space = part[len(part.rstrip()):]
        appended = lead_space + restored_zh + trail_space
        print(f"appended: {repr(appended)}")
        final_parts_zh.append(appended)
        
    if all_parts_ok:
        final_zh = "|".join(final_parts_zh)
        print(f"final_zh: {repr(final_zh)}")
        indent = old_line[:len(old_line) - len(old_line.lstrip())]
        escaped_zh = final_zh.replace('"', '\\"')
        if speaker:
            new_line = f'{indent}{speaker} "{escaped_zh}"\n'
        else:
            new_line = f'{indent}"{escaped_zh}"\n'
        
        print("Generated new_line:", repr(new_line))
        print("Does it contain English?", "breasts" in new_line)
