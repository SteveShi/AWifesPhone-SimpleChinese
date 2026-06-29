#!/usr/bin/env python3
import os

# ==================== 配置 ====================
TRANSLATIONS = {
    # 1. new_main_wife_phone_0_2.rpy
    "/Users/steve/Documents/翻译项目/AWifesPhoneEP1/AWifesPhone_CN_Backup/game/tl/zh_Hans/new_main_wife_phone_0_2.rpy": {
        'old "Continue chatting"': '    new "继续聊聊"',
        'old "Agree to come over"': '    new "同意过来"'
    },
    # 2. new_christmass_phone_0_2.rpy
    "/Users/steve/Documents/翻译项目/AWifesPhoneEP1/AWifesPhone_CN_Backup/game/tl/zh_Hans/xmas content/new_christmass_phone_0_2.rpy": {
        'old "Let\'s visit your sister (MC+Wife Sis content)"': '    new "我们去拜访你妹妹（主角+小姨子剧情）"',
        'old "Let\'s stay home (MC+Wife content/MC\'s Mum content)"': '    new "我们留在家里（主角+妻子/主角母亲剧情）"',
        'old "Let\'s join my son and his friends (Son+Wife or Fem Son content)"': '    new "我们和儿子及他的朋友们聚聚（儿子+妻子或女性化儿子剧情）"',
        'old "Go with Jenna (Wife BBC content)"': '    new "和珍娜一起去（妻子BBC剧情）"',
        'old "Let\'s visit my parents (MC+Wife content)"': '    new "我们去拜访我的父母（主角+妻子剧情）"',
        'old "{color=#000}{cps=+50}Was the son feminised?"': '    new "{color=#000}{cps=+50}儿子被女性化了吗？"',
        'old "{color=#000}{cps=+50}Would you like to see the other branches?"': '    new "{color=#000}{cps=+50}你想看看其他分支剧情吗？"'
    },
    # 3. common.rpy
    "/Users/steve/Documents/翻译项目/AWifesPhoneEP1/AWifesPhone_CN_Backup/game/tl/zh_Hans/common.rpy": {
        'old "Self-voicing would say \\"[renpy.display.tts.last]\\". Press \'alt+shift+V\' to disable."': '    new "系统自动朗读将读出 \\"[renpy.display.tts.last]\\\"。按 \'alt+shift+V\' 禁用。"',
        'old "An error has occured:"': '    new "发生了一个错误："',
        'old "An error occured when trying to download game data:"': '    new "尝试下载游戏数据时发生错误："',
        'old "Force GL Renderer"': '    new "强制使用 GL 渲染器"',
        'old "Force ANGLE Renderer"': '    new "强制使用 ANGLE 渲染器"',
        'old "Force GLES Renderer"': '    new "强制使用 GLES 渲染器"'
    },
    # 4. screens.rpy
    "/Users/steve/Documents/翻译项目/AWifesPhoneEP1/AWifesPhone_CN_Backup/game/tl/zh_Hans/screens.rpy": {
        'old "{size=54}Language"': '    new "{size=54}语言"'
    }
}

def main():
    print("开始针对第一部选项前纯英文 prompt 及选项文本进行就地汉化...")
    for fp, trans in TRANSLATIONS.items():
        if not os.path.exists(fp):
            print(f"[跳过] 文件不存在: {fp}")
            continue
            
        with open(fp, 'r', encoding='utf-8') as f:
            lines = f.readlines()
            
        modified = False
        for idx in range(len(lines)):
            line = lines[idx]
            for old_key, new_val in trans.items():
                # 判断当前行是否匹配 old_key 且下一行是对应的 new 英文行
                # 去除转义斜杠的影响再比对
                norm_line = line.replace('\\\'', "'").replace('\\"', '"')
                norm_key = old_key.replace('\\\'', "'").replace('\\"', '"')
                
                if norm_key in norm_line and idx + 1 < len(lines):
                    next_line = lines[idx+1]
                    # 只有在 new 包含 key 内容或者为原英文时才替换
                    raw_en = old_key.split('old "', 1)[-1].rstrip('"')
                    # 同样 normalization 排除斜杠干扰
                    norm_new = next_line.replace('\\\'', "'").replace('\\"', '"')
                    raw_en_norm = raw_en.replace('\\\'', "'").replace('\\"', '"')
                    
                    if "new " in next_line and 'new "' in next_line and raw_en_norm in norm_new:
                        print(f"正在修复 {os.path.basename(fp)} 第 {idx+2} 行:")
                        print(f"  原行: {repr(next_line)}")
                        print(f"  新行: {repr(new_val + '\n')}")
                        lines[idx+1] = new_val + '\n'
                        modified = True
                            
        if modified:
            with open(fp, 'w', encoding='utf-8') as f:
                f.writelines(lines)
            print(f"  [文件 {os.path.basename(fp)} 汉化成功]")
            
    print("选项前台词及选项汉化写入完成！")

if __name__ == "__main__":
    main()
