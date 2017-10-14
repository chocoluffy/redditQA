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

## After applying TF-IDF weights and de-normalization:

![compare](https://github.com/chocoluffy/redditQA/blob/master/4-LDA-On-Tfidf/results/compare.png)

topic #0 (0.010): 0.020*pokemon + 0.010*shiny + 0.010*mega + 0.006*x2 + 0.004*episode + 0.004*iv + 0.004*jerry + 0.004*hp + 0.003*trainer + 0.003*orb

topic #1 (0.010): 0.011*recipe + 0.008*meat + 0.008*cheese + 0.007*sauce + 0.007*steak + 0.007*pan + 0.007*pepper + 0.007*bread + 0.006*chicken + 0.006*egg

topic #2 (0.010): 0.009*muslim + 0.007*war + 0.006*islam + 0.006*israel + 0.005*nation + 0.005*arab + 0.005*russia + 0.005*empire + 0.005*ayy + 0.004*army

topic #3 (0.010): 0.013*cpu + 0.009*amd + 0.009*ram + 0.008*pc + 0.008*intel + 0.008*motherboard + 0.008*gpu + 0.006*nvidia + 0.006*hdd + 0.005*ssd

topic #4 (0.010): 0.005*mod + 0.005*spawn + 0.005*block + 0.005*zombie + 0.004*ship + 0.004*minecraft + 0.004*server + 0.003*mining + 0.003*portal + 0.003*dwarf

topic #5 (0.010): 0.009*gym + 0.008*weight + 0.008*squat + 0.007*workout + 0.006*muscle + 0.005*lift + 0.005*lifting + 0.005*bench + 0.004*training + 0.004*yoga

topic #6 (0.010): 0.007*rug + 0.007*tent + 0.004*forest + 0.003*dildo + 0.003*erase + 0.003*aka + 0.003*pet + 0.003*sand + 0.003*towel + 0.003*bong

topic #7 (0.010): 0.007*jay + 0.005*channel + 0.005*video + 0.004*starbucks + 0.003*coffee + 0.003*ampnbsp + 0.003*figure + 0.003*co2 + 0.003*neckbeard + 0.003*record

topic #8 (0.010): 0.008*cube + 0.006*episode + 0.004*snake + 0.004*marvel + 0.004*blog + 0.004*javascript + 0.004*tumblr + 0.004*star_war + 0.003*r + 0.003*python

topic #9 (0.010): 0.026*bitcoin + 0.013*beer + 0.010*coin + 0.007*bottle + 0.006*tea + 0.006*scam + 0.006*seller + 0.005*listing + 0.005*buyer + 0.004*price

topic #10 (0.010): 0.008*voltage + 0.007*tank + 0.007*coil + 0.007*battery + 0.007*wire + 0.006*speaker + 0.005*juice + 0.005*circuit + 0.004*output + 0.004*cable

topic #11 (0.010): 0.007*vr + 0.004*email + 0.003*admins + 0.003*employee + 0.003*product + 0.003*company + 0.003*gamestop + 0.003*store + 0.002*oculus + 0.002*customer

topic #12 (0.010): 0.010*team + 0.008*nba + 0.007*season + 0.005*player + 0.005*basketball + 0.005*smith + 0.005*foul + 0.004*curry + 0.004*coach + 0.004*raptor

topic #13 (0.010): 0.004*code + 0.004*language + 0.004*engineering + 0.004*c + 0.004*programming + 0.004*project + 0.004*data + 0.003*engineer + 0.003*math + 0.003*programmer

topic #14 (0.010): 0.026*cat + 0.006*rat + 0.004*hair + 0.003*towel + 0.003*pizza + 0.003*glitch + 0.003*cooper + 0.003*wr + 0.003*duck + 0.003*dog

topic #15 (0.010): 0.006*woman + 0.005*men + 0.004*feminist + 0.003*feminism + 0.003*society + 0.003*culture + 0.003*argument + 0.003*racist + 0.002*racism + 0.002*government

topic #16 (0.010): 0.007*police + 0.006*cop + 0.005*law + 0.005*officer + 0.004*lawyer + 0.004*crime + 0.003*arrest + 0.003*court + 0.002*legal + 0.002*victim

topic #17 (0.010): 0.021*comcast + 0.020*sprint + 0.007*bird + 0.007*shirt + 0.005*coverage + 0.005*cable + 0.005*bow + 0.005*pole + 0.005*atampt + 0.004*cage

topic #18 (0.010): 0.019*car + 0.008*engine + 0.008*wheel + 0.008*tire + 0.005*rear + 0.005*truck + 0.004*vehicle + 0.003*mile + 0.003*honda + 0.003*drive

topic #19 (0.010): 0.013*xx + 0.007*hunter + 0.006*doctor + 0.005*xxx + 0.005*tribe + 0.004*lord + 0.004*x + 0.004*dvd + 0.004*pp + 0.004*melee

topic #20 (0.010): 0.005*toilet + 0.004*egg + 0.004*av + 0.004*sydney + 0.004*sr + 0.004*dun + 0.004*skate + 0.003*jake + 0.002*water + 0.002*glitch

topic #21 (0.010): 0.024*sexy + 0.013*cock + 0.012*hot + 0.010*tit + 0.008*cute + 0.008*gorgeous + 0.008*as + 0.008*deleted_deleted + 0.007*pic + 0.007*beautiful

topic #22 (0.010): 0.013*torrent + 0.012*http + 0.011*vpn + 0.007*sam + 0.007*youtube + 0.006*channel + 0.006*copyright + 0.005*anthony + 0.004*video + 0.004*isp

topic #23 (0.010): 0.015*dog + 0.007*vet + 0.005*cat + 0.005*landlord + 0.004*trail + 0.004*puppy + 0.004*shelter + 0.003*breed + 0.003*pet + 0.003*animal

topic #24 (0.010): 0.016*liberal + 0.014*libertarian + 0.013*conservative + 0.013*republican + 0.011*democrat + 0.005*election + 0.005*government + 0.005*political + 0.005*party + 0.004*marriage

topic #25 (0.010): 0.005*jeremy + 0.004*murray + 0.004*shoe + 0.004*sol + 0.004*2k + 0.004*ea + 0.004*film + 0.003*helm + 0.003*psn + 0.003*movie

topic #26 (0.010): 0.011*guild + 0.008*pvp + 0.006*fc + 0.004*player + 0.004*dp + 0.004*server + 0.004*dungeon + 0.004*mod + 0.003*class + 0.003*raid

topic #27 (0.010): 0.009*trade + 0.009*ex + 0.008*howard + 0.008*88 + 0.007*dog + 0.007*card + 0.007*pack + 0.005*8 + 0.005*gp + 0.004*superb

topic #28 (0.010): 0.017*tb + 0.015*gg + 0.013*duck + 0.008*shark + 0.007*og + 0.005*perry + 0.005*old_school + 0.005*hawk + 0.004*charity + 0.004*team

topic #29 (0.010): 0.005*relationship + 0.003*sex + 0.003*woman + 0.002*her + 0.002*feeling + 0.002*partner + 0.002*talk + 0.002*anxiety + 0.002*girl + 0.002*parent

topic #30 (0.010): 0.007*city + 0.006*downtown + 0.004*uber + 0.004*park + 0.003*taxi + 0.003*street + 0.003*driver + 0.003*cab + 0.003*bus + 0.003*neighborhood

topic #31 (0.010): 0.014*language + 0.011*german + 0.009*english + 0.007*germany + 0.006*japanese + 0.006*american + 0.006*korean + 0.006*chinese + 0.005*japan + 0.005*spanish

topic #32 (0.010): 0.007*anchor + 0.007*axis + 0.005*dock + 0.005*hog + 0.005*screw + 0.004*missile + 0.004*drone + 0.004*motor + 0.004*carrier + 0.003*fiber

topic #33 (0.010): 0.009*jean + 0.006*wear + 0.005*shoe + 0.005*pair + 0.005*wearing + 0.005*pant + 0.004*fit + 0.004*leather + 0.004*clothes + 0.003*vinyl

topic #34 (0.010): 0.003*character + 0.003*ai + 0.003*quest + 0.003*weapon + 0.003*player + 0.003*combat + 0.002*dlc + 0.002*gameplay + 0.002*ship + 0.002*played

topic #35 (0.010): 0.009*tracker + 0.003*nigga + 0.003*girl + 0.003*tree + 0.002*ugly + 0.002*route + 0.002*sprite + 0.002*torrent + 0.002*imgur + 0.002*limb

topic #36 (0.010): 0.023*alien + 0.023*sims + 0.011*oliver + 0.009*hair + 0.006*ceo + 0.006*norway + 0.005*ra + 0.004*canadian + 0.003*arrow + 0.003*harper

topic #37 (0.010): 0.014*lego + 0.011*ps3 + 0.010*ps4 + 0.008*sony + 0.007*code + 0.007*xbox + 0.006*psn + 0.006*360 + 0.005*console + 0.005*destiny

topic #38 (0.010): 0.008*girl + 0.007*condom + 0.007*sex + 0.006*woman + 0.004*dick + 0.004*her + 0.003*gay + 0.003*sexual + 0.003*men + 0.003*shes

topic #39 (0.010): 0.006*cod + 0.005*outfit + 0.004*ui + 0.003*grip + 0.003*aw + 0.003*nc + 0.003*faggot + 0.003*prompt + 0.003*server + 0.003*pilot

topic #40 (0.010): 0.013*player + 0.012*team + 0.009*season + 0.008*club + 0.008*league + 0.007*chelsea + 0.007*kane + 0.006*liverpool + 0.006*goal + 0.005*football

topic #41 (0.010): 0.016*pipe + 0.016*kindle + 0.013*soil + 0.010*amazon + 0.009*radiation + 0.006*bottle + 0.006*plant + 0.006*tobacco + 0.006*coffee + 0.005*creepy

topic #42 (0.010): 0.007*drug + 0.004*heroin + 0.004*weed + 0.004*dose + 0.003*alcohol + 0.003*doctor + 0.003*patient + 0.003*medical + 0.003*trip + 0.003*med

topic #43 (0.010): 0.012*coin + 0.008*card + 0.007*runner + 0.006*pack + 0.005*vita + 0.005*fate + 0.005*5k + 0.004*sting + 0.004*mint + 0.004*milestone

topic #44 (0.010): 0.007*trans + 0.006*gay + 0.004*gender + 0.003*bisexual + 0.003*transgender + 0.003*sexuality + 0.003*sex + 0.003*lgbt + 0.002*woman + 0.002*religious

topic #45 (0.010): 0.005*log + 0.004*episode + 0.004*cube + 0.004*boob + 0.003*shes + 0.003*romantic + 0.003*body + 0.003*screen + 0.003*her + 0.003*relationship

topic #46 (0.010): 0.015*book + 0.006*writing + 0.005*character + 0.005*novel + 0.005*author + 0.005*reader + 0.005*series + 0.005*reading + 0.004*writer + 0.004*story

topic #47 (0.010): 0.013*jersey + 0.006*colt + 0.006*packer + 0.005*team + 0.005*season + 0.004*eagle + 0.004*dentist + 0.004*nfl + 0.004*giant + 0.004*denver

topic #48 (0.010): 0.007*couldve + 0.007*ted + 0.007*donut + 0.005*robin + 0.004*commie + 0.003*host + 0.003*diablo + 0.003*fat + 0.003*hosting + 0.003*15_minute

topic #49 (0.010): 0.009*app + 0.007*apps + 0.007*device + 0.007*phone + 0.007*android + 0.006*file + 0.005*nexus + 0.004*battery + 0.004*linux + 0.004*screen

topic #50 (0.010): 0.016*she + 0.010*ooc + 0.004*smile + 0.004*nod + 0.004*grin + 0.003*kiss + 0.002*walk + 0.002*door + 0.002*her + 0.002*hug

topic #51 (0.010): 0.012*kit + 0.007*paint + 0.007*ship + 0.006*razor + 0.005*shaving + 0.005*shave + 0.005*chapter + 0.005*blade + 0.005*model + 0.005*pls

topic #52 (0.010): 0.017*ooc + 0.012*headphone + 0.009*meme + 0.009*oc + 0.007*ic + 0.006*boot + 0.006*greek + 0.006*chapter + 0.005*happy_birthday + 0.005*leather

topic #53 (0.010): 0.025*pepsi + 0.009*freshman_year + 0.009*high_school + 0.008*trans + 0.008*costume + 0.008*blender + 0.008*freshman + 0.006*arm + 0.005*hair + 0.005*school

topic #54 (0.010): 0.026*gun + 0.008*firearm + 0.006*purse + 0.006*safety + 0.005*weapon + 0.004*concealed + 0.003*carry + 0.003*gang + 0.003*homeless + 0.003*dawn

topic #55 (0.010): 0.009*mario + 0.008*nintendo + 0.008*3d + 0.007*zelda + 0.007*wii + 0.004*console + 0.004*smash + 0.004*disc + 0.004*gamestop + 0.003*controller

topic #56 (0.010): 0.011*hair + 0.010*makeup + 0.009*lip + 0.008*brow + 0.007*chord + 0.006*polish + 0.006*palette + 0.006*eyebrow + 0.006*skin + 0.006*color

topic #57 (0.010): 0.009*boxing + 0.006*silver + 0.006*dip + 0.005*fight + 0.005*map + 0.005*slayer + 0.004*archer + 0.004*fighter + 0.004*developer + 0.004*shield

topic #58 (0.010): 0.012*hockey + 0.011*nhl + 0.008*puck + 0.007*team + 0.006*hawk + 0.006*ref + 0.005*goalie + 0.005*skate + 0.005*cap + 0.005*ice

topic #59 (0.010): 0.032*deck + 0.015*card + 0.010*mana + 0.006*creature + 0.006*token + 0.004*opponent + 0.004*minion + 0.004*dragon + 0.003*spell + 0.003*meta

topic #60 (0.010): 0.023*original + 0.013*snake + 0.013*swim + 0.012*swimming + 0.012*sip + 0.011*civ + 0.010*rust + 0.009*mp + 0.008*thread + 0.007*verse

topic #61 (0.010): 0.006*tax + 0.005*income + 0.004*loan + 0.004*fund + 0.004*company + 0.004*debt + 0.004*market + 0.003*business + 0.003*bank + 0.003*pay

topic #62 (0.010): 0.017*action_performed + 0.017*i_botrautomoderatorcommentsq11puwhatisautomoderator + 0.017*automatically_please + 0.017*contact_moderator + 0.017*botrautomoderatorcommentsq11puwhatisautomoderator + 0.015*moderator + 0.014*question_concern + 0.013*automatically + 0.013*performed + 0.008*tag

topic #63 (0.010): 0.008*smash + 0.007*character + 0.006*usa + 0.006*melee + 0.006*combo + 0.005*tournament + 0.004*opponent + 0.004*battle + 0.004*falcon + 0.004*starcraft

topic #64 (0.010): 0.035*stream + 0.015*twitch + 0.011*miami + 0.010*trailer + 0.008*streamer + 0.008*viewer + 0.007*streaming + 0.007*bird + 0.005*skype + 0.005*ddos

topic #65 (0.010): 0.006*1998 + 0.006*sam + 0.005*lt + 0.003*comma + 0.003*lee + 0.003*repost + 0.003*jelly + 0.003*50 + 0.003*hunter + 0.003*host

topic #66 (0.010): 0.049*kanye + 0.019*jon + 0.012*song + 0.009*betting + 0.008*keyboard + 0.008*taylor + 0.008*bet + 0.008*concert + 0.006*fam + 0.005*ye

topic #67 (0.010): 0.006*customer + 0.005*manager + 0.004*architect + 0.004*london + 0.004*bos + 0.003*unit + 0.003*receipt + 0.003*blah + 0.003*store + 0.003*card

topic #68 (0.010): 0.008*spiderman + 0.007*bryan + 0.006*punk + 0.005*season + 0.005*reign + 0.005*flight + 0.005*vancouver + 0.004*bike + 0.004*tesla + 0.004*victoria

topic #69 (0.010): 0.007*bryan + 0.007*cat + 0.007*daniel + 0.006*charlie + 0.006*kevin + 0.005*adam + 0.005*feedback + 0.005*item + 0.005*podcast + 0.004*gang

topic #70 (0.010): 0.010*baby + 0.005*daughter + 0.004*diaper + 0.004*child + 0.004*pregnant + 0.003*husband + 0.003*ole + 0.003*pregnancy + 0.003*mod + 0.003*son

topic #71 (0.010): 0.015*film + 0.010*movie + 0.007*aircraft + 0.004*ring + 0.003*avenger + 0.003*ray + 0.003*criterion + 0.003*elf + 0.003*pharmacy + 0.003*pilot

topic #72 (0.010): 0.015*smoking + 0.013*smoke + 0.009*smoker + 0.005*quit + 0.005*cigarette + 0.003*sober + 0.003*quit_smoking + 0.003*smoked + 0.003*poop + 0.003*jeff

topic #73 (0.010): 0.010*perk + 0.009*batman + 0.008*sb + 0.008*dart + 0.006*cooper + 0.005*stitch + 0.004*bath + 0.004*knit + 0.003*laura + 0.003*survey

topic #74 (0.010): 0.016*church + 0.012*religion + 0.011*christian + 0.009*bible + 0.008*belief + 0.007*catholic + 0.006*atheist + 0.006*christianity + 0.005*sin + 0.005*prayer

topic #75 (0.010): 0.026*amp009 + 0.009*amp009_amp009 + 0.008*will_also + 0.008*oror + 0.008*parent_commenter + 0.008*can_toggle + 0.008*delete_on + 0.008*of_1 + 0.008*comment_score + 0.007*or_le

topic #76 (0.010): 0.009*terry + 0.006*trek + 0.006*ball + 0.005*ha + 0.005*pizza + 0.004*card + 0.004*star_trek + 0.004*puzzle + 0.004*pokemon + 0.004*dream

topic #77 (0.010): 0.006*san + 0.006*lane + 0.005*park + 0.004*traffic + 0.004*car + 0.004*diego + 0.003*san_diego + 0.003*city + 0.003*sf + 0.003*riding

topic #78 (0.010): 0.008*player + 0.007*hero + 0.007*damage + 0.007*team + 0.006*enemy + 0.005*map + 0.004*dota + 0.004*sniper + 0.004*tier + 0.003*competitive

topic #79 (0.010): 0.009*team + 0.008*draft + 0.008*season + 0.008*nfl + 0.007*qb + 0.007*playoff + 0.007*coach + 0.005*offense + 0.005*player + 0.005*league

topic #80 (0.010): 0.029*anime + 0.018*rick + 0.013*manga + 0.012*͡° + 0.011*sp + 0.008*͜ʖ + 0.006*͡°_͜ʖ + 0.006*scene + 0.005*episode + 0.005*duplicate

topic #81 (0.010): 0.007*ward + 0.007*smile + 0.005*ooc + 0.005*ap + 0.004*artist + 0.004*roman + 0.003*art + 0.003*grin + 0.003*laugh + 0.003*nod

topic #82 (0.010): 0.011*bike + 0.008*ign + 0.008*chess + 0.007*potato + 0.006*relay + 0.006*sin + 0.006*lane + 0.004*nz + 0.004*accident + 0.004*node

topic #83 (0.010): 0.014*planet + 0.011*earth + 0.010*philosophy + 0.009*galaxy + 0.007*moon + 0.007*alien + 0.006*universe + 0.005*cylinder + 0.005*light + 0.005*philosopher

topic #84 (0.010): 0.027*song + 0.020*album + 0.015*music + 0.014*band + 0.008*drum + 0.008*guitar + 0.007*remix + 0.007*track + 0.006*bass + 0.005*lyric

topic #85 (0.010): 0.026*giveaway + 0.012*bra + 0.011*ditto + 0.009*villager + 0.009*sent + 0.008*happy_new + 0.006*curl + 0.006*brawl + 0.006*fox + 0.006*d

topic #86 (0.010): 0.068*de + 0.058*que + 0.040*en + 0.024*la + 0.020*se + 0.017*da + 0.016*si + 0.016*un + 0.016*du + 0.014*der

topic #87 (0.010): 0.009*55 + 0.007*ski + 0.007*disney + 0.006*montana + 0.005*nuclear + 0.005*santa + 0.005*skiing + 0.004*gift + 0.004*resort + 0.004*beach

topic #88 (0.010): 0.004*karma + 0.003*commie + 0.003*poland + 0.003*hi + 0.002*nz + 0.002*portland + 0.002*upvote + 0.002*putin + 0.002*girl + 0.002*euro

topic #89 (0.010): 0.010*superman + 0.006*disney + 0.005*anna + 0.004*danny + 0.004*dc + 0.003*thumbnail + 0.003*oak + 0.003*frozen + 0.003*movie + 0.003*hot_dog

topic #90 (0.010): 0.036*cigar + 0.005*cuban + 0.003*wrapper + 0.003*economics + 0.003*bitcoin + 0.003*libertarian + 0.003*smoke + 0.003*billy + 0.002*rational + 0.002*bitch

topic #91 (0.010): 0.010*spell + 0.007*wizard + 0.007*dm + 0.007*roll + 0.006*ac + 0.006*magic + 0.006*player + 0.005*attack + 0.005*damage + 0.005*npc

topic #92 (0.010): 0.008*archer + 0.006*gt_gt + 0.004*deer + 0.004*endless + 0.004*bird + 0.004*safety + 0.003*wildlife + 0.003*dinosaur + 0.003*nick + 0.003*river

topic #93 (0.010): 0.028*bike + 0.006*awakening + 0.005*riding + 0.005*climbing + 0.005*cycling + 0.004*ride + 0.004*emblem + 0.004*race + 0.003*rider + 0.003*happy_birthday

topic #94 (0.010): 0.014*rifle + 0.013*gun + 0.010*ammo + 0.009*barrel + 0.008*knife + 0.008*pistol + 0.007*round + 0.007*mag + 0.006*magazine + 0.006*firearm

topic #95 (0.010): 0.007*morgan + 0.005*scott + 0.003*seam + 0.003*pat + 0.003*lesbian + 0.003*wish + 0.003*bottled + 0.003*dodge + 0.003*giveaway + 0.003*software

topic #96 (0.010): 0.020*camera + 0.017*photo + 0.015*lens + 0.011*photography + 0.009*exposure + 0.009*shot + 0.009*zen + 0.008*photographer + 0.007*iso + 0.007*image

topic #97 (0.010): 0.016*steam + 0.013*trade + 0.010*key + 0.009*gift + 0.009*paypal + 0.008*tf2 + 0.008*confirmed + 0.007*item + 0.007*bundle + 0.007*beard

topic #98 (0.010): 0.010*calorie + 0.010*fat + 0.008*food + 0.008*protein + 0.007*eat + 0.007*diet + 0.007*carbs + 0.006*eating + 0.005*weight + 0.005*meal

topic #99 (0.010): 0.003*truck + 0.002*belt + 0.002*apple + 0.002*qualification + 0.002*glove + 0.002*trailer + 0.002*fold + 0.002*poker + 0.002*survey + 0.002*fatigue