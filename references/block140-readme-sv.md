## Pass 140 — Fastlandet: de sista gatuhusen

De gatuhus på fastlandet som inget gatupass har tagit: villa- och stadshuskvarteren längst i väster vid Ringgatan, Torsgatan, Baldersvägen, Lillegårdsgatan och Margaretaplan, hyreshuset vid Stensövägen i modellens norra kant och tre fristående hus strax bortom 25 m från gatan (vid Södra vägen, Lilla Dammgatan och Söderportsgatan). De 18 enkla volymerna från pass 98 som ligger inom 25 m från en namngiven gata och inte hör till något tidigare pass, och de tre fristående husen, är tagna ur pass 98:s klumpmesh. Alla 21 är ersatta av hus med verklig form: våningar, sadel-, valm- och mansardtak av rött eller mörkt tegel eller mörk plåt, platta tak, puts i husets färg, stående panel med vita knutbrädor, rött och gult tegel, takfotsbrädor och fönsterfoder, fönster per våning, källarfönster, dörr mot gatan, takkupor och skorstenar. Varje hus är en egen mesh, `SM_Slott140_<osm-id>`:
- på Ringgatans nordvästra sida raden med tre putsade hus i två våningar över källare: det vita med vindsvåning och balkong på sydvästgaveln (93566356), det ljusgula (93566367) och det ockragula med två röda takkupor (93566385);
- på Ringgatans sydöstra sida tegelvillan med balkong i västgaveln (93505709), det höga ljusgula huset med vita hörnlisener och gaveln mot gatan (93505730) och den ljusgula villan med valmat tegeltak bakom buskarna (93505770);
- vid Lillegårdsgatan den vita villan med lågt valmtak, vars östra del ligger innanför modellens kant (93505686), och den gula flerfamiljsvillan över källare med valmat tak och balkong (93505704);
- på Torsgatan den vita panelvillan med frontespiskupa, två skorstenar och inglasad veranda (93487572), villan bakom träden (93487589), det gulbruna tegelhuset med den branta gaveln mot gatan (93487584), det höga vita huset med mörkt mansardtak (93487582) och, vid Margaretaplan, det gula huset med butiken i bottenvåningen och balkongen på gaveln (93487556);
- vid Margaretaplan det gula huset med valmat tegeltak, takkupor och det vita inglasade hörnburspråket (93358537);
- på Baldersvägen den ljusgrå panelvillan med brant tegeltak och gaveln mot gatan (93487591), huset som Google har suddat ut (93487569) och det vita garaget (93487574);
- vid Stensövägen den bakre delen av det gula tegelhuset i tre våningar över källare med balkonger (93326725), de två bitar som ligger innanför modellens kant;
- vid Södra vägen Saga, det beige huset med tegeltak längst in i trädgården bakom grinden (93252863); vid Lilla Dammgatan det gula tegelhuset i tre våningar med balkonger bakom träden (93291989); på kullen ovanför Söderportsgatan den vita villan med hörnpaviljonger och lågt valmtak (93329952).

Ingen av tomterna är riven eller tom på Street View-bilderna; alla 21 hus har en egen mesh. Fyra hus skärs av pass 98:s modellkant (x −1650 eller y 320) och är byggda på den avskurna konturen med släta väggar mot kanten; tegelhuset vid Stensövägen har fått platt tak, eftersom dess låga sadeltak fortsätter utanför kanten. Ett hus syns bara bakom Googles suddning och har fått en rimlig form efter grannarna.

Pass 98:s klumpmesher `SM_Slott98_Buildings_W`, `SM_Slott98_Buildings_M` och `SM_Slott98_Buildings_E` byggs om med `slott98_chunks115` från pass 115, utan de hus som nu är detaljerade. Husen från pass 134, 136, 138 och 139 hålls utanför dem.

Efter det här passet återstår på fastlandet bara gårds- och bakhus: 59 konturer som ligger 25 m eller längre från närmaste gata. De står i `left_to_yards` i `source/block140.json`.

Bara en del av höjderna är inmätta (raden på Ringgatan, det höga gula huset, tegelhuset och villan vid Torsgatan och Baldersvägen och de två gula husen vid Margaretaplan); fem kameror är bestämda mot OSM-konturerna, resten av höjderna är uppskattade från våningar, dörrar och fönster.

Passet är gjort av Claude och finns bara i arbetskopian.

Geometrikontrollerna i Blender är godkända och pass 28–139 är oförändrade utom de avsedda ändringarna: fastlandets samlade husdelar från pass 98 (W, M och E) är återskapade utan de nya husen. Import och kontroller i Unreal görs när modellerna i området är klara.

Källor och mätningar finns i `references/block140-notes.md`.
