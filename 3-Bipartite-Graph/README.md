### New visualization after refined preprocessing
![full](https://github.com/chocoluffy/redditQA/blob/master/3-Bipartite-Graph/results/full.png)

### Stats
Apply algorithm on larger dataset to make bipartite graph more conclusive with 17536 distinct subreddits and 32134
 "reddit-loyal" authors(contribute to at least 5 different subreddits) on 100 topics.

A typical result from console:

User: Deadlifted 
{'topicvecs': defaultdict(<type 'dict'>, {u'circlebroke2': 59, u'cars': 99, u'nfl': 21, u'CFB': 21, u'pics': 93, u'movies': 0, u'SubredditDrama': 59}), 
 'contributions': defaultdict(<type 'int'>, {u'nfl': 10, u'cars': 7, u'circlebroke2': 1, u'CFB': 1, u'pics': 1, u'movies': 1, u'SubredditDrama': 1})
}

User: raohthekenoh 
{'topicvecs': defaultdict(<type 'dict'>, {u'nfl': 21, u'videos': 93, u'todayilearned': 59, u'SuicideWatch': 56, u'SquaredCircle': 21, u'confession': 56, u'atheism': 56, u'movies': 0, u'AskReddit': 93, u'WTF': 59, u'comicbooks': 0, u'politics': 96, u'fantasyfootball': 21}), 
 'contributions': defaultdict(<type 'int'>, {u'confession': 2, u'videos': 4, u'todayilearned': 1, u'SuicideWatch': 11, u'SquaredCircle': 20, u'nfl': 5, u'atheism': 3, u'movies': 48, u'AskReddit': 2, u'WTF': 4, u'politics': 3, u'comicbooks': 1, u'fantasyfootball': 2})
}

And weight cutoff means if the author contributes to that reddit less than T = 4 within a month(meaning less than weekly), we ignore those subreddit. 

### After applying TF-IDF:

Topic #0: 0.011*would + 0.011*really + 0.010*one + 0.009*think + 0.006*much + 0.006*even + 0.006*time + 0.006*see + 0.006*make + 0.006*also

Topic #1: 0.079*post + 0.036*sub + 0.036*mod + 0.033*reddit + 0.028*thread + 0.019*comment + 0.019*subreddit + 0.016*rule + 0.016*link + 0.013*youre

Topic #2: 0.069*god + 0.027*church + 0.026*christian + 0.026*religion + 0.016*jesus + 0.015*religious + 0.014*faith + 0.014*belief + 0.014*believe + 0.013*bible

Topic #3: 0.262*cool + 0.248*late + 0.127*bob + 0.042*refined + 0.033*punctuation + 0.029*maria + 0.028*bit_late + 0.021*noticed + 0.020*celebration + 0.019*deadpool

Topic #4: 0.216*xx + 0.038*bra + 0.027*panty + 0.027*x + 0.022*pair + 0.020*sock + 0.018*kik + 0.016*get + 0.013*wear + 0.012*post

Topic #5: 0.205*day + 0.140*hour + 0.113*month + 0.096*week + 0.058*minute + 0.038*10 + 0.033*date + 0.028*gift + 0.027*30 + 0.025*amazon

Topic #6: 0.010*would + 0.009*people + 0.008*one + 0.006*think + 0.005*also + 0.004*world + 0.004*say + 0.004*mean + 0.004*thing + 0.004*even

Topic #7: 0.109*na + 0.068*da + 0.067*sam + 0.047*o + 0.039*eu + 0.035*um + 0.035*em + 0.034*sa + 0.028*ou + 0.025*nu

Topic #8: 0.048*song + 0.031*music + 0.023*album + 0.019*band + 0.017*really + 0.013*sound + 0.010*good + 0.009*listen + 0.009*track + 0.009*love

Topic #9: 0.089*region + 0.040*agency + 0.035*cert + 0.034*province + 0.034*marketing + 0.034*passport + 0.033*swiss + 0.032*cyclist + 0.030*district + 0.030*ir

Topic #10: 0.116*server + 0.054*network + 0.035*service + 0.032*user + 0.029*ip + 0.026*site + 0.026*client + 0.025*host + 0.025*internet + 0.025*router

Topic #11: 0.315*machine + 0.299*coffee + 0.092*scout + 0.038*ribbon + 0.033*grinder + 0.031*grind + 0.023*espresso + 0.022*patrol + 0.018*scouting + 0.011*drip

Topic #12: 0.087*card + 0.040*deck + 0.019*play + 0.014*turn + 0.010*board + 0.009*chord + 0.009*think + 0.008*mana + 0.007*game + 0.007*good

Topic #13: 0.546*gt + 0.037*gt_gt + 0.036*correct + 0.022*full + 0.020*need + 0.015*all + 0.013*2014 + 0.012*point + 0.012*year + 0.012*posted

Topic #14: 0.017*one + 0.016*thanks + 0.014*trade + 0.014*got + 0.013*get + 0.011*would + 0.011*ill + 0.010*im + 0.009*sent + 0.007*send

Topic #15: 0.304*ad + 0.123*per + 0.082*ed + 0.077*non + 0.053*di + 0.037*ho + 0.029*il + 0.027*dare + 0.024*ci + 0.021*exist

Topic #16: 0.084*coin + 0.058*bitcoin + 0.036*tip + 0.028*hacker + 0.027*bit + 0.022*doge + 0.020*verify + 0.018*wow + 0.018*mining + 0.017*discussion

Topic #17: 0.680*author + 0.047*supremacist + 0.042*white_supremacist + 0.036*essence + 0.034*lecturer + 0.017*coalition + 0.000*aircraft + 0.000*dipped + 0.000*shaman + 0.000*premise

Topic #18: 0.122*game + 0.036*play + 0.023*player + 0.016*playing + 0.012*people + 0.012*get + 0.011*played + 0.010*map + 0.010*time + 0.009*steam

Topic #19: 0.510*project + 0.211*pattern + 0.066*rabbit + 0.043*needle + 0.043*yarn + 0.026*knit + 0.015*pine + 0.008*row + 0.007*stole + 0.003*spill

Topic #20: 0.038*book + 0.027*read + 0.027*story + 0.017*character + 0.012*one + 0.011*reading + 0.010*series + 0.010*first + 0.010*really + 0.010*writing

Topic #21: 0.020*team + 0.018*game + 0.012*year + 0.010*player + 0.009*get + 0.009*season + 0.009*think + 0.009*play + 0.008*he + 0.008*good

Topic #22: 0.012*one + 0.008*get + 0.008*look + 0.008*would + 0.007*good + 0.007*make + 0.006*really + 0.006*im + 0.006*use + 0.006*also

Topic #23: 0.013*get + 0.012*im + 0.010*day + 0.009*dont + 0.009*doctor + 0.009*help + 0.008*feel + 0.007*ive + 0.007*take + 0.007*time

Topic #24: 0.206*google + 0.117*download + 0.115*torrent + 0.087*g + 0.070*gg + 0.051*sign + 0.035*pop + 0.032*joker + 0.028*1080p + 0.024*guru

Topic #25: 0.026*gun + 0.015*ship + 0.009*weapon + 0.007*rifle + 0.007*shoot + 0.007*shot + 0.007*planet + 0.006*plane + 0.006*would + 0.006*air

Topic #26: 0.017*window + 0.013*drive + 0.012*run + 0.011*computer + 0.010*use + 0.010*need + 0.007*ram + 0.007*running + 0.007*work + 0.007*one

Topic #27: 0.358*thank + 0.237*you + 0.203*thank_you + 0.031*free + 0.025*awesome + 0.013*get + 0.011*exp + 0.008*2 + 0.007*bonus + 0.006*brute

Topic #28: 0.779*deleted + 0.165*deleted_deleted + 0.003*fake + 0.002*caption + 0.002*mein + 0.002*moar + 0.002*pm_me + 0.002*gamertag + 0.002*pimp + 0.002*ok

Topic #29: 0.111*word + 0.027*cloud + 0.025*train + 0.020*made + 0.017*subreddits + 0.014*use + 0.014*request + 0.014*common + 0.013*subreddit + 0.012*ml

Topic #30: 0.111*de + 0.101*que + 0.083*la + 0.055*en + 0.036*el + 0.029*los + 0.024*un + 0.024*e + 0.023*se + 0.021*por

Topic #31: 0.072*pen + 0.067*gif + 0.066*paper + 0.059*horse + 0.040*spider + 0.037*letter + 0.036*wolf + 0.031*ink + 0.018*line + 0.018*pencil

Topic #32: 0.075*east + 0.075*coast + 0.066*east_coast + 0.046*pm + 0.033*add + 0.032*im + 0.027*ill + 0.025*added + 0.022*hey + 0.020*looking

Topic #33: 0.085*dog + 0.047*cat + 0.022*animal + 0.016*pet + 0.016*vet + 0.015*bird + 0.014*he + 0.011*puppy + 0.011*uchangetip + 0.010*get

Topic #34: 0.152*de + 0.115*le + 0.053*pa + 0.050*et + 0.045*la + 0.030*un + 0.028*je + 0.024*ben + 0.023*french + 0.023*du

Topic #35: 0.087*die + 0.065*da + 0.047*und + 0.046*der + 0.041*ich + 0.035*e + 0.033*ist + 0.030*nicht + 0.026*von + 0.025*den

Topic #36: 0.137*movie + 0.115*film + 0.037*review + 0.027*rating + 0.024*scene + 0.020*director + 0.018*based + 0.016*actor + 0.014*writer + 0.013*critic

Topic #37: 0.282*ice + 0.126*island + 0.121*land + 0.073*ex + 0.042*mushroom + 0.025*fa + 0.024*biome + 0.022*blaze + 0.021*nether + 0.019*claim

Topic #38: 0.125*beer + 0.121*drink + 0.104*bottle + 0.066*glass + 0.054*drinking + 0.047*wine + 0.041*alcohol + 0.030*taste + 0.018*good + 0.018*whiskey

Topic #39: 0.121*1 + 0.100*2 + 0.094*3 + 0.063*4 + 0.051*5 + 0.033*6 + 0.030*10 + 0.024*7 + 0.022*8 + 0.018*12

Topic #40: 0.047*ball + 0.034*flag + 0.031*roll + 0.030*round + 0.029*match + 0.026*dream + 0.023*new + 0.018*pool + 0.016*badge + 0.015*perk

Topic #41: 0.055*look + 0.018*look_like + 0.016*hair + 0.014*picture + 0.013*girl + 0.012*love + 0.012*think + 0.011*color + 0.011*face + 0.011*see

Topic #42: 0.022*water + 0.017*use + 0.010*oil + 0.009*get + 0.008*plant + 0.008*dry + 0.008*product + 0.006*using + 0.005*ive + 0.005*heat

Topic #43: 0.034*year + 0.033*im + 0.030*new + 0.019*happy + 0.015*thanks + 0.012*love + 0.011*good + 0.011*happy_new + 0.009*time + 0.009*one

Topic #44: 0.098*design + 0.091*print + 0.085*3d + 0.066*model + 0.037*printer + 0.027*printing + 0.026*package + 0.025*wii + 0.025*serial + 0.021*rate

Topic #45: 0.024*food + 0.017*eat + 0.013*meat + 0.012*make + 0.010*eating + 0.010*chicken + 0.010*cheese + 0.010*recipe + 0.009*good + 0.008*egg

Topic #46: 0.475*xd + 0.134*sp + 0.098*oc + 0.083*pony + 0.023*lel + 0.020*wiener + 0.020*hoof + 0.018*hair_color + 0.014*ahhhh + 0.005*orange

Topic #47: 0.198*japanese + 0.171*anime + 0.139*japan + 0.106*chapter + 0.065*manga + 0.061*blah + 0.045*plot + 0.034*arc + 0.021*blah_blah + 0.021*pumping

Topic #48: 0.322*event + 0.187*fire + 0.117*metal + 0.047*x2 + 0.030*deer + 0.026*jon + 0.025*wildlife + 0.015*x4 + 0.013*constructive_criticism + 0.013*brewer

Topic #49: 0.052*key + 0.029*karma + 0.027*rule + 0.025*bot + 0.024*text + 0.022*flair + 0.021*please + 0.019*check + 0.018*clan + 0.016*vote

Topic #50: 0.033*king + 0.029*ticket + 0.025*shot + 0.019*nba + 0.014*guard + 0.012*basketball + 0.012*jordan + 0.012*hawk + 0.012*shooting + 0.012*celtic

Topic #51: 0.018*use + 0.011*using + 0.011*code + 0.011*file + 0.008*data + 0.007*work + 0.006*make + 0.006*need + 0.005*way + 0.005*type

Topic #52: 0.376*led + 0.086*watt + 0.057*parade + 0.055*vapor + 0.041*wick + 0.040*perfection + 0.038*repaired + 0.031*filtered + 0.030*dh + 0.027*resistor

Topic #53: 0.157*watch + 0.132*live + 0.117*tv + 0.114*click + 0.076*hd + 0.061*ncaa + 0.047*stream + 0.033*100 + 0.022*free + 0.021*gtgt

Topic #54: 0.024*science + 0.019*number + 0.016*math + 0.013*a + 0.012*one + 0.012*answer + 0.012*set + 0.011*theory + 0.010*problem + 0.009*question

Topic #55: 0.167*visit + 0.111*sketch + 0.090*meta + 0.059*blown + 0.047*hatch + 0.040*clown + 0.040*blown_away + 0.040*sherlock + 0.034*barn + 0.034*15th

Topic #56: 0.014*people + 0.012*dont + 0.011*woman + 0.011*thing + 0.010*think + 0.009*feel + 0.009*im + 0.008*want + 0.008*life + 0.007*youre

Topic #57: 0.100*riot + 0.079*fuck + 0.051*meme + 0.050*shit + 0.044*fucking + 0.024*bitch + 0.024*pls + 0.021*ayy + 0.021*ur + 0.020*yeah

Topic #58: 0.075*sound + 0.033*speaker + 0.026*audio + 0.022*voice + 0.021*channel + 0.017*signal + 0.016*amp + 0.014*sound_like + 0.013*use + 0.012*noise

Topic #59: 0.022*people + 0.021*dont + 0.012*get + 0.011*guy + 0.011*im + 0.011*thats + 0.011*know + 0.011*shit + 0.010*think + 0.008*even

Topic #60: 0.022*year + 0.017*one + 0.007*love + 0.007*favorite + 0.007*old + 0.006*ever + 0.006*new + 0.006*ive + 0.006*black + 0.005*best

Topic #61: 0.061*en + 0.053*er + 0.052*muslim + 0.044*og + 0.033*isi + 0.033*survivor + 0.030*iraq + 0.028*arab + 0.027*iran + 0.027*har

Topic #62: 0.045*school + 0.025*class + 0.023*student + 0.021*job + 0.015*year + 0.013*program + 0.012*work + 0.012*college + 0.012*course + 0.010*degree

Topic #63: 0.063*please + 0.046*automatically + 0.039*question + 0.039*contact + 0.038*action + 0.036*performed + 0.036*i + 0.036*concern + 0.036*moderator + 0.032*botrautomoderatorcommentsq11puwhatisautomoderator

Topic #64: 0.233*jan + 0.089*poem + 0.085*rhyme + 0.075*crack + 0.072*feb + 0.069*poetry + 0.060*sticky + 0.051*19th + 0.044*millionaire + 0.028*overlord

Topic #65: 0.029*country + 0.022*government + 0.020*state + 0.020*u + 0.015*people + 0.013*party + 0.013*american + 0.010*political + 0.009*right + 0.009*world

Topic #66: 0.423*comment + 0.096*whats + 0.073*be + 0.061*longest + 0.052*limit + 0.045*lol + 0.043*someone + 0.037*wrote + 0.033*character + 0.022*9000

Topic #67: 0.013*40 + 0.012*state + 0.011*45 + 0.011*ampnbsp + 0.010*50 + 0.010*55 + 0.010*60 + 0.009*200 + 0.009*36 + 0.009*41

Topic #68: 0.040*cpu + 0.030*card + 0.029*price + 0.025*monitor + 0.024*video + 0.023*gaming + 0.023*gpu + 0.022*power + 0.022*pc + 0.021*build

Topic #69: 0.239*original + 0.151*amp + 0.106*link + 0.036*remix + 0.035*feat + 0.032*mix + 0.028*track + 0.028*link_original + 0.022*here + 0.018*dj

Topic #70: 0.015*im + 0.013*dont + 0.013*get + 0.012*would + 0.011*know + 0.010*want + 0.010*good + 0.009*work + 0.009*youre + 0.009*really

Topic #71: 0.094*blade + 0.064*beard + 0.062*gem + 0.057*shave + 0.056*r + 0.054*sr + 0.051*razor + 0.050*soap + 0.049*light + 0.034*shaving

Topic #72: 0.066*amp009 + 0.030*gt + 0.025*of + 0.024*amp009_amp009 + 0.024*also + 0.023*score + 0.019*nsfw + 0.019*or + 0.019*delete + 0.019*will

Topic #73: 0.099*ja + 0.061*ne + 0.055*se + 0.054*je + 0.048*ti + 0.043*mi + 0.037*sd + 0.033*va + 0.028*da + 0.025*te

Topic #74: 0.028*phone + 0.021*app + 0.014*screen + 0.012*use + 0.011*device + 0.011*work + 0.010*update + 0.010*android + 0.010*issue + 0.009*apps

Topic #75: 0.081*video + 0.034*link + 0.028*image + 0.024*source + 0.020*thanks + 0.019*cs + 0.015*youtube + 0.014*camera + 0.013*this + 0.012*picture

Topic #76: 0.188*henry + 0.104*violet + 0.068*13th + 0.063*confess + 0.062*artisan + 0.060*nifty + 0.052*relatively_low + 0.048*welsh + 0.044*wale + 0.039*unforgiving

Topic #77: 0.279*space + 0.200*star + 0.163*earth + 0.107*universe + 0.044*mar + 0.041*galaxy + 0.034*travel + 0.018*bang + 0.014*tm + 0.011*big_bang

Topic #78: 0.204*tape + 0.135*teeth + 0.111*laser + 0.069*bong + 0.053*tooth + 0.051*mane + 0.049*dentist + 0.036*duct + 0.035*cleaning + 0.032*butterfly

Topic #79: 0.216*͡° + 0.142*͜ʖ + 0.099*ye + 0.097*͡°_͜ʖ + 0.044*͡o + 0.041*br + 0.035*oh + 0.034*haha + 0.022*͡o_͜ʖ + 0.020*teller

Topic #80: 0.251*show + 0.211*episode + 0.147*season + 0.093*cheek + 0.028*watched + 0.024*series + 0.015*het + 0.014*dat + 0.013*ik + 0.012*viewer

Topic #81: 0.315*lmao + 0.249*lt3 + 0.108*wasting + 0.064*wasting_time + 0.039*oo + 0.038*choir + 0.020*ugh + 0.018*lt3_lt3 + 0.015*trolled + 0.010*x

Topic #82: 0.363*xxx + 0.083*alien + 0.035*watson + 0.030*xpost + 0.021*comment + 0.019*emma + 0.018*wwe + 0.015*child + 0.015*ufo + 0.014*blacklist

Topic #83: 0.598*son + 0.088*cest + 0.046*escort + 0.041*noah + 0.040*cursed + 0.032*orion + 0.022*petite + 0.021*jenkins + 0.012*vie + 0.005*ooh

Topic #84: 0.013*would + 0.007*time + 0.006*much + 0.006*year + 0.006*even + 0.006*people + 0.005*point + 0.004*see + 0.004*make + 0.004*still

Topic #85: 0.263*subreddit + 0.257*submission + 0.152*submitted + 0.105*domain + 0.062*history + 0.056*recent + 0.017*wat + 0.011*helen + 0.002*cropping + 0.001*here

Topic #86: 0.341*arena + 0.214*possession + 0.090*douche + 0.061*harmonic + 0.035*burglar + 0.024*revered + 0.015*tint + 0.003*gram + 0.000*patching + 0.000*dipped

Topic #87: 0.247*name + 0.118*english + 0.045*spanish + 0.042*kanye + 0.034*rap + 0.030*stone + 0.025*accent + 0.023*dash + 0.022*genre + 0.022*kim

Topic #88: 0.234*feedback + 0.107*font + 0.058*ski + 0.044*teamspeak + 0.037*arma + 0.036*rad + 0.034*rt + 0.033*outline + 0.026*ko + 0.024*bikini

Topic #89: 0.277*john + 0.110*horn + 0.080*rust + 0.072*talking + 0.065*candle + 0.050*about + 0.038*talking_about + 0.031*unarmed + 0.028*thompson + 0.024*utc

Topic #90: 0.070*love + 0.060*hot + 0.040*as + 0.040*would + 0.034*sexy + 0.033*nice + 0.030*id + 0.029*dick + 0.024*guy + 0.024*porn

Topic #91: 0.015*weight + 0.013*day + 0.011*get + 0.010*time + 0.009*body + 0.009*week + 0.008*goal + 0.008*im + 0.007*start + 0.007*youre

Topic #92: 0.448*war + 0.105*empire + 0.079*china + 0.073*m + 0.047*troop + 0.038*france + 0.029*jake + 0.025*federation + 0.021*italy + 0.015*belgium

Topic #93: 0.010*time + 0.009*back + 0.008*one + 0.006*you + 0.006*know + 0.006*get + 0.005*could + 0.005*go + 0.005*he + 0.005*around

Topic #94: 0.111*det + 0.087*att + 0.071*som + 0.066*är + 0.053*de + 0.052*på + 0.044*om + 0.043*med + 0.043*jag + 0.041*av

Topic #95: 0.012*place + 0.012*city + 0.009*people + 0.009*go + 0.009*there + 0.008*get + 0.008*area + 0.008*good + 0.006*also + 0.006*around

Topic #96: 0.010*get + 0.010*kid + 0.009*would + 0.009*year + 0.008*family + 0.008*child + 0.007*work + 0.007*time + 0.006*job + 0.006*need

Topic #97: 0.031*money + 0.020*price + 0.020*pay + 0.017*buy + 0.016*year + 0.016*company + 0.015*get + 0.012*customer + 0.012*business + 0.011*cost

Topic #98: 0.013*get + 0.010*damage + 0.009*level + 0.007*use + 0.007*attack + 0.006*one + 0.006*character + 0.006*skill + 0.006*enemy + 0.006*need

Topic #99: 0.064*car + 0.019*bike + 0.012*wheel + 0.012*get + 0.012*drive + 0.011*ride + 0.011*truck + 0.010*vehicle + 0.010*engine + 0.010*driver

> the top words for a topic make much more sense.
