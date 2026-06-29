################################################################################
## Initialization
################################################################################

init offset = -1


################################################################################
## Styles
################################################################################

init -10 python:
    
    def keyboard_sound(event, interact=True, **kwargs):
        if not interact:
            return

        if event == "show_done":
            renpy.sound.play("sound/keyboard.mp3")
        elif event == "slow_done":
            renpy.sound.stop()

    def new_msg(event, interact=True, **kwargs):
        if not interact:
            return

        if event == "begin":
            renpy.sound.play("sound/new_msg.mp3")
        elif event == "end":
            renpy.sound.stop()

    renpy.music.register_channel("moans", "voice", False)

    renpy.music.set_volume(1.0, delay=0, channel='moans')

    renpy.music.set_volume(1.0, delay=0, channel='music')







style default:
    properties gui.text_properties()
    language gui.language

style input:
    properties gui.text_properties("input", accent=True)
    adjust_spacing False

style hyperlink_text:
    color "#ff7700"
    hover_color "#ff0"
    size 46
    font "gui/TMR_Regular.ttf"
    hover_underline True

style gui_text:
    properties gui.text_properties("interface")



# Задание звуков для всех imagebutton
init python:
    style.image_button.hover_sound = "audio/hover.mp3"
    style.image_button.activate_sound = "audio/click.mp3"



style button:
    hover_sound "audio/hover.mp3"   # Звук при наведении на кнопку
    activate_sound "audio/click.mp3"  # Звук при нажатии на кнопку
    properties gui.button_properties("button")




style button_text is gui_text:
    properties gui.text_properties("button")
    yalign 0.5


style label_text is gui_text:
    properties gui.text_properties("label", accent=True)

style prompt_text is gui_text:
    properties gui.text_properties("prompt")


style bar:
    ysize gui.bar_size
    left_bar Frame("gui/bar/left.png", gui.bar_borders, tile=gui.bar_tile)
    right_bar Frame("gui/bar/right.png", gui.bar_borders, tile=gui.bar_tile)

style vbar:
    xsize gui.bar_size
    top_bar Frame("gui/bar/top.png", gui.vbar_borders, tile=gui.bar_tile)
    bottom_bar Frame("gui/bar/bottom.png", gui.vbar_borders, tile=gui.bar_tile)

style scrollbar:
    ysize gui.scrollbar_size
    base_bar Frame("gui/scrollbar/horizontal_[prefix_]bar.png", gui.scrollbar_borders, tile=gui.scrollbar_tile)
    thumb Frame("gui/scrollbar/horizontal_[prefix_]thumb.png", gui.scrollbar_borders, tile=gui.scrollbar_tile)

style vscrollbar:
    xsize gui.scrollbar_size
    base_bar Frame("gui/scrollbar/vertical_[prefix_]bar.png", gui.vscrollbar_borders, tile=gui.scrollbar_tile)
    thumb Frame("gui/scrollbar/vertical_[prefix_]thumb.png", gui.vscrollbar_borders, tile=gui.scrollbar_tile)

style slider:
    ysize gui.slider_size
    base_bar Frame("gui/slider/horizontal_[prefix_]bar.png", gui.slider_borders, tile=gui.slider_tile)
    thumb "gui/slider/horizontal_[prefix_]thumb.png"

style vslider:
    xsize gui.slider_size
    base_bar Frame("gui/slider/vertical_[prefix_]bar.png", gui.vslider_borders, tile=gui.slider_tile)
    thumb "gui/slider/vertical_[prefix_]thumb.png"


style frame:
    padding gui.frame_borders.padding
    background Frame("gui/frame.png", gui.frame_borders, tile=gui.frame_tile)



################################################################################
## In-game screens
################################################################################


## Say screen ##################################################################
##
## The say screen is used to display dialogue to the player. It takes two
## parameters, who and what, which are the name of the speaking character and
## the text to be displayed, respectively. (The who parameter can be None if no
## name is given.)
##
## This screen must create a text displayable with id "what", as Ren'Py uses
## this to manage text display. It can also create displayables with id "who"
## and id "window" to apply style properties.
##
## https://www.renpy.org/doc/html/screen_special.html#say

screen say(who, what):

    window:
        id "window"

        if who is not None:

            window:
                id "namebox"
                style "namebox"
                text who id "who"

        text what id "what"


    ## If there's a side image, display it above the text. Do not display on the
    ## phone variant - there's no room.
    if not renpy.variant("small"):
        add SideImage() xalign 0.0 yalign 1.0


## Make the namebox available for styling through the Character object.
init python:
    config.character_id_prefixes.append('namebox')

style window is default
style say_label is default
style say_dialogue is default
style say_thought is say_dialogue

style namebox is default
style namebox_label is say_label


style window:
    xalign 0.5
    xfill True
    yalign gui.textbox_yalign
    ysize gui.textbox_height

    background Image("gui/textbox.png", xalign=0.5, yalign=1.0)

style namebox:
    xpos gui.name_xpos
    xanchor gui.name_xalign
    xsize gui.namebox_width
    ypos gui.name_ypos
    ysize gui.namebox_height

    background Frame("gui/namebox.png", gui.namebox_borders, tile=gui.namebox_tile, xalign=gui.name_xalign)
    padding gui.namebox_borders.padding

style say_label:
    properties gui.text_properties("name", accent=True)
    xalign gui.name_xalign
    yalign 0.5

style say_dialogue:
    properties gui.text_properties("dialogue")

    xpos gui.dialogue_xpos
    xsize gui.dialogue_width
    ypos gui.dialogue_ypos

    adjust_spacing False

## Input screen ################################################################
##
## This screen is used to display renpy.input. The prompt parameter is used to
## pass a text prompt in.
##
## This screen must create an input displayable with id "input" to accept the
## various input parameters.
##
## https://www.renpy.org/doc/html/screen_special.html#input

screen input(prompt):
    style_prefix "input"

    window:

        vbox:
            xanchor gui.dialogue_text_xalign
            xpos gui.dialogue_xpos
            xsize gui.dialogue_width
            ypos gui.dialogue_ypos

            text prompt style "input_prompt"
            input id "input"

style input_prompt is default

style input_prompt:
    xalign gui.dialogue_text_xalign
    properties gui.text_properties("input_prompt")

style input:
    xalign gui.dialogue_text_xalign
    xmaximum gui.dialogue_width


## Choice screen ###############################################################
##
## This screen is used to display the in-game choices presented by the menu
## statement. The one parameter, items, is a list of objects, each with caption
## and action fields.
##
## https://www.renpy.org/doc/html/screen_special.html#choice


screen choice(items):
    style_prefix "choice"

    vbox:
        for i in items:
            textbutton i.caption action i.action
            if items.index(i) == 0:
                key "K_1":
                    action i.action
            elif items.index(i) == 1:
                key "K_2":
                    action i.action
            elif items.index(i) == 2:
                key "K_3":
                    action i.action
            elif items.index(i) == 3:
                key "K_4":
                    action i.action
            elif items.index(i) == 4:
                key "K_5":
                    action i.action
    

style choice_vbox is vbox
style choice_button is button
style choice_button_text is button_text

style choice_vbox:
    xalign 0.5
    yalign 0.67
    yanchor 0.5

    spacing gui.choice_spacing

style choice_button is default:
    properties gui.button_properties("choice_button")

style choice_button_text is default:
    properties gui.text_properties("choice_button")


## Quick Menu screen ###########################################################
##
## The quick menu is displayed in-game to provide easy access to the out-of-game
## menus.

screen quick_menu():

    ## Ensure this appears on top of other screens.
    zorder 100

    if quick_menu:

        hbox:

            spacing 20

            style_prefix "quick"

            xalign 0.5
            yalign 0.985
            
            textbutton _("Back") action Rollback() text_color '#ff007e' text_hover_color '#0066cc' text_size 42
            textbutton _("Skip") action Skip() alternate Skip(fast=True, confirm=True) text_color '#ff007e' text_hover_color '#0066cc' text_size 42
            textbutton _("Auto") action Preference("auto-forward", "toggle") text_color '#ff007e' text_hover_color '#0066cc' text_size 42
            textbutton _("Save") action ShowMenu('save') text_color '#ff007e' text_hover_color '#0066cc' text_size 42
            textbutton _("Prefs") action ShowMenu('preferences') text_color '#ff007e' text_hover_color '#0066cc' text_size 42


## This code ensures that the quick_menu screen is displayed in-game, whenever
## the player has not explicitly hidden the interface.
init python:
    config.overlay_screens.append("quick_menu")

default quick_menu = False

style quick_button is default
style quick_button_text is button_text

style quick_button:
    properties gui.button_properties("quick_button")

style quick_button_text:
    properties gui.text_properties("quick_button")


################################################################################
## Main and Game Menu Screens
################################################################################

## Navigation screen ###########################################################
##
## This screen is included in the main and game menus, and provides navigation
## to other menus, and to start the game.

screen navigation():

    vbox:
        style "main_menu_vbox"

        if main_menu:
            yalign 0.82 # Ici pour le menu principal, 0.81 pour apk, 0.92 pour pc
            xalign 0.5
        else:
            xalign 0.5
            yalign 0.972


        spacing gui.navigation_spacing

        if main_menu:
            pass


        else:

            textbutton _("Save") action ShowMenu("save") align (0.5, 0.5) 

            textbutton _("Load")  action ShowMenu("load") align (0.5, 0.5) 

            textbutton _("Settings") action ShowMenu("preferences") align (0.5, 0.5) 

        if _in_replay:

            textbutton _("End Replay") action EndReplay(confirm=True) align (0.5, 0.5) 

        elif not main_menu:

            textbutton _("Main Menu") action MainMenu() align (0.5, 0.5) 

        #textbutton _("About") action ShowMenu("about")





style navigation_button is gui_button
style navigation_button_text is gui_button_text

style navigation_button:
    size_group "navigation"
    properties gui.button_properties("navigation_button")

style navigation_button_text:
    properties gui.text_properties("navigation_button")


## Main Menu screen ############################################################
##
## Used to display the main menu when Ren'Py starts.
##
## https://www.renpy.org/doc/html/screen_special.html#main-menu

screen main_menu():

    ## This ensures that any other menu screen is replaced.
    tag menu

    add gui.main_menu_background

    ## This empty frame darkens the main menu.
    frame:
        style "main_menu_frame"

    ## The use statement includes another screen inside this one. The actual
    ## contents of the main menu are in the navigation screen.
    use navigation

    hbox yalign 0.85 xalign 0.5:
        spacing 30

        #text "For Support ->" size 72 ypos 30 outlines [(0.1, "#000")]

        imagebutton:
            idle "gui/ss.png" 
            hover "gui/ss_h.png" 
            action OpenURL("https://scyxar.com/")

        
        imagebutton:
            idle "gui/boosty.png" 
            hover "gui/boosty_h.png" 
            action OpenURL("https://boosty.to/bloody_ink")


        # imagebutton:
        #     idle "gui/subscr.png" 
        #     hover "gui/subscr_h.png" 
        #     action OpenURL("https://subscribestar.adult/bloody-ink")
            

        imagebutton:
            idle "gui/patreon.png" 
            hover "gui/patreon_h.png" 
            action OpenURL("https://www.patreon.com/ScyxarStudios")
            

        imagebutton:
            idle "gui/discord.png" 
            hover "gui/discord_h.png" 
            action OpenURL("https://discord.gg/H9rJWfQ4jf")

        

    vbox yalign 0.7 xalign 0.5:
        
        spacing 20
            
        textbutton _("Unlock"): 
            
            action Start() align (0.5, 0.5) text_size 82 text_outlines [(0.1, "#000")]

        textbutton _("Load")  action ShowMenu("load") align (0.5, 0.5)  text_size 82 text_outlines [(0.1, "#000")]

        textbutton _("Actresses")  action Show("model_list") align (0.5, 0.5)  text_size 82 text_outlines [(0.1, "#000")]
        
        textbutton _("Settings") action ShowMenu("preferences") align (0.5, 0.5) text_size 82 text_outlines [(0.1, "#000")]
        
        textbutton _("Quit")  action Quit(confirm=not main_menu) align (0.5, 0.5) text_size 82 text_outlines [(0.1, "#000")]

    if gui.show_name:

        vbox:
            style "main_menu_vbox"

            text "[config.name!t]":
                style "main_menu_title"

            text "[config.version]":
                style "main_menu_version"



style main_menu_frame is empty
style main_menu_vbox is vbox
style main_menu_text is gui_text
style main_menu_title is main_menu_text
style main_menu_version is main_menu_text

style main_menu_frame:
    xsize 420
    yfill True

    background "gui/overlay/main_menu.png"

style main_menu_vbox:
    xalign 1.0
    xoffset -11
    xmaximum 450
    yalign 1.0
    yoffset -11

style main_menu_text:
    properties gui.text_properties("main_menu", accent=True)

style main_menu_title:
    properties gui.text_properties("title")

style main_menu_version:
    properties gui.text_properties("version")


## Game Menu screen ############################################################
##
## This lays out the basic common structure of a game menu screen. It's called
## with the screen title, and displays the background, title, and navigation.
##
## The scroll parameter can be None, or one of "viewport" or "vpgrid".
## This screen is intended to be used with one or more children, which are
## transcluded (placed) inside it.

screen game_menu(title, scroll=None, yinitial=0.0, spacing=0):

    style_prefix "game_menu"

    if main_menu:
        add gui.main_menu_background
    else:
        add gui.game_menu_background

    frame:
        style "game_menu_outer_frame"

        hbox:

            ## Reserve space for the navigation section.
            frame:
                style "game_menu_navigation_frame"

            frame:
                style "game_menu_content_frame"

                if scroll == "viewport":

                    viewport:
                        yinitial yinitial
                        scrollbars "vertical"
                        mousewheel True
                        draggable True
                        pagekeys True

                        side_yfill True

                        vbox:
                            spacing spacing

                            transclude

                elif scroll == "vpgrid":

                    vpgrid:
                        cols 1
                        yinitial yinitial

                        scrollbars "vertical"
                        mousewheel True
                        draggable True
                        pagekeys True

                        side_yfill True

                        spacing spacing

                        transclude

                else:

                    transclude

    use navigation

    textbutton _("Return") xpos 50 yalign 0.99:
        style "return_button"

        action Return()

    label title

    if main_menu:
        key "game_menu" action ShowMenu("main_menu")


style game_menu_outer_frame is empty
style game_menu_navigation_frame is empty
style game_menu_content_frame is empty
style game_menu_viewport is gui_viewport
style game_menu_side is gui_side
style game_menu_scrollbar is gui_vscrollbar

style game_menu_label is gui_label
style game_menu_label_text is gui_label_text

style return_button is navigation_button
style return_button_text is navigation_button_text

style game_menu_outer_frame:
    bottom_padding 45
    top_padding 180

    background "gui/overlay/game_menu.png"


#не исправлял

style game_menu_navigation_frame:
    xsize 158
    yfill True

style game_menu_content_frame:
    left_margin 23
    right_margin 12
    top_margin 6

style game_menu_viewport:
    xsize 518

style game_menu_vscrollbar:
    unscrollable gui.unscrollable

style game_menu_side:
    spacing 6

style game_menu_label:
    xpos 29
    ysize 68

style game_menu_label_text:
    size gui.title_text_size
    color gui.accent_color
    yalign 0.5

style return_button:
    xpos 40
    yalign 1.0
    yoffset -40


## About screen ################################################################
##
## This screen gives credit and copyright information about the game and Ren'Py.
##
## There's nothing special about this screen, and hence it also serves as an
## example of how to make a custom screen.

screen about():

    tag menu

    ## This use statement includes the game_menu screen inside this one. The
    ## vbox child is then included inside the viewport inside the game_menu
    ## screen.
    use game_menu(_("About"), scroll="viewport"):

        style_prefix "about"

        vbox:

            label "[config.name!t]"
            text _("Version [config.version!t]\n")

            ## gui.about is usually set in options.rpy.
            if gui.about:
                text "[gui.about!t]\n"

            text _("Made with {a=https://www.renpy.org/}Ren'Py{/a} [renpy.version_only].\n\n[renpy.license!t]")


style about_label is gui_label
style about_label_text is gui_label_text
style about_text is gui_text

style about_label_text:
    size gui.label_text_size


## Load and Save screens #######################################################
##
## These screens are responsible for letting the player save the game and load
## it again. Since they share nearly everything in common, both are implemented
## in terms of a third screen, file_slots.
##
## https://www.renpy.org/doc/html/screen_special.html#save https://
## www.renpy.org/doc/html/screen_special.html#load

screen save():

    tag menu

    use file_slots(_("Save"))


screen load():

    tag menu

    use file_slots(_("Load"))


default save_slot_index = 0
default persistent.Giving_Name = 0


screen custom_save_give_name:
    modal True
    on "show" action SetVariable("save_name", "")
    add 'fon_img.png'
    vbox xalign 0.5 yalign 0.5:
        spacing 30
        text "Save Name: " size 52
        input color "#ffffff" size 52:
            value VariableInputValue('save_name')
    

        textbutton 'Save' xalign 0.5 yalign 0.56 action [FileSave(save_slot_index), Hide("custom_save_give_name")]






screen file_slots(title):

    
    default page_name_value = FilePageNameInputValue(pattern=_("Page {}"), auto=_("Automatic saves"), quick=_("Quick saves"))

    use game_menu(title):

        fixed xpos -100:

            ## This ensures the input will get the enter event before any of the
            ## buttons do.
            order_reverse True

            ## The page name, which can be edited by clicking on a button.

            
            hbox xpos -20 ypos -80:
                text "Name saves: " size 58
                style_prefix "radio"
                textbutton _("Yes") action SetVariable("persistent.Giving_Name", 1) text_size 58 ypos -4
                textbutton _("No") action SetVariable("persistent.Giving_Name", 0) text_size 58 ypos -4

            button:
                style "page_label"

                key_events True
                xpos 720
                ypos -80
                action page_name_value.Toggle()

                input:
                    style "page_label_text"
                    value page_name_value

            ## The grid of file slots.
            grid gui.file_slot_cols gui.file_slot_rows:
                style_prefix "slot"
                xalign 0.5
                yalign 0.05

                yspacing 120
                xspacing 80

                for i in range(gui.file_slot_cols * gui.file_slot_rows):

                    $ slot = i + 1

                    button:
                        
                        if persistent.Giving_Name == 0 or title == 'Load':
                            action [SetVariable("save_name", ""), FileAction(slot)]
                        else:
                            action [SetVariable("save_slot_index", slot), Show("custom_save_give_name")]


                        has vbox

                        add FileScreenshot(slot) xalign 0.5

                        text FileTime(slot, format=_("{size=28}{#file_time}%B %d, %H:%M"), empty=_("empty slot")):
                            style "slot_time_text"


                        text FileSaveName(slot):
                            style "slot_name_text"
                            

                        key "save_delete" action FileDelete(slot)
                    
                        


            ## Buttons to access other pages.
            hbox:
                style_prefix "page"

                xalign 0.6
                yalign 0.82

                spacing gui.page_spacing

                textbutton _("<") action FilePagePrevious()

                if config.has_autosave:
                    textbutton _("{#auto_page}A") action FilePage("auto")

                if config.has_quicksave:
                    textbutton _("{#quick_page}Q") action FilePage("quick")

                ## range(1, 10) gives the numbers from 1 to 9.
                for page in range(1, 8):
                    textbutton "[page]" action FilePage(page)

                textbutton _(">") action FilePageNext()


style page_label is gui_label
style page_label_text is gui_label_text
style page_button is gui_button
style page_button_text is gui_button_text

style slot_button is gui_button
style slot_button_text is gui_button_text
style slot_time_text is slot_button_text
style slot_name_text is slot_button_text



style page_label:
    xpadding 75
    ypadding 5

style page_label_text:
    textalign 0.5
    layout "subtitle"
    hover_color gui.hover_color

style page_button:
    properties gui.button_properties("page_button")

style page_button_text:
    properties gui.text_properties("page_button")

style slot_button:
    properties gui.button_properties("slot_button")

style slot_button_text:
    properties gui.text_properties("slot_button")


## Preferences screen ##########################################################
##
## The preferences screen allows the player to configure the game to better suit
## themselves.
##
## https://www.renpy.org/doc/html/screen_special.html#preferences

screen preferences():

    tag menu

    use game_menu(_("Preferences")):

        vbox xpos -110:
                ## Additional vboxes of type "radio_pref" or "check_pref" can be
                ## added here, to add additional creator-defined preferences.

            null height (8 * gui.pref_spacing)

            hbox:
                style_prefix "slider"
                box_wrap True


                vbox:

                    spacing 50

                    if config.has_music:
                        hbox:
                            label _("{size=54}Moans Volume")

                            
                            bar value Preference("music volume") xpos 20 ypos 15
                        

                    if config.has_sound:
                        hbox:
                            label _("{size=54}Sound Volume")

                            bar value Preference("sound volume") xpos 25 ypos 15

                                


                    if config.has_voice:
                        hbox:
                            label _("{size=54}Music Volume")

                            bar value Preference("voice volume") xpos 45 ypos 15

                            

                    if config.has_music or config.has_sound or config.has_voice:
                        null height gui.pref_spacing

                        textbutton _("Mute All") xpos 680 ypos -80:
                            action Preference("all mute", "toggle")
                            style "mute_all_button"


                vbox spacing 20 ypos -50:
                    style_prefix "check"
                    label _("{size=54}Skip") ypos 100
                    textbutton _("Unseen Text") action Preference("skip", "toggle") xpos 300
                    textbutton _("After Choices") action Preference("after choices", "toggle") xpos 300
                    textbutton _("Transitions") action InvertSelected(Preference("transitions", "toggle")) xpos 300

                vbox spacing 20 ypos -50:
                    style_prefix "radio"
                    label _("{size=54}Language") ypos 100
                    textbutton "English" action Language(None) xpos 300
                    textbutton "简体中文" action Language("zh_Hans") xpos 300 text_font "gui/chinese.ttf"


                vbox ypos 100:
                
                    hbox:

                        spacing 100

                        label _("{size=54}Instant messages")

                        hbox:

                            spacing 20

                            style_prefix "check"

                            textbutton "{size=54}On" action Call('Change_Text_Speed') ypos 4

                            textbutton "{size=54}Off" action Call('Default_Text_Speed') ypos 4

style pref_label is gui_label
style pref_label_text is gui_label_text
style pref_vbox is vbox

style radio_label is pref_label
style radio_label_text is pref_label_text
style radio_button is gui_button
style radio_button_text is gui_button_text
style radio_vbox is pref_vbox

style check_label is pref_label
style check_label_text is pref_label_text
style check_button is gui_button
style check_button_text is gui_button_text
style check_vbox is pref_vbox

style slider_label is pref_label
style slider_label_text is pref_label_text
style slider_slider is gui_slider
style slider_button is gui_button
style slider_button_text is gui_button_text
style slider_pref_vbox is pref_vbox

style mute_all_button is check_button
style mute_all_button_text is check_button_text

style pref_label:
    top_margin gui.pref_spacing
    bottom_margin 3

style pref_label_text:
    yalign 1.0

style pref_vbox:
    xsize 338

style radio_vbox:
    spacing gui.pref_button_spacing

style radio_button:
    properties gui.button_properties("radio_button")
    foreground "gui/button/radio_[prefix_]foreground.png"

style radio_button_text:
    properties gui.text_properties("radio_button")

style check_vbox:
    spacing gui.pref_button_spacing

style check_button:
    properties gui.button_properties("check_button")
    foreground "gui/button/check_[prefix_]foreground.png"

style check_button_text:
    properties gui.text_properties("check_button")

style slider_slider:
    xsize 525

style slider_button:
    properties gui.button_properties("slider_button")
    yalign 0.5
    left_margin 15

style slider_button_text:
    properties gui.text_properties("slider_button")

style slider_vbox:
    xsize 675


## History screen ##############################################################
##
## This is a screen that displays the dialogue history to the player. While
## there isn't anything special about this screen, it does have to access the
## dialogue history stored in _history_list.
##
## https://www.renpy.org/doc/html/history.html

screen history():

    tag menu

    ## Avoid predicting this screen, as it can be very large.
    predict False

    use game_menu(_("History"), scroll=("vpgrid" if gui.history_height else "viewport"), yinitial=1.0, spacing=gui.history_spacing):

        style_prefix "history"

        for h in _history_list:

            window:

                ## This lays things out properly if history_height is None.
                has fixed:
                    yfit True

                if h.who:

                    label h.who:
                        style "history_name"
                        substitute False

                        ## Take the color of the who text from the Character, if
                        ## set.
                        if "color" in h.who_args:
                            text_color h.who_args["color"]

                $ what = renpy.filter_text_tags(h.what, allow=gui.history_allow_tags)
                text what:
                    substitute False

        if not _history_list:
            label _("The dialogue history is empty.")


## This determines what tags are allowed to be displayed on the history screen.

define gui.history_allow_tags = { "alt", "noalt", "rt", "rb", "art" }


style history_window is empty

style history_name is gui_label
style history_name_text is gui_label_text
style history_text is gui_text

style history_label is gui_label
style history_label_text is gui_label_text

style history_window:
    xfill True
    ysize gui.history_height

style history_name:
    xpos gui.history_name_xpos
    xanchor gui.history_name_xalign
    ypos gui.history_name_ypos
    xsize gui.history_name_width

style history_name_text:
    min_width gui.history_name_width
    textalign gui.history_name_xalign

style history_text:
    xpos gui.history_text_xpos
    ypos gui.history_text_ypos
    xanchor gui.history_text_xalign
    xsize gui.history_text_width
    min_width gui.history_text_width
    textalign gui.history_text_xalign
    layout ("subtitle" if gui.history_text_xalign else "tex")

style history_label:
    xfill True

style history_label_text:
    xalign 0.5


## Help screen #################################################################
##
## A screen that gives information about key and mouse bindings. It uses other
## screens (keyboard_help, mouse_help, and gamepad_help) to display the actual
## help.

screen help():

    tag menu

    default device = "keyboard"

    use game_menu(_("Help"), scroll="viewport"):

        style_prefix "help"

        vbox:
            spacing 23

            hbox:

                textbutton _("Keyboard") action SetScreenVariable("device", "keyboard")
                textbutton _("Mouse") action SetScreenVariable("device", "mouse")

                if GamepadExists():
                    textbutton _("Gamepad") action SetScreenVariable("device", "gamepad")

            if device == "keyboard":
                use keyboard_help
            elif device == "mouse":
                use mouse_help
            elif device == "gamepad":
                use gamepad_help


screen keyboard_help():

    hbox:
        label _("Enter")
        text _("Advances dialogue and activates the interface.")

    hbox:
        label _("Space")
        text _("Advances dialogue without selecting choices.")

    hbox:
        label _("Arrow Keys")
        text _("Navigate the interface.")

    hbox:
        label _("Escape")
        text _("Accesses the game menu.")

    hbox:
        label _("Ctrl")
        text _("Skips dialogue while held down.")

    hbox:
        label _("Tab")
        text _("Toggles dialogue skipping.")

    hbox:
        label _("Page Up")
        text _("Rolls back to earlier dialogue.")

    hbox:
        label _("Page Down")
        text _("Rolls forward to later dialogue.")

    hbox:
        label "H"
        text _("Hides the user interface.")

    hbox:
        label "S"
        text _("Takes a screenshot.")

    hbox:
        label "V"
        text _("Toggles assistive {a=https://www.renpy.org/l/voicing}self-voicing{/a}.")

    hbox:
        label "Shift+A"
        text _("Opens the accessibility menu.")


screen mouse_help():

    hbox:
        label _("Left Click")
        text _("Advances dialogue and activates the interface.")

    hbox:
        label _("Middle Click")
        text _("Hides the user interface.")

    hbox:
        label _("Right Click")
        text _("Accesses the game menu.")

    hbox:
        label _("Mouse Wheel Up")
        text _("Rolls back to earlier dialogue.")

    hbox:
        label _("Mouse Wheel Down")
        text _("Rolls forward to later dialogue.")


screen gamepad_help():

    hbox:
        label _("Right Trigger\nA/Bottom Button")
        text _("Advances dialogue and activates the interface.")

    hbox:
        label _("Left Trigger\nLeft Shoulder")
        text _("Rolls back to earlier dialogue.")

    hbox:
        label _("Right Shoulder")
        text _("Rolls forward to later dialogue.")

    hbox:
        label _("D-Pad, Sticks")
        text _("Navigate the interface.")

    hbox:
        label _("Start, Guide, B/Right Button")
        text _("Accesses the game menu.")

    hbox:
        label _("Y/Top Button")
        text _("Hides the user interface.")

    textbutton _("Calibrate") action GamepadCalibrate()


style help_button is gui_button
style help_button_text is gui_button_text
style help_label is gui_label
style help_label_text is gui_label_text
style help_text is gui_text

style help_button:
    properties gui.button_properties("help_button")
    xmargin 12

style help_button_text:
    properties gui.text_properties("help_button")

style help_label:
    xsize 375
    right_padding 30

style help_label_text:
    size gui.text_size
    xalign 1.0
    textalign 1.0



################################################################################
## Additional screens
################################################################################


## Confirm screen ##############################################################
##
## The confirm screen is called when Ren'Py wants to ask the player a yes or no
## question.
##
## https://www.renpy.org/doc/html/screen_special.html#confirm

screen confirm(message, yes_action, no_action):

    ## Ensure other screens do not get input while this screen is displayed.
    modal True

    zorder 200

    style_prefix "confirm"

    add "gui/overlay/confirm.png"

    frame:

        vbox:
            xalign .5
            yalign .5
            spacing 45

            label _(message):
                style "confirm_prompt"
                xalign 0.5

            hbox:
                xalign 0.5
                spacing 150

                textbutton _("Yes") action yes_action
                textbutton _("No") action no_action

    ## Right-click and escape answer "no".
    key "game_menu" action no_action


style confirm_frame is gui_frame
style confirm_prompt is gui_prompt
style confirm_prompt_text is gui_prompt_text
style confirm_button is gui_medium_button
style confirm_button_text is gui_medium_button_text

style confirm_frame:
    background Frame([ "gui/confirm_frame.png", "gui/frame.png"], gui.confirm_frame_borders, tile=gui.frame_tile)
    padding gui.confirm_frame_borders.padding
    xalign .5
    yalign .5

style confirm_prompt_text:
    textalign 0.5
    layout "subtitle"

style confirm_button:
    properties gui.button_properties("confirm_button")

style confirm_button_text:
    properties gui.text_properties("confirm_button")


## Skip indicator screen #######################################################
##
## The skip_indicator screen is displayed to indicate that skipping is in
## progress.
##
## https://www.renpy.org/doc/html/screen_special.html#skip-indicator

screen skip_indicator():

    zorder 100
    style_prefix "skip"

    frame:

        hbox:
            spacing 9

            text _("Skipping")

            text "▸" at delayed_blink(0.0, 1.0) style "skip_triangle"
            text "▸" at delayed_blink(0.2, 1.0) style "skip_triangle"
            text "▸" at delayed_blink(0.4, 1.0) style "skip_triangle"


## This transform is used to blink the arrows one after another.
transform delayed_blink(delay, cycle):
    alpha .5

    pause delay

    block:
        linear .2 alpha 1.0
        pause .2
        linear .2 alpha 0.5
        pause (cycle - .4)
        repeat


style skip_frame is empty
style skip_text is gui_text
style skip_triangle is skip_text

style skip_frame:
    ypos gui.skip_ypos
    background Frame("gui/skip.png", gui.skip_frame_borders, tile=gui.frame_tile)
    padding gui.skip_frame_borders.padding

style skip_text:
    size gui.notify_text_size

style skip_triangle:
    ## We have to use a font that has the BLACK RIGHT-POINTING SMALL TRIANGLE
    ## glyph in it.
    font "DejaVuSans.ttf"


## Notify screen ###############################################################
##
## The notify screen is used to show the player a message. (For example, when
## the game is quicksaved or a screenshot has been taken.)
##
## https://www.renpy.org/doc/html/screen_special.html#notify-screen

screen notify(message):

    zorder 100
    style_prefix "notify"

    frame at notify_appear:
        text "[message!tq]"

    timer 3.25 action Hide('notify')


transform notify_appear:
    on show:
        alpha 0
        linear .25 alpha 1.0
    on hide:
        linear .5 alpha 0.0


style notify_frame is empty
style notify_text is gui_text

style notify_frame:
    ypos gui.notify_ypos

    background Frame("gui/notify.png", gui.notify_frame_borders, tile=gui.frame_tile)
    padding gui.notify_frame_borders.padding

style notify_text:
    properties gui.text_properties("notify")


## NVL screen ##################################################################
##
## This screen is used for NVL-mode dialogue and menus.
##
## https://www.renpy.org/doc/html/screen_special.html#nvl



screen nvl(dialogue, items=None):
    window:
        
        style "nvl_window"

        vbox ypos 2080:
            yanchor 1.0
            ymaximum 1840
            spacing gui.nvl_spacing
            use nvl_dialogue(dialogue)

        ## Displays the menu, if given.
        for i in items:
            textbutton i.caption:
                action i.action
                style "nvl_button"

    add SideImage() xalign 1.0 yalign 1.0


    imagebutton ypos 2100:
        idle "images/whatsapp/chat_bottom.png"


    imagebutton ypos 0:
        idle "images/whatsapp/chat_top.png"
    
    fixed ypos 130 xpos 52:

        text current_chat.name size 60 font "gui/TMR_Regular.ttf" color "#fff" ypos -20

        hbox ypos 55:

            spacing 10
            text "🟢" size 16 ypos 10
            text "Online" size 36 color "#fff"

        add current_chat.avatar at shrink_big xalign 0.89 ypos -28




screen nvl_dialogue(dialogue):
    for d in (dialogue):  # Перевернуть список диалогов, чтобы старые были наверху
        window:
            id d.window_id

            fixed:
            
                yfit gui.nvl_height is None

                if d.who is not None:
                    if (current_phone == "mc" and (d.who == "{image=images/whatsapp/people/unknown8_port.png}" or d.who == "{image=images/whatsapp/people/gg_sissy_port.png}" or d.who == "{image=images/whatsapp/people/gg_port.png}" or d.who == "{image=images/whatsapp/people/gg_f_port.png}")) or (current_phone == "wife" and d.who == "{image=images/whatsapp/people/wife_port.png}") or (current_phone == "son" and (d.who == "{image=images/whatsapp/people/son_port.png}" or d.who == "{image=images/whatsapp/people/sson_port.png}")) or (current_phone == "wsis" and d.who == "{image=images/whatsapp/people/w_sister_port.png}") or (current_phone == "talay" and d.who == "{image=images/whatsapp/people/talay_port.png}") or (current_phone == "christina" and d.who == "{image=images/whatsapp/people/christina_port.png}") or (current_phone == "mom" and d.who == "{image=images/whatsapp/people/mom_port.png}") or (current_phone == "mike" and d.who == "{image=images/whatsapp/people/mike_port.png}") or (current_phone == "mark" and d.who == "{image=images/whatsapp/people/mark_port.png}") or (current_phone == "sis" and d.who == "{image=images/whatsapp/people/stepsis_port.png}") or (current_phone == "niece" and d.who == "{image=images/whatsapp/people/julia_port.png}") or (current_phone == "jenna" and d.who == "{image=images/whatsapp/people/jenna_port.png}") or (current_phone == "lena" and d.who == "{image=images/whatsapp/people/lena_port.png}") or (current_phone == "kioko" and d.who == "{image=images/whatsapp/people/kioko_port.png}") or (current_phone == "kioko_m" and d.who == "{image=images/whatsapp/people/kioko_m_port.png}") or (current_phone == "kioko_f" and d.who == "{image=images/whatsapp/people/kioko_f_port.png}") or (current_phone == "cecilia" and d.who == "{image=images/whatsapp/people/cecilia_port.png}"):
                        text d.who xalign 0.98:
                            id d.who_id at (slide_out_avatar if d == dialogue[-1] else shrink_big)
                    else:
                        text d.who:
                            id d.who_id at (slide_in_avatar if d == dialogue[-1] else shrink_big)




                if (current_phone == "mc" and (d.who == "{image=images/whatsapp/people/unknown8_port.png}" or d.who == "{image=images/whatsapp/people/gg_sissy_port.png}" or d.who == "{image=images/whatsapp/people/gg_port.png}" or d.who == "{image=images/whatsapp/people/gg_f_port.png}")) or (current_phone == "wife" and d.who == "{image=images/whatsapp/people/wife_port.png}") or (current_phone == "son" and (d.who == "{image=images/whatsapp/people/son_port.png}" or d.who == "{image=images/whatsapp/people/sson_port.png}")) or (current_phone == "wsis" and d.who == "{image=images/whatsapp/people/w_sister_port.png}") or (current_phone == "talay" and d.who == "{image=images/whatsapp/people/talay_port.png}") or (current_phone == "christina" and d.who == "{image=images/whatsapp/people/christina_port.png}") or (current_phone == "mom" and d.who == "{image=images/whatsapp/people/mom_port.png}") or (current_phone == "mike" and d.who == "{image=images/whatsapp/people/mike_port.png}") or (current_phone == "mark" and d.who == "{image=images/whatsapp/people/mark_port.png}") or (current_phone == "sis" and d.who == "{image=images/whatsapp/people/stepsis_port.png}") or (current_phone == "niece" and d.who == "{image=images/whatsapp/people/julia_port.png}") or (current_phone == "jenna" and d.who == "{image=images/whatsapp/people/jenna_port.png}") or (current_phone == "lena" and d.who == "{image=images/whatsapp/people/lena_port.png}") or (current_phone == "kioko" and d.who == "{image=images/whatsapp/people/kioko_port.png}") or (current_phone == "kioko_m" and d.who == "{image=images/whatsapp/people/kioko_m_port.png}") or (current_phone == "kioko_f" and d.who == "{image=images/whatsapp/people/kioko_f_port.png}") or (current_phone == "cecilia" and d.who == "{image=images/whatsapp/people/cecilia_port.png}"):
                    
                    
                    text d.what ypos 10 xmaximum 840 xalign 0.29 text_align 1 size 46 font "gui/TMR_Regular.ttf" color "#a0a0a0":
                        id d.what_id
                        at (slide_out if d == dialogue[-1] else None)




                elif d.who is None or d.who == "":
                    text d.what ypos 10 text_align 0.5 size 46 font "gui/TMR_Regular.ttf" color "#a0a0a0":
                        id d.what_id

                else:
                    
                    text d.what ypos 10 size 46 font "gui/TMR_Regular.ttf" color "#a0a0a0":
                        id d.what_id
                        at (slide_in if d == dialogue[-1] else None)



transform slide_in_avatar:
    zoom 0.8
    xoffset 50
    alpha 0.0
    linear 0.3 xoffset 0 alpha 1.0


transform slide_out_avatar:
    zoom 0.8
    xoffset -50
    alpha 0.0
    linear 0.3 xoffset 0 alpha 1.0



transform slide_in:
    xoffset 50
    alpha 0.0
    linear 0.3 xoffset 0 alpha 1.0


transform slide_out:
    xoffset -50
    alpha 0.0
    linear 0.3 xoffset 0 alpha 1.0





## This controls the maximum number of NVL-mode entries that can be displayed at
## once.
define config.nvl_list_length = gui.nvl_list_length


style nvl_window is default
style nvl_entry is default

style nvl_label is say_label
style nvl_dialogue is say_dialogue

style nvl_button is button
style nvl_button_text is button_text

style nvl_window:
    xfill True
    padding gui.nvl_borders.padding



style nvl_entry:
    background Frame("ff.png")  # Отступы по бокам 50, снизу 30
    xfill True  # Растягивание по ширине
    ysize gui.nvl_height  # Растягивание по высоте
    



style nvl_label:
    xpos gui.nvl_name_xpos
    xanchor gui.nvl_name_xalign
    ypos gui.nvl_name_ypos
    yanchor 0.0
    xsize gui.nvl_name_width
    min_width gui.nvl_name_width
    text_align gui.nvl_name_xalign

style nvl_dialogue:
    xpos gui.nvl_text_xpos
    xanchor gui.nvl_text_xalign
    ypos gui.nvl_text_ypos
    xsize gui.nvl_text_width
    min_width gui.nvl_text_width
    text_align gui.nvl_text_xalign
    layout ("subtitle" if gui.nvl_text_xalign else "tex")

style nvl_thought:
    xpos gui.nvl_thought_xpos
    xanchor gui.nvl_thought_xalign
    ypos gui.nvl_thought_ypos
    xsize gui.nvl_thought_width
    min_width gui.nvl_thought_width
    text_align gui.nvl_thought_xalign
    layout ("subtitle" if gui.nvl_text_xalign else "tex")

style nvl_button:
    properties gui.button_properties("nvl_button")
    xpos gui.nvl_button_xpos
    xanchor gui.nvl_button_xalign

style nvl_button_text:
    properties gui.button_text_properties("nvl_button")


## Bubble screen ###############################################################
##
## The bubble screen is used to display dialogue to the player when using speech
## bubbles. The bubble screen takes the same parameters as the say screen, must
## create a displayable with the id of "what", and can create displayables with
## the "namebox", "who", and "window" ids.
##
## https://www.renpy.org/doc/html/bubble.html#bubble-screen

screen bubble(who, what):
    style_prefix "bubble"

    window:
        id "window"

        if who is not None:

            window:
                id "namebox"
                style "bubble_namebox"

                text who:
                    id "who"

        text what:
            id "what"

style bubble_window is empty
style bubble_namebox is empty
style bubble_who is default
style bubble_what is default

style bubble_window:
    xpadding 30
    top_padding 5
    bottom_padding 5

style bubble_namebox:
    xalign 0.5

style bubble_who:
    xalign 0.5
    textalign 0.5
    color "#000"

style bubble_what:
    align (0.5, 0.5)
    text_align 0.5
    layout "subtitle"
    color "#000"

define bubble.frame = Frame("gui/bubble.png", 55, 55, 55, 95)
define bubble.thoughtframe = Frame("gui/thoughtbubble.png", 55, 55, 55, 55)

define bubble.properties = {
    "bottom_left" : {
        "window_background" : Transform(bubble.frame, xzoom=1, yzoom=1),
        "window_bottom_padding" : 27,
    },

    "bottom_right" : {
        "window_background" : Transform(bubble.frame, xzoom=-1, yzoom=1),
        "window_bottom_padding" : 27,
    },

    "top_left" : {
        "window_background" : Transform(bubble.frame, xzoom=1, yzoom=-1),
        "window_top_padding" : 27,
    },

    "top_right" : {
        "window_background" : Transform(bubble.frame, xzoom=-1, yzoom=-1),
        "window_top_padding" : 27,
    },

    "thought" : {
        "window_background" : bubble.thoughtframe,
    }
}

define bubble.expand_area = {
    "bottom_left" : (0, 0, 0, 22),
    "bottom_right" : (0, 0, 0, 22),
    "top_left" : (0, 22, 0, 0),
    "top_right" : (0, 22, 0, 0),
    "thought" : (0, 0, 0, 0),
}
