# Smart Start 2026: nacrt prijave (Photoristic)

Rok: **ponedeljak 16. 11. 2026. u 12:00.** Obrazac se predaje kao PDF na portalu, a dugme „Submit“ mora da se klikne pre roka.

Kako čitati ovaj dokument:
- Odgovori su na engleskom, redom kao u obrascu, i spremni za kopiranje u polja.
- Delovi u `[[TODO: ...]]` su stvari koje ja ne znam. Tu upiši svoje podatke.
- Ispod svakog odgovora je kratka napomena na srpskom: zašto je tako napisano i šta treba proveriti.
- Svaki broj ima izvor. Brojevi iz projekta dolaze iz `docs/research/`, a činjenice o agenciji iz `docs/interviews/`.

**Glavna nit cele prijave je traction:**
1. Problem je doneo kupac: vlasnik agencije Foto Tajna (oko 300 svadbi godišnje).
2. Proizvod oblikujemo na sastancima sa njim, sa Ksenijom koja radi culling i sa fotografom Peđom.
3. Sve ostalo (tržište, konkurencija, javne recenzije) samo potvrđuje da problem nije samo njihov.

Ta nit se provlači kroz pitanja Q1, Q2, Q5, Q6, Q8 i Q9 i kroz video. U tekstu se ljudi pominju po ulozi (vlasnik, osoba koja radi culling, fotograf), a ne po imenu.

> Odluka (15. 11.): ime agencije se ne navodi. U tekstu stoji „a Belgrade wedding photo agency“, pa dalje „the agency“.

## Kako se boduje (Program Manual 6.1, 4.2)

| Kriterijum | Poeni | Šta ocenjivači traže |
|---|---|---|
| Korisnost i konkurentska prednost | 30 | jasan problem, pa rešenje; tačna faza razvoja i plan; da nije „me too“ |
| Tržišni potencijal | 30 | poznavanje kupca i konkurencije, put do tržišta, misliti globalno |
| **Tim** | **40** | komplementaran tim (tehnika + tržište), iskustvo u domenu |

- Za finalni krug treba **≥ 75 poena**. U finalnom krugu je prezentacija pred komisijom.
- **Neprihvatljivi troškovi:** marketing, PDV, dnevnice, polovna oprema, troškovi zapošljavanja.
- **Bruto 2 plata** je najviše 450.000 RSD mesečno po osobi.
- Obrazac je zaključan. Sme se kucati samo u poljima, a menjanje strukture znači diskvalifikaciju.

---

## BRIEF SUMMARY

**Title of the project:**
Photoristic: trustworthy AI pre-selection of event photos that never loses a good shot

**Project IF ID:** [[TODO: ID sa portala]]

**Team Name:** SILA

**DESCRIPTION of the project in one sentence:**
Photoristic automatically culls the photos that several photographers take at an event, so the studio only does a quick final review, about five times shorter than manual culling, and no good photo is lost.

**DURATION of the project (in months):** 9

**Industry/Sector:** AI: Process optimization and automation tools

> Napomena uz sektor: naziv je sa padajuće liste „IndustryArea“ na portalu (grupa „AI“). U obrazac upiši isto što izabereš na portalu. Program Manual 6.1 (odeljak 2.1) kaže da je program otvoren za sve sektore, ali da najmanje 50 % sredstava ide u četiri prioritetna domena Strategije pametne specijalizacije: hrana za budućnost, IKT (sa posebnim naglaskom na veštačku inteligenciju), mašine i proizvodni procesi budućnosti, kreativne industrije. Domen ne donosi poene, ali određuje iz kog dela budžeta se projekat finansira. Rezerva, takođe u prioritetnom domenu: „Creative industry&Gaming: Digital Asset Management“.

> Napomena uz opis: rečenica sada kaže samo šta je proizvod. Agencija, broj slika i minuti su u Q1, Q3 i Q5. „About five times shorter“ je cilj, ne merenje: agencijin cilj (sa 2 sata na 15–20 minuta) je 6–8 puta, pa je 5 oprezna strana tog cilja. „No upload“ je izbačeno, jer Aftershoot i Narrative već rade lokalno.
>
> Napomena: biram 9 meseci, maksimum. Pravilnik traži da se izveštaj o prototipu preda tek u drugoj polovini projekta, a nama treba jedna puna svadbena sezona testiranja (proleće).
## BUDGET

| | RSD |
|---|---|
| 1. Innovation Fund co-financing | 5.400.000,00 |
| 2. Applicant's co-financing | 600.000,00 |
| TOTAL PROJECT COST (1+2) | 6.000.000,00 |
| 3. Mentorship support | 600.000,00 |
| TOTAL PROJECT BUDGET (1+2+3) | 6.600.000,00 |

> Napomena: tražimo maksimum. Vaših 10 % (600.000 RSD) mora biti **u novcu** iz privatnih izvora. Uplaćuje se na namenski račun firme u delovima, uz svaku tranšu. Proverite da li tim može to da obezbedi. Ako ne može, smanjite ceo budžet srazmerno.

## Short eligibility questionnaire

| Pitanje | Odgovor |
|---|---|
| ≥ 51 % tima su rezidenti Srbije | [[TODO: Yes]] |
| ≥ 51 % nema udeo ni u jednoj firmi u Srbiji | [[TODO: proveri za svakog člana]] |
| Svaki član je samo u jednoj prijavi | Yes |
| Niko nije na drugom aktivnom projektu Fonda | [[TODO: Yes]] |
| Prijavljivali ste se ranije sa istim projektom | No |

> ⚠️ **Proveri pre slanja.** Suosnivači buduće firme ne smeju imati udeo **ni u jednoj firmi u Srbiji** i ne smeju biti zakonski zastupnici druge firme. To važi od dana prijave do kraja projekta. Ako neko od vas ima preduzetničku radnju ili udeo u nekoj d.o.o., to mora da se reši pre prijave ili ta osoba ne može biti suosnivač.

## DEVELOPMENT PHASE AND INNOVATION LEVEL

**Current stage:** ☑ **Other (explain shortly):**
Prototype in development. We defined the initial requirements with an interested photo agency that came to us with this problem. From that work we derived hypotheses to validate the problem and the solution with other photographers, which we are actively doing now. The agency has given us photos from several weddings, which we use for development and testing.

**Level of innovation:** ☑ **Advanced Innovation**

> Napomena: „Concept Validation“ bi nas potcenio, jer je prvi deo (prepoznavanje momenata) već razvijen i izmeren. Za inovaciju biram „Advanced“, a ne „High“. Pojedinačne tehnike (embeddinzi, lica, VLM) već postoje. Novo je kako ih kombinujemo: dva fotografa u jednoj liniji, sigurnosna pravila i rad bez treniranja. Ocenjivači kažnjavaju precenjivanje, a „Advanced“ odgovara onome što tekst dokazuje. Ako želiš „High“, tekst o prednosti mora biti još jači.

---

## PROBLEM

### Q1. The problem, how you learned about it, size and severity (max 300 words)

**The problem came to us from a customer.** In September 2026 the owner of a Belgrade wedding photo agency asked us for help. The agency covers about 300 weddings a year, each with several photographers. In season they shoot about 20 weddings every weekend, and everything must be delivered by Friday. Otherwise "the system falls apart".

The bottleneck is culling: removing blurred, blinking and duplicate shots before editing can start. The owner calls it "the hardest part of the job in photography, much harder than shooting".

The agency's culler and a photographer gave us the numbers: one wedding produces 5,000–6,000 photos, and culling them takes about two hours "in perfect conditions"; in practice it stretches into the next day. At 20 weddings a weekend, that is 40 hours of culling a week, a full-time job.

The agency had tried several AI tools, including market leaders Aftershoot and Imagen, and went back to manual work: the tools group similar photos, but someone still goes through every group. Their photographer: "If there are five thousand photos, I have to go through all of them again to check whether it did a good job." The culler's answer became our core rule: a bad photo left in is not really a mistake, but deleting a good one is.

**It is not just one agency.** Other photographers we interviewed and thousands of Reddit comments say the same about AI culling tools: the result must be re-checked in full, because the tools reject good photos. One Aftershoot user: "I have to go through and manually cull everything in the end. Always. Every single time." Every year there are 2.1 million weddings in the US and 1.7 million in the EU (CDC, Eurostat, 2024), and 88 % of US couples hire a photographer (The Knot, 2026).

> Napomena: citati su prevedeni sa sastanaka 21. 9. i 7. 10. (`docs/interviews/`). Broj od 40 sati nedeljno je računica: 20 svadbi × 2 h. Broj fotografija je 5–6 hiljada po svadbi, kako su rekli Peđa i Ksenija; Mitar je na prvom sastanku rekao 2–3 hiljade, pa u opisu stoji raspon 2.000–6.000. Broj sastanaka se namerno ne navodi.
>
> Reddit (`docs/research/2026-11-15-reddit-culling-competition.md`):
> - „Thousands of Reddit comments“: pregledane su 183 teme (167 sa korisnim sadržajem). Komentari nisu brojani; „na hiljade“ je procena po broju tema. Ne navodi broj žalbi.
> - Citat je Commercial_Foot3145, tema „AI culling software“, r/WeddingPhotography, stara oko 3 godine. Pre slanja otvori sliku i proveri ga.
> - Nije stalo u 300 reči, ali je dobro za odbranu pred komisijom: fotografi na Redditu navode 2,5–5 sati za 5.000 slika sa drugim fotografom (izjave pojedinaca, ne anketa). To nezavisno potvrđuje agencijina „dva sata“.
> - Broj venčanja u Srbiji je prebačen u Q7, zbog ograničenja reči.
> - Iskusni solo fotografi u Photo Mechanicu završe za 30–60 minuta. Zato svuda piše da je „dva sata“ mera agencije, za 5.000–6.000 slika više fotografa.
> - 88 % (The Knot) nije potvrđeno u proveri tržišta. Otvori izvor pre slanja.

### Q2. Who it affects most and how they cope today (max 200 words)

**Most affected** are **agencies and teams that send several photographers to each wedding**. Work arrives in weekend peaks, and nothing can be edited until culling is done. Every extra photographer adds thousands of frames, most of them repeating moments the others already caught, yet someone must look at each one: at our partner agency, one person checks 5,000–6,000 photos per wedding one by one. Next come **independent "artistic" photographers**, who shoot 20–50 weddings a year and cull and edit everything themselves.

**How they cope today.** Most **cull by hand** in Lightroom or Photo Mechanic, which takes a couple of hours even for an experienced photographer. Many have tried **AI culling tools** such as Aftershoot, Imagen or Lightroom's Assisted Culling, from US$10 a month. The tools mark photos as keep or reject, but users do not trust the marks and re-check everything; a professional on Reddit finds "at least 25 percent of what they chose is unusable". Some tools promise to learn the photographer's taste, but first need thousands of their own edited photos. The third option is **outsourcing**: US$50–200 per wedding, 1–5 days, and every file must be uploaded, about 10 hours per wedding on the agency's connection.

> Napomena:
> - **20–50 svadbi godišnje** su izjave fotografa na Redditu (timovi 60–100). Raniji broj „20–30 (YPWP)“ je izbačen: tvrdnja „28 svadbi godišnje“ je oborena na proveri, a pouzdana anketa nije nađena (`docs/research/2026-11-14-market-size.md`, odeljak 2). Peđinih 5–10 su njegove svadbe pored rada u agenciji, pa ih ne navodimo kao broj.
> - **Ručni culling „a couple of hours“:** na Redditu većina navodi 2–5 sati po svadbi. Najbrži u Photo Mechanicu završe za 30–60 minuta; ako komisija to pomene, odgovor je da ta brzina traži jednog iskusnog čoveka i jednu kameru.
> - **„Every extra photographer adds thousands of frames“:** na Redditu drugi fotograf donese 1.000–5.000 kadrova, a 80–90 % se odbaci.
> - Zbog ograničenja reči izbačeni su: Peđinih 7 dana za 2.000 slika, Trustpilot recenzija (5–10 % uštede) i imena FilterPixel i Narrative Select.
> - **Cena AI alata:** Aftershoot Select je $10 mesečno uz godišnje plaćanje (potvrđeno). Zbirni cenovnici Imagena, Narrativea i FilterPixela su oboreni na proveri, pa raspon „$10–100“ više ne stoji.
> - **Citat „25 percent“** je pass-agress-ive, r/AskPhotography, star 5 meseci, o Aftershootu i Imagenu. Trustpilot recenzija je parafrazirana iz `docs/research/2026-11-10-culling-complaints.md` (odeljak 2.1).
> - **Profili 2.500–5.000 slika** se odnose pre svega na profile za editovanje (Imagen, Aftershoot). Za culling Aftershoot radi i bez profila. Zato ovde ne piše da culling traži treniranje.
> - **Outsourcing:** WeEdit naplaćuje $0,06 po poslatoj slici (oko $150 za 2.500), RDFL oko $50, a korisnici na Redditu navode oko $200. Rok je 1–5 dana, na Redditu i do dve nedelje. Raniji raspon $100–300 se odnosio na editovanje i dolazio je od Imagena.

---

## SOLUTION

### Q3. Proposed solution, concept, key features (max 300 words)

**Photoristic prepares a wedding for delivery with as little human work as possible.** Its core is culling; the editing steps our customer asked for (crop, light, sharpening) come next.

**How it works.** Photoristic takes all the photos of the day, from every photographer. It **recognises the moments of a wedding**, such as the vows, the kiss or the first dance, and understands when several photographers captured the same moment. From each moment it **picks the best frames, and it knows who matters**: a guest blinking in the background is no reason to reject the couple's photo, and an intentional closed-eye or artistically blurred shot is not rejected automatically. It follows strict **safety rules**: every moment keeps at least one photo, a photo is rejected only when a better photo of the same moment is kept, and nothing is deleted, so any photo comes back in one click. Every photo is marked keep, reject or "please look". Because the rules are clear and strict, **"please look" holds only the rare edge cases** that truly need a human eye. The result appears in the software the studio already uses.

**What changes for the studio.** Today someone looks at 5,000–6,000 photos one by one. With Photoristic, **the studio does not review the rejects**: a reject is never the only photo of a moment, so no moment can be lost. That is what lets photographers trust it. The reviewer skims the kept photos and decides only the few "please look" cases, so **the review takes about five times less time** than manual culling.

> Napomena:
> - Namerno bez tehničkih termina, naziva modela i detalja toka obrade. Ne piše ni gde se obrada izvršava (lokalno, server), da bismo ostali slobodni.
> - **Tri ishoda nisu jedinstvena:** FilterPixel već ima „Keepers / Review / Rejects“, sa ocenom i razlogom po slici, a tri korpe ima i imagic. Aftershoot garantuje bar jednu sliku iz svake grupe duplikata, a korisnici se i dalje žale, jer grupe nisu momenti i jer izbor unutar grupe nije dobar (Reddit, odeljak 7.3). Zato prednost nije u tri korpe, nego u tome što je **odbačena slika uvek slabija verzija zadržane slike istog momenta, kod svih fotografa zajedno**. Zbog toga odbačene ne moraju da se proveravaju. To je odgovor na pitanje „pa i ovde moram sve da pregledam“.
> - Tačka 6 (Lightroom) je u planu, ne u kodu. U MVP koracima je eksplicitno navedena.
> - **Verzija od 15. 11.:** bez tehničkih reči (folder, fajl, sat kamere, grupisanje, Lightroom). Tačka 5 naglašava da su pravila stroga i da u „please look“ idu samo retki granični slučajevi. Završni pasus ističe da se odbačene slike ne pregledaju i da je pregled oko pet puta kraći.
> - **Automatsko usklađivanje satova (deo tačke 2: „several photographers captured the same moment“) je takođe u planu, ne u kodu.** Danas se grupiše po kameri. Dodato je jer je to najjasnija praznina kod konkurencije: vodiči Aftershoota i Narrativea to prepuštaju korisniku, a na Redditu se satovi usklađuju ručno. U Q5 je to korak M1–2.
> - **„Dva sata → 15–20 minuta“** je sada vezano za obim agencije (5.000–6.000 slika, više fotografa). Iskusan solo fotograf u Photo Mechanicu završi za oko sat, pa bi tvrdnja bez tog okvira mogla da se ospori.

### Q4. What makes it different and better (max 200 words)

**Existing tools patch single cases. Photoristic is built to understand a photo the way a human eye does.** Our research shows that today's tools apply fixed technical rules: is it sharp, are the eyes open, does it look like the previous one. They add patches for single cases, such as kiss detection, but a patch is not understanding: "the AI will think an intentional shot with my clients eyes closed is bad" (Imagen user). A sharp groom is rejected because a guest behind him is blurred. Different family groups are merged as duplicates; one Aftershoot user noticed a missing group photo only when the couple asked for it. One photographer: "It's far more than deciding that a blink or poor focus is problematic, it's knowing when it isn't."

**Understanding the context of a photo is what we are building.** Photoristic **recognises the moment**, so it compares photos of the same moment, not photos that look alike. It **knows who matters**: the couple and family count, a stranger in the background does not. It **judges closed eyes and blur in context**. And since **no moment is left without a photo**, rejects need no second check.

> Napomena (verzija od 15. 11., drugi put prepisano): poenta je razumevanje naspram tehničkih pravila, potkrepljeno žalbama korisnika.
> - **„Fixed technical rules“** je naš zaključak iz žalbi, ne podatak o tome kako su alati napravljeni. Zato piše „our research shows“.
> - **Zakrpe, ne razumevanje (16. 11.):** Aftershoot (od oktobra 2022) i Imagen imaju „kiss detection“, pa je izbačena tvrdnja da se poljubac odbija kao treptaj. Tekst sada kaže da alati krpe pojedinačne slučajeve, a da mi gradimo razumevanje konteksta slike kao ljudsko oko. Izvori: https://devtest.aftershoot.com/?p=47051 i https://imagen-ai.com/post/ai-photo-culling.md (otvori ih pre slanja).
> - **Izvori primera** (`docs/research/2026-11-15-reddit-culling-competition.md` i `2026-11-10-culling-complaints.md`):
>   - citat o zatvorenim očima: electric-ee110294, r/AskPhotography, star 4 meseca, o Imagenu;
>   - oštar mladoženja odbijen zbog mutnog gosta u pozadini: Adobe Community, o Lightroomu;
>   - spojene porodične grupe: evanrphoto i Phounus, o Aftershootu;
>   - grupna fotografija koja je nedostajala: Thin_Register_849, r/WeddingPhotography, o Aftershootu;
>   - „knowing when it isn't“: LisaandNeil, r/Lightroom, star oko godinu dana.
> - Pre slanja otvori slike tih tema u `docs/reddit-competition/` i proveri citate.
> - **Izbačeno:** učenje iz svadbi agencije (preusko, vezano za jednu agenciju), „no upload“, „Fair pricing“ i „3–5 puta“.
> - Usklađivanje više fotografa ovde se više ne pominje posebno; ostaje u Q3.
> - Ima i zadovoljnih korisnika Aftershoota koji štede 2–3 sata po svadbi. Budi spremna na to pitanje pred komisijom.

### Q5. Current state of technology and steps to MVP, with timeline (max 200 words)

**Today** we are defining the MVP requirements with the agency. We are also testing visual AI models and finishing the first part, **recognising moments**: it is now above 94 % accurate, checked by hand with a photographer.

**Months 1–2:** we finalise the requirements, validate problem and solution in interviews with more photographers, and continue moment recognition. We benchmark visual models and build **test datasets labelled by professional photographers**.

**Months 3–4:** we choose the model from the benchmark results. We research the architecture that understands context (closed eyes, blur, who matters) and **gives the same answer every time**, our biggest technical challenge. We design the interface with photographers.

**Months 5–6:** installation at our partner agency, our proof-of-concept customer. As agreed, the agency gives feedback at every step before we move on.

**Months 7–9:** active use on real weddings, improved from live feedback. Final tests on our datasets and with the agency confirm the targets: **a review up to five times shorter, and no good photo deleted**. The architecture stays scalable, ready for other studios.

> Napomena (verzija od 15. 11.): ne tvrdimo da imamo prototip koji radi i ne navodimo broj testova ni slika. Stanje je: definisanje zahteva, testiranje vizuelnih modela, završavanje prepoznavanja momenata.
> - **„Above 94 %“:** izmereno je 95 % na ručno označenim parovima slika.
> - **Raspored po mesecima** prati tranše Fonda: validacija tržišta do M3, izveštaj o MVP-u u drugoj polovini projekta. Instalacija u agenciji je u M5–6, a sezona svadbi u M7–9. [[TODO: proveri da li se M7–9 poklapa sa sezonom, zavisno od datuma početka projekta.]]
> - **„Give the same answer every time“** je deterministički rad, rečeno bez tehničkog termina. Merenja od 12. do 14. 11. pokazuju zašto je to najveći izazov: kad model poredi kadrove, izbor zavisi od redosleda slika (`docs/research/2026-11-14-ranking-full-model-and-per-photo.md`).
> - **Izbačeno:** poređenje sa Aftershootom na istoj svadbi i Lightroom export. Ako želiš poređenje nazad, staje u M7–9 kao „and compare with the market leader“.
> - **Usklađeno sa Q5:** u „Current stage“ piše „Prototype in development“, što se slaže. U Q10 više ne piše broj linija koda ni broj testova.

### Q6. Shared with potential customers? Feedback? (max 200 words)

**Yes. The product is shaped together with its first customer, a Belgrade wedding photo agency.**

The agency came to us because it had tried existing tools and none solved the problem. In their words: "Sometimes we need those closed eyes" and "I have to go through all the photos again."

In **September 2026** we met the owner, who agreed that we may sell and patent the product. In **October 2026** we held a working session with the owner, the agency's culler and a photographer. Together we fixed the **success criteria** ("Someone will have to look, but not for two hours: finish the package in fifteen, twenty minutes") and the rule **"never delete a good photo"**. To help us develop and test, the agency gave us **several test sets from real weddings, each before and after their culling**. **Since then** we meet every Thursday, and they give feedback on every improvement we make.

**Beyond the agency,** we researched Reddit's photography communities in depth: 183 threads and thousands of comments. Culling is among the most discussed problems there, and existing tools are criticised for the same reasons the agency gave us.

> Napomena: proveri da li sprintovi sa Peđom četvrtkom zaista teku. U intervjuu piše samo da je to dogovoreno. Ako ne teku, napiši „we agreed weekly sprints“.

---

## MARKET POTENTIAL

### Q7. Market size and trends (max 300 words)

**Market size.** Analysts estimate global wedding photography at **US$16–26 billion**, growing 5–8 % a year (Global Industry Analysts: US$25.8 billion in 2024). There are 2.1 million weddings a year in the US (CDC, 2024) and 1.7 million in the EU (Eurostat, 2024) and 29,402 in Serbia (RZS, 2025). The number of weddings is stable; demand for culling grows with photos per wedding, photographers per wedding and AI adoption. **Our serviceable market**, by our estimate, is about 3.3 million photographed weddings a year in the US and EU. At €5–10 per wedding, that is **€17–33 million a year**.

**Photographers already pay, but the problem is not solved.** Aftershoot reports 188,000 photographers and 8.8 billion images processed in 2025 (company data). Imagen raised US$30 million in 2022 and reported over US$10 million in annual recurring revenue (TechCrunch). Yet users of these same tools say they cannot rely on the result. One photographer who tested both: "it left me constantly worried and rechecking it." The demand is proven; the tool photographers can trust is still missing.

**Four trends work for us.** First, **AI is standard**: only 12.9 % of photographers use no AI (Zenfolio/PPA, 2025). Second, **there are more frames per moment**: photographers on Reddit report going from about 1,500 frames per wedding before mirrorless cameras to 3,000–5,000 now, and 4,000–10,000 with two photographers. Third, **privacy regulation**: GDPR treats face recognition data as biometric data, which favours tools that process guests' faces locally. Fourth, **the incumbent has entered**: Adobe added Assisted Culling to Lightroom (2025). This validates the need, but it does not work across several photographers, and one user calls it "worse than not using the tool at all".

**Beyond weddings,** the same engine fits other events covered by several photographers: corporate, school, sports and press.

> Napomena: izmenjeno prema `docs/research/2026-11-14-market-size.md` (odeljak 9) i Reddit istraživanju. Procena od €17–33M: 3,8M svadbi × 88 % (udeo za SAD primenjen i na EU) × €5–10. Zato piše „our estimate“. Ni 88 % ni cena 5–10 € nemaju potvrdu; jedan Mitrov broj bi ovo učvrstio.
> - **Raspon umesto jedne cifre.** Procene analitičara se jako razlikuju (15,8 do 26,1 mlrd USD; jedna čak 3,7 mlrd). Metodologija nije javna, pa piše „analysts estimate“.
> - **Broj venčanja je ravan ili pada** (EU stopa prepolovljena od 1964; Srbija 36.542 u 2011, 29.402 u 2025). Bolje je da to kažemo sami i rast vežemo za broj kadrova, broj fotografa i AI.
> - **Izbačeno, jer nije prošlo proveru:** VSCO 83 %, rast AI softvera 15,4 % (GII), Canon R5 Mark II 30 fps, i BLS 145.000 (to su svi fotografi, ne svadbeni, pa broj više zbunjuje nego što pomaže).
> - **„Already pay, but the problem is not solved“ (16. 11.):** broj korisnika ostaje kao dokaz da se za ovo plaća, a odmah uz njega stoji da isti korisnici i dalje sve pregledaju ručno (citat: PhotosByFonzie, „AI Culling - How is it in 2025“, r/Lightroom, o Imagenu i Aftershootu, star oko godinu dana; proveri ga na slici. Namerno nije isti citat kao u Q1). Da stane u 300 reči, izbačeni su Nemačka i Italija, „7.4 % a year to 2030“ i deo o astroturfingu u trendu 1.
> - **Aftershoot: „processed“, ne „culled“.** Njihova strana meša culling i editovanje.
> - **Imagen ARR** je izjava njihovog direktora iz 2022.
> - **Izvore citiraj primarno:** Eurostat (tabele `demo_nind`, `tps00206`) i stat.gov.rs, ne Sofia Globe i Vreme.
> - **Opciono za trend 1:** noviji Zenfolio SOPI 2026 („almost 50 % of photographers use AI on a weekly basis“). Otvori zenfolio.com/sopi/2026-april i proveri pre navođenja.
> - **Opciono za trend 3:** španski AEPD je kaznio GSMA sa 200.000 € zbog prepoznavanja lica posetilaca bez procene uticaja (TechCrunch, 2023). Nije prošlo proveru, pa ga otvori pre navođenja.
> - **Trend 4:** citat je jollyllama, r/Lightroom, star oko 9 meseci. „Ne pravi stekove preko više foldera“ važi za Lightroom Classic, po prijavama korisnika.
> - Susedna tržišta (škole, sport, korporativni događaji) nemaju nijedan pouzdan broj. Zato ostaju samo kao jedna rečenica.

### Q8. Target group and early adopters (max 200 words)

**Our first customer is our partner agency**: about 300 weddings a year, 20 every weekend in season, several photographers per wedding, and a pilot from month 1.

**Early adopters.** First, **agencies and teams with several photographers per event** that cull in-house. For them culling is the bottleneck between the weekend and delivery. Second, **independent "artistic" photographers** who cull and edit everything themselves, starting with those who work with a second photographer. The agency owner pointed us to them as the strongest market: the tool would shorten their post-production "brutally", and there are more of them every year. Geographically we start with **studios in Serbia and the Western Balkans**, which we reach personally through our partner's network and which are price-sensitive, since full-day packages cost €600–800 (Kurir). Then come **EU studios in privacy-sensitive markets** such as Germany, where a wedding photographer costs €1,656 on average (Bridebook, 2026) and processing guests' faces locally is a buying argument.

**Later** we will address editing and outsourcing companies that cull for many photographers. We do not target wildlife, sports-only and macro photography.

> Napomena: izmenjeno prema istraživanjima od 14. i 15. 11.
> - **Redosled ostaje, i sada ima dokaz.** Na Redditu su solo fotografi najskeptičniji prema AI-ju i najbrži ručno (Photo Mechanic), a timovi sa više fotografa imaju jači bol. Zato je kod solo fotografa dodato „first those who work with a second photographer“.
> - **60–100 svadbi godišnje kod timova** su izjave sa Reddita (jedna firma sa 40 fotografa: 790 svadbi u 2023). Nije anketa.
> - **Nemačka 1.656 €** (Bridebook 2026, anketa parova; ceo dan oko 1.940 €) zamenjuje 3.050 € (Fearless Photographers), jer je taj izvor ocenjen kao nepouzdan.
> - **Izbačeno „underserved by US tools priced per seat in dollars“.** Aftershoot Select košta oko $10 mesečno, pa tvrdnja ne stoji.
> - **„nothing is uploaded“ → „processing guests' faces locally“.** Lokalna obrada nije razlika prema Aftershootu, ali jeste argument za GDPR.
> - Broj fotografa i agencija u Srbiji i regionu nije nađen. Mogući izvor: APR, šifra delatnosti 74.20.
> - Cene u Srbiji (Kurir) nisu proverene u ovom krugu.

### Q9. Business model and roll-out (max 300 words)

**Business model: a licence priced by usage**, matching the seasonal income of studios. Small studios **pay per wedding**, about €5–8 per event, to be validated in the pilot, with no cost in the off-season. We price against hours of skilled work and against outsourced culling (about US$50–200 per wedding, 1–5 days), not against the cheapest subscription: Aftershoot's culling plan costs about US$120 a year, and its users still re-check everything. Agencies buy a **season pass**: a yearly flat fee for unlimited events and several seats. For our partner agency the value is capacity: about 40 hours of culling every weekend of the season. There are no auto-renewal traps and no lock-in, and **the margin is high**, because the AI runs on the customer's hardware and the cost per wedding is close to zero.

**Roll-out.** **During this project (months 1–9)** the agency is the first live user, aiming for a paid contract by its end. Then come 5–10 paying studios in Serbia and the region: only a paying customer proves the need is real. The measured results (minutes of review, photos lost, a head-to-head with the market leader) become our sales evidence. **In year 2 we launch regionally**: Serbia and the Western Balkans, through our partner's network, photographer associations and workshops. **In years 2–3 we launch in the EU**, starting with DACH and Italy, through the Adobe Lightroom plugin marketplace, educators and outsourcing partners. **Expansion** follows three lines: the editing steps our customer asked for (crop, light, sharpening), a curated gallery for the couple, which raises revenue per wedding, and other events covered by several photographers.

**As an illustration** (our estimate), 1 % of photographed weddings in the US and EU at €7 is about **€230,000 a year**, and 1,000 studios with 40 weddings each at €6 is **€240,000**.

> Napomena: pitaj Mitra „koliko biste platili po svadbi ili po sezoni?“, makar okvirno. Jedan njegov broj vredi više od svih procena. Ako ga dobiješ, dodaj ga u Q6 i Q9.
>
> Izmenjeno prema istraživanjima od 14. i 15. 11.:
> - **Cena nije naš adut, i tekst to sada kaže.** 5–8 € po svadbi je za fotografa sa 40 svadbi 200–320 € godišnje, više od Aftershoot Selecta (oko $120). Zato se poredimo sa satima rada i sa outsourcingom. Za solo fotografe ovo ostaje slaba tačka; za agencije je sezonska karta jači argument.
> - **Outsourcing $50–200, 1–5 dana:** WeEdit $0,06 po poslatoj slici (oko $150 za 2.500), RDFL oko $50 (2016), Reddit oko $200. Raniji raspon $160–200 nije potvrđen.
> - **Plaćanje po svadbi** kod AI alata još niko ne nudi, a kod servisa je uobičajeno i hvaljeno (Wildernis Lab, $100–125 po svadbi). Otpor pretplatama na Redditu je stvaran.
> - **Kanali:** Reddit zajednice su neprijateljske prema nalozima proizvođača (moderatori upozoravaju na astroturfing). Zato u roll-outu ostaju lična mreža, udruženja i edukatori, a forumi se ne navode kao kanal.

### Q10. Patent search and IP position (max 200 words)

**Found.** A preliminary Google Patents search (November 2026) shows granted US patents on choosing the best among similar photos: Adobe US 9,817,847 (a neural network scores images and picks representatives that are not alike) and US 9,858,296 (best photo of a person by face quality); Apple US 10,523,894, Microsoft US 10,671,895, Shutterfly US 12,131,363 and Amazon US 9,955,033 (best frame of a burst).

**Not found.** No patents assigned to Aftershoot, Imagen, FilterPixel or Narrative. This is not conclusive: applications are published only after 18 months and may be filed under other names. We have not yet searched for grouping one moment across several photographers.

**Plan.** We do not claim that our approach is patentable or free of existing patents. Within the project a patent attorney will run a prior-art and patentability search and review the closest patents, starting with Adobe's. Then we decide whether to file or keep the know-how a trade secret.

**IP position.** The code is our own and will be transferred to the new company. Our first customer has agreed that the product is ours to sell and patent. The third-party models are open, under Apache 2.0, allowing commercial use: DINOv2, RT-DETR v2, AuraFace and Qwen3.5.

> Napomena (verzija od 16. 11.): tekst ne tvrdi da je naš pristup patentabilan. Kaže šta smo našli, šta nismo i šta planiramo.
> - **Pretraga po nosiocu (16. 11., Google Patents):** Aftershoot, Imagen AI / ImagenAI, FilterPixel i Narrative (foto-firma) nemaju nijedan pogodak. Pravne nazive firmi nismo proveravali, pa tekst kaže „may be filed under other names“.
> - **Adobe US 9,817,847** je najbliži našem toku (ocena slike neuronskom mrežom, rangiranje, izbor reprezentativnih koje nisu slične). Kod nas se slične slike prvo grupišu, a model daje redosled unutar grupe; da li je to dovoljna razlika, procenjuje patentni zastupnik. **US 9,858,296** je odobrena prijava US20170286452A1.
> - Pročitani su nezavisni zahtevi oba Adobe patenta. Opisi Apple, Microsoft, Shutterfly i Amazon patenata su iz ranije verzije nacrta i 16. 11. nisu ponovo otvarani; otvori ih pre slanja.
> - Za fazu sa treniranjem modela vredi pokazati zastupniku i Adobe US 10,489,688 (lična ocena estetike kao pomak na opšti model) i US 10,002,415 (treniranje na parovima slika). Nisu u tekstu, jer se ne tiču MVP-a.
> - Statusi i datumi isteka su sa Google Patents, koji ih označava kao pretpostavku. Članovi patentnih porodica u Evropi nisu proveravani.
> - „Trade secret“ kao druga opcija je predlog; izbaci ako ne želite da se pominje. Blaža varijanta plana: „review the closest patents“, bez „starting with Adobe's“.
> - Izbačeno zbog 200 reči: „Our approach differs in three ways“, „Our core assets are the know-how and the labelled data“ i podatak da je Apple patent istekao. Obrazac je 16. 11. izbrojao 202 reči, pa su skraćene još tri; proveri ponovo posle kopiranja.

> ⚠️ Napomena:
> 1. Mitrova saglasnost je zasad samo usmena („radi što hoćeš od programa“). Zamoli ga da to potvrdi jednim mejlom, zajedno sa izuzetkom za restoranske fotografe.
> 2. **Kome pripada kod?** Ako je projekat rađen u okviru posla ili na opremi poslodavca, proveri ugovor. IP mora pripasti novoj firmi.
> 3. Licence su proverene 14. 11. 2026. na Hugging Face model kartama.

---

## TEAM BEHIND THE IDEA

### Q11. Why you are the right team (max 400 words)

**We are two technical co-founders who have already built computer-vision products together.**

**Lana Radmilović (CEO)** and **Novica Trifković (CTO)** are software and AI engineers specialised in computer vision. We have worked together on several projects built from the same parts this product needs: face recognition, visual language models and model benchmarking. Both hold a master's degree in software engineering and AI from the Faculty of Organizational Sciences (FON), University of Belgrade. Lana has been an AI engineer at Programerika for two and a half years, building AI products. Novica is a PhD candidate in AI at FON, a teaching assistant for AI courses at the University of Novi Sad, and an AI engineer at Givesense.

**We have done this before.** We spent more than eight months building our own product based on face recognition (https://bysila.ai/), which this project also uses. It taught us computer vision in practice and the legal side of face recognition, through many consultations with GDPR lawyers.

**We know the difference between a real problem and a cool idea.** We went through the accelerator programme of Natal, a Serbian venture studio (https://natalstudio.com/), and learned that a tool does not sell unless the problem hurts enough for the user to pay. That is why we value what we have now: a customer who brought the problem to us and takes part in building the solution.

**How we split the work.** So far Novica has led the customer side: Novica found the customer while selling another product to photographers, held the first meeting, and has run the requirements analysis, the go-to-market approach (the interested agency as proof-of-concept customer, giving regular feedback), the weekly Thursday meetings and interviews with other photographers. Lana has led development: the ML pipeline, benchmarking visual models on our own server, measurements, and research into how the system can see a photo the way a human eye does: what is happening, and who matters. From now on the roles converge: Novica joins the implementation and Lana takes on the business side, so both founders stay on top of both the technology and the customer. After years together we know each other's strengths and weaknesses.

**Proof that we deliver.** The first technical milestone the customer set, recognising the same moment across photos from several photographers, already works with over 94 % accuracy.

**Domain expertise comes from the agency:** its lead photographers have agreed to be our advisors.

> Napomena (16. 11.): napisano prema vašem opisu. Ograničenje je 400 reči; proveri broj u obrascu posle kopiranja.
> - **Tim nosi 40 poena, a Fond traži tehniku + tržište.** Oboje ste inženjeri, pa tekst ističe ko je do sada vodio kupca i tržište (Novica: prodaja fotografima, intervjui, odnos sa agencijom; ne pominje se nikakav formalni dogovor o POC-u, jer ga nema), a iskustvo u domenu donose savetnici iz agencije.
> - **Titule i podela posla:** do sada je podela izgledala obrnuto od titula (CEO Lana na tehnici, CTO Novica na kupcu). Tekst to kaže otvoreno i dodaje da se uloge sada približavaju titulama: Novica ulazi u implementaciju, Lana preuzima biznis deo, a oboje ostaju u toku sa obe strane. Ako komisija pita, to je odgovor.
> - **Raniji proizvod:** naveden je link https://bysila.ai/. Proveri da sajt radi i da je na engleskom ili bar razumljiv ocenjivaču. Ako ima korisnike ili rezultat, dodaj jedan broj.
> - **Natal:** sajt https://natalstudio.com/ (otvoren 16. 11.) koristi ime „Natal“ i opisuje se kao „venture studio“; reč „accelerator“ se na sajtu ne pojavljuje, a program se tamo zove „Natal Academy“. Zato piše „the accelerator programme of Natal, a Serbian venture studio“. Ako je vaš program imao zvaničan naziv, upiši ga umesto „the accelerator programme“.
> - **„Another product for photographers“:** napisano kao poseban proizvod. Ako je to isti proizvod sa bysila.ai, spoji te dve rečenice, jer je to onda još jači dokaz iskustva u domenu.
> - **Savetnici:** piše „lead photographers have agreed to be advisors“. Pristanak je usmen; dobro bi došao u istom mejlu kao i saglasnost za IP (Q10). Savetnici nisu članovi tima, pa na njih ne važi uslov o udelima.
> - **Uslov o udelima** važi za vas dvoje: suosnivači ne smeju imati udeo ni u jednoj firmi u Srbiji niti biti zakonski zastupnici. Zaposlenje u firmama Programerika i Givesense nije prepreka.

### Team member tables (do 5 osoba)

**Member 1**

| | |
|---|---|
| Full name | Lana Radmilović |
| Role in the project | CEO, co-founder. Has led development so far (ML pipeline, benchmarking of visual models, measurements, moment recognition and grouping of similar photos) and is taking on the business side. |
| Relevant experience | Software and AI engineer specialised in computer vision. Co-built a face recognition product over more than eight months (https://bysila.ai/; computer vision, GDPR for biometric data). Went through the accelerator programme of Natal (https://natalstudio.com/). Built Photoristic's moment recognition, now above 94 % accurate. |
| Current occupation | AI engineer at Programerika (2.5 years), building AI products. |
| Education | Master's degree in software engineering and AI, Faculty of Organizational Sciences, University of Belgrade. |

**Member 2**

| | |
|---|---|
| Full name | Novica Trifković |
| Role in the project | CTO, co-founder. Has led customer and market work so far (requirements analysis, the relationship with the partner agency and weekly meetings, interviews with photographers, go-to-market, research of implementation options) and is joining the implementation. |
| Relevant experience | Software and AI engineer specialised in computer vision. Co-built a face recognition product over more than eight months (https://bysila.ai/). Sold a software product to photographers, which led to our first customer. Went through the accelerator programme of Natal (https://natalstudio.com/). |
| Current occupation | Teaching assistant at the University of Novi Sad, teaching AI courses [[TODO: naziv fakulteta]]; AI engineer at Givesense. |
| Education | Master's degree in software engineering and AI and PhD candidate in AI, Faculty of Organizational Sciences, University of Belgrade. |

> Napomena: polja u obrascu mogu imati drugačije nazive; prepiši sadržaj u odgovarajuća polja. Savetnici iz agencije se ne upisuju u tabele.

---

## VIDEO CLIP

[[TODO: link (YouTube „unlisted“ ili Vimeo); proveri u anonimnom prozoru da se vidi]]

Obavezno po pravilniku:
- do 3 minuta, na engleskom;
- **svi članovi tima su vidljivi**, i bar jedan govori pred kamerom;
- nisu dozvoljeni samo slajdovi ni AI glas.

**Predlog scenarija (≈2:50), sa fokusom na traction:**

| Vreme | Kadar | Tekst (engleski) |
|---|---|---|
| 0:00–0:20 | Agencija: stolovi puni kartica, ekran sa hiljadama sličica | "Every Monday, this agency in Serbia has around 20 weddings to deliver. That's over 100,000 photos, and someone has to look at every single one." |
| 0:20–0:45 | Mitar govori pred kamerom (na srpskom, sa engleskim titlom), ako pristane | Njegovim rečima: culling je najteži deo posla, i ako se ne završi do petka, „raspadne se sistem“. |
| 0:45–1:05 | Ti, pred kamerom | "He didn't ask for an AI that picks photos for him. His team had tried several AI tools, and they still checked every photo. He asked for something he could trust." |
| 1:05–1:50 | Snimak ekrana: folder svadbe → izveštaj sa grupama, keep / review | "Photoristic takes the photos of all photographers, groups each moment of the day, and picks the best frames. It knows the bride from a guest in the background. No moment is ever lost, and when it's unsure, it asks." |
| 1:50–2:10 | Ksenija ili Peđa za stolom (ako pristanu) | Rečenica o cilju: „ne dva sata, nego 15–20 minuta“. |
| 2:10–2:40 | Ceo tim, svako po 5–8 s | Ime, uloga i šta je doprineo. |
| 2:40–2:55 | Ceo tim zajedno | "We're building it with our first customer, week by week. With Smart Start, we'll turn it into a product for studios across Europe." |

> Napomena:
> - Snimke u agenciji praviti samo uz dozvolu, i bez lica gostiju na ekranu. Za demo koristi sličice bez prepoznatljivih lica ili ih zamuti.
> - 100.000 fotografija je računica: 20 svadbi × 5.000–6.000.

## MENTORSHIP (max 200 words)

**Our ideal mentor** has built and sold software to creative professionals (photographers, videographers, designers), ideally inside the Adobe ecosystem (Lightroom plugins, Adobe Exchange) or at a photo-tech company. We would value experience in **pricing for seasonal small businesses**, in **taking a product from the Balkans to EU and US customers**, and in GDPR for products that process biometric data. The most valuable network for us includes wedding and event photographer associations and educators, editing and outsourcing companies, photo software companies and early-stage investors in creator tools.

**Our single most important question:** What proof does a studio need before it stops re-checking every photo, and how do we turn that proof into a product they will pay for per wedding?

## FOR RETURNING PROJECTS ONLY

N/A: this is our first application to an Innovation Fund program.

> Napomena: polje ne sme biti prazno, zato upisujemo „N/A“.

## SIMPLIFIED BUDGET (9 months, VAT excluded)

| Cost category | Description | Amount (RSD) |
|---|---|---|
| Human resources | Two co-founders, gross-2: CEO (business, customer validation, ML development) 9 × 232.000; CTO (AI engineering, desktop app, integration with studio software) 9 × 232.000 | 4.176.000 |
| Office rent and business support | Coworking for 2 people 9 × 17.000; bookkeeping 9 × 15.000; company registration and bank fees on the dedicated project account (45.500) | 333.500 |
| Equipment and supplies needed for development | New development workstation with a 24 GB GPU, to optimise the AI model for the hardware studios have and to run it locally, months 3–9 (450.000); encrypted storage for test weddings (40.000); AI coding assistant, 2 licences × 9 × 11.750 (211.500); subscriptions to existing culling tools, to test them on the same weddings in parallel with development (120.000) | 821.500 |
| External development and/or business services | Rented cloud GPU for comparing large visual models before the model is chosen, months 1–4, about 310 hours (154.000); UX design of the review screen for the "please look" cases (100.000); prior-art and patentability search by a patent attorney (80.000); trademark application, word mark and logo (53.000); participant platform for about 16 moderated problem and solution interviews with photographers in the EU and US (130.000); professional photographers labelling test datasets: reference selections for past weddings (80.000); licence agreement and data processing agreement with the partner agency, by a lawyer (72.000) | 669.000 |
| **TOTAL PROJECT COSTS** | | **6.000.000** |
| Mentorship support | | 600.000 |
| **TOTAL PROJECT BUDGET** | | **6.600.000** |

> Napomena: iznosi su predlog i treba ih uskladiti sa stvarnim timom. Pravila:
> - bez marketinga;
> - samo nova oprema;
> - plata najviše 450.000 bruto 2 mesečno.
>
> **Stavke preuzete iz budžeta prethodnog projekta** (`Prilog_4_-_Budzet_EN_SILA_v2 (2).xlsx`, 16. 11.):
> - AI coding assistant: 200 € mesečno × 9 ≈ 211.500 RSD (tamo 170.990 za 6 meseci; https://claude.com/pricing). Upisano kao dve licence po 100 € mesečno (2 × 9 × 11.750), jer tim ima dva programera.
> - Platforma za regrutovanje učesnika intervjua: 130.000 RSD za oko 16 moderisanih intervjua (tamo 129.910; https://www.respondent.io/pricing). U tabeli se zove „participant platform“, a ne „recruiting“, da ne liči na neprihvatljive „troškove zapošljavanja“. Stari budžet ju je u „širem“ računanju brojao kao marketing; ovde je to validacija problema i rešenja, ali potvrdi sa Fondom.
> - Pravni savetnik za biometriju (tamo ponuda od 483.000) namerno nije unet (odluka 16. 11.). Umesto njega je u trećem krugu dodata mala pravna stavka od 72.000 (vidi dole).
> - UX dizajn je 100.000 RSD (tamo ponuda od 81.600 za mobilnu aplikaciju).
> - Žig: 53.000 RSD (tamo 52.560, kalkulator ZIS-a). Bankarske naknade namenskog računa: oko 17.000 za 9 meseci (tamo 11.410 za 6), u stavci sa registracijom firme.
> - **Nije preuzeto, jer je marketing neprihvatljiv trošak:** demo i prodajni video, Gitex i Adriatic Luxury Summit, hotel i avionske karte, LinkedIn/Meta oglasi. Kamere i oprema za video-nadzor nisu relevantne za ovaj proizvod.
>
> **Izmene 16. 11. (drugi krug):**
> - **Apple laptop (250.000) je izbačen.** MVP se instalira u jednoj agenciji, pa testiranje na macOS-u nije potrebno u ovih 9 meseci. Vrati ga samo ako agencija radi na Mac računarima.
> - **Pretplate na konkurentske alate: 120.000 RSD.** To je procena (oko 1.000 € za 3–4 alata tokom projekta), jer je potvrđena samo cena Aftershoot Selecta; pre slanja proveri cenovnike. Ovo podržava poređenje sa liderom na tržištu, koje Q9 već obećava.
> - **Ostatak od laptopa je otišao u plate**; cloud GPU je 154.000 (oko 310 sati).
>
> **Plate (16. 11.):** dva suosnivača, jednako: 2 × 9 × 232.000 = 4.176.000 RSD. Granica od 450.000 bruto 2 po osobi se ne može dostići: 2 × 9 × 450.000 = 8.100.000, više od celog budžeta od 6.000.000. Plate zato ograničava ukupan budžet; svakih 18.000 RSD skinutih sa drugih stavki podiže obe plate za 1.000 mesečno. Oboje imate i druge poslove, pa proverite u pravilniku da li plata iz projekta traži određeni procenat angažovanja u novoj firmi.
>
> **Izmene 16. 11. (treći krug, pregled budžeta):**
> - **„Paid validation with studios“ → obeležavanje podataka (80.000).** Plaćanje studijima je ličilo na podsticaj kupcima i sudaralo se sa Q9, gde studiji plaćaju nama (odluka 16. 11.: nema besplatnih pilota, plaćanje je dokaz stvarne potrebe). Sada stavka pokriva ono što Q5 obećava: test skupove koje obeležavaju profesionalni fotografi.
> - **Radna stanica:** izbačeno „matches a typical studio PC“, jer računar od 450.000 nije tipičan. Upisano je „24 GB GPU“; to je moja pretpostavka, upiši stvarnu konfiguraciju iz ponude i proveri da je 450.000 cena bez PDV-a.
> - **Cloud GPU i radna stanica** sada imaju podelu po mesecima (cloud M1–4 za izbor modela, radna stanica M3–9 za optimizaciju i lokalni rad), da ne liče na duplo plaćanje. Slaže se sa Q5.
> - **Patent:** „freedom-to-operate“ je zamenjeno sa „prior-art and patentability search“ ovde i u Q10, jer pravo FTO mišljenje košta nekoliko hiljada evra.
> - **UX:** dodato „for the "please look" cases“, da se slaže sa Q3 (rezultat se inače vidi u softveru koji studio već koristi).
> - **Nova pravna stavka (72.000):** ugovor o licenci i ugovor o obradi podataka sa agencijom. Pokriva cilj iz Q9 (plaćeni ugovor do kraja projekta) i GDPR. Iznos je procena bez ponude. Novac je skinut sa coworkinga: 9 × 25.000 → 9 × 17.000 (225.000 → 153.000).
> - **Zbir:** 4.176.000 + 333.500 + 821.500 + 669.000 = 6.000.000. Plate su nepromenjene.

---

## Izvori

Obrazac traži da se navedu izvori. U tekstu su skraćeni u zagradama; u PDF-u ih možeš pretvoriti u linkove.

- Imagen, vreme cullinga i broj kadrova: https://imagen-ai.com/valuable-tips/how-long-photo-culling-takes-for-wedding-photographers/
- Shotkit, anketa o isporuci (1.850 fotografa, 2023): https://shotkit.com/wedding-photo-delivery-survey/
- Fstoppers / YPWP, raspodela vremena: https://fstoppers.com/news/survey-wedding-photographers-shows-taking-pictures-accounts-only-4-their-time-458050
- Lightroom Assisted Culling, povratne informacije korisnika: https://community.adobe.com/questions-680/early-access-assisted-culling-lightroom-ecosystem-desktop-908852/index2.html
- Trustpilot, Aftershoot: https://www.trustpilot.com/review/aftershoot.com?stars=3
- Adventure Wedding Academy: https://adventureweddingacademy.com/culling-software-for-photographers/
- CDC, broj brakova u SAD: https://www.cdc.gov/nchs/data/dvs/marriage-divorce/national-marriage-divorce-rates-00-24.pdf
- Eurostat, preko Sofia Globe: https://sofiaglobe.com/2026/03/22/eurostat-since-1964-marriage-rate-in-eu-has-more-than-halved-divorce-rate-has-doubled/
- RZS, preko Vremena: https://vreme.com/drustvo/brak-razvod-statistika-demografija-rzs/
- The Knot 2026: https://www.theknot.com/content/wedding-budget-ways-to-save-money
- GII Research, tržište svadbene fotografije: https://www.giiresearch.com/report/go1793964-wedding-photography.html
- Destatis, brakovi u Nemačkoj: https://www.destatis.de/DE/Themen/Gesellschaft-Umwelt/Bevoelkerung/Eheschliessungen-Ehescheidungen-Lebenspartnerschaften/_inhalt.html
- ISTAT, brakovi u Italiji 2024: https://www.istat.it/comunicato-stampa/matrimoni-unioni-civili-separazioni-e-divorzi-anno-2024/
- Aftershoot Snapshot 2025 (podaci firme): https://aftershoot.com/blog/aftershoot-snapshot-2025/
- TechCrunch o Imagenu: https://techcrunch.com/2022/12/19/imagenai-which-uses-ai-to-personalize-photo-editing-styles-lands-30m
- Zenfolio / PPA, SOPI 2025: https://zenfolio.com/sopi/2025-april/ (12,9 % potvrđeno preko https://www.digitalcameraworld.com/cameras/only-12-3-percent-of-respondents-didnt-use-ai-in-last-years-state-of-the-photography-industry-survey-will-this-year-prove-any-different)
- GDPR, Recital 51: https://gdpr-text.com/en/read/recital-51
- Lightroom Assisted Culling, Early Access (PetaPixel, 3. 11. 2025): https://petapixel.com/2025/11/03/lightrooms-new-features-ai-culling-auto-dust-removal-color-variance-slider-and-more
- Cena Aftershoota: https://aftershoot.com/blog/aftershoot-pricing-tiers/ i https://www.pricingsaas.com/companies/aftershoot
- Aftershoot, vodič za svadbe (ručno usklađivanje satova): https://aftershoot.com/blog/cull-wedding-photos/
- Narrative, FAQ o cullingu (usklađivanje satova): https://narrative.so/blog/photo-culling-complete-faq
- Imagen cloud obrada: https://imagen-ai.com/aftershoot-vs-photo-mechanic-vs-imagen/
- WeEdit, outsourcing cullinga ($0,06 po slici): https://weedit.photos/culling-and-choosing
- RDFL, culling oko $50 (Fstoppers, 2016): https://fstoppers.com/originals/wedding-photographers-get-your-life-back-outsourcing-your-editing-142235
- FilterPixel, tri grupe Keepers / Review / Rejects: https://filterpixel.com/culling
- Aftershoot, kategorije i garancija za grupe duplikata: https://aftershoot.com/selects/
- Cene u Srbiji (Kurir): https://biznis.kurir.rs/novcanik/9947225/koliko-kosta-svadba-u-srbiji
- Bridebook Wedding Report 2026, cene u Nemačkoj: https://bridebook.com/de/article/was-kostet-ein-hochzeitsfotograf
- Reddit (r/WeddingPhotography, r/Lightroom, r/AskPhotography, r/photography): 183 teme, snimci ekrana u `docs/reddit-competition/`. Linkovi ka temama nisu sačuvani; tema se nalazi pretragom naslova na Redditu. [[TODO: za citate u Q1, Q2 i Q7 nađi link teme i proveri citat na slici]]
- Patenti:
  - https://patents.google.com/patent/US10523894
  - https://patents.google.com/patent/US10671895
  - https://patents.google.com/patent/US12131363
  - https://patents.google.com/patent/US9955033
  - Adobe, izbor reprezentativnih slika neuronskom mrežom: https://patents.google.com/patent/US9817847B2
  - Adobe, najbolja slika osobe po kvalitetu lica: https://patents.google.com/patent/US9858296B2
  - pretraga po nosiocu, bez pogodaka (16. 11. 2026): https://patents.google.com/?assignee=Aftershoot, https://patents.google.com/?assignee=ImagenAI, https://patents.google.com/?assignee=FilterPixel
- Interna istraživanja:
  - žalbe korisnika: [2026-11-10-culling-complaints.md](../docs/research/2026-11-10-culling-complaints.md)
  - konkurencija i servisi: [2026-11-14-culling-competitors-user-voice.md](../docs/research/2026-11-14-culling-competitors-user-voice.md)
  - veličina tržišta: [2026-11-14-market-size.md](../docs/research/2026-11-14-market-size.md)
  - Reddit: [2026-11-15-reddit-culling-competition.md](../docs/research/2026-11-15-reddit-culling-competition.md)

> Napomena: deo podataka o težini problema dolazi od proizvođača (Imagen, Aftershoot). Zato je svaki takav broj označen imenom izvora. Procene tržišta se razlikuju od firme do firme, pa koristimo jednu i navodimo raspon.
