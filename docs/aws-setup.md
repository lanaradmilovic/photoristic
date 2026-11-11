# AWS: podizanje Qwen-a na EC2 (vodič za korisnika)

Vodič korak po korak za podizanje vLLM servera iz [plana](plan.md#fixed-constraints) i
[0018](decisions/0018-swappable-vlm-client-own-server.md). Pisan na srpskom, za korisnika koji ne
poznaje AWS: kada nastavljaš ovaj posao, izlistaj korisniku korake od mesta gde je stao, jednostavno,
jasno i kratko. Ažuriraj "Dokle se stiglo" na kraju svake sesije u kojoj se radilo na AWS-u.

## Dokle se stiglo (2026-11-11)

- Urađeno: koraci 1–4 (budžet, region Frankfurt `eu-central-1`, dozvola za GPU **odobrena: 8 vCPU**
  za "Running On-Demand G and VT instances", ključ `photoristic.pem`). Pri prvom pokušaju
  pokretanja automatski je napravljena security group `launch-wizard-1` (SSH samo sa "My IP").
- **Zapelo na koraku 5:** "Insufficient capacity" u Frankfurtu za `g6.xlarge`, `g6.2xlarge` i
  `g5.xlarge`, u sve tri zone (1a, 1b, 1c). Nijedna mašina nije pokrenuta, ništa se ne naplaćuje.
- **Isti dan, kasnije: `g4dn.xlarge` (T4, 16 GB) se pokrenula.** Plan: 4-bitni
  `Intel/Qwen3.5-9B-int4-AutoRound` sa `--dtype float16` (T4 nema bfloat16); rezerva
  `Qwen/Qwen3.5-4B`. `config.yaml` već pokazuje na taj model i port 8001.
- **Radi (2026-11-11 20:22):** `ping-vlm` kroz tunel uspešan. Na mašini (IP se menja pri svakom
  Start) postoji `~/start-vllm.sh`; pokreće se sa `tmux new -d -s vlm ~/start-vllm.sh`, log u
  `~/vllm.log`, start traje ~8 min. Bez `--enforce-eager` i `--max-num-seqs 4` pada sa OOM
  (CUDA graphs za 256 zahteva ne staju u 15 GB). Model zauzima 8 GB, KV cache 2.7 GB ≈ 63k tokena.
  Claude može sam da se poveže (`ssh -i ~/.ssh/photoristic.pem ubuntu@<IP>`) i pokrene sve; od
  korisnika treba samo Start mašine i IP.
- Urađeno 2026-11-11: prva prava `judge` proba na 4a (~5,5 s po paru; rezultat u
  [research](research/2026-11-11-judge-first-real-run.md)). Sledeće: faza 3 (ocenjivanje grupa).
- Za kasnije (g6 za pun model): pokušati Frankfurt ponovo u drugo doba dana i/ili tražiti istu dozvolu (8) u Irskoj
  `eu-west-1`, Stokholmu `eu-north-1`, Londonu `eu-west-2` (vidi [Ako nema mesta](#ako-nema-mesta)).
  Nije potvrđeno da su ti zahtevi poslati.
- Otvoreno pitanje za kasnije (za klijenta): vidi [Pouzdanost za klijenta](#pouzdanost-za-klijenta).

## Deo A: jednokratna priprema

1. **Budžet:** pretraga **Budgets** → **Create budget** → **Use a template** → **Monthly cost
   budget** → iznos (npr. 50 USD) i email → **Create budget**.
2. **Region:** gore desno izaberi **Europe (Frankfurt) eu-central-1**. Sve dalje u tom regionu.
3. **Dozvola za GPU:** **Service Quotas** → **AWS services** → **Amazon EC2** → pretraga
   `Running On-Demand G and VT instances` → **Request increase at account level** → **8**.
   Važi samo za jedan region.
4. **Ključ:** **EC2** → **Key Pairs** → **Create key pair** → ime `photoristic`, **RSA**, **.pem**.
   Fajl u `C:\Users\Lana Radmilovic\.ssh\`, pa u PowerShell-u:
   ```
   icacls "$HOME\.ssh\photoristic.pem" /inheritance:r
   icacls "$HOME\.ssh\photoristic.pem" /grant:r "$($env:USERNAME):R"
   ```
   Ključ važi samo za jedan region.
5. **Pokreni mašinu:** **EC2** → **Launch instance**:
   - **Name:** `photoristic-vlm`
   - **Image:** pretraga `Deep Learning OSS Nvidia Driver AMI GPU PyTorch`, najnoviji za **Ubuntu**
     (drajveri za grafičku već unutra)
   - **Instance type:** `g6.xlarge` (rezerva: `g6.2xlarge`, `g5.xlarge`, `g6e.xlarge`, sve u dozvoli od 8)
   - **Key pair:** `photoristic`
   - **Network settings** → **Edit** → **Subnet:** zona koju AWS u poruci greške navodi kao
     slobodnu; **Firewall:** **Select existing security group** → `launch-wizard-1`. Ništa drugo
     ne otvaraj (port 8000 ostaje zatvoren, ide se kroz tunel).
   - **Storage:** **100** GiB, **gp3**
   - **Launch instance**
6. **Poveži se:** **Instances** → mašina → kopiraj **Public IPv4 address**, pa:
   ```
   ssh -i "$HOME\.ssh\photoristic.pem" ubuntu@1.2.3.4
   ```
   Na "Are you sure…" ukucaj `yes`.
7. **Instaliraj vLLM** (samo prvi put), na mašini:
   ```
   python3 -m venv ~/vllm-env
   source ~/vllm-env/bin/activate
   pip install -U vllm
   ```

## Deo B: svaki put kad radiš

8. **Upali mašinu:** **Instances** → označi → **Instance state** → **Start**. IP je posle svakog
   paljenja nova. "Start" može da javi "Insufficient capacity" (vidi dole).
9. **Pokreni model** (poveži se kao u 6):
   ```
   tmux new -s vlm
   source ~/vllm-env/bin/activate
   vllm serve Qwen/Qwen3.5-9B --max-model-len 16384 --reasoning-parser qwen3 --limit-mm-per-prompt '{"image": 16, "video": 0}' --gpu-memory-utilization 0.92
   ```
   Prvi put skida ~20 GB. Spreman kad piše `Application startup complete`. `Ctrl+B` pa `D` za
   izlaz (model radi dalje). Komanda još nije isprobana na pravoj mašini.
10. **Tunel** sa svog računara, u posebnom prozoru koji ostaje otvoren:
    ```
    ssh -i "$HOME\.ssh\photoristic.pem" -N -L 8001:localhost:8000 ubuntu@1.2.3.4
    ```
    Port 8001 jer 8000 na računaru drži DashClientService ([vlm-judge](spec/vlm-judge.md#running)).
11. **Provera:** u `config.yaml` pod `vlm:` stavi `base_url: http://localhost:8001/v1` (jednom), pa
    ```
    .venv\Scripts\python cull.py ping-vlm
    ```
    Treba da ispiše `... serves Qwen/Qwen3.5-9B`.
12. **Na kraju: Stop** (ne Terminate, to briše sve). Upaljena `g6.xlarge` ≈ 1 USD/h, ugašena samo
    disk (nekoliko USD mesečno).

## Ako nema mesta

"Insufficient capacity" znači da AWS u tom trenutku nema slobodnu mašinu tog tipa u toj zoni.
Redom:
- Druga zona (poruka greške kaže koje su slobodne), drugi tip iz koraka 5.
- Drugo doba dana (rano ujutru, kasno uveče, vikend).
- Drugi EU region: ponovi korake 3 i 4 tamo (dozvola i ključ važe po regionu), onda 5 nadalje.
- `g4dn` (T4, 16 GB) ne pomaže: model traži ~19 GB. Spot mašine ne: posebna dozvola, AWS ih gasi.
- GPU van AWS-a (RunPod, Lambda…) menja odluku [0018](decisions/0018-swappable-vlm-client-own-server.md)
  (slike gostiju kod druge firme) — samo uz odluku korisnika, i novi zapis u `decisions/`.

## Pouzdanost za klijenta

Mašina koja radi ne pada zbog gužve, ali svaki Stop → Start ponovo traži mesto i može da ne uspe.
Nije odlučeno; opcije:
1. Mašina radi stalno: sigurno, ~700+ USD/mesec za `g6.xlarge` u Frankfurtu.
2. On-Demand Capacity Reservation: garantovan Start, plaća se kao da radi stalno; uz godišnji
   Savings Plan / Reserved Instance ~30–40% jeftinije.
3. Paliti samo po potrebi, dan ranije, uz rezervni region. Jeftino, bez garancije. Aplikacija
   ionako nastavlja gde je stala (`judge_verdicts.json` posle svakog para).

Cene su okvirne; tačna cena po satu piše u **Launch instance** pri izboru tipa.
