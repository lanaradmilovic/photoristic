# Batch 5 findings: Reddit threads on culling, AI culling tools, outsourcing, second shooters

Source: `batches/batch5.txt` (6,390 lines, 28 threads, all read in full).
Notes on reading this file:
- Quotes are verbatim with only obvious OCR errors fixed ("Al" -> "AI", "101" -> "lol", "0k" -> "ok"). Where OCR is doubtful it is marked `[unclear OCR]`.
- Upvote counts are almost never legible in this batch's OCR, so they are given only where they could be read; absence of a count means "not legible", not "zero".
- Ages are as shown on the screenshot (relative to capture date, roughly late 2026).
- "File" is the screenshot name as it appears in the batch header.

Threads with nothing relevant (3):
- `35 - Lightroom Preset Are you able to get same look as the advertised by original sel.png` (r/WeddingPhotography, 7y): preset/white-balance talk only.
- `38 - Photographers shooting luxury weddings How did you get there r WeddingPhotograph.png` (r/WeddingPhotography, 1y): marketing/planner talk only. One side note: user No-Dig-6580 posts generic "workflow optimization" advice ending in "I've shared some resources on my profile" - reads like disguised self-promotion, names no tool.
- `39 - New wedding photographer help r WeddingPhotography.png` (r/WeddingPhotography, 3y): business/insurance advice only (one line: "the culling & editing will be a big jump up in time requirement").

Relevant threads: 25 (some only marginally; marked as such).

---

## 1. "Može li netko preporučiti dobar softver za selekciju?" (Can anyone recommend good culling software?)
r/WeddingPhotography, 5y ago. File: `33 - Može li netko preporučiti dobar softver za selekciju r WeddingPhotography.png`
Note: the screenshot is Reddit's Croatian auto-translation of an English thread. Quotes below are my English back-translations of the Croatian OCR, so treat wording as approximate, not verbatim English.

**Aftershoot - stability complaint (OP, wedding photographer)**
- u/Eebtek (OP): [translated] "I also tried Aftershoot, but not once did it successfully process ALL my photos without freezing or getting stuck in the middle of the process."
- OP on manual pain: [translated] "It is so time-consuming when you have more than 1000 photos and every raw image takes 3 seconds to load..."
- OP on Photo Mechanic: [translated] "I heard about Photo Mechanic, but it seems it doesn't do the selection for you, it just loads photos faster?"
- the-dagger (identifies himself as Aftershoot's creator): [translated] "Hey u/Eebtek, AfterShoot creator here! Can you contact support, we can check what is happening and help you solve it." -> vendor reply.

**Aftershoot - praise (short, unqualified)**
- [username not legible]: [translated] "Aftershoot will pick for you. I highly recommend it."
- calitmvee: [translated] "I love Aftershoot!"

**Photo Mechanic - dominant recommendation (manual, speed, control)**
- rainontent: [translated] "I use PhotoMechanic. It is manual, but I like being in control and everything loads almost instantly. It literally halved my culling time since I started using it."
- Boganphoto: [translated] "For weddings or sports where I shoot hundreds, if not several thousand frames, the speed for deleting and selecting is great."
- evanrphoto: [translated] "PhotoMechanic has been the standard for a while."
- toin9898: [translated] "PhotoMechanic. You can go so fast that your brain switches to autopilot."
- derno: [translated] "We use Photo Mechanic, it's much faster than Lightroom. We pick manually and just assign colours to the photos we want to keep..."
- Also plain votes from Lightromance, Wdt2000, JulieGrenn-style one-liners ("Another vote for PhotoMechanic").

**Other tools named**
- kitkatKP: "Narrative Select!"
- trevrodriguez: [translated] "Check out Narrative Select. A fairly new culling app, but it has some good analysis tools that will sort based on subject focus, whether the subject has open eyes, and can rate images on various factors to speed up selection. Try the free trial..."
- Daren_Z (prefers Lightroom): [translated] "Lightroom. If you turn on caps lock it automatically advances to the next photo when you press P (pick), U (unflag) or X (reject)... For me it is far better than using an external program like Photo Mechanic."
- FiveInchFails: [translated] "FastRawViewer. It's perfect. $25 perpetual licence after a 30-day free trial."
- Bridge (apageofthedarkhold, northerntouch: "let the photos load and make a coffee"), IrfanView (theBaron01), XnView MP free (Yankeefan801).
- Hardware advice: KeepYourPresets / jakezaruba - don't work off an external HDD, use SSD.

**Indie tool self-promotion**
- roccon79 (8mo ago, newly married, built a tool): [translated] "After my wedding we had ~4k photos to sort, so I built a small tool to speed up the selection process. It runs locally in the browser and is open source." (snapsortr.com) -> self-promotion of a small local/open-source tool; note "runs locally" is used as a selling point.

---

## 2. "Outsourcing Editing"
r/WeddingPhotography, 3y ago. File: `33 - Outsourcing Editing r WeddingPhotography.png`

**Prices: human editing vs AI (hard numbers)**
- waimearock: "I used to pay .10 an image but I have been using AI editing lately. (Aftershoot pro)"
- Werdnamik: "Going rate is still around .10/image"
- passthetreesplease: "Imagen charges .05/photo (cropping and straightening are each one cent more). However, spot healing, teeth whitening, etc. aren't included. It's very fast and you're able to edit using another photographer's 'style' as well. Aftershoot will prob pose some strong competition as well now that it offers unlimited AI-assisted editing for $499/year and learns your editing style after a few thousand images have been uploaded."
- goodmanphotog: "Use an AI service! I used to outsource at .25/per photo and more, but now I use Imagen and the AI has 1000 photos done and delivered in 10 mins!"
- Relevance: AI is displacing human editors on price; note "learns your editing style after a few thousand images have been uploaded" = training/profile requirement + upload.

---

## 3. "What percentage of your second shooter's shots do you use? How do you determine which ones to deliver?"
r/WeddingPhotography, 10y ago. File: `33 - What percentage of your second shooter's shots do you use How do you determine w.png`

**Multi-photographer: everyone merges into one chronological story**
- evanrphoto: "I put all of the photos together in one pot and cull through them independent of photographer. I simply choose the best to tell the story. Sometimes even I forget who took a certain photo, but that shouldn't matter at all. The couple shouldn't see the delineation."
- [deleted]: "My goal is for my couples to not be able to tell who took what... So I mix them in sequentially. When culling, I choose the good photos that aren't duplicates of mine. Depending on the shooter or the day, the amount I use varies pretty wildly."
- [deleted]: "You can sync your images by time stamp and then just edit them all in a row."
- rmric0: "They all kind of go into one big pot for me on import and then I start to hack things down as quickly as I can, so it tends to be blind toward who took it... you don't need three variations of a shot on some guests... my end goal is for the client not to be able to see any differences."
- koronadal: "The final delivered images are sequential to tell the story of the day. The photographer isn't important, it's all about the images shown."

**Client-side pain when photographers are NOT merged (OP speaking as a bride)**
- weallstartatzero (OP): "My photographer for my own wedding had 3 shooters, and her delivered thumb drive showcased them all separately. I felt it just made me look for differences if that makes sense. It also was a little annoying to be going through one part of our day and then when it's over, re start again. It would have been nice to see the story as it happened."

**Hard numbers: share of second shooter's photos in delivery**
- koronadal: "about 30%-40% is used" with a regular partner ("almost half the photos I deliver have to come from my secondary"); with an unfamiliar second "I'm using only 10%-20% of the secondary's photos."
- ChadEEEE: "I look at a second as insurance. I cull and edit mine first then fill in gaps and pull in excellent shots. Probably 10-20% of the final might be my second's."
- koronadal also gives a detailed primary/secondary coverage split (speeches: "Primary on Couple and wide shots, Secondary on Speaker and guest reactions"; first dance: "Primary taking experimental creative shots, Secondary shooting safe standard shots") - i.e. two cameras cover the same moment from different angles, so cross-camera duplicates of a moment are the norm.

---

## 4. "How does this happen???" (photographer who failed 50+ / later 217 clients) - marginal
r/WeddingPhotography, 10mo ago. File: `34 - How does this happen r WeddingPhotography.png`

Mostly about a business collapse; useful only as context for post-production backlog as a business risk.
- evanrphoto: "Then that 'big' season hits and people get completely overwhelmed when the amount of prep and post work hits all at one time in that season."
- Longjumping-Rush-219: "I've learned that culling the same day or the day after works best for me. Once everything is in Lightroom and I've applied my starter preset, it's much easier to finish within a few days."
- DevineBossLady: "50 weddings, unless you have a huge team, is a recipe for disaster."
- shemp33 (friend's case): "his editing and delivery fell further and further behind - bad enough that some brides took him to small claims court... the judge ordered him to either outsource the editing or issue refunds."
- devonjonesphoto: "And here I am thinking I'm the devil when I'm just a week over my guaranteed delivery time."
- Numbers: 50+ brides in the news story; later "over 160 complaints", AG lawsuit "defrauding up to $750k"; "217 clients".

---

## 5. "Need second opinion on AI Photo Culling Software"
r/AskPhotography, 4y ago. File: `34 - Need second opinion on AI Photo Culling Software r AskPhotography.png`

**Aftershoot - the key critical quote (full-time wedding pro, evanrphoto)**
- evanrphoto: "In wedding photography it is more commonly being used these days. Although AfterShoot seems to be the leader. I have been using it for a while and honestly it isn't a massive time save for me with wedding photography. I didn't have many out of focus images and often closed eyes is intended (a tender hug for example). And the AI doesn't pick up what I look for in action shots. And even in static group photos it misses some of the groupings by deeming different grouping as identical. I basically have to review everything that was culled and also review a lot of what was culled out."
- evanrphoto: "I have much more success with the AI editing (Aftershoot)."

**Aftershoot - praise**
- electrikgypsyl: "I've tested most of them and had the most success with Aftershoot. It takes some tweaking and getting used to a slightly different workflow, but it's definitely a time saver for me!"

**FilterPixel - praise that another user flags as spam**
- Dangerous-Box-9929: "I started using filterpixel 2 months back and it really is so helpful... I culled 3400 images in 15 minutes... The only problem is I also shoot wildlife and it is not so good with culling those, but overall a good one to cull wedding & portraits."
- Open_Jackfruit_7813: "The AI was able to figure out intentionally closed eyes for me. It is still 90% accurate, but that's enough for me to save 5-6 hours of manual effort... It tags out of focus & blinks as rejects. Then I press Autoselect to select one best shot from similar photos. Finally, I do a quick review of chosen images and click export to Lightroom."
- Mercuti0999: "Filterpixel seem to have a lot of accounts posting spam, on this and other culling posts." (SeekTheLightPhotos: "good looking out. appreciate that.") -> treat the two FilterPixel comments above as likely vendor promotion; note the vendor itself markets "intentionally closed eyes" detection and a 90% accuracy figure.

---

## 6. "Remote culling/sharing large folders"
r/WeddingPhotography, 1y ago. File: `34 - Remote culling sharing large folders r WeddingPhotography.png`

**Pain of getting files to a remote culler (upload/cloud friction)**
- ladynomingtonn (OP): "I have someone remote who helps me cull. In the past we have made iCloud work, but with some of these bigger weddings/events (and with a new camera w/ bigger files) it's just not reasonable anymore... 100% of the time the browser version does not upload all of the files... Making it incredibly frustrating."
- OP: "My solution for the time being is to create LR catalogs with smart previews, but I'm aware that LR culling is awful compared to photomechanic." / "I've used Dropbox in years past, but it also sucked."
- pwar02 suggests a NAS: "basically acting as your own cloud storage except everything stays on your hard drives."

**Aftershoot - qualified praise, needs training**
- sarahg999: "Recently though I have started using aftershoot AI for culling and editing and it's not bad once trained. (I do high volume, non wedding events)"
- sarahg999 on LR smart catalogs via Dropbox: "I like this method because it's cheap and when outsourcing via a LR catalog, I can easily check and alter the selections/editing that was done."

---

## 7. "Some thoughts on the keyboard shortcuts for flagging while culling"
r/Lightroom, 1y ago. File: `34 - Some thoughts on the keyboard shortcuts for flagging while culling r Lightroom.png`

**Manual culling in Lightroom: ergonomics complaints and workarounds**
- Edg-R (OP): "This is especially useful when culling massive galleries with thousands of photos and you need to work quickly." / "It would be cool if Adobe improved the keyboard shortcuts for culling to improve efficiency and so that we don't have to rely on third party tools to do the job." (He remaps keys on a programmable keyboard.)
- joergonix: "it's not great ergonomically and kind of slow... So my personal preferred method is right hand on my mouse scrolling and left hand rating 1-5. Using this method I can cull a 6000 image wedding in about an hour maybe a bit less if I am very focused."
- sublimeinator: "I bought a 9 key programmable keypad for this exact reason."
- Edg-R: "You don't go back and forth to compare 2+ similar photos before picking one?" -> comparing near-duplicates is the slow part.
- nac_nabuc on hide-as-you-flag filter: "This only works if you are 100% accurate with your first assessment, otherwise if you want to revisit a flagging choice it's a waste of time."

---

## 8. "How long does it take you to edit a wedding?"
r/WeddingPhotography, 4y ago. File: `35 - How long does it take you to edit a wedding r WeddingPhotography.png`

**Culling is a large, separate time block (hard numbers)**
- azionix: "Culling takes most of my time. Once I narrow it down between 600-700, if I'm really into it, yeah 4 hours."
- [deleted]: "It would take me 4 hours to cull!"
- nuttychichi: "It takes me like 4 hours just to cull LOL. To edit a typical 8-hour wedding day takes me 10-15 hours."
- pb_and_banana_toast: "This is time for editing only. I don't know anyone who can turn a wedding around in the time that includes culling."
- mouettefluo: "Just uploading and culling is a few hours. I go from 3k pictures to 4-500."
- chickthatclicks: "It takes me 1 hour to cull 2000 photos. So a two shooter wedding might take me 2.5 hours to cull (5000 images). After the cull, maybe 3 hours to edit."
- EttVenter: "I get the culling done in an hour or so (no second shooter, and I don't shoot a ton on the day either - 1500-2000 shots)."
- mehraaza: "10 hour shoot, 3400 frames in lightroom. 1,5 hour culling, 2 hours batch editing... 3 hours detail editing... Delivery will be approx 330 photos."
- mrcow20: "I'd estimate 12-20 hours per wedding. For context there are two shooters with 2000+ shots including plenty of candids etc."
- Brattshandles: "I take [3]-4k (with a second) and deliver 800-1200. I take about 8 hours to cull, and try to keep it to 32 hours for edits" [first number unclear OCR: "0-4k"].
- JoelBoily (husband-and-wife team): "we typically shoot 6000-9000 RAWS at any given wedding and deliver 700-1200 final images. Here is our workflow breakdown: 1 Hour - Upload, run through Aftershoot for rough Cull and create LR catalogue. 1 Hour - select, edit and share Sneak Peeks. 3-6 Hours - Final Cull. 8-12 Hours - Edit all colour and Export..." and "our actual turnaround time ends up being 3-4 weeks". -> Even with Aftershoot, a two-shooter team still spends 3-6 hours on a manual "final cull".
- waimearock: "I cull down from 3-6k down to 500-2000 in about 60-90 mins then edit about 500 per hour after that."
- niresangwa: "usual delivery is 700/800, between me and the 2nd, there's usually around 1500 off the cards... I use Photomechanic to cull" and delivers next day.
- missdanal105: "I'm slow to cull (2 hours minimum)."
- floobenstoobs: "Including culling, it takes me about 12 hours to edit 800ish photos."
- X4dow: "30-40 hours. Including getting distracted with Reddit...YouTube..etc"; Shutter-Shock: "around 30 hours divided between 6-7 days"; Angy-jy: "30 hours for 600 images"; Filmandnature93: "minimum of 4 full working days... I deliver between 800-1200 images."
- [deleted]: "it all depends, generally I have a 3 month turnaround on a wedding album." / another [deleted]: "I always say 4-6 weeks and usually try my best to do it in 4."
- k_fine_bye: "Culling takes the longest then WB".

**Aftershoot - praise**
- Joris818: "I used to spend at least 2 hours on culling but I recently started using Aftershoot and I'm really glad I did!"

**Imagen - mentioned for editing head start**
- pb_and_banana_toast: "I know a few photographers who turn around a wedding in 3-4. This is done by using something like ImagenAI to give you a head start..."

**Why culling is slow / emotional (artistic-control argument)**
- [deleted]: "I have to basically reimmerse myself in the day each time I cull...so it takes time. And I let it. Why would I disserve my clients that?"
- supercali5: "Use Photo Mechanic to Edit. Be brutal and fast. Don't second guess yourself." / "Edit your wedding from back to front. Your last images in a series are almost always your best."

---

## 9. "Trouble with clients sending me the selected pics" - marginal
r/WeddingPhotography, 2y ago. File: `35 - Trouble with clients sending me the selected pics. r WeddingPhotography.png`

Culling is seen as the photographer's core expertise, not something to hand to clients (relevant to "who decides").
- NebulousCeiling: "Consider yourself the expert when it comes to culling/selecting. Not the client... Clients are not good at this... It is also very time consuming and overwhelming to them to have to make those choices... that's why we get paid the big bucks."
- josephallenkeys: "Having the client see all of the images gives an option paralysis and also shows all of your misses or otherwise unflattering outtakes. You provide a service by making these decisions for them."
- Letywolf: "...you get an email or a drive with 3500 photos you have to sort through and select the best... This is insane!"
- PanicSwtchd: "You shouldn't be using AI for ordering images...it's not going to be a consistent and repeatable process." (OP had used ChatGPT to sort file names.) Also: "I will group the photos based on the 'locations' that were in the wedding while simultaneously culling and rating the shots".
- minaret_photo: "You're outsourcing culling to your clients. This is just next-level productivity!"

---

## 10. "What is your editing workflow?"
r/WeddingPhotography, ~1y ago. File: `35 - What is your editing workflow r WeddingPhotography.png`

**Astroturfing fatigue (OP's own header)**
- hillsong1 (OP): "NB! Please AI company affiliates don't reply here. It is more helpful for the community if only real photographers answer."
- OP numbers: "I can edit a wedding in a day and a half, but usually it goes up to 4-5 days (for 700-800 images for 9-10hrs wedding)." Workflow starts with "Cull 1st pass - Cull 2nd pass - Import into lightroom".

**Multi-camera time sync - explicit manual workaround**
- disgruntledempanada: "I shoot on two cameras (A7iii and A7Cii). When I'm getting the cameras out for the day or putting the cameras away for the night I take a synchronized photo on each so that I can sync up the timing of the shots and keep things in chronological order (I select all the A7iii images and sync them to the A7Cii's first or last shot time in Lightroom Classic)."
- Same user on culling: "Culling I'm brutal with. I take between 2 and 5k photos on a wedding weekend... I get mad at the photographer as the editor. We're separate people and we hate each other."
- Same user, why he culls on graded previews: "Shots that don't stand out to me sooc look much better graded and they get included vs. culled."

**Aftershoot - used as first pass, then manual second pass**
- Nikbryantphoto: "Cull 1st pass in Aftershoot, 2nd pass of the cull manually in Aftershoot, Run aftershoot edits, import into lightroom, slight adjustments and final tweaks..."
- Morgdort (culls manually, uses Aftershoot only for editing): "I just do one cull, one finger on 5 for keepers... Then I send it through aftershoot (trained on my stuff)..."

**Imagen - positive on culling time**
- [deleted]: "I've culled manually in LR but recently tried ImagineAI [Imagen AI] and it seemed to cut the culling time significantly. However, knowing how to do it in LR would be great (and preferable)."

**Narrative Select - praise for face panel**
- Limit760: "I cull in Narrative Select. Incredible for the faces panel which makes family formals much more enjoyable." [OCR garbled but readable]

**FilterPixel - used for editing, not culling**
- egoldenmoments: "After I cull, I do the first round of edits with filterpixel..."

**Outsourcing cull + edit**
- redrabbit1977: "Import to Lightroom, export to Dropbox, place order with editing lab, go surfing. Download a week later culled & edited."

**Photo Mechanic / Lightroom / FastRawViewer - manual tools**
- josephallenkeys: "Photo Mechanic got recommended so often I tried it out and was shocked to find an unintuitive Windows 95 program with infuriating shortcuts. Yeah, it's fast to show a preview but as an extra step, it slowed me down."
- CommercialShip810: "when you use embedded previews the culling and previewing is instantaneous. Seems like a wasted step and another bit of software to add into the mix."
- [username not legible]: "...especially when it comes to client work where they might be nervous to change up any aspect of their file management for fear of something going missing etc." (why people do not switch tools)
- aygross: "I have never found anyone who has tried frv [FastRawViewer] go back to using Lr."
- Upsidedown0310: "I hate culling so I HAVE to be forced to do it straight away otherwise I procrastinate and put it off for ages!"
- rmric0 workflow includes "Break events into scenes for bulk edits/adjustments" - OP asks "How do you break everything into scenes?" (unanswered in screenshot) -> unmet need: automatic scene/moment segmentation.

---

## 11. "How do you cull?"
r/photography, 7mo ago. File: `36 - How do you cull r photography.png`

**The pain, in the OP's words**
- OP: "You come back from a shoot with 2000 shots of birds, or your kids, or randos at somebody's wedding. Culling them is soul-destroying. How do you do it?"

**Manual methods (no AI tool is recommended anywhere in the visible comments)**
- TeamHuman (top comment, ~178 upvotes): "I use lightroom and do multiple passes... First round: Any usable photo is ranked 1 star. Second round: Select the best images from sets of good photos (for example, multiple of the same group shot. select the best) rank 2 star. Third round: ...select the best of the best".
- 100Kinthebank: "I'll end up with 10% keeper rate on average"; and why he refuses auto-advance: "I like being able to look back especially if it's a burst of my daughter and trying to decide on one frame vs another".
- AndrewThomasPhoto (motorsports pro): "as a motorsports shooter who has culled as many as 30K images from a 24-hour endurance race, I use Photo Mechanic to do my culling... I never trash an image, they all go on my NAS".
- trying_to_adult_here: "Another for Photo Mechanic here. It's much, much faster than Lightroom when you're culling. My only gripe is that it's not great for finding fine focus..."
- Relative_Escape (wedding pro): "One summer when I was shooting 35-40 weddings I made a rule that if I finished my first cull by noon the day after the shoot, I would give myself a $26 shopping spree on Amazon... I edit IN (tagging only keepers) and use Photo Mechanic."
- rmric0 (wedding): "1. Come back from a wedding exhausted, begin uploading photos... 3. have an existential crisis 4. fast pass, flag passes and reject duds..." five passes; "Typically this is a day or two."
- LisaandNeil (wedding duo): "We cull around 300Gb of shots, often two or more times a week... We use Bridge... 'Cull in' rather than 'cull out'. A keeper should be screamingly obvious".
- NotJebediahKerman: "2000 photos might take 30m".

**Never delete / fear of losing a shot**
- bdgbill: "I keep everything... Keeping everything has paid off for me. Sometimes, boring photos become interesting with time."
- LeicaM6guy: "Nothing gets deleted. Everything gets a triple save: RAID drive, SSD and cloud. Never know when a shot will be useful".
- RedGreenBaluga: "why not have a cull drive?... It's there if you want it but it isn't cluttering your working drives."
- Sidebar evidence of indie tools: related post "I built a free photo-culling tool with Claude - it takes 8,000 trip..." (r/ClaudeAI, 6mo).

---

## 12. "Outsource editing"
r/WeddingPhotography, 2y ago. File: `36 - Outsource editing r WeddingPhotography.png`

**Outsourcing services named and priced**
- evanrphoto: "Raw Digital, FotoFafa, or The Image Salon are well regarded human editors."
- redrabbit1977: "Wildernis lab for me. Others are freedom edits, raw digital, image salon."
- annopano: "I've tried Freedom Edits about 2-3 years ago? It worked out to be roughly 30-40 cents per image edited... Not using it anymore though."
- fotisdragon: "Take a look at The Image Architects too, they do both culling and editing with quick turnaround times!"
- [deleted]: "Just remember to bake outsourcing editing into your pricing".

**Aftershoot - praise, and resale of an Aftershoot profile as a service**
- az_desert_rat: "Aftershoot is a lifesaver."
- Max_Sandpit: "I'll run weddings thru my Aftershoot profile for $100/wedding. Unlimited images. Culling and corrections included." -> a photographer reselling per-wedding access; shows demand for per-wedding pricing rather than a yearly subscription.

**Unmet need: express turnaround**
- maxmaxw (OP): "I was once asked to present my work to the guests on the brunch the morning after. I declined... is there any company that does 'express editing'?"
- Happy-Strawberry-748: "I run a bespoke non AI editing service..." -> vendor self-promotion; "non AI" used as a selling point.

---

## 13. "Photo Culling Process Tips"
r/photography, 1y ago. File: `36 - Photo Culling Process Tips r photography.png`

**Lightroom Assisted Culling - underwhelming**
- cbunn81: "There are some AI culling tools out there. They're not cheap, and reviews seem to be mixed. I use Lightroom, which just recently got some AI culling features in beta. They're pretty underwhelming. They can do okay with working out which are obviously out of focus or have closed eyes of the subject. But those are also the cases that are easiest to cull manually."
- Sinandomeng: "Lightroom recently introduced assisted culling. It's still very basic. Try it out"

**AI rejects photos the user still wanted (unnamed tool)**
- Dioxybenzone: "There is one, I'll try and find it. It culls the stuff that's out of focus immediately. I stopped using it because sometimes I still liked the photos lol"

**Narrative Select - liked, but cost objection; user builds own app**
- itsmii: "I tried a few different solutions on a Mac (Adobe Bridge and Narrative Select) but wasn't really happy with the ongoing costs (as much as I loved the close up panel in NarrativeSelect). Over the last couple of months in my spare time I've been trying to build my own app for culling".
- itsmii on his design: "The goal... is to not necessarily let AI rate images initially (although I have just implemented a feature I am testing that suggests the best photo out of a group of images that seem to be visually similar), but to help speed up the initial pass... it can show me close up views of each person's face with visual indicators".

**Demand for AI first pass (hobbyist OP)**
- Grouchy-Culture-4062 (OP, amateur): "as I'm shooting a lot of series like my boy jumping on a bike, it should be piece of cake for an AI/ML tool to select the one with good composition, focus, visible eyes etc. and suggest it for keeping." / "Now what I'd like to have is AI that gives the first one or two stars!"

**Photo Mechanic - "gold standard" for manual**
- qogudwls: "The gold standard is photo mechanic, you can cull/tag/rate/ whatever your heart desires as fast as you can click with full raw files... I can cull a full baseball game in 20 minutes or so."
- qogudwls: "if you have multiple photos and they are all usable but you cannot figure out which to keep, the differences are so minute it doesn't matter."
- SaltyPatriot76: "Photo mechanic, worth the money"; Illinigradman: "Crazy fast".

**Psychology of rejecting**
- LightPhotographer: "Every photo you throw away causes a little sense of loss. After 100 your will to live is gone. Instead grab the winners."
- FloridaManZeroPlan: "Months later I'll go back and look at the ones I only flagged and there's likely a few hidden gems I missed the first time."

**Possible promotion**
- ichuy18u: "I've used photomind.online to cherry-pick photos from my sports competition albums and it worked surprisingly well. I definitely recommend it" -> single-purpose recommendation with URL; possibly promotional.

---

## 14. "Processing your wedding images - workflow survey"
r/WeddingPhotography, 10y ago. File: `36 - Processing your wedding images -- workflow survey r WeddingPhotography.png`

Pre-AI baseline; shows that volumes and pain points are a decade old.

**Hard numbers**
- napster73 (OP): "usually end up with about 1500-2000 pics for a normal 8 hour wedding" / "The set I deliver is usually 30% of the shots. So with 1500 pics shot, I end up with 500 pics spending say 2 minutes each or so which works out to 15-20 hours."
- OP on emotion: "I do my culling over a couple of days since I am too emotionally attached to almost every shot, but do I really need 10 of the bride's dad's speech?"
- PhotoTableau: "I usually shoot about 3000-5000 images at a wedding... From there I'm usually left with about 1000-1500 photos that I get down to 800-1200... The whole process usually takes about 6-8 hours".
- [deleted] (employed editor for a wedding photographer): "I'm given ~4,500 images on average per job (ugh). I start in photo mechanic. It's such an overwhelming amount of images that first I go through and star with a 1 anything that's worth keeping. Usually get down to around 2,000-2,500 images. Then I go through again and star with a 2 for the images I am going to edit and deliver. This ends up being 600-800 images." / "That whole process (aside from exporting) takes me anywhere from 6-8 hours. I've been doing ~50 weddings and portraits a year for almost 4 years".

**Second shooter handling / outsourcing cull**
- chrishartphoto: "At the wedding/right after, I download my second shooter's files onto my surface by importing into LR, then usually throw my card in too." If busy: "upload smart previews and the .lrcat file to a dropbox and send RDFL an e-mail, then I get my photos edited and back two weeks later! I have them cull, color correct, straighten, exposure correct and pick a group of the best".
- cltmn: "Pick two teasers, one each of us took." / "We try and break the wedding into as many chapters as possible. Edit a chapter in each sitting."
- elsee28: culls twice "especially if there are small children in formals - I'll cull the first time for any shot that has everyone looking, eyes open, etc. and then again to narrow down my fav." Delivers "sorted by time".

**Safety habits (never lose a file)**
- ToTouchAnEmu: "after I've delivered the photos and given the client enough time to request a photo I may have missed (usually a month or two), I go back and select all of the unflagged photos and delete them".
- elsee28: "Cards go in a card holder in my purse until wedding is fully online. If my house burns down while I'm at Target, at least I've got the cards on me."
- Danivan: "Night of wedding import to lightroom with my own import preset, render smart previews, cry, go to bed."

**Photo Mechanic vs Lightroom**
- napster73: "I used to cull in LR but that is just too slow." / "Clicking 'next' to see the next pictures takes a few seconds for me while LR shows 'Loading'... In PM it's instantaneous".

---

## 15. "Are AI culling tools worth it?"
r/AskPhotography, 4y ago. File: `37 - Are Ai culling tools worth it r AskPhotography.png`

The strongest thread in this batch for the "never lose a good photo" argument.

**Aftershoot - "risk and little to no value" for weddings (full-time wedding pro)**
- evanrphoto: "Full time wedding photographer. AI culling is only marginally productive if at all. I use AfterShoot for some shoots where it provides some value, but with weddings for me it provides risk and little to no value. It 'selects' about 40% of the images and I need to review both the culled-in and culled-out images. It groups like photos and chooses the 'best ones', but I am not impressed by its decision making here. It primarily culls out out of focus images (which I barely have these days) and closed eye photos (which are sometimes the emotional ones which are the most important). AI editing on the other hand is a great tool and time saver."
- evanrphoto on how pros actually cull: "generally you 'cull in' not 'cull out'. So you are selecting the photos that are unique and represent the best moments of each burst. After many years of doing this I personally try to be over inclusive and don't agree with 'less is more' when you are covering such a complex event with so many people, emotions, moments, and details."

**Refusing AI: fear of a missed good photo**
- One_Chart7921 (event/corporate shooter): "Personally I don't trust AI to cull my photos for me. I go through them all manually. It takes time, but I can't risk a good photo being missed on the whims of an AI." He rates in camera instead.
- TinfoilCamera: "If you do not look at each image yourself then you will never spot the 'imperfectly awesome' shots that sometimes happen... where you totally screw something up and that screwup makes the image rather than breaking it. The 'A.I.' stuff can help you sort wheat from chaff, but you're still gonna have to actually look at the images yourself."
- sjmheron: "If you want to nix the blurry shots, OK. It won't make sure you have a picture of Uncle Steve without his finger in his nose." / "With practice you can rank 1k images in 3 categories in less than 10 minutes in PhotoMechanic."

**Too strict on focus; user wants to keep slightly blurred special moments**
- Aloket (tool name unclear in OCR, used on a performance shoot): "it doesn't remove anything, it just adds a color label or stars. It is pretty strict regarding focus, so I just went back over them (easier than going through all of them)." Also: "it does choose a certain percentage of images it considers to be the best ones, which can be helpful".
- luka_anders (OP, ~3k-picture wedding to cull): "That honestly sounds like I'd not have much use for it. The color and stars part is fine, but I'd like to keep slightly blurred photos as well. Most often I can either fix them, or I end up delivering them anyways if the moment is special."
- OP's actual need: "I'm mainly looking to get the best one out of each series. If it ends up being slightly blurry it's alright... But I really want to cull through all those near duplicates fast." and "I'd prefer if it runs as LR plug-in."
- OP after reading replies: "I suppose I have to do the culling manually."

**Numbers:** OP has a ~3k-picture wedding and expects "another 4-5k pictures" at a graduation party; One_Chart7921 "2000-3000 photos easily. For one wedding I even ended up shooting 5000+".

---

## 16. "HELP! 2nd Shooter shot in JPEG" - marginal (second-shooter economics and risk)
r/WeddingPhotography, 4y ago. File: `37 - HELP! 2nd Shooter shot in JPEG r WeddingPhotography.png`

- OP adamhyme108: second shooter "was paid $600 for 5 hours and she handed me the memory card so I could edit them. I upload them, and she shot ALL IN JPEG". Lead photographer receives the second's cards and does all the post work; mixed RAW/JPEG input from the second camera is a real-world case.
- pasbair1917: "Second shooters in the US get paid as little as $15/wedding day shoot hour - mostly around $20-30 per shoot hour." About an associate-shooter company: "their post processing system required culling images and their upload system was so slow and convoluted, it would take days to post process the wedding."
- [deleted]: "in NYC/NJ, I pay lead photographers $70 per hour, and if they shoot as second, they get $60"; another: "Most primary shooters... after adding in editing time and overhead, take home about 35-60 an hour."
- [deleted]: "Some large volume studios like The George Street ask photographers to shoot in jpeg."
- SasquatchGroomer: "I'd be handing that disk to my sister and saying 'here are your other photographer's photos.'" / Drix22: "For sure keep the images separate and clearly labeled." (minority view; most merge).

---

## 17. "Hey, it's Fotofafa. AMA about color correction, outsourcing your editing..." (vendor AMA)
r/WeddingPhotography, 12y ago. File: `37 - Hey, it's Fotofafa. AMA about color correction, outsourcing your editing, and ho.png`
Speaker fotofafa = vendor employee ("David from Fotofafa"). Mods' disclaimer: "The mods of r/WeddingPhotography do not endorse any product or vendor and do not receive any compensation for vendor AMA's."

**Outsourcing price points (historic baseline)**
- fotofafa: "Our color correction is $.35/image." / "Culling is $.09 per image submitted (in your case, 2000 or 3000)." -> $180-270 to cull one wedding of 2,000-3,000 frames.
- fotofafa: "the rest of the color correction is usually completed in 5-7 business days."
- fotofafa: "We see a huge spread - sometimes 200, sometimes 1200. However I'd say about 80% of the weddings we see are in the 600-800 range." (photos selected for edit per wedding)
- fotofafa: "we processed just under 200,000 images last month"; editors do "sometimes as much as 2500 images a day"; "edited for over a thousand photographers worldwide".
- fotofafa: "Most of our clients like to do the culling themselves, but some have us do it." -> even with outsourcing, photographers keep the cull.
- MarblesAreDelicious (wedding photographer): "end up shooting between 2000 to 3000 photos for the entirety of a wedding day".
- itskayguys: "For ~1k images... I can probably cull them in an hour, maybe hour and a half. Corrections would take me another 2-3 hours at most."

**Customer praise**
- mattkoskela: "I've used Fotofafa on every wedding I've shot since early 2013 and will never shoot a wedding without using them again."
- evanrphoto: "It took me a long time to get comfortable with outsourcing. I am a bit of a perfectionist".

**Complaints / objections**
- ascottmccauley: "Why can't you just put your pricing on your website?"; [deleted]: "when you don't post your prices it makes me think... you're going to nickel-and-dime me to death with bullshit addons and fees."
- Upload/security: icydog: "Since FTP is an ancient protocol built before security was a concern, I prefer to avoid that for any purpose (especially transmitting usernames and passwords in clear text)." Vendor's answer: "Even if they were to be compromised, I'm not sure your RAW files or SmartPreviews have much value to anyone else." -> dismissive attitude to client-photo privacy.
- Profile set-up effort: "If this is your first order, it might take a revision or two before we've perfected your style".
- evanrphoto: "outsourcing used to be a big pain because of file delivery"; KipperTheCat: "Dropbox is usually extremely slow."

---

## 18. "How do you select your photos after returning from a trip?"
r/AskPhotography, 5mo ago. File: `37 - How do you select your photos after returning from a trip r AskPhotography.png`

**Lightroom Assisted Culling - still must double-check everything**
- Coryan: "Lightroom now has a feature called Assisted Culling which helps identify images that are out of focus or people's eyes are closed. It can help speed up the process. But be warned, it's not perfect, so look at those photos before removing them."
- 02911_Photography: "This feature makes me nervous, I assume it puts them all into its own bucket so you can make a pass at them to double check but doesn't that defeat the purpose?"
- Coryan: "Yes, you still make the final call about what gets removed. I had a nice bird shot that AI said was out of focus, it was wrong. So I still double check everything, but it goes quicker with this feature."

**Manual culling attitudes**
- C_sapidus (dance performances, "2-3,000 photos"): "Culling is the part I hate the most." / "I usually hang onto all my photos for a few months to make sure I don't need to go back and find one, then I'll permanently delete the x'ed ones."
- kali_tragus: "I never delete the raw files. Never."
- Comfortable_Tank1771: "life's too short to look at bad pictures again and again. So I delete mercilessly. Camera shake, misfocus, bad pose, closed eyes, duplicate, just not interesting - DELETE."
- Free tools named: DigiKam, NX Studio.

---

## 19. "Photographers who shoot 30+ weddings a year... HOW do you do it?!"
r/WeddingPhotography, 9y ago. File: `38 - Photographers who shoot 30+ weddings a year... HOW do do it ! r WeddingPhotograp.png`

**Culling stays with the photographer even when editing is outsourced**
- Meganlee (OP, 16 weddings in a 5-month season, already outsources editing): "I edit for the blog and slideshow, then cull... which I'll quickly admit takes me much more time than it should. Then I outsource the rest."
- andersphoto: "I do a little over 40 and if I get to 50 I will start outsourcing my editing, but I've been holding onto it. Isn't it the editing that makes your final image yours? I'm admittedly scared to give up the reins I guess."

**Culling speed numbers and method**
- IS064: "The one thing that increased my speed for culling was the idea of culling to add, not culling to remove... I now cull my weddings ([~3000] images down to around 600) in around an hour." [OCR shows "63000"; first digit unclear]
- electrikgypsyl: "I have gotten my culling down to about an hour and a half for just me and an 8 hour wedding... Between 2,000 and 4,000 [frames]." Sends to editor Tuesday, "get it back Thursday or Friday".
- arcterex (why bursts make culling slow): "I've had too many times when I miss 'the shot' with a blink or slightly bad timing or slightly missed focus that I generally end up taking 2-5 shots of almost everything. Because of this my culling isn't so much picking a shot from the list but picking which of the 2 or 5 shots is the 'best' one from that moment, so it's doubly long it feels like."
- Ularsing: "cull in reverse order. A lot of the time, you'll shoot until you get the shot you want."
- CrankyPhotographer: "If you have 600 images and you spend 10 seconds per image watching the little dots go in a circle, that's 6,000 seconds, or 100 minutes".
- JulieGrenn: "+1 for Photo Mechanic, I very much regret not buying it before this year. It's saved me so much time."

**Workload / backlog numbers**
- DawildWest: "during the busy season I regularly work 70+ hours per week."
- innsaei_vi: "Last October I had 9 weddings and I just caught up on that shit in June."
- pspetrini: "I'm at 23 per year... I can do everything related to shoot a wedding in eight days and that's down from 13 a year ago." / "I work faster if I pre-sort everything into folders and tackle each part of the day (Bridal Prep, ceremony, family formals, etc) as a separate assignment." -> manual moment/segment grouping as a speed-up.
- northerntouch: "47 weddings this year... don't see much about burnout, it can happen if you never come up for air."

---

## 20. "What software do you use for photo culling?"
r/AskPhotography, 7mo ago. File: `38 - What software do you use for photo culling r AskPhotography.png`

**Trust gap: Lightroom Assisted Culling and Aftershoot**
- lexiestudios: "Lightroom AI culling works okay for me, but it's not really 'set and forget.' AfterShoot looks promising but I haven't fully trusted it yet for client work. I still end up manually reviewing everything."
- OP: "I have used Adobe Lightroom's AI culling feature. It takes a while depending on the number of pictures but it is good. I have also been seeing a lot of ads about AfterShoot but I haven't used it before."

**AI tools not faster than doing it yourself**
- morningpeach: "Photo Mechanic, I have tried Imagen and Aftershoot but for me it's nearly as fast to do it myself and obviously gives me control over what I'm keeping."
- itchinginsomnia (indie developer of a free open-source sorter): "I actually built and use my own photo culling app for this exact thing. Got tired of Lightroom's culling being slow, and AfterShoot felt overkill for what I needed. It's just 1/2/3 keys / bad, maybe, good. I can rip through a thousand wedding photos in like 15 minutes... It's open source and free. No AI, no sliders, no bullshit. Just culling."

**Aftershoot - strongest positive, with numbers (also shows pricing lock-in)**
- SnooRegrets8767: "Aftershoot, but I'm also locked in at early pricing. As someone who 10 years ago was paying about $200 a wedding for just the basic culling service, this was a no brainer. Even if not 100% perfect, for it to get to 95% accurate for what I would pick in less than 10 minutes, for me to spend another 10-20 is still a win considering 10 years ago 2 hours was considered near impossible".

**Imagen - praise (two comments; both read promotional, unverified)**
- Longjumping-Bed-9528: "I used to use Photo mechanic. But since AI started doing the hard work, I switched to Imagen AI. Their culling tool is pretty trustworthy and I was more blown away by the editing tool. The app is more of a full workflow solution... Culling, editing with different AI tools and masks even delivery to client and posting to social media from one platform".
- AppointmentLucky3894: "I use Imagen Ai, highly recommend you give it a try. It has saved me a bunch of time"

**FilterPixel - praise with price (reads promotional, unverified)**
- Hefty_Jellyfish_8812: "I use FilterPixel, their new feature DeepCull helps me (wedding photographer) and my husband (sports photographer) at the same time. They call it genre aware... We pay around $40 every month. But what I love is the system scores every photo out of 10 and it is pretty bang on."

**Evoto**
- Ander_Sloost: "evoto is amazing" (no detail; possibly promotional).

**Cheap/manual alternatives people actually use**
- a_rogue_planet: "FastRAWviewer here... It's not free, but it is cheap and the license gives you updates forever." (KCHome: "yup, cheap, fast, efficient!")
- dkfotog / AndrewThomasPhoto: Photo Mechanic "my go to app for culling and a whole lot more. Lightroom and Photoshop for editing are great but way behind PM for culling".
- OldTiger3832: "people keep recommending Photo Mechanics to me at one photography workshop, and it's expensive for an amateur" (building his own).
- LiamoLuo: "I've still stuck with manual in Lightroom... Can usually sort a couple thousand pictures pretty quickly this way, and I still have my rejected ones if I want to review them again."
- Also: XnView MP, FastStone, IrfanView, Darktable, Capture One, DxO PhotoLab, Apple Photos smart albums.
- Sidebar: related post "Keeper - Fast Photo culling app (Aftershoot alternative)" (r/macapps, 10mo) and "Aftershoot is a waste of money." (r/WeddingPhotography, 1y, 95 upvotes, 156 comments) - titles only.

---

## 21. "What's New in the Massive Lightroom Update (LrC 16.0, Lr 10.0, Mobile/iPad 12.0)" (vendor post)
r/Lightroom, 4d ago. File: `38 - What's New in the Massive Lightroom Update (LrC 16.0, Lr 10.0, Mobile iPad 12.0).png`
Speaker terryleewhite = Adobe employee (flair). 308 upvotes, 314 comments.

**What Adobe is shipping for culling (competitive positioning)**
- terryleewhite: "Under-the-Hood Upgrades to Assisted Culling: Assisted Culling just got a major AI model refresh to make picking your best shots way more accurate. It's much better at scoring focus and judging true sharpness (especially when you're shooting wide open with a shallow depth of field). We also heavily upgraded face and eyes-open detection for smaller faces in the background, which makes a massive difference when you're culling large group shots, weddings, or events and don't want to spend hours comparing near-identical burst frames."
  -> Adobe is improving detection of small background faces' eyes, i.e. the opposite of "who matters in the frame": more background faces will be scored, not fewer.
- Also announced: "Survey View (Lr Desktop)... compare up to 100 similar frames side-by-side"; "Focus Points Overlay (LrC)"; "Import Filter (LrC)... filter your import grid by file type..., star ratings, locked/protected, and color labels that you set in-camera"; "Open Eyes (... Early Access)... Using another photo from the same shoot as a reference, Open Eyes replaces their closed eyes with open ones."

**User complaints in comments (Lightroom general)**
- KevinAndEarth: "All I care about is: Does LrC still run like crap on a massive workstation that I throw software development and video editing tasks at all day long with no problems?"
- tofuchrispy: "Tested the update on windows and sadly still performing worse than on mac m1 pro. 13600k RTX 5090 128gb ram. What the hell."
- [username garbled]: "it crashed on me once because it maxed my 32GB RAM."
- livetotell: "Would really appreciate some attention to the face recognition/tagging feature in LRC. It doesn't combine faces that are different instances of the exact same photo, it doesn't seem to sort suggestions on best match. It feels really behind the times right now."
- aparis99: "And I STILL can't natively search my catalog for 'dog' and it return me all the images with dogs.... Sheesh"
- ArcjoAllspark: "the Open Eyes feature isn't detecting their closed eyes, probably from the makeup."
- alllmossttherrre: Lightroom apps "refuse to let you customize the keyboard shortcuts."
- Positive: anonymous_panelist: "for the first time, I loved Lightroom UI and the features they added in this update."; several happy with Survey View and Glow.
- No commenter in the visible part discusses Assisted Culling accuracy after the refresh.

---

## 22. "Did you ever Outsource the editing of your photos?"
r/WeddingPhotography, 5y ago. File: `39 - Did you ever Outsource the editing of your photos r WeddingPhotography.png`

**Outsourcing: onboarding cost, mixed quality**
- evanrphoto: "I highly recommend FotoFafa and Raw Digital. Best tip I can give you is to accept the fact that there is a learning curve to the process and workflow... if you try to jump in when you are already slammed and don't have spare time then you are going to have a bad time guaranteed."
- evanrphoto on Image Salon: "My primary push away was driven by specific customer service disappointments".
- ras1304: "I've used Image Salon for years and had never had a problem. Outsourcing editing is the best decision I ever made... I have an assigned editor, it's been the same editor for me for the last 3 years."
- tylerc66: "IMO no one is going to edit the images with as much care as you would. I have tried 2 of these services [Image Salon and PhotographersEdit] and end up still editing the images." / "At the end of the day culling and editing is gruelling and I wish there was an easy way out."
- NikitaNinja: "Avoid Evolve"; nickthake: "Do not use shoot dot edit. worst experience ever".
- Inner_Audience (ShootDotEdit, detailed): "Received my galleries and the colors were off between my different cameras. Greens were two different greens." / "I get my first catalog back, and it is so flat and off... I had to re-edit the whole gallery." / "About to cancel my unlimited plan with them for a second time."
  -> also a multi-camera consistency complaint (colour mismatch between two bodies).
- OP lists nine competing outsourcing firms and says "there are a thousand companies!" -> crowded, undifferentiated market.

---

## 23. "How many photos do you edit per hour?"
r/Lightroom, 28d ago. File: `39 - How many photos do you edit per hour r Lightroom.png`

**Aftershoot - founder present, accused of astroturfing**
- Temporary-Mix8022: "Aftershoot never worked for me.. tried it for a year and it is terrible at white balance, tint and pretty much every parameter I ended doing by hand." (recommends Imagen or FotoLab instead)
- getluminarymedia: "I don't like Aftershoot. It doesn't do a good job IMO."
- the-dagger (Aftershoot founder): "Look at tools like Aftershoot. They can automate the bulk of the mundane tasks..." and later "If there's anything we can do better, all ears!"
- Temporary-Mix8022: "Open source it.. I'm so done with the astroturfing by that scam company. They deserve to have it name dropped every single time they AstroTurf as punishment. Even this is another astroturfing account of theirs. It isn't a real customer."
- the-dagger: "Bro I'm the founder of Aftershoot - check my Reddit profile. Idk why you have to hate on something so much".
- Mattman254: "Recently used Claude to completely clone Aftershoot, saved me $500p/y" ... "It's also running 4-5x as fast"; the-dagger warns about reverse-engineering Aftershoot's models ("those are our IP").
- Mattman254: "a lot of the photography sub reddits have banned talking about AI projects, leaves me little options to get it in people's hands and free from Aftershoot" -> go-to-market obstacle for any new AI tool on Reddit.
- Wartz (advice to indie AI-tool makers): "Do not freakin use AI to write your Reddit post... You do not need a massive AI generated website".
- XOMaddsPhoto (long, polished pro-Aftershoot comment; reads promotional, unverified): "I gave Lightroom's AI-assisted culling a shot, and it was okay! My biggest issue was that it didn't learn my personal culling preferences... I eventually landed on Aftershoot because it offered a flat annual fee rather than charging per image, and it could learn both my culling preferences and my editing style."

**Human editing prices (hard numbers)**
- XOMaddsPhoto: "my costs were regularly $400+ per wedding for galleries of around 600 images"; "roughly $0.50 per image".
- defeldus: "The going rate is like 20 cents an image for wedding stuff"; weetzie724 (private editor): "it is closer to .40/image" and "Aftershoot works for some, but there's still plenty of people who prefer a human!"
- aygross: "For weddings typical pricing is per image 35-50 cents and most editors are 1-200 images an hr."
- OP: friend quotes "$20 an hour... up to 30 pics an hour"; origionalroman paid "$50/hour"; Either_Awareness_772 charges "minimum $50/hr".
- MattChan1506: "i can edit and deliver a full wedding delivering 2000-3000 photos in less than 2 sittings about 7 hours each... if you shoot to a set of rules and standards and your shooters follow your same rules" (multi-shooter studio).

---

## 24. "Photo Editing/Culling Tips: How to cull photos quickly" (vendor-style research post)
r/AskPhotography, 5y ago. File: `39 - Photo Editing Culling Tips How to cull photos quickly r AskPhotography.png`
OP aayusharora113 writes "We have interviewed 2000 professional photographers for the past two years to learn about their editing & culling workflows... Please check our research here:" -> content marketing by a company (company name not visible in the screenshot); OP only asks follow-up survey questions. Flag as vendor promotion.

**Manual methods and numbers from replies**
- killchain: "FSViewer, tagging keepers as I go. It's super fast as it relies on the embedded JPEG in each RAW"; one pass.
- LeicaM6guy (news): "Photo mechanic is the fastest method." / "No longer than absolutely necessary. The job is to beat the other photographers to the punch."
- kurtozan251: "Buying photo mechanic was the best money I've ever spent!"
- kowalski71 (motorsport): "I'm coming home with like 6000-8000 files per day of shooting. I can usually cull that in 3-4 hours... I'm shooting for a 90% delete rate." Uses PhotoMechanic first pass, Lightroom second pass.
- need2know2: "I often ended up with thousands of shots per event or session, and the culling process was hell. My eyes get blurry trying to decide which shot is the best focused among the dozen burst."
- Sp00nSlayer: "How long do you cull for?" -> "way too damn long."
- radeklat (hobbyist, photos from multiple people/devices): "I collect photos from my DSLR, phone, other people's phones and import all in lightroom... This pass also tells me where are duplicates located because photos from multiple sources are not always next to each other. Sometimes similar pictures are taken on different days... Order manually duplicates next to each other and keep ideally one of each." -> multi-source ordering/duplicate pain stated explicitly.

---

## 25. "Culling photos as a newbie wildlife photographer... will this get easier and more enjoyable?"
r/photography, 2y ago. File: `40 - Culling photos as a newbie wildlife photographer... will this get easier and mor.png`
Hobbyist/wildlife, not wedding; useful for general sentiment.

**The pain**
- turtle_shock (OP, hobbyist): "I absolutely detest sitting at my computer sorting through everything. I've been at this for an hour, and I'm not even halfway done. Everything starts to look the same after a while, my eyes go funny and I end up keeping far too many."
- [deleted] (nightlife events): "Culling is the process I detest the most and I shoot night life events I average 1500 photos a night".
- Junin-Toiro: "No it is not enjoyable, at least until you come to looking at the top 2-10% of the images. It won't become enjoyable."
- Bishops_Guest: "I recently shot a fire performance and came home with 11,000 pictures."

**AI culling: expectations vs. current state**
- Tak_Galaman: "I tried a few trial of after shoot and it sort of worked, but obviously needed a bird or wildlife mode."
- Junin-Toiro: "Nothing yet. It is not ready for my style of photo. It needs to get better first, and as you say needs to excel at niches." / "out-of-focus is kind of easy to detect as long as it is not artistry pics." / "In a decade new photographers will look at us with pity when they learn we were doing this by hand."
- BuddhaChrist_ideas (second-hand praise): "There are AI culling programs out there that have very high success rates, and can be fine tuned and tweaked based on your own needs. My buddy uses them for wedding photography, and swears by them. Saves hundreds of hours over the course of a work year."
- Tak_Galaman on Adobe: a preset question in an Adobe survey was "we're thinking of helping you cull through a ton of pictures".

**Manual tips**
- mostlyharmless71: "Lightroom allows you to create photo stacks organized by capture time... 'Auto-stack by capture time' is the Lightroom option you want." (others: "something I didn't know") -> time-based burst grouping exists in LrC but is little known and single-camera.
- trying_to_adult_here: "Photo Mechanic will make your first pass through much faster... A one-second delay to show you a sharp photo adds up when you're going through 2000 photos."
- Framemake: "go backwards - most of the time, your pick from the batch of X photos of your subject is nearer to the back of the pack".
- RedditredRabbit: "Deleting is painful. Deleting 400 times is painful 400 times! Invert the process. Pick winners."
- AlexHD: "If you have to think about whether a photo is good or bad, it's bad."

---

## Batch summary

### (1) Complaints per competitor, ranked by how often they appear in this batch

**Aftershoot** (most discussed; ~9 distinct critical voices)
1. You still have to review everything, so little or no time is saved for weddings - evanrphoto (twice, threads 5 and 15), lexiestudios (20), morningpeach (20), JoelBoily's 3-6 h "final cull" after Aftershoot (8), Nikbryantphoto's manual second pass (10).
2. Closed eyes treated as a defect although often intentional/emotional - evanrphoto (5, 15).
3. Poor "best of group" choices / wrong grouping ("deeming different grouping as identical") - evanrphoto (5, 15).
4. AI editing quality (white balance, tint) - Temporary-Mix8022, getluminarymedia (23).
5. Astroturfing / heavy advertising - Temporary-Mix8022 (23); OP of thread 20 "seeing a lot of ads"; OP of thread 10 bans "AI company affiliates".
6. Price / subscription: $499-500 per year (2, 23); "locked in at early pricing" (20); one user cloned it to save "$500p/y" (23); "overkill for what I needed" (20).
7. Stability: never finished a full set "without freezing or getting stuck" (1).
8. Needs training on your own data: "not bad once trained" (6), "learns your editing style after a few thousand images have been uploaded" (2).
9. No genre modes for non-wedding work: "needed a bird or wildlife mode" (25).

**Adobe Lightroom Assisted Culling** (5 voices)
1. Only catches the easy cases: "pretty underwhelming... those are also the cases that are easiest to cull manually" (13); "still very basic" (13).
2. Must double-check: "defeat the purpose?", wrong out-of-focus call on a good shot (18); "not really 'set and forget'" (20).
3. "didn't learn my personal culling preferences" (23); "takes a while" (20).

**Lightroom (classic manual culling)**: slow previews / "Loading" (14, 19, 25), poor shortcut ergonomics and no remapping (7, 21), performance and crashes (21), weak face recognition (21).

**FilterPixel**: accused of spam accounts (5); weak on wildlife (5); self-reported "90% accurate" (5). Costs "around $40 every month" (20).

**Imagen**: "nearly as fast to do it myself" for culling (20); per-photo pricing with extras for crop/straighten, retouching not included (2). Otherwise mostly praised.

**Narrative Select**: "wasn't really happy with the ongoing costs" (13).

**Photo Mechanic**: does not select for you (1); "unintuitive Windows 95 program with infuriating shortcuts", an extra step (10); "expensive for an amateur" (20); weak for fine focus comparison (11).

**Outsourcing services**: ShootDotEdit - colours mismatched between cameras, had to re-edit whole gallery, cancelled twice (22); Evolve - "Avoid" (22); Image Salon - customer service, "end up still editing" (22); Freedom Edits - 30-40 c/image, stopped using (12); Fotofafa - hidden pricing, FTP security (17). General: 5-7 business days to 2 weeks turnaround (14, 17), onboarding learning curve (22), upload friction (6, 17), loss of personal style (19).

**Unnamed AI cullers**: "pretty strict regarding focus" (15); "I stopped using it because sometimes I still liked the photos" (13).

### (2) Praise per competitor
- **Aftershoot**: "lifesaver" (12); "definitely a time saver" (5); culling from 2 h to much less (8, Joris818); "95% accurate for what I would pick in less than 10 minutes" (20); used as rough-cull first pass by a 6,000-9,000-frame team (8); AI editing praised even by its culling critic evanrphoto (5, 15); flat annual fee liked vs per-image (23, possibly promotional).
- **Imagen**: "1000 photos done and delivered in 10 mins" for editing (2); "cut the culling time significantly" (10); "pretty trustworthy" culling (20, reads promotional).
- **FilterPixel**: 3,400 images in 15 minutes; detects intentional closed eyes (5, flagged as probable spam); 10-point scoring "bang on" (20, reads promotional).
- **Narrative Select**: face/close-up panel loved (10, 13); focus/eyes analysis (1).
- **Photo Mechanic**: by far the most recommended tool in this batch - "the standard", "gold standard", "best money I've ever spent", "halved my culling time" (1, 8, 11, 13, 14, 19, 20, 24, 25).
- **Lightroom Assisted Culling**: "it is good" (20); "goes quicker with this feature" (18); "it was okay!" (23).
- **FastRawViewer**: cheap perpetual licence, "$25", fast (1, 10, 20).
- **Outsourcing**: Fotofafa and Raw Digital customer service (22); Image Salon same editor for 3 years (22); "best decision I ever made" (22).

### (3) Multi-photographer / multi-camera findings
- Consensus: photos of all shooters go "in one pot", are culled blind to author and delivered sequentially by time (thread 3: evanrphoto, rmric0, koronadal, two deleted users).
- A bride's view of unmerged delivery from 3 shooters: "annoying... It would have been nice to see the story as it happened" (3).
- Time sync is done by hand: shooting a synchronized frame on both bodies and shifting capture time in Lightroom Classic (10, disgruntledempanada); "sync your images by time stamp" (3).
- Second shooter's share of the final gallery: 10-20% (ChadEEEE; koronadal with unfamiliar second), 30-40% up to "almost half" with a regular partner (3).
- Cross-shooter duplicates are an explicit cull criterion: "I choose the good photos that aren't duplicates of mine" (3); two cameras deliberately cover the same moment (3, koronadal's coverage plan).
- Two shooters multiply volume and cull time: 5,000 images / 2.5 h (8, chickthatclicks); 6,000-9,000 RAWs (8, JoelBoily); "two shooters with 2000+ shots" -> 12-20 h total (8); "3-4k (with a second)" -> 8 h cull (8).
- Colour mismatch between cameras is a known outsourcing failure (22, Inner_Audience).
- Mixed inputs from the second (JPEG instead of RAW, empty card) land on the lead, who does all post work (16).
- Multi-source duplicates not adjacent in the timeline (hobbyist, 24, radeklat).
- No AI culling tool is mentioned anywhere in this batch as handling merging, time sync or cross-camera duplicates.

### (4) Hard numbers
Photos shot / delivered per wedding
- 1,500-2,000 shot, ~500 delivered (30%) (14). 3,000-5,000 shot, 800-1,200 delivered (14). ~4,500 received, 600-800 delivered (14).
- 3k shot -> 400-500 (8). 3,400 frames -> ~330 delivered (8). 3-6k -> 500-2,000 (8). ~1,500 off the cards with a second -> 700-800 (8). 6,000-9,000 RAWs (couple team) -> 700-1,200 (8). 2,000-4,000 frames solo, 8 h wedding (19). 2-5k per wedding weekend (10). 2,000-3,000 per wedding (17). Wedding of 6,000 images (7). ~3,000 -> ~600 (19).
- Fotofafa: 80% of weddings 600-800 images selected for edit; range 200-1,200 (17).
- Keep rate examples: 30% (14); ~10% (11, non-wedding); 90% delete target in motorsport (24).

Culling time
- 1 h per 2,000 photos; 2.5 h for a two-shooter 5,000 (8). 1-1.5 h (8, 19, 17). ~1 h for 6,000 with mouse-wheel method (7). 60-90 min for 3-6k (8). 2 h minimum (8). "4 hours just to cull" (8, two users). 8 h for 3-4k (8). 3-6 h final cull after Aftershoot rough cull (8). 6-8 h cull+edit for an employed editor (14). 3-4 h for 6,000-8,000 motorsport files (24). 1,000 wedding photos in 15 min with a 3-key sorter (20). 1k images in <10 min in Photo Mechanic (15).
- AI claims: 3,400 images in 15 min (FilterPixel, 5, probable promo); Aftershoot <10 min + 10-20 min review, "95% accurate" (20); "save 5-6 hours" (5, probable promo); "hundreds of hours over the course of a work year" (25, second-hand).

Total post-production and turnaround
- 4-6 h, 6 h, 8-12 h, 10-15 h, 12-20 h, 30 h, 30-40 h, 4 working days per wedding (8). 15-20 h (14). 1.5 to 4-5 days for 700-800 images (10). 8 working days per wedding, down from 13 (19).
- Delivery: next day (8, niresangwa); within a month (19); 3-4 weeks (8); 4-6 weeks (8); 3 months for album (8); 9 October weddings finished in June (19).
- Outsourcing turnaround: 2-3 days (19), 5-7 business days (17), 1 week (10), 2 weeks (14).

Weddings per year
- 16 in a 5-month season (19), 23 (19), 35-40 in one summer (11), "a little over 40" (19), 47 (19), ~50 jobs/yr for an editor (14), 50 called "a recipe for disaster" (4). 70+ h weeks in season (19).

Prices
- Culling service: Fotofafa $0.09/image submitted (17); "about $200 a wedding for just the basic culling service" ten years ago (20).
- Human editing per image: $0.10 (2), $0.20 (23), $0.25+ (2), $0.30-0.40 (12), $0.35 (17), $0.35-0.50 (23), $0.40 (23), ~$0.50 / $400+ per 600-image wedding (23). Hourly: $20, $50 (23).
- AI: Imagen $0.05/photo + $0.01 each for crop and straighten (2); Aftershoot $499/year unlimited (2), "$500p/y" (23); FilterPixel ~$40/month (20); Aftershoot profile resold at $100/wedding (12); FastRawViewer $25 perpetual (1).
- Second shooters: $15-30/h typical, $60/h NYC, $600 for 5 h (16).
- Fotofafa volume: ~200,000 images/month, >1,000 photographers, editors up to 2,500 images/day (17).

### (5) Unmet needs and feature wishes
- A cull whose rejects do not need re-checking: every AI user in this batch who gives detail still reviews both piles (5, 15, 18, 20).
- Respect for intentional closed eyes and emotional frames (5, 15) and for slightly soft but special moments (15: "I'd like to keep slightly blurred photos as well"; 15: "imperfectly awesome" shots).
- Reliable "best of each series" across near-duplicates, the stated core need (15 OP; 13 OP; 19 arcterex; 7).
- Correct grouping: not merging different group photos as identical (5).
- Automatic split of the day into scenes/chapters (10: "How do you break everything into scenes?"; 19 pspetrini; 14 cltmn; 9 PanicSwtchd).
- Multi-camera timeline: automatic time sync and merged chronological order (3, 10), cross-shooter duplicate removal (3), consistent colour across bodies (22).
- Works without training/profile and without upload: "once trained", "after a few thousand images have been uploaded" (2, 6); upload friction and privacy unease with FTP/cloud (6, 17); indie tools advertise "runs locally" (1).
- Fair pricing: complaints about ongoing costs/subscriptions (13, 20, 23), per-wedding resale at $100 (12), cheap perpetual licences praised (1, 20).
- Genre awareness (wildlife, sports) (5, 25).
- Express/same-night turnaround (12).
- Lightroom plug-in or in-Lightroom workflow preferred (15 OP, 10).
- Seeing who is in the frame: face close-up panels are the single most praised AI-adjacent feature (10, 13).
- Trustworthy community presence: Reddit users are hostile to vendor accounts and some subs ban AI project posts (5, 10, 23).

### (6) Ten strongest quotable lines
1. evanrphoto, full-time wedding photographer (thread 15, `37 - Are Ai culling tools worth it r AskPhotography.png`): "I use AfterShoot for some shoots where it provides some value, but with weddings for me it provides risk and little to no value. It 'selects' about 40% of the images and I need to review both the culled-in and culled-out images."
2. evanrphoto (same thread): "It primarily culls out out of focus images (which I barely have these days) and closed eye photos (which are sometimes the emotional ones which are the most important)."
3. evanrphoto (thread 5, `34 - Need second opinion on AI Photo Culling Software r AskPhotography.png`): "even in static group photos it misses some of the groupings by deeming different grouping as identical. I basically have to review everything that was culled and also review a lot of what was culled out."
4. One_Chart7921 (thread 15): "Personally I don't trust AI to cull my photos for me. I go through them all manually. It takes time, but I can't risk a good photo being missed on the whims of an AI."
5. TinfoilCamera (thread 15): "If you do not look at each image yourself then you will never spot the 'imperfectly awesome' shots that sometimes happen... where you totally screw something up and that screwup makes the image rather than breaking it."
6. lexiestudios (thread 20, `38 - What software do you use for photo culling r AskPhotography.png`): "Lightroom AI culling works okay for me, but it's not really 'set and forget.' AfterShoot looks promising but I haven't fully trusted it yet for client work. I still end up manually reviewing everything."
7. 02911_Photography on Lightroom Assisted Culling (thread 18, `37 - How do you select your photos after returning from a trip r AskPhotography.png`): "This feature makes me nervous, I assume it puts them all into its own bucket so you can make a pass at them to double check but doesn't that defeat the purpose?"
8. cbunn81 on Lightroom Assisted Culling (thread 13, `36 - Photo Culling Process Tips r photography.png`): "They can do okay with working out which are obviously out of focus or have closed eyes of the subject. But those are also the cases that are easiest to cull manually."
9. weallstartatzero, as a bride whose 3 shooters were delivered separately (thread 3, `33 - What percentage of your second shooter's shots do you use How do you determine w.png`): "It also was a little annoying to be going through one part of our day and then when it's over, re start again. It would have been nice to see the story as it happened."
10. disgruntledempanada (thread 10, `35 - What is your editing workflow r WeddingPhotography.png`): "I take a synchronized photo on each so that I can sync up the timing of the shots and keep things in chronological order (I select all the A7iii images and sync them to the A7Cii's first or last shot time in Lightroom Classic)."

Runner-up lines: Temporary-Mix8022 (thread 23): "I'm so done with the astroturfing by that scam company."; chickthatclicks (thread 8): "a two shooter wedding might take me 2.5 hours to cull (5000 images)"; nuttychichi (thread 8): "It takes me like 4 hours just to cull LOL."; SnooRegrets8767 (thread 20, positive): "for it to get to 95% accurate for what I would pick in less than 10 minutes, for me to spend another 10-20 is still a win".

### Caveats for citation
- Thread 1 quotes are back-translated from a Croatian auto-translation; cite by paraphrase, not as verbatim English.
- Several pro-vendor comments (FilterPixel in thread 5; Imagen, FilterPixel, Evoto in thread 20; XOMaddsPhoto in thread 23; photomind.online in thread 13) could not be verified as genuine users; thread 5 contains an explicit spam accusation against FilterPixel accounts.
- evanrphoto is a single, very active r/WeddingPhotography voice; his Aftershoot critique appears in two threads and should be counted as one person.
- Most volume/time numbers in threads 3, 14, 17 and 19 are 9-12 years old; threads 8, 15 and 5 are ~4 years old; threads 10, 11, 18, 20, 21, 23 are within about the last year.
