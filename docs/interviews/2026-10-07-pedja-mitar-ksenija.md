# Intervju 2 — Peđa, Mitar, Ksenija (2026-10-07)

Drugi sastanak u agenciji. Prisutni:

- **Peđa**, fotograf. Radi i svoje svadbe (5–10 godišnje) koje sam obrađuje u Photoshopu. U
  agenciji je samo četvrtkom.
- **Mitar**, vlasnik (vidi [prvi intervju](2026-09-21-mitar.md)).
- **Ksenija**, radi culling u agenciji.

Sažetak je napravljen iz automatskog transkripta. Govornici nisu bili označeni imenima, pa su
prepoznati iz konteksta. Citati su lako očišćeni od poštapalica.

## Postojeći alati: Aftershoot i Imagen

- Peđa: dva najpopularnija su **Imagen AI** i **AfterShot** (Aftershoot). Probao je oba.
- Imagen bolje sređuje slike i ima bolji izbor filtera. Ipak, „nije ni blizu“ onoga što on
  radi ručno.
- Alati izravnaju slike, prepoznaju slične slike, duplikate i zatvorene oči. Ali **„nekad nama i
  trebaju te zatvorene oči“**.
- **Glavna zamerka:** posle alata i dalje mora da se prođe kroz sve slike.
  „Ako ima pet hiljada slika […] ja sad opet moram da prođem sve te slike jel' mi je on to dobro
  uradio.“ Podela u dve gomile mu oduzima još više vremena: prvo pregleda dobre, pa loše, pa se
  vraća napred-nazad.
- Probni period: Aftershoot mesec dana besplatno, Imagen 1.000 slika besplatno.

Ovo je ista nit kao u [žalbama korisnika na culling alate](../research/2026-11-10-culling-complaints.md#21-ipak-moram-sve-da-pregledam-tema-br-1).

## Cilj: nije nula pregleda, nego 15–20 minuta

- Pitanje je bilo da li je cilj da čovek uopšte ne gleda. Mitar: **„Moraće da pogleda“**, ali
  „da ne provodi dva sata, nego da završi taj paket za petnaest, dvadeset minuta“.
- Ksenija: „Meni ne smeta toliko da to bude editovano koliko mi olakšava ako mi je on skinuo sve
  što ne valja i ja samo trebam da preletim to što je ostavio da valja.“
- Peđa: kada jednom bude i obrade, najbrže bi bilo da Ksenija pregleda gotovu galeriju i javi šta
  ne valja. U programu bi trebalo da postoji povratna informacija („ovo ne valja zbog ovoga“) iz
  koje alat uči.

## Šta je gore: baciti dobru ili zadržati lošu

- Pitanje Kseniji: šta je veći problem, odbaciti sliku koja nije trebalo ili zadržati sliku koja
  je trebalo da se odbaci?
- Ksenija: ako ostane neka loša, „nije baš“ greška, **„ali ako obrišemo nešto…“** (kvalitetno),
  to je problem.
- Odatle je tvrdo pravilo projekta „nikad ne izgubi dobru sliku“ ([plan](../plan.md#goal-and-the-hard-rule)).

## Kako Ksenija danas radi culling

- „Imam šest hiljada slika. Idem sliku po sliku i brišem. Da li žmuri, da li je mutna, da li se
  isplazila, da li je slična, da li je tamna.“
- **6.000 slika: oko 2 sata u savršenim uslovima** (bez telefona i prekida). U stvarnosti traje
  do sutradan. Ako slike nisu dobre, traje i duže.

## Prioriteti (redosled koraka)

Peđa nabraja šta im treba za pakete, a Ksenija potvrđuje („mislim da je to to“):

1. **odabir slika** (culling): odabrati dobre, odbaciti loše. „Najbitnije“;
2. **krop** kada je kadar preširok i **ravnanje**;
3. **balans svetla**: svetle slike malo zatamniti, tamne malo posvetliti;
4. **izoštravanje** kada pobegne fokus. Ksenija: „ali najviše izoštravanje“;
5. **denoise** za crkvu („kao u Lightroomu“);
6. **filter na kraju**, najneutralniji, „true color“. „Nek ostane filter za kraj […] on nije ni
   toliko bitan.“

Pitanje Peđe: neki fotografi sve snimaju na f/1.4. Može li se popraviti i rezolucija/oštrina?

Dogovor: **prvi korak je samo culling**, drugi je krop i ravnanje.

## Format: računati na JPG

- Peđa snima RAW, ali restoranski fotografi snimaju **JPEG**. Slike se prodaju i štampaju na samoj
  svadbi, pa moraju odmah biti JPEG. „Nemoj da računaš na to“ (na RAW).
- Mitar: „To ćemo rešiti.“ Ksenija: „Za prodaju mora JPEG.“
- Peđa o razlici: RAW je 12/14-bitni, „siv“, i iz njega se vadi sve. JPEG je sRGB kompresija u
  kojoj nestaju tonovi kože (bež, roze, narandžasta). Kamera može da snima RAW+JPEG istovremeno.
- Peđa: za culling RAW „njima nije bitan“.
- Zaključak sa sastanka: **podrazumevati da je ulaz samo JPG**.

## Podaci za razvoj

- Predlog za culling: **10 svadbi pre i posle cullinga** (šta je ostalo, šta je bačeno). Ksenija to
  može da da. Zatim 11. svadba samo „pre“, alat predloži izbor, a agencija oceni šta valja.
- Peđa misli da je idealno 10 svadbi sa svim fotografima, originalima i obrađenim verzijama, ali
  sumnja da iko može da ih uradi: „Ne vidim ni kako bi to neko uradio, ni ko to može da uradi.“
  - Fotografi su ranije poslali po oko 100 RAW slika sa sopstvenom obradom. Mnogi su
    „kompjuterski nepismeni“, pa slike posle njihove obrade izgledaju lošije nego pre.
  - Peđi treba oko 7 dana za 1.500–2.000 slika, a oko dve nedelje za 5–6 hiljada. „Posle dva sata
    počnu boje da se mešaju.“
- Mitar: obrađene svadbe će biti spremne **u novembru**.
- **Peđa je na sastanku dao svoju svadbu iz Crne Gore ([Talići](../datasets.md))** na hard disku:
  - RAW (NEF) podeljeno po karticama 1–5;
  - folder „Talići sređeno“ sa obrađenim JPEG-ovima, podeljen po danima (dva dana);
  - oko 80 GB ukupno (≈20 + 60 GB). Kopiranje je trajalo oko 18 minuta po delu.
- **Važno:** ovo je Peđina „umetnička“ svadba. Snimljena je u RAW-u i obrađena slika po slika,
  uključujući generativno popunjavanje u Photoshopu (dodavanje ćoškova kod arhitekture, uklanjanje
  senki). Peđa sam kaže da je to „vrlo specifičan slučaj“. Restoranske svadbe agencije su JPEG,
  sa više fotografa i bez takve obrade.

## Obim i rokovi

- U sezoni (otprilike maj–septembar) je **oko 20 svadbi po vikendu** (20–27), plus rođendani i
  drugi događaji. Zimi manje. Godišnje je to oko **300 svadbi**.
- **5–6 hiljada slika po svadbi** (Peđa i Ksenija). Prvi intervju je pominjao 2–3 hiljade.
- Fajlovi su veliki: 20–27 foldera po svadbi, podeljeno po fotografima i po sekcijama.
- Culling od **5 minuta po svadbi je „sasvim okej“**, a i 20 minuta je okej.
- Isporuka: slike stižu u subotu i nedelju, gotovo u ponedeljak ili utorak je u redu.
- Za galeriju Peđa predlaže **rok od 7 dana** (može i 5), da devojke stignu da pregledaju i vrate
  greške. „Uvek će nešto biti.“
- Upload: 80 GB je oko 10 sati na njihovom internetu. Razgovaralo se o lokalnoj grafičkoj kartici
  i cloudu koji se plaća po satu.

## Krajnji proizvod koji Mitar opisuje

- Slike se prebace, a sistem ih poređa u galeriju za mladence. **Prvo lepe slike mladenaca**, uz
  laganu retušu kroz filtere.
- Izdvajanje mladenaca prepoznavanjem lica već postoji iz ranijeg proizvoda intervjuera.
- Galerija treba da bude malo dizajnirana i personalizovana, ne samo spisak imena. Mitar je
  poslao primer.
- Mora postojati način da se galerija lako izmeni pre slanja.

## Ostalo

- Peđa koristi generativno popunjavanje u Photoshopu i pominje Seedream i alate za uklanjanje
  senki.
- Rad u nedeljnim sprintovima, sa sastancima sa Peđom četvrtkom.
