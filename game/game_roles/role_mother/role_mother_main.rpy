#Contains all of the role events and actions related to the main Mom storylin.

init -2 python:
    #MOM ACTION REQUIREMENTS
    def mom_weekly_pay_requirement(the_person):
        if day%7 == 5: #It is the end of the day on friday
            return True
        return False

    def mom_offer_make_dinner_requirement(the_person):
        if time_of_day == 3:
            return True
        return False

    def mom_date_intercept_requirement(the_person, the_date):
        if the_person is the_date:
            return False
        if not person_at_home(the_person):
            return False
        elif the_person.energy < 80:
            return False
        elif not mc_at_home():
            return False
        elif the_person.love < 10:
            return False
        return True

    def mom_office_person_request_requirement():
        if time_of_day >= 4 or time_of_day == 0:
            return False
        elif mc.business.is_weekend():
            return False
        return True

    def add_mom_weekly_pay_action():
        mom_weekly_pay_action = Action("mom weekly pay", mom_weekly_pay_requirement, "mom_weekly_pay_label", args=mom, requirement_args =[mom]) # Reload the event for next week.
        mc.business.mandatory_morning_crises_list.append(mom_weekly_pay_action)
        return

    def add_sister_instapic_discover_crisis():
        sister_instapic_discover_crisis = Action("sister insta mom reveal", sister_instapic_discover_requirement, "sister_instathot_mom_discover", args = lily, requirement_args = lily)
        mc.business.mandatory_crises_list.append(sister_instapic_discover_crisis)
        return

### MOM ACTION LABELS ###

label mom_weekly_pay_label(the_person):
    #todo: at some point demand to take over the house, adds extra "house rules" options
    $ bedroom.show_background()
    "You're just getting out of bed when [the_person.possessive_title] calls from downstairs."
    the_person "[the_person.mc_title], could we talk for a moment?"
    mc.name "Sure, down in a second."
    $ mc.change_location(kitchen)
    $ mc.location.show_background()
    $ the_person.draw_person(position = "sitting")
    "[the_person.title] is sitting at the kitchen table, a collection of bills laid out in front of her."

    if the_person.effective_sluttiness() < 40:
        the_person "This new mortgage on the house is really stressing our finances. It would really help if you could chip in."
        call mom_low_sluttiness_weekly_pay(the_person) from _call_mom_low_sluttiness_weekly_pay #The menu is separated out to make looping easier.
    else:
        if mc.business.event_triggers_dict.get("Mom_Payment_Level",0) >= 1: #We've been through this song and dance already.
            if the_person.event_triggers_dict.get("Mom_forced_off_bc", False) and not pregnant_role in the_person.special_role:
                if the_person.on_birth_control:
                    $ mc.change_locked_clarity(10)
                    the_person "The budget is still really tight [the_person.mc_title], so I was wondering if you wanted to buy some sort of favour from me?"
                    $ the_person.event_triggers_dict["Mom_forced_off_bc"] = False
                else:
                    the_person "The budget is still really tight [the_person.mc_title]. I was hoping you could help out, for a favour, of course."
                    $ mc.change_locked_clarity(10)
                    the_person "I haven't taken my birth control all week. If you're able to pay me I won't start again."
                    menu:
                        "Keep her off her birth control\n{color=#ff0000}{size=18}Costs: $150{/size}{/color}" if mc.business.funds >= 150:
                            mc.name "I think we can keep this deal going."
                            "You pull out the cash and hand it over. She places them alongside the bills."
                            $ mc.business.funds += -150
                            the_person "Thank you so much. Is there anything else I could do for a little more help?"

                        "Keep her off her birth control{color=#ff0000}{size=18}Requires: $150{/size}{/color} (disabled)" if mc.business.funds < 150:
                            pass

                        "Let her start taking her birth control":
                            mc.name "I'm sorry, the budget at work has been a little tight lately."
                            the_person "I understand. Is there anything else I can do for then?"
                            $ manage_bc(the_person, start = True)
                            $ the_person.event_triggers_dict["Mom_forced_off_bc"] = False
            else:
                $ mc.change_locked_clarity(10)
                the_person "The budget is still really tight [the_person.mc_title], so I was wondering if you wanted to buy any sort of favour from me?"

            if lily.event_triggers_dict.get("sister_instathot_special_pictures_recent", False) and not lily.event_triggers_dict.get("sister_instathot_mom_knows", False): #She sold special pictures this week and Mom doesn't know about them yet.
                call mom_weekly_pay_lily_question(the_person) from _call_mom_weekly_pay_lily_question
                $ lily.event_triggers_dict["sister_instathot_special_pictures_recent"] = False


        else:
            the_person "Our budget is really stretched thin right now, and it would be a huge relief if you could help out."
            the_person "I wouldn't feel right about just taking your hard earned money though, so I was hoping we could make a deal..."
            mc.name "What sort of deal Mom?"
            $ mc.change_locked_clarity(5)
            the_person "Remember last summer, and you paid me for some... personal favours?"
            "Of course you remember all of the naughty things you convinced her to do last year."
            "Her memory of it seems much foggier, probably as a result of all the serum you exposed her to."
            "[the_person.title] blushes and looks away for a second before regaining her composure."
            $ mc.change_locked_clarity(10)
            the_person "Maybe we could start doing that again... I know I shouldn't even bring it up."
            mc.name "No [the_person.title], you're doing it for the good of the family, right? I think it's a great idea."
            $ the_person.change_slut_temp(2)
            $ the_person.change_happiness(5)
            $ the_person.change_love(2)
            the_person "Of course, it's the best thing for all of us. What would you like to do?"
            $ mc.business.event_triggers_dict["Mom_Payment_Level"] = 1
        call mom_high_sluttiness_weekly_pay(the_person) from _call_mom_high_sluttiness_weekly_pay

    $ add_mom_weekly_pay_action()
    return

label mom_low_sluttiness_weekly_pay(the_person):
    menu:
        "Give her nothing":
            mc.name "Sorry Mom, I'm just not turning a profit right now. Hopefully we will be soon though. I'll help out as soon as I can."
            $ the_person.change_happiness(-5)
            $ the_person.change_love(-1)
            $ the_person.draw_person(position = "sitting", emotion = "sad")
            the_person "Okay [the_person.mc_title], I understand. I'll talk with Lily and let her know that we have to cut back on non essentials."

        "Help out\n{color=#ff0000}{size=18}Costs: $100{/size}{/color}" if mc.business.funds >= 100:
            "You pull out your wallet and count out some cash, but hesitate before you hand it over."
            $ mc.business.funds += -100
            menu:
                "Ask for a kiss":
                    mc.name "I'd like a kiss for it though."
                    if the_person.has_taboo("kissing"):
                        the_person "A kiss?"
                        mc.name "For being such a good son."
                        the_person "Oh, well that's easy then."
                        "[the_person.possessive_title] stands up and leans in to give you a kiss on the cheek."
                        mc.name "On the lips, [the_person.title]. Please?"
                        the_person "You've always been so affectionate. Not like other boys at all, you know. Fine."
                        $ kissing.call_taboo_break(the_person, None, None) #We can reuse the kissing taboo break scene for improved dialogue and description.
                        $ mc.change_locked_clarity(10)
                        "After a moment she pulls back and looks away from you, blushing."
                        $ the_person.break_taboo("kissing")
                    else:
                        the_person "Okay, come here."
                        if the_person.effective_sluttiness("kissing") > 15:
                            "You lean down to kiss her as she's sitting. [the_person.possessive_title] puts a hand on the back of your head and pulls you against her as your lips meet."
                            "Her mouth opens slightly, letting your tongues meet as she makes out with you."
                            $ the_person.change_arousal(5 + mc.sex_skills["Foreplay"])
                            "It might be your imagination, but you think you might even hear her moan."
                            $ mc.change_locked_clarity(10)
                            "When you finally break the kiss she fixes her hair and smiles proudly at you."
                        else:
                            "You lean down to kiss her. She lets you press your lips against hers, and even returns the gentle kiss after a moment of hesitation."
                            $ mc.change_locked_clarity(10)
                            "When you finally break the kiss she looks away from you, blushing with embarrassment."

                    $ the_person.change_slut_temp(2)
                    the_person "There, have I earned my reward?"
                    "You hold out the cash for her and she takes it."
                    the_person "Thank you so much, every little bit helps."

                "Make her say please":
                    mc.name "What are the magic words?"
                    the_person "Abracadabra?"
                    mc.name "No, the words we say when we want help?"
                    the_person "Oooh, I see what you're getting at. I've drilled it into you and now I'm getting a taste of my own medicine."
                    "She smiles and rolls her eyes playfully."
                    $ mc.change_locked_clarity(5)
                    the_person "May I {i}please{/i} have some help with the bills?"
                    mc.name "I'm not sure if you mean it..."
                    the_person "Pretty please, [the_person.mc_title]?"
                    $ the_person.change_obedience(2)
                    "You hold out the cash and she takes it."
                    mc.name "And..."
                    the_person "Thank you [the_person.mc_title], you're very kind."
            $ the_person.change_happiness(5)
            $ the_person.change_love(3)
            $ the_person.draw_person(position = "sitting", emotion = "happy")
            "She gives you a hug and turns her attention back to organizing the bills."

        "Help out\n{color=#ff0000}{size=18}Requires: $100{/size}{/color} (disabled)" if mc.business.funds < 100:
            pass
    return

label mom_high_sluttiness_weekly_pay(the_person): #TODO: Change all of these over to use Actions instead of just being a menu.
    menu:
        "Strip for me\n{color=#ff0000}{size=18}Costs: $100{/size}{/color}" if mc.business.funds >= 100:
            if mc.business.event_triggers_dict.get("Mom_Strip", 0) >= 1:
                mc.name "I want you to show off yourself off to me, how does that sound?"
                the_person "Fair is fair, but I'll need a little extra if you want to see anything... inappropriate."
                $ mc.business.funds += -100
                "You hand over the cash and sit back while [the_person.possessive_title] entertains you."
            else:
                $ mc.business.event_triggers_dict["Mom_Strip"] = 1
                mc.name "I'd like to see a little more of you Mom, how about I pay you to give me a little strip tease."
                the_person "Oh my god, I've raised such a dirty boy. How about I pose for you a bit, and if you want to see more you can contribute a little extra."
                mc.name "Sounds like a good deal Mom."
                $ mc.business.funds += -100
                "You hand over the cash and sit back while [the_person.possessive_title] entertains you."

            call pay_strip_scene(the_person) from _call_pay_strip_scene_2

        "Strip for me\n{color=#ff0000}{size=18}Requires: $100{/size}{/color} (disabled)" if mc.business.funds <100:
            pass

        "Test some serum\n{color=#ff0000}{size=18}Costs: $100{/size}{/color}" if mc.business.funds >= 100:
            if mc.business.event_triggers_dict.get("Mom_Serum_Test",0) >= 1:
                mc.name "I've got some more serum I'd like you to test Mom."
                call give_serum(the_person) from _call_give_serum_10
                if _return:
                    $ mc.business.funds += -100
                    "You hand the serum to [the_person.possessive_title], followed by the cash."
                    the_person "Okay, so that's all for now?"
                    mc.name "That's all. I'll just be keeping an eye on you in the future, but you don't need to worry about that."
                    the_person "Well thank you [the_person.mc_title], this money will really make a difference. I'm so proud of you!"
                else:
                    mc.name "Actually, I don't have anything right now. Maybe next week though, okay?"
                    the_person "Okay [the_person.mc_title], thanks for at least thinking about it."
            else:
                $ mc.business.event_triggers_dict["Mom_Serum_Test"] = 1
                mc.name "I have something you could help me with Mom."
                the_person "What is it [the_person.mc_title]? I'll do whatever I can for you."
                mc.name "We have a little bit of a research bottleneck at work. I have something I'd like you to test for me."
                the_person "Oh, okay. If it helps I can be your for hire test subject!"
                mc.name "Excellent, let me just see if I have anything with me right now..."
                call give_serum(the_person) from _call_give_serum_11
                if _return:
                    $ mc.business.funds += -100
                    "You hand the serum to [the_person.possessive_title], followed by the cash."
                    the_person "Okay, so that's all for now?"
                    mc.name "That's all. I'll just be keeping an eye on you in the future, but you don't need to worry about that."
                    the_person "Well thank you [the_person.mc_title], this money will really make a difference. I'm so proud of you!"
                else:
                    mc.name "Actually, I don't have anything right now. Maybe next week though, okay?"
                    the_person "Okay [the_person.mc_title], thanks for at least thinking about it."

        # "I want to make some changes around here." if the_person.obedience >= 120:
        #     #TODO: Requires obedience, but unlocks a bunch of other options, like having your Mom bring you breakfast every morning, not wearing anything at home, etc.
        #     mc.name "Now that I'm the man of the house, I want to make some changes around the house."
        #     the_person "What sorts of changes?"
        #     call mom_make_house_changes(the_person)
        #
        # "I want to make some changes around here.\nRequires: 120 Obedience (disabled)" if the_person.obedience < 120:
        #     pass


        #TODO: "I want to breed Lily" option, once you've got Mom at high sluttiness, obedience, and Love. She gives you the go-ahead to knock up your sister.

        "Suck me off\n{color=#ff0000}{size=18}Costs: $300{/size}{/color}" if mc.business.funds >= 300 and the_person.effective_sluttiness("sucking_cock") >= 30:
            mc.name "Alright, I'll pay you to give me a blowjob."
            if (not the_person.has_taboo("sucking_cock")) or the_person.effective_sluttiness("sucking_cock") >= 60:
                the_person "If that's what you need."
                $ mc.change_locked_clarity(10)
                "You pull out your wallet and count out her cash while [the_person.possessive_title] gets onto her knees in front of you."
                $ mc.business.funds += -300
                $ the_person.draw_person(position = "blowjob")
                the_person "Remember, not a word to anyone else though. Okay?"
                mc.name "Of course, this is just between you and me."
                $ the_person.break_taboo("sucking_cock")

            else:
                the_person "What? I mean... I could never do that! How could you even say that?"
                "You pull out your wallet and count out the cash while you talk."
                mc.name "Sure you could. It's just me and you here, nobody would ever need to know."
                mc.name "Besides, it's for the family, right? This is just another way to help everyone out. Myself included, I've been real stressed at work lately."
                $ mc.business.funds += -300
                "You lay the cash down on the table. [the_person.possessive_title] hesitates, then meekly reaches for the money."
                the_person "Not a word to anyone, or I'll kick you out of the house."
                mc.name "Of course [the_person.title], don't you trust your own son?"
                $ the_person.draw_person(position = "blowjob")
                $ mc.change_locked_clarity(10)
                "She sighs and kneels down in front of you. You unzip your pants and pull your cock out for your mother."
                mc.name "Don't worry, it won't bite."
                the_person "This isn't my exactly my first blowjob [the_person.mc_title], I'm not worried."
                $ the_person.break_taboo("sucking_cock")

            "With that she opens her mouth and slides the tip of your hard cock inside. Her tongue swirls around the tip, sending a jolt of pleasure up your spine."
            $the_person.add_situational_obedience("deal", 20, "I'm doing this for the family")
            call fuck_person(the_person, private = True, start_position = blowjob, skip_intro = True, position_locked = True) from _call_fuck_person_33
            $ the_person.clear_situational_obedience("deal")
            $ the_report = _return
            $ the_person.apply_outfit()
            if the_report.get("girl orgasms", 0) > 0:
                "You pull up your pants while [the_person.possessive_title] is on her knees panting, trying to get her breath back."
                mc.name "I didn't know you were going to enjoy that so much. Maybe you should be paying me next time."
                the_person "Ah... I hope we can come to some sort of deal... Ah... In the future..."
            else:
                $ the_person.draw_person()
                "You pull your pants up while [the_person.possessive_title] gets off of her knees and cleans herself up."
            $ the_person.change_obedience(4)

        "Suck me off\n{color=#ff0000}{size=18}Requires: $300{/size}{/color} (disabled)" if mc.business.funds < 300 and the_person.effective_sluttiness("sucking_cock") >= 30:
            pass

        "Stop your birth control\n{color=#ff0000}{size=18}Costs: $150{/size}{/color}" if mc.business.funds >= 150 and the_person.effective_sluttiness() >= 30 and persistent.pregnancy_pref > 0 and not the_person.event_triggers_dict.get("Mom_forced_off_bc", False) and not pregnant_role in the_person.special_role:
            mc.name "I have something I'd like you to do. I want you to stop taking your birth control."
            if the_person.on_birth_control:
                if the_person.has_taboo("vaginal_sex"):
                    the_person "[the_person.mc_title], why would you want that? I hope you aren't thinking about something inappropriate between us!"
                else:
                    the_person "[the_person.mc_title], why would you want that? It's already so wrong every time we're together!"
                mc.name "I just think it would be a good way to remind you about what's important."
                "She seems like she's about to say more, but she stops when you pull out your money."
                the_person "How about... I stop for the week. If you don't want me to take it you'll have to pay me every week."
                mc.name "Okay, let's test it out for this week and see how you do."
                "You hand over the money to her and she tucks it away quickly."
                $ mc.business.funds += -150
                the_person "One moment."
                "[the_person.possessive_title] leaves the room, but returns quickly. She hands you a small blister pack labeled with each day of the week."
                the_person "Here are my pills for the week, so you know I'm not lying. I've already taken one for today, but starting tomorrow I won't have any."
                mc.name "Thank you [the_person.title]."
                $ the_person.event_triggers_dict["Mom_forced_off_bc"] = True
                $ manage_bc(the_person, start = False)
            else:
                the_person "I'm sorry, I can't take your money for that [the_person.mc_title]."
                mc.name "Sure you can [the_person.title], it's..."
                "[the_person.possessive_title] shakes her head and interrupts you."
                the_person "No, I mean I can't take your money because I'm not taking any birth control right now."
                if the_person.has_taboo("vaginal_sex"):
                    the_person "It's been a while since I needed it, so I don't bother."
                else:
                    the_person "I know I should, but... I just haven't bothered talking to my doctor."
                $ the_person.update_birth_control_knowledge()
                the_person "Is there something else you would like?"
                call mom_high_sluttiness_weekly_pay(the_person) from _call_mom_high_sluttiness_weekly_pay_1


        "Stop your birth control\n{color=#ff0000}{size=18}Costs: $150{/size}{/color} (disabled)" if mc.business.funds < 150 and the_person.effective_sluttiness() >= 30 and persistent.pregnancy_pref > 0  and not the_person.event_triggers_dict.get("Mom_forced_off_bc", False) and not pregnant_role in the_person.special_role:
            pass

        #TODO: Enable this and tie it into Lily's new Instapic story chunk
        # "Let [lily.title] get a boob job. -$500" if mc.business.funds >= 200 and lily.event_triggers_dict.get("insta_boobjob_wanted", False): #TODO: Implement this!
        #     mc.name "This will be some easy money for you. I want you to let [lily.title] have some cosmetic surgery done."
        #     mc.name "I'll pay you $500 if you just tell her you're okay with it. You don't need to do anythin else."
        #     the_person "Cosmetic surgery? What does she want to have changed? She's a beautiful young woman!"
        #     menu:
        #         "She wants breast implants.":
        #             mc.name "She wants to have breast implants put in."
        #
        #             pass
        #
        #         "She wants bigger tits.":
        #             mc.name "She's tired of her tiny tits and she wants some bigger ones."
        #             pass

        "Nothing this week":
            mc.name "Sorry Mom, but I'm tight on cash right now as well. Maybe next week, okay?"
            "[the_person.possessive_title] nods and turns back to her bills."
            the_person "I understand [the_person.mc_title]. Now don't let me keep you, I'm sure you were up to something important."

        #TODO: pay her to fuck you.
        #TODO: pay her to change her wardrobe
        #TODO: pay her to do somehting with Lily.
        #TODO: have Lily start a cam show to make cash, then bring your Mom into it.



    return

label mom_post_sex_confront(the_person):
    #TODO: She talks to you after the first time you seduce her somehow and talks about how "it was wrong... we can't do that!"

    return

label mom_make_house_changes(the_person):
    # A list of house rules to put into place.
    # TODO: This entire event. Make each one a linked action so that requirements work properly.

    #TODO: Just display a bunch of action options os that the requirements are propertly formatted for all of these.

    # menu:
    #     "I want breakfast delivered to me every morning." if mc.business.event_triggers_dict.get("mom_home_breakfast", false): #Bonus energy recovery. #TODO: Figure out how this works with other random events.
    #
    #
    #     "I want breakfast delivered to me every morning. (disabled)" if not mc.business.event_triggers_dict.get("mom_home_breakfast", false):
    #         pass
    #
    #     "I want my breakfast delivered to me naked." if mc.business.event_triggers_dict.get("mom_home_breakfast", true) and the_person.obedience >= 140 and
    #
    #     "You are going to be naked when you deliver my breakfast.": #Once you're having breakfast delivered
    #         pass
    #
    #     "You are going to service me when you deliver my breakfast.":
    #         pass
    #
    #     "I want you to start wearing more comfortable clothes around the house.": #Sets minimum sluttiness for Mom's outfits
    #         pass
    #
    #     "You are only allowed to wear your underwear when you're at home.":
    #         pass
    #
    #     "You can't wear anything that would keep your tits and pussy from me.":
    #         pass
    #
    #     # TODO: The disipline options are only available after Lily's started her InstaPic account and is posting stuff and you turn her in. If Mom is too slutty she says she doesn't care.
    #     # TODO: Add other "bad" things you can use as leverage against Lily.
    #     "I want to be in charge of Lily's discipline.": #Only after she's done somethign "bad", let's you punish her somehow, or just unlocks other things in this menu?
    #         # The whole Lily section might be better broken out into her role. with this as the enabling action. Definitely one of the paths to breaking them both and having your incest harem.
    #         pass
    #
    #     "Lily is only allowed to be in her underwear while at home.":
    #         pass
    #
    #     "Lily can't wear anything that would keep her tits or pussy from me.":
    #         pass
    #
    #     "Never mind.":
    #         call mom_high_sluttiness_weekly_pay(the_person) #Go back and pick something else.

    return

label mom_offer_make_dinner_label(the_person): #you offer to make dinner. It takes up time, but you can slip serum to your mom and sister.
    mc.name "You've been working yourself so hard lately Mom, how about you let me make dinner tonight?"
    the_person "Oh [the_person.mc_title], that's such a sweet thing for you to offer!"
    $ the_person.change_happiness(5)
    $ the_person.change_obedience(-1)
    $ the_person.change_love(2)

    the_person "Do you know where everything is?"
    mc.name "Yeah, I think I can take care of it."
    the_person "Well thank you, you're always such a help around here!"
    if the_person.love < 20 and the_person.effective_sluttiness() < 10:
        $ mc.change_locked_clarity(5)
        "[the_person.possessive_title] gives you a quick hug."
    elif the_person.love < 40 and the_person.effective_sluttiness() < 30:
        $ mc.change_locked_clarity(10)
        "[the_person.possessive_title] gives you a hug, then a quick kiss on the lips."
    else:
        $ mc.change_locked_clarity(10)
        "[the_person.possessive_title] gives you a hug, then kisses you on the lips."
        the_person "It's so nice having a man around the house again..."
        "She leans her head happily on your shoulder for a moment."
        menu:
            "Hold her gently":
                "You just hold [the_person.title] in your arms for a few moments."
                $ the_person.change_love(1)
                "After a little while she sighs and steps back."
                the_person "I should get out of your way."

            "Slap her ass":
                "You reach around [the_person.possessive_title] and give her ass a quick slap."
                if the_person.outfit.vagina_visible():
                    "The strike makes a satisfying smack and sets her butt jiggling for a few moments."
                    $ mc.change_locked_clarity(20)
                    "You give her bare ass a few more taps before letting her step back."
                else:
                    $ mc.change_locked_clarity(10)
                    "The strike makes a satisfying smack and sets her butt jiggling for a few moments."
                the_person "Oh!"
                mc.name "Come on [the_person.title], I've got dinner to cook. Run along, or I'll find some way to put you to work."


    the_person "Let me know if you need anything."
    $ clear_scene()
    $ kitchen.show_background()
    "You get to work. The cooking isn't hard, but it takes up most of your evening."
    "As you're plating out dinner you have a perfect opportunity to give your mother or sister some serum in secret."
    menu:
        "Add serum to Mom's food":
            call give_serum(mom) from _call_give_serum_8

        "Leave Mom's food alone":
            pass

    menu:
        "Add serum to [lily.name]'s food":
            call give_serum(lily) from _call_give_serum_9

        "Leave [lily.name]'s food alone":
            pass

    if hall.has_person(aunt):
        menu:
            "Add serum to [aunt.name]'s food":
                call give_serum(aunt) from _call_give_serum_32

            "Leave [aunt.name]'s food alone":
                pass

        menu:
            "Add serum to [cousin.name]'s food":
                call give_serum(cousin) from _call_give_serum_33

            "Leave [cousin.name]'s food alone":
                pass

    "You bring the food out and have a nice family dinner together."
    call advance_time from _call_advance_time_10
    return

label mom_serve_breakfast_request(the_person):
    #TODO: You ask her to make you breakfast every morning as your helping-with-the-bills request
    mc.name "I want breakfast brought to me every morning. I'm usually so busy with work I don't have any time to do it myself."
    the_person "Okay [the_person.mc_title], if you're able to help out every week with the bills I can do that."
    the_person "I'll have to get up early to get it made before work, but I'll do it for you. Maybe [lily.title] can help me."
    # TODO: She wants some extra money from you every week she keeps doing this.
    # TODO: Hook this up to actually do something.
    #TODO: If she's slutty enough to move onto the nude_serve level she has a chance of showing up in her underwear.
    return

label mom_nude_serve_breakfast_request(the_person): # TODO: Hook this up
    mc.name "When you bring me breakfast in the morning I want you to bring it to me naked."
    if the_person.effective_sluttiness() < 60: #She has some reservations about it
        the_person "What! [the_person.mc_title], I couldn't..."
        mc.name "Come on [the_person.title], it's nice to start my day off with a little eye candy. I've seen you naked before."
        the_person "When you were younger, sure, but you're so much older now."
        mc.name "Well you wanted to know what I wanted in exchange for my help. There it is."
        "She thinks about it for a long time, then nods."
        the_person "Fine, if you're going to be paying for it I'll go along with it. I want you to know I think it's silly though."
    else: #She's already really slutty and that's not a big deal
        the_person "Okay, if that's what you'd like [the_person.mc_title]."

    return

label mom_breakfast_with_service_request(the_person): # TODO: Hook this up. as a reward
    mc.name "When you bring me breakfast I want you to give me some entertainment as well."
    the_person "I'm already naked when I come in, what more do you want [the_person.mc_title]?"
    mc.name "I wake up with morning wood a lot, I want you to use your tits and mouth to take care of that for me."
    if the_person.effective_sluttiness() < 80:
        the_person "Oh my god, do you really mean..."
        if the_person.sex_record.get("Blowjobs",0) > 0 or the_person.sex_record.get("Tit Fucks") > 0:
            mc.name "Sure, why not? We've done it before."
            the_person "Maybe, but... Do you really want to be doing that every morning?"
            mc.name "Just something quick to blow off some steam. Come on, I love you Mom, don't you love me?"
        else:
            mc.name "Sure, why not? I love you and I want to feel close to you every day. Don't you love me Mom?"
        "You watch as her heart melts. She nods and hugs you."
        the_person "Of course I love you [the_person.mc_title]. Okay, I'll do this for you as long as you're helping out with the bills."
    else:
        the_person "Of course, I should have thought about that [the_person.mc_title]."
        the_person "As long as you're helping with the bills I'll make sure your morning wood is always taken care of."


    return

label mom_weekly_pay_lily_question(the_person):
    if the_person.event_triggers_dict.get("mom_instathot_questioned", False):
        the_person "Before we talk about that, do can I ask you a question?"
        mc.name "Sure, what do you want to know?"
        the_person "Well, it's your sister again. She had more money to help with the bills, but she still won't tell me where it's from."
        the_person "I know I said I wouldn't pry, but the only times she leaves the house is to go to class."
        the_person "I just really want to be sure she's not in some sort of trouble."
    else:
        the_person "Oh, before we talk about that I'm hoping you can answer something for me."
        mc.name "Okay, what do you need to know?"
        the_person "Your sister was very strange just now. She actually offered to help with the bills."
        the_person "She wouldn't tell me where she's getting this money though."
        the_person "I respect her privacy, but I want to make sure she isn't getting into any trouble."
        $ the_person.event_triggers_dict["mom_instathot_questioned"] = True

    menu:
        "Cover for [lily.title]":
            if the_person.event_triggers_dict.get("mom_instathot_questioned", False):
                mc.name "She's working on campus, so I guess she's working between classes."
                the_person "I just wish she would trust me."
                mc.name "I'm sure she'll tell you eventually, but you don't need to worry about her."
                the_person "I hope she does. Thank you [the_person.mc_title]."

            else:
                mc.name "Uh... No, she isn't getting into any trouble. I think she's just got a job on campus."
                the_person "Really? Why wouldn't she tell me about that, I'm so proud of her!"
                mc.name "I don't know, maybe she didn't want you to think she's doing it just because we need money."
                the_person "Well, I'll let her tell me when she's ready. I'm just happy to know it's nothing to worry about."

        "Tell her about InstaPic":
            mc.name "Well, I think she's picked up a part time job."
            the_person "Oh, why haven't I heard about this?"
            mc.name "It's not exactly a traditional job. She's been putting pictures up on InstaPic."
            the_person "InstaPic? Isn't that an internet thing? I don't understand."
            mc.name "[lily.title] puts up pictures showing off clothing, and InstaPic pays her for the ad traffic she generates."
            the_person "So it's like modeling, but she can do it from home?"
            mc.name "I guess so, yeah. She's just worried that you wouldn't approve."
            the_person "Why wouldn't I? Models can be very successful. And there are no photographers or agents to take advantage of her."
            the_person "I'm going to tell her how proud I am of her. Maybe she'll even let her Mom take a few photos with her."
            "She laughs and shrugs."
            the_person "Never mind, nobody's interested in looking at someone old like me."
            mc.name "You should absolutely ask [lily.title] to take some pictures with you. I think you'd be surprised."
            the_person "Aww, you're too sweet."
            $ lily.event_triggers_dict["sister_instathot_mom_knows"] = True
            $ add_sister_instapic_discover_crisis()
    return

label mom_stress_relief_offer(the_person): #TODO: Write and hook this up.
    #TODO: Mom sees that you're "stressed" - maybe triggered by going to work too many days in a row without doing something else - and offers to help "relieve" you.
    #TODO: What she offers to do depends on her sluttiness.
    return

label mom_date_intercept(the_mom, the_date): #TODO: Add some relationship awareness to Mom so she can comment on you dating multiple girls, ect.
    #Triggers when you've got a date planned with a girl, but Mom has high Love.
    #TODO: Write a Mom specific movie date. Maybe mirror the LR1 event and have Lily join in sometimes.

    $ mc.change_location(bedroom)
    $ mc.location.show_background()

    "You're getting ready for your date with [the_date.title] when you hear a knock at your door."
    the_mom "Knock knock. Are you in there [the_mom.mc_title]?"
    mc.name "Yeah, come on in [the_mom.title]."
    $ the_mom.draw_person()
    "[the_mom.possessive_title] steps into your room and closes the door behind her."
    the_mom "Oh, you're looking very handsome tonight. Is there some special occasion?"
    if the_date.has_role(girlfriend_role) and (not the_date.has_role(sister_girlfriend_role) or the_date.event_triggers_dict.get("sister_girlfriend_mom_knows",False)):
        mc.name "I'm taking [the_date.title] on a date tonight."
    else:
        mc.name "I'm going out on a date tonight."

    if the_mom.love > 70 and the_mom.effective_sluttiness() > 60: #High slut, she offers to fuck you (with slut bonus) if you stay at home
        if the_mom.get_opinion_score("not wearing anything") > 0 or the_mom.get_opinion_score("lingerie") < 0:
            the_mom "You are? Oh [the_mom.mc_title]..."
            $ strip_list = the_mom.outfit.get_full_strip_list()
            if strip_list:
                $ first_item = strip_list[0]
                $ the_mom.draw_animated_removal(first_item)
                "[the_mom.possessive_title] grabs her [first_item.display_name] and pulls it off."
                $ strip_list.remove(first_item)
                $ del first_item
            else:
                "[the_mom.possessive_title] spreads her legs, displaying her naked body for you."


            mc.name "[the_mom.title], what are you doing?"
            $ mc.change_locked_clarity(10)
            the_mom "Convincing you to stay home tonight."
            $ generalised_strip_description(the_mom, strip_list)
            $ mc.change_locked_clarity(20)
            $ del strip_list

        else:
            the_mom "You are? I... Don't go anywhere, okay? I'll be right back."
            $ clear_scene()
            "Before you can ask her any questions she's hurried out of your room."
            "You shrug and go back to preparing for your date. A few short minutes later [the_mom.possessive_title] steps back into your room."
            $ the_mom.apply_outfit(lingerie_wardrobe.get_random_appropriate_outfit(the_mom.sluttiness + 20, 0 + (the_mom.sluttiness/2), guarantee_output = True), update_taboo = True)
            $ the_mom.draw_person()
            $ mc.change_locked_clarity(30)
            the_mom "[the_mom.mc_title], are you still sure you want to go out and see some other girl?"
            mc.name "[the_mom.title], what are you doing?"
            the_mom "Convincing you to stay home tonight."

        the_mom "What are you expecting this girl to do for you that I can't? You know nobody will ever love you like your mother."
        the_mom "You're a man now, which means you have different needs, but I still want to be the one to take care of you."
        $ mc.change_locked_clarity(20)
        "She steps close to you and cups your crotch, rubbing your already-hard cock through your pants."
        the_mom "Let me take care of you. Stay home tonight."
        menu:
            "Cancel your date with [the_date.title]":
                mc.name "[the_mom.title]... You know you're the most important woman in my life. I'll call [the_date.title] and cancel."
                $ the_mom.change_happiness(10)
                $ the_mom.change_love(2)
                $ the_mom.change_slut_temp(2)
                "[the_mom.possessive_title]'s face lights up."
                the_mom "Thank you [the_mom.mc_title], you're making the right decision. We're going to have such a wonderful time together."
                mc.name "Just give me a moment, okay? She's probably not going to be happy about this."
                $ skip_intro = False
                $ start_position = None
                $ skip_condom = False
                if the_mom.get_opinion_score("giving blowjobs") > the_mom.get_opinion_score("vaginal_sex") or the_mom.effective_sluttiness("vaginal_sex") < 70:
                    $ the_mom.draw_person(position = "kneeling1")
                    "[the_mom.possessive_title] drops to her knees in front of you."
                    the_mom "I'll be quiet. Go ahead, I'm going to get you warmed up and show you just how thankful I am!"
                    "You get your phone out while [the_mom.title] pulls down your pants. Your hard cock bounces against her face when it springs free of your underwear."
                    the_mom "Oh! Sorry, sorry..."
                    $ mc.change_locked_clarity(20)
                    "You call [the_date.title] as [the_mom.possessive_title] starts to lick at your shaft."
                    $ the_mom.draw_person(position = "blowjob", special_modifier = "blowjob", the_animation = blowjob_bob, animation_effect_strength = 0.3)
                    the_date "Hello?"
                    if the_date.is_family():
                        mc.name "Hey Sweety, it's me."
                    else:
                        mc.name "Hey [the_date.title], it's [the_date.mc_title]."
                    the_date "Hey [the_date.mc_title], I was just about to head out the door. Is everything okay?"
                    mc.name "Well, I hate to tell you this so late, but..."
                    $ mc.change_locked_clarity(30)
                    "[the_mom.possessive_title] looks up at you from her knees, your cock bulging out one cheek."
                    mc.name "Something important has come up, and it needs to be taken care of. I won't be able to go out tonight."
                    $ the_mom.change_love(4)
                    $ the_mom.change_slut_temp(3)
                    $ mc.change_locked_clarity(30)
                    "[the_mom.title]'s eyes light up, and she bobs her head up and down on your shaft happily. You have to stifle a moan."
                    the_date "Oh no, is everyone okay?"
                    $ the_date.change_happiness(-20)
                    $ the_date.change_love(-3)
                    "[the_date.possessive_title]'s disappointment is clear, even over the phone."
                    if the_date.is_family():
                        mc.name "Something urgent came up at work, that has to be taken care of."
                    else:
                        mc.name "It's a family situation, I'm sorry that I can't say any more."
                    $ mc.change_locked_clarity(20)
                    "[the_mom.possessive_title] sucks gently on the tip of your cock."
                    the_date "Okay, well... I hope you get that resolved. Let's try and reschedule, okay?"
                    mc.name "Yeah, I'll be in touch. Thanks for understanding [the_date.title]. Bye."
                    the_date "Bye..."
                    "[the_mom.possessive_title] pulls off your cock, smiling happily."
                    the_mom "Thank you [the_mom.mc_title]. I'm the only woman you'll ever need in your life."
                    "With that she slides you back into her warm, wet mouth and continues to suck you off."
                    $ skip_intro = True
                    $ start_position = blowjob

                else:
                    the_mom "I'll just be over here, ready for you..."
                    $ the_mom.draw_person(position = "doggy")
                    $ mc.change_locked_clarity(20)
                    "[the_mom.title] climbs onto your bed, face down and ass up, while she waits for you."
                    if the_date.is_family():
                        mc.name "Hey Sweety, it's me."
                    else:
                        mc.name "Hey [the_date.title], it's [the_date.mc_title]."
                    the_date "Hey [the_date.mc_title], I was just about to head out the door. Is everything okay?"
                    if not the_mom.outfit.vagina_available():
                        if the_mom.outfit.can_half_off_to_vagina():
                            $ generalised_strip_description(the_mom, the_mom.outfit.get_half_off_to_vagina_list(), position = "doggy", half_off_instead = True)
                        else:
                            $ generalised_strip_description(the_mom, the_mom.outfit.get_full_strip_list(), position = "doggy")
                        $ mc.change_locked_clarity(40)
                    "You're distracted as [the_mom.possessive_title] reaches back and jiggles her butt for you."
                    the_date "[the_date.mc_title]? Are you there?"
                    mc.name "Uh, yeah. Sorry, I hate to tell you this so late, but something important has come out."
                    mc.name "I'm not going to be able to make it for our date tonight."
                    the_date "Oh no, is everyone okay?"
                    $ the_date.change_happiness(-20)
                    $ the_date.change_love(-3)
                    $ mc.change_locked_clarity(30)
                    "[the_mom.title] grabs one ass cheek and pulls it to the side, giving you a clear view of her pretty pink pussy."
                    menu:
                        "Fuck [the_mom.title]'s pussy right away":
                            "You unzip your pants and step closer to [the_mom.possessive_title]."
                            if the_date.is_family():
                                mc.name "Something urgent came up at work and requires my full attention."
                            else:
                                mc.name "It's my Mom, she really needs me close right now."
                            $ mc.change_locked_clarity(40)
                            "You grab [the_mom.title]'s hips with your free hand and hold her steady as you slide your cock into her wet pussy. You fuck her slowly while you talk."
                            $ the_mom.draw_person(position = "doggy", the_animation = blowjob_bob, animation_effect_strength = 0.3)
                            mc.name "I can't really say any more than that right now. I'm sorry."
                            the_date "I understand, I hope everything works out. Let's try and reschedule some time soon, okay?"
                            $ mc.change_locked_clarity(30)
                            "[the_mom.possessive_title] grabs one of your pillows to muffle her moans with."
                            if the_date.is_family():
                                mc.name "Yeah, I'll be in touch. Thanks for understanding sweety. Bye."
                            else:
                                mc.name "Yeah, I'll be in touch. Thanks for understanding [the_date.title]. Bye."
                            the_date "Bye..."
                            if the_mom.has_taboo("condomless_sex") or the_mom.wants_condom():
                                the_mom "[the_mom.mc_title], did you put on a condom?"
                                mc.name "Nope. [the_date.title] doesn't like condoms."
                                the_mom "Then... I'll give you everything she could give you! I don't care if you fuck my pussy unprotected [the_mom.mc_title]!"
                                $ the_mom.break_taboo("condomless_sex")
                            else:
                                "As soon as you put your phone down [the_mom.title] starts to moans loudly."
                                the_mom "Oh [the_mom.mc_title], that feels amazing!"
                            $ skip_intro = True
                            $ start_position = doggy
                            $ skip_condom = True


                        "Wait until you're off the phone":
                            "You place a hand on [the_mom.possessive_title]'s butt and squeeze it idly as you talk."
                            if the_date.is_family():
                                mc.name "Something urgent came up at work and requires my full attention."
                            else:
                                mc.name "It's my Mom, she really needs me close right now."
                            mc.name "I can't really say any more than that right now. I'm sorry."
                            the_date "I understand, I hope everything works out. Let's try and reschedule some time soon, okay?"
                            $ mc.change_locked_clarity(30)
                            "[the_mom.possessive_title] puts a hand between her legs and starts to massage her clit while you're talking."
                            if the_date.is_family():
                                mc.name "Yeah, I'll be in touch. Thanks for understanding sweety. Bye."
                            else:
                                mc.name "Yeah, I'll be in touch. Thanks for understanding [the_date.title]. Bye."
                            the_date "Bye..."


                $ the_mom.add_situational_slut("Eager", 10, "I'll show that skank how a {i}real{/i} woman should treat him!")
                call fuck_person(the_mom, private = True, skip_intro = skip_intro, start_position = start_position, skip_condom = skip_condom) from _call_fuck_person_36
                $ the_report = _return
                $ the_mom.clear_situational_slut("Eager")
                if the_report.get("guy orgasms", 0) > 0:
                    the_mom "Ah... Well, wasn't that better than anything that girl would have done?"
                    mc.name "That was great [the_mom.title]."
                    $ the_mom.change_happiness(10)
                    $ the_mom.draw_person()
                    the_mom "Anything for my special man."
                else:
                    the_mom "I'm sorry [the_mom.mc_title], I just don't have the energy I used to have..."
                    mc.name "It's okay [the_mom.title], maybe later we can finish this up."
                    $ the_mom.draw_person()
                    $ the_mom.change_happiness(-5)
                    the_mom "I'll do my best. For my special man I'll try anything at all."

                the_mom "Now, would you like to watch some TV with me? I'll get us some snacks, we can spend the whole night together."
                mc.name "Sounds good [the_mom.title]."
                $ the_mom.change_love(1 + mc.charisma)
                $ the_mom.apply_outfit()
                $ the_mom.draw_person(position = "sitting")
                "You spend the rest of the evening with [the_mom.possessive_title], sitting on the couch, watching TV, and chatting."
                #TODO: Add a proper Mom date that this leads into

            "Tell her no":
                mc.name "Sorry [the_mom.title], but I just can't cancel my plans this suddenly."
                mc.name "I need to get going."
                if the_mom.love > 80:
                    "You hurry to the door, but [the_mom.possessive_title] grabs your arm."
                    $ mc.change_locked_clarity(10)
                    the_mom "Wait! How about just a quickie? You can tell her you're running late."
                    the_mom "I want to take all of your cum, so she doesn't get any. Can you give me that, at least?"
                    menu:
                        "Fuck [the_mom.title] before your date":
                            "You sigh, then nod."
                            mc.name "Fine, but we need to make it quick."
                            $ the_mom.change_love(1)
                            $ the_mom.change_slut_temp(1)
                            "She nods happily."
                            $ the_mom.add_situational_slut("Eager", 20, "I need to drain those balls before that skank touches him!")
                            call fuck_person(the_mom, private = True) from _call_fuck_person_40
                            $ the_report = _return
                            $ the_mom.clear_situational_slut("Eager")
                            if the_report.get("guy orgasms", 0) > 0:
                                the_mom "Mmm, that was great [the_mom.mc_title]. Whatever happens I'll always be the first woman you come to, right?"
                                mc.name "Of course [the_mom.title]."
                                $ the_mom.change_happiness(5)
                            else:
                                the_mom "I'm sorry [the_mom.mc_title], I just don't have the energy I used to have..."
                                mc.name "It's okay [the_mom.title], maybe later we can finish this up."
                                the_mom "Maybe you do need this other girl... You should find someone who can take care of you properly."
                                $ the_mom.change_happiness(-5)

                            "You're interrupted by a phone call. It's [the_date.title]."
                            if the_date.is_family():
                                mc.name "Hey Sweety...."
                                the_date "[the_date.mc_title], are you on your way?"
                                mc.name "I'm just heading out the door. Something important came up at work, but it's taken care of."
                            else:
                                mc.name "Hey [the_date.title]..."
                                the_date "[the_date.mc_title], are you on your way?"
                                mc.name "I'm just heading out the door. Something important came up, but it's taken care of. Family related."
                            $ the_date.change_happiness(-5)
                            $ the_date.change_love(-1)
                            the_date "Okay, well I'm waiting here."
                            mc.name "I'm on my way, I won't be long."
                            "You hang up and stuff your cock back into your pants."
                            $ the_mom.draw_person()
                            the_mom "Have a good date [the_mom.mc_title]. Give me a kiss before you go."
                            "You kiss [the_mom.possessive_title], then hurry out of your room."

                        "Tell her no again":
                            mc.name "I don't have time [the_mom.title]. I'm sorry, but I really need to go."
                            mc.name "We can spend time together later, okay?"
                            $ the_mom.change_happiness(-10)
                            $ the_mom.change_love(-2)
                            $ clear_scene()
                            "You hurry out of the room, leaving [the_mom.possessive_title] behind."
                else:
                    "You hurry out of the room, leaving [the_mom.possessive_title] behind."
                    $ the_mom.change_happiness(-10)
                    $ the_mom.change_love(-2)
                    $ clear_scene()

                return False

    elif the_mom.love > 50 and the_mom.effective_sluttiness("sucking_cock") > 40 and the_mom.get_opinion_score("giving blowjobs") >= 0: #TODO: Moderate sluttiness. She tries to convince you to stay home by offering sex (default sex system entry)
        the_mom "Oh, you are? I was hoping you would spend some time at home, I barely see you these days."
        mc.name "Sorry, but I've already made these plans. Maybe some other time, okay?"
        the_mom "[the_mom.mc_title], you aren't seeing this girl just for... physical reasons, are you?"
        mc.name "What? Why?"
        the_mom "Well, A boy your age can sometimes be thinking with his penis instead of his head."
        $ mc.change_locked_clarity(10)
        "She steps closer to you and puts a hand to your crotch. It twitches in response, quickly growing hard."
        the_mom "I don't want you out getting in trouble with girls if all you really need is some physical relief."
        the_mom "If you decide to stay home, maybe I can... take care of this for you?"
        mc.name "[the_mom.title], [the_date.title] won't be happy with me if I cancel last minute."
        $ the_mom.draw_person(position = "kneeling1")
        "[the_mom.possessive_title] gets onto her knees in front of you, face level with the large bulge in your pants."
        if the_mom.has_taboo("sucking_cock"):
            the_mom "Please [the_mom.mc_title]? You were probably hoping to get a blowjob from her, right? Well..."
            "She hesitates, as if she needs to be extra sure she means what she's about to say."
            $ mc.change_locked_clarity(20)
            the_mom "I could do that too! You wouldn't need to worry about dressing up, or paying for dinner, or even leaving the house."
            the_mom "Just stay home and I'll take better care of you than any whatever skank is trying to get her hands on you!"
        else:
            the_mom "Please [the_mom.mc_title]? If you stay you don't need to worry about dressing up or paying for dinner."
            $ mc.change_locked_clarity(20)
            the_mom "I'll give you a nice blowjob, then when you're finished we can watch some TV and relax."
            the_mom "Doesn't that sound so much nicer than trying to impress some skank you just met? You've known me your whole life already."

        menu:
            "Cancel your date with [the_date.title]":
                $ mc.change_locked_clarity(20)
                "[the_mom.possessive_title] cups your crotch and massages it gently while you think about it."
                mc.name "Fine, but she's really not going to be happy about this."
                the_mom "Don't worry about her, I'm the only woman you need in your life right now. You can worry about finding a wife when you're older."
                mc.name "Just... Give me a minute to call her, okay?"
                if the_mom.get_opinion_score("giving blowjobs") > 0 and the_mom.effective_sluttiness("sucking_cock") >= 50:
                    the_mom "I can be quiet. Go ahead, I'll just get started..."
                    $ mc.change_locked_clarity(10)
                    "You get your phone out while [the_mom.title] pulls down your pants. Your hard cock bounces against her face when it springs free of your underwear."
                    the_mom "Oh! Sorry, sorry..."
                    $ mc.change_locked_clarity(20)
                    "You call [the_date.title] as [the_mom.possessive_title] starts to lick at your shaft."
                    $ the_mom.draw_person(position = "blowjob", special_modifier = "blowjob", the_animation = blowjob_bob, animation_effect_strength = 0.3)
                    the_date "Hello?"
                    if the_date.is_family():
                        mc.name "Hey Sweety, it's me."
                    else:
                        mc.name "Hey [the_date.title], it's [the_date.mc_title]."
                    the_date "Hey [the_date.mc_title], I was just about to head out the door. Is everything okay?"
                    mc.name "Well, I hate to tell you this so late, but..."
                    $ mc.change_locked_clarity(20)
                    "[the_mom.possessive_title] looks up at you from her knees, your cock bulging out one cheek."
                    mc.name "Something important has come up, and it needs to be taken care of. I won't be able to go out tonight."
                    $ the_mom.change_love(4)
                    $ the_mom.change_slut_temp(3)
                    $ mc.change_locked_clarity(20)
                    "[the_mom.title]'s eyes light up, and she bobs her head up and down on your shaft happily. You have to stifle a moan."
                    the_date "Oh no, is everyone okay?"
                    $ the_date.change_happiness(-20)
                    $ the_date.change_love(-3)
                    "[the_date.possessive_title]'s disappointment is clear, even over the phone."
                    if the_date.is_family():
                        mc.name "Something urgent came up at work and requires my full attention."
                    else:
                        mc.name "It's a family situation, I'm sorry that I can't say any more."
                    "[the_mom.possessive_title] sucks gently on the tip of your cock."
                    the_date "Okay, well... I hope you get that resolved. Let's try and reschedule, okay?"
                    mc.name "Yeah, I'll be in touch. Thanks for understanding [the_date.title]. Bye."
                    the_date "Bye..."
                    $ mc.change_locked_clarity(20)
                    "[the_mom.possessive_title] pulls off your cock, smiling happily."
                    the_mom "Thank you [the_mom.mc_title]. Now, should I keep going?"
                    "She starts to suck you off again before you even respond."

                else:
                    "[the_mom.title] nods and waits, still on her knees, while you get your phone out and call [the_date.title]."
                    the_date "Hello?"
                    if the_date.is_family():
                        mc.name "Hey Sweety, it's me."
                    else:
                        mc.name "Hey [the_date.title], it's [the_date.mc_title]."
                    the_date "Hey [the_date.mc_title], I was just about to head out the door. Is everything okay?"
                    mc.name "Well, I hate to tell you this so late, but..."
                    mc.name "Something important has come up, and it needs to be taken care of. I won't be able to go out tonight."
                    "[the_mom.possessive_title]'s eyes light up, and she smiles happily at you."
                    $ the_mom.change_love(3)
                    $ the_mom.change_slut_temp(2)
                    the_date "Oh no, is everyone okay?"
                    $ the_date.change_happiness(-20)
                    $ the_date.change_love(-3)
                    "[the_date.possessive_title]'s disappointment is clear, even over the phone."
                    if the_date.is_family():
                        mc.name "Something urgent came up at work and requires my full attention."
                    else:
                        mc.name "It's a family situation, I'm sorry that I can't say any more."
                    the_date "Okay, well... I hope you get that resolved. Let's try and reschedule, okay?"
                    if the_date.is_family():
                        mc.name "Yeah, I'll contact you soon, thanks for understanding. Bye."
                    else:
                        mc.name "Yeah, I'll be in touch. Thanks for understanding [the_date.title]. Bye."
                    the_date "Bye..."
                    the_mom "Thank you [the_mom.mc_title]. Now, should I take care of this?"
                    $ mc.change_locked_clarity(10)
                    "She unzips your pants and pulls them down. Your hard cock springs free, bouncing in front of her face."
                    the_mom "Oh!"
                    if the_mom.break_taboo("sucking_cock"):
                        $ mc.change_locked_clarity(20)
                        the_mom "It looks so much bigger when it's right in your face..."
                        "She takes a deep breath."
                        the_mom "It's fine, I can do this. Anything to make my [the_mom.mc_title] feel special and want to spend more time with me."
                    "She gives it an experimental kiss, then slips her lips over the tip."


                if not the_mom.outfit.vagina_visible() or not the_mom.outfit.tits_visible():
                    menu:
                        "Order her to strip" if the_mom.obedience >= 140:
                            mc.name "You should be dressed for the occasion first. Strip."
                            the_mom "Of course, right away [the_mom.mc_title]."
                            $ the_mom.draw_person()
                            "She stands up to get undressed."
                            $ remove_shoes = False
                            $ item = the_mom.outfit.get_feet_top_layer()
                            if item:
                                the_mom "Do you want me to keep my [item.display_name] on?"
                                menu:
                                    "Strip it all off":
                                        mc.name "Take it all off, I don't want you to be wearing anything."
                                        the_mom "Yes [the_mc.title]. I'll get completely naked for you."
                                        $ remove_shoes = True

                                    "Leave them on":
                                        mc.name "You can leave them on."
                            $ del item

                            $ generalised_strip_description(the_mom, the_mom.outfit.get_full_strip_list(strip_feet = remove_shoes))
                            $ mc.change_locked_clarity(30)

                            the_mom "There, now you can properly enjoy the view. Shall I get to it, then?"
                            mc.name "Go ahead."

                        "Order her to strip\n{size=16}{color=#FF0000}Requires: 140 Obedience{/color}{/size} (disabled)" if the_mom.obedience < 140:
                            pass

                        "Enjoy your blowjob":
                            pass

                $ the_mom.draw_person(position = "blowjob", special_modifier = "blowjob", the_animation = blowjob_bob, animation_effect_strength = 0.3)
                "You rest a hand on the top of [the_mom.possessive_title]'s head as she starts to suck on your cock. She starts slowly, but quickly picks up speed and confidence."
                mc.name "That feels great [the_mom.title]."
                "She pops off your cock for a moment and smiles up at you."
                $ mc.change_locked_clarity(20)
                the_mom "See? You don't need any other women in your life. I'll take care of you [the_mom.mc_title], just like I always have."
                "With that she slides you back into her mouth."
                call fuck_person(the_mom, start_position = blowjob, skip_intro = True, girl_in_charge = True, position_locked = True) from _call_fuck_person_99
                $ the_report = _return
                if the_report.get("guy orgasms", 0) > 0:
                    the_mom "Ah... Well, wasn't that better than anything that girl would have done?"
                    mc.name "That was great [the_mom.title]."
                    $ the_mom.change_happiness(10)
                    the_mom "Anything for my special man."
                else:
                    the_mom "I'm sorry [the_mom.mc_title], I just don't have the energy I used to have..."
                    mc.name "It's okay [the_mom.title], maybe later we can finish this up."
                    $ the_mom.change_happiness(-5)
                    the_mom "I'll do my best. For my special man I'll try anything at all."
                the_mom "Now, would you like to watch some TV with me? I'll get us some snacks, we can spend the whole night together."
                mc.name "Sounds good [the_mom.title]."
                $ the_mom.change_love(1 + mc.charisma)
                $ the_mom.apply_outfit()
                $ the_mom.draw_person(position = "sitting")
                "You spend the rest of the evening with [the_mom.possessive_title], sitting on the couch, watching TV, and chatting."
                return True


            "Tell her no":
                mc.name "I can't do that [the_mom.title]! I'm sorry, but I really do have to get going."
                "You leave her on her knees and hurry out of your room."
                $ the_mom.change_happiness(-5)
                $ the_mom.change_love(-1)
                return False


    elif the_mom.love > 30 and the_mom.effective_sluttiness("touching_penis") > 15 and the_mom.get_opinion_score("giving handjobs") >= 0:
        the_mom "That's nice, I'm sure you'll show her a wonderful time."
        the_mom "This girl, I assume you're interested in her... physically?"
        mc.name "I suppose so, why?"
        $ the_mom.draw_person(position = "sitting")
        "[the_mom.possessive_title] sits down on your bed and pats the spot beside her. You sit down with her to talk."
        the_mom "Well, for young men like yourself it's easy to get distracted by a girls looks."
        the_mom "It's not your fault, your hormones just take over and suddenly all you can look at are her butt and breasts!"
        mc.name "[the_mom.title], I think I'll be fine."
        "She places her hand on your upper thigh and gives it a gentle squeeze."
        the_mom "I want you to find a girl that's really right for you emotionally, not just some bimbo with nice tits."
        the_mom "The easiest way to be sure is to flush out all of those hormones first, so you can see her with a clear head."
        if the_mom.has_taboo("touching_penis"):
            the_mom "I was thinking... Well, if you wanted me to, I could, umm..."
            "[the_mom.possessive_title] blushes and looks away, struggling to finish her sentence."
            mc.name "What is it [the_mom.title]?"
            the_mom "I can help you deal with all of those hormones, if you'd like."
            $ mc.change_locked_clarity(10)
            the_mom "I've got a bit of experience, I can... give you a handjob?"
        else:
            $ mc.change_locked_clarity(10)
            the_mom "Let me help you. I'll give you a quick handjob before you go, so you aren't thinking with your penis all night."
            the_mom "You'll feel better, and I promise she'll notice how much more respectful you are."

        menu:
            "Let her \"help\" you":
                if the_mom.has_taboo("touching_penis"):
                    mc.name "That sounds like a really good idea [the_mom.title]."
                    "She breathes a sigh of relief."
                    the_mom "Okay, well then... You just stand up and I'll take care of you."
                    the_mom "Nothing sexual here, of course. I'm just doing my motherly duty trying to help you."
                    mc.name "Of course [the_mom.title], of course."
                else:
                    mc.name "That sounds like a good idea [the_mom.title]."
                    "She smiles happily."
                    the_mom "Good, you just stand up and I'll take care of you."
                    the_mom "It's my job as your mother to do things like this, after all. I think it's more common than people say, really."

                $ the_mom.draw_person()
                "You and [the_mom.possessive_title] both stand up. She reaches down for your pants and unzips them."
                "She pulls them down, gasping softly when your hard cock springs out of your underwear."
                $ mc.change_locked_clarity(10)
                if the_mom.has_taboo("touching_penis"):
                    the_mom "Oh... This is just to help you, okay? There's nothing wrong with it, it's just because I love you..."
                else:
                    the_mom "Oh, you really do need this [the_mom.mc_title]. I'll take care of this for you, leave it to mommy."
                "She wraps her fingers gently around your shaft and gives it a few experimental strokes."
                if not the_mom.outfit.tits_visible() and (the_mom.effective_sluttiness(["underwear_nudity","bare_tits"]) > 25 or the_mom.get_opinion_score("showing her tits") > 0):
                    if the_mom.has_taboo(["underwear_nudity","bare_tits"]):
                        the_mom "This would probably be faster if you had some more... stimulation, right?"
                        the_mom "Let me take my breasts out... It's just to speed this along, there's nothing wrong about it."
                    else:
                        the_mom "Of course, you probably want to see mommy's tits. Let me get those out for you to look at."
                    "She lets go of your cock and steps back."
                    if the_mom.outfit.can_half_off_to_tits():
                        $ generalised_strip_description(the_mom, the_mom.outfit.get_half_off_to_tits_list(), half_off_instead = True)
                    else:
                        $ generalised_strip_description(the_mom, the_mom.outfit.get_tit_strip_list())
                    $ mc.change_locked_clarity(20)
                    the_mom "There, now you have something to ogle while I get you off."
                    if not the_mom.outfit.vagina_visible():
                        menu:
                            "Order her to strip completely" if the_mom.obedience >= 140:
                                mc.name "That's not enough for me. Get naked for me [the_mom.title]."
                                if the_person.has_taboo("bare_pussy"):
                                    the_mom "[the_mom.mc_title], I can't... I shouldn't do that."
                                    mc.name "Come on, I need to get off, and I need to see you naked to do that."
                                    mc.name "You're already jerking me off, it's not a big deal seeing you naked while you do it."
                                    mc.name "I'm going to be late if you keep stalling. Hurry up and get naked!"
                                    $ the_mom.change_obedience(5 + the_mom.get_opinion_score("being submissive"))
                                    "She takes a deep breath and starts to strip down."
                                else:
                                    $ the_mom.change_obedience(1 + the_mom.get_opinion_score("being submissive"))
                                    the_mom "Of course [the_mom.mc_title]. Whatever you need me to do to make you cum I'll do it."
                                $ remove_shoes = False
                                $ item = the_mom.outfit.get_feet_top_layer()
                                if item:
                                    the_mom "Do you want me to keep my [item.display_name] on?"
                                    menu:
                                        "Strip it all off":
                                            mc.name "Take it all off, I don't want you to be wearing anything."
                                            $ remove_shoes = True

                                        "Leave them on":
                                            mc.name "You can leave them on."
                                $ del item

                                $ generalised_strip_description(the_mom, the_mom.outfit.get_full_strip_list(strip_feet = remove_shoes))
                                $ mc.change_locked_clarity(20)
                                if the_mom.break_taboo("bare_pussy"):
                                    the_mom "There. I guess this isn't so strange, really. Now, where were we..."
                                else:
                                    the_mom "There you go [the_mom.mc_title], now enjoy my naked body while I stroke you off."

                            "Order her to strip completely\n{size=16}{color=#FF0000}Requires: 140 Obedience{/color}{/size} (disabled)" if the_mom.obedience < 140:
                                pass

                            "Ogle her tits":
                                pass
                    "She wraps her fingers around your shaft again and starts to stroke it."

                else:
                    pass

                the_mom "You've got a date to keep, so cum quickly, okay?"
                call fuck_person(the_mom, start_position = handjob, skip_intro = True, girl_in_charge = True, position_locked = True) from _call_fuck_person_100
                $ the_report = _return
                if the_report.get("guy orgasms", 0) > 0:
                    the_mom "There we go [the_mom.mc_title], all taken care of. Now I don't have to worry about you getting into trouble while you're out."
                    "She gives you a happy smile."
                    $ the_mom.change_slut_temp(2)
                    $ the_mom.change_love(2)
                    $ the_mom.draw_person()
                    the_mom "Now go on, you've got a date to keep. Have fun out there, okay?"
                    mc.name "Thanks [the_mom.title], I will."
                    "You stuff your cock back in your pants and get ready to leave."
                    the_mom "Wait, one last thing..."
                    $ the_mom.draw_person(position = "kissing", special_modifier = "kissing")
                    "She hurries over to you and kisses you, deeply and passionately."
                    $ the_mom.draw_person()
                    the_mom "Mmm... Remember, Mommy loves you and will always be here for you."
                    mc.name "I love you too [the_mom.title]. See you later."

                else:
                    the_mom "I'm sorry [the_mom.mc_title], I just don't have the energy to finish you off. I need more practice I guess."
                    "She seems rather disappointed in herself."
                    $ the_mom.change_slut_temp(1)
                    $ the_mom.draw_person()
                    mc.name "We can work on that. Thanks for trying [the_mom.title], it was still nice."
                    "[the_mom.possessive_title] gives you a weak smile."
                    the_mom "Go on, you've got a date to keep. Have fun out there."
                $ the_mom.break_taboo("touching_penis")
                $ the_mom.update_outfit_taboos()
                $ the_mom.apply_outfit()
                "You hurry out of the house to meet [the_date.title]."
                $ clear_scene()
                return False

            "Tell her no":
                mc.name "Sorry [the_mom.title], but I'm going to pass."
                if the_mom.has_taboo("touching_penis"):
                    the_mom "Of course! It's not right, I'm your mother and I shouldn't... How could I even suggest that!"
                    mc.name "Relax, it's fine. I don't think it's a bad idea, but I might need my energy for later tonight."
                    the_mom "Oh, I... Oh [the_mom.mc_title], please promise me you'll be safe, at the very least."
                    mc.name "I will [the_mom.title], I promise."
                    $ the_mom.change_slut_temp(2)
                    the_mom "Well, if that's what you're planning... Be sure to show her a good time. Don't be selfish, girls don't like that."
                    mc.name "Okay [the_mom.title], I'll do that."
                else:
                    mc.name "Depending on how the date goes I might need all my energy for later tonight."
                    the_mom "Oh [the_mom.mc_title], well..."
                    $ the_mom.change_slut_temp(1)
                    the_mom "In that case, be sure to show her a good time. Don't be selfish, girls don't like that."
                    mc.name "Noted, thanks [the_mom.title]."
                $ the_mom.draw_person()
                "She stands up and moves to the door."
                the_mom "Don't be out too late, I worry when I don't know where you are. Love you sweetheart."
                mc.name "Love you too [the_mom.title]."
                $ clear_scene()
                return False

    else:
        the_mom "That's nice, I'm sure you'll have a wonderful time together."
        the_mom "Don't stay out too late, and make sure you use protection if you two are going to..."
        "She blushes and shrugs."
        the_mom "You know."
        mc.name "Relax [the_mom.title], I'm not a little kid."
        the_mom "I know. Oh lord, do I know. You've grown up into such a fine man, I just... hate to think of you leaving."
        the_mom "Come here, I need a hug."
        "[the_mom.possessive_title] pulls you into her arms. She rests her head on your shoulder while you hold her."
        "You're silent for a few moments, then she steps back and holds you at arms length."
        $ the_mom.change_love(1)
        the_mom "I love you sweetheart. Have a good night."
        mc.name "I love you too [the_mom.title]. I'll see you later."
        $ clear_scene()
        return False #Returns False if the date was not intercepted.
    return False

init -2 python:
    def create_mom_office_secretary():
        secretary = create_random_person()
        secretary.generate_home()
        secretary.home.add_person(secretary)
        secretary.set_work(mom_office_lobby, work_times = [1,2])
        mc.business.event_triggers_dict["mom_office_secretary"] = secretary.identifier
        return secretary

    def get_mom_secretary():
        identifier = mc.business.event_triggers_dict.get("mom_office_secretary", None)
        if not identifier:
            return create_mom_office_secretary()
        return next((x for x in all_people_in_the_game() if x.identifier == identifier), None)

    def get_mom_office_actions():
        ask_for_actions = ["Ask for someone"]
        other_actions = ["Other", "Leave"]

        ask_for_actions.append(mom)
        if mom.event_triggers_dict.get("mom_promotion_boss_phase_one", False) and mom.event_triggers_dict.get("mom_replacement_approach", None) is None:
            ask_for_actions.append([mom.title + "'s Boss","Boss"])
        return [ask_for_actions, other_actions]


label mom_office_person_request():
    $ the_person = get_mom_secretary()
    $ the_person.draw_person(position = "sitting")
    "You walk up to the reception desk. The receptionist looks up at you."
    the_person "Hello, can I help you? Do you have an appointment?"

    if "action_mod_list" in globals():
        call screen enhanced_main_choice_display(build_menu_items(get_mom_office_actions(), draw_person_previews = False, draw_hearts_for_people = False))
    else:
        call screen main_choice_display(get_mom_office_actions(), draw_person_previews = False, draw_hearts_for_people = False)

    if _return == "Leave":
        mc.name "Sorry to bother you."
        $ clear_scene()
    elif _return == "Boss":
        call mom_promotion_boss_phase_one(the_person) from _call_mom_promotion_boss_phase_one

    else:
        mc.name "I'm here to see Ms. [mc.last_name]. Can you let her know I'm here?"
        the_person "Of course, one moment."
        "The receptionist picks up her phone and calls someone. After a brief quiet conversation she hangs up."
        if mom_offices.has_person(mom):
            the_person "She's coming down right now to meet you."
            "After a brief wait [mom.title] steps out of the elevator banks and smiles happily at you."
            $ mom_offices.move_person(mom,mom_office_lobby)
            $ clear_scene()
            $ mom.draw_person() #TODO: Make sure she's wearing her work uniform.
            mom "Hi [mom.mc_title], did you need me for something?"
            call talk_person(mom) from _call_talk_person_25

        else:
            the_person "I'm sorry, but she doesn't seem to be in the building at the moment."
            mc.name "Right, okay. Sorry to bother you."
    return

label breeding_mom_label(the_person):
    #TODO: This event. Enabled by an LTE that can trigger at high Love and Sluttiness, greatly impacted by high Fertility.
    #TODO: Starts by talking to her in her room.

    mc.name "I've got some spare time [the_person.title], want to try for that baby again?"
    $ wants_breeding = True
    if the_person.effective_sluttiness() >= the_person.get_no_condom_threshold(): #Slutty enough that she'd fuck you raw any time, no big deal just comment on it
        if the_person.fertility_percent >= 70: #Crazy high fertility
            the_person "Oh [the_person.mc_title], how did you know just what I was thinking?"
            the_person "It might sound crazy, but my entire body just feels ready for breeding today!"
            the_person "I'll probably be knocked up the second you cum inside me, but you should still try and do it a few times, okay?"
            $ mc.change_locked_clarity(30)
            the_person "Really fill me up with cum so we can be sure!"


        elif the_person.fertility_percent >= 20: #High fertility. She's "Feeling ready".
            the_person "Of course I do [the_person.mc_title]!"
            $ mc.change_locked_clarity(20)
            the_person "I've got a good feeling about today! Make sure to cum nice and deep, I want the best chances of getting pregnant!"

        elif the_person.days_from_ideal_fertility() <= 3:
            the_person "Of course I do [the_person.mc_title]!"
            the_person "The key to breeding is consistency. Each time you cum inside me is another chance for me to get knocked up."
            $ mc.change_locked_clarity(30)
            the_person "It's the right time of the month too, so keep me filled up and I'll be pregnant in no time!"

        else: #Not likely to work, but she'll give it a try anyways because it's fun. I mean, because it's necessary...
            the_person "She pauses to think for a moment, then shrugs and nods."
            the_person "It's not the right time of the month, but there's no harm in trying!"
            $ mc.change_locked_clarity(10)
            the_person "It's a fun time either way, and if I get knocked up then even better!"

    else:  #Ie. she's not slutty enough to fuck you without a condom usually. Probably comes up because of massive fertility
        if the_person.days_from_ideal_fertility() <= 3: #ie. one week out of the month. She's fertile enough that she wants to try.
            "She thinks for a moment, then nods."
            the_person "It's the right time of the month for me, we should try as much as possible."
            the_person "Well then, let's get to it!"
        else:
            "She thinks for a moment, then shakes her head."
            the_person "It's not the right time of the month for me. We need to wait until it's likely to work, okay?"
            $ wants_breeding = False
            menu:
                "Fuck her anyways" if the_person.obedience >=140:
                    mc.name "You want to get you knocked up [the_person.title], and every load I put inside of you is one more chance for that to happen."
                    $ mc.change_locked_clarity(10)
                    "You reach around her and grab her ass, squeezing it hard. She moans, but doesn't try to pull away"
                    mc.name "So I need to get inside of you and pump you full of cum as often as possible. Even if it's not likely to knock you up."
                    the_person "I suppose that makes sense... Okay, you're right, as usual."
                    $ wants_breeding = True

                "Fuck her anyways\n{color=#ff0000}{size=18}Requires: 140 Obedience{/size}{/color}" if the_person.obedience < 140:
                    pass

                "Try some other time":
                    mc.name "We'll have to try some other time then."
                    "She nods happily."
                    the_person "There's nothing I want more, [the_person.mc_title], than to get pregnant and be a mother all over again."

    if wants_breeding:
        # Option to give her some serum (ie. ability to give her some fertility stuff right away)."
        if mc.inventory.get_any_serum_count():
            menu:
                "Give her some serum":
                    mc.name "Before we get started, I have something for you."
                    the_person "You do? What does it do?"
                    mc.name "It'll help you get pregnant. You want the best chance possible, right?"
                    "She nods eagerly and and waits for you to hand something over."
                    call give_serum(the_person)
                    if _return is not None:
                        "[the_person.title] takes the vial of serum and drinks it down as quickly as she can."
                    else:
                        mc.name "I must have left it at the office."
                        the_person "Bring it for me next time. Until then..."

                "Don't give her anything":
                    pass

        $ strip_list = the_person.get_full_strip_list()
        $ generalised_strip_description(the_person, strip_list)
        $ the_person.draw_person(position = "missionary")
        "[the_person.possessive_title] lies down her bed and spreads her legs, waiting for you."
        menu:
            "Fuck her":
                "You pull down your pants and get your hard cock out. You climb onto [the_person.title]'s bed and fit your hips between her legs."
                the_person "Get inside me [the_person.mc_title], come fuck your mother."
                "She reaches down and holds onto your shaft, rubbing the tip of your cock against her pussy lips. She strokes your cheek lovingly with her other hand."
                "You push forward, sinking your dick inside of her. Her eyes flutter and she gasps softly."
                the_person "Oh [the_person.title]..."
                call fuck_person(the_person, start_position = missionary, start_object = mc.location.get_object_with_name("bed"), skip_intro = True, skip_condom = True)
                $ sex_record = _return

            "Have her suck you off first":
                mc.name "Not so fast [the_person.title], I need you to get me ready first."
                "You pull your cock out and present it to her."
                mc.name "Get me hard and wet, I'll be sure to slide into you before I cum."
                the_person "Of course [the_person.mc_title], right away!"
                $ the_person.draw_person(position = "blowjob")
                $ mc.change_locked_clarity(20)
                "She swings her legs off of the bed and gets onto her knees in front of you. She holds onto your shaft with one hand and slips your tip into her mouth eagerly."
                call fuck_person(the_person, start_position = blowjob, skip_intro = True, skip_condom = True)
                $ sex_record = _return


        if sex_record.get("creampies", 0) >= 3:
            "[the_person.title] puts a hand between her legs, gasping as it touches the hot cum still rushing out of her overflowing pussy."
            the_person "Oh god, there's so much! I want it all inside me but there's just too much!"
            $ mc.change_locked_clarity(50)
            "She quivers gently with pleasure, and even that small movement sends a pulse of your cum gushing out of her and onto the bed."
            $ the_person.change_slut_temp(1 + 3*the_person.get_opinion_score("creampies"))
            $ the_person.change_happiness(15 + 5*the_person.get_opinion_score("creampies"))
        elif sex_record.get("creampies", 0) == 2:
            "[the_person.title] puts a hand between her legs, gasping when it touches her cum covered cunt."
            the_person "Oh, there's so much! You did such a good job [the_person.mc_title]."
            $ mc.change_locked_clarity(40)
            "She slips her middle finger inside her pussy and holds it there, keeping all of your seed trapped inside."
            $ the_person.change_slut_temp(1 + 2*the_person.get_opinion_score("creampies"))
            $ the_person.change_happiness(10 + 5*the_person.get_opinion_score("creampies"))
        elif sex_record.get("creampies", 0) == 1:
            $ mc.change_locked_clarity(20)
            "[the_person.title] puts a hand between her legs, petting her slit with her middle finger."
            the_person "Mmm, I can feel it deep inside me. Now I just have to hope I'm lucky."
            $ the_person.change_slut_temp(1 + 1*the_person.get_opinion_score("creampies"))
            $ the_person.change_happiness(5 + 5*the_person.get_opinion_score("creampies"))
        elif sex_record.get("guy orgasms", 0) > 0: #You came, but not inside her. She's pissed."
            the_person "You're not... done, are you?"
            mc.name "Sorry [the_person.title], but I just can't keep going."
            "[the_person.possessive_title] scowls at you."
            the_person "[the_person.mc_title], you said you were going to cum inside of me. That was our deal."
            the_person "If you were tired and couldn't finish, or even if you came inside me after, that would have been fine."
            the_person "But this... This just feels selfish."
            mc.name "I said I was sorry, I..."
            "She waves a hand and cuts you off."
            the_person "Forget it, just... Let's get dressed."
            $ the_person.change_happiness(-10)
            $ the_person.change_love(-2)
            $ the_person.apply_outfit()
            $ the_person.draw_person()
        else: #You couldn't cum. She's disappointed, but not angry
            the_person "Wait, you're not... finished already, are you?"
            mc.name "Sorry [the_person.title], but I just can't keep going."
            "She sighs and frowns. She doesn't seem angry, but she does seem disappointed."
            $ the_person.change_happiness(-10)
            the_person "Well, I suppose there's nothing you can do about it now... Try and save your energy for next time, okay?"
            mc.name "Okay [the_person.title], I will."

    else:
        pass
    #TODO: Have a girlfriend analog to this where she approaches you and tells you she wants to get pregnant. Same basic idea, you can fuck her and cum inside of her whenever you want.
    #TODO: Have a crisis where Mom comes to you (or texts you) and begs you to fuck her, because it's her most fertile day (or just because her fertility percent is huge).
    return