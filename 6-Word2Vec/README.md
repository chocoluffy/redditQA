## Progress

Fixing issue listed here [10.18 meeting](https://github.com/chocoluffy/redditQA/issues/4).

### Check Topics

TF-IDF model with de-normalization from week 4. 
![tfidf](https://github.com/chocoluffy/redditQA/blob/master/5-Model-Inspection/results/topic_dist.png)

Normal BOW model.
![normal](https://github.com/chocoluffy/redditQA/blob/master/5-Model-Inspection/results/topic_dist_normal.png)

TF-IDF denorm version gives more polarized results than normal BOW version, meaning its ability to classify subreddit into topics is limited, given the assumption that author's interests are balanced. 

Other than above comparison, pure TF-IDF without de-normalization performs the worst from week 3's result.

### Pick Extreme Authors

Download [csv file](https://github.com/chocoluffy/redditQA/blob/master/5-Model-Inspection/results/updated_each_author_topic_comment.csv).

Each row represents a user, with columns: ["name", "dom_topics", "dom_topic_str", "score", "mapped_score", "contributions", "comments", "subreddit_num"]

- name: Author name;
- dom_topics: A array of tuples, each tuple contains the dominant topic ID and its probability. (it is obtained by weighted averaging all subreddits' topic distributions that author involve and do a cutoff using 8%)
- dom_topic_str: A string presentation of "dom_topics" field, by displaying the top 4 words of that topic.
- score: The generalist/specialist score calculated by pairwise similarity with Hellinger distance. Between 0 and 1, and more closer to 1 means more likely being specialist.
- mapped_score: The re-scaling value of "score" field, map from [0,1] to [1, 100].
- contributions: A sorted array of the total number of comment ups the author receive at each distinct subreddit, decreasingly.
- comments: The top voted 20 comments the author makes.
- subreddit_num: The number of distinct subreddit the author involves.

Sort by "mapped_score" in Excel can check the most extreme generalist and specialist's details.


### Hyper-parameters

- top 5% most acitve user.
- `topic_cut_off = 0.08`. Only investigate topics with probability higher than 0.08(0.1 gives less dominant topics).
- `corpus_tfidf = map(lambda x: map(lambda y: (y[0], round(y[1] * 200, 1)), x), corpus_tfidf)`. De-normalize TF-IDF weights to have approximate scale as BOW values.




## Original BOW Model


topic #0 (0.010): 0.009*doctor + 0.006*drug + 0.006*anxiety + 0.004*drinking + 0.004*depression + 0.004*meditation + 0.004*symptom + 0.003*healthy + 0.003*study + 0.003*med

topic #1 (0.010): 0.054*deck + 0.011*opponent + 0.010*combo + 0.010*minion + 0.009*mana + 0.009*ice + 0.009*corp + 0.008*matchup + 0.008*runner + 0.007*meta

topic #2 (0.010): 0.008*sex + 0.005*gay + 0.004*male + 0.003*female + 0.003*gender + 0.003*dating + 0.003*sexual + 0.003*trans + 0.003*boyfriend + 0.002*partner

topic #3 (0.010): 0.132*que + 0.125*de + 0.043*um + 0.039*da + 0.037*para + 0.033*se + 0.033*uma + 0.030*com + 0.028*o + 0.028*ma

topic #4 (0.010): 0.015*file + 0.007*speaker + 0.007*device + 0.007*server + 0.006*cable + 0.006*network + 0.006*gb + 0.006*download + 0.006*mac + 0.006*audio

topic #5 (0.010): 0.004*meme + 0.003*drawing + 0.003*gif + 0.003*lmao + 0.003*͡° + 0.003*comic + 0.003*upvote + 0.002*artist + 0.002*karma + 0.002*xd

topic #6 (0.010): 0.016*spell + 0.011*enemy + 0.009*hp + 0.008*armor + 0.008*weapon + 0.007*bonus + 0.007*dungeon + 0.007*dp + 0.006*dm + 0.006*farm

topic #7 (0.010): 0.059*coffee + 0.027*customer + 0.019*milk + 0.014*manager + 0.014*cup + 0.012*tea + 0.011*starbucks + 0.009*restaurant + 0.009*boat + 0.009*bean

topic #8 (0.010): 0.018*album + 0.013*band + 0.007*guitar + 0.006*bass + 0.005*listening + 0.004*drum + 0.004*artist + 0.004*metal + 0.004*genre + 0.004*chord

topic #9 (0.010): 0.021*planet + 0.011*sun + 0.011*universe + 0.010*solar + 0.008*galaxy + 0.008*moon + 0.007*orbit + 0.007*nuclear + 0.006*gas + 0.006*object

topic #10 (0.010): 0.011*tank + 0.008*makeup + 0.008*lip + 0.007*fish + 0.006*paint + 0.006*brush + 0.006*lipstick + 0.006*nail + 0.005*cream + 0.005*oil

topic #11 (0.010): 0.019*linux + 0.014*file + 0.011*web + 0.010*server + 0.010*php + 0.008*programmer + 0.008*install + 0.008*ubuntu + 0.008*portal + 0.007*package

topic #12 (0.010): 0.138*xx + 0.118*xxxx + 0.111*xxx + 0.100*xxxxxx + 0.009*karma + 0.004*gilded + 0.003*commenters + 0.003*per_user + 0.002*episode + 0.001*bitcoin

topic #13 (0.010): 0.015*lane + 0.011*gg + 0.011*gamergate + 0.011*tb + 0.009*champion + 0.007*adc + 0.007*mid + 0.006*jungle + 0.006*ad + 0.006*enemy

topic #14 (0.010): 0.045*blade + 0.036*razor + 0.027*shave + 0.024*soap + 0.020*brush + 0.020*shaving + 0.011*knife + 0.010*lather + 0.008*steel + 0.008*de

topic #15 (0.010): 0.023*climbing + 0.015*climb + 0.011*rope + 0.009*skate + 0.009*assist + 0.009*anchor + 0.008*route + 0.007*gear + 0.007*climber + 0.007*mid

topic #16 (0.010): 0.011*she + 0.007*smile + 0.004*ooc + 0.002*nod + 0.002*daughter + 0.002*sigh + 0.002*walked + 0.002*bottle + 0.002*seat + 0.002*husband

topic #17 (0.010): 0.047*tea + 0.018*hero + 0.016*soul + 0.014*ancient + 0.013*bl + 0.008*jack + 0.007*solomon + 0.006*buffy + 0.006*arrow + 0.006*oliver

topic #18 (0.010): 0.009*nfl + 0.008*coach + 0.008*qb + 0.008*defense + 0.008*draft + 0.008*playoff + 0.007*offense + 0.006*football + 0.005*cowboy + 0.005*bowl

topic #19 (0.010): 0.044*vegan + 0.036*animal + 0.030*meat + 0.021*vegetarian + 0.016*link_original + 0.014*pebble + 0.011*diet + 0.006*bacon + 0.006*dairy + 0.006*milk

topic #20 (0.010): 0.044*hero + 0.020*dota + 0.009*tesla + 0.009*league + 0.007*blizzard + 0.007*lane + 0.006*sc + 0.006*mid + 0.005*mmr + 0.005*korean

topic #21 (0.010): 0.011*hockey + 0.008*nhl + 0.007*jersey + 0.007*puck + 0.006*cap + 0.006*league + 0.006*goalie + 0.005*ice + 0.005*playoff + 0.004*contract

topic #22 (0.010): 0.018*weapon + 0.009*enemy + 0.008*ship + 0.006*unit + 0.006*shield + 0.005*halo + 0.005*mission + 0.004*map + 0.004*armor + 0.004*combat

topic #23 (0.010): 0.027*doctor + 0.020*episode + 0.012*jones + 0.007*dc + 0.007*pedal + 0.006*howard + 0.005*jon + 0.005*bjj + 0.004*scott + 0.004*belt

topic #24 (0.010): 0.093*tank + 0.057*tier + 0.044*t + 0.012*jax + 0.011*bot + 0.009*armor + 0.009*map + 0.008*premium + 0.007*crew + 0.007*arty

topic #25 (0.010): 0.063*da + 0.049*je + 0.047*na + 0.043*se + 0.036*di + 0.033*ne + 0.023*su + 0.017*ti + 0.017*bi + 0.016*si

topic #26 (0.010): 0.019*mountain + 0.018*park + 0.017*snow + 0.015*trail + 0.014*beach + 0.013*san + 0.013*lake + 0.012*mile + 0.012*island + 0.011*river

topic #27 (0.010): 0.006*russia + 0.006*nation + 0.005*russian + 0.005*army + 0.005*military + 0.004*usa + 0.004*government + 0.004*india + 0.004*empire + 0.003*culture

topic #28 (0.010): 0.014*ship + 0.011*vr + 0.009*pc + 0.007*assassin + 0.007*console + 0.007*fps + 0.007*ac + 0.006*keyboard + 0.005*oculus + 0.005*unity

topic #29 (0.010): 0.020*anime + 0.015*episode + 0.011*manga + 0.009*chapter + 0.008*arc + 0.006*gundam + 0.006*spoiler + 0.005*plot + 0.005*ending + 0.005*korra

topic #30 (0.010): 0.030*da + 0.028*und + 0.026*batman + 0.024*ich + 0.023*der + 0.021*ist + 0.018*comic + 0.018*nicht + 0.016*marvel + 0.015*e

topic #31 (0.010): 0.024*server + 0.007*pvp + 0.007*gear + 0.005*guild + 0.005*map + 0.005*quest + 0.004*bug + 0.004*patch + 0.003*raid + 0.003*minecraft

topic #32 (0.010): 0.012*wire + 0.012*battery + 0.008*led + 0.008*heat + 0.008*voltage + 0.006*circuit + 0.006*unit + 0.005*pin + 0.005*output + 0.005*panel

topic #33 (0.010): 0.018*beard + 0.009*curl + 0.008*cute + 0.007*persona + 0.007*makeup + 0.006*oil + 0.006*smile + 0.006*eyebrow + 0.006*dry + 0.006*facial

topic #34 (0.010): 0.040*episode + 0.007*podcast + 0.007*adam + 0.003*comedy + 0.003*frank + 0.003*netflix + 0.003*dan + 0.003*joe + 0.003*alison + 0.003*guest

topic #35 (0.010): 0.030*ray + 0.028*gavin + 0.023*ryan + 0.017*geoff + 0.011*michael + 0.011*gu + 0.009*gta + 0.009*rpics + 0.007*jack + 0.007*minecraft

topic #36 (0.010): 0.075*plant + 0.023*bug + 0.015*soil + 0.014*seed + 0.013*flower + 0.010*root + 0.008*listing + 0.008*generated + 0.008*karma + 0.008*modmail

topic #37 (0.010): 0.021*plane + 0.016*aircraft + 0.015*pilot + 0.014*flight + 0.012*f + 0.010*tank + 0.010*flying + 0.007*fighter + 0.007*jet + 0.007*wing

topic #38 (0.010): 0.136*submission + 0.039*tab + 0.036*removal + 0.017*moderator + 0.015*flair + 0.012*original_post + 0.011*rnews + 0.009*submission_removed + 0.007*subreddit_rule + 0.007*meta

topic #39 (0.010): 0.019*lens + 0.014*mm + 0.009*film + 0.009*photography + 0.008*exposure + 0.008*frame + 0.007*iso + 0.006*f + 0.006*canon + 0.006*shooting

topic #40 (0.010): 0.014*gym + 0.012*muscle + 0.012*lb + 0.011*training + 0.010*squat + 0.010*knife + 0.010*lift + 0.009*workout + 0.007*calorie + 0.007*exercise

topic #41 (0.010): 0.026*app + 0.015*android + 0.013*apps + 0.013*device + 0.012*battery + 0.008*io + 0.007*iphone + 0.007*nexus + 0.007*apple + 0.005*icon

topic #42 (0.010): 0.019*survivor + 0.016*rating + 0.013*play_store + 0.012*ad + 0.011*perk + 0.010*survey + 0.009*sb + 0.009*epic + 0.008*legendary + 0.008*reward

topic #43 (0.010): 0.013*religion + 0.013*church + 0.011*christian + 0.009*belief + 0.006*bible + 0.006*catholic + 0.006*religious + 0.006*atheist + 0.006*muslim + 0.005*faith

topic #44 (0.010): 0.037*league + 0.012*ml + 0.012*chelsea + 0.010*manager + 0.009*football + 0.009*kane + 0.008*liverpool + 0.008*striker + 0.008*transfer + 0.007*squad

topic #45 (0.010): 0.004*park + 0.004*traffic + 0.004*police + 0.003*driver + 0.003*parking + 0.003*downtown + 0.003*station + 0.003*ticket + 0.002*neighborhood + 0.002*restaurant

topic #46 (0.010): 0.010*meat + 0.009*chicken + 0.009*recipe + 0.009*cheese + 0.008*cook + 0.008*egg + 0.007*sauce + 0.007*oil + 0.007*butter + 0.007*meal

topic #47 (0.010): 0.067*ja + 0.039*ei + 0.021*chess + 0.020*se + 0.017*ole + 0.015*bg + 0.013*tai + 0.009*sen + 0.009*pawn + 0.008*nyt

topic #48 (0.010): 0.027*disney + 0.023*disc + 0.019*park + 0.015*amazon + 0.015*confirmed + 0.014*completed + 0.014*traded + 0.011*paypal + 0.010*golf + 0.009*rematch

topic #49 (0.010): 0.131*de + 0.055*la + 0.042*et + 0.042*pa + 0.039*que + 0.034*un + 0.028*il + 0.028*en + 0.028*je + 0.026*cest

topic #50 (0.010): 0.004*novel + 0.004*dragon + 0.003*lord + 0.003*fantasy + 0.003*harry + 0.003*plot + 0.003*author + 0.003*evil + 0.003*elf + 0.003*dwarf

topic #51 (0.010): 0.033*map + 0.009*server + 0.008*tf + 0.007*silver + 0.006*banned + 0.006*competitive + 0.005*scout + 0.005*knife + 0.005*rank + 0.005*faction

topic #52 (0.010): 0.016*bow + 0.011*fighter + 0.010*baseball + 0.009*boxing + 0.009*arrow + 0.009*mets + 0.008*floyd + 0.007*sport + 0.006*dodger + 0.006*flamingo

topic #53 (0.010): 0.031*israel + 0.026*jew + 0.021*muslim + 0.020*jewish + 0.015*israeli + 0.015*conservative + 0.009*tax + 0.007*government + 0.005*district + 0.005*public_school

topic #54 (0.010): 0.096*uchangetip + 0.034*changetip + 0.027*bitcoin + 0.016*rbitcoin + 0.014*pd + 0.013*collected + 0.013*changetip_video + 0.013*changetip_info + 0.010*tg + 0.010*bitcoin_tip

topic #55 (0.010): 0.015*gta + 0.014*mission + 0.011*tracker + 0.011*invite + 0.010*crew + 0.008*psn + 0.008*monster + 0.007*xbox + 0.006*hunter + 0.006*pc

topic #56 (0.010): 0.096*det + 0.057*att + 0.052*som + 0.050*er + 0.049*en + 0.044*på + 0.036*de + 0.036*har + 0.035*med + 0.034*og

topic #57 (0.010): 0.028*uber + 0.022*route + 0.020*driver + 0.015*surge + 0.012*morgan + 0.011*taxi + 0.010*vn + 0.009*eso + 0.009*gg + 0.006*fare

topic #58 (0.010): 0.042*pen + 0.018*ink + 0.016*nib + 0.013*print + 0.013*printer + 0.008*capitalism + 0.007*worker + 0.007*printing + 0.006*communist + 0.006*colonist

topic #59 (0.010): 0.099*feedback + 0.079*blog + 0.072*faq + 0.063*ampnbsp + 0.062*debug + 0.058*root + 0.051*tumblr + 0.016*picture_picture + 0.013*queen + 0.009*drag

topic #60 (0.010): 0.102*de + 0.098*que + 0.093*la + 0.052*en + 0.049*el + 0.037*e + 0.033*un + 0.033*los + 0.028*se + 0.026*lo

topic #61 (0.010): 0.033*bra + 0.020*japanese + 0.016*sp + 0.013*cup + 0.013*band + 0.012*goku + 0.010*breast + 0.009*firearm + 0.007*boo + 0.006*kanji

topic #62 (0.010): 0.040*dip + 0.026*welding + 0.019*cope + 0.017*mint + 0.017*weld + 0.016*redneck + 0.014*copenhagen + 0.013*welder + 0.010*southern + 0.009*dipping

topic #63 (0.010): 0.007*police + 0.007*government + 0.006*society + 0.005*cop + 0.004*feminist + 0.004*crime + 0.004*rape + 0.004*political + 0.003*feminism + 0.003*racist

topic #64 (0.010): 0.017*smash + 0.014*mario + 0.014*nintendo + 0.013*wii + 0.008*melee + 0.007*zelda + 0.007*lego + 0.007*pokemon + 0.006*fox + 0.006*console

topic #65 (0.010): 0.040*snapshot + 0.032*skyrim + 0.023*morrowind + 0.020*open_source + 0.019*mirror + 0.013*fallout + 0.011*quest + 0.010*oblivion + 0.007*imperial + 0.007*legion

topic #66 (0.010): 0.008*rifle + 0.007*stock + 0.007*barrel + 0.006*kit + 0.006*shooting + 0.005*mag + 0.005*mm + 0.005*ammo + 0.004*shipping + 0.004*ebay

topic #67 (0.010): 0.089*de + 0.033*het + 0.031*sa + 0.031*nu + 0.026*si + 0.026*dat + 0.023*ik + 0.022*la + 0.021*ca + 0.021*pe

topic #68 (0.010): 0.016*tax + 0.011*income + 0.008*fund + 0.007*bank + 0.007*fee + 0.006*stock + 0.006*loan + 0.006*payment + 0.006*cash + 0.006*debt

topic #69 (0.010): 0.023*sexy + 0.018*porn + 0.012*cock + 0.011*che + 0.010*cute + 0.009*tit + 0.009*gorgeous + 0.008*cum + 0.007*pussy + 0.007*boob

topic #70 (0.010): 0.008*teacher + 0.008*university + 0.008*engineering + 0.007*career + 0.006*semester + 0.006*study + 0.005*science + 0.005*interview + 0.005*professor + 0.004*teaching

topic #71 (0.010): 0.052*deck + 0.022*creature + 0.014*mana + 0.012*gatherer + 0.009*token + 0.008*mc + 0.008*opponent + 0.008*spell + 0.008*combo + 0.008*pod

topic #72 (0.010): 0.000*plant + 0.000*soil + 0.000*seed + 0.000*tomato + 0.000*garden + 0.000*la + 0.000*fruit + 0.000*root + 0.000*bjj + 0.000*flower

topic #73 (0.010): 0.005*science + 0.005*universe + 0.004*philosophy + 0.003*evidence + 0.003*moral + 0.003*specie + 0.002*study + 0.002*sentence + 0.002*definition + 0.002*society

topic #74 (0.010): 0.050*moderator + 0.047*performed + 0.041*botrautomoderatorcommentsqpuwhatisautomoderator + 0.041*action_performed + 0.037*contact_moderator + 0.037*automatically_please + 0.036*i_botrautomoderatorcommentsqpuwhatisautomoderator + 0.023*question_concern + 0.021*submission + 0.011*bot

topic #75 (0.010): 0.022*router + 0.013*cable + 0.012*network + 0.011*antenna + 0.010*wedding + 0.009*device + 0.009*port + 0.008*ip + 0.008*og + 0.008*optic

topic #76 (0.010): 0.012*florida + 0.009*lineup + 0.007*truck + 0.006*league + 0.006*betting + 0.005*uc + 0.005*driver + 0.005*skating + 0.005*sf + 0.004*hh

topic #77 (0.010): 0.014*ship + 0.008*engine + 0.007*station + 0.006*rocket + 0.006*fuel + 0.005*launch + 0.005*landing + 0.005*engineer + 0.004*faq + 0.004*planet

topic #78 (0.010): 0.075*film + 0.013*director + 0.011*horror + 0.010*imdb + 0.008*stfu + 0.007*netflix + 0.007*rating + 0.007*writer + 0.007*script + 0.006*actor

topic #79 (0.010): 0.021*shoe + 0.016*boot + 0.014*shirt + 0.011*jean + 0.011*dress + 0.010*pant + 0.010*leather + 0.010*jacket + 0.008*clothes + 0.005*clothing

topic #80 (0.010): 0.008*pc + 0.005*gameplay + 0.005*steam + 0.005*gaming + 0.004*console + 0.003*stream + 0.003*dlc + 0.003*xbox + 0.003*fps + 0.003*soul

topic #81 (0.010): 0.014*smoke + 0.013*beer + 0.010*smoking + 0.009*bottle + 0.008*flavor + 0.006*weed + 0.006*cigar + 0.005*juice + 0.005*pipe + 0.005*vape

topic #82 (0.010): 0.106*rr + 0.047*moderator + 0.036*guideline + 0.034*performed + 0.034*botrautomoderatorcommentsqpuwhatisautomoderator + 0.029*tagging + 0.027*f + 0.026*letter + 0.024*format + 0.024*gender

topic #83 (0.010): 0.007*uk + 0.007*government + 0.005*germany + 0.005*german + 0.004*china + 0.004*chinese + 0.004*london + 0.003*visa + 0.003*nuclear + 0.003*tax

topic #84 (0.010): 0.030*jay + 0.019*tattoo + 0.014*evidence + 0.013*lucid + 0.010*dart + 0.009*murder + 0.007*dreaming + 0.006*artist + 0.006*guilty + 0.006*nerf

topic #85 (0.010): 0.133*steam + 0.041*giveaway + 0.031*confirmed + 0.020*csgo + 0.017*paypal + 0.015*shipped + 0.014*bundle + 0.013*tf + 0.012*thanks_giveaway + 0.011*valve

topic #86 (0.010): 0.040*bitcoin + 0.020*coin + 0.012*btc + 0.010*doge + 0.009*exchange + 0.009*scam + 0.008*wallet + 0.007*bitcoins + 0.007*transaction + 0.006*currency

topic #87 (0.010): 0.011*vet + 0.011*animal + 0.010*pet + 0.007*puppy + 0.007*breed + 0.005*rat + 0.005*training + 0.005*toy + 0.005*shelter + 0.005*rabbit

topic #88 (0.010): 0.015*stream + 0.010*cup + 0.008*melbourne + 0.008*australia + 0.007*cunt + 0.007*sport + 0.007*sydney + 0.006*west + 0.005*rugby + 0.005*newcastle

topic #89 (0.010): 0.134*artist + 0.119*remix + 0.078*dj + 0.039*genre + 0.037*van + 0.033*trance + 0.022*resubmit + 0.015*producer + 0.014*feat + 0.014*techno

topic #90 (0.010): 0.031*prison + 0.029*prisoner + 0.021*crate + 0.018*cell + 0.017*gopro + 0.011*delivery + 0.010*inmate + 0.010*guard + 0.009*email + 0.007*staff

topic #91 (0.010): 0.000*xx + 0.000*sex + 0.000*xxxx + 0.000*xxxxxx + 0.000*xxx + 0.000*de + 0.000*stfu + 0.000*rabbit + 0.000*que + 0.000*submission

topic #92 (0.010): 0.051*coin + 0.033*barry + 0.032*silver + 0.023*flash + 0.009*dart + 0.008*arrow + 0.008*cocktail + 0.007*bronze + 0.007*collection + 0.006*reverse

topic #93 (0.010): 0.029*gb + 0.025*cpu + 0.013*motherboard + 0.013*intel + 0.012*monitor + 0.011*core + 0.011*ram + 0.011*newegg + 0.010*atx + 0.010*supply

topic #94 (0.010): 0.124*submitted + 0.109*sex + 0.069*domain + 0.067*submission + 0.052*partner + 0.030*poly + 0.019*marriage + 0.016*husband + 0.013*divorce + 0.013*ap

topic #95 (0.010): 0.022*function + 0.011*python + 0.010*math + 0.009*object + 0.009*programming + 0.007*string + 0.007*cube + 0.007*variable + 0.006*r + 0.006*solve

topic #96 (0.010): 0.010*nba + 0.007*defense + 0.007*basketball + 0.007*lebron + 0.007*smith + 0.007*shooting + 0.006*league + 0.006*kobe + 0.006*bench + 0.005*coach

topic #97 (0.010): 0.035*pokemon + 0.026*shiny + 0.016*iv + 0.014*ign + 0.013*fc + 0.013*flair + 0.011*female + 0.011*egg + 0.010*male + 0.010*mega

topic #98 (0.010): 0.017*bike + 0.013*wheel + 0.011*tire + 0.010*engine + 0.008*truck + 0.007*vehicle + 0.007*mile + 0.007*driver + 0.006*brake + 0.006*rear

topic #99 (0.010): 0.036*pattern + 0.023*stitch + 0.023*yarn + 0.022*netflix + 0.016*fabric + 0.013*knit + 0.012*needle + 0.010*knitting + 0.009*sewing + 0.008*quilt