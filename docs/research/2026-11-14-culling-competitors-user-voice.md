# Konkurencija za culling: alati, servisi i šta kažu korisnici

Prikupljeno 2026-11-14. Nadogradnja na [2026-11-10-culling-complaints.md](2026-11-10-culling-complaints.md); ono što je tamo već pokriveno ovde se ne ponavlja.

## Kako čitati ovaj dokument

- **Postupak:**
  - pretraga iz 5 uglova: Reddit, YouTube, G2/Capterra i cene, servisi koji rade culling za fotografe, rad sa više fotografa;
  - preuzeto 19 izvora i iz njih izvučena 71 tvrdnja;
  - 25 najvažnijih tvrdnji proverio je svaki od tri nezavisna proveravača;
  - **19 je potvrđeno, 6 oboreno.**
- **Oznake:**
  - **[potvrđeno]**: prošlo trostruku proveru;
  - **[nepotvrđeno]**: izvučeno iz izvora, ali nije provereno;
  - **[proizvođač]**: tvrdnja firme o sebi ili o konkurentu.
- **Reddit i dalje nije pokriven.** reddit.com blokira alate za preuzimanje. Reddit se ovde pojavljuje samo preko citata u tuđim tekstovima.
- **G2 se nije mogao preuzeti.** G2 podaci dolaze iz rezimea pretraživača.
- **Facebook grupe i YouTube komentari nisu dostupni.** Postoje samo naslovi YouTube videa.
- **Glas korisnika je i dalje najslabiji deo.** Gotovo sve potvrđeno potiče od proizvođača, affiliate blogova i cenovnika servisa.
- **Pristrasnost izvora:** jedan tekst primećuje da gotovo svaki članak o Lightroom AI cullingu piše firma koja prodaje konkurentski alat ([lightroom-tools](https://lightroom-tools.pages.dev/blog/lightroom-classic-ai-culling)). To važi i za ovaj skup izvora.

---

## 1. Alati, pregled

Cene su mesečne u USD. Kod plana „godišnje“ cena je preračunata po mesecu.

| Alat | Cena (nov 2026) | Lokalno / cloud | Treniranje | Više fotografa | Ušteda vremena, šta se zna |
|---|---|---|---|---|---|
| **Aftershoot** | Select (culling) $10 uz godišnje plaćanje, $15 mesečno; Complete (culling + editovanje + retuš) $45 / $55; neograničen broj slika. **[potvrđeno, proizvođač]** ([cene](https://aftershoot.com/blog/aftershoot-pricing-tiers/), [PricingSaaS](https://www.pricingsaas.com/companies/aftershoot)). Sredinom 2026. ukinuti planovi Pro i Max. | **Lokalno, radi offline**, najmanje 8 GB RAM-a **[potvrđeno]** ([support](https://support.aftershoot.com/en/articles/5353902)) | Opciono: „uči iz zamena koje napraviš“ **[proizvođač]** | Nema posebne funkcije; vodič kaže da korisnik **ručno uskladi vreme obe kamere** **[potvrđeno]** ([vodič](https://aftershoot.com/blog/cull-wedding-photos/)) | Proizvođač: 3–5 h ručno → 20–30 min pregleda. Nezavisni primer: 3h50 → 1h15, 4h30 → 1h55 (~57–67 %). Vidi 3.1. |
| **Imagen** (culling) | ~$12 godišnje / $18 mesečno, ili $0,05 po slici **[nepotvrđeno; zbirni cenovnik je oboren]** | Editovanje u cloudu **[potvrđeno]**; za culling postoji i offline desktop proizvod | Profil za editovanje | Imagen u FAQ-u ima pitanje „radi li za drugog fotografa sa drugim telom“, ali bez jasnog odgovora [nepotvrđeno] ([Imagen](https://imagen-ai.com/post/what-is-a-second-shooter.md)) | — |
| **Narrative Select** | ~$10–20 [nepotvrđeno] | Lokalno [proizvođač]. FilterPixel tvrdi da je od juna 2026. samo za macOS; Narrative kaže Mac i Windows. Protivrečno. | Ne; „AI pokazuje dokaze, ti biraš“ [proizvođač] ([compare](https://narrative.so/compare)) | Vodič kaže da korisnik može da „zaboravi da uskladi vreme kamera“, pa je to opet na korisniku [proizvođač] ([FAQ](https://narrative.so/blog/photo-culling-complete-faq)) | Korisnik na Adobe forumu ga plaća posebno samo zbog brzih pregleda, „kao Photo Mechanic“ [nepotvrđeno] |
| **FilterPixel** | Prema tri izvora ~$15/$35/$65 uz godišnje plaćanje, za 20/70/… snimanja godišnje, i $7,99 po dodatnom snimanju. **Svi zbirni cenovnici oboreni su na proveri.** | Cloud (prema konkurentima) | — | — | Sopstveni benchmark: 1.000 slika za 8 min, Aftershoot 10, Narrative 18; 3.000 RAW: ručno 204 min [proizvođač] ([FP](https://filterpixel.com/ai-photo-culling-software)). YouTube: „7.000 svadbenih fotografija za 20 minuta“, samo naslov, nije provereno ([video](https://www.youtube.com/watch?v=lZSkkoS7Y-I)) |
| **Lightroom Assisted Culling** | Uključen u Adobe pretplatu | Lokalno | Ne | Auto Stack grupiše po vremenu snimanja, pa mu neusklađeni satovi takođe smetaju [nepotvrđeno] | Opšta dostupnost jun 2026 [nepotvrđeno]. Rani tester (okt 2025): „uglavnom za portrete, još ne za svadbe“ [nepotvrđeno] ([Adobe FR](https://community.adobe.com/feature-requests-676/p-ai-culling-665458)) |
| **Excire Foto 2027** | **Jednokratno $249** **[potvrđeno]** (affiliate blog, potvrđeno i preko PetaPixela) | **Lokalno [potvrđeno]** | — | — | — |
| **imagic** | **Jednokratno €19/49/99** **[potvrđeno]** | **Lokalno [potvrđeno]** | — | — | Jedini izmeren primer: 52 HDR kadra za 18 s → 30 zadrži / 16 pogledaj / 6 odbaci [nepotvrđeno]. Zanimljivo: i on ima **tri korpe**. |
| **Optyx** | Besplatno (bez AI), Pro ~$7 [nepotvrđeno] | Obrada lokalna, ali **AI analiza traži internet** (Shotkit, maj 2026) [nepotvrđeno] | — | — | Pouzdano hvata zatvorene oči; malo koristi onima koji snimaju 1–2 kadra po momentu [nepotvrđeno] ([Shotkit](https://shotkit.com/optyx-ai-photo-selection-tool/)) |
| **Photo Mechanic** | $14,99 mesečno, $149 godišnje ili $299 trajno [nepotvrđeno] | Lokalno | Bez AI | — | ON1: ručno u LR 4–8 h, u Photo Mechanicu 2–4 h, sa AI 20–60 min **[potvrđeno da ON1 to tvrdi; metod nije naveden]** ([ON1](https://www.on1.com/blog/ai-photo-culling-for-weddings/)) |
| **Evoto, Selekt, ON1 Lightpanel** | — | — | — | — | **Nijedna tvrdnja nije prošla proveru.** |

### Ocene na platformama

- **Aftershoot na Trustpilotu (nov 2026):**
  - 4,8 od 1.808 recenzija, 98 % sa pet zvezdica [nepotvrđeno];
  - firma aktivno poziva kupce da ostave recenziju;
  - pozitivne recenzije svadbenih fotografa hvale uštedu samo uopšteno („countless hours“), **bez brojeva pre i posle**;
  - nijedna od prikazanih ne ocenjuje tačnost cullinga ([Trustpilot](https://au.trustpilot.com/review/aftershoot.com));
  - 1★ od 27. 10. 2026: otkazivanje i dalje ide kroz više „zadržavajućih“ ekrana, a firma je u odgovoru priznala da je postupak previše komplikovan.
- **Aftershoot na G2:**
  - ~4,4 od ~35 recenzija, prema rezimeu pretraživača [nepotvrđeno];
  - hvale brzinu;
  - zameraju netačne izbore, zbog kojih **i dalje sve proveravaju ručno da ne izgube dobar kadar**, kao i sporo učitavanje i skupu pretplatu.
- **PhotoFocus (Aftershoot):** „ponekad je ostavio odvojeno ono što bih ja nazvao duplikatom“; najbolje radi kad u kadru ima lica [nepotvrđeno] ([PhotoFocus](https://photofocus.com/reviews/aftershoot-review-a-timesaver-for-event-portrait-and-wedding-photographers/)).

---

## 2. Servisi koji rade culling umesto fotografa

| Servis | Cena | Rok | Napomena |
|---|---|---|---|
| **WeEdit.photos** | **$0,06 po poslatoj slici**, dakle ~$150 za 2.500. Paket Standard $119 po svadbi (culling + editovanje). **[potvrđeno, proizvođač]** | **24 h da prihvate narudžbinu + 3–5 dana** za Standard [potvrđeno] | Naplaćuje **sve poslate** slike, ne samo zadržane ([link](https://weedit.photos/culling-and-choosing)) |
| **ShootDotEdit** | **Samo pretplata:** Rollover $119 mesečno (do ~12 svadbi godišnje), Unlimited $299 mesečno **[potvrđeno]**. Rezimei pominju godišnju obavezu i $179 po dodatnoj svadbi [nepotvrđeno]. | 800–1.000 obrađenih slika za 48 h (jedan klijent, 2017) [nepotvrđeno] | Nema pojedinačne narudžbine ([Shotkit](https://shotkit.com/photo-editing-service/), [FixThePhoto](https://fixthephoto.com/shootdotedit-review.html)). Tvrdnja „$0,16 po slici za culling“ je **oborena**. |
| **RDFL** (2016) | ~$50 za culling do 5.000 slika [potvrđeno, staro] | — | ([Fstoppers 2016](https://fstoppers.com/originals/wedding-photographers-get-your-life-back-outsourcing-your-editing-142235)) |
| **The Image Salon** (2017) | — | — | JAGstudios: 24–30 h obrade po svadbi u kući; kad su dali editovanje napolje, 10–12 h; kad su dali i culling i editovanje, **2–4 h** [potvrđeno, jedan studio, staro] ([Rangefinder](https://rangefinderonline.com/?p=42887)) |

**Pouke:**

- **Ljudski culling je jeftin, ali spor.** Košta $50–150 po svadbi, a traje 1 do 5 dana, uz slanje svih fajlova napolje.
- **Gubi se kontrola.** Autor koji je protiv outsourcinga piše da AI ili tuđe oko neizbežno propušta dobre kadrove sa zatvorenim očima ili blagim neoštrinama, koji su često najbolji dokumentarni ([PetaPixel 2022](https://petapixel.com/2022/02/26/why-outsourcing-wedding-photography-editing-is-a-slippery-slope)).
- **Od kvaliteta servisa nije ništa prošlo proveru.** Nismo našli ni ocene korisnika o tome da li servisi bacaju dobre slike.

---

## 3. Šta je novo u odnosu na 2026-11-10

### 3.1 Brojevi o uštedi vremena: tri nivoa

1. **Proizvođači:**
   - Aftershoot: 3–5 h → 20–30 min;
   - ON1: AI 20–60 min;
   - FilterPixel: 3.000 RAW slika za 30 min kod Aftershoota, 204 min ručno.
   - Nijedan ne navodi kako je merio.
2. **Nezavisni blog** ([Bhattacharya, sep 2026](https://sagnikbhattacharya.com/blog/ai-culling-worth-it-wedding-photographer)): kad se uračuna i ljudski pregled, 3h50 → 1h15 i 4h30 → 1h55, dakle **~57–67 %**, a ne 83–93 %. Autor kaže da su primeri ilustrativni, ne merenja.
3. **Korisnici** (dokument od 11-10): **5–30 %**, jer i dalje gledaju sve.

**Zaključak:** razlika između obećanja (20–30 min) i stvarnosti (1–2 h, ili skoro sve ručno) je upravo **pregled zbog nepoverenja**. Photoristic cilja baš na tu razliku. Istu metu (20 minuta) proizvođači već obećavaju, pa **samo „20 minuta“ nije razlika. Razlika je u dokazu da je tih 20 minuta stvarno i bez izgubljenih slika.**

**Prag za izgubljene slike:** isti blog predlaže da je prihvatljivo da AI odbaci **manje od ~2 %** slika koje fotograf na kraju isporuči. U njegovom probnom primeru to je bilo 0,9 % i 2,7 %. Autor kaže da to nije industrijski standard [nepotvrđeno]. Ovo je korisna spoljna referenca za našu metriku „izgubljene dobre slike“: naš cilj je 0, a tržište implicitno toleriše ~2 %.

### 3.2 Lokalna obrada više nije prednost

- Aftershoot (lider na tržištu), Narrative, Excire i imagic rade lokalno. Aftershoot radi i offline. **[potvrđeno]**
- U cloudu su Imagenovo editovanje, FilterPixel, a delimično i Optyx (AI analiza).
- Korisnici na Adobe forumu izričito traže lokalni rad („This needs to happen locally“), dakle potražnja postoji, ali je vodeći alat već pokriva.

### 3.3 Jednokratna cena postoji

- Excire ($249) i imagic (€19–99) se plaćaju jednom. **[potvrđeno]**
- Naplata po događaju ili po sezoni i dalje nije viđena kod AI alata. Kod servisa je to normalno (po svadbi).
- Aftershoot je sredinom 2026. pojednostavio i pojeftinio planove, a Select košta $120 godišnje. **Cena kao argument je slaba:** $10 mesečno je teško potući.

### 3.4 Više fotografa: praznina je potvrđena, ali iz vodiča, ne iz žalbi

- **Aftershoot i Narrative u svojim vodičima prepuštaju usklađivanje satova korisniku. [potvrđeno]**
- Nezavisni blog daje konkretan primer greške: druga kamera kasni 7 minuta, pa AI uparuje kadar drugog fotografa sa pogrešnim momentom (razmena prstenova sa zavetima) i validan ugao označi kao duplikat.
  - Rešenje je ručno: pomeriti vreme snimanja u Lightroomu i ponovo pokrenuti culling.
- Digital Photography School i Fundy Designer takođe opisuju razliku u satovima kao glavni problem, koji se rešava ručno.
- **Pretraga nije našla automatsko usklađivanje satova** ni u Aftershootu, ni u Narrativeu, ni u FilterPixelu. To što ga nema u vodičima ne dokazuje da ga nema u proizvodu.
- Imagen u FAQ-u ima pitanje o drugom fotografu, ali bez jasnog odgovora. Postoji, dakle, bar pitanje korisnika.
- **I dalje nema korisničkih žalbi u većem broju**, verovatno zato što većina korisnika radi sama.

### 3.5 Obim i procenat zadržanih

- Svadbeni i komercijalni fotograf na Adobe forumu: 2.000–3.000 snimaka → **400–600 isporučenih (~15–25 %)**. Pokreće ga i poskupljenje Adobe pretplate [nepotvrđeno] ([Adobe FR](https://community.adobe.com/feature-requests-676/p-ai-culling-665458)).
- U istom threadu: strah da AI baci nezamenljiv kadar, na primer jedinu sliku rođaka koji je u međuvremenu preminuo. To je direktna podrška pravilu „nikad ne izgubi dobru sliku“.
- Aftershoot iz svake grupe duplikata zadržava bar jedan kadar. „Cull to Target“ zadržava 10–60 % albuma [proizvođač].

### 3.6 YouTube: kandidati za ručni pregled

Transkripti i komentari nisu bili dostupni. Ovo su samo naslovi:

- [The Ultimate AI Photo Culling Face Off](https://www.youtube.com/watch?v=DBkLVlxDoEI) (verovatno Britney Clause, 2024)
- [How I Cull 7,000 Wedding Photos in 20 Minutes](https://www.youtube.com/watch?v=lZSkkoS7Y-I) (FilterPixel)
- [Aftershoot Alternative, „Unbiased“ review](https://www.youtube.com/watch?v=sPXtgj_CTFw)
- [I Tested Aftershoot vs Narrative](https://www.youtube.com/watch?v=qvkAZg5pwj0), [Narrative vs Aftershoot 2025](https://www.youtube.com/watch?v=N-RomBjQ7Do), [FilterPixel vs Aftershoot](https://www.youtube.com/watch?v=1KAjpeYqEoc)
- [Photographer Saves 50% Time](https://www.youtube.com/watch?v=R-Utu3QlkFA) (FilterPixel, tvrdi 50 % uštede na cullingu)

### 3.7 Oborene tvrdnje (ne koristiti u prijavi)

- **Zbirni cenovnici Imagena, Narrativea i FilterPixela** iz tri bloga (0-3 i 1-2). Pre navođenja treba ih proveriti na sajtu proizvođača.
- ShootDotEdit „$0,16 po slici za culling, ~$480 po svadbi“ (0-3).
- „Aftershoot nema timski plan“ (0-3).
- „~$150 po svadbi za outsourcing kod 25 svadbi godišnje“ (0-3).

---

## 4. Po čemu Photoristic može biti drugačiji

### Potkrepljeno dokazima

| Razlika | Dokaz | Snaga |
|---|---|---|
| **Usmeren na poverenje, ne na detekciju:** cilj je 0 izgubljenih dobrih slika i pregled samo onoga oko čega sistem nije siguran | Korisnici i dalje sve pregledaju: 5–30 % uštede (11-10), G2 („proveravam sve ručno da ne izgubim kadar“), Adobe (strah od nezamenljivog kadra). Proizvođači obećavaju 20–30 min, a nezavisni primeri pokazuju 1–2 h. Tržište implicitno toleriše ~2 % izgubljenih. | **Jaka** (problem je potvrđen). Da ga Photoristic **rešava**, još nije dokazano. |
| **Dva fotografa u jednoj vremenskoj liniji, uz automatsko usklađivanje satova** | Vodiči Aftershoota i Narrativea prepuštaju to korisniku; primer sa 7 minuta razlike; DPS i Fundy opisuju ručno rešenje; nijedan alat nema poznatu automatiku. | **Srednja.** Praznina u proizvodima je jasna, ali je dokaz o potražnji tanak (vodiči i blogovi, ne žalbe). |
| **Radi bez treniranja** | Aftershoot i Imagen se oslanjaju na profile koji uče; žalbe na treniranje (11-10); Mitar neće da trenira. | Srednja. Narrative i Lightroom takođe ne traže treniranje, pa ovo nije jedinstveno. |
| **Brže od servisa, bez slanja fajlova napolje** | Servisi rade 1–5 dana i traže slanje svih slika; Photoristic radi isti dan, lokalno. | Srednja, kao argument protiv servisa. Cena servisa ($50–150 po svadbi) je realna referenca za cenu po svadbi. |

### Nije prednost (ne isticati kao glavno)

- **Lokalna obrada i privatnost:** Aftershoot, Narrative, Excire i imagic već rade lokalno. Argument važi samo prema Imagenu, FilterPixelu i servisima, i za GDPR priču.
- **Niska cena:** Aftershoot Select košta $120 godišnje, Excire i imagic se plaćaju jednom.
- **Grupisanje duplikata:** svi to rade, a Aftershoot je referenca (11-10).
- **„Pregled za 20 minuta“ kao obećanje:** proizvođači već obećavaju isto. Razlika može biti samo **izmeren** rezultat.
- **Tri korpe (zadrži / pogledaj / baci):** imagic ima isto, a Narrative ima „potential / unlikely“.

### Hipoteze koje tek treba dokazati

1. Pregled 2.000–3.000 slika dva fotografa traje ~20 min, uz 0 izgubljenih dobrih slika, na Tajninim svadbama sa Ksenijinim izborom kao referencom.
2. Na istoj svadbi Photoristic gubi manje dobrih slika od Aftershoota. Bez ovog poređenja tvrdnja „bolji smo“ nema osnovu.
3. Studiji sa više fotografa imaju problem sa satovima i spajanjem dovoljno često da bi platili za rešenje. To treba proveriti razgovorima.
4. Studio je spreman da plati po svadbi ili po sezoni. Raspon cena: AI alati ~$10 mesečno, servisi $50–150 po svadbi.

---

## 5. Šta i dalje nedostaje

1. **Reddit ručno**, jer alati nemaju pristup: r/WeddingPhotography, upiti „aftershoot“, „second shooter culling“, „sync camera time culling“, „AI culling worth it“.
2. **YouTube:** pogledati Face Off i video sa 7.000 slika, zapisati koliko je slika ostalo za pregled i da li je video sponzorisan.
3. **Cene Imagena, Narrativea i FilterPixela** proveriti direktno na njihovim sajtovima, jer su svi zbirni cenovnici oboreni.
4. **Probati Aftershoot** na jednoj Talići svadbi sa dva fotografa, bez ručnog usklađivanja satova, i zapisati šta se desi. To je najjači mogući dokaz za tačku 3.4.
5. **Pitati regionalne studije** da li plaćaju servise za culling i koliko.

## Izvori

- Proizvođači: [Aftershoot cene](https://aftershoot.com/blog/aftershoot-pricing-tiers/), [Aftershoot vodič za svadbe](https://aftershoot.com/blog/cull-wedding-photos/), [Aftershoot best culling](https://aftershoot.com/blog/best-culling-software/), [Aftershoot support](https://support.aftershoot.com/en/articles/5353902), [Imagen vs Aftershoot](https://imagen-ai.com/post/imagen-ai-vs-aftershoot), [Imagen second shooter](https://imagen-ai.com/post/what-is-a-second-shooter.md), [Narrative compare](https://narrative.so/compare), [Narrative FAQ](https://narrative.so/blog/photo-culling-complete-faq), [FilterPixel benchmark](https://filterpixel.com/ai-photo-culling-software), [ON1](https://www.on1.com/blog/ai-photo-culling-for-weddings/), [WeEdit](https://weedit.photos/culling-and-choosing)
- Nezavisni i polunezavisni: [Bhattacharya 2026](https://sagnikbhattacharya.com/blog/ai-culling-worth-it-wedding-photographer), [PhotoWorkout 2026 (affiliate)](https://www.photoworkout.com/?p=223718), [lightroom-tools](https://lightroom-tools.pages.dev/blog/lightroom-classic-ai-culling), [PhotoFocus](https://photofocus.com/reviews/aftershoot-review-a-timesaver-for-event-portrait-and-wedding-photographers/), [Shotkit Optyx](https://shotkit.com/optyx-ai-photo-selection-tool/), [PricingSaaS](https://www.pricingsaas.com/companies/aftershoot)
- Servisi: [Shotkit ShootDotEdit](https://shotkit.com/photo-editing-service/), [FixThePhoto (konkurent)](https://fixthephoto.com/shootdotedit-review.html), [Rangefinder 2017](https://rangefinderonline.com/?p=42887), [Fstoppers 2016](https://fstoppers.com/originals/wedding-photographers-get-your-life-back-outsourcing-your-editing-142235), [PetaPixel 2022](https://petapixel.com/2022/02/26/why-outsourcing-wedding-photography-editing-is-a-slippery-slope)
- Korisnici: [Trustpilot Aftershoot](https://au.trustpilot.com/review/aftershoot.com), [G2 Aftershoot](https://www.g2.com/products/aftershoot) (samo rezime pretraživača), [Adobe feature request AI culling](https://community.adobe.com/feature-requests-676/p-ai-culling-665458)
