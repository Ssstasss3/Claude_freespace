# Brief: «Клуб» — a 3D game about Orange Premium Club (manager ⇄ client)

## 0. Who you are and why this brief exists

You are building a single-file browser game in the repo `Claude_freespace` (`games/opc_klub.html`). You are both the game designer and the graphics engineer. The user judges **depth of thinking** first and polish second.

Two earlier pieces set the bar and the trap:
- An animated film about OPC: good visuals, factual.
- An arcade game called «Сфера»: catch roubles, dodge commissions, keep your average balance up. The user's verdict was *"polished but too safe, simplistic, repetitive."*

The lesson: **more particles won't fix it; decisions will.** This game must produce situations where a smart player thinks and a careless one pays, and where the right move comes from the real rules of the product.

The in-game language is **Russian**. This brief is in English.

---

## 1. The game in one paragraph

«Клуб» is set in a PSB premium office at night: marble, copper, graphite, warm light, floating spheres. You choose a role.

- **Manager (main mode, ~80% of the effort):** a shift at your desk. Clients of Orange Premium Club and OPC+ come in one after another, each with a real situation. You read their file, look things up in the tariff handbook and put together advice. A **rules engine** then plays out the client's month and shows what your advice actually leads to: free service kept, a commission avoided, or 3 990 ₽ lost. Clients come back with results, and trust accumulates or collapses. Think *Papers, Please* meets premium banking.
- **Client (compact mode, ~20%):** you live one to three months as a club member in a small 3D city diorama. You decide where your money sits, how you pay, and where you withdraw and transfer. The **same engine** tallies the month. The twist: in this mode, **you** get advice from a manager NPC, and it isn't always right. Your job is to tell the good advice from the bad.

The architecture follows from this: **one pure rules engine, two views of it.**

---

## 2. Source of truth: OPC facts

These come from the official tariffs «Orange Premium Club» and «Orange Premium Club +», **effective 01.07.2026**, plus official psbank.ru screenshots. Do not browse for more: psbank.ru is not reachable from the sandbox, and aggregator sites contradict each other. **Use only the ✅ facts in anything the game scores.** ⚠️ facts may appear only as neutral flavour, never as the basis for a right or wrong answer.

### 2.1 Free-service conditions (each is "one of")

| | Orange Premium Club | Orange Premium Club + |
|---|---|---|
| Average monthly balance, Moscow & Moscow region | ✅ ≥ 3 000 000 ₽ | ✅ ≥ 10 000 000 ₽ |
| Average monthly balance, other regions | ✅ ≥ 1 500 000 ₽ | ✅ ≥ 7 000 000 ₽ |
| Balance + card purchases in the calendar month | ✅ ≥ 1 000 000 ₽ **and** ≥ 50 000 ₽ | ✅ ≥ 5 000 000 ₽ **and** ≥ 150 000 ₽ |
| Salary | ✅ average salary credits ≥ 300 000 ₽ (Moscow & MO) / ≥ 200 000 ₽ (regions) | ✅ **no salary condition in OPC+** |
| Otherwise | ✅ 3 990 ₽/month | ✅ 10 000 ₽/month |

- ✅ **Grace period:** the calendar month in which the agreement is signed is free. If the client ends the agreement during the grace period or the following calendar month, a one-off fee equal to one month's fee is charged.
- ✅ The fee is charged only for a **full** calendar month of use (the grace month is the exception).
- ✅ **Region** is set by the office where the client obtains the package. With courier delivery, it's the region where the card contract is serviced. (A common trap: applying the Moscow threshold to a client from Yekaterinburg.)
- ✅ Switching from the «PSB-Приоритет» package at the client's initiative: no fee until the end of the period already paid for.
- ✅ Only one package per client. If a package is already active, a new one isn't issued.

### 2.2 How the average monthly balance works (the key mechanic)

- ✅ The **sum of the daily positive balances** of the client's own funds at the end of each bank operating day (Moscow time), **divided by the number of calendar days in the month.** So it is **time-weighted**: 5 млн deposited on the 29th of a 30-day month adds only ≈ 0.33 млн to the month's average.
- ✅ **Counts towards it:** card, current, deposit and on-demand accounts; brokerage accounts and IIS (securities portfolio value plus cash); units in mutual funds (ПИФ) of partner management companies; trust management (ДУ); unallocated metal accounts (ОМС); digital financial assets on the «Токеон» platform issued by the bank; the НПФ ПСБ long-term savings programme; premiums on life, endowment and pension insurance taken out at bank offices and paid from a bank account (counted from the payment date until the insurer pays out).
- ✅ Foreign-currency accounts are converted at the Central Bank rate on the last day of the month.
- ✅ The calculation happens in the calendar month after the reporting month.

### 2.3 What counts as a purchase (for the "balance + purchases" condition)

- ✅ **Counts:** authorised card payments for goods and services, in shops and online, on all package cards and on a card under the «Только вперёд» tariff. Also payments for telecoms (mobile, internet, TV) and utilities made through the PSB-Retail internet bank to partner organisations or with payment templates.
- ✅ **Does not count:** cash withdrawals, transfers (including card-to-card), **QR-code payments**, and e-wallet top-ups.
- ✅ Only transactions debited from the account **by the 14th of the following month** count.

### 2.4 Cash (OPC / OPC+)

- ✅ PSB and partner-bank ATMs: free.
- ✅ **PSB cash desk (OPC):** 0% for 100 000–300 000 ₽ a day, but **1% (minimum 200 ₽) for under 100 000 ₽** or over 300 000 ₽ a day. *This is counter-intuitive: 50 000 ₽ at the desk costs 500 ₽, while the same sum at the ATM next to it is free.* OPC+: 0% up to 1 500 000 ₽ a day.
- ✅ Other banks' ATMs: OPC 0% up to 300 000 ₽ a day, then 1% (minimum 200 ₽). OPC+ 0% up to 1 500 000 ₽ a day.
- ✅ Limits: OPC 1 000 000 ₽ a day per card and 5 000 000 ₽ a month per account. OPC+ debit card: 1 500 000 a day and 20 000 000 a month. Withdrawing above the limit costs 2% of the excess (OPC) or 1% (OPC+).
- ✅ Since 10.03.2022 there are no foreign-currency cash withdrawals in Russia, except at specific PSB ATMs.

### 2.5 Transfers

- ✅ **SBP (Faster Payments System) to other people:** free up to 100 000 ₽ a month in total. Above that, 0.5% (maximum 1 500 ₽). **Gotcha:** if a transfer takes you past the limit, the fee applies to **the whole transfer**, not just the excess, and the remaining free limit stays as it was. Limit per transfer: 300 000 ₽ for residents.
- ✅ SBP to your own accounts at other banks: free up to 50 000 000 ₽ a month (up to 30 000 000 ₽ per transfer). Above that, 0.5% (maximum 1 500 ₽).
- ✅ **Transfer by account details to another bank through the internet bank:** OPC free up to 500 000 ₽ a month, then 0.6% (minimum 20, maximum 1 500 ₽). OPC+ free up to 1 500 000 ₽ a day and 20 000 000 ₽ a month, then 0.5%. *So the right answer to "send my son 150 000 ₽" is by account details, not SBP.*
- ✅ Transfers within PSB through the internet bank: free.
- ✅ Card-to-card to another bank's card through the internet: 1.99% (minimum 199 ₽).
- ✅ Taxes and payments to the state budget: free.
- ✅ Card spending abroad in a currency other than USD, EUR or the account currency: 1.99% conversion fee.

### 2.6 Cards and services

- ✅ OPC cards: World Mastercard Black Edition, Мир Продвинутая, Visa Signature, Mir Supreme, Mir Supreme sticker. OPC+ cards: World Elite Mastercard, Visa Infinite, Мир Продвинутая, Mir Supreme. No USD or EUR cards have been issued since 24.02.2022. Cards are valid for 7 years and issued within 5 working days. Issue, reissue and annual service of the main card are free.
- ✅ **Additional cards: 3 free in total** (across all such cards in the client's name). The 4th and 5th cost 6 000 ₽ a year (OPC) or 6 250 ₽ (OPC+).
- ✅ Interest on the card account: 0%. (A client keeping 3 млн on the card earns nothing. The manager can suggest a deposit or investments, which still count towards the average balance.)
- ✅ Free: priority service in offices, personal manager consultations, a dedicated phone line, investment advice.
- ✅ Safe deposit box rental: 30% off (OPC) or 35% off (OPC+).
- ✅ «Защита путешественника» insurance (accident and illness during trips in Russia and abroad, civil liability, critical illness). OPC+ has a raised limit of up to €300 000 (from the site).
- ✅ OPC+ (from the site): 100% cashback on taxis, car sharing and Golden Key services; unlimited business-lounge access.
- ⚠️ **Unconfirmed (flavour only):** up to 10 lounge visits a year for base OPC; the concierge provider being Aspire; restaurants through ON·FOOD; a 20 000 ₽/year cap on taxi cashback; base OPC cashback percentages.

---

## 3. The rules engine: build this first and test it

This is the heart of the game. It must be **pure, deterministic and data-driven**: the tariffs live in one `TARIFF` object, and the functions don't touch the DOM or three.js. Minimum API (names are yours to choose):

```
avgBalance(ledger, month)          // ledger: daily snapshots by asset type → time-weighted average of what counts
countsTowardBalance(assetType)     // 'card','deposit','brokerage','iis','pif','du','oms','tokeon','npf','life_ins', and non-counting ones: 'other_bank','cash_home','crypto'
purchaseCounts(op)                 // card_pos, card_online, qr, card2card, sbp, cash, ewallet, utility_psbretail, … + the debit-by-the-14th rule
monthVerdict(client, month)        // → { free: bool, reason: clauseId, fee, nearestFix }
cashFee(tier, channel, amount, alreadyToday)
sbpFee(tier, amount, usedThisMonth, toSelf)
transferFee(tier, channel, amount, usedThisMonth/Day)
addCardFee(tier, nthCard)
simulateMonth(client, adviceActions) // applies the advice to the client's plan and returns the month's outcome + client cost
```

- Every rule has a **clause id** and a short Russian paraphrase («п. 1.1.2 — покупки картой: QR-оплата не учитывается»). The in-game handbook and the post-case debrief both cite them.
- Add a **self-test**: `?test` in the URL runs ≥ 40 assertions and prints the result. Cover every "gotcha" in section 2, including the SBP whole-amount rule, the cash desk under 100k, the time-weighted average, the regional threshold, the absence of a salary condition in OPC+, the grace period, and the 4th additional card.
- The engine also **generates the right answers**: for each case it computes the cheapest valid fix, so no answer is hard-coded.

---

## 4. Manager mode (main)

### 4.1 The loop
A shift is 8–10 clients, about 10–12 minutes. In each case:
1. **Arrival (3D):** the client walks from the waiting lounge to your desk. Their tier is visible from how they carry themselves and their accent colour (copper for OPC, gold for OPC+). Each client has a **patience meter**; OPC+ clients are less patient.
2. **File:** tier, region (issuing office), today's date, how many days are in the month, balance so far this month by asset type, purchases broken down by type (QR vs card), salary, what they hold at other banks, and the request in their own words, in Russian, as a natural line of dialogue.
3. **Handbook:** a searchable binder of the section 2 clauses, grouped into Conditions, Balance, Purchases, Cash, Transfers and Cards. Players who read it win. Opening a clause costs a little client patience, which is the time-versus-accuracy tension.
4. **Advice:** assembled from **action cards** with parameters, not multiple choice. For example: «Перевести брокерский счёт в ПСБ», «Открыть вклад на N ₽», «Платить картой вместо QR», «Оплачивать ЖКХ через PSB-Retail», «Перевести по реквизитам вместо СБП», «Снять в банкомате ПСБ, не в кассе», «Разбить перевод», «Остаться на OPC вместо OPC+», «Ничего не менять — всё и так бесплатно», «Нельзя: объяснить почему». There may be several valid solutions; the engine ranks them by cost to the client and by effort.
5. **Consequence:** `simulateMonth` plays out the month from your advice. The client leaves happy, or **comes back later in the shift or the next one** with a statement («Мне списали 3 990 ₽. Вы сказали, что QR считается…»). The debrief cites the clause.

### 4.2 Scoring
Build **client trust** (NPS-style), **money saved** for clients and **accuracy**. The bank's "plan" is a sales KPI, for example selling N investment products per shift. Selling a product helps the average balance only if it suits the client. A life policy sold to someone who needs the money for a flat next month hits KPI but costs trust later. Keep this a **generic game mechanic about the player's own temptation**, and never suggest that PSB actually behaves unethically.

### 4.3 Interruptions and variety (against repetitiveness)
- **The dedicated line:** the phone rings in the middle of a case with a quick 15-second question («Сколько доп. карт бесплатно?»). Answer it or let it ring out.
- **VIP escalation:** an OPC+ client with several accounts across asset types needs a combined solution.
- **Returning clients** with consequences from earlier shifts.
- **Days of the month** matter: the same problem on the 5th and on the 28th calls for different advice (time weighting).
- **Difficulty curve:** shift 1 teaches the two main conditions; shift 2 covers purchases, QR and utilities; shift 3 covers cash and transfers; shift 4 covers regions, OPC+ and combined cases; after that, cases are generated procedurally from templates. Build **≥ 24 handwritten cases plus a generator** that produces new cases from templates, always checked by the engine.

### 4.4 Reference cases (the quality bar; the numbers are checked)
1. **Анна, Moscow, OPC.** It's the 20th of a 30-day month. Her average balance for the 1st–19th is 2.6 млн (on her card), and she has 1.2 млн in a brokerage account at another bank. She wants to keep free service. There are two correct answers. **(a)** Move the brokerage account to PSB now: 2.6×19 + 3.8×11 = 91.2 млн ruble-days ÷ 30 = **3.04 млн ✓**. **(b)** If she spends money anyway, make ≥ 50 000 ₽ of card purchases this month, since her balance is already ≥ 1 млн ✓. Adding cash on the 28th would **not** get her there.
2. **Игорь, Moscow, OPC.** Balance 1.4 млн; he pays for everything by QR code, 80k a month; he was charged 3 990 ₽ and asks why. **QR payments don't count as purchases** and 1.4 млн < 3 млн. The fix is to pay by card, sticker or contactless, and pay utilities through PSB-Retail.
3. **Ольга, Yekaterinburg office.** Balance 1.7 млн, no purchases; she's worried she has to pay. **She doesn't**: the regional threshold is 1.5 млн. The trap is applying 3 млн. The right advice is «ничего не менять».
4. **Сергей, OPC.** He wants to send 150 000 ₽ to his son at another bank by SBP, and hasn't used any SBP this month. By SBP it's **0.5% of the whole 150 000 = 750 ₽**. By account details through the internet bank it's **0 ₽** (within 500 000 a month).
5. **Марина, OPC.** She wants 50 000 ₽ in cash from the desk at the office. At the desk that's **1% = 500 ₽**; at the PSB ATM in the lobby it's 0 ₽. (If she needed 150 000, the desk would be free.)
6. **Дмитрий, OPC+, Moscow.** Balance 6 млн, card purchases 120k a month; he's surprised by a 10 000 ₽ fee. He's short of the 150k in purchases. There are three fixes, ranked: add ≥ 30k in card purchases (utilities through PSB-Retail count); raise the balance to 10 млн; or **downgrade to OPC**, where 6 млн ≥ 3 млн is free but he loses unlimited lounges and taxi cashback. The last one is a matter of values, so ask him what matters to him. Remember that OPC+ has **no salary condition**.
7. **Елена** opened OPC on the 27th and wants to cancel next month because «не понравилось». The grace month is free, but ending the agreement during the grace period or the following month means **a one-off 3 990 ₽ fee**. The honest advice is to state the cost and suggest weighing whether keeping it is worthwhile.
8. **Павел** wants 5 additional cards for his family. **3 are free**; the 4th and 5th cost 6 000 ₽ a year each (OPC).

### 4.5 A shift
Start with a short 3D arrival: the lights come on in the office and the first client walks in. End with a shift report: trust, money saved, accuracy, KPI, a list of mistakes with clauses, and your manager rank. Save progress in `localStorage` (inside try/catch).

---

## 5. Client mode (compact)

- An isometric 3D diorama of the city: home, the PSB office, a shop, an ATM, the airport (lounge) and a taxi rank. There's a **month calendar**; each day you choose 0–2 actions: move money, pay, withdraw, transfer, travel.
- The same engine calculates the month live, with a **"forecast average balance"** meter.
- **The twist:** at the office, the manager NPC gives advice, and sometimes it's wrong (from the section 4.4 pool). The player can "check the handbook" and refuse bad advice. That puts the player on the other side of the same knowledge.
- One to three months, then a statement with what you paid in fees and why.

---

## 6. 3D and art direction

- **Three.js**, pinned version, via an `importmap` from `cdn.jsdelivr.net/npm/three@<version>/…`. Check that the version exists. Take `RoomEnvironment` from `examples/jsm` for PBR reflections. Bloom (`UnrealBloomPass`) only if it holds the frame rate; turn it off on mobile.
- **Everything procedural, no external models or textures:** marble from a canvas-generated texture; brushed copper as `MeshStandardMaterial` with metalness around 0.9; graphite walls, copper slats, warm spotlights.
- **The psbank.ru premium visual language** (marble spheres, copper, a gold ring for OPC+, sculptural calm) as **inspiration, not a copy**: **no PSB logos**, no reproduced ad imagery.
- **People are "marble mannequins":** stylised low-poly figures without faces. They're elegant, avoid the uncanny valley, and match the style. Posture and accent colours carry character. Animate them simply but smoothly: walk, sit, gesture.
- **The camera:** in manager mode, sitting at the desk facing the visitor's chair, with the waiting lounge visible behind glass (you can see the queue building up). Smooth transitions. In client mode, a ¾ isometric view of the diorama.
- **UI** is a DOM overlay in the same style as the earlier film and game: Unbounded + Manrope, copper/gold on graphite. Keep the reading content large, since the handbook is text.

## 7. Audio
Procedural Web Audio, no licensed music: a calm lo-fi jazz-ambient score in F minor during the shift, rising as the queue grows. Also a phone ring for the dedicated line, a soft "stamp" when advice is submitted, and good and bad chords for outcomes. A mute button, remembered between sessions.

## 8. Technical requirements
- One file, `games/opc_klub.html`. No build step. External scripts only from `cdn.jsdelivr.net` (three) and fonts from Google Fonts.
- Must work on phones in portrait: a touch UI where the handbook and cards are bottom sheets. DPR ≤ 1.5, fewer than ~150 draw calls, shadows only from the main light. Target 60 fps on desktop and ≥ 30 fps on a mid-range phone.
- Keyboard: 1–9 for cards, H for the handbook, Enter to confirm, P to pause. Respect `prefers-reduced-motion`.
- The code is structured into sections: `TARIFF`/`RULES` → `CASES`/`GENERATOR` → `SIM` → `SCENE` → `UI` → `AUDIO`. Expose `window.KLUB` for tests.

## 9. Scope and priorities
1. Rules engine + `?test` (must be done).
2. Manager mode: one polished shift of 8 cases with consequences and a debrief (must be done).
3. The full manager arc: 4 shifts + the generator + returning clients.
4. The 3D polish: arrivals, lighting, the queue behind glass.
5. Client mode.

If you're short of time, cut from the bottom of this list, **never** the engine's correctness or the debrief.

## 10. Before you hand it back
- `?test` passes all assertions.
- A Playwright bot plays a shift twice: once "perfectly" (asking the engine for the best advice) and once randomly. The perfect bot must end with high trust and no complaints; the random bot must get returns and complaints. If both score the same, the scoring is broken.
- Screenshots at 1440×900, 1024×768 and 390×844, with no console errors (fonts blocked by the sandbox's proxy is expected).
- Re-read every case in `CASES` and check its numbers by hand against section 2. **One wrong fact in a game that teaches the product is worse than a missing feature.**
- Commit to the working branch with a clear message.

## 11. Guardrails
- An **unofficial fan game**: say so on the title screen. It isn't advertising or an offer from PSB, and the tariffs are those in force from 01.07.2026.
- No real people and no PSB logos. Characters are fictional.
- Don't invent facts. If a case needs a fact that isn't in section 2, drop the case.
- The ethics mechanic is about the **player's** choice, not a claim about how the real bank behaves.
