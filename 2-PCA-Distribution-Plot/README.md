## Plots

The following plots uses topic number N = 100.

Rudimentary Visual:
![raw](https://github.com/chocoluffy/redditQA/blob/master/2-PCA-Distribution-Plot/results/raw.png)

Make it prettier:
![pretty](https://github.com/chocoluffy/redditQA/blob/master/2-PCA-Distribution-Plot/results/full.png)

Examine local tribes:

- Game
![game](https://github.com/chocoluffy/redditQA/blob/master/2-PCA-Distribution-Plot/results/game-cluster.png)

- Anime & Science
![anime](https://github.com/chocoluffy/redditQA/blob/master/2-PCA-Distribution-Plot/results/anime%26science-cluster.png)

- Daily life topics & Funny jokes
![life](https://github.com/chocoluffy/redditQA/blob/master/2-PCA-Distribution-Plot/results/daily-life-jokes-cluster.png)

- Other small tribes (subreddits with less comments)
![small](https://github.com/chocoluffy/redditQA/blob/master/2-PCA-Distribution-Plot/results/smaller-tribes.png)

When we pick topic number N = 500:

![500](https://github.com/chocoluffy/redditQA/blob/master/2-PCA-Distribution-Plot/results/full-500topics2.png)
![500-2](https://github.com/chocoluffy/redditQA/blob/master/2-PCA-Distribution-Plot/results/full-500topics2.png)


## Further Explore

Given a random subreddit, can find its semantically relevant subreddits by searching through its closest N neighbors.

-> can clustering subreddit's topic vector, (currently topic vector in length 100, the number is set by user), and 100 topics will not necessarily generate 100 local clusters, as each topic is a distribution of words, and words can repeat under different topics, thus final number of clusters N will be << 100, and can be treated as labels.

-> given cluster and labels, we can observe from the perspective of reddit users by looking at which clusters of topics they have contributed to, and form a distribution of clusters for each user.

-> and thus given each user will have a cluster vector, of length the number of clusters generated, we can form a matrix of user to cluster vector, and visualize that into 2-dimensinal bubble plots and examine how closely each user are to each other from the perspective of their contribution towards reddit community. If two users are mostly contribute to the same clusters, their cluster vector will be close and so does the points on plots.

-> 【business value】: recommend talkative friends to users! (by pairing users with utmost coverage with similar clusters) so that they can subscribe to each other's timeline or simply just spark more talks, based on the assuption that they share more common interests. 

But, to achieve the same goal, how about the collaborative filtering?


## Results Analysis

### For some specific subreddits

For subreddit:  sports  , the dominant topic is:  55  with prob:  0.946214236108 [(u'like', 0.011087387610678684), (u'it', 0.0093680805542206511), (u'one', 0.0086519078867964786), (u'think', 0.0070324609834460554), (u'time', 0.0065027045776066472), (u'match', 0.0062731460845245014), (u'people', 0.0062219240262443663), (u'get', 0.0062160119208536759), (u'look', 0.0061323629948739026), (u'dont', 0.0057569724123223863), (u'really', 0.005544670614390115), (u'much', 0.0047943417880615862), (u'would', 0.0047567246641804176), (u'guy', 0.0047375955307975611), (u'cena', 0.0046395501184146185), (u'even', 0.004292544006002855), (u'owen', 0.0042583150373042208), (u'wwe', 0.0042242151628961409), (u'back', 0.003791728152328284), (u'thing', 0.0037067632828028897)]

For subreddit:  technology  , the dominant topic is:  5  with prob:  0.499099070198 [(u'people', 0.011383612552051033), (u'it', 0.0080071297050256559), (u'would', 0.007221692313621228), (u'u', 0.005166862890726813), (u'country', 0.004294637242946913), (u'state', 0.0040288956579367773), (u'like', 0.0039328834053325877), (u'one', 0.0038917151003275189), (u'law', 0.0037374781772805828), (u'government', 0.0036247694478967374), (u'even', 0.0035208414773401074), (u'time', 0.0033292159569652062), (u'year', 0.0032381885777499199), (u'many', 0.003131044817484642), (u'dont', 0.0030429561225119917), (u'also', 0.0030069360975051342), (u'get', 0.0029864415474676236), (u'way', 0.0029700148104635027), (u'right', 0.002923793923789737), (u'make', 0.0029103416594497729)]

For subreddit:  Music  , the dominant topic is:  86  with prob:  0.651615518061 [(u'it', 0.011469860811182847), (u'like', 0.011273183530741962), (u'one', 0.0071964344137323694), (u'get', 0.0071172615258524334), (u'dont', 0.0067568930380207046), (u'would', 0.0062126179788250099), (u'people', 0.0059532579174598711), (u'im', 0.0058177055447945413), (u'time', 0.0057778463051540536), (u'know', 0.0050547793731076209), (u'think', 0.0044648381465809848), (u'thing', 0.0043807369346259579), (u'guy', 0.0041316788294841035), (u'make', 0.0040870313498464943), (u'really', 0.0040084961489970398), (u'go', 0.0038548912083067335), (u'year', 0.0037766914015277008), (u'want', 0.0034978690840969801), (u'got', 0.0033855200113045822), (u'even', 0.0033595154709892398)]

For subreddit:  4chan  , the dominant topic is:  86  with prob:  0.558498735081 [(u'it', 0.011469860811182847), (u'like', 0.011273183530741962), (u'one', 0.0071964344137323694), (u'get', 0.0071172615258524334), (u'dont', 0.0067568930380207046), (u'would', 0.0062126179788250099), (u'people', 0.0059532579174598711), (u'im', 0.0058177055447945413), (u'time', 0.0057778463051540536), (u'know', 0.0050547793731076209), (u'think', 0.0044648381465809848), (u'thing', 0.0043807369346259579), (u'guy', 0.0041316788294841035), (u'make', 0.0040870313498464943), (u'really', 0.0040084961489970398), (u'go', 0.0038548912083067335), (u'year', 0.0037766914015277008), (u'want', 0.0034978690840969801), (u'got', 0.0033855200113045822), (u'even', 0.0033595154709892398)]

For subreddit:  nba  , the dominant topic is:  86  with prob:  0.801322618748 [(u'it', 0.011469860811182847), (u'like', 0.011273183530741962), (u'one', 0.0071964344137323694), (u'get', 0.0071172615258524334), (u'dont', 0.0067568930380207046), (u'would', 0.0062126179788250099), (u'people', 0.0059532579174598711), (u'im', 0.0058177055447945413), (u'time', 0.0057778463051540536), (u'know', 0.0050547793731076209), (u'think', 0.0044648381465809848), (u'thing', 0.0043807369346259579), (u'guy', 0.0041316788294841035), (u'make', 0.0040870313498464943), (u'really', 0.0040084961489970398), (u'go', 0.0038548912083067335), (u'year', 0.0037766914015277008), (u'want', 0.0034978690840969801), (u'got', 0.0033855200113045822), (u'even', 0.0033595154709892398)]

For subreddit:  apple  , the dominant topic is:  49  with prob:  0.863821733955 [(u'it', 0.010656441211939821), (u'u', 0.0068737578454730695), (u'game', 0.0068544057195435611), (u'use', 0.0066414382560581317), (u'one', 0.0062687398605598592), (u'like', 0.0049020254803554993), (u'dont', 0.004894797998293822), (u'want', 0.0047580833019199749), (u'apple', 0.0047580764345340042), (u'pc', 0.00473649200037641), (u'thing', 0.0044212994000362724), (u'right', 0.0043555038196155041), (u'really', 0.0042130410220909027), (u'update', 0.0041742229841560518), (u'time', 0.0040640908465968762), (u'google', 0.0040573954984478395), (u'work', 0.0039689580645811918), (u'2', 0.0039479903030041003), (u'make', 0.0037582358726961501), (u'would', 0.0037467186222058875)]

For subreddit:  PS4  , the dominant topic is:  61  with prob:  0.693972291939 [(u'game', 0.017928831580174699), (u'it', 0.013271417445039766), (u'like', 0.010508002712660501), (u'one', 0.0073933226624713572), (u'get', 0.0056276120825998442), (u'would', 0.0053530150881997973), (u'people', 0.0051698161724853817), (u'dont', 0.0050086422359945067), (u'make', 0.0046387509940797331), (u'look', 0.0045117209780389401), (u'really', 0.0044921925702589623), (u'time', 0.0043987690883699948), (u'im', 0.0042801194583691402), (u'new', 0.0040773112079892969), (u'think', 0.003825341541062427), (u'good', 0.0038234422595791085), (u'much', 0.0035992705172136624), (u'even', 0.0035261002012282852), (u'play', 0.0035158781985551958), (u'going', 0.003466188717434193)]

For subreddit:  anime  , the dominant topic is:  86  with prob:  0.397621795801 [(u'it', 0.011469860811182847), (u'like', 0.011273183530741962), (u'one', 0.0071964344137323694), (u'get', 0.0071172615258524334), (u'dont', 0.0067568930380207046), (u'would', 0.0062126179788250099), (u'people', 0.0059532579174598711), (u'im', 0.0058177055447945413), (u'time', 0.0057778463051540536), (u'know', 0.0050547793731076209), (u'think', 0.0044648381465809848), (u'thing', 0.0043807369346259579), (u'guy', 0.0041316788294841035), (u'make', 0.0040870313498464943), (u'really', 0.0040084961489970398), (u'go', 0.0038548912083067335), (u'year', 0.0037766914015277008), (u'want', 0.0034978690840969801), (u'got', 0.0033855200113045822), (u'even', 0.0033595154709892398)]

And printing out some random topics, by running `lda.print_topics(20)`:

2017-10-02 12:20:25,485 : INFO : topic #41 (0.010): 0.008*one + 0.007*number + 0.006*it + 0.006*get + 0.006*need + 0.005*shall + 0.005*scientist + 0.005*omar + 0.005*ac51 + 0.005*actually

2017-10-02 12:20:25,493 : INFO : topic #62 (0.010): 0.019*cat + 0.019*dog + 0.012*like + 0.010*it + 0.007*one + 0.007*people + 0.006*would + 0.005*get + 0.005*see + 0.005*guy

2017-10-02 12:20:25,500 : INFO : topic #21 (0.010): 0.017*it + 0.007*people + 0.006*dont + 0.005*game + 0.005*grayson + 0.005*refund + 0.005*developer + 0.005*fortran + 0.005*turn + 0.004*know

2017-10-02 12:20:25,506 : INFO : topic #34 (0.010): 0.081*meme + 0.054*4chan + 0.033*reddit + 0.032*it’s + 0.031*ampnbsp + 0.028*comic + 0.022*board + 0.021*popular + 0.019*site + 0.016*b

2017-10-02 12:20:25,512 : INFO : topic #12 (0.010): 0.010*it + 0.007*gavin + 0.006*see + 0.006*fan + 0.006*like + 0.006*intolerance + 0.006*deli + 0.006*burnie + 0.004*ah + 0.004*comment

2017-10-02 12:20:25,518 : INFO : topic #7 (0.010): 0.012*twin + 0.012*aerial + 0.007*penis + 0.007*like + 0.007*would + 0.007*reddit + 0.005*gold + 0.005*even + 0.005*right + 0.005*everyone

2017-10-02 12:20:25,524 : INFO : topic #96 (0.010): 0.008*it + 0.008*dont + 0.008*unusually + 0.006*say + 0.006*me + 0.006*box + 0.006*ness + 0.005*win + 0.005*ill + 0.005*right

2017-10-02 12:20:25,530 : INFO : topic #31 (0.010): 0.012*it + 0.008*like + 0.008*would + 0.006*one + 0.006*think + 0.005*thing + 0.005*make + 0.004*dont + 0.004*could + 0.004*get

2017-10-02 12:20:25,537 : INFO : topic #5 (0.010): 0.011*people + 0.008*it + 0.007*would + 0.005*u + 0.004*country + 0.004*state + 0.004*like + 0.004*one + 0.004*law + 0.004*government

2017-10-02 12:20:25,544 : INFO : topic #67 (0.010): 0.009*degree + 0.008*vr + 0.008*ppd + 0.007*im + 0.007*get + 0.007*like + 0.006*latency + 0.006*two + 0.006*eye + 0.005*fov

2017-10-02 12:20:25,551 : INFO : topic #71 (0.010): 0.017*weight + 0.010*it + 0.009*food + 0.008*like + 0.008*eat + 0.006*calorie + 0.006*exercise + 0.006*get + 0.006*would + 0.006*fat

2017-10-02 12:20:25,557 : INFO : topic #8 (0.010): 0.012*fookin + 0.008*abe + 0.008*worldthats + 0.006*little + 0.006*whole + 0.006*man + 0.006*got + 0.005*bitch + 0.004*your + 0.004*ice

2017-10-02 12:20:25,563 : INFO : topic #18 (0.010): 0.014*get + 0.009*cop + 0.008*police + 0.007*dont + 0.007*one + 0.006*like + 0.006*need + 0.006*time + 0.006*even + 0.006*people

2017-10-02 12:20:25,569 : INFO : topic #17 (0.010): 0.028*de + 0.021*la + 0.019*un + 0.012*ma + 0.012*et + 0.012*chauffeur + 0.009*le + 0.009*taxi + 0.009*une + 0.009*en

2017-10-02 12:20:25,576 : INFO : topic #15 (0.010): 0.007*one + 0.007*like + 0.006*it + 0.006*want + 0.006*get + 0.006*would + 0.005*going + 0.005*im + 0.005*picture + 0.005*fleet

2017-10-02 12:20:25,582 : INFO : topic #52 (0.010): 0.015*sander + 0.010*gop + 0.010*nomination + 0.007*would + 0.007*it + 0.007*something + 0.006*enough + 0.005*need + 0.005*win + 0.005*clinton

2017-10-02 12:20:25,588 : INFO : topic #76 (0.010): 0.014*magic + 0.014*it + 0.013*suspect + 0.013*prime + 0.011*deck + 0.010*competitive + 0.009*card + 0.009*creature + 0.009*collection + 0.009*time

2017-10-02 12:20:25,596 : INFO : topic #23 (0.010): 0.009*like + 0.006*lol + 0.006*pee + 0.006*trash + 0.006*doge + 0.006*persuaded + 0.006*arsene + 0.006*lukaku + 0.005*people + 0.005*want

2017-10-02 12:20:25,602 : INFO : topic #51 (0.010): 0.013*it + 0.009*arin + 0.008*edit + 0.006*sub + 0.006*map + 0.006*people + 0.005*criticism + 0.005*grump + 0.004*didnt + 0.004*this

2017-10-02 12:20:25,608 : INFO : topic #4 (0.010): 0.010*it + 0.007*pokemon + 0.007*would + 0.007*like + 0.007*luvdisc + 0.006*much + 0.006*reich + 0.006*pikachu + 0.005*though + 0.005*game

We observe a phenomenon that, for some reddits, they are easily classified to be dominated by topic 86 (which is like daily speaking style). However, those words can also well-likely appear in other subreddits. Use TF-IDF to filter them!

### After applying TF-IDF:

2017-10-03 09:54:48,328 : INFO : topic #49 (0.010): 0.052*key + 0.029*karma + 0.027*rule + 0.025*bot + 0.024*text + 0.022*flair + 0.021*please + 0.019*check + 0.018*clan + 0.016*vote

2017-10-03 09:54:48,333 : INFO : topic #27 (0.010): 0.358*thank + 0.237*you + 0.203*thank_you + 0.031*free + 0.025*awesome + 0.013*get + 0.011*exp + 0.008*2 + 0.007*bonus + 0.006*brute

2017-10-03 09:54:48,337 : INFO : topic #26 (0.010): 0.017*window + 0.013*drive + 0.012*run + 0.011*computer + 0.010*use + 0.010*need + 0.007*ram + 0.007*running + 0.007*work + 0.007*one

2017-10-03 09:54:48,342 : INFO : topic #43 (0.010): 0.034*year + 0.033*im + 0.030*new + 0.019*happy + 0.015*thanks + 0.012*love + 0.011*good + 0.011*happy_new + 0.009*time + 0.009*one

2017-10-03 09:54:48,348 : INFO : topic #51 (0.010): 0.018*use + 0.011*using + 0.011*code + 0.011*file + 0.008*data + 0.007*work + 0.006*make + 0.006*need + 0.005*way + 0.005*type

2017-10-03 09:54:48,352 : INFO : topic #29 (0.010): 0.111*word + 0.027*cloud + 0.025*train + 0.020*made + 0.017*subreddits + 0.014*use + 0.014*request + 0.014*common + 0.013*subreddit + 0.012*ml

2017-10-03 09:54:48,357 : INFO : topic #84 (0.010): 0.013*would + 0.007*time + 0.006*much + 0.006*year + 0.006*even + 0.006*people + 0.005*point + 0.004*see + 0.004*make + 0.004*still

2017-10-03 09:54:48,361 : INFO : topic #69 (0.010): 0.239*original + 0.151*amp + 0.106*link + 0.036*remix + 0.035*feat + 0.032*mix + 0.028*track + 0.028*link_original + 0.022*here + 0.018*dj

2017-10-03 09:54:48,365 : INFO : topic #75 (0.010): 0.081*video + 0.034*link + 0.028*image + 0.024*source + 0.020*thanks + 0.019*cs + 0.015*youtube + 0.014*camera + 0.013*this + 0.012*picture

2017-10-03 09:54:48,369 : INFO : topic #76 (0.010): 0.188*henry + 0.104*violet + 0.068*13th + 0.063*confess + 0.062*artisan + 0.060*nifty + 0.052*relatively_low + 0.048*welsh + 0.044*wale + 0.039*unforgiving

2017-10-03 09:54:48,374 : INFO : topic #57 (0.010): 0.100*riot + 0.079*fuck + 0.051*meme + 0.050*shit + 0.044*fucking + 0.024*bitch + 0.024*pls + 0.021*ayy + 0.021*ur + 0.020*yeah

2017-10-03 09:54:48,378 : INFO : topic #83 (0.010): 0.598*son + 0.088*cest + 0.046*escort + 0.041*noah + 0.040*cursed + 0.032*orion + 0.022*petite + 0.021*jenkins + 0.012*vie + 0.005*ooh

2017-10-03 09:54:48,382 : INFO : topic #3 (0.010): 0.262*cool + 0.248*late + 0.127*bob + 0.042*refined + 0.033*punctuation + 0.029*maria + 0.028*bit_late + 0.021*noticed + 0.020*celebration + 0.019*deadpool

2017-10-03 09:54:48,386 : INFO : topic #15 (0.010): 0.304*ad + 0.123*per + 0.082*ed + 0.077*non + 0.053*di + 0.037*ho + 0.029*il + 0.027*dare + 0.024*ci + 0.021*exist

2017-10-03 09:54:48,391 : INFO : topic #14 (0.010): 0.017*one + 0.016*thanks + 0.014*trade + 0.014*got + 0.013*get + 0.011*would + 0.011*ill + 0.010*im + 0.009*sent + 0.007*send

2017-10-03 09:54:48,395 : INFO : topic #41 (0.010): 0.055*look + 0.018*look_like + 0.016*hair + 0.014*picture + 0.013*girl + 0.012*love + 0.012*think + 0.011*color + 0.011*face + 0.011*see

2017-10-03 09:54:48,400 : INFO : topic #82 (0.010): 0.363*xxx + 0.083*alien + 0.035*watson + 0.030*xpost + 0.021*comment + 0.019*emma + 0.018*wwe + 0.015*child + 0.015*ufo + 0.014*blacklist

2017-10-03 09:54:48,404 : INFO : topic #44 (0.010): 0.098*design + 0.091*print + 0.085*3d + 0.066*model + 0.037*printer + 0.027*printing + 0.026*package + 0.025*wii + 0.025*serial + 0.021*rate

> the top words for a topic make much more sense.
