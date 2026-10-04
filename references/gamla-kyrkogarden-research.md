# Gamla kyrkogården i Kalmar – underlag för modellering

Sammanställt 2026-10-01 med webbsökning. Bilder är referenser och ligger kvar hos källorna; inget är nedladdat till projektet.

**Säkerhetsmärkning:**
- **[KÄLLA]**: står uttryckligen i en primär eller auktoritativ källa (Sveriges kyrkor, RAÄ, Kalmar läns museum).
- **[MÄTT]**: uppmätt av mig från en skalsatt ritning eller från OSM. Felmarginalen anges.
- **[OSÄKERT]**: härlett, uppskattat eller motsägs av en annan källa.

**Viktigaste fyndet:** två skalsatta planer går att lägga ovanpå varandra med det Stagnellska gravhuset som gemensam fixpunkt. Den ena är Sven Rosmans grävningsplan från 1924 (Sveriges kyrkor vol. 158, plansch I). Den andra är Harald Åkerlunds gravvårdsplan från 1944, kompletterad 1974 (Sveriges kyrkor vol. 162, plansch XIII). Båda finns fritt som PDF på DiVA, se Källor. Kyrkans planform finns som skalsatt rekonstruktion av läget omkring år 1610. Där finns också fasader, så höjderna går att mäta.

## Koordinatsystem i detta dokument

- **EN** = meter öster/norr (sant norr), origo i den **södra spetsen av OSM-polygonen** `w149032114` (landuse=cemetery, "Gamla Kyrkogården", 9 272 m² enligt `references/osm-slott98.json`). Spetsen ligger i projektramen på (x −950,4; y −15,2).
- **proj** = projektets ram (x mot ENE, 28,2° från öst; origo 56,66412 / 16,3656). Formeln är densamma som i `scripts/prepare_block79.py`.
- Åkerlunds plan stämmer med OSM inom ungefär 1–4 m. Hörnen i NV (−33,2; 108,7) och NÖ (59,2; 121,1) motsvarar OSM-hörnen (−32,0; 108,6) och (62,3; 124,6). Planen är norrorienterad inom ungefär 1°. **[MÄTT]**
- RAÄ:s egen polygon (L1958:9244) är däremot förskjuten och för liten, ungefär 7 900 m². Använd inte den för läget. **[MÄTT]**

---

## Kyrkan

### Namn och identitet
- Kyrkan hette **Bykyrkan** ("by" = stad), även **Storkyrkan** eller **S:t Nikolai kyrka**. Den var helgad åt S:t Nikolaus av Myra, skyddshelgon för sjöfarare och köpmän. **[KÄLLA]**
- Det var **inte Sankt Johannes**. Dagens S:t Johannes kyrka i Kalmar är byggd 1979–80 och har inget med den medeltida stadskyrkan att göra. **[KÄLLA]**
- Gamla staden hade också en mindre kyrka, *Sancta Birgittas kyrka* ("Lilla kyrkan", senare Tyska kyrkan), och Svartbrödraklostret. Ingen av dem låg på Gamla kyrkogården. **[KÄLLA]**

### Datering
| Händelse | År | Status |
|---|---|---|
| Första kyrkan och kyrkogården anläggs | 1200-talets första hälft (museet anger "omkring 1200") | [KÄLLA] |
| Kyrkogården nämns första gången (avtal som minskar den) | 1293 | [KÄLLA] |
| Utbyggd omkring 1300; kapellrader på långsidorna under senare 1300-tal; färdig femskeppig kyrka | tidigt 1400-tal | [KÄLLA] |
| Erik av Pommern kröns här (Kalmarunionen) | 17 juni 1397 | [KÄLLA] |
| Kungen förklarar kyrkan som "halvan dom" | 1430 | [KÄLLA] |
| Bränd och svårt förstörd i Kalmarkriget (valven rasar, tornet skadas) | 1611 | [KÄLLA] |
| Återställd efter 1611; tornet byggs inte upp igen som torn, taket dras över det | 1613–1630-tal | [KÄLLA] (Olssons sammanfattning) |
| Skadad i stadsbranden | 1647 | [KÄLLA] |
| Sprängd med krutladdningar och jämnad med marken; stenen går till domkyrkan och fästningsverken | 1678 | [KÄLLA] |
| Gravvalv i det gamla kyrkgolvet bryts upp | 1857 | [KÄLLA] |
| Arkitekten Sven Rosman gräver ut grundresterna | 1924 | [KÄLLA] |

### Plan och mått
Källa: Martin Olsson, *Kalmar gamla stads kyrkor 1. Storkyrkan* (Sveriges kyrkor vol. 158, 1974). Olsson bygger på Rosmans utgrävning.
- **Total längd cirka 75 m och total bredd cirka 38 m** inklusive kapellraderna. Utan högkoret var längden 65 m. **[KÄLLA]**
- **Äldsta kyrkan:** treskeppig, cirka 50 × 22 m (utvändigt, utan torn). Den hade ungefär 2 m tjocka grundmurar av gråsten och två rader fyrsidiga pelargrunder. **[KÄLLA]**
- **"Koret":** förlängning mot öster, cirka 12 m lång, lika bred som långhuset. Byggd av kalksten med strävpelare, även snedställda hörnsträvpelare. **[KÄLLA]**
- **"Högkoret":** cirka 10 m långt, lika brett som mittskeppet och tresidigt avslutat (polygonal östände). Grunden förstördes 1906 när ett lasarettshus byggdes på platsen. Bara NÖ-hörnet med strävpelare hittades. **[KÄLLA]**
- **Kapellrader:** en sammanhängande rad på norra sidan och en på södra, med smalare murar (ned till 1 m). Enligt Kalmar läns museum fanns sex kapell med altare på ena långsidan och sju på den andra. **[KÄLLA]**
  - Kapellens namn enligt planen omkring 1610:
    - Norr, från väster: **Kalkkoret (U)**, T, S, *Bårkammaren*, R, Q och **Lübeska koret (P/O)**.
    - Söder, från väster: **Södra valvet (D)**, **Vapenhuset (E) med "Stora kyrkodörren"**, F, G, H, I och **Sakristia och liberiet (J)**.
  - Kalkkoret sköt ut cirka 3 m väster om västfasaden. Stadsplanerna anger cirka 5 m, men det motsägs av utgrävningen. **[KÄLLA]**
- **Långhuset omkring 1610:** femskeppig hallkyrka (tre skepp och kapellens två) med sex pelare i varje rad enligt räkenskaperna. På planen syns fyra fria pelare per rad i det västra långhuset. **[KÄLLA]** / [OSÄKERT om exakt antal]
- **Tornet:** västtorn med **två höga spiror**. Det står på informationstavlan och i Olssons rekonstruktion. Olsson ger tornet cirka **9 m i öst–väst och cirka 14 m i nord–syd** (bredden är ett antaget medelvärde) och spirorna cirka 7 × 9 m vid basen. Spirorna är gotiska och senare än tornkroppen. Sylvanders teori att tornet stod i NV-hörnet har vederlagts. **[KÄLLA]**, men tornets bredd är **[OSÄKERT]**.
- **Material:**
  - grundmurar av gråsten och granit;
  - murverk av **öländsk kalksten**;
  - koret hade kalkstensmur med ett invändigt lager av halvstens tegel;
  - golvet var av tegel och kalksten.
  **[KÄLLA]**

### Mått tagna ur Olssons skalsatta rekonstruktioner (läget omkring 1610)
Planen finns som plansch II (skala 1:300). Fasaderna är plansch V (söder) och VII a–b (öster och väster) i vol. 158. Måtten nedan är **[MÄTT]** av mig, med en felmarginal på ±0,5–1 m:

| Del | Mått |
|---|---|
| Hela kyrkan, ytterlinje | cirka 74 m (västmur Södra valvet → högkorets spets) × cirka 36 m (norra kapellradens ytterliv → södra) |
| Mittskeppet, invändigt | cirka 7,8 m brett |
| Sidoskeppen, invändigt | cirka 5,5 m vardera |
| Långhuset, invändigt (tre skepp) | cirka 38 × 19 m |
| Travéer | cirka 8 m |
| Koret ("Kor" och "Långa koret") | cirka 11 m långt, cirka 21 m brett |
| Högkoret | cirka 10 m långt, cirka 14 m brett, tresidig avslutning |
| Spirornas spets | cirka 52–53 m över mark |
| Tornmurens takfot | cirka 26 m |
| Långhusets takås | cirka 22 m |
| Långhusets takfot | cirka 13,5 m |
| Kapellradens takfot | cirka 6,3 m |
| Kapellgavlarnas toppar (sågtandsrad av gavlar mot söder) | cirka 13 m |
| Takryttare över koret | cirka 30 m |
| Högkorets takås | cirka 15 m |

### Läge på dagens kyrkogård
Rosmans grävningsplan 1924 (plansch I, vol. 158) visar kyrkans grundmurar, den nuvarande kyrkogårdsgränsen, lasarettet och **det Stagnellska gravhuset**. Därför går läget att bestämma ganska väl:
- **Gravhuset står på linjen för kyrkans södra yttermur**, ungefär 11–14 m öster om kyrkans västligaste hörn (Södra valvet). Det ligger alltså vid vapenhuset och "Stora kyrkodörren", i kyrkans sydvästra del. Olsson bekräftar det: fig. 129 visar golvrester vid "Stora västra kyrkodörren" med gravhuset överst i bilden. **[KÄLLA + MÄTT]**
- **Kyrkans längdaxel har bäring cirka 80°**, alltså cirka 10° norr om öst. Det är **[MÄTT]** genom jämförelse mellan Rosmans plan, museets karta och OSM. Felmarginalen är ±5° och värdet är **[OSÄKERT]**.
- Kyrkan ligger i kyrkogårdens **södra och mellersta del**. RAÄ skriver "S om områdets centrala del". Kristoffermonumentet står i kyrkogårdens SÖ del "på platsen för den försvunna Storkyrkan". **[KÄLLA]**
- Östpartiet ligger **utanför dagens kyrkogård**. Högkoret och delar av koret ligger under lasarettsbygget från 1906 (det gamla lasarettet vid Slottsvägen). Samma år lades Österlånggatan igen och kyrkogårdens SÖ-gräns fick sitt nuvarande läge. **[KÄLLA]**

Kyrkans hörn i EN (från OSM-spetsen) och i proj, förankrade i gravhusets mitt och beräknade med axeln 80°. Alla punkter är **[MÄTT/OSÄKERT, ±2–3 m]**:

| Punkt | EN (m) | proj (x, y) |
|---|---|---|
| Gravhusets mitt (OSM-byggnad `w500979084`) | (−17,6; 21,9) | (−955,6; 12,5) |
| Kyrkans SV-hörn (Södra valvet) | (−30,7; 18,0) | (−968,9; 15,2) |
| Kalkkorets NV-hörn | (−34,2; 54,0) | (−955,1; 48,6) |
| Norra kapellradens NÖ-hörn (Lübeska koret) | (16,4; 62,9) | (−906,2; 32,5) |
| Korets NÖ-hörn | (27,0; 56,8) | (−899,7; 22,1) |
| Högkorets östspets | (38,9; 47,6) | (−893,6; 8,4) |
| Högkorets SV-hörn | (30,2; 38,8) | (−905,4; 4,7) |
| Sakristians SÖ-hörn | (25,8; 30,4) | (−913,3; −0,6) |
| Södra kapellradens SÖ-hörn | (21,3; 27,2) | (−918,8; −1,3) |
| Tornets mitt (mellan Kalkkoret och Södra valvet) | (−22,7; 36,5) | (−953,2; 27,7) |
| Kyrkans ungefärliga mittpunkt | (2; 42) | – |

Kontroller av placeringen:
- Kristoffermonumentet (−4,0; 41,6) hamnar i mittskeppets axel, cirka 17 m öster om gravhuset. Det stämmer med källorna.
- Kalkkorets västmur hamnar cirka 12–13 m innanför kyrkogårdens västmur. Rosmans plan ger cirka 12 m.
- RAÄ:s punkt för kyrkplatsen (L1958:9149) ligger cirka 10 m norr om min mittpunkt. RAÄ:s koordinater är grova.

### Synligt i dag
- **Kantställda kalkstenshällar** markerar ungefär var kyrkan låg. RAÄ skriver: "Kyrkplats, ca 75x35 m utan idag synliga lämningar. Kyrkans ungefärliga utsträckning ställvis markerad med kantställda kalkstenshällar." På museets karta från 2006 är kyrkplatsen ett grått fält: "Bykyrkans läge, idag markerat av kantställda stenar". **[KÄLLA]** Hur stenarna ser ut och exakt var de står är **[OSÄKERT]**. Landsantikvarie Hofrén ville 1935 ersätta dem med en orienteringskarta.
- **Kristoffermonumentet (nr 45, RAÄ Kalmar 56:3, L1958:8710):** en fyrsidig pelare av ljusröd granit, **2,1 m hög, 0,61 × 0,52 m**, på en granitplatta som är 0,1 m hög och 0,91 × 0,91 m. **[KÄLLA]**
  - Överst står en bronsstatyett av S:t Kristoffer med Jesusbarnet på axeln, av Arvid Källström.
  - Inskriften står på norra sidan: TILL MINNE AV KALMAR STORKYRKA SPRÄNGD 1678.
  - På södra sidan finns **kyrkans plan i relief** efter Rosman.
  - På östra sidan sitter en bronsplakett, 0,39 × 0,39 m, med kyrkan och omgivningen efter Dahlberg 1645.
  - På västra sidan sitter en likadan plakett med en interiör efter "Vicklebytavlan". Den föreställer inte Storkyrkan.
  - Monumentet bekostades av S:t Kristoffers gille. Årtalet är **[OSÄKERT]**: Sveriges kyrkor anger 1929, Wikipedia "reses 1937".
- **Informationstavlor** finns vid södra ingången. En av dem har en teckning av kyrkan med västtorn och två spiror samt sågtandsgavlarna över kapellraden.
- **Unionsstenen** restes 1997 (600-årsminnet av unionen) med namnteckningar av de nordiska statscheferna. Var på kyrkogården den står har jag inte kunnat belägga: **[OSÄKERT]**.

### Bilder och ritningar av kyrkan
| Vad | Var | Kommentar |
|---|---|---|
| **Rosmans grävningsplan 1924**, skala 1:300, med kyrkogårdsgräns, lasarett och Stagnells gravhus | Sveriges kyrkor vol. 158, plansch I = **PDF-sida 243** i https://raa.diva-portal.org/smash/get/diva2:1244147/FULLTEXT01.pdf | Bästa underlaget för läget. Norr är ungefär uppåt (cirka 10° vridning). Skalstock 0–40 m. |
| **Rekonstruerad plan omkring 1610**, 1:300, med rumsnamn | Samma PDF, plansch II (sida 244). Även blogg: https://blogger.googleusercontent.com/img/b/R29vZ2xl/AVvXsEj3k6VfEZpA5t7u0f7lxDqabE8QXuHfrjr48QJLwpFbBtB-WD6H6XblKmR-yq83C9SnHlTeHQ_U8slWb98u0P6EcaNhNugPJI9yzXMqvNADHrURiyQNtqjmg8H8SFaCWA0WXr-nu8ItnU1t/s1600/grundplan+kyrka.jpg | Söder nedåt, öster till höger. Skalstock 0–60 m. Gravhusets oktagon är inritad vid vapenhuset. |
| **Fasad mot söder omkring 1610** (1:300) | Samma PDF, plansch V (sida 247) | Ett torn och en spira i profil, sågtandsgavlar, takryttare |
| **Fasader mot öster och väster omkring 1610** (1:300) | Samma PDF, plansch VII a–b (sida 249) | Visar tornets två spiror bredvid varandra |
| Sektioner | Samma PDF, sidorna 245–246, 248 | Inte granskade i detalj |
| Erik Dahlberg, Kalmar 1645 (stadsvy; kyrkan till höger) | https://commons.wikimedia.org/wiki/File:Kalmar_Erik_Dahlbergh.jpg | Visar läget efter 1611. Olsson har visat att tornet på bilden är Söderport, inte kyrktornet. |
| Dahlbergs vy från mitten av 1670-talet; "Spionkartan" 3 juni 1611; Wolfenbüttel-teckningen 1611 | Återgivna i vol. 158 (fig. 147 ff, 149, 187–188) | Inte granskade sida för sida. Någon *Suecia antiqua*-gravyr av Storkyrkan har jag inte hittat. |
| Utgrävningsfoton 1924 (G. Weiden, M. Hofrén) | DigitaltMuseum: https://digitaltmuseum.se/021016859282, …859278, …859279, …859280, …859281, https://digitaltmuseum.se/021017024513, …024525, …024537, https://digitaltmuseum.se/021017093877 (och 021017093880–889) | Kalmar läns museum, public domain |
| Skiss över grävningarna 1924 | https://digitaltmuseum.se/021017074110 | |
| "Plan av gamla Calmare Stadskyrka – rekonstruerad … 1924" med kyrkogårdens gränser a–a, c–c, e–e och o–o | https://digitaltmuseum.se/021017077503 | Visar kyrkogårdens gränser vid olika tider (1977 års foto av planen) |
| Kringla/RAÄ KMB-foton "Kalmar storkyrka (Bykyrkan)" (mest Frigelius teckningar av gravhällar, cirka 1750) | https://commons.wikimedia.org/w/index.php?search=Kalmar+storkyrka+(Bykyrkan)+KMB | Gravhällarna i kyrkan och på kyrkogården |
| 3D-rekonstruktion (privat projekt av Nicholas Nilsson) | http://arkeologiikalmar.blogspot.com/2013/02/kalmar-storkyrka.html | Bilder från sydost och en interiör. Bygger på Olsson. |

---

## Kyrkogårdens plan

### Form och mått
- **OSM `w149032114`:** 9 272 m². **[MÄTT]**
  - Hörnen i EN, medurs från södra spetsen: (0; 0) → (−38,7; 18,5) → (−50,0; 66,7) → NV (−32,0; 108,6) → längs norra muren → (62,3; 124,6) → utskott mot NÖ-grinden (75,2; 149,6) och (82,2; 145,0) → (63,0; 94,2) → (28,8; 43,0) → tillbaka till spetsen.
  - Den långa SÖ-sidan har bäring cirka 34°. Norra sidan är cirka 95 m lång med bäring cirka 81°.
- **RAÄ:** "Ödekyrkogård, oregelbunden, **115 × 55–80 m (NÖ–SV)**." **[KÄLLA]**
- Formen är ett oregelbundet femhörnigt område, smalt i söder (spetsen mot Slottsvägen och parkeringen) och brett i norr. Den långa raka SÖ-sidan vetter mot Biblioteksparken och det gamla lasarettet. Västsidan har en knäckt mur mot Gamla stans trähustomter.
- Kyrkogårdens gränser lades fast på 1600-talet: kyrkogården minskades i slutet av 1600-talet och fick då mur runt om. SÖ-gränsen ändrades 1906. **[KÄLLA]**

### Murar
- RAÄ: "I S-V-N-NÖ omgärdad av stenmur, **1–1,3 m h, 0,75 m br**, av murade (betong) gråstenar med gjutet krön. **I NÖ–S saknas mur**." **[KÄLLA]**
- Muren är alltså kallmurad gråsten, delvis cementfogad. Den löper längs söder–väster–norr till NÖ-hörnet. **SÖ-sidan mot Biblioteksparken saknar mur**. Där stod tidigare ett gunnebostängsel, som är borttaget. **[KÄLLA]**
- Kalmar läns museums rapport från 2006 skriver på ett ställe "alla väderstreck utom sydväst" och på ett annat "utom sydost". Kartan och RAÄ visar att **sydost** är rätt.
- 1987 års murarbete avslöjade en murklack, tolkad som en gammal husgrund, under muren. **[KÄLLA]**

### Ingångar
- Det finns **två ingångar med dubbla svartmålade smidesgrindar**: en i söder/sydväst och en i nordost. **[KÄLLA]**
  - **Södra ingången** ligger vid kyrkogårdens sydspets, cirka (−8; 0) i EN, mot Slottsvägen och parkeringen. Informationstavlan står strax innanför, vid den röda punkten på museets karta. **[MÄTT]**
  - **NÖ-ingången** ligger där grusgången når NÖ-hörnet, mot Molinsgatan, vid OSM-utskottet (75–82; 145–150).
- Historiskt hade kyrkogården 1627 minst fyra ingångar (mot torget i söder, mot öster, norr och väster), med galler som kreatursspärr. 1671 gjordes "twenne Portar". 1777 fick den "nya portar och murar". Grindarna av konstsmide skänktes senare till Solliden. **[KÄLLA]**

### Gångar
- Det finns **en grusgång (fint grus)** längs hela SÖ-gränsen, från södra ingången till NÖ-hörnet. Från den går **en böjd sidogång västerut till Stagnells gravhus**, som avslutas med en **rund grusplats runt gravhuset**. Diametern är cirka 9 m på Åkerlunds plan. I övrigt är allt gräs. **[KÄLLA + MÄTT]**
  - Gångarna finns i OSM: `w149032157` (huvudgången), `w500979083` (gången till gravhuset) och `w441934472` (ytterligare en grusgång längs SÖ-sidan). **[MÄTT]**
- På Åkerlunds plan finns streckade äldre gångslingor, en stor ögla i norra delen och en i södra. De syns inte i dag. **[OSÄKERT]**

### Byggnader
- **Stagnells gravhus** är den enda byggnaden. Se det egna avsnittet nedan.
- **Benhuset** byggdes 1777 i kyrkogårdens **nordvästra hörn** och revs 1888. Det var femsidigt, av sten, med 7 m långa sidor och högt valmtak. På en stång överst satt en dödskalle med korslagda ben i förgylld koppar. Dörren låg i SÖ-väggen med två inskriftstavlor från 1645 och 1777. På Åkerlunds plan är det inritat streckat vid cirka (−29; 105) i EN. Det äldre benhuset från 1645 stod vid den nordöstra muren. **[KÄLLA]**
- **Skolstugan** stod i kyrkogårdens nordvästra del och revs i slutet av 1600-talet. **[KÄLLA]**

### Vegetation
- Det finns flera gamla **almar, lindar, hästkastanjer och hängask**. Kyrkogården har en trädvårdsplan, och gamla träd ersätts successivt. **[KÄLLA]**
- Museets karta från 2006 (`Träd.shp`) visar cirka 50 trädlägen jämnt spridda. Det finns en tät grupp på kyrkplatsen och några träd längs SÖ-gången. Fotona från 2014 visar stora hästkastanjer söder och öster om Kristoffermonumentet. **[KÄLLA + foto]**
- Hela kyrkogården är gräsbevuxen och parklik. Flest gravvårdar finns i söder och öster. **[KÄLLA]**

### Kartor och planer
| Vad | URL |
|---|---|
| **Åkerlunds gravvårdsplan 1944/1974**, numrerad 1–168, med skalstock 0–40 m, norrpil, gångar, murar, gravhus och benhusets plats | Sveriges kyrkor vol. 162, plansch XIII = **PDF-sida 10** i https://diva-portal.org/smash/get/diva2:1244151/FULLTEXT01.pdf (texten finns i FULLTEXT02.txt) |
| Kalmar läns museums folder (2006): karta med murar, grus, kullersten, gravar, träd och kyrkplatsen markerad, skala 50 m | https://www.svenskakyrkan.se/Sve/Bin%c3%a4rfiler/Filer/29C1E1C4-5D72-45D0-A883-76C5E4913A8A.pdf |
| Kalmar läns museum, *Gamla kyrkogården*, fördjupad inventering 2006 (M. Jonsson). Den bilagda gravvårdskartan ingår inte i webb-PDF:en. | https://kalmarlansmuseum.se/wp-content/uploads/2022/05/kalmargamlakyrkogard.pdf (även https://www.svenskakyrkan.se/Sve/Bin%c3%a4rfiler/Filer/55EBCB3A-0689-46A5-8529-FA20DB1246EB.pdf) |
| Historiska kartor: D. Schmidt 1698 (kyrkogården med "Capell"), Köhlin nr 176 omkring 1721 (förminskad kyrkogård med ny mur), Frigelius plan från 1750-talet | Återgivna i vol. 162, fig. 215, 216 och 324 (PDF-sidorna 16–17) |
| Rosmans plan med kyrkogårdens gränser vid olika tider | https://digitaltmuseum.se/021017077503 |

### Valda monument, lägen ur Åkerlunds plan
Lägena är **[MÄTT]** ur Åkerlunds plan med en felmarginal på ±1,5 m.

| Nr | Monument | EN (m) | proj (x, y) |
|---|---|---|---|
| 1 | Stagnells gravhus | (−17,6; 21,9) | (−955,6; 12,5) |
| 45 | Kristoffermonumentet | (−4,0; 41,6) | (−934,2; 23,4) |
| 15 | Obelisken över Per Wijk | (−9,3; 20,8) | (−948,7; 7,6) |
| 28 | Biskop Magnus Stagnelius, gjutjärnskors | (−19,6; 29,0) | (−953,9; 19,7) |
| 20 | Marmorurnan, Johansson | (−29,4; 27,4) | (−963,4; 22,9) |
| 22–23 | Nordenanckar, kolmårdsmarmor | (−22,4; 25,7) | (−958,0; 18,1) |
| 36 | Familjen Wiberg, gjutjärnsstaket med två gjutjärnskors | (−32,3; 37,5) | (−961,1; 33,2) |
| 44 | Gravplats med smidesstaket | (−10,0; 51,0) | (−935,1; 34,5) |
| 50 | Swarss tumba med smidesstaket | (5,4; 51,9) | (−921,1; 28,0) |
| 53 | Wiganders gjutjärnskors | (12,6; 38,9) | (−921,0; 13,2) |
| 54 | Ekmans tumba | (16,6; 41,7) | (−916,0; 13,8) |
| 73 | Jägers gjutjärnskors | (27,1; 46,6) | (−904,5; 13,1) |
| 74 | Kinneckes pelare | (27,7; 49,5) | (−902,6; 15,4) |
| 96 | Balabregas urna | (30,0; 104,8) | (−874,5; 63,0) |
| 139 | Korssemans obelisk | (41,5; 80,7) | (−875,7; 36,3) |
| 166–168 | 1500-talshällarna (Grip, Lillie, Stierna), längs SÖ-gången | (cirka 46; 86–92) | (cirka −868; 39–44) |

---

## Stagnelius gravkapell

**Namnet är missvisande.** Källorna kallar byggnaden *det Stagnellska gravkoret* eller *gravhuset*. Det byggdes **inte** för biskop Magnus Stagnelius, utan för **lektor Johan Stagnell/Stagnel** (1711–1795) och hans hustru **Anna Margareta Botin** (1731–1773). Johan Stagnell var farbror till biskop Magnus Stagnelius och alltså bror till skaldens farfar. **[KÄLLA]**
- Biskop **Magnus Stagnelius** (död 1829, 82 år) är visserligen begravd på Gamla kyrkogården, men under ett **gjutjärnskors (nr 28, 187 × 107 cm)** tillsammans med hustrun Hedvig Christina Bergstedt (död 1859). Korset står cirka 7 m NNV om gravhuset. **[KÄLLA + MÄTT]**
- Skalden Erik Johan Stagnelius är inte begravd här.

### Utseende enligt Sveriges kyrkor vol. 162, nr 1
- **Åttasidig gravbyggnad av tegel**, putsad och kalkfärgad **gulgrå**. I dag är den tydligt ockragul. **[KÄLLA]**
- **Väggarnas rektangulära mittpartier är insänkta cirka 15 cm.** Varje sida har alltså en fördjupad panel, inramad av hörnlisener. **[KÄLLA]**
- Under takfoten löper en **putsad fris** (DigitaltMuseum 021017059179) och en sockel av grå sten. **[KÄLLA + foto]**
- **Taket** beskrivs som "koniskt sexsidigt, täckt med järnplåt och oljemålat svart". **[KÄLLA]** Fotona från 1973 och 2014 visar dock en **svängd, klock- eller lökformad huv** med falsade ribbor i hörnen, utkragad takfot och spetsig topp. **[foto]** Antalet takfall (sex mot åtta) är **[OSÄKERT]**. Byggnaden är åttasidig, och på fotot verkar taket följa den.
- **Toppen** hade tidigare en cylindrisk eller sexsidig lanternin som bar en dödskalle med korslagda ben. Det framgår av John Roséns teckning från 1871, som visar ett rakt, valmat åttasidigt tak med liten lanternin och spira. Prydnaden är borta. **[KÄLLA]**
- **Dörren** sitter i **norra väggen**, alltså mot kyrkogårdens inre och gångens rundel. Den är rektangulär, plåtklädd och svartmålad. **På var sida om dörren finns en halvkolonnett** utan bärande funktion. **[KÄLLA]**
- **Över dörren** sitter en **tavla av röd kalksten** med en lång inskrift: HÄR HVILA 2 KÄRA VÄNNER / LECT: HR IOH: STAGNEL … och FRU ANNA MARGARETA BOTIN … (fullständig text i vol. 162 s. 368). **[KÄLLA]**
- **Byggår** anges inte. Inskriften omfattar hans död 1795, så tavlan sattes upp 1795 eller senare. Byggnaden tillkom troligen mellan 1773 och 1795. **[OSÄKERT]**
- Byggnaden renoverades på 1920-talet. 1950 diskuterades en restaurering av en av minnestavlorna, och 1980 behövde den lagas och målas. **[KÄLLA]**

### Mått
| Mått | Värde | Status |
|---|---|---|
| Diameter mellan hörnen | cirka 4,8–5 m (OSM-byggnad `w500979084`: oktagon med radie 2,3–2,6 m, 16,6 m²) | [MÄTT] |
| Diameter enligt planerna | cirka 4,9 m (Åkerlund), cirka 4,4 m (Rosman) | [MÄTT] |
| Sidlängd | cirka 1,9–2,0 m | [MÄTT] |
| Väggarnas höjd till takfot | cirka 3–3,5 m | [OSÄKERT], uppskattat från foto mot dörrhöjden |
| Takhuvens höjd inklusive spets | cirka 3 m | [OSÄKERT], uppskattat från foto |

### Läge
- Gravhuset står i **kyrkogårdens södra till sydvästra del**. Det står "i sydvästra hörnet" enligt museet och "in the southernmost part" enligt Sveriges kyrkor.
- Mitten ligger vid **EN (−17,6; 21,9)**, proj (−955,6; 12,5): cirka 28 m norr om och 10 m väster om södra ingången, och cirka 12 m innanför SV-muren.
- Det står mitt i grusrundeln vid änden av sidogången.
- Gravhuset står ovanpå linjen för Storkyrkans södra mur, vid det forna vapenhuset (se Kyrkan).

### Bilder (endast referenser)
| Vad | URL |
|---|---|
| Foto 2014, gravhuset bakom Kristoffermonumentet, från NO | https://commons.wikimedia.org/wiki/File:Kalmar_%C3%96dekyrkog%C3%A5rden_02.png |
| Foto 2014, gravhuset med dörren mot norr, från NO | https://commons.wikimedia.org/wiki/File:Kalmar_%C3%96dekyrkog%C3%A5rden_05.png |
| Foto 2016, översikt med gravhuset i bakgrunden | https://commons.wikimedia.org/wiki/File:Gamla_kyrkog%C3%A5rden_i_Kalmar.jpg |
| Foto 1973 (R. Boström), fig. 222 | vol. 162 PDF-sida 23 |
| Teckning av John Rosén 1871 med den gamla takformen, fig. 221 | vol. 162 PDF-sida 22 |
| DigitaltMuseum, gravhuset med skador på frisen | https://digitaltmuseum.se/021017059179 |
| DigitaltMuseum, gravhuset | https://digitaltmuseum.se/021017064890 |
| DigitaltMuseum, gravhuset och kyrkogården | https://digitaltmuseum.se/021016470653 |
| DigitaltMuseum, gravhuset och muren (serien 021017109604–109607) | https://digitaltmuseum.se/021017109604, https://digitaltmuseum.se/021017062354, https://digitaltmuseum.se/021017062355 |
| DigitaltMuseum, teckningar | https://digitaltmuseum.se/021016526436, https://digitaltmuseum.se/021017079634 (tuschteckning av John Sjöstrand) |
| Svenska kyrkans folder, gravkoret på omslagsfotot | https://www.svenskakyrkan.se/Sve/Bin%c3%a4rfiler/Filer/29C1E1C4-5D72-45D0-A883-76C5E4913A8A.pdf |

---

## Gravstenar

### Översikt
- **Antal:** cirka 160 gravvårdar fanns kvar 2006. Sveriges kyrkor från 1976 beskriver nr 1–172a på kyrkogården och nr 173–273 efter Frigelius teckningar från omkring 1750 (många försvunna). RAÄ anger "ett 100-tal gravstenar, ett 30-tal med väderskydd av plåt". Flera hällar täcks vintertid. **[KÄLLA]**
- **Typer:** **[KÄLLA]**
  - **Liggande hällar av kalksten**, röd och grå öländsk kalksten, är i majoritet. Många är från 1600-talet och har dekor: änglahuvuden, timglas, dödskalle med ben, lagerkrans, bomärken, kalk och ros.
  - De flesta **stående vårdar är från 1800-talet**. De är klassicistiska och har facklor, urnor, akroterier, pinjekottar och stjärnor.
  - **Gjutjärnskors** är vanliga vid mitten av 1800-talet. Flera har trepassavslutade armar, fjäril och puppa samt nedåtvända facklor; några bär märket "BOLINDER STOCKHOLM".
  - Det finns dessutom **tumbor** (låga kistformade gravar), gravplatser med **smidesstaket**, **obelisker**, en **marmorurna** och en **keramikurna**.
- **Återanvändning:** det är vanligt att 1600-talshällar har återanvänts under 1700- och 1800-talen. Spår av den äldre inskriften finns ofta kvar. Ett exempel är hällen för bagaren Hans Friborn från 1668, som återanvändes 1841 av juveleraren C. G. Högstedt. **[KÄLLA]**
- **Äldst:** ett fragment av en **senmedeltida häll** med latinsk text ("…his wife Ma…"). Därefter kommer tre **1500-talshällar** som har legat inne i kyrkan. **[KÄLLA]**
- **Ursprungligt läge:** de yngre vårdarna från 1800-talets mitt står troligen på sina platser. De äldre hällarna är för det mesta flyttade. **[KÄLLA]**
- **Kyrkans egna gravhällar:** många låg i kyrkgolvet. En del flyttades 1834 till domkyrkans golv. Andra förvaras på slottet. Frigelius ritade av en stor del 1750–54, och teckningarna finns i KB. **[KÄLLA]**

### Särskilt kända gravar
Numren följer Åkerlunds plan, och lägena finns i tabellen under Kyrkogårdens plan.

| Nr | Vem, datum | Typ, mått | Läge | Status |
|---|---|---|---|---|
| 166 | **Christopher Andersson (Grip)** till Stensnäs och hustrun Gertrud Ulfsdotter (Snakenborg), död på Kalmar slott 1588. Grip avrättades vid Kalmar blodbad 16/5 1599, och hans dödsdatum höggs aldrig in. | Grå kalkstenshäll, **180 × 150 cm**, med riddare och dam i relief. Hällen är stympad så att båda saknar huvud. Enligt traditionen lät hertig Karl slå sönder den. Den låg inne i kyrkan, "in mot höge Choren". | NÖ delen, vid SÖ-gången | [KÄLLA] |
| 167 | **Brunte Birgersson (Lillie)**, död 1586 | Kalkstenshäll **236 × 120 cm** med evangelistsymboler och harneskklädd riddare. Nu kraftigt vittrad. Den låg ursprungligen i högkoret. | Som ovan | [KÄLLA] |
| 168 | **Christina Månsdotter (Stierna)**, död 6/1 1594 | Kalkstenshäll **210 × 124 cm** med kvinnorelief och vapen (Stierna, Bölja) | Som ovan | [KÄLLA] |
| 1 | Johan Stagnel med hustru | Gravhuset, se ovan | S/SV | [KÄLLA] |
| 28 | **Biskop Magnus Stagnelius**, död 1829, och Hedvig Christina Bergstedt, död 1859 | Gjutjärnskors **187 × 107 cm** på postament | S, nära gravhuset | [KÄLLA] |
| 15 | **Kansliråd Per Wijk** (1746–1823), stiftare av Wijkska fonden | **Obelisk av slipad svart granit, cirka 3,5 m hög**, på en rund jordkulle med 3 m diameter | Cirka 8 m öster om gravhuset | [KÄLLA] |
| 20 | Konsistorienotarien Johan Johansson, död 1836 | **Vit marmor, cirka 225 cm hög**, med urna, akantus och pinjekotte | SV | [KÄLLA] |
| 22–23 | Landshövding Gustaf Peter Nordenanckar, död 1839, och Henrika Nordenanckar, död 1859 | Kors och stående sten av **kolmårdsmarmor**, 127 respektive 144 cm | SV | [KÄLLA] |
| 36 | Familjen Wiberg, bland andra Ulrika Gustava Wiberg, död 1859 | **Gjutjärnsstaket 320 × 320 cm** på kalkstenssockel med två gjutjärnskors med fjärilar (Bolinder) | V | [KÄLLA] |
| 44 | Okänd | Gravplats inom **smidesstaket 530 × 390 × 92 cm** på kalkstensblock | Mitten | [KÄLLA] |
| 50 | Tobaksfabrikören Eric Swarss, död 1823, och två hustrur | **Låg tumba 223 × 162 × 55 cm** inom smidesstaket som är 133 cm högt | Mitten | [KÄLLA] |
| 53 | **Apotekaren Johan Christoffer Wigander**, död 1856 | **Gjutjärnskors, 250 cm högt och 119 cm brett**, med akantus, timglas och lagerfeston. Det kallas ett "praktexemplar". | Ö, vid gången | [KÄLLA] |
| 54 | Tullförvaltaren Anders Ekman, död 1785, och Metta Helena Treter, död 1773 | **Tumba av grå kalksten 207 × 152 × 56 cm** | Ö | [KÄLLA] |
| 73 | **Coopv(erdi)kapten Lorentz Jäger** | **Gjutjärnskors 136 × 88 cm** med trepass, fjäril, puppa och nedåtvända facklor | Ö, vid gången | [KÄLLA] |
| 74 | J. P. Kinnecke, handlande och engelsk vicekonsul, död 1840 | **Fyrsidig pelare av röd kalksten, 200 cm**, med postament och svampliknande krön, totalt cirka 2,5 m | Ö | [KÄLLA] |
| 96 | **Mekanikus Jacob Balabrega**, död i Kalmar 1859, född i Amsterdam och ägare av hälsobrunnen Hälsan vid Helsingborg | **Urna av gulbrunt lergods (Höganäs), 106 cm hög och 52 cm i diameter**, på en kalkstensplatta 57 × 57 cm. Formgiven av F. E. Ring. Urnan är omvirad med eklöv. | N delen | [KÄLLA] |
| 139 | Apotekaren G. Korsseman | **Obelisk av röd kalksten, 135 cm**, på en trappformig sockel, totalt cirka 2,4 m | NÖ | [KÄLLA] |
| 2 | Skepparen Jacob Krul, död 1654, och Maria Sicherman, död 1649 | Röd kalkstenshäll 177 × 114 cm | SV | [KÄLLA] |
| 5 | Maria Bockes, död 1629, hustru till Peter Tessin i Stralsund (farbror till Nicodemus Tessin d.ä.) | Röd kalkstenshäll 180 × 125 cm | SV | [KÄLLA] |
| – | Stenhuggarmästaren Johan Pettersson Bergsten, 1715 | Stående sten med Kristi uppståndelse och stenhuggarverktyg; skadad | Ö delen enligt folderns pil | [KÄLLA] |

### Foton av gravvårdar (endast referenser)
- Svenska kyrkans folder har foton av Bergsten, Friborn och Högstedt, Jäger, Balabrega och Grip: https://www.svenskakyrkan.se/Sve/Bin%c3%a4rfiler/Filer/29C1E1C4-5D72-45D0-A883-76C5E4913A8A.pdf
- Balabregas grav på DigitaltMuseum: https://digitaltmuseum.se/021016510528
- Gravhällar och gravstenar på DigitaltMuseum:
  - https://digitaltmuseum.se/021016517685
  - https://digitaltmuseum.se/021017024616
  - https://digitaltmuseum.se/021017078692
  - https://digitaltmuseum.se/021017107310
  - https://digitaltmuseum.se/021017107312
- Sveriges kyrkor vol. 162 innehåller foton från 1971–73 av nästan varje vård (R. Näslund). Fig. 211–214 visar översiktsbilder från 1943 och 1973.
- Frigelius teckningar av gravhällar, med RAÄ-nr Kalmar 56:2 i beskrivningen, finns på Commons under "Kalmar storkyrka (Bykyrkan) – KMB – …". Ett exempel: https://commons.wikimedia.org/wiki/File:Kalmar_storkyrka_(Bykyrkan)_-_KMB_-_16001000535410.jpg
- Bloggbilder (inte granskade i detalj): https://mikaeledberg.se/gamla-kyrkogarden-i-kalmar/, http://jennysutflykter.blogspot.com/2016/08/gamla-kyrkogarden-i-kalmar.html, https://alvarsamt.wordpress.com/2013/07/09/gamla-kyrkogarden-kalmar/

---

## Källor

### RAÄ (Fornsök/KMR via Kulturarvsdata)
- **Kalmar 56:1, L1958:9244** – Begravningsplats (ödekyrkogård), fornlämning: http://kulturarvsdata.se/raa/lamning/3adf63b2-576b-4355-95f9-82af60e11a4a
  - Mått, mur och gravhus enligt citaten ovan.
- **Kalmar 56:2, L1958:9149** – Kyrka/kapell (kyrkplatsen, cirka 75 × 35 m, delundersökt av Rosman 1924), fornlämning: http://kulturarvsdata.se/raa/lamning/4e899e8e-a6a2-4436-98a1-72d3efbb8678
- **Kalmar 56:3, L1958:8710** – Minnesmärke (Kristoffermonumentet, med mått): http://kulturarvsdata.se/raa/lamning/f897de1d-cdc4-4a6b-b261-4ded755d68f9
- Kalmar 89:1, L1958:8098 – stadslager vid Söderportsskolan (provschakt 1975, cirka 2 m kulturlager). Det är bara omgivning.
- Kyrkogården ligger inom riksintresset för kulturmiljövården (Kalmar).

### Sveriges kyrkor (Riksantikvarieämbetet, fritt på DiVA)
- Martin Olsson, *Kalmar gamla stads kyrkor 1. Storkyrkan*, Småland III:2, vol. 158 (1974):
  - post: https://raa.diva-portal.org/smash/record.jsf?pid=diva2:1244147
  - PDF: https://raa.diva-portal.org/smash/get/diva2:1244147/FULLTEXT01.pdf
  - text: …/FULLTEXT02.txt
  - Innehåll: Rosmans grävningsplan (pl. I), rekonstruerad plan omkring 1610 (pl. II), fasader och sektioner, mått och byggnadshistoria.
- Martin Olsson och Rolf Näslund, *Kalmar gamla stads kyrkor 2. Kyrkogården, nu kallad Gamla kyrkogården* (samt Sancta Birgitta och Svartbrödraklostret), Småland III:3, vol. 162 (1976):
  - PDF: https://diva-portal.org/smash/get/diva2:1244151/FULLTEXT01.pdf
  - text: https://diva-portal.org/smash/get/diva2:1244151/FULLTEXT02.txt
  - Innehåll: kyrkogårdens historia, benhuset, gravvårdsplanen pl. XIII och beskrivning av alla gravvårdar med mått.
- I projektet finns redan `references/Kalmar-domkyrka-Sveriges-kyrkor-209.pdf` (vol. 209). Den berör Storkyrkan bara i förbigående.

### Kalmar läns museum och Svenska kyrkan
- Magdalena Jonsson, *Gamla kyrkogården*, fördjupad inventering, Kalmar läns museum 2006: https://kalmarlansmuseum.se/wp-content/uploads/2022/05/kalmargamlakyrkogard.pdf
  - Innehåll: historik, murar, ingångar, gångar, vegetation och gravvårdstyper. Kartbilagan ingår inte.
- Folder *Gamla kyrkogården* (Kalmar kyrkogårds- och fastighetsförvaltning, Kalmar läns museum, Länsstyrelsen). Den innehåller en karta med kyrkplatsen markerad: https://www.svenskakyrkan.se/Sve/Bin%c3%a4rfiler/Filer/29C1E1C4-5D72-45D0-A883-76C5E4913A8A.pdf
- Kalmar läns museum, *Möt medeltiden – Kyrkor i Kalmar stad*, med 75 × 38 m, kalksten på gråstensgrund, tegelgolv och 6 + 7 kapell: http://medeltiden.kalmarlansmuseum.se/mot-medeltiden-i-kalmar-lan/more-under-medeltiden/kyrkan/kyrkor-i-kalmar-stad/ (certifikatet är trasigt; hämtad med curl -k)
- DigitaltMuseum (Kalmar läns museums fotoarkiv): se URL:erna i respektive avsnitt.

### Övrigt
- Wikipedia (sv), *Gamla kyrkogården, Kalmar*: https://sv.wikipedia.org/wiki/Gamla_kyrkog%C3%A5rden,_Kalmar
  - Där står 75 × 38 m, rivning 1678, Kristoffer 1937 och Unionsstenen 1997.
- Wikipedia (sv), *Johan Stagnell*: https://sv.wikipedia.org/wiki/Johan_Stagnell (farbror till biskop Magnus Stagnelius)
- Kalmarkusten.se, *Kalmar Storkyrka/Bykyrkan*: https://kalmarkusten.se/platser/kalmar-storkyrka-bykyrkan/
- Kalmarkusten.se, *Gamla kyrkogården i Kalmar*: https://www.kalmarkusten.se/platser/gamla-kyrkogarden-i-kalmar/
- Arkeologi i Kalmar län (blogg), *Kalmar Storkyrka*, med 1610-planen och Dahlberg 1645: http://arkeologiikalmar.blogspot.com/2013/02/kalmar-storkyrka.html
- Wikimedia Commons, *Gamla kyrkogården i Kalmar Info.jpg* (informationstavlan, med texten "ett torn med två höga spiror"): https://commons.wikimedia.org/wiki/File:Gamla_kyrkog%C3%A5rden_i_Kalmar_Info.jpg
- OSM: `w149032114` (kyrkogården), `w500979084` (gravhuset), `w149032157`, `w500979083` och `w441934472` (gångar). Allt finns i `references/osm-slott98.json`.

### Kvarstående osäkerheter
1. **Kyrkans axel:** bäringen cirka 80° är härledd och kan vara fel med ±5°. Den kan skärpas genom att Rosmans plansch I georefereras mot muren och gravhuset i OSM eller mot en ortofoto.
2. **Tornets bredd** (14 m) och **antalet takfall på gravhusets tak** (sex eller åtta).
3. **Kristoffermonumentets årtal** (1929 eller 1937) och **Unionsstenens läge**.
4. **Var de kantställda kalkstenshällarna står** i dag. De syns inte i någon källa jag har sett och behöver kontrolleras på ett foto eller på plats.
5. **Gravhusets höjder** är bara uppskattade från foton.
