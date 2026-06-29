# AWifesPhone EP1 简体中文完美字体覆盖

translate zh_Hans style default:
    font "gui/chinese.ttf"

translate zh_Hans style button_text:
    font "gui/chinese.ttf"

# 覆盖选项按钮的文字样式，彻底解决绿色按钮方框问题
translate zh_Hans style choice_button_text:
    font "gui/chinese.ttf"

translate zh_Hans style input:
    font "gui/chinese.ttf"

# 解决第一部硬编码字体导致的方框
init python:
    config.font_replacement_map["gui/TMR_Regular.ttf", False, False] = ("gui/chinese.ttf", False, False)
    config.font_replacement_map["gui/TMR.ttf", False, False] = ("gui/chinese.ttf", False, False)
