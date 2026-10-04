## Pass 115 — husen i Stadsparken och längs Slottsvägen

Fjorton av de enkla volymerna från pass 98 på fastlandet väster om Kvarnholmen är ersatta av de byggnader som står där. Varje hus är nu en egen mesh, `SM_Slott115_<osm-id>`:
- 91931339, Kalmar konstmuseum: den svarta kantiga byggnaden, klädd med kvadratiska svarta plattor. Den har den glasade entrén under ett mörkt skyltband mot parken, trappan och avsatsen och några stora fönster högt upp;
- 91222116, Byttan: den vita putsade parkrestaurangen på grå sockel, med mörka fönsterspröjs och ett lågt mörkt tak med breda takfötter. Den indragna övervåningen har ett fönsterband och en skorsten;
- 91222187 och 874870421: två små parkbyggnader utan användbar bild. De är enkla putsade paviljonger;
- 93332243, Slottshotellet: den röda putsade huvudbyggnaden med vita fönsteromfattningar, branta röda tegeltak och två frontespiser mot sydost, flygeln mot nordost och den gröna stående panelflygeln mot Molinsgatan. Flygeln har ockra fönsterfoder och hörnbrädor, ett gavelfönster och snidade vindskivor;
- 93332252, Västerlånggatan 1: den laxrosa putsade villan under ett brant brunt tegeltak, med en frontespis med rundbågig balkongdörr, en balkong med smidesräcke över entrén och en skorsten;
- 93306354: tegelhuset under ett mörkgrått bandtäckt plåttak med takfönster och den glasade verandan i trä längs sydostsidan;
- 387312779 och 387312778: det låga mörkgröna panelhuset med platt tak och förrådet bredvid;
- 91970278: den gräddvita villan i två höga våningar på grå sockel, med gördelgesims, rundbågiga fönster i bottenvåningen, en fronton med fönster mot öster och den rundbågiga dörren på sin trappa;
- 91970355: den vita paviljongen under ett mörkbrunt mansardtak med takkupor och skorsten i mitten;
- 91970390: det gräddvita tvåvåningshuset med glasad entréveranda och en mörk indragen takvåning bakom ett räcke;
- 91970274, Söderportspaviljongen: gräddvit och i en våning, med höga fönster under fönsterhuvar mellan pilastrar och en fronton med lunettfönster mot Kungsgatan;
- 564958332, KIKAIN: en rund kiosk under ett koniskt tak. Den saknar bild och formen är uppskattad.

Pass 98:s klumpmeshar `SM_Slott98_Buildings_M` och `_E` byggs om med pass 98:s egen kod, utan de detaljerade husen. Mängden `SLOTT98_DETAILED` och funktionen `slott98_chunks115` gör att senare pass kan ta ut fler hus på samma sätt. Ett prov i sandlådan visade att funktionen ger exakt pass 98:s meshar för de hus som är kvar.

Slottshotellets huvudbyggnad sågs bara på långt håll och konstmuseet och Byttan bara på en osäker användarbild, så deras höjder och detaljer är uppskattade.

Passet är gjort av Claude och finns bara i arbetskopian.

Geometrikontrollerna i Blender är godkända och pass 28–114 är oförändrade utom de avsedda ändringarna: pass 98:s husdelar M och E (och pass 107:s version av M) är återskapade utan de fjorton husen, och de tidigare rättningarna i pass 85, 100, 105, 109 och 111 gäller. Import och kontroller i Unreal görs när modellerna i området är klara.

Källor och mätningar finns i `references/block115-notes.md`.
