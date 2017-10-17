## Progress

Fixing issue listed here [10.11 meeting](https://github.com/chocoluffy/redditQA/issues/3).

### TF-IDF weights

![compare](https://github.com/chocoluffy/redditQA/blob/master/4-LDA-On-Tfidf/results/compare.png)
![compare](https://github.com/chocoluffy/redditQA/blob/master/4-LDA-On-Tfidf/results/compare2.png)

Try to mimic the magnitude of BOW matrix, but with TF-IDF weights.

### comments counts

Before: 2G(two days) data, top 10% subreddits, i.e., 1753 subreddits. (with each 10000 comments desired)
> Problems: the reality is that, the smallest subreddit inside that top 10%, has only ~200 comments.

Then, I try to increase the dataset.
After: 4G(four days) data, top 8% subreddits, i.e., 1819 subreddits.
> Situation: `(694366, 345)`, the largest subreddit and smallest subreddit's comments count.

In order for a balanced dataset for TF-IDF and LDA. Pick each top voted 1000 comments concatenated as documents.

## Hyper-parameters

- top 5% most acitve user.
- `topic_cut_off = 0.08`. Only investigate topics with probability higher than 0.08(0.1 gives less dominant topics).
- `corpus_tfidf = map(lambda x: map(lambda y: (y[0], round(y[1] * 200, 1)), x), corpus_tfidf)`. De-normalize TF-IDF weights to have approximate scale as BOW values.


## Result Analysis

In our 4G(~four days) data:

### Case 1: deweymm

Distinct subreddit number : 32,
Comments count: 99

### Our prediction

4 dominant topics, with generalist/specialist score: 0.261935180797, (relative high, meaning he's relatively a specialist)
[(66, 0.13144566362518412), (93, 0.10145583869818586), (96, 0.15925248910595119), (99, 0.085331145698520142)]

topic #66 (0.010): 0.002*cop + 0.002*police + 0.002*officer + 0.001*pizza + 0.001*driver + 0.001*lawyer + 0.001*customer + 0.001*arrest + 0.001*court + 0.001*toilet

topic #93 (0.010): 0.003*government + 0.002*muslim + 0.002*religion + 0.002*political + 0.002*society + 0.002*christian + 0.002*islam + 0.001*liberal + 0.001*rape + 0.001*libertarian

topic #96 (0.010): 0.008*apps + 0.008*android + 0.008*battery + 0.007*app + 0.007*nexus + 0.006*moto + 0.005*device + 0.005*lollipop + 0.005*rom + 0.005*iphone

topic #99 (0.010): 0.002*drug + 0.002*weed + 0.002*symptom + 0.002*dose + 0.002*doctor + 0.002*lsd + 0.002*gram + 0.002*anxiety + 0.002*mdma + 0.001*medication

### Ground Truth

His top voted 10 comments: [
    "an unstable cry baby", 
    "Apologies - sounds like you have it all figured out. \n\nHappy New Year", 
    "me too - AKA where DC works out is a mile down the road from where I live - was disgusted and decided to shun my neighbor", 
    "and you heartbroken :(", 
    "You changed my mind - all the markings of a winner", 
    "\"amazing\"? Do you live in a cave?", 
    "First and foremost, I pay the company that you work for - not you clearly. Second, you get paid well to do the job and should be grateful for having the opportunity to do it. Just about anyone can be trained to do it so a good attitude goes a long way.  \n\nSo you are no hero for doing your job oblivious douchebag. Paying a tow driver for a service does not give scum the right to rob and fliece the public. That is what this thread is about. \n\n\nYour post is cringe-worthy and there is nothing \"friendly\" about it. I am actually embarrassed for you. Wake the fuck up.", 
    "way too naturally beautiful and young for that much make up. Also poorly done - see a pro.", 
    "Yeah other than the fact he is a fraud about his fighting credentials, has been discussed and is the laughing stock of the community including Joe Rogan, Dana White, Rhonda Rousey, Ariel Helwani , etc. etc. in the last 48 hours, he is just plain bad for the sport. We can just pretend this is not happening.\n\nLook Fanboy, I didn't mean to hurt your feelings - perhaps we can get that Steven Seagal - Under Siege poster hanging over your bed autographed for you at some point. But in the meantime, head over to the SG fanboy site and stop your sniveling.", 
    "Sure enough - thank you - goes to show beautiful women come from everywhere", 
]


### Case 2: TheRealPeteWheeler

Distinct subreddit number : 15,
Comments count: 102

### Our prediction

3 dominant topics, with generalist/specialist score: 0.350207616138, (more specialist than Case 1).
[(46, 0.46703078917570201), (66, 0.12712723743667273), (93, 0.086705506845797406)]

topic #46 (0.010): 0.004*sex + 0.002*dating + 0.002*gender + 0.002*trans + 0.002*gay + 0.002*sexual + 0.002*male + 0.002*partner + 0.002*boyfriend + 0.002*feminist

topic #66 (0.010): 0.002*cop + 0.002*police + 0.002*officer + 0.001*pizza + 0.001*driver + 0.001*lawyer + 0.001*customer + 0.001*arrest + 0.001*court + 0.001*toilet

topic #93 (0.010): 0.003*government + 0.002*muslim + 0.002*religion + 0.002*political + 0.002*society + 0.002*christian + 0.002*islam + 0.001*liberal + 0.001*rape + 0.001*libertarian

### Ground Truth

His top voted 5 subreddit: [
    AskReddit, InternetIsBeautiful, nfl, CHIBears, standupshots
]

His top voted 10 comments: [
        "Helterskelter48", 
        "chronicwaffles", 
        "xMIGG", 
        "As a Michigan fan, I'M SO CONFLICTED", 
        "A little. Actually, no, wait. No, not at all. ", 
        "http://i.imgur.com/UDQpWw6.png\n\nYou're not posting again on a throwaway, are you? ;)", 
        "As long as I can find a black t-shirt in that size, it comes in that size. ", 
        "Just a little hobby of mine. I'm actually a preschool teacher by day. ", 
        "http://www.reddit.com/r/thelastofus/comments/2r0g9e/official_tlou_tshirt_giveaway_thread/", 
        "If it's around that area, I would be okay with paying for shipping. ", 
        "Ugh. I hated that shit in middle/high school. Also the whole high school girl attitude \"haha ew sports i don't want to get sweaty\". No. You're not cute. ", 
]

## Distribution plot

![plot](https://github.com/chocoluffy/redditQA/blob/master/4-LDA-On-Tfidf/results/plot.png)

x: each subreddit average generalist/specialist scores.

y: avg contribution (within 4 days)

radius: how many authors involved.

## After applying TF-IDF weights and de-normalization:


topic #0 (0.010): 0.014*giveaway + 0.012*steam + 0.011*thanks_giveaway + 0.010*grump + 0.007*csgo + 0.006*jon + 0.006*tf2 + 0.004*game_grump + 0.004*dont_starve + 0.004*steam_key

topic #1 (0.010): 0.012*mag + 0.010*paypal + 0.010*ebay + 0.010*shipping + 0.008*ammo + 0.008*shipped + 0.007*holster + 0.007*buyer + 0.006*tesla + 0.006*rifle

topic #2 (0.010): 0.113*manga + 0.090*anime + 0.046*arc + 0.041*naruto + 0.037*chapter + 0.015*gon + 0.013*hunter + 0.010*dub + 0.009*potion + 0.008*heather

topic #3 (0.010): 0.014*nhl + 0.013*puck + 0.012*hockey + 0.011*goalie + 0.006*playoff + 0.006*oiler + 0.005*pp + 0.005*jersey + 0.005*hawk + 0.004*scoring

topic #4 (0.010): 0.009*flour + 0.006*baking + 0.006*dough + 0.004*espresso + 0.004*recipe + 0.003*bake + 0.003*bread + 0.003*mixer + 0.003*starbucks + 0.003*yeast

topic #5 (0.010): 0.036*titan + 0.018*downton + 0.017*asylum + 0.014*germany + 0.014*german + 0.013*maggie + 0.011*aldi + 0.010*mary + 0.010*vault + 0.009*abbey

topic #6 (0.010): 0.106*cigar + 0.081*smoke + 0.076*smoking + 0.058*smoker + 0.054*nicotine + 0.052*tobacco + 0.040*smoked + 0.033*flavor + 0.033*cigarette + 0.027*cat_cat

topic #7 (0.010): 0.013*morrowind + 0.013*tf2 + 0.013*medic + 0.011*tank + 0.009*scout + 0.008*sc2 + 0.008*overwatch + 0.007*arty + 0.007*kanye + 0.007*tier

topic #8 (0.010): 0.016*lens + 0.007*photography + 0.007*iso + 0.007*shutter + 0.006*dslr + 0.006*gopro + 0.006*aperture + 0.005*film + 0.005*tripod + 0.005*exposure

topic #9 (0.010): 0.008*nba + 0.006*lebron + 0.006*kobe + 0.005*playoff + 0.005*basketball + 0.004*fsu + 0.004*coach + 0.004*melo + 0.004*cavs + 0.004*knicks

topic #10 (0.010): 0.011*calorie + 0.011*squat + 0.010*gym + 0.009*workout + 0.008*muscle + 0.006*lifting + 0.006*vape + 0.006*lift + 0.005*deadlift + 0.005*protein

topic #11 (0.010): 0.012*vg + 0.009*coin + 0.009*blu_ray + 0.008*blu + 0.007*ea + 0.007*madden + 0.007*stargate + 0.007*bo + 0.006*mvp + 0.006*victoria

topic #12 (0.010): 0.025*pvp + 0.023*gamergate + 0.023*guild + 0.022*server + 0.015*tb + 0.013*pve + 0.012*gg + 0.010*eso + 0.009*glyph + 0.008*kotaku

topic #13 (0.010): 0.021*sexy + 0.014*cock + 0.011*cum + 0.009*gorgeous + 0.008*tit + 0.007*cute + 0.007*pussy + 0.006*panty + 0.006*nipple + 0.005*kik

topic #14 (0.010): 0.020*chess + 0.016*rating + 0.014*finn + 0.013*warlock + 0.012*psn + 0.012*iq + 0.012*kpop + 0.008*sm + 0.008*jake + 0.008*idol

topic #15 (0.010): 0.023*vpn + 0.017*torrent + 0.015*vr + 0.014*netflix + 0.014*tracker + 0.008*tor + 0.007*vpns + 0.006*oculus + 0.006*dns + 0.006*isp

topic #16 (0.010): 0.023*meditation + 0.020*plant + 0.014*jones + 0.012*soil + 0.011*buddhism + 0.011*zen + 0.009*buddhist + 0.008*flower + 0.008*seed + 0.008*buddha

topic #17 (0.010): 0.005*pregnancy + 0.005*pregnant + 0.005*diaper + 0.004*husband + 0.003*curl + 0.003*shampoo + 0.003*breastfeeding + 0.003*cyst + 0.002*daughter + 0.002*conditioner

topic #18 (0.010): 0.004*smiled + 0.004*ja + 0.003*barry + 0.003*bono + 0.003*thank_mr + 0.003*meme + 0.003*trashy + 0.003*gtpost + 0.003*gtpost_title + 0.003*linked_meme

topic #19 (0.010): 0.010*disney + 0.007*floyd + 0.006*gaston + 0.006*jax + 0.005*runescape + 0.005*cast_member + 0.004*solomon + 0.004*duncan + 0.003*disneyland + 0.002*cleric

topic #20 (0.010): 0.004*kit + 0.003*motor + 0.003*wire + 0.003*truck + 0.003*voltage + 0.003*battery + 0.003*jeep + 0.002*mustang + 0.002*axle + 0.002*bolt

topic #21 (0.010): 0.025*album + 0.015*band + 0.014*guitar + 0.009*chord + 0.008*beatles + 0.008*lyric + 0.007*vocal + 0.007*drum + 0.007*punk + 0.007*kanye

topic #22 (0.010): 0.011*antenna + 0.011*nib + 0.010*outpost + 0.007*ink + 0.007*dongle + 0.007*pen + 0.007*pagan + 0.006*far_cry + 0.005*fc4 + 0.004*dice

topic #23 (0.010): 0.012*ps4 + 0.012*gta + 0.008*psn + 0.008*rockstar + 0.008*xbox + 0.008*crew + 0.007*korean + 0.007*ps3 + 0.006*mission + 0.005*xbox_one

topic #24 (0.010): 0.028*heathen + 0.015*deity + 0.015*religion + 0.012*coil + 0.011*pagan + 0.009*eric + 0.008*ritual + 0.008*loki + 0.008*norse + 0.008*christian

topic #25 (0.010): 0.011*civ + 0.010*ai + 0.009*roy + 0.008*bask + 0.008*survivor + 0.007*dorian + 0.006*trade_route + 0.005*unit + 0.005*tile + 0.005*lord

topic #26 (0.010): 0.009*hookah + 0.009*morty + 0.008*rug + 0.008*rick + 0.007*tracy + 0.007*see_sidebar + 0.007*creature + 0.006*ted + 0.006*jasmine + 0.006*anal

topic #27 (0.010): 0.003*downtown + 0.003*park + 0.002*parking + 0.002*neighborhood + 0.002*rent + 0.002*bus + 0.002*traffic + 0.002*restaurant + 0.002*st + 0.001*hotel

topic #28 (0.010): 0.005*boob + 0.005*tit + 0.004*chloe + 0.003*thailand + 0.003*annie + 0.002*bpd + 0.002*molly + 0.002*sal + 0.002*thai + 0.002*nude

topic #29 (0.010): 0.017*remix + 0.010*dj + 0.007*festival + 0.006*dodger + 0.006*trance + 0.006*soundcloud + 0.005*mets + 0.005*edm + 0.005*skrillex + 0.005*baseball

topic #30 (0.010): 0.006*louisville + 0.006*yang + 0.006*pm_sent + 0.006*height + 0.005*barry + 0.005*tall + 0.005*taller + 0.005*mx + 0.004*prisoner + 0.004*keyboard

topic #31 (0.010): 0.013*cpu + 0.008*gpu + 0.008*ram + 0.007*ssd + 0.007*intel + 0.006*motherboard + 0.006*monitor + 0.006*pc + 0.006*amd + 0.005*usb

topic #32 (0.010): 0.032*uber + 0.016*checklist + 0.016*taxi + 0.016*surge + 0.014*patient + 0.012*recent_post + 0.012*posting_again + 0.012*guideline + 0.012*comply + 0.011*must_wait

topic #33 (0.010): 0.063*que + 0.042*de + 0.031*en + 0.017*un + 0.017*por + 0.016*para + 0.015*la + 0.015*si + 0.015*una + 0.014*se

topic #34 (0.010): 0.014*cest + 0.013*je + 0.009*et + 0.008*dans + 0.007*pa + 0.006*sur + 0.006*poem + 0.006*toll + 0.005*pour + 0.005*est

topic #35 (0.010): 0.038*please_contact + 0.038*submission + 0.036*performed_automatically + 0.016*submission_removed + 0.015*question_concern + 0.012*moderator + 0.011*submitted + 0.010*please_review + 0.010*please_message + 0.009*performed

topic #36 (0.010): 0.004*server + 0.004*weapon + 0.003*gameplay + 0.003*quest + 0.003*dlc + 0.003*enemy + 0.003*map + 0.002*multiplayer + 0.002*armor + 0.002*spawn

topic #37 (0.010): 0.023*electrician + 0.021*crate + 0.014*michigan + 0.012*electrical + 0.011*circuit + 0.010*outlet + 0.009*minnesota + 0.009*wire + 0.008*solar + 0.008*breaker

topic #38 (0.010): 0.006*bow + 0.006*tps + 0.005*moba + 0.005*slag + 0.004*arrow + 0.004*mp + 0.004*archery + 0.004*robot + 0.004*borderland + 0.003*tote

topic #39 (0.010): 0.005*russia + 0.005*aircraft + 0.004*nation + 0.003*army + 0.003*troop + 0.003*russian + 0.003*empire + 0.003*military + 0.003*france + 0.003*german

topic #40 (0.010): 0.009*lucid + 0.008*girth + 0.006*erotica + 0.005*dentist + 0.004*shepard + 0.004*poker + 0.004*dreaming + 0.003*lucid_dreaming + 0.003*paranormal + 0.003*condom

topic #41 (0.010): 0.017*tank + 0.010*fish + 0.008*ammonia + 0.007*shrimp + 0.007*gallon + 0.006*algae + 0.006*plant + 0.006*fin + 0.006*charleston + 0.006*marching_band

topic #42 (0.010): 0.004*wood + 0.003*fabric + 0.003*pipe + 0.003*blade + 0.003*sewing + 0.002*quilt + 0.002*tile + 0.002*knife + 0.002*jar + 0.002*copper

topic #43 (0.010): 0.012*og + 0.009*snake + 0.008*ezra + 0.008*optic + 0.007*rat + 0.006*acorn + 0.006*gecko + 0.005*reptile + 0.004*destiny + 0.004*bracket

topic #44 (0.010): 0.017*cena + 0.016*rollins + 0.016*wwe + 0.013*bryan + 0.012*jay + 0.011*sting + 0.011*trey + 0.009*wrestling + 0.008*osu + 0.008*removal

topic #45 (0.010): 0.019*bike + 0.016*tire + 0.012*brake + 0.012*wheel + 0.009*engine + 0.007*rear + 0.006*bmw + 0.006*vehicle + 0.006*turbo + 0.006*vw

topic #46 (0.010): 0.004*sex + 0.002*dating + 0.002*gender + 0.002*trans + 0.002*gay + 0.002*sexual + 0.002*male + 0.002*partner + 0.002*boyfriend + 0.002*feminist

topic #47 (0.010): 0.016*dart + 0.006*hiker + 0.006*hike + 0.006*1112 + 0.005*cuban + 0.005*nelson + 0.005*survival + 0.005*fax + 0.005*blaster + 0.004*map

topic #48 (0.010): 0.012*wii + 0.011*mario + 0.011*nintendo + 0.008*3d + 0.008*zelda + 0.007*pokemon + 0.007*snes + 0.006*fire_emblem + 0.006*console + 0.006*smash

topic #49 (0.010): 0.048*bitcoin + 0.030*uchangetip + 0.024*btc + 0.022*coin + 0.013*changetip + 0.012*bitcoins + 0.010*doge + 0.008*rbitcoin + 0.006*scam + 0.006*currency

topic #50 (0.010): 0.012*dota + 0.010*ult + 0.009*lane + 0.008*adc + 0.007*hero + 0.006*jungle + 0.006*mmr + 0.005*minion + 0.005*champion + 0.004*enemy

topic #51 (0.010): 0.012*yosemite + 0.011*apple + 0.010*mac + 0.009*mrw + 0.009*sip + 0.009*macbook + 0.008*itunes + 0.007*chromebook + 0.007*omar + 0.006*mbp

topic #52 (0.010): 0.017*skyrim + 0.014*je + 0.010*het + 0.008*terry + 0.008*joel + 0.008*fps + 0.008*armenian + 0.007*ik + 0.006*ig + 0.006*texture

topic #53 (0.010): 0.006*furries + 0.005*furry + 0.004*buffy + 0.004*o7 + 0.004*fleet + 0.004*pl + 0.004*fandom + 0.004*ヽ༼ຈل͜ຈ༽ﾉ + 0.004*karma + 0.004*cosplay

topic #54 (0.010): 0.023*bjj + 0.019*cube + 0.018*mma + 0.013*fighter + 0.013*wordpress + 0.013*martial_art + 0.012*martial + 0.012*sparring + 0.011*ufc + 0.010*pen_pal

topic #55 (0.010): 0.005*episode + 0.003*film + 0.002*det + 0.002*podcast + 0.002*trailer + 0.001*dan + 0.001*scott + 0.001*director + 0.001*comedy + 0.001*audience

topic #56 (0.010): 0.008*meat + 0.007*sauce + 0.007*recipe + 0.006*cook + 0.006*cheese + 0.006*chicken + 0.006*garlic + 0.006*veggie + 0.006*pepper + 0.006*steak

topic #57 (0.010): 0.004*loan + 0.004*tax + 0.003*debt + 0.003*semester + 0.003*income + 0.003*gpa + 0.003*employer + 0.002*fund + 0.002*engineering + 0.002*payment

topic #58 (0.010): 0.007*lego + 0.005*disc + 0.004*bike + 0.004*rematch + 0.003*bra + 0.003*protector + 0.003*nascar + 0.003*rider + 0.003*strap + 0.003*string

topic #59 (0.010): 0.039*pokemon + 0.027*shiny + 0.017*ign + 0.011*giveaway + 0.011*ev + 0.011*deposited + 0.010*iv + 0.009*eevee + 0.009*breeding + 0.008*gts

topic #60 (0.010): 0.023*wallpaper + 0.017*jaime + 0.007*icon + 0.006*homer + 0.006*jon + 0.006*ned + 0.005*candle + 0.005*launcher + 0.005*lannister + 0.004*simpson

topic #61 (0.010): 0.026*makeup + 0.022*lipstick + 0.017*brow + 0.016*palette + 0.015*eyeshadow + 0.014*lip + 0.014*polish + 0.013*brush + 0.013*eyeliner + 0.011*mascara

topic #62 (0.010): 0.027*spiderman + 0.025*marvel + 0.015*avenger + 0.012*thor + 0.011*skate + 0.011*spidey + 0.010*iron_man + 0.010*xmen + 0.010*ug + 0.010*wolverine

topic #63 (0.010): 0.013*minecraft + 0.008*headliner + 0.008*colonist + 0.007*coachella + 0.007*gamestop + 0.006*shipped + 0.006*obsidian + 0.005*og + 0.005*pvp + 0.005*nether

topic #64 (0.010): 0.019*ign + 0.015*faction + 0.012*pvp + 0.010*skype + 0.008*dm + 0.008*stitch + 0.007*alien_blue + 0.007*vouch + 0.006*server + 0.006*cst

topic #65 (0.010): 0.020*sauron + 0.019*knife + 0.018*gandalf + 0.017*tolkien + 0.015*elf + 0.014*frodo + 0.014*hobbit + 0.009*bilbo + 0.008*dwarf + 0.008*lotr

topic #66 (0.010): 0.002*cop + 0.002*police + 0.002*officer + 0.001*pizza + 0.001*driver + 0.001*lawyer + 0.001*customer + 0.001*arrest + 0.001*court + 0.001*toilet

topic #67 (0.010): 0.017*twitch + 0.016*tinder + 0.009*streamer + 0.006*instagram + 0.006*photography + 0.005*photographer + 0.005*ig + 0.004*molotov + 0.004*moe + 0.004*swipe

topic #68 (0.010): 0.009*chelsea + 0.009*liverpool + 0.009*striker + 0.008*league + 0.007*ml + 0.006*gerrard + 0.006*arsenal + 0.006*messi + 0.006*kane + 0.005*perth

topic #69 (0.010): 0.005*linux + 0.004*file + 0.003*server + 0.003*developer + 0.003*software + 0.003*python + 0.003*java + 0.002*browser + 0.002*install + 0.002*php

topic #70 (0.010): 0.027*vet + 0.015*puppy + 0.014*pet + 0.014*breeder + 0.013*breed + 0.013*yarn + 0.012*rabbit + 0.011*litter + 0.011*shelter + 0.011*pup

topic #71 (0.010): 0.009*meme + 0.007*dank + 0.007*ayy + 0.005*ayy_lmao + 0.004*rekt + 0.004*lmao + 0.003*m8 + 0.003*gavin + 0.003*dank_meme + 0.003*duplicate

topic #72 (0.010): 0.067*firearm + 0.057*rifle + 0.040*ak + 0.018*pistol + 0.016*gem + 0.016*mag + 0.016*ar + 0.015*barrel + 0.014*ar15 + 0.013*muzzle

topic #73 (0.010): 0.006*orbit + 0.006*physic + 0.005*solar + 0.005*science + 0.005*math + 0.004*reactor + 0.004*equation + 0.004*universe + 0.004*nuclear + 0.004*planet

topic #74 (0.010): 0.023*beard + 0.019*printer + 0.019*vendor + 0.017*inventory + 0.016*seller + 0.015*amazon + 0.012*shipment + 0.012*listing + 0.009*undercut + 0.008*printing

topic #75 (0.010): 0.040*deck + 0.020*mana + 0.010*elsa + 0.009*creature + 0.007*druid + 0.006*aggro + 0.006*minion + 0.006*opponent + 0.006*anna + 0.005*gatherer

topic #76 (0.010): 0.025*archer + 0.025*mormon + 0.017*tc + 0.010*church + 0.007*lana + 0.007*temple + 0.006*gif + 0.006*chivalry + 0.006*kc + 0.005*steelers

topic #77 (0.010): 0.057*botrautomoderatorcommentsq11puwhatisautomoderator + 0.056*action_performed + 0.055*contact_moderator + 0.055*automatically_please + 0.054*i_botrautomoderatorcommentsq11puwhatisautomoderator + 0.040*moderator + 0.034*performed + 0.032*question_concern + 0.021*submission + 0.020*submission_automatically

topic #78 (0.010): 0.001*dragon + 0.001*sword + 0.001*chapter + 0.001*spell + 0.001*universe + 0.001*dwarf + 0.001*wizard + 0.001*weapon + 0.001*planet + 0.001*demon

topic #79 (0.010): 0.012*ps3 + 0.011*vita + 0.008*ps4 + 0.006*hentai + 0.005*psn + 0.005*persona + 0.005*sony + 0.004*final_fantasy + 0.004*bleach + 0.004*playstation

topic #80 (0.010): 0.017*ship + 0.015*vader + 0.012*jedi + 0.010*star_war + 0.009*vape + 0.009*luke + 0.009*x2 + 0.007*pax + 0.007*anakin + 0.007*darth

topic #81 (0.010): 0.009*sauce + 0.008*porn + 0.007*morgan + 0.006*cum + 0.006*griffith + 0.005*sp + 0.005*ua + 0.005*gif + 0.005*rune + 0.003*alexis

topic #82 (0.010): 0.348*ampnbsp + 0.130*debug + 0.036*blog + 0.033*tumblr + 0.030*root + 0.003*bondage + 0.003*gif + 0.002*dom + 0.002*clamp + 0.001*gag

topic #83 (0.010): 0.007*dean + 0.005*carlin + 0.004*rogan + 0.004*aston + 0.004*nico + 0.004*george_carlin + 0.003*lucifer + 0.003*gild + 0.003*sam + 0.003*burr

topic #84 (0.010): 0.054*ooc + 0.039*she + 0.014*nod + 0.014*smile + 0.010*grin + 0.009*magnus + 0.008*kiss + 0.007*chuckle + 0.007*clover + 0.006*shrug

topic #85 (0.010): 0.011*xxxx + 0.010*harper + 0.010*bart + 0.009*xxx + 0.008*xx + 0.007*rochester + 0.006*alberta + 0.005*mp + 0.005*lane + 0.005*texas

topic #86 (0.010): 0.015*qb + 0.011*nfl + 0.009*playoff + 0.008*draft + 0.008*coach + 0.006*cowboy + 0.005*steelers + 0.005*mariota + 0.005*raven + 0.005*wr

topic #87 (0.010): 0.023*vn + 0.012*rin + 0.010*raiden + 0.009*lilly + 0.007*shoujo + 0.007*saber + 0.007*shiv + 0.007*heist + 0.007*route + 0.006*skype

topic #88 (0.010): 0.007*kanye + 0.005*nigga + 0.004*rapper + 0.004*neckbeard + 0.004*eminem + 0.003*fedora + 0.003*rap + 0.003*pony + 0.003*meme + 0.003*mlady

topic #89 (0.010): 0.018*beer + 0.013*bottle + 0.012*wine + 0.010*brewery + 0.010*bourbon + 0.009*tea + 0.008*stout + 0.007*cocktail + 0.007*ale + 0.007*whisky

topic #90 (0.010): 0.031*fc + 0.028*gate_open + 0.019*villager + 0.015*added_you + 0.013*added_added + 0.013*gate + 0.013*pls + 0.012*stfu + 0.010*55 + 0.009*thank_feedback

topic #91 (0.010): 0.011*nigger + 0.011*tattoo + 0.008*piercing + 0.006*swimming + 0.006*piercings + 0.006*ng + 0.006*swim + 0.005*swimmer + 0.005*pierced + 0.005*queen

topic #92 (0.010): 0.020*router + 0.014*stream + 0.013*plex + 0.010*chromecast + 0.009*modem + 0.009*xbmc + 0.007*ap + 0.007*cable + 0.007*wireless + 0.007*roku

topic #93 (0.010): 0.003*government + 0.002*muslim + 0.002*religion + 0.002*political + 0.002*society + 0.002*christian + 0.002*islam + 0.001*liberal + 0.001*rape + 0.001*libertarian

topic #94 (0.010): 0.007*batman + 0.007*novel + 0.006*superman + 0.004*comic + 0.004*fiction + 0.004*trilogy + 0.004*author + 0.003*doctor + 0.003*writer + 0.003*scifi

topic #95 (0.010): 0.010*korra + 0.009*drawing + 0.009*melee + 0.007*sketch + 0.006*smash + 0.005*pencil + 0.005*artist + 0.004*falcon + 0.004*omega + 0.004*sheik

topic #96 (0.010): 0.008*apps + 0.008*android + 0.008*battery + 0.007*app + 0.007*nexus + 0.006*moto + 0.005*device + 0.005*lollipop + 0.005*rom + 0.005*iphone

topic #97 (0.010): 0.013*shoe + 0.012*jean + 0.010*jacket + 0.010*denim + 0.009*leather + 0.009*shirt + 0.008*boot + 0.007*sneaker + 0.007*dress + 0.007*tee

topic #98 (0.010): 0.011*kappa + 0.009*unaltered_suggestionhttpwwwredditcommessagecomposetotweetposterampsubjectsuggestion + 0.009*suggestionhttpwwwredditcommessagecomposetotweetposterampsubjectsuggestion + 0.009*faqhttpnpredditcomrtweetpostercomments13relk + 0.009*faqhttpnpredditcomrtweetpostercomments13relk_codehttpsgithubcombuttsciclestweetposter + 0.009*issueshttpsgithubcombuttsciclestweetposterissues + 0.009*codehttpsgithubcombuttsciclestweetposter + 0.009*leave_link + 0.009*unaltered + 0.008*fishing

topic #99 (0.010): 0.002*drug + 0.002*weed + 0.002*symptom + 0.002*dose + 0.002*doctor + 0.002*lsd + 0.002*gram + 0.002*anxiety + 0.002*mdma + 0.001*medication