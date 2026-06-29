#!/usr/bin/env python3
import re

lines = open('/Users/steve/Documents/翻译项目/AWifesPhoneEP1/AWifesPhone_CN_Backup/game/tl/zh_Hans/new_main_son_phone_0_2.rpy').readlines()
pattern_spk_id = re.compile(r'^\s*([a-zA-Z0-9_]+)\s*"((?:[^"\\]|\\.)*)"\s*$')

line = lines[75428]
print('Original Line:', repr(line))
m = pattern_spk_id.match(line)
if m:
    print('Match Group 1 (spk):', repr(m.group(1)))
    print('Match Group 2 (zh):', repr(m.group(2)))
else:
    print('No match!')
