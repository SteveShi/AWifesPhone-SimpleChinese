# AWifesPhone 2 简体中文完美字体与彩色 Emoji 缝合配置

# 1. 声明官方默认语言为简体中文
define config.default_language = "zh_Hans"

init -3 python:
    # 2. 声明一个支持中文和彩色 Emoji 的缝合字体组
    zh_emoji_font = FontGroup()
    zh_emoji_font = zh_emoji_font.add("TwemojiCOLRv0.ttf", 0x1f000, 0x1faff)
    zh_emoji_font = zh_emoji_font.add("TwemojiCOLRv0.ttf", 0x2600, 0x27bf)
    zh_emoji_font = zh_emoji_font.add("TwemojiCOLRv0.ttf", 0x2300, 0x23ff)
    zh_emoji_font = zh_emoji_font.add("gui/fonts/Chinese.ttf", 0x0000, 0xffff)

# 3. 当语言为 zh_Hans 时，直接静态替换默认、对白和按钮的样式字体
translate zh_Hans style default:
    font zh_emoji_font

translate zh_Hans style say_dialogue:
    font zh_emoji_font

translate zh_Hans style nvl_dialogue:
    font zh_emoji_font

translate zh_Hans style button_text:
    font zh_emoji_font

translate zh_Hans style input:
    font zh_emoji_font

# 4. 拦截解决硬编码字体导致的豆腐块方框（使用合法的字符串路径，绝对不能传 FontGroup 对象）
init python:
    config.font_replacement_map["gui/TMR_Regular.ttf", False, False] = ("gui/fonts/Chinese.ttf", False, False)
    config.font_replacement_map["gui/TMR.ttf", False, False] = ("gui/fonts/Chinese.ttf", False, False)

# 5. 全局动态汉化拦截器（处理硬编码 UI 字符串及 Fuckstagram/Walkthrough 界面）
init 10 python:
    import json
    import os
    import re

    # 加载高品质汉化拦截词典
    global_translation_dict = {}
    try:
        json_path = os.path.join(config.gamedir, "tl", "zh_Hans", "strings.json")
        if os.path.exists(json_path):
            with open(json_path, "r", encoding="utf-8") as f:
                global_translation_dict = json.load(f)
    except Exception as e:
        pass

    # 刚性全局人名智能重映射（彻底汉化 WhatsApp/WifeSpy 中的各种英文名字）
    global_name_remap = {
        "kirely": "绮芮", "Kirely": "绮芮",
        "sola": "索拉", "Sola": "索拉",
        "hearth": "赫斯", "Hearth": "赫斯",
        "aria": "艾莉亚", "Aria": "艾莉亚",
        "julia": "朱莉娅", "Julia": "朱莉娅",
        "helsa": "海尔莎", "Helsa": "海尔莎",
        "chee": "阿琦", "Chee": "阿琦",
        "dani": "丹妮", "Dani": "丹妮",
        "gianna": "吉安娜", "Gianna": "吉安娜",
        "paloma": "帕洛玛", "Paloma": "帕洛玛",
        "lera": "蕾拉", "Lera": "蕾拉",
        "jenna": "珍娜", "Jenna": "珍娜",
        "mike": "麦克", "Mike": "麦克",
        "george": "乔治", "George": "乔治",
        "christina": "克里斯蒂娜", "Christina": "克里斯蒂娜",
        "edwin": "埃德温", "Edwin": "埃德温",
        "talay": "塔莱", "Talay": "塔莱",
        "casey": "凯茜", "Casey": "凯茜",
        "steve": "轩楝", "Steve": "轩楝",
        "stefanie": "斯蒂芬妮", "Stefanie": "斯蒂芬妮",
        "steph": "斯蒂芬", "Steph": "斯蒂芬",
        "john": "约翰", "John": "约翰",
        "paul": "保罗", "Paul": "保罗",
        "paula": "保拉", "Paula": "保拉",
        "carl": "卡尔", "Carl": "卡尔",
        "ashley": "艾希莉", "Ashley": "艾希莉",
        "ann": "安", "Ann": "安",
        "amelia": "阿米莉亚", "Amelia": "阿米莉亚",
        "eva": "艾娃", "Eva": "艾娃",
        "dave": "戴夫", "Dave": "戴夫",
        "jessica": "杰西卡", "Jessica": "杰西卡",
        "jack": "杰克", "Jack": "杰克",
        "iris": "艾莉丝", "Iris": "艾莉丝",
        "tyrone": "泰隆", "Tyrone": "泰隆",
        "dad": "爸爸", "Dad": "爸爸",
        "mom": "妈妈", "Mom": "妈妈",
        "jasmin": "贾斯敏", "Jasmin": "贾斯敏",
        "natasha": "娜塔莎", "Natasha": "娜塔莎",
        "wilson": "威尔逊", "Wilson": "威尔逊",
        "edgar": "埃德加", "Edgar": "埃德加",
        "doug": "道格", "Doug": "道格",
        "damian": "达米安", "Damian": "达米安",
        "enrico": "恩里克", "Enrico": "恩里克",
        "sheldon": "谢尔顿", "Sheldon": "谢尔顿",
        "ryan": "赖安", "Ryan": "赖安",
        "jolene": "乔琳", "Jolene": "乔琳",
        "rosa": "罗莎", "Rosa": "罗莎",
        "norman": "诺曼", "Norman": "诺曼",
        "mark": "马克", "Mark": "马克",
        "jacob": "雅各布", "Jacob": "雅各布",
        "danny": "丹尼", "Danny": "丹尼",
        "kevin": "凯文", "Kevin": "凯文",
        "bubba": "布巴", "Bubba": "布巴",
        "hugo": "雨果", "Hugo": "雨果",
        "linda": "琳达", "Linda": "琳达",
        "anna": "安娜", "Anna": "安娜",
    }

    # 攻略静态短语字典
    walkthrough_vocab = {
        "This is the end of the current content": "当前内容已结束",
        "Finish branch": "完成分支",
        "condition:": "条件:",
        "Find Lera in M&F and like her": "在约炮软件中找到蕾拉并选择喜欢她",
        "Find Chee in M&F and like her": "在约炮软件中找到阿琦并选择喜欢她",
        "Find Gianna in M&F and like her": "在约炮软件中找到吉安娜并选择喜欢她",
        "Find Dani in M&F and like her": "在约炮软件中找到丹妮并选择喜欢她",
        "Find Rick in M&F and like her": "在约炮软件中找到里克并选择喜欢他",
        "Find Roby in M&F and like him": "在约炮软件中找到罗比并选择喜欢他",
        "Find a new couple in M&F": "在约炮软件中找到新伴侣",
        "Buy a business in the StarTaxi app": "在 StarTaxi 应用中购买业务",
        "Choose the son as your target in WifeSpy in v0.15": "在 v0.15 的 WifeSpy 中选择儿子作为目标",
        "Increase StarTaxi’s prestige in the app": "在应用中提高 StarTaxi 的声望",
        "Jenna was added to WifeSpy": "珍娜已添加到 WifeSpy",
        "Kioko was added to WifeSpy": "京子已添加到 WifeSpy",
        "Kirely's income is more than $9,000": "绮芮的收入超过 $9,000",
        "Mark was added to WifeSpy and command issued in the WifeSpy app": "马克已被添加到 WifeSpy 且在应用中下达了指令",
        "Mike was added to WifeSpy": "麦克已添加到 WifeSpy",
        "Mrs Salim was added to WifeSpy": "萨利姆夫人已添加到 WifeSpy",
        "Onlyfaps installed": "已安装 OnlyFaps",
        "Say hello to her in the shop in v0.15": "在 v0.15 的商店里和她打个招呼",
        "Talay added to the WifeSpy app": "塔莱已添加到 WifeSpy 应用",
        "[niece_name_is] added to the WifeSpy app": "[niece_name_is] 已添加到 WifeSpy 应用",
        "a couple found on M&F": "在 M&F 上找到了一对情侣",
        "a few BBC hypno-spam messages in the WifeSpy app": "WifeSpy 应用中收到几条 BBC 催眠垃圾短信",
        "a few hypno-spam messages": "收到几条催眠垃圾短信",
        "a house has been purchased through the RE app": "已通过 RE 房产应用购买房屋",
        "after a few hypno-spam messages": "在收到几条催眠垃圾短信之后",
        "all of Kirely's photos and videos uploaded to Onlyfaps": "绮芮的所有照片与视频都已上传到 OnlyFaps",
        "all of Niece's photos and videos uploaded to Onlyfaps": "[niece_name_is] 的所有照片与视频都已上传到 OnlyFaps",
        "all of Sola's photos and videos uploaded to Onlyfaps": "索拉的所有照片与视频都已上传到 OnlyFaps",
        "all of Sola's photos and videos uploaded to Onlyfaps and her income is more than $10,000": "索拉的所有照片视频已上传且其收入超过 $10,000",
        "all of Sola's photos and videos uploaded to Onlyfaps and her income is more than $4,000": "索拉的所有照片视频已上传且其收入超过 $4,000",
        "all of Sola's photos and videos uploaded to Onlyfaps and her income is more than $6,000": "索拉的所有照片视频已上传且其收入超过 $6,000",
        "all of Sola's photos and videos uploaded to Onlyfaps and her income is more than $9,000": "索拉的所有照片视频已上传且其收入超过 $9,000",
        "all of Wife's photos and videos uploaded to Onlyfaps": "妻子的所有照片与视频都已上传到 OnlyFaps",
        "all the photos and videos uploaded to Onlyfaps": "所有照片与视频都已上传到 OnlyFaps",
        "check the son's fuckstagram": "查看儿子的 Fuckstagram",
        "check user profiles on M&F": "在 M&F 上查看用户资料",
        "command issued in the WifeSpy app": "在 WifeSpy 应用中已下达指令",
        "commanded to be more feminine": "已被命令要求表现得更加女性化",
        "conversation with the husband / command issued in the WifeSpy app": "与丈夫交谈 / 在 WifeSpy 应用中下达指令",
        "daytime": "白天",
        "daytime & all of Wife's photos and videos uploaded to Onlyfaps": "白天 & 妻子的所有照片视频都已上传到 OnlyFaps",
        "daytime and command issued in the WifeSpy app": "白天且已在 WifeSpy 应用中下达指令",
        "daytime and sending out the sissy spam": "白天且已发送娘炮垃圾短信",
        "logged in to Sola's profile and uploaded photos": "已登录索拉的个人主页并上传了照片",
        "night": "夜晚",
        "night and command issued in the WifeSpy app": "夜晚且已在 WifeSpy 应用中下达指令",
        "publish two posts to Cecilia’s OnlyFaps": "向塞西莉亚的 OnlyFaps 发布两篇帖子",
        "sending out the sissy spam": "发送娘炮垃圾短信",
        "the MC started a new company": "主角开创了一家新公司",
        "the husband created an M&F account for his wife": "丈夫为妻子创建了 M&F 账号",
        "the son isn't feminised & step 13 in the brach of the wife and Greg is complete": "儿子尚未女性化且妻子与格雷格的故事线已完成第13步",
        "the son isn't feminised": "儿子尚未女性化",
    }

    # 攻略分支名完整翻译词典
    branch_names = {
        "Haley's branch": "海莉的故事线",
        "Fem Mark's branch": "马克女性化故事线",
        "Lera's branch": "蕾拉的故事线",
        "Chee's branch": "阿琦的故事线",
        "Gianna's branch (Alpha)": "吉安娜故事线 (Alpha)",
        "Paloma's branch (Alpha)": "帕洛玛故事线 (Alpha)",
        "Dani's branch (Alpha)": "丹妮故事线 (Alpha)",
        "Hearth's branch": "赫斯的故事线",
        "Aria's branch": "艾莉亚的故事线",
        "Kirely's branch": "绮芮的故事线",
        "Julia's romance branch": "珍妮特/朱莉娅罗曼史故事线",
        "[d_name_is]'s branch": "[d_name_is]的故事线",
        "[niece_name_is]'s romance branch": "[niece_name_is]的罗曼史故事线",
        "The branch of the MC and Sola": "主角与索拉的故事线",
        "The branch of the MC and StarTaxi business": "主角与 StarTaxi 业务的故事线",
        "The branch of Cecilia and the MC": "塞西莉亚与主角的故事线",
        "The branch of Christina and BBC": "克里斯蒂娜与 BBC 的故事线",
        "The branch of Christina and the husband": "克里斯蒂娜与丈夫的故事线",
        "The branch of Mum": "妈妈的故事线",
        "The branch of Talay and Cecilia": "塔莱与塞西莉亚的故事线",
        "The branch of Talay and Mr Salim": "塔莱与萨利姆先生的故事线",
        "The branch of Talay and the MC": "塔莱与主角的故事线",
        "The branch of Talay and the MC (corrupted)": "塔莱与主角的故事线 (堕落)",
        "The branch of [stepsis_name_is] and Jenna": "[stepsis_name_is]与珍娜的故事线",
        "The branch of [stepsis_name_is] and Joshua": "[stepsis_name_is]与约书亚的故事线",
        "The branch of [stepsis_name_is] and Mark": "[stepsis_name_is]与马克的故事线",
        "The branch of [stepsis_name_is] and the husband": "[stepsis_name_is]与丈夫的故事线",
        "The branch of [stepsis_name_is] and the neighbour": "[stepsis_name_is]与邻居的故事线",
        "The branch of [wife_name_is] and Christina": "[wife_name_is]与克里斯蒂娜的故事线",
        "The branch of [wife_name_is] and Eric (the colleague)": "[wife_name_is]与埃里克 (同事) 的故事线",
        "The branch of [wife_name_is] and Eric (the student)": "[wife_name_is]与埃里克 (学生) 的故事线",
        "The branch of [wife_name_is] and Greg": "[wife_name_is]与格雷格的故事线",
        "The branch of [wife_name_is] and Jenna": "[wife_name_is]与珍娜的故事线",
        "The branch of [wife_name_is] and her job": "[wife_name_is]与她的工作的故事线",
        "The branch of [wife_name_is] and sharing": "[wife_name_is]与分享的故事线",
        "The branch of [wife_name_is] and the MC (Femdom)": "[wife_name_is]与主角的故事线 (女王路径)",
        "The branch of [wife_name_is] and the QOS chat": "[wife_name_is]与 QOS 聊天的故事线",
        "The branch of [wife_name_is] and the brother (Mark)": "[wife_name_is]与兄弟 (马克) 的故事线",
        "The branch of [wife_name_is] and the brother (Mark) cuckold path": "[wife_name_is]与兄弟 (马克) 故事线 (绿帽路径)",
        "The branch of [wife_name_is] and the fuckstagram": "[wife_name_is]与 Fuckstagram 故事线",
        "The branch of [wife_name_is] and the son": "[wife_name_is]与儿子的故事线",
        "The branch of [wife_name_is]'s random events #1": "[wife_name_is]的随机事件 #1",
        "The branch of [wsis_name_is] and Steph": "[wsis_name_is]与斯蒂芬的故事线",
        "The branch of [wsis_name_is] and her boss": "[wsis_name_is]与老板的故事线",
        "The branch of [wsis_name_is] and the husband": "[wsis_name_is]与丈夫的故事线",
        "The branch of the MC and Henrique": "主角与恩里克的故事线",
        "The branch of the sissy son and Greg": "伪娘儿子与格雷格的故事线",
        "The branch of the son and Ahat": "儿子与阿哈特的故事线",
        "The branch of the wife and the MC's company": "妻子与主角公司的故事线",
        "The son's feminisation branch": "儿子的女性化故事线",
    }

    # 简易英文分段处理辅助替换
    simple_replacements = {
        "and": "且",
        "is complete": "已完成",
        "are complete": "已完成",
        "in the branch of": "在故事线",
        "in the brach of": "在故事线",  # 原版游戏中的拼写错误 brach
        "Sola's branch": "索拉故事线",
        "the son's feminisation branch": "儿子的女性化故事线",
        "the modelling branch": "模特故事线",
        "the branch of": "故事线",
    }

    def clean_text(t):
        if not t:
            return ""
        t = t.replace("\\'", "'").replace("\\\"", "\"").replace("’", "'").replace("“", "\"").replace("”", "\"")
        return t.strip()

    clean_translation_dict = {clean_text(k): v for k, v in global_translation_dict.items()}

    def custom_translation_filter(text):
        if renpy.game.preferences.language != "zh_Hans":
            return text

        # 1. 精确匹配
        if text in global_translation_dict:
            return global_translation_dict[text]

        # 2. 模糊匹配
        cleaned = clean_text(text)
        if cleaned in clean_translation_dict:
            return clean_translation_dict[cleaned]

        # 3. 动态角色名字智能修正映射
        if text in global_name_remap:
            return global_name_remap[text]

        # 4. 动态攻略（Walkthrough）正则匹配翻译
        if "Step " in text and "Wait " in text:
            t_fixed = text
            t_fixed = re.sub(r'Step\s+(\d+)\.', r'步骤 \1.', t_fixed)
            t_fixed = re.sub(r'Wait\s+(\d+)\s+days\.?', r'等待 \1 天。', t_fixed)
            
            t_fixed = t_fixed.replace("Switch to the son's/wife's phone", "切换到儿子/妻子的手机")
            t_fixed = t_fixed.replace("Switch to the wife's phone", "切换到妻子的手机")
            t_fixed = t_fixed.replace("Switch to the son's phone", "切换到儿子的手机")
            t_fixed = t_fixed.replace("Text your son", "给儿子发短信")
            t_fixed = t_fixed.replace("Progress ALL THE OTHER branches OF ALL THE CHARACTERS", "推进所有其他角色的所有故事线")
            
            for eng, zhs in walkthrough_vocab.items():
                t_fixed = t_fixed.replace(eng, zhs)
            
            m_cond = re.search(r'\(condition:\s*(.*?)\)', t_fixed)
            if m_cond:
                orig_cond = m_cond.group(1)
                cond_fixed = orig_cond
                for eng, zhs in simple_replacements.items():
                    cond_fixed = cond_fixed.replace(eng, zhs)
                for eng_b, zhs_b in branch_names.items():
                    b_pure = eng_b.replace("The branch of ", "").replace("'s branch", "")
                    cond_fixed = cond_fixed.replace(b_pure, zhs_b)
                t_fixed = t_fixed.replace(orig_cond, cond_fixed)

            return t_fixed

        # 5. 动态分支标题翻译
        if text in branch_names:
            return branch_names[text]

        clean_branch = re.sub(r'\{[^}]+\}', '', text).strip()
        if clean_branch in branch_names:
            return branch_names[clean_branch]

        return text

    # 将拦截器绑定到引擎渲染总管道上
    config.replace_text = custom_translation_filter

# 6. 安全劫持：在游戏加载完毕、闪屏播放阶段执行一次语言纠正，安全无崩！
label splashscreen:
    python:
        if _preferences.language in [None, "", "zh_anubisbr"]:
            renpy.change_language("zh_Hans")
    return
