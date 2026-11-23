# Intervju 3, slika po slika — Peđini komentari na stranicama sa sastanka (2026-11-19)

Šta je Peđa rekao za svaku sliku na dve stranice pokazane na sastanku 2026-11-19. Lana je
2026-11-23 ponovo preslušala snimak, išla redom po slikama i zapisala komentar i svoje razumevanje
zahteva iza svake. Ovaj fajl je dokaz; pravila izvedena iz njega su u
[requirements.md](../requirements.md). [Sažetak sastanka](2026-11-19-pedja-ksenija-grupisanje-i-izbor.md)
ostaje kao kraći pregled; gde se razlikuju, važi ovaj fajl.

Izvor svake rečenice:

- bez oznake: Lanina beleška. To je ručno zapisan transkript snimka i **glavni izvor**: gde se
  automatski transkript razlikuje, važi beleška ([spisak razlika](#gde-automatski-transkript-kaže-drugačije));
- **[stranica]**: odgovor ili napomena sačuvana na stranici tokom sastanka
  (`data/meeting/meeting_answers.json`, `data/out-4a/picks.agency.json`);
- **[transkript]**: dopuna iz automatskog transkripta (`propmt-images/meeting-1.txt`, `meeting-2.txt`,
  bez oznake govornika, mestimično nerazumljiv). Samo dodaje detalj i ne menja belešku, osim
  gde beleška protivreči sama sebi;
- **[slika]**: šta se vidi na slici ili u podacima (pregled agenta 2026-11-23). To nije Peđina izjava.

Odgovori na stranici sa parovima: **jedna** („Ista slika — dovoljna je jedna“), **obe** („Isti
trenutak, ali idu obe“), **različito** („Različit trenutak ili drugi ljudi“).

Folderi ([datasets](../datasets.md)): Talići 1 je prvi dan (2026-08-31: sesija mladenaca na brodu i
u starom gradu, veče). Talići 3, 4a i 4 su dan venčanja (2026-09-01): spremanje, prvi susret, mol,
crkva (3); crkva i venčanje u bašti (4a); zabava (4). Brojevi su `_KAD####.NEF`.

Brojevi sličnosti i razmaka za sve parove i grupe: [merenje](../research/2026-11-23-meeting-choices-vs-signals.md).

## Opšti utisak

- Grupisanje treba vratiti na veću sličnost: grupa je **bukvalno isti trenutak**, ne „jedan sličan
  momenat“. Treba da bude strože, kao što je bilo ranije.
- Primer koji je Peđa sam napravio makazama (`propmt-images/poostri-grupisanje.png`, vidi
  [X11](#pregled-grupa-isečci)): dve uspravne slike poljupca na brodu ostaju zajedno, a položena
  slika na kojoj se mlada naslanja na mladoženju i smeju se odvaja se u novu grupu.

## Stranica 1: sporni parovi (M1–M20)

`cull.py meeting --output data\meeting`, pitanje: „Da li biste mladencima isporučili jednu od ove
dve slike ili obe?“

**M1** `_KAD9971` / `_KAD9973` — 4a, 17:05, razmak 29 s. **[stranica]** obe.
- Isti je trenutak, ali ni na jednoj nisu ispali loše. Pošto postoje samo ove dve slike, daje obe.
  Da ih je bilo mnogo, pravio bi selekciju nekoliko najboljih.
- **[slika]** Dvoje gostiju sede pod suncobranom (nisu mladenci). Poza i položaj suncobrana se
  razlikuju. Ista dva kadra su u grupi P19, gde je ostavio sva tri.

**M2** `_KAD9872` / `_KAD9873` — 4a, 15:34, razmak 1 s. **[stranica]** obe.
- Bitan je momenat: izlazak iz crkve. Daje obe jer su na obe dobro ispali. Kaže da nisu skroz iste.
- Dodaje: da nisu mladenci, možda ne bi dao obe. Za mladence važi da im daješ sve slike na kojima
  su ispali dobro, a izbacuješ samo one gde su ispali loše. Da je neko drugi u pitanju, uradio bi
  selekciju.
- **[transkript]** U stvarnoj isporuci im je dao obe. „Na kraju, ako su baš iste, onda ću da
  izbacim jednu. Ali ulazak i izlazak iz crkve su specifične situacije.“
- **[slika]** Mladenci izlaze na vrata crkve. Razlika je u ruci kojom mlada maše i u koraku.

**M3** `_KAD9877` / `_KAD9878` — 4a, 15:36, ista sekunda. **[stranica]** jedna; napomena „pogleda mladence“.
- Grupna slika. Misli da je ovakvih bilo tri ili četiri i da je on dao dve.
- Gleda kako su ljudi generalno ispali. U redu je i da je neko zatvorio oči, jer je sunce bilo
  direktno, a i takav je „filmski“ kadar.
- U ovom slučaju gleda kako su ispali mladenci. Na drugoj je mladoženja ispao bolje (na prvoj ne
  gleda u aparat), pa bi dao drugu.
- Nema određenog broja slika koji mora da se isporuči mladencima posle cullinga.
- **[transkript]** Širi kadar je Đoletov, uži njegov (105 mm, izdaleka). Uži mu je lepši, ali
  „njima je bitnija ona slika da se svi vide“.
- **[slika]** Dvadesetak ljudi ispred crkve. Na drugoj su ruke podignute i mladoženja gleda u aparat.

**M4** `_KAD9862` / `_KAD9863` — 4a, 15:20, razmak 1 s. **[stranica]** jedna; napomena „druga jer je prva bzvz“.
- Gotovo iste slike. Mladoženja je na prvoj ispao loše, pa ide samo druga. Da je ispao dobro,
  mogle bi obe ako nisu skroz iste.
- **[transkript]** Ne zna koliko je osoba koja čestita bitna mladencima („ja to ne mogu da znam“).
- **[slika]** Čestitanje u crkvi: gošća grli mladoženju. Na prvoj su mu oči zatvorene, na drugoj se
  smeje. Kadar je isti (vrsta „širi-uži“ u `meeting.json` je pogrešna).

**M5** `_KAD9930` / `_KAD9931` — 4a, 16:18, razmak 4 s, položena pa uspravna. **[stranica]** obe.
- Dao bi obe. Širok kadar naspram uskog, a slična poza: zadrži obe.
- **[transkript]** Nije imao gde da se odmakne, a hteo je da se vide sa stolom: „obe bih im dao“.
- **[slika]** Mladenci stoje ispred postavljenih stolova, poza je ista. Položena pokazuje ceo sto i
  imanje, uspravna samo njih.

**M6** `_KAD8404` / `_KAD8405` — Talići 1 (stari grad), 13:11, razmak 30 s. **[stranica]** jedna.
- Jako slične slike. Izabrao bi jednu od te dve.
- **[transkript]** „Koja god“, „nije sad to toliko bitno“. Misli da je jedna njegova, a jedna Đoletova.
- **[slika]** Mlada sama u uličici. Okret glave i položaj tela se razlikuju, drugi kadar je bliži.

**M7** `_KAD8412` / `_KAD8413` — Talići 1 (stari grad), 13:13, razmak 1 s. **[stranica]** bez odgovora; napomena „ništa“.
- Jako je mračno. Ništa im ne bi dao dok prvo ne sredi sliku i vidi kakva je. On čuva RAW fajlove,
  pa se može izvući.
- **[transkript]** Ksenija: ovakvu sliku ne daju mladencima; lošu posvetli koliko može.
- **[slika]** Mladenci u senci uske ulice. Ugrađeni pregled je crno-beo i vrlo taman.

**M8** `_KAD9309` / `_KAD9310` — Talići 3, 12:31, razmak 1 s. **[stranica]** obe; napomena „jer je mlada na obe ok“.
- Obe, jer je mlada lepa na obe. Da je na nekoj ispala loše, tu bi izbacio.
- **[transkript]** „Da si ti mlada, voleo bih da imaš ove slike.“
- **[slika]** Mladenci se drže za ruke ispred kuće, oko njih deca i gosti. Razlika je u pogledu i rukama.

**M9** `_KAD8144` / `_KAD8145` — Talići 1 (brod), 11:31, razmak 7 s. **[stranica]** jedna.
- Crno-bela ili u boji: nije važno. Za njega je to ista slika kad radi culling, jer je RAW uvek u
  boji. Dovoljna je jedna.
- **[transkript]** Na jednoj su stopalo i ruke „problematični“, pa bi pre izabrao drugu (iz
  transkripta se ne vidi koju).
- **[slika]** Mladoženja sedi na brodu. Prva je crno-bela i šira, druga u boji i malo uža.

**M10** `_KAD8637` / `_KAD8638` — Talići 1 (veče), 19:13, razmak 2 s, uspravna pa položena. **[stranica]** obe; napomena „sa najbližima sve“.
- Slike sa mamom i bratom. Ostavio bi sve: obe su u redu, svi su dobro ispali.
- Opšte: kada je ista slika, na prvoj su tri osobe, a na sledećoj se pridruži četvrta, zadržava obe.
- **[transkript]** „Ja ne znam šta će njoj da se dopadne.“
- **[slika]** Tri osobe. Uspravna je cela figura, položena je uži kadar do kolena.

**M11** `_KAD9078` / `_KAD9079` — Talići 3, 11:25, razmak 29 s. **[stranica]** obe; napomena „bitan momenat prvi susret“.
- Specifičan momenat: njihov prvi susret. Bitan je kao izlazak iz crkve. Daje sve gde su ispali
  dobro, jer nema previše slika tog momenta.
- **[slika]** Mladoženja stoji sam ispred kuće i čeka. Položaj ruku se razlikuje.

**M12** `_KAD9425` / `_KAD9426` — Talići 3 (mol), 13:41, razmak 1 s. **[stranica]** bez odgovora; napomena „različite, obe“.
- To su različite slike; daje obe.
- Ispravio bi perspektivu i pomoću AI dodao deo venčanice koji nedostaje (korisno za kasniji korak obrade).
- **[transkript]** Slikao je sa strane jer je glavnu poziciju prepustio snimatelju.
- **[slika]** Na prvoj su glave priljubljene iza bidermajera, na drugoj oboje gledaju u aparat.

**M13** `_KAD9440` / `_KAD9443` — Talići 3 (mol), 13:42, razmak 3 s. **[stranica]** jedna; napomena „lice osvetljenije na prvoj, iste su“.
- Jako slične, skoro iste. Birao bi jednu: prvu, jer je lice osvetljenije.
- **[transkript]** Blic na jakom suncu nekad opali, nekad ne.
- **[slika]** Mladenci se drže za ruke. Razlikuje se pravac pogleda.

**M14** `_KAD9037` / `_KAD9038` — Talići 3, 11:02, ista sekunda. **[stranica]** obe; napomena „druga bolja samo da se posvetli“.
- Druga je bolja: bolji kadar, prav, ravan. Samo će je malo posvetliti. Ipak bi dao obe, jer je na
  obe dobro ispao.
- **[transkript]** Prva je sa blicem („mnogo mu je blic udario“), druga bez. U tamnijoj „ima
  podatak“ i može da se vrati.
- **[slika]** Portret mladoženje. Prva je šira i svetla, druga uža i u pregledu vrlo tamna.

**M15** `_KAD9410` / `_KAD9411` — Talići 3 (mol), 13:39, razmak 2 s, uspravna pa položena. **[stranica]** jedna; napomena „širu jer su iste“.
- Iste su, pa bi izabrao širu jer je lepši kadar.
- **[slika]** Mladenci na molu u istoj pozi. Položena (šira) pokazuje više mora i planine.

**M16** `_KAD9659` / `_KAD9662` — Talići 3 (crkva), 14:48, razmak 34 s. **[stranica]** različito.
- Obe, jer su različite.
- **[slika]** Na prvoj je mladoženja u pokretu levo, a mlada u kontra-svetlu na vratima. Na drugoj
  je mlada napred, mladoženja okrenut leđima, iza gosti.

**M17** `_KAD0600` / `_KAD0601` — Talići 4 (prvi ples), 20:49, razmak 1 s. **[stranica]** obe.
- Obe, različite su.
- **[transkript]** „Različit trenutak, prosto. […] Tu bih obe zadržao.“ Na stranici je ipak
  kliknuto „isti trenutak, ali idu obe“.
- **[slika]** Prvi ples u dimu. Na prvoj mlada gleda u aparat, na drugoj se smeje zabačene glave.

**M18** `_KAD0395` / `_KAD0396` — Talići 4, 19:17, razmak 6 s. **[stranica]** jedna.
- Jedna je dovoljna jer su iste. Manje je kritično kad je u pitanju enterijer (prostor, a ne ljudi).
- **[transkript]** Gosti za stolovima, slikano izdaleka: „ne treba ni da slikam dok jedu“.
- **[slika]** Širok kadar bašte sa stolovima. Druga je malo bliža.

**M19** `_KAD0197` / `_KAD0198` — Talići 4, 18:07, razmak 7 s. **[stranica]** obe.
- Obe, jer su lepe.
- **[transkript]** „Nešto su se smejali.“
- **[slika]** Gosti nazdravljaju. Na drugoj je kadar širi i u njemu je još jedna gošća. Naše
  grupisanje ih već razdvaja.

**M20** `_KAD0417` / `_KAD0418` — Talići 4 (govor), 19:25, razmak 3 s, položena pa uspravna. **[stranica]** jedna.
- Dovoljna je jedna jer su jako slične.
- **[transkript]** Bolja je uža, na kojoj se ne vide noge. Ženu koja govori zove mama.
- **[slika]** Žena govori u mikrofon, pored nje muškarac. Položena je uža (do kolena), uspravna je
  izdaleka sa celom figurom. Po haljini je to ista osoba kao na P18. Naše grupisanje ih već razdvaja.

## Pregled grupa (isečci)

Ista stranica, drugi deo: naše grupe prikazane redom, Peđa klikne samo tamo gde su pogrešne.
Sačuvana su četiri klika; ostalo je iz razgovora. Deo 3 nije otvoren.

**X1** Talići 4a, `_KAD9785` / `_KAD9786` (naša grupa od 2). Gosti u crkvi, jedan drži lepezu.
- Jeste ista grupa. Izabrao bi prvu kao bolju.
- **[transkript]** Na prvoj „ima neku foru“. To je atmosfera u crkvi, da se prikažu gosti.

**X2** 4a, `_KAD9787`, `9788`, `9789`, `9796` (naša grupa od 4). Mladenci stoje pred oltarom.
- Četiri jako slične slike, može jedna. Grupa je dobra.
- **[slika]** Četvrta je snimljena minut posle treće; naš algoritam ju je vratio u grupu.

**X3** 4a, `_KAD9794` / `_KAD9795` (naša grupa od 2, ista kao P4). Mladin brat i dečak koji zeva.
- Bolja je ona na kojoj mali ne zeva.
- **[transkript]** To je „slika brata“: gleda brata, ali dete odlučuje.

**X4** Označavanje bitnih ljudi (rodbine) na početku obrade.
- Loša ideja zbog gužve: ponedeljkom imaju i po 30 paketa od petka, subote i nedelje.
- **[transkript]** „Nemoguće“: roditelji, sestre i braća sa obe strane. Naš predlog da sistem sam
  prepozna mladence kao ključne figure nije osporen.

**X5** 4a, `_KAD9806`–`9811`, `9820`–`9823` (naša grupa od 10, ista kao P6). Mladenci hodaju kroz crkvu, snimljeni s leđa.
- Iz velike grupe bira nekoliko, jer ih ima baš mnogo.

**X6** 4a, `_KAD9815` | `_KAD9817` (naša grupa od 2). **[stranica]** makaze: različito.
- Nije ista grupa, jer nije potpuno isti momenat.
- Da jeste baš isti momenat, a samo je jedna položena i druga uspravna, mogla bi samo jedna.
- Za selekciju se ne gleda da li je slika položena ili uspravna, već da li je isti momenat ili ne.
- **[slika]** Razmak 2 s. Prva je uspravna, cela figura, kum iza. Druga je položena i uža, mladenci
  sa svećama i gosti iza.

**X7** 4a, `_KAD9846`, `9847` + `9848` (naše dve grupe: 2 i 1). **[stranica]** spojeno `9847` + `9848`.
- Sto u crkvi. Dovoljna je jedna široka, prva. Ostale ne: ne trebaju mu tri slike toga.
- **[slika]** Prva je položena i šira, druga uspravna, treća uspravna i bliža.

**X8** 4a, `_KAD9852`–`9856` (naša grupa od 5, ista kao P2). Poljubac mladenaca pod velom.
- Kada ima pet ovakvih slika, bira na primer dve: jednu gde se smeju i jednu gde se ljube.

**X9** Koliko slika ostaje, opšte.
- Kada ima jako mnogo slika, radi se selekcija. Kada nema mnogo slika nekog momenta, daju se sve
  dobre, bez loših.
- Postoje svadbe sa jako malo slika, pa hoćeš da izvučeš maksimum. Ovde je bilo jako mnogo slika.
- Ako imaš 12 slika, biraj 5.
- Momenti kao što su venčanje, prvi ples, prvi susret i izlazak iz crkve: minimalno odbacuješ.
- **[transkript]** „U ovom segmentu imaš 10 slika i zadržiš 3 najlepše ili 4. Ali nemaš ti to
  stalno.“ Obično imaju 10–15 minuta sa mladencima, pa se trude da zadrže što više. „Prosečni
  momenti“: tri-četiri najlepše, ili pet od dvanaest. Prvi ples: „odatle se vadi najviše“.

**X10** Talići 1, `_KAD8033`–`8049` (naša grupa od 11). Brod: on sedi, ona stoji iznad njega.
- Tamne slike iz ove grupe nisu za bacanje, jer se mogu izvući. Ovo bi i JPG mogao da izvuče; iz
  RAW-a može više, ali i iz JPG-a može malo. Ne izbacuj one koje se mogu vratiti.
- **[transkript]** Blic opali tri-četiri puta, dva puta ne opali. „Ja ih sredim i onda odaberem
  najlepše od toga.“ Bacaju se samo ekstremne („ako može da se vrate, okej“).
- **[slika]** Tri od jedanaest su tamne (`8041`, `8044`, `8046`), snimljene sekundu posle svetle.

**X11** Talići 1, `_KAD8019`, `8020` | `8029`, `8030` (naša grupa od 4). **[stranica]** makaze: različito. Primer sa slike `poostri-grupisanje.png`.
- Primer kako treba pooštriti grupisanje.
- **[slika]** Prve dve su uspravne, skoro poljubac. Druge dve su položene, snimljene dva minuta
  kasnije: mlada se naslanja, gledaju se i smeju. Naš algoritam ih je spojio vraćanjem unazad.

**X12** Talići 1, `_KAD8026`–`8028` | `8032` (naša grupa od 4). **[stranica]** makaze: različito.
- **[transkript]** „Ove tri su ti slične. […] Ova nije ista.“ U istom delu: na jednoj slici „malo
  oko otišlo, nekako žmiri, tu bih sklonio“.
- **[slika]** Četvrta je snimljena 75 s kasnije, u drugoj pozi (čaša, gledaju se).

**X13** Dva fotografa.
- Treba uzeti slike oba fotografa za taj dan, poređati ih po vremenu nastanka (date created) i
  birati bolju.

## Stranica 2: izbor najbolje slike (P1–P23)

`cull.py pick --output data\out-4a --sample data\meeting\picks_sample.json --picks-file
picks.agency.json`. Sve grupe su iz Talići 4a. „Izabrano“ je ono što je kliknuto na stranici.

**P1** `_KAD9843`, `9844` — izabrano 1 od 2 (`9843`), označeno „svejedno“. Mladenci sa svećama pred oltarom.
- Jako slične, uzmeš jednu. Razlika je zamućeni kum iza, ali on nije u fokusu, u fokusu su
  mladenci. Nije bitno koja.

**P2** `_KAD9852`–`9856` — izabrano 3 od 5 (`9852`, `9854`, `9856`); napomena „3 od 5“. Poljubac pod velom.
- Izabereš dve ili tri od pet. On bi konkretno za ovo izabrao tri: lepa je slika pre poljupca,
  poljubac i osmeh posle.
- **[slika]** Nisu kliknute `9853` (drugi kadar poljupca) i `9855` (drugi kadar osmeha).

**P3** `_KAD0033`, `0034` — izabrano 2 od 2; napomena „nema ih puno, brat je uvodi, bitan momenat“.
- Nema mnogo slika momenta kada je brat uvodi. Bitan je momenat, pa bi zato izabrao obe. Nisu
  skroz iste. Drugu bi malo sredio, jer je svetlost „pukla“.
- **[transkript]** Hodaju kroz hlad i sunce naizmenično, ekspozicija ne može da se podesi tom brzinom.

**P4** `_KAD9794`, `9795` — izabrano 1 od 2 (`9795`). Brat i dečak.
- Bira drugu, jer je dečak na prvoj otvorio usta.

**P5** `_KAD9904`, `9906`, `9907` — izabrano 1 od 3 (`9907`). Cveće na stolu.
- Dekoracija: ako su uglovi slični ili isti, uzmeš jednu; ako su različiti, dve ili tri. Druga i
  treća su jako slične, izabrao bi treću.
- **[slika]** Prva je iz drugog ugla (stolica, visoke vaze). Po pravilu koje je izrekao ostala bi i ona.

**P6** `_KAD9806`–`9811`, `9820`–`9823` — izabrano 4 od 10 (`9810`, `9821`, `9822`, `9823`); napomena „nije toliko bitno“. Šetnja kroz crkvu s leđa.
- Ima ih jako mnogo, izabereš par. Gledao je gde je korak u redu, ali to nije toliko bitno. Bitno
  je da imaju dve-tri slike.
- **[slika]** Izabrane su tri uzastopne skoro iste. Nije izabrana `9811`, na kojoj kroz kadar
  prolazi čovek, ni prve tri, koje su presvetle.

**P7** `_KAD0026`–`0029` — izabrano 4 od 4; napomena „sve jer ih je malo“. Devojčice sa korpicama prolaze između gostiju.
- Malo je slika ovog momenta, pa bi zadržao sve, jer su svuda ispale dobro.
- Na slikama se vide senke videografa. Bilo bi sjajno da sistem ume da ukloni senke.
- Predlog: sistem treba da shvati kada je slika nekog momenta malo i da ih, ako su sve dobre,
  zadrži; a kada ih je previše, na primer 12, da zadrži 5.
- **[transkript]** „Vrlo kritična situacija“, sačuvao bi sve i pokušao da ih sredi. Na predlog je
  odgovorio da on zna šta se desilo jer je slikao, ali da to ne može da zna na svim svadbama.

**P8** `_KAD9916`, `9917` — izabrano 1 od 2 (`9917`), „svejedno“. Širok kadar bašte sa stolovima.
- Identične slike, uzmi jednu, svejedno koju.

**P9** `_KAD9928`, `9929` — izabrano 2 od 2. Mlada sama pored stolova.
- Obe: kad si mlada, želiš sve slike, a na obe je dobro ispala.
- **[transkript]** „Malo gleda vamo, malo tamo.“ Priča o alatu koji je izbacio sliku za koju je
  mlada posle pitala.

**P10** `_KAD0011`, `0012` — izabrano 2 od 2; napomena „nema ih previše“. Ulazak mladoženje.
- Bilo bi jako dobro da mogu da se uklone senke. Nema previše slika ulaska mladoženje, a na obe je
  dobro ispao, pa bi sačuvao obe.
- **[slika]** Razmak 1 s, razlika je u koraku.

**P11** `_KAD9923`–`9925` — izabrano 3 od 3. Mladenci za stolom, tri kadra.
- Zadržao bi sve. Ne bi dao samo sliku na kojoj je nekome lice loše; na svima su dobro ispali.
- **[transkript]** Mladu bi malo posvetlio jer je senka pala na nju. „Te senke nisu loše.“

**P12** `_KAD9908`, `9909` — izabrano 1 od 2 (`9909`), „svejedno“. Detalj na tanjiru.
- Svejedno, jako slično.

**P13** `_KAD0063`–`0079` — izabrano 8 od 8. Venčanje u bašti.
- Momenat venčanja: daješ sve što je dobro.
- **[transkript]** „Malo slične, a različiti kadrovi. Ako su dobre, dajem sve.“

**P14** `_KAD9983`, `9985` — izabrano 2 od 2. Gost pod suncobranom.
- Obe, na obe je dobro. Bolja je druga, ali bi dao obe; nisu skroz iste.
- **[transkript]** Gost je Peđin rođak i bivši mladoženja agencije. Na jednoj mu se bolje vidi
  lice, druga je „simpatična“.

**P15** `_KAD0139`, `0140` — izabrano 2 od 2. Mladenci u bašti, žena im prilazi sa trakom.
- Ima malo slika, pa bi dao obe. Da ih ima mnogo, jednu.
- **[transkript]** „Tu imam dve ili tri. Ako imam dvadeset, ne bih im dao.“

**P16** `_KAD9953`, `9954` — izabrano 1 od 2 (`9953`); napomena „svj“. Hrana.
- Svejedno za hranu, jedna.

**P17** `_KAD0095`–`0097` — izabrano 3 od 3; napomena „sve“. Venčanje, mladenci se smeju.
- Sve: svuda su dobro ispali, bitan je trenutak. Idealno bi bilo da se na trećoj ukloni glava osobe
  koja je ušla u kadar.

**P18** `_KAD0174`, `0175` — izabrano 2 od 2, „svejedno“. Mama sa pićem.
- Ovo je mama, pa bi dao obe. Da je gost, jednu. Pošto sistem ne zna da je mama, i jedna je u redu,
  ne bi bilo strašno.

**P19** `_KAD9970`, `9971`, `9973` — izabrano 3 od 3. Gosti pod suncobranom (isti par kao M1).
- Sve bi dao, sve su dobre.
- **[transkript]** „Tu atmosferu možda im daš. Nije njima toliko bitan broj.“

Usput: „Naši su seljaci, vole što više slika.“

**P20** `_KAD0177`–`0180` — izabrano 2 od 4 (`0178`, `0180`); napomena „svj al 2“. Par gostiju pozira.
- Od četiri bi dao dve: jednu gde su celi i jednu užu. Nebitno je da li gost nosi naočare ili ne.
- Od celih bi dao drugu; četvrtu zato što je bolji kadar.

**P21** `_KAD0124`–`0132` — izabrano 9 od 9. Poljubac uz dim u boji, rafal od 4 s.
- Sve su za davanje, bitan je momenat. Nešto bi možda pretvorio u crno-belo (na primer poslednje),
  pa bi sve bilo u redu. Nigde nisu ispali loše.
- **[transkript]** „I obrišeš neku“, pa odmah: uzmi sve, jer je bitan momenat. „Bolje nego da me
  jure posle da je nešto nestalo.“
- **[slika]** Poza je ista na svih devet, menja se samo dim; poslednje su skoro bele od dima.
  Zapis o ovoj grupi u `picks.agency.json` nosi vreme 2026-11-23 (stranica je ponovo otvarana);
  izbor je isti kao 2026-11-19.

**P22** `_KAD0154`, `0156` — izabrano 1 od 2 (`0156`). Glavni sto.
- Ako postoje samo dve slike stola, daješ obe; ako ih ima 15, daš dve-tri.
- Ove slike su generalno loše jer iza ima ljudi. Dao bi drugu, jer je prva pretamna.
- **[transkript]** Na pitanje koja je bolja: „nijedna“, jer su iza ljudi.

**P23** `_KAD0155`, `0164` — izabrano 1 od 2 (`0164`), „svejedno“. Kutija za koverte.
- Jedna slika kutije za pare je dovoljna, svejedno koja.

## Opšte izjave

### Šta sistem treba da radi (rečeno posle M13)

- Bitno je da se odbaci ono što nije dobro.
- U redu je da mladencima ode sve što je dobro, pa da oni sami prave selekciju po svom ukusu.
  Sistem izbacuje ono što je stvarno loše.
- Izbacuju se: zatvorene oči (koje nisu „dreamy“ momenat), mutne slike koje su loše a ne umetničke,
  jako tamne slike kojima nema popravke. Aftershoot to ne zna da razlikuje.
- U redu je i da im odu jako slične dobre slike, pa neka oni biraju.
- Značilo bi im da se slika ispravi, da se podesi ekspozicija, da se podignu senke.

### Čemu alat služi (rečeno posle M7)

- Alat je za culling posle svadbe, za slike koje idu digitalno mladencima.
- Nije za štampu na licu mesta. Za to nema vremena; tada se ne filtrira, ide sve: slike gostiju
  koje idu u prodaju, slike gostiju sa mladencima, stolovi.
- Ova svadba je specifična: potpuno digitalna, bez štampe. Slike sa gostima su spontane (gosti
  stoje za koktel stolom); nije bilo tradicionalnog slikanja sa mladencima na ulazu.
- Glavni fotograf slika mladence i ima pomoćnika. Sporedni fotografi slikaju goste.
- Alat je za glavnog fotografa i pomoćnike koji slikaju mladence.

### Ulaz i obrada posle cullinga (rečeno posle M14)

- Ulaz je i RAW (Peđa, Đole, Danilo) i JPG (ostali).
- Obrada dolazi posle cullinga. Na kraju se pravi najosnovniji filter: malo smanjen kontrast,
  nešto kao onaj koji on koristi. Ime filtera nije sigurno (u belešci „bebe vaus ??“), varijanta
  3 ili 4: jedna vuče na ružičasto, druga na žućkasto. Može da promeni boju odela.
- Ta dva filtera ne idu kada je sunce jako i kontrast prevelik. Tada treba filter koji spušta
  svetle delove, podiže senke i dovodi sliku „u ravan“.
- Značilo bi da se preeksponirane slike vrate. Svetli delovi idu do 255: ono što je do 250 može da
  se vrati, poslednjih pet ne može. Isto za senke: prvih pet je potpuno crnilo koje se ne vraća,
  ostalo može. Blic nekad „pukne“ već na 230. Tipičan problem: bela haljina i crna kosa u istom kadru.
- Kod RAW-a se može izvući, a kad ode u JPG dobiješ DNG (digital negative file).
- Misli da je Lightroom uveo denoise i na JPG; do sada je radio samo na RAW fajlovima. ISO 1600
  ili 1200 u crkvi, pa je odlično za crkvu i prvi ples. Crkva je najčešće najmračnija; on ide na
  denoise 50 %.
- Ako stavi filter na jednu sliku, stavi ga na sve. Ideja: staviti filter na jednu, pa mi
  primenimo na sve. To Lightroom već radi (sync); daje tabelu u kojoj biraš šta se prenosi, na
  primer samo denoise. Uklanja i nesavršenosti kože (blemishes).
- Lightroom mu je odličan i ima culling koji je probao i koji je u redu. Njemu taj culling ne znači
  mnogo, jer svaku sliku i dalje gleda sam.
- Problem ostalih su loši računari, u koje se ne ulaže, pa ne mogu da koriste Lightroom: upload
  slika traje dugo (20 minuta). Kažu da će kupiti Mac i da će svi preći na to.
- Kada je slika malo mutna, koristi Topaz AI (sharpening, denoise, recover face). Radi kada je malo
  mutno, ne kada je mnogo.
- Velika želja: uklanjanje senki drugih ljudi (videografa) sa mladenaca.

## Gde automatski transkript kaže drugačije

Važi beleška. Spisak postoji da neka kasnija sesija ne bi belešku „ispravila“ po automatskom
transkriptu.

| Mesto | Beleška (važi) | Automatski transkript |
|---|---|---|
| DNG | kad ode u JPG dobiješ DNG | iz JPG-a se ne dobija ništa; DNG se može kasnije sređivati |
| Ime filtera | „bebe vaus ??“ | „BW Aus“ |
| Spori računari | upload slika traje 20 minuta | izbacivanje slika iz Lightroom-a traje 20 minuta |
| P22, prva slika | pretamna | „malo taman, ali može se posvetliti“ |
| M10, četvrta osoba na grupnoj slici | zadržava obe | pitanje je postavila Lana, odgovor „dobro“ |
| M5, širok i uzak kadar | zadrži obe | pravilo je kao pitanje izgovorila Lana; Peđa: „obe bih im dao“ |
| P7, predlog o malom broju slika | predlog sa sastanka | predlog je izrekla naša strana; Peđa: ne može se znati šta se desilo na svakoj svadbi |

Razrešeno 2026-11-23:

- P2: u belešci je pisalo „izabrao bi 5“. Lana je potvrdila da je tri (toliko je i kliknuto na
  stranici).
- Denoise: u belešci je pisalo „uveo i na JPG; do sad je bio samo na JPG“, što ne može oba da
  važi. Drugi deo je uzet iz automatskog transkripta: do sada samo na RAW fajlovima.

Pravilo (Lana, 2026-11-23): ono čega nema ni u belešci ni u automatskom transkriptu nije rečeno i
ne zapisuje se kao Peđina izjava. Gde beleška protivreči sama sebi, gleda se automatski transkript.

M17 nije razlika u transkriptu: i beleška i transkript kažu „različite“, a na stranici je kliknuto
„isti trenutak, ali idu obe“. Važi izgovoreno ([Q7](../requirements.md#open-questions)).
