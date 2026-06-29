#!/usr/bin/env python3
import json

CACHE_FILE = "/Users/steve/.gemini/antigravity/brain/691e26d2-a768-49c7-b653-dfedbdac50b9/scratch/translate_cache.json"

with open(CACHE_FILE, 'r', encoding='utf-8') as f:
    translate_cache = json.load(f)

en = "Dad, you... I don't know how you did, but I have a woman's breasts now {image=love_emoji.png}"
role_hint = "Edwin_Son_Mickey"
ck = f"{en}###{role_hint}"

val = translate_cache.get(ck)
print("Type of val:", type(val))
print("Content of val:", repr(val))
