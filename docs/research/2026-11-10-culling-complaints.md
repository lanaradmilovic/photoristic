# Žalbe korisnika na postojeće alate za culling

Prikupljeno 2026-11-10. Cilj: videti gde postojeći alati ne rade i šta od toga Photoristic može da pretvori u konkurentsku prednost.

## Kako čitati ovaj dokument

- **Izvori:**
  - Adobe Community (javni feedback threadovi za Lightroom Assisted Culling, ukupno ~370 odgovora);
  - Trustpilot (recenzije od 1 do 3 zvezdice za Aftershoot, Imagen i FilterPixel);
  - forumi: Fred Miranda, MacRumors, BCG, DxO;
  - recenzije: Fstoppers, Shotkit, Digital Camera World, Adventure Wedding Academy;
  - Mac App Store, Product Hunt;
  - četiri naučna rada o automatskom biranju fotografija.
- **Reddit nije pokriven.** Alati za pretragu i preuzimanje ne mogu da mu pristupe. G2 i Capterra su blokirani, pa G2 tvrdnje dolaze samo iz rezimea pretraživača.
- **Lightroom je prezastupljen**, jer su Adobe threadovi javni i veliki. Za Aftershoot ima malo negativnih recenzija u odnosu na ukupan broj (Trustpilot ~4.9 od ~1.600+ recenzija).
- **Ne postoji nijedan nezavisan, kontrolisan test** u kome je ista svadba puštena kroz više alata i upoređena sa fotografovim izborom. Svi procenti tačnosti koji kruže (65 %, 80 %…) potiču od proizvođača i nisu proverljivi.
- Brojevi u tabeli su **ručno prebrojani različiti korisnici/izvori**, gruba procena, ne popis.
- Žalbe su parafrazirane. Uz svaku je link ka izvoru.

---

## 1. Teme žalbi po učestalosti

| # | Tema | ~izvora | Alati | Relevantno za Photoristic? |
|---|---|---|---|---|
| 1 | **Ipak moram sve da pregledam: nema poverenja, mala ušteda** | ~20+ | svi | **Da, ovo je glavni problem** |
| 2 | Pogrešna detekcija očiju/fokusa (žmurenje, naočare, grupe, pozadinski ljudi) | ~20 | Lightroom, Aftershoot, FilterPixel | **Da** |
| 3 | Brzina, CPU/GPU, padanje programa, memorija | ~20 | Lightroom, FilterPixel, Aftershoot | Higijena |
| 4 | Cena, pretplata, otkazivanje, naplata | ~20 | Aftershoot, Imagen, FilterPixel, Evoto | **Da (poslovni model)** |
| 5 | Kontrola i UX (prečice, undo, pokreće se sam, gubi se mesto) | ~18 | Lightroom, Aftershoot | Higijena |
| 6 | Odbacuje dobre, emotivne, umetničke ili kontekstualne kadrove | ~15 | Aftershoot, Narrative, Lightroom, Optyx | **Da** |
| 7 | Duplikati: ne postoje, pogrešni ili ih zadrži previše | ~14 | Lightroom (nema), Aftershoot (previše) | **Da (već imamo)** |
| 8 | Radi samo za ljude (sport, ptice, makro, kostimi) | ~13 | Lightroom | Ne (van fokusa) |
| 9 | Pragovi i ocene nekonzistentni i nelinearni | ~9 | Lightroom | **Da** |
| 10 | Integracija sa Lightroomom/katalogom | ~9 | Narrative, Aftershoot, Lightroom | Kasnije |
| 11 | Korisnička podrška | ~7 | Aftershoot, Imagen, FilterPixel | Higijena |
| 12 | Slabo svetlo, blic, koncerti, mračne sale | ~7 | Lightroom, Aftershoot | **Da (restorani, crkve)** |
| 13 | Treniranje ličnog profila je naporno ili ne uči | ~7 | Imagen, Aftershoot, FilterPixel | **Da** |
| 14 | Grupne fotografije | ~6 | Lightroom, Aftershoot, Optyx | **Da** |
| 15 | Upload u cloud, privatnost, GDPR | ~6 | FilterPixel, Imagen | Delimično |
| 16 | Više fotografa ili više kamera na istom događaju | ~2 | (gotovo ništa) | **Neprovereno: dokaz je tanak** |

---

## 2. Teme detaljno

### 2.1 „Ipak moram sve da pregledam“ (tema br. 1)

Ovo je zajednička nit kroz sve izvore, i isto je rekao Mitar.

- **Merni podaci iz Lightrooma (motorsport):**
  - Jedan korisnik je u odbačenim našao ~1.171 dobar kadar, a alat je odobrio ~450 od ~3.800. Uhvaćeno je ~28 % upotrebljivih.
  - Drugi je u odbačenim našao još 315 dobrih, uz 160 odobrenih od 1.600 (~34 %).
  - Obojica kažu da su rezultati sa ljudima bolji.
  - [Adobe EA thread](https://community.adobe.com/questions-680/early-access-assisted-culling-lightroom-ecosystem-desktop-908852/index2.html)
- **Aftershoot:**
  - Jedan svadbeni i event fotograf (godišnji plan) kaže da mu culling štedi samo 5–10 % vremena u odnosu na ručni rad u Lightroomu, a želeo bi 30–40 %. I dalje gleda svaki kadar. [Trustpilot 3★](https://www.trustpilot.com/review/aftershoot.com?stars=3)
  - Više recenzija od 1 i 2 zvezdice: biranje nekonzistentno, pa je sve morao ručno; ručno u Lightroomu bilo brže. [Trustpilot](https://www.trustpilot.com/review/aftershoot.com?stars=1&stars=2)
- **Adventure Wedding Academy** (Aftershoot i FilterPixel na pravim svadbama): ponovo je prošla skoro svaku sliku, pa je ušteda mala. [link](https://adventureweddingacademy.com/culling-software-for-photographers/)
- **Digital Camera World** (Lightroom): ako moraš da proveravaš šta je AI uradio, AI ti nije uštedeo vreme. Sa podrazumevanim pragovima sve slike su bile „Select“. [link](https://www.digitalcameraworld.com/tech/software/lightroom-classics-assisted-photo-culling-is-a-great-idea-but-is-really-annoying-but-i-have-found-a-solution)
- **Sportski fotografi (Fred Miranda):** moraju da otvore svaku grupu da vide šta je izabrano, pa nema uštede. [link](https://www.fredmiranda.com/forum/topic/1957341)
- **Sam Adobe** u tekstu o dizajnu kaže da je poverenje najveća prepreka i da su zato uveli pravilo „kad nisi siguran, zadrži“. [adobe.design](https://adobe.design/ideas/behind-the-design-assisted-culling-in-adobe-lightroom)
- **Način na koji ljudi to zaobilaze:** nikad ne koriste „reject“, nego samo označavaju šta zadržavaju ([Jessica Whitaker](https://www.jessicawhitaker.co/blog/honest-review-of-narrative-select-how-does-it-compare-to-aftershoot-culling)). Narrative to ima kao filozofiju: sortira, ali ne odlučuje.

**Zaključak:** problem nije u tome što alati ne umeju da prepoznaju mutnu sliku, nego u tome što **korisnik ne zna kojim odlukama može da veruje**. Zato proverava sve, i ušteda nestaje.

### 2.2 Oči, fokus i ko je „subjekt“ (teme 2, 6, 14)

- **Zatvorene oči se odbacuju i kad su namerne ili emotivne.** Primeri: mlada koja plače, poza sa zatvorenim očima. Alat ne gleda da li je ta osoba uopšte važna u kadru. ([DCW Aftershoot](https://www.digitalcameraworld.com/news/i-work-smarter-not-harder-with-ai-photo-culling-software-aftershoot), [Shotkit](https://shotkit.com/aftershoot-review/), Whitaker)
- **Detekcija očiju greši u oba smera:**
  - pušta treptaje;
  - naočare za sunce čita kao oštre otvorene oči;
  - grupa od troje, od kojih dvoje žmuri, dobija ocenu „sve oči otvorene“;
  - na koncertu je pola „dobrih“ imalo zatvorene oči.
  - [Adobe LrC thread](https://community.adobe.com/questions-675/assisted-culling-feedback-thread-lrc-1627467/index3.html)
- **Pogrešan subjekt:**
  - Oštar mladoženja odbijen je zato što je neko u pozadini namerno mutan.
  - Svi detektovani ljudi tretiraju se kao subjekt.
  - Fotografije sa malom dubinom polja i fotografije celog tela odbijene su kao neoštre.
  - Adobe sam priznaje da su lica u većim grupama propuštana ili spajana. ([Adobe LrD thread](https://community.adobe.com/questions-680/assisted-culling-feedback-thread-lrd-1627465/index1.html), adobe.design)
- **Bira „uvodni“ kadar umesto vrhunca momenta.** Svadbeni fotograf sa ~30 svadbi, Aftershoot. ([Trustpilot](https://www.trustpilot.com/review/aftershoot.com?stars=1&stars=2))
- **Odbacuje umetničko zamućenje, difuzioni filter, low-key i moody kadrove.** (AWA, DCW, Optyx [Shotkit](https://shotkit.com/optyx-ai-photo-selection-tool/))

### 2.3 Duplikati i grupisanje (tema 7)

- **Lightroom:** prepoznavanje duplikata je najtraženija funkcija još od Adobe MAX 2024, ali u Lightroomu i dalje ne radi dobro.
  - Stackovanje spaja nepovezane slike (torte, kokoške i cveće u istom stacku, jedan stack od 200+).
  - Ocene su apsolutne na nivou albuma, a ne relativne unutar grupe.
- **Aftershoot** je referenca za duplikate, ali mu zameraju da **zadrži previše sličnih** (~300 izabranih naspram ~180 ručno) umesto jednog najboljeg.
- **Optyx:** namerna promena ugla tretira se kao duplikat; grupisanje mora da se podešava za svaki posao posebno.

### 2.4 Slabo svetlo, blic, sale (tema 12)

- Low-key fotografije i ljudi u tamnoj odeći označeni su kao podeksponirani. Dva skoro identična kadra dobila su ocene 36 i 64.
- Na koncertima i u malim salama ne radi detekcija očiju, a kadrovi u slabom svetlu se odbacuju.
- Jedan korisnik traži da se razdvoje kadrovi sa blicem i bez blica.
- **Akademski rad (Kuzovkin 2017):** generička mera oštrine odbacila je većinu fotografija u mračnim kolekcijama (svadba, sport, žurka), a slabo svetlo je pokvarilo i klasterovanje. [PDF](https://diglib.eg.org/bitstream/handle/10.2312/cae2017a06/a06-C30-kuzovkin.pdf)

### 2.5 Pragovi i kalibracija (tema 9)

- Pomeranje praga fokusa sa 20 na 30 menja broj odbačenih sa 9 na 387 (~900 slika).
- Ista slika dobija ocenu ispod 30, a posle otvaranja preko celog ekrana 64.
- Ponovno pokretanje daje drugačije rezultate.
- **Zaključak:** jedan „klizač“ nad apsolutnom ocenom nije razumljiv korisniku i ne gradi poverenje.

### 2.6 Treniranje profila (tema 13)

- **Imagen:** profil traži 2.000–5.000 slika. Korisnik kaže da posle dva sata nije dobio nikakav AI rezultat. Culling samo grupiše i boji oznakama. [Trustpilot](https://www.trustpilot.com/review/imagen-ai.com?stars=1&stars=2)
- **Aftershoot:** učenje AI-ja je „gnjavaža“.
- **FilterPixel:** treniranje nije pomoglo.
- **Mitrov studio** izričito neće sam da trenira alate (docs/plan.md).
- **Nema nezavisnog dokaza da učenje ličnog stila poboljšava culling.** Akademski rad (Goree 2023) pokazuje da personalizacija nekim korisnicima mnogo pomaže, a drugima ne, i da se to teško predviđa.

### 2.7 Cena i naplata (tema 4)

- Pretplata koja se plaća pored Adobea, a skupa je za one koji rade povremeno.
- Imagen naplaćuje culling posebno, a konkurenti ga daju u paketu.
- Otkazivanje samo preko chata, kroz više „da li ste sigurni“ ekrana. Naplata posle otkazivanja i obnova bez upozorenja (Aftershoot, FilterPixel, Imagen).
- Evoto: kupljeni krediti propadaju (u jednom slučaju $1.200).
- Neki su zato napravili svoj alat: jedan korisnik Aftershoota, i autor alata imagic na Product Huntu.

### 2.8 Više fotografa i više kamera (tema 16): dokaz je tanak

- U pregledanim izvorima postoje samo jedan zahtev za automatsko stackovanje preko podfoldera po kameri i jedan zahtev za „zajednički culling“ sa pomoćnikom.
- Proizvođači savetuju da korisnik **sam sinhronizuje vreme kamera** pre cullinga (Narrative) ili da filtrira po kameri (Aftershoot).
- Nijedan alat ne spaja kadrove više fotografa u jednu vremensku liniju momenata.
- **Ovo ne znači da potražnje nema**, jer su korisnici ovih alata uglavnom fotografi koji rade sami. Znači samo da je **moraš sama dokazati**, kroz razgovore sa studijima koji rade sa više fotografa.

### 2.9 Koliko je zadatak težak uopšte (akademski radovi)

- **Kuzovkin 2017:** ljudi se međusobno slabo slažu oko toga šta zadržati.
  - Fleiss kappa: svadbena ceremonija 0,42, sport 0,34, žurka 0,26, profesionalno snimanje 0,17.
- **Chang 2016:** najbolji model bira bolji od dva kadra u 73 % slučajeva, i to samo na parovima oko kojih se ljudi slažu.
  - Vlasnik fotografija bira istu favoritkinju kao publika u ~65 % serija. [PDF](https://gfx.cs.princeton.edu/pubs/Chang_2016_ATF/chang2016-triage-preprint.pdf)
- **ML-CUFED 2017** (autori i iz Adobe Researcha): kod izbora top 20 % albuma najbolji model ima preciznost ~0,41, a nasumičan izbor ~0,19. [arXiv](https://arxiv.org/pdf/1707.05911)
- **Pouka:** „savršen izbor“ ne postoji. Ni dva čoveka se ne slažu. Zato je realan cilj **ne izgubiti dobru sliku i smanjiti vreme pregleda**, a ne pogoditi ukus.

---

## 3. Od žalbe do prilike za Photoristic

| Žalba | Prilika | Šta već postoji u kodu | Šta treba dokazati |
|---|---|---|---|
| Moram sve da pregledam (#1) | **Tri korpe umesto dve:** „sigurno zadrži“, „sigurno baci“ (vrlo uska) i „pogledaj“. Proizvod se meri **minutima pregleda po svadbi** i brojem **izgubljenih dobrih slika (cilj 0)**, a ne „tačnošću“. Svaka odluka ima objašnjenje zašto. | Tvrdo pravilo „nikad ne izgubi dobru sliku“ (README, PLAN). VLM vraća razlog (planirano). | Na 3–5 Tajninih svadbi, uz Ksenijin pravi izbor: koliko minuta, koliko izgubljenih. Isto pustiti kroz Aftershoot. |
| Pogrešan subjekt, oči nevažnih ljudi (#2, #6, #14) | **Kontekst: ko je važan u kadru.** Preko identiteta lica znamo ko su mladenci. Zatvorene oči gosta u pozadini nisu razlog za odbacivanje; zatvorene oči mlade možda jesu, a možda su emocija. | `faces.py` (SCRFD + AuraFace), identiteti. | Popraviti problem „smeće-identiteta“ od sitnih pozadinskih lica (vidi faces nalaze). Proveriti na grupnim i ceremonijalnim kadrovima. |
| Bira uvodni kadar umesto vrhunca, ne razume moment (#6) | Rangiranje **unutar grupe istog momenta** (VLM vidi celu grupu), ne apsolutna ocena slike. | Grupisanje + VLM po grupi (faza 3, planirano). Podela dana na delove. | Da VLM stvarno bira vrhunac. Meriti protiv Ksenijinog izbora. |
| Duplikati loši ili ih je previše (#7) | Grupa = zamenljivi kadrovi (tvoja definicija), sa jednim predlogom najboljeg + „pogledaj“ samo kad je razlika stvarna. | Grupisanje, look-back, faces, judge (dry-run). | Grupisanje je danas tvoj najrazvijeniji deo, ali i ono što **Aftershoot već dobro radi**. Nije prednost samo po sebi. |
| Mračne sale, blic, mešano svetlo (#12) | Podešeno na **realne uslove svadbi u salama, crkvama i restoranima**, ne na studijske portrete. | Ništa specifično. Eksperiment sa normalizacijom ekspozicije je uklonjen (nije imao efekta). | Testni skup od mračnih delova svadbi. Videti gde konkurenti greše. |
| Pragovi nerazumljivi (#9) | Bez klizača nad apsolutnim ocenama: odluke relativno unutar grupe plus jasna korpa „nisam siguran“. | Grupni pristup. | UX koji Ksenija razume bez objašnjenja. |
| Treniranje je naporno (#13) | **Radi od prve svadbe bez treniranja**, a uči tiho iz ispravki koje studio ionako pravi. | Labels alat (osnova za učenje iz ispravki). | Da podrazumevano ponašanje bude dovoljno dobro bez treniranja. |
| Cena i otkazivanje (#4) | **Naplata po događaju ili po sezoni**, bez zamki pri otkazivanju. Odgovara studijima sa sezonskim radom (jun–oktobar). | — | Spremnost na plaćanje: pitati Mitra i druge studije koliko po svadbi. |
| Više fotografa (#16) | **Jedna vremenska linija za sve kamere jednog događaja**, automatsko usklađivanje satova. | Grupisanje je danas po kameri jer satovi nisu sinhronizovani (README). | Prvo potražnja (razgovori), pa tek onda razvoj. |
| Privatnost, cloud (#15) | Lokalna obrada, ništa ne izlazi. | DINOv2 i lica lokalno. VLM je na sopstvenom serveru. | Slaba prednost, jer Aftershoot i Excire takođe rade lokalno. Pomaže samo kao argument za GDPR. |
| Padanje programa, UX, prečice (#3, #5) | Osnovna stabilnost. | — | Nije prednost, samo uslov. |
| Samo ljudi, sport, ptice (#8) | **Ne ulaziti.** Fokus su svadbe i događaji. | — | — |

### Najjača priča koju ovo podržava

> Postojeći alati optimizuju **detekciju** (mutno, žmuri, duplikat) i zato korisnici i dalje proveravaju sve, a ušteda pada na 5–30 %.
> Photoristic optimizuje **poverenje**: nijedna dobra slika ne sme da se izgubi, a čovek gleda samo ono oko čega sistem nije siguran. Sistem pri tome razume ko je važan u kadru (mladenci, a ne gosti u pozadini) i radi bez treniranja.

**Ova priča je hipoteza dok nema brojeva sa Tajninih svadbi.** Bez poređenja „X minuta i 0 izgubljenih kod nas, naspram Y kod Aftershoota na istoj svadbi“ ovo je samo tvrdnja, a Smart Start i kupci traže dokaz.

---

## 4. Šta nedostaje i sledeći koraci

1. **Reddit** (r/WeddingPhotography, r/photography, r/Lightroom): pregledati ručno. Upiti: „aftershoot“, „imagen culling“, „AI culling worth it“, „assisted culling“. Najviše mi nedostaju podaci o više fotografa i o JPEG-u u velikom obimu.
2. **YouTube:** Britney Clause, „The Ultimate AI Photo Culling Face Off“ (2024): Aftershoot, FilterPixel i Narrative na istom materijalu, nije sponzorisano. https://www.youtube.com/watch?v=DBkLVlxDoEI (transkript nije bio dostupan).
3. **Probati Aftershoot** (mesec dana besplatno) na jednoj Talići svadbi i zapisati gde greši na tvojim podacima. To je jedini dokaz o konkurentu koji niko ne može da ospori.
4. **Razgovori sa studijima** koji imaju više fotografa po događaju (region, škole i mature, event agencije). Proveriti da li je tema br. 16 stvaran problem.
5. Facebook grupe svadbenih fotografa (tamo Aftershoot prima zahteve). Nije pretraživano.

## Izvori (glavni)

- Adobe Community: [LrC GA feedback](https://community.adobe.com/questions-675/assisted-culling-feedback-thread-lrc-1627467), [LrD GA feedback](https://community.adobe.com/questions-680/assisted-culling-feedback-thread-lrd-1627465/index1.html), [LrC early access](https://community.adobe.com/questions-675/early-access-assisted-culling-lrclassic-983825/index2.html), [LrD early access](https://community.adobe.com/questions-680/early-access-assisted-culling-lightroom-ecosystem-desktop-908852/index2.html), [crash bug, 19 glasova](https://community.adobe.com/bug-reports-674/p-lrc-v15-5-on-windows-assisted-culling-triggers-crash-and-memory-leaks-1637630/index1.html), [feature request AI Culling, 85 glasova](https://community.adobe.com/feature-requests-676/p-ai-culling-665458/index1.html)
- Adobe dizajn: https://adobe.design/ideas/behind-the-design-assisted-culling-in-adobe-lightroom
- Trustpilot: [Aftershoot 1–2★](https://www.trustpilot.com/review/aftershoot.com?stars=1&stars=2), [Aftershoot 3★](https://www.trustpilot.com/review/aftershoot.com?stars=3), [Imagen 1–2★](https://www.trustpilot.com/review/imagen-ai.com?stars=1&stars=2), [Imagen 3★](https://www.trustpilot.com/review/imagen-ai.com?stars=3), [FilterPixel](https://www.trustpilot.com/review/filterpixel.com?stars=1&stars=2&stars=3), [Evoto](https://www.trustpilot.com/review/evoto.ai?stars=1&stars=2)
- Forumi: [Fred Miranda sport](https://www.fredmiranda.com/forum/topic/1957341), [Fred Miranda Excire](https://www.fredmiranda.com/forum/topic/1937544/), [MacRumors Aftershoot](https://forums.macrumors.com/threads/thoughts-on-aftershoot.2396263/), [BCG](https://bcgforums.com/threads/ai-program-for-culling.20120/page-3), [DxO](https://forum.dxo.com/t/what-about-this-automated-ai-culling-and-editing/38874), [Adobe: Narrative → LrC gubi slike](https://community.adobe.com/questions-675/not-all-images-importing-from-narrative-select-973247)
- Recenzije: [Adventure Wedding Academy](https://adventureweddingacademy.com/culling-software-for-photographers/), [DCW Lightroom](https://www.digitalcameraworld.com/tech/software/lightroom-classics-assisted-photo-culling-is-a-great-idea-but-is-really-annoying-but-i-have-found-a-solution), [DCW Aftershoot](https://www.digitalcameraworld.com/news/i-work-smarter-not-harder-with-ai-photo-culling-software-aftershoot), [Fstoppers Aftershoot](https://fstoppers.com/reviews/speed-your-culling-and-editing-aftershoot-pro-and-edits-629141), [Fstoppers 2026](https://fstoppers.com/best-ai-retouching-and-culling-tools-2026), [Shotkit Aftershoot](https://shotkit.com/aftershoot-review/), [Shotkit Optyx](https://shotkit.com/optyx-ai-photo-selection-tool/), [Shotkit Narrative](https://shotkit.com/narrative-real-world-test/), [Jessica Whitaker](https://www.jessicawhitaker.co/blog/honest-review-of-narrative-select-how-does-it-compare-to-aftershoot-culling), [Sam Hurd](https://samhurdphotography.com/aftershoot-ai-editing-in-depth-review/), [Excire vs Lightroom (proizvođač)](https://excire.com/en/lightroom-classic-ai-culling-vs-excire-search-plugin/)
- Naučni radovi: [Chang 2016](https://gfx.cs.princeton.edu/pubs/Chang_2016_ATF/chang2016-triage-preprint.pdf), [Wang 2017 ML-CUFED](https://arxiv.org/pdf/1707.05911), [Kuzovkin 2017](https://diglib.eg.org/bitstream/handle/10.2312/cae2017a06/a06-C30-kuzovkin.pdf), [Goree 2023](https://ojs.aaai.org/index.php/AAAI/article/view/26395)
