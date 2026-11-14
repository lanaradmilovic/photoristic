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

> ⚠️ **Pitaj Mitra da li sme da se navede ime agencije „Foto Tajna“.** Imenovan partner mnogo jače dokazuje traction. Ako ne sme, zameni ga sa „a Belgrade wedding photo agency“ [[TODO: proveri grad]].

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

**Team Name:** [[TODO: ime tima kako je registrovano]]

**DESCRIPTION of the project in one sentence:**
Co-developed with a Serbian photo agency that covers about 300 weddings a year, Photoristic groups the 2,000–6,000 photos that several photographers take at a wedding into moments and pre-selects the best frames of each, with no profile training, so hours of culling become a 15–20-minute check in which no good photo is lost.

**DURATION of the project (in months):** 9

**Industry/Sector:** Information and communication technologies, Artificial Intelligence [[TODO: proveri tačan naziv koji si štiklirala na portalu]]

> Napomena uz opis: „no upload“ je izbačeno. Aftershoot i Narrative već rade lokalno, pa to nije razlika prema lideru (`docs/research/2026-11-14-culling-competitors-user-voice.md`, odeljak 3.2).
>
> Napomena: biram 9 meseci, maksimum. Pravilnik traži da se izveštaj o prototipu preda tek u drugoj polovini projekta, a nama treba jedna puna svadbena sezona testiranja (proleće). Sektor IKT/AI je prioritetna oblast. Kreativne industrije su druga opcija, ali AI nosi više težine.

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

> Napomena: „Concept Validation“ bi nas potcenio, jer imamo radni prototip i merenja. Za inovaciju biram „Advanced“, a ne „High“. Pojedinačne tehnike (embeddinzi, lica, VLM) već postoje. Novo je kako ih kombinujemo: dva fotografa u jednoj liniji, sigurnosna pravila i rad bez treniranja. Ocenjivači kažnjavaju precenjivanje, a „Advanced“ odgovara onome što tekst dokazuje. Ako želiš „High“, tekst o prednosti mora biti još jači.

---

## PROBLEM

### Q1. The problem, how you learned about it, size and severity (max 300 words)

**The problem came to us from a customer.** In September 2026 the owner of Foto Tajna asked us for help. His Serbian agency covers about 300 weddings a year, each with several photographers. In season they shoot about 20 weddings every weekend, and everything must be delivered by Friday. Otherwise "the system falls apart".

The bottleneck is culling: removing blurred, blinking and duplicate shots before editing can start. The owner calls it "the hardest part of the job in photography, much harder than shooting".

The agency's culler and a photographer gave us the numbers: one wedding produces 5,000–6,000 photos, and culling them takes about two hours "in perfect conditions"; in practice it stretches into the next day. At 20 weddings a weekend, that is about 40 hours of culling a week in season, a full-time job.

The agency had tried several AI tools, including market leaders Aftershoot and Imagen, and went back to manual work: the tools group similar photos, but someone still goes through every group. Their photographer: "If there are five thousand photos, I have to go through all of them again to check whether it did a good job." The culler's answer became our core rule: a bad photo left in is not really a mistake, but deleting a good one is.

**It is not just one agency.** In more than 160 Reddit threads, the most frequent complaint about AI culling tools is the same: the result must be re-checked in full, because the tools reject good photos. One Aftershoot user: "I have to go through and manually cull everything in the end. Always. Every single time." Every year there are 2.1 million weddings in the US and 1.7 million in the EU (CDC, Eurostat, 2024), and 88 % of US couples hire a photographer (The Knot, 2026).

> Napomena: citati su prevedeni sa sastanaka 21. 9. i 7. 10. (`docs/interviews/`). Broj od 40 sati nedeljno je računica: 20 svadbi × 2 h. Broj fotografija je 5–6 hiljada po svadbi, kako su rekli Peđa i Ksenija; Mitar je na prvom sastanku rekao 2–3 hiljade, pa u opisu stoji raspon 2.000–6.000. Broj sastanaka se namerno ne navodi.
>
> Reddit (`docs/research/2026-11-15-reddit-culling-competition.md`):
> - „more than 160“ je broj tema sa korisnim sadržajem (167 od 183), ne broj žalbi. Ne navodi broj žalbi.
> - Citat je Commercial_Foot3145, tema „AI culling software“, r/WeddingPhotography, stara oko 3 godine. Pre slanja otvori sliku i proveri ga.
> - Nije stalo u 300 reči, ali je dobro za odbranu pred komisijom: fotografi na Redditu navode 2,5–5 sati za 5.000 slika sa drugim fotografom (izjave pojedinaca, ne anketa). To nezavisno potvrđuje agencijina „dva sata“.
> - Broj venčanja u Srbiji je prebačen u Q7, zbog ograničenja reči.
> - Iskusni solo fotografi u Photo Mechanicu završe za 30–60 minuta. Zato svuda piše da je „dva sata“ mera agencije, za 5.000–6.000 slika više fotografa.
> - 88 % (The Knot) nije potvrđeno u proveri tržišta. Otvori izvor pre slanja.

### Q2. Who it affects most and how they cope today (max 200 words)

**Most affected:**
- **Agencies and teams with several photographers per wedding.** Work arrives in weekend peaks, and nothing can start until culling is done. Foto Tajna's culler checks 5,000–6,000 photos per wedding one by one. Photographers on Reddit reject 80–90 % of a second photographer's frames, yet must view them all.
- **Independent "artistic" photographers** who cull and edit everything themselves, typically 20–50 weddings a year (their own accounts on Reddit). Our partner photographer needs about 7 days to edit 2,000 photos, and culling comes before that.

**How they cope today:**
- **Manual culling** in Lightroom or Photo Mechanic. Experienced solo photographers cull a wedding in about an hour and often return to it after trying AI. That speed depends on one experienced person.
- **AI culling tools** (Aftershoot, Imagen, FilterPixel, Narrative Select, Lightroom Assisted Culling), from US$10 a month. Users still re-check everything. One wedding photographer on Trustpilot says Aftershoot saves only 5–10 % of the time. A professional on Reddit: "at least 25 percent of what they chose is unusable". Personal profiles need 2,500–5,000 edited photos.
- **Outsourced culling** costs about US$50–200 per wedding, takes 1–5 days and means sending every file. Uploading one wedding (80 GB) takes about 10 hours on the agency's connection.

> Napomena:
> - **20–50 svadbi godišnje** su izjave fotografa na Redditu (timovi 60–100). Raniji broj „20–30 (YPWP)“ je izbačen: tvrdnja „28 svadbi godišnje“ je oborena na proveri, a pouzdana anketa nije nađena (`docs/research/2026-11-14-market-size.md`, odeljak 2). Peđinih 5–10 su njegove svadbe pored rada u agenciji, pa ih ne navodimo kao broj.
> - **Photo Mechanic** je dodat namerno. Na Redditu je to stvarni standard: 4.000–7.000 slika za 30–60 minuta. Ocenjivač koji poznaje oblast to zna, pa je bolje da to kažemo sami i pokažemo gde ta brzina prestaje (više fotografa, angažovan culler).
> - **Cena AI alata:** Aftershoot Select je $10 mesečno uz godišnje plaćanje (potvrđeno). Zbirni cenovnici Imagena, Narrativea i FilterPixela su oboreni na proveri, pa raspon „$10–100“ više ne stoji.
> - **Citat „25 percent“** je pass-agress-ive, r/AskPhotography, star 5 meseci, o Aftershootu i Imagenu. Trustpilot recenzija je parafrazirana iz `docs/research/2026-11-10-culling-complaints.md` (odeljak 2.1).
> - **Profili 2.500–5.000 slika** se odnose pre svega na profile za editovanje (Imagen, Aftershoot). Za culling Aftershoot radi i bez profila. Zato ovde ne piše da culling traži treniranje.
> - **Outsourcing:** WeEdit naplaćuje $0,06 po poslatoj slici (oko $150 za 2.500), RDFL oko $50, a korisnici na Redditu navode oko $200. Rok je 1–5 dana, na Redditu i do dve nedelje. Raniji raspon $100–300 se odnosio na editovanje i dolazio je od Imagena.

---

## SOLUTION

### Q3. Proposed solution, concept, key features (max 300 words)

**Photoristic prepares a wedding for delivery with as little human work as possible.** Its key feature, and the core of the MVP, is culling. Next come the editing steps our customer asked for (crop, light, sharpening), so the whole package is delivery-ready after a short human review.

**How it works:**
1. **All photos of the day in one place.** All photographers put their photos into one folder.
2. **Moments, not files.** It aligns the cameras' clocks on its own, recognises the moments, such as the vows or the first dance, and groups each moment's photos across all photographers.
3. **The best frames of each moment.** It picks the strongest photos of every moment and knows who matters in the frame. A guest blinking in the background is no reason to reject the couple's photo, and an intentional closed-eye or artistically blurred shot is not rejected automatically.
4. **Safety rules.** No moment ever disappears: every moment keeps at least one photo. A photo is rejected only when a better photo of the same moment is kept. Nothing is deleted; any photo comes back in one click.
5. **Three outcomes:** keep, reject and "please look". When unsure, it does not guess; it asks.
6. **Results where the work happens:** ratings go straight into Lightroom, so the team keeps its usual workflow.

**What changes for the studio.** Today someone looks at 5,000–6,000 photos one by one. With Photoristic they look at moments: they skim the kept frames and decide only the "please look" photos. Rejects need no second check, because a reject is never the only photo of a moment. At worst, a near-identical alternative stays among the rejects; a moment is never lost. The agency's target for such a wedding: a 15–20-minute review instead of two hours, with no good photo lost.

> Napomena:
> - Namerno bez tehničkih termina, naziva modela i detalja toka obrade. Ne piše ni gde se obrada izvršava (lokalno, server), da bismo ostali slobodni.
> - **Tri ishoda nisu jedinstvena:** FilterPixel već ima „Keepers / Review / Rejects“, sa ocenom i razlogom po slici, a tri korpe ima i imagic. Aftershoot garantuje bar jednu sliku iz svake grupe duplikata, a korisnici se i dalje žale, jer grupe nisu momenti i jer izbor unutar grupe nije dobar (Reddit, odeljak 7.3). Zato prednost nije u tri korpe, nego u tome što je **odbačena slika uvek slabija verzija zadržane slike istog momenta, kod svih fotografa zajedno**. Zbog toga odbačene ne moraju da se proveravaju. To je odgovor na pitanje „pa i ovde moram sve da pregledam“.
> - Tačka 6 (Lightroom) je u planu, ne u kodu. U MVP koracima je eksplicitno navedena.
> - **Automatsko usklađivanje satova (tačka 2) je takođe u planu, ne u kodu.** Danas se grupiše po kameri. Dodato je jer je to najjasnija praznina kod konkurencije: vodiči Aftershoota i Narrativea to prepuštaju korisniku, a na Redditu se satovi usklađuju ručno. U Q5 je to korak M1–2.
> - **„Dva sata → 15–20 minuta“** je sada vezano za obim agencije (5.000–6.000 slika, više fotografa). Iskusan solo fotograf u Photo Mechanicu završi za oko sat, pa bi tvrdnja bez tog okvira mogla da se ospori.

### Q4. What makes it different and better (max 200 words)

**Existing tools detect flaws. Photoristic is built for trust: you look only at what it is unsure about, no moment is ever lost, and it works from the first wedding, with no profile training.**

- **Rejects need no second check.** Users of every tool re-check everything, so by their own accounts they save 5–30 % of the time, not the advertised "20-minute review". Aftershoot keeps one photo per duplicate group, but its groups are not moments. Our reject is always a weaker version of a kept photo of the same moment.
- **Several photographers, one story.** Aftershoot's and Narrative's guides tell users to sync camera clocks by hand. In 160+ Reddit threads nobody names a tool that aligns clocks or groups one moment shot from several cameras. Photoristic does both.
- **Knows who matters, respects intent.** Other tools read intentional closed eyes and blur as faults and judge focus on background people.
- **Learns from real decisions, not from the user's effort.** The agency gives us whole weddings before and after their culling. Studios never train a profile; competitors' profiles need 2,500+ edited photos.
- **Built with its users** and measured on their weddings. Target: a 15–20-minute review instead of two hours, zero good photos lost.

> Napomena: odgovor je prepisan prema istraživanju konkurencije (`docs/research/2026-11-14-culling-competitors-user-voice.md`, odeljak 4, i `2026-11-15-reddit-culling-competition.md`, odeljak 7). Stavke su poređane po snazi dokaza.
> - **Izbačeno „3–5 puta“.** Nije izmereno, a proizvođači već obećavaju isto (Aftershoot: 3–5 h → 20–30 min). Samo obećanje nije razlika. Razlika je izmeren rezultat, i zato je cilj naveden kao cilj.
> - **Izbačeno „no upload“.** Aftershoot, Narrative, Excire i imagic rade lokalno. Argument važi samo prema Imagenu, FilterPixelu i outsourcingu, i ostaje u Q7 kao GDPR trend.
> - **Izbačeno „Fair pricing“.** Aftershoot Select košta oko $120 godišnje, a 5–8 € po svadbi je za 40 svadbi 200–320 €. Cena ostaje u Q9, kao model za sezonski rad, ne kao prednost.
> - **„No tool we know of merges...“ je suženo.** Photo Mechanic i Lightroom spajaju po vremenu kad korisnik ručno uskladi satove. Niko ne poravnava satove sam i ne grupiše isti momenat iz više kamera. Usklađivanje satova kod nas je još u planu (vidi napomenu uz Q3).
> - **„5–30 %“** su izjave korisnika (Trustpilot, Adventure Wedding Academy, Reddit). Ima i zadovoljnih korisnika Aftershoota koji štede 2–3 sata po svadbi. Tržište nije „niko ne veruje AI-ju“, nego „mnogi ne veruju dovoljno da prestanu da proveravaju“. Budi spremna na to pitanje pred komisijom.
> - **„2,500+ edited photos“** su profili za editovanje kod Imagena i Aftershoota. Narrative i Lightroom takođe ne traže treniranje, pa „bez treniranja“ nije jedinstveno. Zato je naglasak na tome da učimo iz odluka agencije.
> - **Najvažnije:** da Photoristic problem zaista **rešava** još nije dokazano. Zato Q5 sada ima poređenje sa Aftershootom na istoj svadbi.

### Q5. Current state of technology and steps to MVP, with timeline (max 200 words)

**Today (TRL 4):** a working prototype, built in weekly iterations with Foto Tajna.
- It runs end-to-end on a real two-day wedding from the agency's photographer (about 80 GB; 2,575 photos used for tests).
- It has 157 automated tests.
- Against hand labels, it groups 95 % of 1,043 photo pairs correctly; only 0.9 % are wrongly merged.
- AI judgements of eyes, focus and expression are stable: 95–98 % agree when re-run at another image size.

**Steps to MVP (9 months), each checked with the agency:**
- **M1–2:**
  - ground truth from 10 weddings the agency has already culled (before/after);
  - JPEG from several photographers on one timeline;
  - per-photo ranking.
- **M3–4:**
  - Lightroom export and review page;
  - blind test on an 11th wedding, judged by the agency against their target: 15–20 minutes of review, zero good photos deleted;
  - the same wedding run through Aftershoot, for comparison.
- **M5–6:** runs on studio hardware (consumer GPU or Apple Silicon); installer.
- **M7–9:** live use at Foto Tajna in the spring season and at 5–10 more studios; measure time saved, photos lost and willingness to pay.

**Next, as the agency prioritised:** crop and straightening, then light and sharpening.

> Napomena: koraci prate tranše Fonda. Validacija tržišta je do M3, izveštaj o MVP-u u drugoj polovini projekta, poslovni model na kraju. Mitar je rekao da su obrađene svadbe spremne u novembru. [[TODO: proveri da li 10 svadbi „pre i posle cullinga“ stiže u isto vreme.]]
>
> - **Poređenje sa Aftershootom je novo.** Oba istraživanja konkurencije kažu isto: bez poređenja na istoj svadbi tvrdnja „bolji smo“ nema osnovu. Spoljna referenca za metriku: jedan nezavisni blog smatra prihvatljivim da AI odbaci manje od oko 2 % slika koje fotograf na kraju isporuči; naš cilj je 0. Ako ne želiš da se obavežeš na poređenje, obriši tu stavku.
> - **Biranje najboljeg kadra još nije rešeno.** Merenja od 12. do 14. 11. pokazuju da model, kad poredi kadrove, bira po redosledu, a ne po slici (isti pobednik u oba redosleda u 12–26 od 53 grupe, sa dva modela i tri prompta). Ocena svake slike posebno je stabilna (odatle 95–98 %), ali u oko polovini grupa ne razdvaja kadrove. Zato u M1–2 stoji „per-photo ranking“ i referentni izbor agencije. Tekst ovo ne prećutkuje, ali ga i ne ističe. Ako komisija pita, ovo je iskren odgovor: `docs/research/2026-11-14-ranking-full-model-and-per-photo.md`.

### Q6. Shared with potential customers? Feedback? (max 200 words)

**Yes. The product is shaped together with its first customer, Foto Tajna** (about 300 weddings a year).

- **September 2026:** a call and an on-site meeting with the owner, who brought us the problem. He agreed that we may sell and patent the product. He asked only that we not sell to his ten or so direct local competitors.
- **October 2026:** a working session with the owner, the agency's culler and a photographer. Together we fixed:
  - the success criteria: "Someone will have to look, but not for two hours: finish the package in fifteen, twenty minutes";
  - the priorities: culling first, then crop, light and sharpening;
  - the input: JPEG, because photos are printed and sold at the wedding;
  - the rule "never delete a good photo".

  The photographer handed us a full two-day wedding for development.
- **Since then:** weekly sprints with a Thursday check-in. The agency will provide 10 already-culled weddings as ground truth and will judge our selection on an 11th.

On existing tools: "Sometimes we need those closed eyes" and "I have to go through all the photos again."

[[TODO: drugi klijenti. Ko još, kada ste razgovarali i šta su rekli, makar jedna rečenica po klijentu. Ako ih nema u pisanom obliku, napiši mi šta znaš i dopisaću.]]

> Napomena: proveri da li sprintovi sa Peđom četvrtkom zaista teku. U intervjuu piše samo da je to dogovoreno. Ako ne teku, napiši „we agreed weekly sprints“.

---

## MARKET POTENTIAL

### Q7. Market size and trends (max 300 words)

**Market size:**
- Analysts estimate global wedding photography at **US$16–26 billion**, growing 5–8 % a year (Global Industry Analysts: US$25.8 billion in 2024, 7.4 % a year to 2030).
- Weddings per year: 2.1 million in the US (CDC, 2024) and 1.7 million in the EU (Eurostat, 2024), of which 349,000 in Germany (Destatis, 2025) and 173,000 in Italy (ISTAT, 2024); 29,402 in Serbia (RZS, 2025).
- The number of weddings is stable, not growing. Demand for culling grows with photos per wedding, photographers per wedding and AI adoption.

**Our serviceable market** (our estimate): about 3.3 million photographed weddings a year in the US and EU. At €5–10 per wedding for culling, that is **€17–33 million a year**.

**Proof that photographers pay for this:** Aftershoot reports 188,000 photographers and 8.8 billion images processed in 2025 (company data). Imagen raised US$30 million in 2022 and reported over US$10 million in annual recurring revenue (TechCrunch).

**Trends:**
1. **AI is standard, trust is not.** Only 12.9 % of photographers use no AI (Zenfolio/PPA, 2025). Yet Reddit moderators warn of vendor astroturfing around these tools. The question is no longer "AI or not" but "which AI can I trust".
2. **More frames per moment.** Photographers on Reddit report going from about 1,500 frames per wedding before mirrorless cameras to 3,000–5,000 now, and 4,000–10,000 with two photographers.
3. **Privacy regulation.** GDPR treats face recognition data as biometric data. This favours tools that process guests' faces locally.
4. **The incumbent has entered.** Adobe added Assisted Culling to Lightroom (Early Access in 2025, first for portraits). This validates the need, but it does not stack across several photographers' folders, and one user calls it "worse than not using the tool at all".

**Beyond weddings,** the same engine fits any event covered by several photographers: corporate events, school photography, sports and press agencies.

> Napomena: izmenjeno prema `docs/research/2026-11-14-market-size.md` (odeljak 9) i Reddit istraživanju. Procena od €17–33M: 3,8M svadbi × 88 % (udeo za SAD primenjen i na EU) × €5–10. Zato piše „our estimate“. Ni 88 % ni cena 5–10 € nemaju potvrdu; jedan Mitrov broj bi ovo učvrstio.
> - **Raspon umesto jedne cifre.** Procene analitičara se jako razlikuju (15,8 do 26,1 mlrd USD; jedna čak 3,7 mlrd). Metodologija nije javna, pa piše „analysts estimate“.
> - **Broj venčanja je ravan ili pada** (EU stopa prepolovljena od 1964; Srbija 36.542 u 2011, 29.402 u 2025). Bolje je da to kažemo sami i rast vežemo za broj kadrova, broj fotografa i AI.
> - **Izbačeno, jer nije prošlo proveru:** VSCO 83 %, rast AI softvera 15,4 % (GII), Canon R5 Mark II 30 fps, i BLS 145.000 (to su svi fotografi, ne svadbeni, pa broj više zbunjuje nego što pomaže).
> - **Aftershoot: „processed“, ne „culled“.** Njihova strana meša culling i editovanje.
> - **Imagen ARR** je izjava njihovog direktora iz 2022.
> - **Izvore citiraj primarno:** Eurostat (tabele `demo_nind`, `tps00206`) i stat.gov.rs, ne Sofia Globe i Vreme.
> - **Opciono za trend 1:** noviji Zenfolio SOPI 2026 („almost 50 % of photographers use AI on a weekly basis“). Otvori zenfolio.com/sopi/2026-april i proveri pre navođenja.
> - **Opciono za trend 3:** španski AEPD je kaznio GSMA sa 200.000 € zbog prepoznavanja lica posetilaca bez procene uticaja (TechCrunch, 2023). Nije prošlo proveru, pa ga otvori pre navođenja.
> - **Trend 4:** citat je jollyllama, r/Lightroom, star oko 9 meseci. „Ne pravi stekove preko više foldera“ važi za Lightroom Classic, po prijavama korisnika.
> - Susedna tržišta (škole, sport, korporativni događaji) nemaju nijedan pouzdan broj. Zato ostaju samo kao jedna rečenica.

### Q8. Target group and early adopters (max 200 words)

**First customer: Foto Tajna.**
- Covers about 300 weddings a year, about 20 every weekend in season.
- Several photographers per wedding, JPEG workflow.
- Pilot from month 1.

**Early adopters:**
1. **Agencies and teams with several photographers per event** that cull in-house. For them culling is the bottleneck between the weekend and delivery. Such teams shoot 60–100 weddings a year.
2. **Independent "artistic" photographers** who cull and edit everything themselves, first those who work with a second photographer. The agency owner pointed us to them as the strongest market: the tool would shorten their post-production "brutally", and there are more of them every year. Our photographer partner is one of them (5–10 own weddings a year).
3. **Studios in Serbia and the Western Balkans:**
   - reached personally through our partner's network;
   - price-sensitive, since full-day packages cost €600–800 (Kurir).
4. **EU studios in privacy-sensitive markets** such as Germany. There a wedding photographer costs €1,656 on average (Bridebook Wedding Report, 2026), and processing guests' faces locally is a buying argument.

**Later:** editing and outsourcing companies that cull for many photographers.

**By agreement with our first customer,** we will not sell to his ten or so direct local competitors.

**Not targeted:** wildlife, sports-only and macro photography.

> Napomena: izmenjeno prema istraživanjima od 14. i 15. 11.
> - **Redosled ostaje, i sada ima dokaz.** Na Redditu su solo fotografi najskeptičniji prema AI-ju i najbrži ručno (Photo Mechanic), a timovi sa više fotografa imaju jači bol. Zato je kod solo fotografa dodato „first those who work with a second photographer“.
> - **60–100 svadbi godišnje kod timova** su izjave sa Reddita (jedna firma sa 40 fotografa: 790 svadbi u 2023). Nije anketa.
> - **Nemačka 1.656 €** (Bridebook 2026, anketa parova; ceo dan oko 1.940 €) zamenjuje 3.050 € (Fearless Photographers), jer je taj izvor ocenjen kao nepouzdan.
> - **Izbačeno „underserved by US tools priced per seat in dollars“.** Aftershoot Select košta oko $10 mesečno, pa tvrdnja ne stoji.
> - **„nothing is uploaded“ → „processing guests' faces locally“.** Lokalna obrada nije razlika prema Aftershootu, ali jeste argument za GDPR.
> - Broj fotografa i agencija u Srbiji i regionu nije nađen. Mogući izvor: APR, šifra delatnosti 74.20.
> - Cene u Srbiji (Kurir) nisu proverene u ovom krugu.

### Q9. Business model and roll-out (max 300 words)

**Business model:** a licence priced by usage, matching the seasonal income of studios.
- **Pay per wedding:** about €5–8 per event, to be validated in the pilot. We price against hours of skilled work and against outsourced culling (about US$50–200 per wedding, 1–5 days), not against the cheapest subscription: Aftershoot's culling plan costs about US$120 a year, and its users still re-check everything. There is no cost in the off-season.
- **Agency season pass:** a yearly flat fee for unlimited events and several seats. For Foto Tajna the value is capacity: about 40 hours of culling every weekend of the season.
- **Fair terms:** no auto-renewal traps and no lock-in, because results are standard Lightroom ratings.
- **High margin:** the AI runs on the customer's hardware, so the cost per wedding is close to zero.

**Roll-out:**
1. **This project (months 1–9):**
   - Foto Tajna as the first live user, with the goal of a paid contract by the end of the project;
   - then 5–10 studios in Serbia and the region, free in exchange for data and feedback;
   - measured results (minutes of review, photos lost, a head-to-head with the market leader) become our sales evidence.
2. **Year 2, regional launch:** Serbia, Croatia, Bosnia and Herzegovina, Montenegro, North Macedonia and Slovenia, through our partner's network, photographer associations and workshops.
3. **Year 2–3, EU launch:** the DACH countries and Italy, through the Adobe Lightroom plugin marketplace, wedding photography educators and outsourcing partners.
4. **Expansion:**
   - the editing steps our customer already asked for (crop, light, sharpening);
   - a curated gallery for the couple, which raises revenue per wedding. Couples already pay extra for edited packages.
   - other events covered by several photographers.

**Illustration** (our estimate):
- 1 % of photographed weddings in the US and EU at €7 is about **€230,000 a year**;
- 1,000 studios with 40 weddings each at €6 is **€240,000**.

> Napomena: pitaj Mitra „koliko biste platili po svadbi ili po sezoni?“, makar okvirno. Jedan njegov broj vredi više od svih procena. Ako ga dobiješ, dodaj ga u Q6 i Q9.
>
> Izmenjeno prema istraživanjima od 14. i 15. 11.:
> - **Cena nije naš adut, i tekst to sada kaže.** 5–8 € po svadbi je za fotografa sa 40 svadbi 200–320 € godišnje, više od Aftershoot Selecta (oko $120). Zato se poredimo sa satima rada i sa outsourcingom. Za solo fotografe ovo ostaje slaba tačka; za agencije je sezonska karta jači argument.
> - **Outsourcing $50–200, 1–5 dana:** WeEdit $0,06 po poslatoj slici (oko $150 za 2.500), RDFL oko $50 (2016), Reddit oko $200. Raniji raspon $160–200 nije potvrđen.
> - **Plaćanje po svadbi** kod AI alata još niko ne nudi, a kod servisa je uobičajeno i hvaljeno (Wildernis Lab, $100–125 po svadbi). Otpor pretplatama na Redditu je stvaran.
> - **Kanali:** Reddit zajednice su neprijateljske prema nalozima proizvođača (moderatori upozoravaju na astroturfing). Zato u roll-outu ostaju lična mreža, udruženja i edukatori, a forumi se ne navode kao kanal.

### Q10. Patent search and IP position (max 200 words)

**Search:** we did a preliminary search on Google Patents. Related patents exist on best-of-burst selection:
- Apple US 10,523,894 (keeper images from a burst; listed as expired);
- Microsoft US 10,671,895 (best of burst with a learned quality model);
- Shutterfly US 12,131,363 (similarity-based burst grouping);
- Amazon US 9,955,033 (preferred image from several captures).

Our approach differs in three ways:
- it aligns several cameras on one timeline;
- it groups moments by combining image embeddings, face identities and time;
- its safety rules forbid rejection under uncertainty.

A formal freedom-to-operate search with a patent attorney is planned within the project.

**IP position:**
- The code is our own: about 5,000 lines of Python and 157 tests. It will be transferred to the new company.
- Our first customer has agreed that the product is ours to sell and patent.
- The third-party models are open, with Apache 2.0 licences that allow commercial use: DINOv2, RT-DETR v2, AuraFace and Qwen3.5.
- Our core assets are the know-how and the labelled data from real weddings.

> ⚠️ Napomena:
> 1. Mitrova saglasnost je zasad samo usmena („radi što hoćeš od programa“). Zamoli ga da to potvrdi jednim mejlom, zajedno sa izuzetkom za restoranske fotografe.
> 2. **Kome pripada kod?** Ako je projekat rađen u okviru posla ili na opremi poslodavca, proveri ugovor. IP mora pripasti novoj firmi.
> 3. Licence su proverene 14. 11. 2026. na Hugging Face model kartama.

---

## TEAM BEHIND THE IDEA

### Q11. Why you are the right team (max 400 words)

[[TODO: podaci o timu. Za svakog člana: ime, uloga, iskustvo, trenutni posao, obrazovanje.]]

Kostur odgovora:
- **Zašto mi:** problem nismo izmislili, nego nam ga je doneo kupac, i proizvod gradimo sa njim, sedmicu po sedmicu. U jednom mesecu, od drugog sastanka do danas, napravili smo prototip koji radi na njihovoj svadbi. To je najbolji dokaz da tim isporučuje.
- **Tehnika:** Lana (ML pipeline, merenja, VLM na sopstvenom serveru).
  - Iz intervjua: „izdvajanje mladenaca prepoznavanjem lica već postoji iz ranijeg proizvoda“. Ako je to tvoj raniji proizvod, to je jak dokaz iskustva u domenu. [[TODO: koji proizvod, šta radi, koliko korisnika]]
- **Tržište i odnos sa kupcima:** [[TODO]]
- **Operacije i finansije:** [[TODO]]

> ⚠️ **Tim nosi 40 poena.** Fond traži da tim pokrije i tehniku i tržište.
> - **Razmisli o Peđi kao članu tima.** On je fotograf sa sopstvenim svadbama i radi u agenciji. Dao nam je podatke i definisao prioritete. Sa njim bi tim dobio pravo iskustvo u domenu.
> - Uslov: najmanje 51 % članova ne sme imati udeo u firmama u Srbiji, a suosnivači ne smeju imati udeo nigde. Ako Peđa ima preduzetničku radnju, može biti član tima, ali ne i suosnivač.
> - Isto važi i za Mitra kao savetnika: on nije član tima, ali može da se pojavi u videu.

### Team member tables (do 5 osoba)

Za svakog člana: puno ime / uloga u projektu / relevantno iskustvo / trenutni posao / obrazovanje. [[TODO]]

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

**Ideal mentor:** someone who has built and sold software to creative professionals (photographers, videographers, designers), ideally inside the Adobe ecosystem (Lightroom plugins, Adobe Exchange) or at a photo-tech company.

**Desirable experience:**
- pricing for seasonal small businesses;
- taking a product from the Balkans to EU and US customers;
- GDPR for products that process biometric data.

**Valuable network:**
- wedding and event photographer associations and educators;
- editing and outsourcing companies;
- photo software companies;
- early-stage investors in creator tools.

**Our single most important question:** What proof does a studio need before it stops re-checking every photo, and how do we turn that proof into a product they will pay for per wedding?

## FOR RETURNING PROJECTS ONLY

N/A: this is our first application to an Innovation Fund program.

> Napomena: polje ne sme biti prazno, zato upisujemo „N/A“.

## SIMPLIFIED BUDGET (9 months, VAT excluded)

| Cost category | Description | Amount (RSD) |
|---|---|---|
| Human resources | [[TODO: prema timu]] Draft for 3 people, gross-2: technical lead / ML engineer 9 × 200.000; software engineer (desktop app, Lightroom export) 9 × 170.000; product & customer validation (50 %) 9 × 100.000 | 4.230.000 |
| Office rent and business support | Coworking for 3 people 9 × 25.000; bookkeeping 9 × 15.000; company registration, legal and GDPR documents (data processing agreement for studios), software tool subscriptions | 600.000 |
| Equipment and supplies needed for development | New GPU workstation that matches a typical studio PC, to run and optimise the AI model locally (450.000); Apple Silicon laptop to test on macOS, which many photographers use (250.000); encrypted storage for test weddings (40.000) | 740.000 |
| External development and/or business services | Rented cloud GPU for model experiments, about 300 hours (150.000); UX design of the review screen (120.000); freedom-to-operate patent search (80.000); paid validation with studios: past weddings with their final selections and interviews (80.000) | 430.000 |
| **TOTAL PROJECT COSTS** | | **6.000.000** |
| Mentorship support | | 600.000 |
| **TOTAL PROJECT BUDGET** | | **6.600.000** |

> Napomena: iznosi su predlog i treba ih uskladiti sa stvarnim timom. Pravila:
> - bez marketinga;
> - samo nova oprema;
> - plata najviše 450.000 bruto 2 mesečno.
>
> „Paid validation with studios“ je naknada studijima za ustupanje podataka i vreme. To nije marketing, ali proveri na info sesiji ili mejlom.

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
- Interna istraživanja:
  - žalbe korisnika: [2026-11-10-culling-complaints.md](../docs/research/2026-11-10-culling-complaints.md)
  - konkurencija i servisi: [2026-11-14-culling-competitors-user-voice.md](../docs/research/2026-11-14-culling-competitors-user-voice.md)
  - veličina tržišta: [2026-11-14-market-size.md](../docs/research/2026-11-14-market-size.md)
  - Reddit: [2026-11-15-reddit-culling-competition.md](../docs/research/2026-11-15-reddit-culling-competition.md)

> Napomena: deo podataka o težini problema dolazi od proizvođača (Imagen, Aftershoot). Zato je svaki takav broj označen imenom izvora. Procene tržišta se razlikuju od firme do firme, pa koristimo jednu i navodimo raspon.
