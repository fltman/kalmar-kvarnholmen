# Public edition note

Historical working notes below describe research files on the author’s machine. Reference photos and PDFs are intentionally not redistributed. The CC BY-SA altar photograph described below is **not included or used in this public edition**; its material is a neutral canvas pending a compatible image contribution. See THIRD_PARTY.md for distributed asset licenses.

# Referenser och modellens noggrannhet

Arbetsdatum: 18 september 2026. Område: Stortorget i Kalmar med närmaste kvarter. Detta är en modellerad proof of concept, inte en laserskanning eller fotogrammetrisk uppmätning.

## Google Street View — visuell granskning

- [Västra Sjögatan 9, Google Street View, april 2025](https://www.google.com/maps/@56.6636921,16.3653991,3a,90y,10h,95t/data=!3m4!1e1!3m2!1sR7rUnr3zUBEYEEGVcuUOxg!2e0). Torgets västra infart, domkyrkan, planteringskärl och beläggning.
- [Panorama på Stortorget, Alexander Gustafsson, maj 2017](https://www.google.com/maps/@56.6641045,16.365755,3a,90y,147.42h,97t/data=!3m4!1e1!3m2!1sCIHM0ogKEICAgIDEh9iP6QE!2e10). Roterad visuellt för kyrkans huvudfasad, rådhuset, stadshotellet och husraden söder om torget. Panoramats riktning är inte en tillförlitlig uppmätningsreferens.

Street View har granskats visuellt. Modellens texturer är lokalt skapade och innehåller inga Google-bilder. Inga panorama-, djup- eller 3D-data har extraherats från Google.

## Planläge

[OpenStreetMap](https://www.openstreetmap.org/#map=19/56.66412/16.36560), kartutdrag hämtat via offentlig API. © OpenStreetMap contributors, [ODbL](https://www.openstreetmap.org/copyright).

Originalutdrag: `references/osm-map.osm`. Bearbetade konturer: `source/site.json`. Blender använder meter, Unreal centimeter. Geografiskt origo: WGS84 56.66412° N, 16.36560° E. Lokal X-axel är 28,2° moturs från öster; Y-axeln ligger vinkelrätt mot denna. Det är ett lokalt plan för detta lilla område, inte ett fullständigt nationellt koordinatsystem.

Domkyrka: OSM way 38319501. Rådhus: way 92412845. Låga vita grannhuset: way 92412866. Gula huset, andra huset höger om rådhuset sett från torget: way 92412857. Stadshotellet: relation 1343844, ytterkontur way 91846976. Hotellets innergård är förenklad i denna version.

## Kompletterande referenser

- [Kalmar kommun: Rådhuset](https://kalmar.se/uppleva-och-gora/kulturupplevelser-och-fritidsaktiviteter/kulturhistoria-kulturarv/kalmar-kommuns-serie-om-historiska-kalmar/radhuset.html).
- [eCKsplorer: Kalmar](https://www.ecksplorer.com/blog/kalmar-the-town-you-should-know-more-about-in-sweden). Flygfoto uppifrån användes för att korrigera domkyrkans korsformade tak. Den lokala referensbilden är endast arbetsreferens, inte en textur eller egenproducerad bild.
- [Wikimedia Commons: Stortorget, Kalmar](https://commons.wikimedia.org/wiki/Category:Stortorget,_Kalmar). Kompletterande byggnadsidentifiering.

## Tolkningar och kvarvarande arbete

Byggnadskonturerna följer OSM. Höjder, takfall, fönsterdimensioner och ornament är visuella uppskattningar. Fasader på kringliggande kvarter är generiska; de tre huvudbyggnaderna och den södra husraden har särskild detaljering. Torgets gångstråk och möblering är en schematisk tolkning. Terrängen är plan. Domkyrkan har en förenklad interiör; övriga byggnaders interiörer saknas. Bilar, människor och tillfälliga uteserveringar/skyltar är inte inventerade.

Denna version är avsedd att prova skala, platskänsla, arbetsflöde Blender → Unreal och förflyttning. För en nära fotorealistisk kopia behövs fler fasadreferenser, verifierade höjder, detaljerade material och en separat kvalitetskontroll per byggnad.

Förstapersonskontroller och karaktärsresurser kommer från den lokalt installerade officiella Epic Games First Person-mallen för Unreal Engine 5.8 och omfattas av dess villkor.

## Domkyrkans interiör och ritningar

- [Svenska kyrkan, Historik och arkitektur](https://www.svenskakyrkan.se/kalmar/historik-och-arkitektur/history-and-architecture/geschichte-und-architektur): korsvalv, joniska pilastrar, dokumenterad fri höjd 23 m, läktare, orgel, ljuskronor och altarparti.
- [Interiör mot öster, 2015, Wikimedia Commons](https://commons.wikimedia.org/wiki/File:Kalmar_domkyrka,_interiör_med_altaret_mot_öster,_2015a.jpg). Visuell arbetsreferens i `references/interior-east.jpg`.
- [Interiör mot väster, Wikimedia Commons](https://commons.wikimedia.org/wiki/File:Kalmar_domkyrka_Interiör_mot_väster_001.jpg). Visuell arbetsreferens i `references/interior-west.jpg`. Bilderna har inte använts som texturer; upphov och licens finns på respektive källsida.
- [Richard Edlund, Kalmar läns museum: Bänkinredningen i Kalmar domkyrka 1682–2007](https://kalmarlansmuseum.se/wp-content/uploads/2022/05/kalmardomkyrkabankinredning.pdf). Lokal PDF: `references/domkyrka-bankinredning-2007.pdf`. PDF-sida 22 visar planritning signerad J. Fred. Olson 1912, beskriven på nästa sida. PDF-sida 52, bilaga 3, visar relationsritning av bänkdörrar och fronter 2007. Båda är visuellt granskade. Historisk plan, inte en verifierad nutida relationsritning av hela byggnaden.
- [Barup och Edström, restaureringsprojektet, STEN december 2011](https://media.sten.se/2011/12/STEN-4_2011_web1.pdf). Stöd för det förändrade koret och återöppnade fönster.

Interiörens korsgång, sidobänkar, västläktare och östliga altarparti har jämförts med planritningen och senare foton. Måttsättningen är fortfarande en uppskattning inpassad i OSM-konturen; 23 meters centrala takhöjd följer kyrkans beskrivning. Skulpturer, orgelornament, epitafier och altaruppsats är förenklade. Altarmålningen återges med ett licensierat fotografi, se attribution nedan. Kyrkans södra portal har öppnats för den spelbara modellen. Mindre rum, läktartrappor och gravkrypta ingår inte. Skulpturerna är fortfarande stiliserade tolkningar, och vapensköldar/epitafier är inte en fullständig inventering.

En sökträff på kommunens takplan i ärende SBK-2026-253 hittades, men filen gav HTTP 404. Den har därför inte använts som verifierat ritningsunderlag.


## Detaljpass: domkyrkan

- **Ingrid Rosell och Robert Bennett, Kalmar domkyrka, Sveriges kyrkor 209 (1989)**, Riksantikvarieämbetet. [Bibliografisk post och öppen fulltext](https://raa.diva-portal.org/smash/record.jsf?pid=diva2%3A1244199), [direkt PDF](https://www.diva-portal.org/smash/get/diva2:1244199/FULLTEXT01.pdf). Komplett lokal PDF: `references/Kalmar-domkyrka-Sveriges-kyrkor-209.pdf`, 274 PDF-sidor, 159 664 895 byte. Planschförteckning på PDF-sida 260. Planscher 1–10 finns på PDF-sidor 261–270: huvudplan, sydfasad, östfasad, längdsektion, tvärsektion, gavelsektioner, takplan, golv/bänkplan, ytterligare takplan samt klocktorn/orgelläktare. Ritningarna är från 1910–1912 eller odaterade. Sydfasad och längdsektion är visuellt granskade och har styrt blindnischer, tornhuvar, voluter och rumshöjd. De ersätter inte en nutida uppmätning.
- [Kalmar domkyrka, juli 2015c](https://commons.wikimedia.org/wiki/File:Kalmar_domkyrka,_juli_2015c.jpg), lokal visuell referens `cathedral-front-detail.jpg`: puts, stenfogar, fasadprofiler.
- [Predikstolen, Kalmar Domkyrka 035.JPG](https://commons.wikimedia.org/wiki/File:Kalmar_Domkyrka_035.JPG), `pulpit-detail.jpg`: paneler, bladverk, baldakin och underbyggnad.
- [Dopfunt 0099.JPG](https://commons.wikimedia.org/wiki/File:Kalmar_domkyrka_Dopfunt_0099.JPG), `font-detail.jpg`: blå genombruten fot och klar skål; modellen är en förenklad geometrisk tolkning, inte en avbildning av varje utskärning.
- [Koret 010.jpg](https://commons.wikimedia.org/wiki/File:Kalmar_Domkyrka_Koret_010.jpg), `choir-detail.jpg`: kororgel, räcken, stolar, ljusstakar och dopfunt.

### Altartavlans bildtextur — attribution

**Bernt Fransson, Lindås**, *Kalmar Domkyrka Altartavlan 041.JPG*, 24 mars 2012. [Original och licens](https://commons.wikimedia.org/wiki/File:Kalmar_Domkyrka_Altartavlan_041.JPG), **[Creative Commons Erkännande-DelaLika 4.0](https://creativecommons.org/licenses/by-sa/4.0/)**. Fotografiet visar altartavlan med målningen av David von Krafft.

Originalfilen är bevarad oförändrad i `references/altar-detail.jpg` och kopierad byte för byte till `exports/textures/T_AltarpiecePhoto.jpg`. Modellens UV-koordinater väljer ut och anpassar målningens område till en välvd duk. Det är en beskärning/perspektivförenkling i visningen. Bilden och denna bildbearbetning omfattas av CC BY-SA 4.0. Fotografen har inte godkänt eller medverkat i detta projekt. Behåll attribution och licens när bildtexturen återanvänds.

### Ytmaterial

13 proceduriellt skapade materialuppsättningar med 2 048 × 2 048 bildpunkter: basfärg, tangentnormal och roughness. Kartorna representerar cirka 4 meter per UV-repetition. Puts och trä har fin relief; stenfogar och plåtfalsar har tydligare relief. Förgyllda och marmorerade ytor har små ojämnheter. Normalerna genereras i OpenGL-konvention och grön kanal vänds vid Unreal-import. Kyrkans geometri har dessutom mjuka ytnormaler på valv/svarvade delar och små kantfasningar.

Projektet är fortfarande en tolkad modell. Höjder och placeringar utöver verifierad central takhöjd är inte inmätta. Altarfigurer, bladverk, orgeldekor, begravningsvapen och mindre inventarier är förenklade eller saknas; inga påhittade inskriptioner används. Alla historiska detaljer är alltså inte färdiginventerade.

### Detaljpass 2 — formgranskning

Närbilderna `altar-detail.jpg` och `pulpit-detail.jpg` samt västbilden `interior-west.jpg` har återanvänts för att korrigera altarram, brutet krön, gloria, skulpturernas silhuetter och orgelläktarens välvda front. Draperier, ansiktsdrag, händer, fjädrar och akantusblad är proceduriellt modellerade tolkningar. Figurernas exakta poser och ornamentens fördelning är inte inmätta. Den marmorerade ytans nya oregelbundna ådror är fortfarande ett eget procedurmaterial. Inga nya fotografier används som texturer i detta pass.

## Kvalitetspass 3: renderings- och ytmaterial

- [Poly Haven: White Plaster 02](https://polyhaven.com/a/white_plaster_02), Rob Tuytel. Diffusfärg, tangentnormal och roughness i 2K, hämtade via officiellt API. Kalkputsen har neutral färgsättning och normalstyrkan är dämpad för kyrkorummets släta puts.
- [Poly Haven: Marble 01](https://polyhaven.com/a/marble_01), Rob Tuytel. Ett område inne i en platta används som strukturunderlag för marmorerat måleri och kalkstensgolv. Fogarna i originalet är bortvalda; färg, normalstyrka och roughness är bearbetade. Materialet är inte en skanning av kyrkans egen sten.
- Dessa två material är **CC0**, se [Poly Havens licens](https://polyhaven.com/license). Originalkartor, författare och API-metadata bevaras i `references/polyhaven/`. `stone_floor` hämtades för jämförelse men används inte, eftersom fogmönstret och slitaget inte stämmer med interiören.
- [Epic: macOS Development Requirements](https://dev.epicgames.com/documentation/en-us/unreal-engine/macos-development-requirements-for-unreal-engine), kontrollerat 18 september 2026. Renderingspasset använder programvarubaserad Lumen, Nanite och virtuella skuggkartor på Apple Silicon. Ingen experimentell hårdvaruraytracing krävs.

Figurerna har omarbetats med sammanhängande ansiktsytor, ögonhålor, ändrad kroppssilhuett och varierande veck. Predikstolens paneler har ramar och bladverk, och dess krön har figur och fana efter bildreferensen. Även denna version innehåller tolkade, proceduriella skulpturer. Den är ännu inte färdig på AAA-nivå; närgranskning mot skannade original, full inventering och en paketerad prestandamätning återstår.

Altarfigurernas attribut har kompletterats efter Svenska kyrkans beskrivning: **Tron** bär kors och kalk, **Nåden** ett ymnighetshorn, pingstflamma och sköld. Ymnighetshorn och flamma saknades i den tidigare förenklingen. [Primärkälla: Historik och arkitektur](https://www.svenskakyrkan.se/kalmar/historik-och-arkitektur/history-and-architecture/geschichte-und-architektur).


## Detaljpass 5: bänksnickeri och joniska kapitäl

`references/interior-east.jpg` och `references/pulpit-detail.jpg` har granskats på nytt som form- och materialreferenser. Bänkdörrarnas indragna speglar, hörnförskjutna ramprofiler, mörka målade ornament, tunna förgyllda lister och rundade överliggare har tolkats i ny geometri. Beslag och dekor är uppskattade från foton, inte uppmätta eller exakta kopior. Pilastrarnas joniska kapitäl har fått slutna volymer för voluter, spiralrelief och äggstav.

De tre snickerimaterialen är egenproducerade 2K-kartor med 4 meters repetition: grå färg, spegelfält och listverk. Reliefens RMS-höjd är cirka 0,0095 mm; fin penselstruktur och glansvariation ersätter den tidigare tydliga träådringen. De två extra materialuppsättningarna ger sammanlagt 15 kyrkouppsättningar. Inga ytterligare fotografier används som texturer.

## Exteriörpass 7 — samtida sydfasad

- [Kalmar cathedral Kalmar Sweden 002.JPG, Wikimedia Commons](https://commons.wikimedia.org/wiki/File:Kalmar_cathedral_Kalmar_Sweden_002.JPG), foto 8 juli 2006, lokal arbetsreferens `references/cathedral-south-2006.jpg`. Fotot visar glasade övre sidofält och ett runt fönster i det högra tornet. Den historiska elevationens blindnischer har därför inte återanvänts på den aktuella sydfasaden. Filens fotograf och licens anges på Commons-sidan; ingen del av fotot används som bildtextur.
- [Swedish Nomad: Att göra i Kalmar](https://www.swedishnomad.com/sv/att-gora-i-kalmar/), fasadfoto från sidans bildkatalog 2021/09, lokal visuell referens `references/cathedral-south-2021.jpeg`. Bilden styr stenprofilernas uppdelning, portalens plana taklist, mörka krön och gavlarnas urnor. Exakt fotograferingsdatum är inte verifierat. Endast arbetsreferens; inte en textur eller en bild skapad för projektet.
- [Svenska kyrkan: Historik och arkitektur](https://www.svenskakyrkan.se/kalmar/historik-och-arkitektur/history-and-architecture/geschichte-und-architektur) identifierar Karl XI:s monogram på sydportalen. Modellens förgyllda spegelvända C/XI-form och krona är en egen förenklad geometrisk tolkning. Inskriptionsfältet under gesimsen lämnas utan påhittad text eftersom den inte går att läsa säkert i de valda fotografierna.

Fotografiernas perspektiv och ritningens historiska skick ger fortfarande osäkerhet i dimensioner och ornamentens exakta form. Materialen `ChurchCopperFine`, `ChurchRoofFine` och `ChurchPierStone` är egna procedurytor med separata normalkartor och roughness; de innehåller inga fotografiska pixlar. Plåtfalsar följer modellerad takgeometri i stället för ett rutnät i materialet. Ingen slutsats om dagens norra fasad har dragits från sydfotografierna.


## Detaljpass 8 — husen runt Stortorget

- [Kalmar kommun: Rådhuset](https://kalmar.se/bygga-bo-och-miljo/forvaltning-av-byggnader/radhuset.html), publicerad 17 maj 2023 och uppdaterad 9 oktober 2025. Kommunens fasad- och detaljbilder (`references/radhus-front.jpg`, `radhus-detail.jpg`) visar elva fönsteraxlar, blågrå snickerier, grund rustik, smidda ankarslut och tre stentavlor. Dessa styr den nya modellens fönsterindelning och färg. Tavlornas bildinnehåll är fortsatt förenklat; ingen läsbar inskrift har hittats på.
- [Kalmar kommun: Nelsonska huset](https://kalmar.se/bygga-bo-och-miljo/forvaltning-av-byggnader/nelsonska-huset.html), publicerad 24 mars 2023 och uppdaterad 9 oktober 2025. `references/nelson-front.jpg` och `nelson-window.jpg` visar panel, vita omfattningar och blågrå fönster. Kommunen beskriver fasaden som putsimiterande träpanel från omkring 1974; modellen får därför en panelnormal i stället för grov puts.
- [Wikimedia Commons: Kalmar rådhus och Calmar Stadshotell vid Stortorget, 2015](https://commons.wikimedia.org/wiki/File:Kalmar_r%C3%A5dhus_och_Calmar_Stadshotell_vid_Stortorget,_2015.jpg), lokal fil `references/square-south-2015.jpg`. Översikt av södra husraden, den låga gamla brandstationen samt hotellets relation till rådhuset.
- [Wikimedia Commons: Kalmar.Stortorget.Stadshotellet 027.JPG](https://commons.wikimedia.org/wiki/File:Kalmar.Stortorget.Stadshotellet_027.JPG), lokal fil `references/hotel-front.jpg`. Hotellets slutna formgavlar, norra tornplacering, koppartak, röda falsade takytor, burspråk, balkonger och markiser är visuella referenser. Fotografer och licensuppgifter finns på respektive Commons-filsida. Endast visuella arbetsreferenser; fotografierna används inte som texturer eller som nya projektbilder.

Kartkonturerna är fortsatt OpenStreetMap-underlaget i `source/site.json`. Byggnadshöjder, bakgårdstak och flera av de västra fasadernas enskilda detaljer är fortfarande uppskattningar. De fem västra/nordöstra husens fasadprofiler är ett material- och detaljpass, inte en verifierad inventering av varje fasad. Hotellets dekor, tornprofil och rådhusets emblem är förenklade tolkningar. Ingen interiör i dessa hus har byggts i detta pass.

De femton `Town*`-ytorna är egna proceduriella 2K-ytor med färg, roughness och OpenGL-normaler: kalkputs/sten, målade snickerier, panel, tegel, plåt och glas. Takens ståndfalsar är geometri, tegelpannornas grunda relief ligger i normalkartan. Direkta hämtningsadresser finns i `references/town-pass8-urls.json`. De två ytterligare Commons-bilderna kunde hämtas efter en tillfällig 429-begränsning: `square-west-2024.jpg` ger en översikt av den östra husraden sedd västerifrån (arbetsnamnet anger kamerans sida), och `radmannen-2024.jpg` visar Rådmannen 2:s panel, fem fönsteraxlar, fronton och bruna snickerier. Dessa användes i korrigeringspasset. Källa: [Rådmannen 2 sept 2024](https://commons.wikimedia.org/wiki/File:R%C3%A5dmannen_2_sept_2024.jpg) och [Stortorget Kalmar sept 2024](https://commons.wikimedia.org/wiki/File:Stortorget_Kalmar_sept_2024.jpg).


## Detaljpass 9 — hotellets torn, portal och portsnickerier

`references/hotel-front.jpg` har granskats igen för hotellets profilerade kopparhuv, lanterninfönster, höga undre fönsterbågar, mindre överljus och stenportalen. Den tidigare generiska takpyramiden har ersatts av en svept huv med avfasade hörn, modellerade falsar och övre lanternin. Portalen får fanljus, profilerad stenbåge, voluter, bladrelief, dörrar och beslag. Ornamenten och lyktorna är fortfarande tolkningar; de är inte inmätta kopior av varje detalj. Rådmannens, Nelsonska husets och rådhusets portar bygger vidare på referenserna i pass 8.

[Hotellets egen presentation](https://ligula.se/en/profilhotels/profilhotels-calmar-stadshotell/) har kontrollerats som kompletterande primärkälla. Modellens namntext CALMAR STADSHOTELL återger byggnadsnamnet; typsnittet är en approximation. Inga fotografiska texturer har lagts till. Det nya materialet `M_Town_Copper` återanvänder projektets egen normal- och roughnessuppsättning `ChurchCopperFine` utan att ändra kyrkans material.


## Utvidgning 10 — Storgatan och Larmtorget

- OpenStreetMap contributors: byggnads- och gatukonturer, hämtade 19 september 2026 via [OSM API](https://api.openstreetmap.org/api/0.6/map?bbox=16.3583,56.6616,16.3655,56.6651). ODbL; lokal råfil `references/osm-storgatan-larmtorget.osm`. Projektets tidigare WGS84-origin och rotation används oförändrade. Multipolygonernas innergårdar bevaras.
- Google Maps, Joakim Nilsson, juni 2020: gatupanorama vid [Storgatans östra del](https://www.google.com/maps/@56.6637895,16.3645886,3a,90y,240h,90t/data=!3m4!1e1!3m2!1sCIHM0ogKEICAgIDy3beo4wE!2e10) och [vid det västra kvarteret](https://www.google.com/maps/@56.6632644,16.3627861,3a,90y,240h,90t/data=!3m4!1e1!3m2!1sCIHM0ogKEICAgIDy3de_1AE!2e10), granskat i båda riktningar. Underlag för skiftande höjder, butiksvåningar, taklinjer, markbeläggning, beskurna träd och möbler. Panoramabilderna är visuella referenser och används inte som texturer.
- Sinikka Halme, maj 2022, [Larmtorget mot Storgatan](https://commons.wikimedia.org/wiki/File:Larmtorget_Storgatan_Kalmar_Sweden_May_2022.jpg). Lokal `references/larmtorget-east-2022.jpg`: rosa nordvästra hörnhuset och gult södra hörnhus, tak, butikspartier och torgets gatukorsning.
- [Vasabrunnen och Kalmar teater, maj 2022](https://commons.wikimedia.org/wiki/File:Larmtorget_in_Kalmar_Sweden_with_Vasabrunnen_and_Kalmar_Theatre_May_2022.jpg), lokal `references/larmtorget-theatre-2022.jpg`: teaterns vita centralfasad, bågfönster, tre entréaxlar, parapet och lägre sidoflyglar. Vasabrunnen modelleras tills vidare som en förenklad volymstudie i sin kartlagda position.
- [Frimurarehuset vid Larmtorget, maj 2022](https://commons.wikimedia.org/wiki/File:Frimurarehuset_Larmtorget_Kalmar_Sweden_May_2022_01.jpg), lokal `references/frimurare-2022.jpg`: gul fasad, låg mellanvåning med parade fönster, höga bågfönster ovanför, hörntorn och takfris. Den första modellen korrigerades efter att denna bild hämtats. Exakt dekor och mått är inte verifierade.

Fotografer och bildlicenser anges på Commons respektive filsidor. Hämtningsadresser och panoramahänvisningar finns i `references/storgatan-reference-urls.json`. Inga bilder har bakats in i fasadmaterial. De nya beläggningstexturerna och lövgeometrin är egen procedurgenerering. Företagsnamn och tillfälliga uteserveringar från fotografierna ska inte läsas som en inventering av dagens verksamheter.


## Larmtorget facade review — 2026-09-19 (pass 11)

- North frontage: Sinikka Halme, May 2022, [Commons](https://commons.wikimedia.org/wiki/File:Kalmar_Larmtorget_Blockmakaren_Kalmarhemshuset_May_2022_01.jpg). Local `references/larmtorget-north-2022.jpg`. Distinct functionalist western section, three-storey white arched section, and lower eastern white frontage.
- Ludvigshuset: [Ross Murteknik renovation reference](https://www.murteknik.com/projekt/ludvigshuset-larmtorget/), local `references/ludvigshuset-renovation.jpg`; white Jugend facade, copper roof, curved gable and corner roof hoods. Supplemental street detail: Sinikka Halme, [Commons](https://commons.wikimedia.org/wiki/File:Frimurarehuset_Västra_Vallgatan_Larmtorget_Västerport_Kalmar_Sweden_May_2022_01.jpg), local `references/larmtorget-south-2022.jpg`.
- Theatre and Frimurarhuset: previously downloaded 2022 Commons photographs, `larmtorget-theatre-2022.jpg` and `frimurare-2022.jpg`. Rechecked window groups, parapets, cornices, upper tracery and mezzanine paired windows.
- [Kalmar läns museum: Ludvigshuset](https://kvarnholmen.kalmarlansmuseum.se/ludvigshuset) identifies the southern block as Jugend, designed by Gustaf Wickman, built 1903–1905. Text accessible through search; direct museum image endpoint failed certificate verification and was not used.

These photographs are visual references, not facade texture sources. Dimensions, building subdivision within combined OSM footprint 91846938, decorative profiles and partly obscured surfaces remain interpretations. Existing original procedural PBR textures retained. No claim of survey accuracy or completed AAA quality.


## Kvarnholmen street network and building massing — 2026-09-19 (pass 12)

- [OpenStreetMap district boundary, relation 6422397](https://www.openstreetmap.org/relation/6422397), `references/osm-kvarnholmen-boundary.osm`. The administrative district sets this pass's extent, including the station and the immediate southern waterfront, excluding Tjärhovet farther south.
- OpenStreetMap API map extract, bbox `16.3565,56.6588,16.3775,56.6690`, downloaded 2026-09-19, `references/osm-kvarnholmen-full.osm`. Street centre-lines, building outlines, inner courtyards, coastline and available tags. © OpenStreetMap contributors, ODbL.
- [Kalmar kommun, parking/street map](https://kalmar.se/download/18.7ee82f39180b05dcf971e72/1764683190797/ParkeringKvarnholmen.pdf): street-name cross-check from indexed municipal map text. No parking regulations are modelled or asserted.

New houses are explicitly massing, not photo-matched facade reconstructions. Mapped heights/storeys are used where available; otherwise 1–3 storeys are estimated by footprint size/type. Generic roof heightfields are constrained to each footprint and its courtyard rings. Widths and sidewalk widths are estimates unless tagged. The terrain is level; no elevation survey or detailed bridge engineering is included. Existing detailed Stortorget, Storgatan and Larmtorget buildings are preserved. Asphalt and water PBR maps are original procedural work, with physical height-derived normals; no map imagery is used as a texture.

## Södra Långgatan facade pass 13 — 2026-09-19/20

- [Google Street View, 57 Södra Långgatan, April 2025](https://www.google.com/maps/@56.6641998,16.3684139,3a,90y,150h,90t/data=!3m4!1e1!3m2!1swwIlR2svk8lTZ1l5PvuLIQ!2e0). Inspected interactively in Chrome: white three-storey frontage with rectangular window groups and dormers; narrow red timber gable house, yellow gate, low half-timbered neighbour. Panorama headings rotated through the street frontage.
- [Google Maps contributor panorama, Alex Karpsson, April 2021](https://www.google.com/maps/@56.6637154,16.3669605,3a,90y,270h,90t/data=!3m4!1e1!3m2!1sCIHM0ogKEICAgIDqjcPufQ!2e10). Inspected interactively: corner hotel's pale upper plaster, dark window frames and panels, continuous canopy and stone ground-storey supports. This location opened a contributed panorama, not Google camera-car imagery.
- [-wuppertaler, SWE Kalmar, Södra Långgatan 2022](https://commons.wikimedia.org/wiki/File:SWE_Kalmar,_Södra_Långgatan_2022.jpg), photographed 7 June 2022, CC BY-SA 4.0. Local `references/sodra-langgatan-2022.jpg`. Northern corner: plaster pilasters, western gable, broad ground windows, intermediate ochre timber and eastern pale green frontage.

Observations are recorded in `references/sodra-facades-reference-notes.json`. Photographs informed modelling only; no Google imagery is used as a mesh texture. The five new PBR materials are original procedural textures. Facade divisions, measurements and obscured sides remain interpretations. Hotel signs and present-day occupants are not asserted. Rear upper-storey structures, precise historical joinery, planted walls, roof skylights and several decorative profiles remain simplified or absent.

## Landmärken och ringmur — pass 14

Se [utförliga referensanteckningar](references/landmarks14-notes.md) för bilder, granskade Street View-panorama-id:n och tolkningar. Primärunderlag för befästningarna: Kalmar läns museum, *Kvarnholmens befästningsverk — Bevarande- och utvecklingsplan*,2020, lokalt `references/befastningsverken-2020.pdf`. Brandstationen: samma museum, *Brandstationen i Kalmar — Bebyggelsehistorisk utredning*,2012, lokalt `references/brandstationen-kulturhistorik.pdf`; den nuvarande ljusa färgen och ombyggda västflygeln kontrollerades i Street View från juni2025.

## Pass 15: ytmaterial och återstående fasader

[Materialkällor och begränsningar](references/polish15-notes.md) beskriver de tio CC0-materialen från Poly Haven, färgvarianterna och fasadernas proveniens. Originalkartor, källmetadata och kontrollsummor finns i `references/polyhaven15/`. De 267 nya fasaderna är tolkningar utifrån kartlagda grundformer och våningshöjder, inte individuellt verifierade Street View-rekonstruktioner.


Pass 16: [Granskade Storgatan-referenser och husvisa observationer](references/street16-notes.md).


Pass 17: [Hela husbeståndet, sju nya bildstudier och tydlig åtskillnad mellan observerade och uppskattade fasader](references/district17-notes.md). Referensfotografierna används för formstudier, inte som projicerade texturer. Inga nya Street View-panorama granskades i detta pass.
