## Pass 142 — Fastlandet: gårdshusen

De sista 59 konturerna från pass 98 på fastlandet, de som ligger 25 m eller längre från närmaste gata och som inget gatupass har tagit: förråd, garage och garagelängor på bakgårdarna, uthus och gårdsflyglar bakom villorna och stadskvarteren, två radhuslängor vid gångvägar, villorna på den privata vägen norr om Kalmarsundsparken, husen vid Södra kyrkogården, den gula före detta kasernen vid Gamla torget, Café Flädern, gårdshusen bakom Unionsgatan och Smålandsgatan och kiosken och toaletten i Kalmarsundsparken. De flesta syns inte från någon gata. Takform, nockriktning och takfärg är lästa från satellitbilder rakt ovanifrån, och fyra byggnader är dessutom kontrollerade i Street View. Alla 59 har tagits ur pass 98:s klumpmesher och ersatts av byggnader med sadel-, valm-, pulpet- eller platta tak av rött, brunt eller mörkt tegel eller grå eller mörk plåt. Väggarna har puts eller stående panel med vita knutbrädor. Byggnaderna har takfotsbrädor, fönster per våning, dörr mot närmaste gata (annars på den längsta väggen), garageportar på garagen, takkupor och skorstenar. Varje byggnad är en egen mesh, `SM_Slott142_<osm-id>`:
- vid Stora Dammgatan: det långa panelförrådet vid rosenträdgårdens mur (1453534570), ett litet förråd (93238186), tre sektioner av 1940-talslängorna vid gångvägen (93238220, 93238284, 93238239) och det gula panelhuset med takkupor i trädgården (93238221);
- bakom Västerlånggatan: huset med valmat brunt tegeltak och garaget bredvid (93238283, 93238290) och villan på Västerlånggatan 28 med korsvalmat tegeltak och runt burspråk (93329957);
- i kvarteren mellan Ståthållaregatan, Johan III:s gata och Sankta Britas gata: tre hus i radhuslängan 1E–1F (93291962, 93291967, 93292008), det L-formade huset med valmat tak (93329938), villan nr 6 (93329953), Wollinska Stiftelsens hus (93329965), uthuset med platt grått tak (93329980), det lilla röda uthuset (93329987), huset med takkupor (93330000) och det lilla huset nr 1 med grått valmtak (93330001);
- vid Sankt Eriks gata de tre garagen på bakgården (93358502, 93358543, 93358547) och längre söderut det lilla huset på kvarterets baksida (93329937);
- vid Folkungagatan, Drottning Margaretas väg, Ringgatan, Torsgatan och Baldersvägen: det L-formade garaget, som skärs av modellens kant (93361181), villan nr 2 med korsvalmat tak (93487550), huset med tillbyggnader (93487564), garaget bakom Ringgatan (93505688) och garagelängan (93505695);
- norr om Kalmarsundsparken: den vita villan med rött tegeltak och mittgavel på Kalmarsundsparken 3 (93460175), villan med vit gavel (93460156), villorna nr 7, 9 och 15A och ytterligare en (93460187, 93460204, 93460194, 93460172), två garage (93460203, 93460209) och garaget vid Gustaf Vasagatan (93460214);
- i Kalmarsundsparken glasskiosken (874145313) och den offentliga toaletten (874145314);
- vid Gamla torget den gula kasernbyggnaden i tre våningar med den långa flygeln med mörkt tak och takkupor och den södra delen med lågt valmtak (91970346);
- vid Kungsgatan och Västerlånggatan: förråds- och garagelängan bakom Kungsgatan 5 (93292689), två små förråd (93292706, 93292702), gårdsflygeln bakom Västerlånggatan 13A (93306352) och bakhuset 20C (93326718);
- vid Södra kyrkogården huset nr 3 (93293012), den långa ekonomibyggnaden (93293025) och ett förråd under träden (93293041);
- på gårdarna bakom Frejagatan och Vegagatan garage- och förrådslängan (93325645) och gårdshuset vars gamla tak från pass 98 stack in över grannen från pass 139 (93325656);
- bakom Molinsgatan ett bakhus (93306356);
- mellan Järnvägsgatan, Bremergatan och Västerlånggatan: Café Fläderns gula panelhus med rött tegeltak (93333638) och dess annex med platt tak (93333623), det gula tvåvåningshuset (93333658), huset 1B med mörkt tak (93333627) och garaget med mörkt tak (93333660);
- på gården bakom Unionsgatan och Smålandsgatan de tre gårdshusen med valmade bruna tegeltak, 4C, 4D och huset med korsvalmat tak (93453481, 93453516, 93453490).

Ingen byggnad är riven. Tre konturer skärs av pass 98:s modellkant (x −1650 eller y 320) och är byggda på den avskurna konturen med släta väggar mot kanten. Radhussektionerna har samma höjd som grannarna som tidigare pass har byggt, så att taken går ihop.

Pass 98:s klumpmesher `SM_Slott98_Buildings_W`, `SM_Slott98_Buildings_M` och `SM_Slott98_Buildings_E` byggs om med `slott98_chunks115` från pass 115. Nu finns det inget hus kvar i dem. En helt tom mesh går inte att exportera, och en borttagen mesh skulle bryta de tidigare passens namnlistor. Därför får varje klumpmesh en liten dold markör: en kvadrat på 0,4 × 0,4 m, 0,10 m under marken på öppen mark. Den syns inte och är inget hus. Alla hus från pass 98 på fastlandet är därmed detaljerade.

Nästan allt är uppskattat: höjderna kommer från våningar, takens storlek och grannarna. Bara kasernens takfot (12,4 m) är inmätt, från en kamera som är bestämd mot OSM-konturen vid Gamla torget. Väggfärgerna på byggnader som inte syns från gatan är rimliga val, inte avläsningar.

Passet är gjort av Claude och finns bara i arbetskopian.

Geometrikontrollerna i Blender är godkända och pass 28–141 är oförändrade utom de avsedda ändringarna: fastlandets samlade husdelar från pass 98 (W, M och E) är återskapade utan husen och innehåller nu bara var sin dold markör. Import och kontroller i Unreal görs när modellerna i området är klara.

Källor och mätningar finns i `references/block142-notes.md`.
