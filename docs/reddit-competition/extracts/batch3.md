# Batch 3 — Reddit evidence on culling tools, AI culling and multi-photographer workflow

Source: `batches/batch3.txt` (6,200 lines of OCR, 33 thread screenshots, all read in full).

Notes on reading this file:
- Quotes are verbatim; only obvious OCR errors were fixed ("Al" -> "AI", "1m" -> "I'm", "0k" -> "ok", "10096" -> "100%"). `[...]` marks an omission, `[unclear OCR]` a doubtful passage.
- **Upvote counts are almost never legible in this OCR** (they come out as "0 11", "O IO", "e 020"), so they are omitted unless clear. Post-level counts are given where readable.
- Where the OCR dropped a username (it shows only "• 2y ago"), the speaker is given as "[username lost in OCR]".
- Ages are as shown on the screenshot (relative to capture time, 2026).
- "File" is the screenshot name as it appears in the `######## THREAD FILE:` header.

Threads with nothing relevant (one line each):
- `17 - How to become a second shooter r WeddingPhotography.png` (5y) — career advice only. Only side fact: a studio trains "third shooters" whose photos are not expected to go to the couple (ThufirrHawat).
- `19 - For people who didn't do first looks, how much time did photos take r BigBudgetB.png` (3y) — timeline planning for couples; only says a "very strong 2nd shooter" is needed to shoot reception details in parallel.
- `20 - Photography 6 hours vs. 10 hours r weddingplanning.png` (5y) — couple-side pricing only: 6 h = $4,000, 10 h = $5,000, both with second shooter included; another couple paid $850 for 4 h.
- `22 - How Do You Handle Final Timeline Calls with Associate Photographers r WeddingPho.png` (1y) — studio/associate client-call etiquette.
- `25 - As a second shooter, am I okay to edit pics r WeddingPhotography.png` (10mo) — copyright/contract dispute between lead and second shooter.

Relevant threads: 28 (sections below).

---

## 1. "Culling/Editing process" — r/Lightroom, 3mo ago
File: `17 - Culling Editing process r Lightroom.png` (OP u/LDubya1, semi-pro; 30 comments)

**Lightroom's own AI culling / Imagen**
- No Parfait 2104: "Ai culling is also a great way to automate more of your process while still retaining control. I haven't had much success with Lightroom's culling so I also occasionally use Imagen's culling to rate my photos and quickly select the strongest of each set of images. For this I just upload my project then I'm able to see the rated, edited photos in their app and quickly go through them to adjust for my preferences."
- No Parfait 2104 (earlier comment): "Another way that I cull larger projects is using Imagen Ai and just uploading the entire folder. When its done I'm able to review the rated photos with a preview of what the final edit will look like, make any changes to the selected images then submit for editing." (Same user praises Imagen in two separate comments — reads somewhat promotional, unverified.)
- Jazzlike Diamond 441: "Lightroom has AI-assisted culling features now but using that doesn't really solve 'running slow' problem. If you are a heavy shooter then definitely use culling software."

**Multiple photographers**
- No Parfait 2104: "If there are more than one photographers I'll also rate each set of photos with a different color label." (manual workaround to keep two shooters' sets apart)

**Manual culling tools / method**
- yorchsans: "give a try to Photo-mechanic. the speed of culling is on another level with this program"
- Jeffrey_J_Davis: "you really should consider using a culling specific front end (FastRawViewer, Faststone, PhotoMechanic) to ONLY bring the 5% - 10% of your photos which are likely to be keepers. Will dramatically speed up your workflow and debloat your catalog."
- wreeper007: "Learn to lock/tag in camera and use photomechanic to only import those first."
- ExploreroftheLight: "I've usually picked maybe 10% or 15% of my photos at this point" (after first star pass).
- grim-eyed-goat: "I NEED to delete the ones I don't want to keep to free my mind of them and focus on the set I want to edit."
- Lightroom_Help: "The sad truth is that LrC doesn't work well on all Windows systems. [...] a PC may run LrC flawlessly or with several performance or stability issues."

**Vendor promotion / moderation**
- danielrobthis (tool founder, self-disclosed): "Or Cullibrate - it's a more modern alternative at 1/5th the price :) (Disclaimer: I am the founder)." (alternative to Photo Mechanic)
- Lightroom-ModTeam removed another comment: "Your post has been removed because it looks to be purely promoting your own product or services."

---

## 2. "I built this very fast RAW previewer with AI assisted culling features" (OptiCull) — r/SonyAlpha, 3y ago
File: `17 - I built this very fast RAW previewer with AI assisted culling features r SonyAlp.png` (OP u/shelehs = developer of OptiCull; 80 upvotes, 50 comments)

All "shelehs" quotes are from the tool's developer (vendor).

**Pricing / platform**
- shelehs (developer): "Currently there is Lifetime offer of USD 59.99 [...] There are annual and monthly offers also." "The base product, without upgrade to Pro also gives generous manual culling features."
- shelehs: "OptiCull is just launched to AppStore this Wednesday, after being in Beta on TestFlight for around 2 months. There are already around 20 users who bought the Lifetime offer".
- shelehs: "Sorry [...] but Windows app is not planned." "You can try other products in market like Narrative Select, Aftershoot, Filterpixel, Optyx etc. for Windows version."
- PixelFNQ: "So maybe make it clear that this is for Apple users only in the description so thousands of us don't waste time." (Three more users ask for Windows/Linux.)

**Faces: who matters in the frame (developer admits limitation)**
- shelehs (developer): "Currently it works good with faces occupying at least 15-20% of full image size. For certain conditions when there are lot of faces in background like in wedding shoot, it helps also to not get background faces while comparing. But I agree this is a limitation for certain kind of shoots and also for certain scenarios in wedding shoots."
- shelehs: "this will be fixed in coming releases with detecting even a face occupying very small area in whole image. Just that with that there has to be some way to filter the background faces in the UI. Also beyond certain size it will not be able to give you the correct focus score, as there won't be enough pixels to assess that with confidence."
- WombatKiddo (working photographer): "The main thing I'm interested in is the jumping from face to face for quick loupe checking. Although it seems to be buggy and is not working on every photo." / "How do you feel about it only recognizing 3 faces in this photo? Is there a limit on faces?" / "this photo will not recognize any face. So pressing 'V' just does nothing."

**Grouping / scenes / ordering**
- WombatKiddo: "Can I merge two scenes if the auto processor didn't realize they're the same scene?"
- shelehs (developer) answer: "you can first tune the 'Grouping Duplicates' preference [...] Ideally keep the maximum number of photos in group around 9. [...] if you see next scene to be also similar then you can just select that scene also and you can compare photos from multiple scenes".
- PhotoKada (wedding photographer): "Why am I not able to sort my photos by file name? It sorts by capture time, sure, but sometimes this throws a sequence of photos out of order."
- shelehs: "Scenes are always sorted by capture time. This is required to see the Keepers, Duplicates and Rejects in order while reviewing."

**Bugs / hardware**
- WombatKiddo: "Well, I tried a few photos down from there and... it crashed." "M2 Pro Macbook 32GB ram btw."
- jebrennan: "I'm trying it on a folder full of photos, 4800 small photos. I scroll in the left filmstrip, but it keeps jumping to the selected image. [...] Update: OptiCull was using over 20GB of memory."

**Praise**
- PhotoKada: "This helps me plenty as a wedding photographer when I need to make my first-pass selections." / "So it's very effective".
- KenjiroOshiro: "This has opened my eyes to culling software to improve my workflow. It's something I never considered before but would definitely use."

**Privacy as a selling point (vendor claim)**
- shelehs: "OptiCull is the only option available on the Apple AppStore [...] OptiCull has to run in Apple's Sandbox on the device and it only has access to files and folders you select inside the app."

---

## 3. "Building an AI wedding video culling system — selects some clips but missing best emotional moments" — r/computervision, 7mo ago
File: `18 - Building an AI wedding video culling system — selects some clips but missing bes.png` (OP u/perrychawla, a developer — not a photographer)

Relevant as independent evidence that "technical filtering + VLM" misses moments (video, but same problem):
- perrychawla (developer): stack is "Local setup (Mac M1 Max / M4 Mini)", "Qwen2.5-VL (MLX) for visual understanding", "OpenCV for blur/shake filtering".
- "V3 misses genuinely strong emotional moments. Frame-based approach seems to fail for things like: reactions, subtle prep moments, emotional build-up."
- "Current system feels more like 'technical filtering + basic AI' rather than true culling".
- Vimerse Media: "I think AI should provide context for each clip and what the shot is about. And it should decide if the shot is relevant for the flow OR is worth keeping due to emotional value."

---

## 4. "Imagen AI" — r/WeddingPhotography, 4y ago
File: `18 - Imagen AI r WeddingPhotography.png` (OP u/awkwardlyalexa; 92 comments). Mostly about Imagen **editing**, with remarks on Aftershoot culling.

**Aftershoot culling — complaints**
- thefrenchdev: "I haven't but I tried Aftershoot and it was rather disappointing (discarding good pictures and selecting bad ones) and not giving any credit to the artistic aspect of photography."
- evanrphoto: "I also haven't found Aftershoot very useful to me but my experience with Imagen AI has been very different. Don't let Aftershoot taint your idea of AI."
- [deleted]: "As for other AI software, I tried Aftershoot but hated it. It would literally delete all my favorite photos. The file categorizing is confusing, and lastly not all my images were added to load into the software."

**AI culling in general — refusal for weddings**
- [deleted]: "Fwiw I think all AI culling tools are absolutely useless for weddings but that's just my experience and opinion."
- thefrenchdev: "I also kind of think AI culling, at least as it is now, is useless for weddings. Maybe because there are too many situations where the choice to keep or reject a picture depends on how the photographer feels at the moment."
- [deleted]: "Some wedding photographers appear to be fine with letting AI make culling 'decisions', they often justify it with 'my clients were happy so I'm happy' but I... disagree that that is good justification."

**Imagen — training/profile hassle and upload**
- OP awkwardlyalexa: "my ADHD brain just wanted an answer faster than the Imagen custom profile upload process will allow for."
- overconfidentquartz: "They want something like 3000+ edited photos to build your editing style though (unless you use one of theirs) so be aware of that if you don't have 3000 wedding edits available..."
- ServiceB4Self: "You have to feed it like 5,000 of your previous edits in order for it to properly learn your style".
- [deleted]: "You have to send it thousands of shots. [...] as many full weddings edited with your consistent style, in as many different environments as possible."
- evanrphoto: "You have to put in the time to put together a good initial input upload to create a profile."

**Imagen — pricing / billing / support complaints**
- user 467 [username partly lost]: "Submitted 3 orders and did not like the edits. Also, be careful... They continued to charge my card a 'monthly fee'. [...] I did not select or signup for a subscription service whatsoever. I paid per image. They were resistant, but finally refunded me."
- user 467 quoting Imagen's reply: "'Since June 2nd, we changed our pricing, and now there is a general minimum monthly fee of $7'. So it was after I had started."
- ServiceB4Self: "it was pretty clear that there would be a minimum $7 monthly charge on months I don't use it".
- Civil_Priority3736 (2y): "I used it and hated it personally. Every single photo was dark and muddy. [...] And they proceeded to charge me $131 dollars even though no images were downloaded or taken. Customer service is ridiculous on trying to delete accounts and giving refunds for photos that were never used."
- Active_Asparagus_952 (2y, studio): "Our photo studio tried Imagen and regret doing so greatly! Although there was SOME time savings, the number of photos we still had to re-edit wasn't worth the price. We used up our 72k images in first 7 months and should've been charged $240/mo. Upon further investigation after our 72k images ran out we'd been [screenshot cut off]"
- donatedknowledge: "Why save, upload, wait, download, and double-check while paying for it?" / "This 'AI' basically just pressed Ctrl+U for you."

**Imagen — praise (editing)**
- royal_friendly: "I used it for all my weddings last year, takes me from around 16 to 2 hours per wedding gallery. It is not perfect but is better than regular presets (by a long shot)."
- [username lost in OCR]: "everything i shoot runs through it, and it elevates my starting point for a final manual pass so well that my most common edit is 'next.'"
- e-lishaphoto: "Sessions cost under ten bucks and weddings are about $30. I save SO much time."
- ServiceB4Self: "30 bucks and a wedding pops out edited in my own style better than if I paid some dude to edit them for me (and faster too!)"
- Erick_oseguera: "I used to pay a guy for editing my weddings and it was kind of expensive, it took a one or two weeks and I had to make a final retouch after that. Imagen now solves the 'base' for editing faster (it takes just 1 hour) [...] The faster wedding I've done is just 3 days (700 photos). I think it's not a game changer, but a great tool."
- Rjs-images81: "2000 images edited all consistent in like 20 min!"
- slandoe (2y): "Once you have it trained and have uploaded about 3,000 images from previously edited galleries, it's scary how good it is. I just spent 2 hours tweaking the gallery it edited for me".
- plantypete: "It's very good, 90% success. But it only adjusts white balance, exposure and straightening - so isn't going to save you more than an hour unless you're pretty slow." (disputed by others)

**Astroturfing / sponsorship suspicion**
- donatedknowledge to a frequent Imagen advocate [username lost in OCR]: "Don't you need to disclose your being sponsored by Imagen AI? You're in every thread they're mentioned." Reply: "not 'sponsored' by Imagen as i've never signed a single agreement with them."
- Bitesandtickles (German): sells own profile in the Imagen profile shop (link posted) — interested party.
- Imagen "has a beta program for their upcoming culling feature" ([deleted], 4y ago).

---

## 5. "Improving editing workflow efficiency" — r/WeddingPhotography, 2y ago
File: `18 - Improving editing workflow efficiency r WeddingPhotography.png` (OP u/accl1k; 22 comments)

**OP's workflow and second-shooter pain**
- OP: "Cull in narrative select, Cull again, Export into Lightroom, Organize by scene (reception, getting ready, bridal party, family etc.), Edit by scene, Final retouchups".
- OP: "there's a ton of variability from my photos and my second shooter".
- OP: "I also have 800 photos. I've noticed the last two galleries I have thrown out repeat images while I'm editing. Maybe I need to cull better?"

**Aftershoot / Narrative**
- AccomplishedSir535: "I use Aftershoot AI to cull & apply my edit. I always go thru the cull to make sure that the images it tossed are good to go & then I tweak the images as needed in Lightroom. Using Aftershoot has saved me hours on every gallery!!! I typically deliver 500-750 images for a 8 hour wedding, I can get that done in 3 hours if my ADHD & kids will let me!" (praise — but note she still checks the rejects)
- michael_jonny (1y; creator of competing tool Cureyta — vendor): "With Aftershoot, it's so high level and not very accurate, I still end up having to do the culling manually". / "I used to use Aftershoot and Narrative a lot but it didn't wanna just do simple stuff... wanted to be able to describe with words the types of photos to cull. So I created Cureyta.com".
- CommercialShip810: "You can cut out the separate program for culling though, they're unnecessary."
- webguynd: "For now I don't use any AI culling so I can't really speak to that process. Outside of things like family formals, the last time I tried AI culling I found it wasn't really all that much of a time saver."

**Manual methods and numbers**
- Arvosss: "I make a first selection on my camera, I have a shortcut to add 4 stars when viewing my photos. [...] This saves me at least 2-3 hours of culling on PC." Also: "I'm experimenting with neurapix to edit my pictures with AI."
- fedornuthugger: "Using photo mechanic to cull and rank before importing into Lightroom saves me a lot of time. It is much faster than Lightroom."
- dreadpirater: "I can usually edit a 500 photo wedding in an 8 hour day."
- CommercialShip810: "In an 8 hour day I will have an entire wedding edited and exported"; "I'm in the 400-600 range for a full day."; "I also use a Loupedeck [...] It probably took another hour off each client edit."

---

## 6. "When to hire a second shooter?" — r/WeddingPhotography, 4y ago
File: `18 - When to hire a second shooter r WeddingPhotography.png` (OP u/jehovahsthickness77; 23 comments)

Multi-photographer context only (no tool talk):
- OP: "(bc i know that for weddings, the second just gives the main all their raw files [...])" — confirms the standard hand-over: lead receives all of the second's RAWs and must cull them.
- OP's case: 500-guest wedding where the couple hired a second, independent lead photographer.
- maxlovesbears: "I like to work with a second photographer on weddings that are 6 hours or greater."
- bettie-rage: "Anything over 120 guests is 2 photographer automatically. [...] For a 500 person wedding I would have had a 3 photographer package and maybe brought along an intern as a fourth".
- evanrphoto: "most of my clients also want a second shooter as safety and to ensure as many candid guest photos as possible."
- Studio_Xperience: "2nd shooter is for peace of mind and they take the bland boring photos that 'have' to be taken."

---

## 7. "AI culling software" — r/WeddingPhotography, ~3y ago
File: `19 - AI culling software r WeddingPhotography.png` (OP u/Commercial_Foot3145; 36 comments). **Strongest thread in the batch.**

**Moderator note on astroturfing (verbatim)**
- WeddingPhotography-ModTeam (MOD): "Please note that this subreddit has experienced a significant level of astroturfing relating to this topic and specific AI companies. The mods will remove comments and/or delete this thread if it appears astroturfing, brigading, or bad faith comment reporting is occurring. OP is an active community member. Community members should be extra vigilant and critical of advice, recommendations, and comments in any and all threads related to this topic and these companies."

**Aftershoot — accuracy, "still have to check everything"**
- OP Commercial_Foot3145: "I currently use AfterShoot. I'll find AfterShoot marking an image a 5-star that is out of focus and super dark, but yet marking a perfectly sharp and properly exposed image as a 1-star. A lot. I have to go through and manually cull everything in the end. Always. Every single time."
- OP: "Sometimes I feel as though someone sat down at the computer completely blindfolded and randomly selected images with AS."
- 444rj44: "tried AS, deleted. my eye and style is far better to decide."
- plantypete: "I thought Aftershoot was pretty good. But no faster than me as a human."
- ConstructionSma11979 (1y): "AfterShoot gave me the same headaches with weird ratings, so I started trying out Evoto AI. What stood out is how it handles sharpness and exposure more reliably and quickly flags blinks or blurs. It's definitely not perfect, but it cut down the amount of manual culling I had to do." (late comment recommending another product — possible promotion)

**Aftershoot — lost a photo the couple asked for (false reject)**
- Thin_Register_849: "Been with aftershoot since the start. Tested the edits in alpha and beta too. I shall not be using it from now on. I've realised it's essentially made me a worse photographer. I'm actually quite ashamed, I can cull pretty quick inside of LR anyway, so not sure why I fell for the branding".
- Thin_Register_849 (asked why): "Because i trusted it far too much. I became lazy, to the point where i was very happy with it, oblivious to the fact that it was bad. It's when I had a group photo missing from the gallery, and the couple asked me for it. I found it in Lightroom, I went back through aftershoot's initial cull and was sure they were all there, but they weren't. My eyes became lazy. I stopped using aftershoot for a season, and it was nice culling manually again. This year I've had used it twice, and both times it's failed on me. There is absolutely no reason to have selected the photos it selected this [screenshot cut off]"

**Aftershoot — defence / praise, and how it treats blur and training**
- LarryAndHisCats: "Ask me to choose 3 photos from a group of 7 and I'll give you 7..no I mean 4... no I mean 6... no I mean 2. For me, Aftershoot has been a miracle......"
- LarryAndHisCats: "that AI culling just gets it right the first time because it should just know because it's AI, right? That's not really the case."
- LarryAndHisCats: "it will give you 1 of everything. Things like in your case, the out of focus and super dark 5-star image. The AI doesn't know if you took that photo with intentional blur or not - it could be a creative technique you use. From what I understand, the lighting - properly exposed or way underexposed is not part of the selection process."
- LarryAndHisCats: "The AI will also learn from you [...] I think it took 4 or 5 weddings till it got what I like to see down. I have a 2nd shooter who takes soft focus photos of the bride with her father - it's not really my style, but my clients like them. Because I've marked them as 5-star images, Aftershoot now gives me some of those".
- LarryAndHisCats workflow: "when the cull is done in Aftershoot, I'll double check the cull in grid view in Aftershoot and make any adjustments."
- shawtywannaparty: "Aftershoot has been a game-changer for sure! +100 on customizing and using it over time for it to learn your style" (short, generic — treat with the mod warning in mind)

**AI culling refused; humans preferred**
- redrabbit1977: "Wildernis Hybrid Ai. They use human cullers, Ai editing, then humans to finish and fix. Game changer! $120 for a wedding. Ai simply cant cull, it requires a human eye imho." (same user recommends this service in three threads of this batch)
- No-Neighborhood-2109: "Hire a human culler. AI still cannot detect emotions in photos. Its a worthy investment for your photography business."
- noblankish: "Ai sucks. Best thing i did regarding culling was getting a Playstation controller."
- noblankish: "After years playing with a bunch of softwares for culling, from non Ai (photomechanic) to Ai ones, i realized that jumping to one thing to another and also needing to re-check everything was just a waste of time. Lightroom + a cheap usb playstation 4 controller + Joystick mapper app [...] is the fastest way i've found to cull 3500+ pictures per wedding."
- bugpfeifee: "I'm not a supporter of ai culling. You need to see the bad photos you took, to actually improve and become a better photographer, imho."

**FilterPixel — praise**
- ckisela: "I use Filter Pixel and have had a positive experience using it. The company seems small enough that when I need a feature added I can send a message and they're responsive enough to key it in. Just looked and it's already edited into the 6 figures of photos and 10,000 hours saved."

**Vendor self-promotion (privacy angle)**
- pickeraiapp (developer, 2y): "i made Picker AI which uses our 100% private AI so your photos never leave your device. [...] Or if interested create a Mac app version specifically for culling for photographers that's 100% private and you have control over how the AI behaves."

---

## 8. r/ImagenApp front page (vendor's own subreddit) — posts 5–20 days old
File: `19 - ImagenApp.png`

Vendor material, not user voice (OCR is heavily garbled):
- Subreddit self-description: "The official spot for Imagen [...] high-volume photo and video [...] need to end the backlog."
- u/WeAreImagen: "Imagen Studio is out now!" and "Which culling method should you choose in Imagen Studio?"
- Two culling modes shown: "Keep the best of each group — Best when [you] want at least one photo [from each] scene. You stay in control of the details" and "Cull to an exact number — for high-volume projects where you [need] a specific [number] of photos. Not intended for sneak peeks [or] storytelling". Warning text: "By [...] rated, you'll [no] longer get at least one photo from each group." [unclear OCR]
- Profile Shop prices visible: "US$250", "US$197".
- Relevance: Imagen itself concedes that culling to a target count breaks the "at least one photo per moment" guarantee.

---

## 9. "Tips for culling ~10k photos after a long trip?" — r/photography, 1y ago
File: `19 - Tips for culling ~10k photos after a long trip r photography.png` (OP u/turalaliyev, hobbyist; 74 comments). Mostly hobbyists; manual-method evidence, no AI tools named.

**Photo Mechanic — praise**
- henryrodenburg: "Most pros I know use photomechanic to cull."
- IntensityJokester (hobbyist): "Best purchase ever! Loads pics fast, helps me move through the culling process quickly, makes it easy to batch caption and rename."
- Affenbein: "Photo Mechanic is the best software to select/sort your photos, in my professional sports bubble everyone uses it to sip through thousands of photos every other day."
- curiousjosh: "I'm a pro too. It's the choice of champions."

**Free tools**
- 5hoursawk: "Try FastStone Image Viewer. It's free and I can scroll through photos faster than I can review them with no loading or waiting time."
- Others: IrfanView (ganajp), Adobe Bridge, Capture One, Lightroom P/X flags, Apple Aperture auto-stacking by time ("Aperture will auto-stack images based on time between them, which I find useful if I was burst shooting" — Disastrous-Focus8451).

**Method: "cull in", and imperfect photos that still matter**
- Grouchy_Reserve_4860: "The best advice I once got was to switch the mindset of not getting rid of the bad ones, but to pick the good ones."
- TreJ: "Make sure that you tell the story of your trip with the photos. That might mean that some blurry or imperfect photos make the cut because they might remind you of something fun that happened."
- docherself (pro): "if there is very slight motion blur/handshake it will get culled. if it involves people and if they look unflattering in any way it gets culled. [...] if i have multiple good shots with none of the problems above i pick the best one of the lot".
- TinfoilCamera: "make a backup of the images before you start. [...] your fingers might decide to press delete on an image you wanted to 'next' and keep." / "when in doubt, next it and keep it."
- Fun_Inspector_8633: "I've gone back and found some 'diamonds in the rough' later".

---

## 10. "Editing Hangover: How do you deal with wedding photos?" — r/WeddingPhotography, 3mo ago
File: `20 - Editing Hangover How do you deal with wedding photos r WeddingPhotography.png` (OP u/Warm-Elderberry-7665, German part-time wedding photographer; 21 comments)

**OP's pain**
- OP: "I cull very heavily and only deliver the images that I genuinely feel are worth keeping. But getting from, say, 2,500 shots down to the final gallery takes me FOREVER."

**AI culling refused (recent, 2026)**
- davispw: "Absolute no AI culling. It is garbage. The ONLY use I can see for it is if you need to quickly pick 5 shots for a 'Sneak Preview'. There are too many false positives and false negatives so you WILL have to go back through the whole shoot yourself, which will take MORE time."
- Weak-Bumblebee9978: "I don't use AI for culling, I do it by hand with photo mechanic. Usually takes me a couple hours to cull a big wedding and I'm also an over shooter, but AI just missed too many images the one wedding I tried it on."
- [username lost in OCR]: "my biggest pieces of advice are not to use AI culling. Just turn on a show or podcast, move through the previews as fast as you can and 1 star the ones you like".
- davezaplephoto: "I don't use AI for culling. A fast program like Photo Mechanic or the soon to be released Shot Safe for backing up and culling helps loads! I've also linked a PlayStation 5 controller to my laptop to make it easier/gamify the process a little. [...] Usually deliver around 10% of what I've actually shot on a full wedding day."

**Narrative Select — used only as a fast viewer, AI ignored**
- FilmCameragirl: "I have come home from weddings with 6000 photos to cull (when I first started out). I started using Narrative to cull my photos maybe 2 years ago. There is an AI feature where you can just look at Narrative's picks. But I don't use that and I don't find it helpful. I literally only use narrative because I can get a close-up of the face at the same time as the full image and it cut down my culling time significantly. When I was culling in Lightroom, a wedding might take two days to cull. Now, a wedding will take about 8 hours or less. But I do put eyes on every single image."

**Aftershoot — mixed**
- Terrible Document 20: "After Shoot and a fast computer. I deliver full galleries 3-4 days after each wedding! 700-1200 images typically." / "I use the Pistachio preset [...] Have done the last 60 weddings that way and everyone loves it!"
- Remarkable-Pian07284: "I cull either in Aftershoot or Photo Mechanic. Sometimes, Aftershoot is really good for culling and others, it's not. When that happens, I go to Photo Mechanic. But for editing, it's all Aftershoot."

**Other**
- togDoc: "Outsource it. I can't stand editing anymore. Unless it's a nice wedding".
- FunkyTownPhotography: "I use photo mechanic because its fast at previewing raws. I do two rounds. I cull 'in' first round [...] Then I take those images and go back through them... usually backwards chronologically... and cull 'out'".
- YourMajesty90: "2500 is not 'a lot'....in fact you might be undershooting unless these are 6 hour weddings...."
- Big_Rip4015 (contributor to Mac app Palomino — vendor, self-disclosed): "do the first cull off the embedded JPEG preview in each RAW instead of waiting on a full render per image. [...] I contribute to a Mac App called Palomino".

---

## 11. "Exhaustion from culling photos" — r/photography, 2 days ago
File: `20 - Exhaustion from culling photos r photography.png` (OP u/Frosty1397, hobbyist; 147 upvotes, 209 comments)

**Fear of losing a good shot to an algorithm (the core trust objection)**
- Perfect House2143: "AI culling is a thing these days". OP Frosty1397: "I'm afraid to delegate the culling process to an algorithm. What if it deletes ones that are good?"
- barefut_ (about Mac app Fovea): "How does it help you? If it's AI choosing for you, it can be tricky".

**Decision fatigue from near-duplicates**
- OP: "These could be photos that are basically the exact same (from a burst sequence) but might differ by like a millimeter [...] So now i gotta flip back and forth deciding which to keep: A, B, C or D. Then repeat that 50 more times, next thing it's 4 hours later and my brain's pulsing from decision fatigue".
- geo_walker: "I'll try to cull photos and don't want to delete the mediocre ones in case I like them later. I just end up with semi culled projects and the photos usually don't get edited or shared."
- Halfang: "Don't do what I do and 'keep that ok photo just in case someone asks if I have a photo of that very specific thing [...]' times 2 billion".

**Wedding volume is the hard case**
- the-reoccuring-lemon: "600 shots? Try culling 3000+ from a wedding. I dread post production."
- silverarrrowamg: "to be clear culling 10k racing photos is easier than 3k wedding photos".

**Photo Mechanic — praise with numbers**
- sheldoneousk (sports shooter): "Usually come home with 1000-5000 shots a night. Photomechanic has been a life changer for culling photos." / "I used LR to cull until September of this year. I can get through 1000 photos in like 15 mins with PM if I don't have interruptions. Previously would take hour + in Lightroom. There is 0 lag or loading time once the photos are in PM".
- landofcortados (former sports photographer): "For photojournalism work it was the industry standard forever. [...] It also seems to build previews of images faster than lightroom, capture one, or bridge ever seemed to."

**Manual methods**
- Luckyth13teen: "Get a video game controller [...] completely changed my dislike of culling, and honestly sped me up considerably."
- Disastrous-Chair-007 (birds): "I can go through 1000 images in about 10 minutes."
- GoodAsUsual (Lightroom colour labels at weddings): "RED might be pictures of only the bride and groom; YELLOW might be group photos; GREEN might be candids".
- bdgbill: "Eventually, your reluctance to face the growing mountain of photos that need culling can make you walk away from the hobby forever."
- Few Mastodon 1271: Steve Perry "reviewed a big set of 4000 photos in an hour."

---

## 12. "I don't have a large enough profile to use Imagen AI to batch edit, and I have 3500 photographs from a previous wedding" — r/WeddingPhotography, 3y ago
File: `20 - I don't have a large enough profile to use Imagen AI to batch edit, and I have 3.png` (OP deleted; 33 comments)

**Training-data barrier (cold start)**
- Title itself: OP cannot use Imagen because the profile needs more edited images than they have.
- scottwyden (**Imagen employee**, self-identified): "Scott from Imagen here. 3,000 is our minimum so you should be good to go. Your other options are to create a profile based on a Lightroom preset which we call Lite Personal AI Profiles, use our available Talent AI Profiles".
- [username lost in OCR] (3y): "Hey there! I started with Aftershoot, and it required me 2500 images to create a profile." [cut off]
- Workarounds people suggest — a sign of friction: DengleDengle: "Upload the 3500 photos twice"; [deleted]: "Batch flip them horizontally and upload the second 3500 as new training images."; Weddingbean: "You can upload the same gallery multiple times to hit the requirement."
- lazysundays: "Gosh you haven't edited enough to warrant using an AI product just yet!"

**Pricing**
- Weddingbean: "Not a fan of imagen ai, too pricey for anyone doing volume. I've really loved neurapix [...] $50 a month and it's gotten my style down to a science. I was paying close to $200 or more with imagen a month between 4 or more weddings." Also: "my little edit bot cuts about 10 hours of editing down to around 2 or three for a full 700+ wedding gallery."
- OP: "$200 is way too much for me especially for someone who does not have dozens of weddings booked."
- dockerinspect (about Neurapix): "Do you still have to buy each SmartPreset from their store separately after paying the $50/mo fee?"

**Resistance to AI**
- thebahle: "Why is everyone trying to cut corners with ai when we've been using tried and true workflows for years".
- Chrisser6677 (manual culling): "Its the best 2 hour video game you can play. Get that gallery down to 400".

---

## 13. "Any advice for those who are too busy? Feels like I'm drowning" — r/WeddingPhotography, 5y ago
File: `21 - Any advice for those who are too busy Feels like I'm drowning r WeddingPhotograp.png` (OP deleted)

**Backlog numbers**
- pspetrini: "I was current and had an empty queue on July 31st. Now I'm 31,000 photos behind (literally.) It happens." / "This is the busiest year I have ever had and I've been doing this for over a decade."

**Outsourcing (editing services) — praise**
- Wh1skyJack (15+ years pro): "professional editing companies are VERY good at editing. After a few weeks of back and forth with them about what I was looking for in an image edit, they could make an image have my look faster and more consistently than I could. [...] For reference I use Shoot Dot Edit".
- sivasee: "Outsource your editing. I was with Shoot Dot Edit for over a year and they were really good, or even better get an editor on staff [...] Lets be honest, editing sucks ass!"
- waimearock: "The times I've been too busy and I had to outsource I always looked over the work that the editors did and adjusted anything so that it would have my look to it."

**AI tools — praise**
- [username lost in OCR]: "aftershoot AI for culling and imagen AI for editing is saving my life this year. might slow you down at first as you get used to a new work flow but i'll never work without AI again."

---

## 14. "Any thoughts on AI/batch editing? Currently looking at Batch AI and Imagen AI" — r/WeddingPhotography, 5y ago
File: `21 - Any thoughts on AI batch editing Currently looking at Batch AI and Imagen AI r W.png` (OP u/Snoo-19679; 26 comments)

**Imagen — mixed**
- ThankfulFox: "I like Imagen AI but I'm amazed it's saving people so much time. It doesn't save me that much - it only applies your look (preset) and makes small changes to white balance and exposure etc."
- evphoto: "I was a big fan in the beginning, not anymore though."
- evanrphoto: "I would say it probably reduces around 70% of my editing time for a wedding [...] You can also look into AI culling like Aftershoot but that doesn't provide anywhere near the time savings for me that IAI does."
- pb_and_banana_toast: "It's not going to replace a good human editor, but if you upload enough for a solid profile it will cut your editing time down 50-70%."
- FrostyPhotog: "[Imagen] is stellar, but you need at least 5k similarly edited photos to build your profile."
- [deleted] (4y): "Waste of time. You end up spending 3-4 hours reviewing and making adjustments to the AI's edits. Human editors are a far better use of money."
- NYmadlad (1y, on posted before/after samples): "its crazy how I was amazed by the original instead of the edit."

**Local vs. cloud, flat vs. per-image pricing (from a likely promotional account)**
- Maddface (posted "7mo ago" into a 5-year-old thread, three long pro-Aftershoot comments, offers to "point you to the FB Aftershoot community" — **reads as vendor/ambassador promotion; flag**): "I ended up with Aftershoot because it is like $500 for the ENTIRE YEAR for unlimited culling, editing and retouching!"
- Maddface: "it's fully local (runs on your computer), so I don't have to upload galleries or rely on internet, which is huge when I'm traveling or working on the go" / "because it's local, there's also a bit more peace of mind with files staying on your machine" / "pricing is flat (monthly or annual) instead of per image, which made a big difference for me during busy season".
- Maddface on Imagen: "if I am paying per image, I would have rather kept paying for an editing [service] for $0.10/image more and have it 100% done."
- Even if promotional, it shows which arguments the market leader uses against Imagen: local processing, no upload, flat price.

**Vendor / referral flags**
- scottwyden (Imagen employee, see thread 12): "Definitely Imagen - they created the category of AI photo editing, and the others are trying to [follow]. Imagen also just announced AI culling in the works."
- heatherkan: posts an Imagen "Referral link to get more free edits".

---

## 15. "Does anyone prefer to do weddings solo these days?" — r/WeddingPhotography, 4y ago
File: `21 - Does anyone prefer to do weddings solo these days r WeddingPhotography.png` (OP u/patriotraitor; 33 comments). **Key multi-photographer thread.**

**Second shooter = extra culling/editing work**
- Filmandnature93: "However I just end up with so many photos that I never use, I believe more than 90% of the second's photos are rejected which makes me think."
- floobenstoobs: "I'm a huge fan of working solo and don't like the extra work I get with editing a second shooter's almost identical view points."
- X4dow: "I prefer shooting with company/backup peace of mind. But much easier to edit 1 shooter weddings. Specially video".
- EverythingBagelLife: "I don't need to worry about where/what someone else is doing and editing is more straightforward."
- [deleted] (11 years in industry): "the shooters provided unfocused/blurry images and most were not usable. [...] the images they handed over weren't properly exposed or focused [...] I'm shocked they handed over so many blurry images with incorrect focusing..."
- OP: "usually just ends up being just different angles of poses I've got that look better, very seldom has a second saved my butt with a misfocus".

**But the market demands it**
- floobenstoobs: "I've recently added a package with a second shooter because the market calls for it. Clients want a second photographer whether or not it matters - they are under the impression that they will get more."
- Prestigious-Iron2699: "with weddings that are spread out and at different locations as well as over 150 people I'd highly recommend [...] a second shooter. Especially if shooting a South Asian wedding. Too many traditions and little things happening that require capturing."
- doeydoey76: "I like a second especially if the other shooter is doing close ups versus your wider angles."
- zeezeepants: "70% of my weddings this year was solo"; ny_AU: "I do 90% of weddings solo".

---

## 16. "UK wedding photographers. Who is still editing?" — r/WeddingPhotography, 2y ago
File: `21 - UK wedding photographers. Who is still editing r WeddingPhotography.png` (OP u/StrikingPainter455; 46 comments)

**AI culling still needs control**
- josephallenkeys (on Imagen/Aftershoot, trained on "around 10k images from my back catalogue"): "I found the culling still needed controlling but the edits, once I really stacked up the reference library for it to learn from, were basically flawless."
- redrabbit1977: "Wildernis Lab. It's ai + humans so you don't have to fix and tweak every image like you do with imagen/aftershoot. They also use humans for culling, given that ai completely sucks at culling." (repeat recommender of this service)
- dylansluna: "You still have to make many decisions and train ai with your vision. You still have to go through every single photo. It's just a tool."
- OP on Imagen: "It was good but I was still having to put a lot of work in."
- redrabbit1977: "It's a starting point only. Anyone that says it's a perfect solution delivers bad edits."

**Vendor voices**
- SetReasonable5825 (**Aftershoot co-founder**, self-disclosed): "I'm biased as the co-founder of Aftershoot but it really does make delivering galleries on time way easier for me. I'm down to about 3-4 hours of manual work per wedding. That's like 1 hour reviewing culling and 2-3 hours of reviewing editing and photoshopping." / "The key is to just keep training! Ai is only as good as the energy you put in to making it work like you!" — note: even the co-founder spends ~1 hour reviewing the cull.
- [username lost in OCR], addressed as "Sam" by Foam099 ("I still need to try yours Sam, wedding incoming this Saturday for first trial"): "there's good ai culling out there..." — a tool developer promoting own product.
- redfishgoldy: "imagen saves me so much time, I use it for culling too. Use my code 'georgia' for a discount" (affiliate code).
- Sad-Ad377 (1y; list-style post ending in an outsourcing recommendation — likely promotion): "Imagen AI — speeds up editing by learning your style, but still needs some fine-tuning. Narrative Select — great for culling, but not full editing. Photodotedit — if you want full outsourcing, they're solid."
- Happy-Strawberry-748: freelance editor soliciting work.

**Praise**
- RaspberryOrganic3783: "Imagen has been a game changer for me". Frazier10k: "Same! went from stressful wedding season to very manageable."
- WeDoItForFunUK: "Anything over 200 images and the robot does it. When I say it I mean the grunt work white balance, straighten, manage highlights, a light grade. Then I double check and spend some time on the hero images and b&w. [...] I use imagine. It's ace."
- Mountain-Theme-7792: "I've started using AI editing tools like Aftershoot and it's helped take a lot off my plate. It's not perfect, but definitely saves time on the bulk of the work."

**Refusal on principle**
- navigator87: "I feel using this type of AI removes the human connection from something so intimate and intentional. [...] I'd totally use one of them for corporate jobs [...] But not something so personal and important as a wedding."
- [deleted]: "If everyone is saving time and energy with AI doing the heavy lifting are you guys lowering your prices?" WeDoItForFunUK: "Of course not. They're getting my experience, quality control, taste, and guarantees."

---

## 17. "Culling, or how not to lose your mind?" — r/AskPhotography, 2mo ago
File: `22 - Culling, or how not to lose your mind r AskPhotography.png` (OP u/DeltaPapaWhiskey, motorsport, part-time; 146 comments). No AI tools discussed; manual-culling pain and numbers.

- OP: "right now I'm sitting on about 3500 photos from a 2 days of shooting"; "it takes me at minimum a couple of weeks to cull and edit one weekend's event, usually longer."; "Computer takes a few seconds to go to the next frame".
- OP's summary of the advice: "Cull ruthlessly, only two passes, edit & done. Secondly, use Photo Mechanic to cull faster".
- jeeperjalop: "For the big events, over 7 days, I'll get roughly 17-19k shots."
- OpportunityReal2767: "I cull in Photo Mechanic. Blazing fast compared with Lightroom. Hardly any lag from one photo to the next."
- slash153 (tool overview with pricing remark): "photomechanic - win/mac, monthly sub or expensive perpetual, photoculler - mac only, cheap and perpetual, FastRawViewer - few bux but more or less only viewer with ranking". Also: "this way I can blast through a set of 1-5k photos in few mins and narrow it down to 100-600."
- Mediocre_Spell_9028: "Lightroom is notoriously slow, especially on Windows [...] it feels like I'm working on a laptop made in 2005 when I pull Lightroom out".
- feelxrosic: "Better get the shot and do more culling - this is the way. Better safe than sorry!"; "For 3500 photos that would only take me 1 hour max".
- Overread2K: "A pro is expected to deliver much more today than in the past [...] If you're chimping you're missing shots".
- Latter_Drawing_5224: "It not free if it's costing you time culling after."

---

## 18. "Imagen.ai" — r/RealEstatePhotography, 2y ago
File: `22 - Imagen.ai r RealEstatePhotography.png` (OP u/SWEDISH_M4N)

Editing only, other niche — brief:
- tankminder: "thus far I'm not super impressed. [...] I still find I need to do a lot of tweaking of its output. In fairness I didn't upload the 'recommended 3000 edited pictures' or some silly number for it to build its most robust model. I uploaded more like 20-30".
- boothatwork: "Best AI editing tool out. [...] it's like 90% there. The best part is that it edits them in Lightroom classic for you, so you can adjust things yourself after."
- Adjusterguy567: "My wife and I use it for our wedding galleries and it's great".
- OP: "I keep getting ads from imagen.ai on instagram." (heavy ad spend noted)

---

## 19. "do you actually enjoy editing or is it just damage control?" — r/WeddingPhotography, 1y ago
File: `22 - do you actually enjoy editing or is it just damage control r WeddingPhotography.png` (62 comments)

**Culling is the hated part**
- Upsidedown0310: "I don't mind editing but I HATE culling."
- GimmeDatSideHug: "I hate culling, but I enjoy making my photos look like bangers."
- CapCityPhotos: "I love editing. It's my favorite part of the post shoot workflow. Culling is another story.."
- Counter-view — Phounus: "I find culling fairly relaxing and goes by pretty fast, even for big weddings."; kuzumby: "I love sorting, culling, and editing almost as much as taking the photos."

**Aftershoot / Imagen fell short**
- u_matter_to_someone: "I tried after shoot and imagen and they fell short for me, wasn't happy with either one so I cull and edit myself, takes a bit of time but in the end it's worth it."
- kuzumby: "I found AI culling and editing doesn't even come close to what I want."
- OP: "i batch with imagen [...] but the second i open lightroom i still feel like i'm putting out fires."
- ylime114: "Otherwise it just takes 8+ hours for one wedding AFTER imagen."

**Unmet need: ordering / curation / story**
- ylime114: "What I don't love as much as editing that I spend a lot of time on is curating/organizing the photos in a way that makes the most sense and tells the best story of the day. I don't even do the first cull, but making sense of the photos as a whole is what takes me the most brain power. [...] the organization & final curation is a slog".

**Refusal on artistic control**
- jordantbaker: "Will I sub the editing out to AI because of that? Also no. I want my fingerprints to be present in the product as much as possible."
- Aeri73: "so no automation or AI for that, ever".

---

## 20. "AI Photo culling vs manual culling programs" — r/AskPhotography, 4y ago
File: `23 - AI Photo culling vs manual culling programs r AskPhotography.png` (OP u/SeekTheLightPhotos, event photographer; archived)

- OP lists the field: "AI Culling: Aftershoot, Narrative Select, Imagen AI, FilterPixel, Optyx, OptiCull (aka Dope AI aka Cull AI 2.0). Manual Culling: Photo Mechanic, Adobe Bridge, Fast Raw Viewer". "Culling takes up SO much of my time, (I shoot a lot of events, so thousands of photos every day.)"
- ibetyouranerd (top comment): "They work but you're still gonna find yourself double checking every single photo anyways."
- OP SeekTheLightPhotos (after <2 weeks with Aftershoot): "I have actually really loved Aftershoot for culling. [...] Being able to group the photos together to see up close images that are identical, have them rate them based off eyes closed or focus, saves me SO much time. Yes, I go through damn near every picture just in case, but 80% of the work is already done for me once I go through that final look through."
- IronMan2524: "I have used Aftershoot and ImagenAI but I found Aftershoot to be more user friendly than ImagenAI."

---

## 21. "Culling questions" — r/WeddingPhotography, 2y ago
File: `23 - Culling questions r WeddingPhotography.png` (OP u/elmerwfx; 30 comments)

**Unmet need: reorder and compare**
- OP: "Is there a culling site that allows you move images in a different order? Or to see images side by side to compare? I tend to manually cull in aftershoot and then move images into Lightroom for a second round of culling where I can see them side by side and move all my cake photos next to each other, or all photos of shoes together and so on... but lightroom is slow."
  (Note: uses Aftershoot only as a manual viewer; needs grouping by subject.)

**Tools**
- DesperateStorage: "It actually amazes me when a wedding photographer isn't using photomechanic." / "I've boycotted Adobe for almost 20 years now".
- DirtyWaterPirate2017: "I use Photomechanic for culling. [...] I specifically use the 'cull in' method. [...] I only import finalist images into LR [...] I also tag images in Lightroom with what part of the day they are, such as '01 prep', '02 first look' etc. [...] I got this old Xbox controller from walmart for $10".
- merm1823: "I've really enjoyed narrative for my culling needs!"; NickiD39: "Have you tried Narrative Select? They have the survey mode like Lightroom. I know Aftershoot added the survey mode feature in the past year".
- [deleted]: "It amazes me that people still insist Lightroom is slow. I cull at the exact same speed in LRC Library mode as I do in PM."
- LisaandNeil: "Amazingly, we get by fine with Bridge."
- roccon79 (8mo; a groom, built own tool): "After my wedding we had around ~4k photos to go through. I ended up building a small tool to make the culling process faster. It runs locally in the browser and is open source: https://snapsortr.com" (self-promotion, but shows local/open-source demand)
- the-dagger: points to Aftershoot survey-mode video (possibly affiliated; unverified).

---

## 22. "Questions and Anything Goes (Official Thread)" — r/WeddingPhotography, 4y ago
File: `23 - Questions and Anything Goes (Official Thread) Questions, Stories, Photos, Shower.png`

**Hard numbers on workload**
- evanrphoto: "There is 25-40 'man-hours' directly associated to each wedding plus additional overhead work [...] so something like 25-30 weddings per year is basically a full time job".
- benhowland (asked what stops 80+ weddings/year): "Lead generation and edit time. If someone else did my edits, shooting 80-100/year would be easy. 40 is my target but last year was 60-65."
- ajp233 (student, citing what he read): "I've read that editing usually takes 8-12 hours but could you half that time to 4-6 hours with the use of AI programs?"

**AI culling misses the moment**
- evanrphoto (an AI-editing advocate): "AI editing is very good, and more consistent than my eye across a set/series/wedding. But AI culling really missed the mark on identifying the most powerful moments."
- umwhat333 (second shooter): "the culling programs tend to choose photos I typically wouldn't."; "I know some photographers who will send full wedding galleries the next day, with little to no regard for small details the AI editing software may have missed, making it possible for them to do 50+ weddings a year."
- bad_tichy: "The AP editor views 30000 plus images during a Super Bowl and has the selects ready by the time the Lombardi trophy is lifted. [...] I would never trust it and I can never believe it would be better than a human for delivering on how a photo 'feels'."

**Astroturfing awareness**
- [deleted]: "I feel like the photographers who are 'almost entirely relying on ai' are the ones with a discount code they want you to use."

---

## 23. "Tips for second shooter (but not the obvious ones)" — r/WeddingPhotography, 4y ago
File: `23 - Tips for second shooter (but not the obvious ones) r WeddingPhotography.png` (OP u/WedMannn; 18 comments)

Multi-photographer pain points for the lead in post:
- grimmauld12: "Align with your photographer on expectations - I know it sounds obvious but it'll make the lead's job in post so much easier. Are they a quantity person, or a less is more type person?"
- MundanelyCool: "when people start shooting family formals while I'm shooting them it's more I have to cull through. I don't need copies of family formals".
- MundanelyCool: "I had a SS take like 4 photos of the groom by himself and only two were usable and I had to edit one in photoshop because his collar was messed up."
- MundanelyCool: "I want to rip my hair out when I get photos back and they're all soft focus in the face because they couldn't be bothered to double check the eyes were in focus."
- MundanelyCool: "Check in from time to time to see what their settings are so that your work is cohesive with theirs."
- X4dow: second shooter of 10 years "done hundreds of weddings now".
- (No mention of clock sync in this thread.)

---

## 24. "Culling and gallery redundancies" — r/WeddingPhotography, 2y ago
File: `24 - Culling and gallery redundancies r WeddingPhotography.png` (OP deleted, beginner; 8 comments)

- OP: "I'm going to be editing with Lightroom. I saw it has a culling feature.. so why do people also subscribe to Aftershoot / Photo Mechanic / Imagen? Is the culling much better? Do they offer something else that Lightroom doesn't that makes the subscription price worth it?"
- plantypete: "I use photomechanic because it's quicker. If it's saving me time I will pay the price. It's faster than culling in Lightroom and I'm more efficient than Aftershoot."
- bunnyhunnyy: "I love culling on Narrative and then shipping/importing to Lightroom! It's free but it's just what I prefer! I can't cull that quickly in Lightroom".
- [username lost in OCR]: "i've been using aftershoot! you definitely don't need photo mechanic, ever, unless you're doing highly complex organization with metadata".
- annopano: "I use PM to cull and it saves me sooo much time. Yes it's paid but for me its really worth it."

---

## 25. "Hands up if culling makes you want to stab your eyes out." — r/WeddingPhotography, 3y ago
File: `24 - Hands up if culling makes you want to stab your eyes out. 🤣 r WeddingPhotography.png` (OP u/timwoodphoto; 114 upvotes, 104 comments)

**Pain**
- OP: "I love photography. I love editing. [...] But omg.... Culling makes me want to stab my eyes out. The concentration needed especially on big volumes is beyond me."
- wickedcold: "Culling is the reason I deliver in 8-12 weeks and not like five days."

**Second shooter and camera clock sync (direct evidence)**
- kstinasunflower: "I'm with you, I have 7000 photos for this wedding to go through. My second shooter way over shot."
- mimosaholdtheoj: "Culling second shooter shots is by far worse than culling my own. And an overshooter?? I'll just go die in a corner brb".
- OP timwoodphoto: "Culling a second's work is just as bad, especially if their cam clock isn't synced with yours!"
- (Sidebar shows a related thread title: "Losing my mind editing second sh[ooter]..." — 60 upvotes, 74 comments, r/WeddingPhotography, 2y ago.)

**Aftershoot — praise (blinks/blur) and limits (duplicates)**
- shemp33: "Aftershoot for the win. Is it perfect? No. Can it reliably pull out blinks and blurs? Yes. If the AI training on which duplicate is your favorite isn't there yet, at least the blinks and blurs are really accurate and that saves me a ton of time."
- jtobiason: "Sign up for aftershoot. I was you, but now have a new lease on life."

**AI distrust / cost more time**
- OP timwoodphoto (reply to Aftershoot tip): "I'm a control freak. Ai scares me. Ha ha".
- AnonymouslyObvious5: "I've tried a few of the ai culls, and cost me more time reviewing the mistakes than it would have taken had I just done the cull."

**Photo Mechanic — praise**
- defeldus: "Ever since switching to photo mechanic it takes me 1/4 of the time and 1/10th the stress."
- PhotographerRex: "Photo Mechanic, its still culling, yes it lets you go as fast as a human can possibly cull."

**Outsourced human culling**
- redrabbit1977: "I star my favourites throughout the day [...] I have about a 100 keepers by the time I get home. Then I send the wedding to Wildernis Lab (their hybrid ai option includes human culling and only costs $120). When I put my order in I have them cull to about a hundred shots more than I will deliver [...] This gives their human cullers a bit of wriggle room, so they can keep some duplicates that they can't decide between. It's not a perfect system but its super fast & cheap".

**Manual habits**
- Mercuti0999: "I have my hand on two buttons and look at each photo for about a second. I go with my gut".
- alexjohnsonphoto: "cull as soon as you can following the wedding day [...] all the shots are fresh in my mind".
- DesperateStorage: "Personally I think culling is my favorite part of the wedding".

---

## 26. "How to not overshoot?" — r/WeddingPhotography, 1y ago
File: `24 - How to not overshoot r WeddingPhotography.png` (OP u/hillsong1; 65 comments). **Best source of shot/deliver numbers.**

**Why people overshoot: fear of missing the moment**
- OP: "I find it a good practice because this minimizes the missed moments and there are a lot of cases where I was glad I did it. On the other hand culling 8k images is a lot to go through, I need a day and a half to cull it all".
- josephallenkeys: "Just overshoot. No one ever looked back at a wedding and said 'ah, I messed that up because I overshot!' Better to have the extra work than crushing disappointment in yourself."
- frolickingorca: "You miss all the shots you don't take. It's worth culling for longer knowing you captured the exact right moment."
- Old-obligation7421: "Yeah the culling sucks but missing the bride's reaction during vows because I was trying to be 'selective' would suck way more."
- minaret_photo: "I end up spending a lot more time culling but the nuanced moments you can get from 'shooting the sh!t' out of an important part of the day can truly pay off. This doesn't work if you're shooting 75 weddings a year though."
- InternationalSky7598: "I will shoot probably 5-10 shots of group photos because inevitably someone blinks or is talking."
- FunkyTownPhotography: "One of the best international photo teams - Two Mann - overshoot. [...] Overshooting is the secret to success for a lot of us." Also: "Imagen's culling service is cheap and is another thing to try."

**Numbers: shot vs delivered (see summary table)**
- Terrible Document 20: "Pro shooter with over 1,000 weddings done, almost all solo. I do less than 2000 photo per wedding. Typically 1400 on average. [...] Then I cull down to about 700 perfect photos [...] I have other photographers that shoot for me and they take way too many photos [...] I have to cull out 80% of it as they are not good."
- magwestphoto: "I also end up with about 1400 for an 8 hour wedding. [...] I deliver between 900-1100 photos captured across my entire team for an 8 hour wedding."
- palinsafterbirth: "I also tend to end up with 8-10k at a wedding between myself and my assistant. Honestly, I have never heard a client say 'we wish you photographed less'."
- CommercialShip810: "My personal record is 3200, with most weddings coming in around 2500. And this is a lot more since the days of DSLRs. Then I would average about 1200."
- Guitar74 47: "I get home with 8k shots on regular basis, but I get 14 hours weddings here".
- Bomzeetit: earlier style "around 1.5k - 2k per wedding"; now "I shoot 5k-8k."
- ylime114: "My partner and I shot 12k photos across 12 hours last Friday evening + Saturday [...] We'll get that down to 1500ish on the first cull then closer to 1200-1300 unique photos before delivering".
- ylime114: "I just delivered a wedding that was 7 hours of coverage and they had about 600 unique photos."; "I also make sure there are 100-150 photos flagged as 'highlights'".
- KariBjornPhotography: "I'm around 4-5k (6-7k with 2nd shooter) for a full day and I cull three at a time."
- dreadpirater: "I shoot about 4:1 or 5:1. So on a typical wedding, I'll click 2000 to 3000 times and deliver 500ish images."
- InternationalSky7598: "The most I've ever had to cull was 5k because it was a 10 hour day with a second shooter and it was A LOT for me. I prefer around 3k photos max for culling and tend to deliver around 600-800 photos for a wedding day."
- u_matter_to_someone: "Going home with 5-7k images on 2 bodies was exhausting to cull and edit and I would regularly export around 1.5k and 2k images [...] Now I shoot around 2.5k and 2.9k images and cull, edit and export max 800 images."
- LiterallyUrDad: "I was shooting for a service, and they wanted 100 photos per hour delivered. So for an 8-hour wedding, I would need to deliver 800 photos." / mirrorless at 20 fps pushed him to "3,000-5,000 shot range".
- efoxp13244: "I end up with around 10-20% of great photos to send to the client."
- Old-obligation7421: "I usually end up around 2-4k"; wokeisme2: "now I keep it to around 1500 or so after 6-8 hours"; -shandyyy-: "If I hit 2500 at a wedding I am annoyed at how much culling I have to do"; tohpai: "Mine is 4k and that's already a lot"; Upsidedown0310: "My record is 10k".
- oh_my_ns (client-side view): "I cannot imagine having a need for 1200 photos of my wedding day. Do people actually want that many?"

**Aftershoot — double-cull risk, referral**
- superduperburger81: "Alternatively you can use something like Aftershoot to reduce your initial cull down by 50% but it may remove images you would actually want, so you'll have to kind of cull twice as you start to see if it does a good job narrowing things down for you or not."
- AppropriateShirt8529: "Then look into AI culling with Aftershoot and you'll only have to manually cull through a fraction of your photos. Here's a 10% off link if you want to try it" (**referral link — interested party**).

**Indie tool promotion**
- Old-obligation7421: "I've been using Cureyta.com lately which has helped a ton with the culling nightmare. You can actually describe what you're looking for like 'ceremony shots where both bride and groom are visible' instead of just scrolling through everything mindlessly." (Cureyta's creator posts under another name in thread 5 — possible promotion; shows a wish for semantic search/filter.)

**Manual technique**
- KariBjornPhotography: "I'd rather have to go through 75 photos to find 3 great ones vs pulling a few images from 15-20".
- superduperburger81: "If the composition is where you want it for a series of bursts, I'm just looking at facial expressions because that's the thing that can change in an instant."

---

## 27. "Is 2 photographers necessary?" — r/weddingplanning, 3y ago
File: `24 - Is 2 photographers necessary r weddingplanning.png` (OP u/NoCaterpillar392, bride; 21 comments)

Client-side demand for two photographers (context for the multi-camera claim):
- anna_alabama (bride): "While my photographer was taking photos of me walking down the aisle from the front, the second shooter was taking photos from the back. [...] I loved getting a gallery of 1,000+ photos back and would have been super upset if any of them were missing."
- [deleted]: "When someone is walking down the aisle one photographer gets photos of the person walking and the other gets the person at the altar's reaction." (same moment, two cameras)
- Thresholds quoted: mackarie "100 was like the cut-off point"; juliaffe "recommended a second shooter if our guest count exceeded 150"; Waste-Carpenter-8035 "I had just one with 150 guests! I still got a ton (1000+) amazing photos."
- OkOne2171 (photographer, 15 years): second shooter as insurance — "If there's a second shooter, he/she can take over the role of the lead photographer."

---

## 28. "Have you ever felt this way about editing a wedding?" — r/WeddingPhotography, 2y ago
File: `25 - Have you ever felt this way about editing a wedding r WeddingPhotography.png` (OP u/Frosty-Apricot-8304, first wedding as lead; 95 comments)

**Grouping helps even without auto-picking**
- readyforachallenge89: "I realized it was because I'm an overshooter and the culling process was very tedious. Now, I use a culling software to help me group similar images together and for some reason the groupings make me feel less overwhelmed."

**Workflow and numbers**
- OP: "I did 8 hours of coverage and saw other photographers advertise that they deliver 800 photos for 8 hours, so that's what I offered and am contracted for... but I have a feeling it's just overwhelming me."
- Complete-Mechanic907: "I will say about 75 images per hour of coverage".
- esotericunicornz: "I wouldn't promise 800 photos tho, 100 per hour is too much imo".
- EcstaticEnnui (15 years full time): "I do an initial cull, a second cull, first edit with imagen and a final tweak, each of these steps takes me a day, and usually the final tweaking is more like 2 days. (Not 8 hour days mind you but I find if I edit for more than 2-3 hours I start to lose it)."
- [deleted] (14 seasons): "Backlogs and timely deliveries are always in conflict if you don't have a refined, expeditious, efficient workflow." / "With the advent of mirrorless cameras and AI, the race to the bottom is real in a saturated market".
- Upsidedown0310: breaks the job into "culling each 'section' of the day (getting ready, ceremony, portraits etc) and then editing each section."

---

## Batch summary

### 1. Complaints per competitor (ranked by how often they appear in this batch)

**Aftershoot (culling) — about 15 distinct complainants, the most-criticised tool**
1. Wrong ratings / rejects good, keeps bad (most frequent): Commercial_Foot3145 ("5-star that is out of focus and super dark... perfectly sharp... as a 1-star"), thefrenchdev ("discarding good pictures and selecting bad ones"), [deleted] ("It would literally delete all my favorite photos"), ConstructionSma11979 ("weird ratings"), michael_jonny (competitor: "not very accurate"), Remarkable-Pian07284 ("Sometimes... really good... and others, it's not").
2. Still have to check everything / cull twice: Commercial_Foot3145 ("Always. Every single time."), superduperburger81 ("cull twice"), SeekTheLightPhotos ("I go through damn near every picture just in case" — a fan), AccomplishedSir535 ("I always go thru the cull to make sure" — a fan), LarryAndHisCats ("double check the cull" — a fan), Aftershoot's own co-founder ("1 hour reviewing culling").
3. Lost an important shot: Thin_Register_849 (group photo missing from delivered gallery; couple asked for it).
4. No real time saving: plantypete ("no faster than me as a human"; "I'm more efficient than Aftershoot"), evanrphoto ("haven't found Aftershoot very useful"), u_matter_to_someone ("fell short"), 444rj44 ("tried AS, deleted").
5. Ignores artistic intent / cannot tell intentional blur: thefrenchdev ("not giving any credit to the artistic aspect"), LarryAndHisCats' explanation that it cannot know intent and ignores exposure.
6. Needs training over several weddings / profile size: LarryAndHisCats ("4 or 5 weddings"), "required me 2500 images to create a profile", co-founder ("just keep training!").
7. Duplicate choice weak: shemp33 ("If the AI training on which duplicate is your favorite isn't there yet").
8. UI/loading: "file categorizing is confusing... not all my images were added".
9. Makes you lazy / worse: Thin_Register_849.

**Imagen (editing, culling since ~2022) — about 12 complainants**
1. Large training profile needed (3,000–5,000 edited images) and slow upload: overconfidentquartz, ServiceB4Self, FrostyPhotog, the whole "not a large enough profile" thread, OP awkwardlyalexa, tankminder.
2. Billing surprises / minimum monthly fee / refunds / support: user 467 ($7 minimum introduced after signup), Civil_Priority3736 ($131 charged, "Customer service is ridiculous"), Active_Asparagus_952 (studio, "regret doing so greatly").
3. Price at volume: Weddingbean ("too pricey for anyone doing volume", ~$200/month for 4 weddings), OP of thread 12, Maddface (per-image vs flat).
4. Still a lot of manual work after: StrikingPainter455, [deleted] ("3-4 hours reviewing"), ylime114 ("8+ hours for one wedding AFTER imagen"), ThankfulFox, evphoto, u_matter_to_someone, thread-19 OP ("putting out fires").
5. Cloud upload round-trip: donatedknowledge ("save, upload, wait, download, and double-check while paying for it").
6. Suspected undisclosed promotion; heavy Instagram ads.
7. Own culling: Imagen's "cull to an exact number" mode no longer guarantees one photo per group (vendor's own text).

**AI culling in general (no tool named) — about 15 voices**
- False positives/negatives force a full re-check: davispw, AnonymouslyObvious5, ibetyouranerd, noblankish, dylansluna, webguynd.
- Misses moments/emotion: evanrphoto, Weak-Bumblebee9978, No-Neighborhood-2109, redrabbit1977, bad_tichy, umwhat333, kuzumby, the computer-vision developer in thread 3.
- Fear of losing a good shot / control: Frosty1397, timwoodphoto, navigator87, jordantbaker, bugpfeifee, thefrenchdev, [deleted] ("absolutely useless for weddings").

**Adobe Lightroom (incl. Assisted Culling)**
- Slow for culling, especially on Windows: OP of thread 21, Mediocre_Spell_9028, Lightroom_Help, sheldoneousk (1 hour+ vs 15 min), FilmCameragirl (two days vs 8 hours), bunnyhunnyy. (Disputed by several: "can be set up to work exactly the same".)
- AI culling: "I haven't had much success with Lightroom's culling" (No Parfait 2104); "doesn't really solve 'running slow' problem" (Jazzlike Diamond 441).

**Narrative Select**
- AI picks not used / not helpful (FilmCameragirl); "separate program... unnecessary" (CommercialShip810); "didn't wanna just do simple stuff" (michael_jonny, competitor).

**Photo Mechanic**
- Only complaints are price ("monthly sub or expensive perpetual" — slash153; Cullibrate founder pitches "1/5th the price") and "you definitely don't need" it. No AI.

**OptiCull (indie)**
- Mac-only, crash, 20 GB memory, face detection misses small/background faces, scenes not merged, order-by-capture-time problems.

**Outsourcing / editing services**
- Slow and costly (Erick_oseguera: "kind of expensive... one or two weeks and I had to make a final retouch"); need weeks of back-and-forth to learn the look (Wh1skyJack); still must review (waimearock).

**Second shooters as a "competitor" to solo simplicity** — see section 3.

No substantive user comments on **FilterPixel** beyond one positive, on **Optyx** (name only), or on **Evoto** beyond one positive late comment.

### 2. Praise per competitor

- **Photo Mechanic** (most consistently praised; ~15 voices): "1/4 of the time and 1/10th the stress" (defeldus); "1000 photos in like 15 mins" (sheldoneousk); "Most pros I know use photomechanic to cull"; "industry standard forever".
- **Aftershoot**: "has been a miracle" (LarryAndHisCats); "saved me hours on every gallery" (AccomplishedSir535); blinks and blurs "really accurate" (shemp33); "80% of the work is already done" (SeekTheLightPhotos); "new lease on life" (jtobiason); galleries in 3–4 days (Terrible Document 20); "saving my life this year" with Imagen. Local processing and flat ~$500/year (Maddface — likely promotional).
- **Imagen (editing)**: "from around 16 to 2 hours per wedding gallery" (royal_friendly); "reduces around 70% of my editing time" (evanrphoto); "50-70%" (pb_and_banana_toast); "~$30 a wedding"; "game changer" (several); "scary how good it is" once trained (slandoe).
- **Narrative Select**: face close-up next to full image cut culling from two days to ~8 hours (FilmCameragirl); "It's free" (bunnyhunnyy); survey mode (NickiD39).
- **FilterPixel**: small, responsive team (ckisela).
- **Evoto**: more reliable on sharpness/exposure, flags blinks/blur (ConstructionSma11979 — possible promotion).
- **Neurapix**: $50/month flat, cut ~10 h editing to 2–3 h (Weddingbean).
- **Shoot Dot Edit / staff editor**: "faster and more consistently than I could" (Wh1skyJack, sivasee).
- **Wildernis Lab** (human culling + AI edit, $120/wedding): "super fast & cheap" (redrabbit1977 only; repeated in three threads).
- **Free viewers**: FastStone, IrfanView, FastRawViewer, Bridge.

### 3. Multi-photographer findings

- **Clock sync is a named pain**: timwoodphoto — "Culling a second's work is just as bad, especially if their cam clock isn't synced with yours!" (thread 25). PhotoKada reports capture-time sorting throwing "a sequence of photos out of order" in OptiCull (thread 2).
- **Culling the second shooter's files is worse than one's own**: mimosaholdtheoj ("by far worse than culling my own"); kstinasunflower ("7000 photos... My second shooter way over shot"); related thread title "Losing my mind editing second sh[ooter]..." (60 upvotes, 74 comments).
- **Most of the second's photos are rejected / duplicates of the lead's view**: Filmandnature93 ("more than 90% of the second's photos are rejected"); floobenstoobs ("almost identical view points"); MundanelyCool ("it's more I have to cull through. I don't need copies of family formals"); Terrible Document 20 ("I have to cull out 80%" of associates' photos); [deleted] ("so many blurry images").
- **Photographers go solo partly to avoid this post-production cost**: X4dow ("much easier to edit 1 shooter weddings"), EverythingBagelLife, floobenstoobs.
- **Yet clients and logistics demand two (or more) cameras**: thresholds quoted at 100/120/150 guests or 6+ hours; "the market calls for it"; "3 photographer package" for 500 guests; South Asian weddings; brides want both the aisle walk and the reaction at the same moment (thread 27).
- **Standard hand-over**: "the second just gives the main all their raw files" (thread 6).
- **Manual workarounds**: colour labels per photographer in Lightroom (No Parfait 2104); matching exposure/style between shooters by hand (accl1k: "a ton of variability from my photos and my second shooter"); asking the second to copy the lead's settings.
- **Volume with two shooters**: 6–7k (KariBjorn), 8–10k (palinsafterbirth), 12k over 12 h (ylime114), 7k (kstinasunflower), 5k/10 h (InternationalSky7598).
- **No commenter in this batch names any tool that merges cameras into one timeline or handles clock offset.** The need is expressed; no solution is mentioned.

### 4. Hard numbers

**Shot per wedding**
| Who | Shot | Context |
|---|---|---|
| Terrible Document 20 | ~1,400 avg, <2,000 | solo, 1,000+ weddings, single-shot mode |
| magwestphoto | ~1,400 | 8 h |
| wokeisme2 | ~1,500 | 6–8 h |
| dreadpirater | 2,000–3,000 | typical |
| CommercialShip810 | ~2,500 (record 3,200; ~1,200 in DSLR days) | full day |
| OP thread 10 | ~2,500 | German part-timer |
| u_matter_to_someone | 2,500–2,900 (was 5–7k on 2 bodies) | |
| Old-obligation7421 | 2,000–4,000 | |
| the-reoccuring-lemon | 3,000+ | |
| noblankish | 3,500+ | |
| LiterallyUrDad | 3,000–5,000 (mirrorless 20 fps) vs ~1,500 pre-mirrorless | |
| KariBjornPhotography | 4–5k solo, 6–7k with second | full day |
| Bomzeetit | 5–8k (was 1.5–2k) | |
| FilmCameragirl | up to 6,000 | early career |
| kstinasunflower | 7,000 | second overshot |
| OP hillsong1 | 8,000 | |
| Guitar74 47 | 8,000 | 14 h weddings |
| palinsafterbirth | 8–10k | with assistant |
| ylime114 | 12,000 | 2 shooters, 12 h over two days |
| Upsidedown0310 | 10k (record, by accident) | |

**Delivered per wedding**: ~400 (Chrisser6677 target); 400–600 full day (CommercialShip810); ~500 (dreadpirater); 500–750 for 8 h (AccomplishedSir535); 600 for 7 h (ylime114); 600–800 (InternationalSky7598); ~700 (Terrible Document 20; Weddingbean "700+"); 700–1,200 (Terrible Document 20, other thread); max 800 (u_matter_to_someone); 800 for 8 h = "100 per hour" (service requirement, LiterallyUrDad; contracted by Frosty-Apricot-8304); "about 75 images per hour" (Complete-Mechanic907); 900–1,100 team, 8 h (magwestphoto); 1,200–1,300 (ylime114, 10 h, 2 shooters); 1,000+ (two brides).

**Keep rate**: "around 10%" (davezaplephoto); "10-20%" (efoxp13244); 4:1–5:1 (dreadpirater); ~50% (Terrible Document 20: 1,400 -> 700); 5–15% keepers in general photography (Jeffrey_J_Davis, ExploreroftheLight); second shooter's files: >90% rejected (Filmandnature93), 80% culled (Terrible Document 20).

**Time spent**
- Culling: "a day and a half" for 8k (hillsong1); two days in Lightroom -> ~8 h in Narrative (FilmCameragirl); "a couple hours" for a big wedding in Photo Mechanic (Weak-Bumblebee9978); "best 2 hour video game" (Chrisser6677); initial cull = 1 day, second cull = 1 day (EcstaticEnnui, 2–3 h sessions); in-camera starring saves "2-3 hours" (Arvosss); 1,000 photos in ~15 min in PM vs 1 h+ in Lightroom (sheldoneousk); Photo Mechanic "1/4 of the time" (defeldus); 4,000 in an hour (Steve Perry, cited).
- Editing: 16 h -> 2 h with Imagen (royal_friendly); ~10 h -> 2–3 h (Weddingbean, Neurapix); "8-12 hours" typical (ajp233, hearsay); 500-photo wedding in an 8 h day (dreadpirater; CommercialShip810); 8+ h after Imagen (ylime114); 3–4 h reviewing AI edits ([deleted]); 2 h tweaking (slandoe); 3 h total with Aftershoot for 500–750 images (AccomplishedSir535); 3–4 h manual work per wedding incl. 1 h cull review (Aftershoot co-founder).
- Total per wedding: "25-40 'man-hours'" (evanrphoto).
- Turnaround: "8-12 weeks and not like five days" because of culling (wickedcold); 3–4 days with Aftershoot (Terrible Document 20); 3 days for 700 photos (Erick_oseguera); next-day galleries by AI users (umwhat333, critical); outsourced editor "one or two weeks"; backlog "31,000 photos behind" (pspetrini).

**Weddings per year**: 25–30 = full-time job (evanrphoto); target 40, did 60–65 (benhowland); "80-100/year would be easy" if someone else edited (benhowland); 50+ with AI (umwhat333); "75 weddings a year" (minaret_photo, as upper case); 1,000+ career weddings (Terrible Document 20).

**Prices**
- Aftershoot: "like $500 for the ENTIRE YEAR for unlimited culling, editing and retouching" (Maddface).
- Imagen: "weddings are about $30", sessions under $10 (e-lishaphoto, ServiceB4Self); $7 minimum monthly fee (rolls over as credit); "close to $200 or more... a month between 4 or more weddings" (Weddingbean); studio: 72k images in 7 months, "$240/mo"; $131 disputed charge; Profile Shop profiles US$197–250; free trial 1,000 images; competitor editing service costs "$0.10/image more" than Imagen (Maddface).
- Neurapix: $50/month. OptiCull: $59.99 lifetime. Cullibrate: "1/5th the price" of Photo Mechanic. Narrative: "It's free" (culling tier). Wildernis Lab: $120/wedding incl. human culling. Game controller for culling: $10.
- Training-set sizes: Imagen 3,000 minimum (employee), users say 3,000–5,000, one trained on ~10k; Aftershoot profile 2,500.
- Client-side: photographer packages $4,000 (6 h) / $5,000 (10 h) with second shooter; third-shooter trainee paid $50 per wedding.

### 5. Unmet needs and feature wishes

1. **Rejects that can be trusted without a second look.** Nearly every user, including fans and Aftershoot's co-founder, still reviews the whole cull ("you're still gonna find yourself double checking every single photo anyways"). One documented lost group photo. The stated fear: "What if it deletes ones that are good?"
2. **Recognising the moment/emotion, not just sharpness and open eyes** ("AI culling really missed the mark on identifying the most powerful moments"; "AI still cannot detect emotions"; frame-based VLM pipeline "misses genuinely strong emotional moments").
3. **Respect for artistic intent** — intentional blur/soft focus, dark frames, style ("The AI doesn't know if you took that photo with intentional blur or not").
4. **Knowing whose face matters** — OptiCull's developer admits background faces at weddings are a limitation and that there "has to be some way to filter the background faces".
5. **Second-shooter handling** — clock sync, near-identical viewpoints, 80–90% rejection, style mismatch; no tool named as solving it.
6. **Working from the first wedding** — profiles need 2,500–5,000 edited images or "4 or 5 weddings" of feedback; users resort to uploading the same gallery twice.
7. **Grouping and ordering by moment/subject** — "move all my cake photos next to each other"; merge scenes the tool split; order problems with capture time; "the groupings make me feel less overwhelmed"; curation/storytelling "is what takes me the most brain power"; Imagen's own "at least one photo from each scene" mode.
8. **Choosing between near-duplicates** — decision fatigue ("A, B, C or D"); Aftershoot weak on "which duplicate is your favorite".
9. **Local processing / no upload** — used as a selling point by Aftershoot advocates, OptiCull, Picker AI, snapsortr; Imagen criticised for the upload-wait-download loop.
10. **Fair, predictable pricing** — complaints about minimum monthly fees, per-image cost at volume, unexpected charges; low-volume shooters say $200/month is too much.
11. **Speed on Windows / ordinary hardware** — Lightroom slowness; several requests for Windows versions of Mac-only indie tools.
12. **Describing what to find in words** (Cureyta pitch: "ceremony shots where both bride and groom are visible").
13. **Sneak-peek selection** as the one use even sceptics accept for AI ("quickly pick 5 shots for a 'Sneak Preview'").

### 6. The 10 strongest quotable lines

1. Commercial_Foot3145, r/WeddingPhotography, "AI culling software" (`19 - AI culling software r WeddingPhotography.png`): "I'll find AfterShoot marking an image a 5-star that is out of focus and super dark, but yet marking a perfectly sharp and properly exposed image as a 1-star. A lot. I have to go through and manually cull everything in the end. Always. Every single time."
2. Thin_Register_849, same thread: "Because i trusted it far too much. [...] It's when I had a group photo missing from the gallery, and the couple asked me for it. I found it in Lightroom, I went back through aftershoot's initial cull and was sure they were all there, but they weren't."
3. davispw, r/WeddingPhotography, "Editing Hangover" (`20 - Editing Hangover ...png`), 3mo ago: "There are too many false positives and false negatives so you WILL have to go back through the whole shoot yourself, which will take MORE time."
4. ibetyouranerd, r/AskPhotography (`23 - AI Photo culling vs manual culling programs r AskPhotography.png`): "They work but you're still gonna find yourself double checking every single photo anyways."
5. Frosty1397, r/photography, "Exhaustion from culling photos" (`20 - Exhaustion from culling photos r photography.png`), 2 days ago: "I'm afraid to delegate the culling process to an algorithm. What if it deletes ones that are good?"
6. evanrphoto, r/WeddingPhotography (`23 - Questions and Anything Goes ...png`): "AI editing is very good, and more consistent than my eye across a set/series/wedding. But AI culling really missed the mark on identifying the most powerful moments."
7. timwoodphoto, r/WeddingPhotography, "Hands up if culling..." (`24 - Hands up if culling makes you want to stab your eyes out. 🤣 r WeddingPhotography.png`): "Culling a second's work is just as bad, especially if their cam clock isn't synced with yours!"
8. Filmandnature93, r/WeddingPhotography, "Does anyone prefer to do weddings solo" (`21 - Does anyone prefer to do weddings solo these days r WeddingPhotography.png`): "I just end up with so many photos that I never use, I believe more than 90% of the second's photos are rejected".
9. wickedcold, "Hands up if culling..." (same file as 7): "Culling is the reason I deliver in 8-12 weeks and not like five days."
10. WeddingPhotography-ModTeam, "AI culling software" (same file as 1): "Please note that this subreddit has experienced a significant level of astroturfing relating to this topic and specific AI companies. [...] Community members should be extra vigilant and critical of advice, recommendations, and comments in any and all threads related to this topic and these companies."

Runners-up: LarryAndHisCats ("The AI doesn't know if you took that photo with intentional blur or not"); OptiCull developer on background faces at weddings; SetReasonable5825, Aftershoot co-founder ("1 hour reviewing culling"); ServiceB4Self ("You have to feed it like 5,000 of your previous edits"); the-reoccuring-lemon ("600 shots? Try culling 3000+ from a wedding. I dread post production.").

### Caveats for citing
- Praise for Aftershoot and Imagen in these threads is mixed with self-disclosed vendors (Aftershoot co-founder, Imagen employee "Scott from Imagen"), affiliate/referral codes (redfishgoldy, AppropriateShirt8529, heatherkan), and accounts that read as promotional (Maddface; late one-off comments for Evoto, Photodotedit, Cureyta). The subreddit moderators warn about this explicitly.
- Several of the harshest AI-culling comments are 3–5 years old; the tools have changed since. The 2026 threads (items 1, 10, 11) still show the same objections (re-checking, fear of lost shots), which supports that the problem persists.
- Indie-tool developers (OptiCull, Cullibrate, Cureyta, Picker AI, Palomino, snapsortr) appear in comments promoting their own products; their statements are vendor claims, though the OptiCull developer's admissions of limits are useful.
- Nothing in this batch mentions Adobe Lightroom "Assisted Culling" by that exact name; two comments refer to Lightroom's AI culling in general terms (thread 1).
