## New visualization after refined preprocessing
![full](https://github.com/chocoluffy/redditQA/blob/master/3-Bipartite-Graph/results/full.png)

See my data preprocessing steps at [here](https://github.com/chocoluffy/redditQA/issues/1).

## Stats

Aggregate all subreddits yields result of length 17536, sort by the comments count involved, and slice the top 10% for analysis. Meaning, 1753 top subreddits, with each top 10000 comments concatenated as document. 

## Result Analysis

After applying tfidf weighted matrix, the result seems strange, as highly centered.

For subreddit:  food
its 100-dimension topic distribution vector: [ 
  0.00059416  0.09496453  0.00059416  0.00059416  0.00059416  0.17863321
  0.00059416  0.00059416  0.00059416  0.00059416  0.00059416  0.00059416
  0.00059416  0.00059416  0.00059416  0.00059416  0.00059416  0.00059416
  0.00059416  0.00059416  0.00059416  0.00059416  0.00059416  0.00059416
  0.00059416  0.00059416  0.00059416  0.00059416  0.00059416  0.09455455
  0.00059416  0.00059416  0.00059416  0.00059416  0.00059416  0.0579896
  0.00059416  0.01233819  0.00059416  0.00059416  0.00255502  0.00059416
  0.00059416  0.00059416  0.00059416  0.00059416  0.00059416  0.00059416
  0.00059416  0.00059416  0.00059416  0.00059416  0.00059416  0.00059416
  0.00059416  0.00059416  0.00059416  0.00059416  0.00059416  0.26822576
  0.0406464   0.00059416  0.00059416  0.00059416  0.00059416  0.00236835
  0.00059416  0.00059416  0.00059416  0.00059416  0.00059416  0.00059416
  0.00059416  0.00059416  0.00059416  0.01625865  0.00059416  0.00059416
  0.00059416  0.00059416  0.00059416  0.00059416  0.00059416  0.00059416
  0.00059416  0.00059416  0.00059416  0.00059416  0.00059416  0.00059416
  0.00059416  0.00059416  0.00059416  0.17858542  0.00059416  0.00059416
  0.00059416  0.00059416  0.00059416  0.00059416]
the dominant topic is:  59  with prob:  0.268225759386 
The topic words distribution vector: [(u'book', 0.0021412641639557777), (u'school', 0.0020023633433475284), (u'shes', 0.001964448962033231), (u'food', 0.0018984495498444885), (u'story', 0.0018858799679918571), (u'kid', 0.0018701277593627115), (u'happy_new', 0.0018595942859653538), (u'win', 0.0018548040808453916), (u'child', 0.0018533745081384557), (u'her', 0.0018529151533049953), (u'cat', 0.001774539496115292), (u'girl', 0.0017717986893578236), (u'class', 0.0016612548061929798), (u'app', 0.0016258010899753536), (u'new_year', 0.0016080510069601895), (u'night', 0.0016063324521158747), (u'photo', 0.0015854904707682934), (u'car', 0.0015782120783439356), (u'state', 0.0015754608155859771), (u'store', 0.0015631149515416682)]

### User Score Example

User name: necromundus 
{'topicvecs': defaultdict(<type 'dict'>, {u'funny': 59, u'chemicalreactiongifs': -1, u'gameofthrones': 59, u'pathofexile': 93, u'gifs': 59, u'aww': 59, u'science': 59, u'horror': 5, u'Metal': 59, u'AskReddit': 59, u'pics': 59, u'movies': 93, u'AdviceAnimals': 59, u'futurama': 93, u'food': 59, u'ImaginaryMonsters': -1, u'Unexpected': 59, u'gaming': 59, u'Dachshund': -1, u'todayilearned': 59}), 'contributions': defaultdict(<type 'int'>, {u'funny': 19, u'gameofthrones': 1, u'pathofexile': 4, u'gifs': 2, u'aww': 1, u'science': 1, u'horror': 3, u'Metal': 1, u'AdviceAnimals': 7, u'pics': 5, u'futurama': 2, u'movies': 10, u'AskReddit': 15, u'Unexpected': 2, u'food': 2, u'ImaginaryMonsters': 2, u'todayilearned': 2, u'gaming': 1, u'Dachshund': 2, u'chemicalreactiongifs': 1})} 0.505679660161

User name: agentnola 
{'topicvecs': defaultdict(<type 'dict'>, {u'CivPapacy': -1, u'Civcraft': 59, u'civ': 93, u'eu4': 93, u'pcmasterrace': 93, u'Senntisten': -1}), 'contributions': defaultdict(<type 'int'>, {u'CivPapacy': 17, u'Civcraft': 13, u'civ': 2, u'eu4': 2, u'pcmasterrace': 1, u'Senntisten': 4})} 0.539027035881
LOHare {'topicvecs': defaultdict(<type 'dict'>, {u'canada': 59, u'funny': 59, u'todayilearned': 59, u'pics': 59, u'CanadianForces': -1, u'AskReddit': 59}), 'contributions': defaultdict(<type 'int'>, {u'canada': 1, u'funny': 79, u'todayilearned': 1, u'pics': 2, u'CanadianForces': 3, u'AskReddit': 7})} 1.0

Almost centered at topic 59 and 93.

## After applying TF-IDF weighted matrix:

topic #0 (0.010): 0.008*chess + 0.000*victoria + 0.000*rug + 0.000*median + 0.000*tended + 0.000*stocking + 0.000*student_loan + 0.000*dessert + 0.000*loan + 0.000*kit

topic #1 (0.010): 0.005*fan + 0.004*car + 0.004*window + 0.004*bike + 0.004*driver + 0.004*beer + 0.004*update + 0.004*program + 0.004*running + 0.004*fit

topic #2 (0.010): 0.000*deck + 0.000*token + 0.000*creature + 0.000*hash + 0.000*siege + 0.000*penalty + 0.000*ceramic + 0.000*nail + 0.000*rigorous + 0.000*whip

topic #3 (0.010): 0.000*mob + 0.000*farming + 0.000*strawberry + 0.000*bleach + 0.000*reward + 0.000*dungeon + 0.000*guild + 0.000*pg + 0.000*qualification + 0.000*recipe

topic #4 (0.010): 0.000*ski + 0.000*vegetarian + 0.000*thor + 0.000*bass + 0.000*skiing + 0.000*mega + 0.000*trap + 0.000*pokemon + 0.000*sonic + 0.000*bitcoin

topic #5 (0.010): 0.005*player + 0.004*team + 0.003*season + 0.003*woman + 0.003*song + 0.003*mod + 0.002*sex + 0.002*men + 0.002*music + 0.002*playing

topic #6 (0.010): 0.000*dank + 0.000*pls + 0.000*meme + 0.000*dank_meme + 0.000*oc + 0.000*brigade + 0.000*inb4 + 0.000*giveaway + 0.000*donut + 0.000*smoking

topic #7 (0.010): 0.000*panda + 0.000*registered + 0.000*microsoft + 0.000*authority + 0.000*china + 0.000*70 + 0.000*barely + 0.000*printer + 0.000*arsenal + 0.000*captain

topic #8 (0.010): 0.000*charlie + 0.000*frank + 0.000*gang + 0.000*shirt + 0.000*climbing + 0.000*left_behind + 0.000*firefly + 0.000*balcony + 0.000*forest + 0.000*weirdly

topic #9 (0.010): 0.009*picky + 0.007*sims + 0.006*watch_tv + 0.006*bigotry + 0.005*brushing + 0.005*branded + 0.000*milestone + 0.000*buffet + 0.000*aspiration + 0.000*alabama

topic #10 (0.010): 0.000*oliver + 0.000*bunny + 0.000*arabic + 0.000*ign + 0.000*ra + 0.000*radically + 0.000*partying + 0.000*tank + 0.000*programmer + 0.000*piano

topic #11 (0.010): 0.016*kane + 0.015*striker + 0.014*chelsea + 0.012*liverpool + 0.011*winger + 0.010*stash + 0.009*stocking + 0.009*kindle + 0.008*spur + 0.008*lcd

topic #12 (0.010): 0.010*ir + 0.008*sp + 0.002*pony + 0.001*vinyl + 0.000*waterfall + 0.000*smoker + 0.000*smoke + 0.000*mattress + 0.000*sidewalk + 0.000*smoking

topic #13 (0.010): 0.031*shiny + 0.024*pokemon + 0.023*ditto + 0.013*mmo + 0.010*added + 0.006*giveaway + 0.002*pls + 0.002*crossing + 0.001*framerate + 0.001*hosted

topic #14 (0.010): 0.006*nigger + 0.005*ben + 0.000*detroit + 0.000*landlord + 0.000*engineering + 0.000*engineer + 0.000*giveaway + 0.000*beer + 0.000*boston + 0.000*ml

topic #15 (0.010): 0.000*mk + 0.000*lord + 0.000*egg + 0.000*snake + 0.000*fam + 0.000*jew + 0.000*supreme + 0.000*fetch + 0.000*kanye + 0.000*ceo

topic #16 (0.010): 0.000*montana + 0.000*shiny + 0.000*mp + 0.000*comcast + 0.000*liberal + 0.000*libertarian + 0.000*mt + 0.000*galaxy + 0.000*expansion + 0.000*transformer

topic #17 (0.010): 0.013*gpa + 0.011*virginity + 0.011*vi + 0.010*highschool + 0.010*raining + 0.008*tha + 0.008*dang + 0.007*socializing + 0.007*pretty_neat + 0.007*outgoing

topic #18 (0.010): 0.028*winston + 0.019*super_bowl + 0.018*quarterback + 0.014*blizzard + 0.014*rb + 0.010*ruler + 0.010*cardinal + 0.007*cb + 0.001*conference + 0.000*britain

topic #19 (0.010): 0.000*calorie + 0.000*cardio + 0.000*protein + 0.000*carbs + 0.000*dessert + 0.000*twice_week + 0.000*september + 0.000*socializing + 0.000*msg + 0.000*kickass

topic #20 (0.010): 0.000*orb + 0.000*pat + 0.000*dodge + 0.000*lane + 0.000*hero + 0.000*pokemon + 0.000*mech + 0.000*vita + 0.000*enemy + 0.000*rage

topic #21 (0.010): 0.008*16th + 0.005*duplicate + 0.005*re + 0.004*ignored + 0.003*rick + 0.000*fascist + 0.000*michigan + 0.000*ohio + 0.000*detroit + 0.000*ukraine

topic #22 (0.010): 0.013*watson + 0.011*leash + 0.011*si + 0.010*un + 0.010*buffet + 0.008*student_loan + 0.007*shoving + 0.006*ikea + 0.006*di + 0.005*mi

topic #23 (0.010): 0.000*dmg + 0.000*counselor + 0.000*hair + 0.000*mod + 0.000*curse + 0.000*dm + 0.000*nerf + 0.000*anxiety + 0.000*curl + 0.000*flop

topic #24 (0.010): 0.005*transitioning + 0.001*bigotry + 0.000*transgender + 0.000*trans + 0.000*gender + 0.000*talk_to + 0.000*transition + 0.000*suicidal + 0.000*razor + 0.000*tracker

topic #25 (0.010): 0.000*vape + 0.000*juice + 0.000*recipient + 0.000*coil + 0.000*quit_smoking + 0.000*smoking + 0.000*tobacco + 0.000*aspire + 0.000*cigarette + 0.000*smoked

topic #26 (0.010): 0.008*dart + 0.000*88 + 0.000*andy + 0.000*nerf + 0.000*larry + 0.000*headphone + 0.000*aw + 0.000*gore + 0.000*rec + 0.000*jerry

topic #27 (0.010): 0.000*meditation + 0.000*mindful + 0.000*vegan + 0.000*bacon + 0.000*fabric + 0.000*seam + 0.000*ruler + 0.000*superb + 0.000*stitch + 0.000*gp

topic #28 (0.010): 0.000*packer + 0.000*ordeal + 0.000*winston + 0.000*goodwill + 0.000*college_football + 0.000*cinnamon + 0.000*cooper + 0.000*ramen + 0.000*hot_dog + 0.000*thrift

topic #29 (0.010): 0.005*track + 0.004*truck + 0.004*dream + 0.004*eating + 0.004*heat + 0.004*smoking + 0.004*died + 0.004*center + 0.004*lord + 0.004*belief

topic #30 (0.010): 0.016*nba + 0.014*cole + 0.013*detroit + 0.012*davis + 0.011*vita + 0.010*walker + 0.009*dried + 0.009*lit + 0.009*rebound + 0.008*wade

topic #31 (0.010): 0.011*ethnicity + 0.009*racer + 0.006*privileged + 0.000*brewing + 0.000*tampa + 0.000*physician + 0.000*racing + 0.000*hm + 0.000*race + 0.000*davis

topic #32 (0.010): 0.000*villager + 0.000*pp + 0.000*plugin + 0.000*winger + 0.000*plugins + 0.000*sc + 0.000*map + 0.000*thus_far + 0.000*wrapper + 0.000*itunes

topic #33 (0.010): 0.000*verb + 0.000*vocabulary + 0.000*native + 0.000*arabic + 0.000*spanish + 0.000*language + 0.000*arab + 0.000*alabama + 0.000*english_speaker + 0.000*israel

topic #34 (0.010): 0.018*vinyl + 0.014*taller + 0.007*discretion + 0.006*reacting + 0.004*rigorous + 0.001*privileged + 0.000*ikea + 0.000*resting + 0.000*unattractive + 0.000*coyote

topic #35 (0.010): 0.007*sexy + 0.006*dog + 0.005*sent + 0.005*shoe + 0.005*racist + 0.005*pizza + 0.005*comic + 0.004*clothes + 0.004*giant + 0.004*pant

topic #36 (0.010): 0.009*thread_linked + 0.008*elsewhere_reddit + 0.008*herehttpwwwredditcommessagecomposeto2fr2fmetabotmailbag + 0.008*rule_of + 0.008*follow_any + 0.008*question_abuse + 0.008*respect_the + 0.008*above_link + 0.008*vote_or + 0.001*britain

topic #37 (0.010): 0.011*coach + 0.011*playoff + 0.009*football + 0.009*nfl + 0.009*jersey + 0.008*qb + 0.007*nexus + 0.006*league + 0.006*battery + 0.006*motor

topic #38 (0.010): 0.009*cat + 0.000*rat + 0.000*vita + 0.000*bisexual + 0.000*resembles + 0.000*bi + 0.000*racer + 0.000*gay + 0.000*vet + 0.000*sexuality

topic #39 (0.010): 0.000*dentist + 0.000*brushing + 0.000*tooth + 0.000*oc + 0.000*ic + 0.000*teeth + 0.000*gum + 0.000*armor + 0.000*tread + 0.000*armour

topic #40 (0.010): 0.011*mattress + 0.009*modifier + 0.009*depot + 0.008*flaming + 0.007*ow + 0.007*trivia + 0.006*dessert + 0.006*74 + 0.006*exploiting + 0.005*expands

topic #41 (0.010): 0.008*terry + 0.000*tapped + 0.000*resting + 0.000*raven + 0.000*bloke + 0.000*oc + 0.000*ir + 0.000*jim + 0.000*anthony + 0.000*sam

topic #42 (0.010): 0.031*action_performed + 0.030*i_botrautomoderatorcommentsq11puwhatisautomoderator + 0.030*botrautomoderatorcommentsq11puwhatisautomoderator + 0.030*contact_moderator + 0.030*automatically_please + 0.024*question_concern + 0.023*bitcoin + 0.021*moderator + 0.020*performed + 0.019*automatically

topic #43 (0.010): 0.013*verizon + 0.013*brewing + 0.010*sweetheart + 0.008*55 + 0.006*ordeal + 0.002*mayor + 0.000*ruler + 0.000*pedal + 0.000*uber + 0.000*surge

topic #44 (0.010): 0.016*original + 0.007*hinge + 0.006*thread + 0.000*freelance + 0.000*wall + 0.000*weight_loss + 0.000*elf + 0.000*av + 0.000*dwarf + 0.000*weight

topic #45 (0.010): 0.000*spiderman + 0.000*india + 0.000*slayer + 0.000*master_race + 0.000*wallpaper + 0.000*commie + 0.000*mormon + 0.000*religion + 0.000*freedom + 0.000*oc

topic #46 (0.010): 0.005*college_football + 0.000*osu + 0.000*vita + 0.000*psn + 0.000*ps3 + 0.000*spotify + 0.000*dang + 0.000*raider + 0.000*michigan + 0.000*console

topic #47 (0.010): 0.005*brandon + 0.005*worm + 0.004*smith + 0.003*fish + 0.001*source + 0.000*dip + 0.000*flyer + 0.000*ooc + 0.000*taylor + 0.000*civ

topic #48 (0.010): 0.003*1100 + 0.003*au + 0.002*johnny + 0.002*thoughtful + 0.002*paris + 0.002*hour_ago + 0.002*intellectual + 0.002*1500 + 0.002*38 + 0.002*miracle

topic #49 (0.010): 0.007*1998 + 0.004*50 + 0.003*p + 0.002*40 + 0.002*2014 + 0.002*cannot + 0.000*assist + 0.000*ir + 0.000*yahoo + 0.000*handsome

topic #50 (0.010): 0.000*arabic + 0.000*province + 0.000*vietnam + 0.000*war + 0.000*balcony + 0.000*fishing + 0.000*dota + 0.000*fish + 0.000*quote + 0.000*draft

topic #51 (0.010): 0.009*sb + 0.002*redeem + 0.000*referral + 0.000*homophobic + 0.000*towards_end + 0.000*na + 0.000*se + 0.000*da + 0.000*karma + 0.000*ne

topic #52 (0.010): 0.000*van + 0.000*dust + 0.000*cr + 0.000*bong + 0.000*accounting + 0.000*storage + 0.000*tax + 0.000*bryan + 0.000*faction + 0.000*smoke

topic #53 (0.010): 0.022*cooper + 0.013*rick + 0.000*brewing + 0.000*dessert + 0.000*walker + 0.000*jersey + 0.000*winger + 0.000*physician + 0.000*boxing + 0.000*towel

topic #54 (0.010): 0.007*referral + 0.000*shark + 0.000*perry + 0.000*duck + 0.000*ref + 0.000*watch_tv + 0.000*voltage + 0.000*bragging + 0.000*yeast + 0.000*remake

topic #55 (0.010): 0.005*blog + 0.005*ampnbsp + 0.004*root + 0.004*tumblr + 0.000*x2 + 0.000*racer + 0.000*dream + 0.000*dreaming + 0.000*dj + 0.000*rd

topic #56 (0.010): 0.021*oc + 0.010*britain + 0.009*edward + 0.007*rebuttal + 0.007*organizing + 0.006*pfft + 0.003*colder + 0.001*resembles + 0.001*knit + 0.001*kanye

topic #57 (0.010): 0.000*nursing + 0.000*slider + 0.000*crew + 0.000*bike + 0.000*milk + 0.000*nose + 0.000*nurse + 0.000*bottle + 0.000*skyrim + 0.000*coin

topic #58 (0.010): 0.000*verizon + 0.000*sprint + 0.000*furry + 0.000*bike + 0.000*coverage + 0.000*curry + 0.000*lamp + 0.000*faction + 0.000*referenced + 0.000*finale

topic #59 (0.010): 0.002*book + 0.002*school + 0.002*shes + 0.002*food + 0.002*story + 0.002*kid + 0.002*happy_new + 0.002*win + 0.002*child + 0.002*her

topic #60 (0.010): 0.005*album + 0.004*wall + 0.004*bottle + 0.004*v + 0.003*drinking + 0.003*ring + 0.003*league + 0.003*movie + 0.003*watched + 0.003*serious

topic #61 (0.010): 0.051*que + 0.048*de + 0.032*en + 0.018*la + 0.016*se + 0.010*lo + 0.008*knit + 0.008*el + 0.007*los + 0.006*ole

topic #62 (0.010): 0.000*fi + 0.000*debt + 0.000*ct + 0.000*dwarf + 0.000*carbs + 0.000*fund + 0.000*category + 0.000*student_loan + 0.000*income + 0.000*expense

topic #63 (0.010): 0.007*howard + 0.001*vinegar + 0.000*twice_week + 0.000*interrupt + 0.000*russia + 0.000*richard + 0.000*putin + 0.000*russian + 0.000*freshman_year + 0.000*yummy

topic #64 (0.010): 0.000*dye + 0.000*vinegar + 0.000*ted + 0.000*robin + 0.000*bra + 0.000*pvp + 0.000*nudity + 0.000*developer + 0.000*boob + 0.000*hue

topic #65 (0.010): 0.023*islam + 0.011*allah + 0.010*ritual + 0.010*sjws + 0.010*arabic + 0.009*sidewalk + 0.009*gilded + 0.009*physician + 0.008*vr + 0.008*challenged

topic #66 (0.010): 0.012*tapped + 0.000*compelled + 0.000*en + 0.000*du + 0.000*de + 0.000*dem + 0.000*que + 0.000*hitch + 0.000*se + 0.000*vi

topic #67 (0.010): 0.018*widget + 0.013*hm + 0.010*bulky + 0.009*master_race + 0.009*tyler + 0.009*icon + 0.009*spawned + 0.008*customize + 0.008*framework + 0.007*professionally

topic #68 (0.010): 0.012*conference + 0.011*pittsburgh + 0.011*transgender + 0.010*rap + 0.009*soccer + 0.009*september + 0.009*raider + 0.009*hip_hop + 0.008*rapper + 0.008*musical

topic #69 (0.010): 0.000*stream + 0.000*leash + 0.000*edmonton + 0.000*vlc + 0.000*map + 0.000*meme + 0.000*everybody_else + 0.000*verse + 0.000*coyote + 0.000*hover

topic #70 (0.010): 0.000*social_anxiety + 0.000*ui + 0.000*fascist + 0.000*rifle + 0.000*scope + 0.000*democracy + 0.000*anxiety + 0.000*kappa + 0.000*offline + 0.000*chat

topic #71 (0.010): 0.000*sentient + 0.000*awakening + 0.000*arizona + 0.000*patient + 0.000*nurse + 0.000*trailer + 0.000*fallacy + 0.000*skype + 0.000*personality + 0.000*subconscious

topic #72 (0.010): 0.006*milestone + 0.000*tit + 0.000*nude + 0.000*nipple + 0.000*yummy + 0.000*gifs + 0.000*sexy + 0.000*boob + 0.000*breast + 0.000*massive_amount

topic #73 (0.010): 0.007*resting + 0.000*cardio + 0.000*punk + 0.000*roast + 0.000*smoker + 0.000*vacuum + 0.000*duke + 0.000*marvel + 0.000*carolina + 0.000*belt

topic #74 (0.010): 0.006*er + 0.004*og + 0.004*der + 0.002*af + 0.000*bare + 0.000*fx + 0.000*downtown + 0.000*detroit + 0.000*poetry + 0.000*poem

topic #75 (0.010): 0.009*gender + 0.008*speaker + 0.007*suicide + 0.007*audio + 0.007*loan + 0.006*apply + 0.006*bass + 0.005*emotion + 0.005*loop + 0.005*recording

topic #76 (0.010): 0.014*char + 0.010*nacho + 0.001*dessert + 0.000*crunch + 0.000*msg + 0.000*taco + 0.000*slider + 0.000*tb + 0.000*salsa + 0.000*bean

topic #77 (0.010): 0.000*tea + 0.000*confirmed + 0.000*interstellar + 0.000*tf2 + 0.000*parade + 0.000*bullied + 0.000*museum + 0.000*steak + 0.000*csgo + 0.000*key

topic #78 (0.010): 0.000*watson + 0.000*intuition + 0.000*pronounce + 0.000*yoga + 0.000*language + 0.000*pronounced + 0.000*pronunciation + 0.000*tracker + 0.000*ethnicity + 0.000*smoking

topic #79 (0.010): 0.000*remix + 0.000*widget + 0.000*eleven + 0.000*boxing + 0.000*jones + 0.000*dc + 0.000*motor + 0.000*icon + 0.000*raider + 0.000*marcus

topic #80 (0.010): 0.010*pharmacy + 0.000*firefox + 0.000*german + 0.000*japanese + 0.000*25th + 0.000*lane + 0.000*shitpost + 0.000*soccer + 0.000*smith + 0.000*walker

topic #81 (0.010): 0.008*pepsi + 0.000*super_bowl + 0.000*lo + 0.000*comcast + 0.000*london + 0.000*furnace + 0.000*cole + 0.000*ranger + 0.000*wade + 0.000*wiring

topic #82 (0.010): 0.009*fascist + 0.000*socialist + 0.000*capitalism + 0.000*assassin + 0.000*creed + 0.000*capitalist + 0.000*socialism + 0.000*unity + 0.000*deleted_deleted + 0.000*islam

topic #83 (0.010): 0.004*sa + 0.003*pe + 0.000*legion + 0.000*si + 0.000*minimalist + 0.000*reign + 0.000*bryan + 0.000*brass + 0.000*bitcoin + 0.000*primer

topic #84 (0.010): 0.024*osu + 0.021*alabama + 0.015*ohio + 0.014*ohio_state + 0.011*oregon + 0.008*espn + 0.007*sec + 0.002*conference + 0.001*gpa + 0.001*freshman_year

topic #85 (0.010): 0.000*pittsburgh + 0.000*jay + 0.000*loan + 0.000*justin + 0.000*silicone + 0.000*dodgy + 0.000*feedback + 0.000*unexpected + 0.000*miniature + 0.000*survivor

topic #86 (0.010): 0.008*zen + 0.000*ml + 0.000*soccer + 0.000*goalie + 0.000*corsair + 0.000*next_season + 0.000*jersey + 0.000*nvidia + 0.000*amd + 0.000*keyboard

topic #87 (0.010): 0.007*inc + 0.000*123 + 0.000*tb + 0.000*she + 0.000*uv + 0.000*resting + 0.000*ow + 0.000*diaper + 0.000*biological + 0.000*jazz

topic #88 (0.010): 0.008*frowned + 0.007*frowned_upon + 0.000*lt + 0.000*hatch + 0.000*gag + 0.000*hacked + 0.000*m + 0.000*balcony + 0.000*van + 0.000*al

topic #89 (0.010): 0.007*rumour + 0.007*submitted + 0.005*piercing + 0.005*jewelry + 0.004*domain + 0.003*submission + 0.002*recent + 0.000*winston + 0.000*disney + 0.000*pea

topic #90 (0.010): 0.000*guild + 0.000*app + 0.000*dp + 0.000*fragment + 0.000*wire + 0.000*horde + 0.000*limp + 0.000*switch + 0.000*nt + 0.000*crow

topic #91 (0.010): 0.000*column + 0.000*excel + 0.000*ribbon + 0.000*int + 0.000*integer + 0.000*kane + 0.000*halo + 0.000*cardinal + 0.000*tall + 0.000*sexy

topic #92 (0.010): 0.000*bread + 0.000*recipe + 0.000*bake + 0.000*x2 + 0.000*baking + 0.000*yeast + 0.000*employer + 0.000*derivative + 0.000*dough + 0.000*resume

topic #93 (0.010): 0.002*server + 0.002*price + 0.002*trade + 0.002*city + 0.002*company + 0.002*hot + 0.002*2015 + 0.002*police + 0.002*map + 0.002*item

topic #94 (0.010): 0.006*fc + 0.002*dan + 0.001*omega + 0.000*laura + 0.000*blizzard + 0.000*diablo + 0.000*pvp + 0.000*batman + 0.000*nip + 0.000*arabic

topic #95 (0.010): 0.012*xx + 0.011*xxx + 0.000*frowned + 0.000*ac + 0.000*int + 0.000*nvidia + 0.000*dmg + 0.000*amd + 0.000*marine + 0.000*snap

topic #96 (0.010): 0.017*simon + 0.013*sip + 0.004*lewis + 0.000*brushing + 0.000*traded + 0.000*confirmed + 0.000*delusional + 0.000*python + 0.000*android + 0.000*api

topic #97 (0.010): 0.000*miami + 0.000*korean + 0.000*bench + 0.000*avenger + 0.000*comic + 0.000*story_short + 0.000*lvl + 0.000*squat + 0.000*sprint + 0.000*chili

topic #98 (0.010): 0.000*swimming + 0.000*swim + 0.000*irish + 0.000*jail + 0.000*packaging + 0.000*british + 0.000*student_loan + 0.000*2k + 0.000*cell + 0.000*product

topic #99 (0.010): 0.016*bryan + 0.001*debut + 0.001*tyler + 0.000*cole + 0.000*stability + 0.000*daniel + 0.000*alien + 0.000*dough + 0.000*band + 0.000*stone