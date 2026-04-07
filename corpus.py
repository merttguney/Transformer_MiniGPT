"""Türkçe metin tamamlama için genişletilmiş corpus (~60KB)."""

from __future__ import annotations


def build_corpus() -> str:
    paragraphs = [
        # ════════════════════════════════════════
        # İSTANBUL
        # ════════════════════════════════════════
        "İstanbul iki kıtayı birleştiren eşsiz bir şehirdir. Boğazın mavi suları üzerinde yükselen minareler ve tarihi yapılar bu kadim şehre benzersiz bir güzellik katmaktadır. Kapalıçarşı'nın labirent gibi sokaklarında yürürken geçmişin izlerini her köşede görebilirsiniz. Ayasofya ve Sultanahmet Camii şehrin en önemli simgeleri arasında yer alır. Her yıl milyonlarca turist bu muhteşem yapıları ziyaret etmek için dünyanın dört bir yanından İstanbul'a gelir.",
        "İstanbul'un sokakları tarih kokar. Galata Kulesi'nden bakıldığında Haliç'in muhteşem manzarası gözler önüne serilir. Balat'ın renkli evleri, Beyoğlu'nun canlı caddeleri ve Kadıköy'ün hareketli pazarları şehre ayrı bir karakter katar. Her mevsim farklı bir güzellik sunan İstanbul dünyanın en büyüleyici şehirlerinden biridir. Şehrin her köşesinde keşfedilmeyi bekleyen bir hazine vardır.",
        "Boğaziçi İstanbul'un en güzel manzaralarını sunar. Rumeli Hisarı'ndan Anadolu Hisarı'na uzanan kıyı şeridi boyunca yalılar ve köşkler sıralanır. Akşam olduğunda Boğaz'ın suları üzerinde yansıyan ışıklar büyülü bir atmosfer yaratır. Vapurla Boğaz turu yapmak İstanbul'un en keyifli deneyimlerinden biridir. Martıların eşliğinde yapılan bu yolculuk unutulmaz anılar bırakır.",
        "İstanbul'da sabahlar çok güzeldir. Simitçilerin sesleri sokaklarda yankılanır. Çay bardakları tezgahlarda buhar bırakır. İnsanlar işe giderken vapurlara koşar. Boğaz'ın üzerinden geçen gemiler ufukta kaybolur. Balıkçılar Galata Köprüsü'nde sabırla bekler. Güvercinler Sultanahmet Meydanı'nda uçuşur. Şehir uyanır ve hayat başlar.",
        "İstanbul'un tarihi yarımadası dünya mirası listesindedir. Topkapı Sarayı yüzyıllarca Osmanlı padişahlarına ev sahipliği yapmıştır. Yerebatan Sarnıcı'nın gizemli atmosferi ziyaretçileri büyüler. Süleymaniye Camii Mimar Sinan'ın şaheseridir. Küçük Ayasofya ise en eski kiliselerden biridir. Bu yapılar İstanbul'un zengin tarihini gözler önüne serer.",

        # ════════════════════════════════════════
        # ANADOLU VE TÜRKİYE
        # ════════════════════════════════════════
        "Anadolu'nun bereketli toprakları binlerce yıldır medeniyetlere ev sahipliği yapmıştır. Hititlerin, Friglerin, Lidyalıların ve daha nice uygarlıkların izleri bu topraklarda yaşamaktadır. Kapadokya'nın peri bacaları, Pamukkale'nin travertenleri ve Nemrut Dağı'nın dev heykelleri Anadolu'nun zengin mirasını yansıtmaktadır. Her taşın altında bir tarih, her vadide bir hikâye saklıdır.",
        "Anadolu steplerinden Ege kıyılarına, Karadeniz yaylalarından Akdeniz sahillerine uzanan bu topraklar eşsiz bir coğrafi çeşitlilik sunmaktadır. Doğu Anadolu'nun sert kışları, Akdeniz'in ılıman iklimiyle tezat oluşturur. Bu zengin coğrafya farklı kültürlerin bir arada yaşamasına olanak tanımıştır. Türkiye hem doğunun hem batının renklerini taşıyan bir köprü ülkedir.",
        "Ankara Türkiye Cumhuriyeti'nin başkentidir. Modern bir şehir olan Ankara'da Anıtkabir ülkenin en önemli ziyaret noktasıdır. Kızılay Meydanı şehrin kalbinde yer alır. Ankara Kalesi ise şehrin en eski yerleşim alanıdır. Atatürk Orman Çiftliği geniş yeşil alanlarıyla halkın dinlenme mekanıdır. Ankara büyük üniversiteleriyle de tanınır.",
        "İzmir güzel bir liman şehridir. Kordon boyunca yürümek insana huzur verir. Saat Kulesi şehrin simgesidir. Kemeraltı Çarşısı canlı ve renkli bir ticaret merkezidir. Efes Antik Kenti yakınlarda bulunur ve dünyanın en önemli arkeolojik alanlarından biridir. İzmir Ege'nin incisi olarak anılır.",
        "Kapadokya dünyanın en ilginç doğal oluşumlarına ev sahipliği yapar. Peri bacaları milyonlarca yıllık erozyonun eseridir. Bölgede kayalara oyulmuş kiliseler ve yeraltı şehirleri bulunur. Sabah erken saatlerde gökyüzünü kaplayan sıcak hava balonları muhteşem bir manzara oluşturur. Kapadokya'yı ziyaret eden herkes bu büyülü atmosferden etkilenir.",
        "Antalya Türkiye'nin turizm başkentidir. Masmavi denizi, altın sarısı kumsalları ve antik kentleriyle ünlüdür. Kaleiçi tarihi dokusunu koruyan bir semttir. Düden Şelalesi şehrin en güzel doğal güzelliklerinden biridir. Aspendos Antik Tiyatrosu hâlâ konserler için kullanılmaktadır. Antalya her yıl milyonlarca turisti ağırlar.",
        "Trabzon Karadeniz'in en güzel şehirlerinden biridir. Sümela Manastırı dik yamaçlara inşa edilmiş hayranlık uyandıran bir yapıdır. Uzungöl doğal güzelliğiyle ünlü bir yayladır. Trabzon mutfağı özellikle kaymağı ve pidesiyle tanınır. Bölgenin yeşil vadileri ve çay bahçeleri huzur verici manzaralar sunar.",

        # ════════════════════════════════════════
        # DOĞA VE MEVSİMLER
        # ════════════════════════════════════════
        "Bahar geldiğinde doğa uyanır. Ağaçlar çiçek açar, kuşlar ötmeye başlar ve her yer yeşile bürünür. İlkbaharın taze havası insanlara enerji verir. Günler uzar, güneş daha sıcak parlar ve hayat yeniden canlanır. Kırlarda rengarenk çiçekler açar ve arılar bal toplamak için çalışmaya başlar. Bahar yeniden doğuşun simgesidir.",
        "Yaz mevsiminde güneş en yüksek noktasına ulaşır. Sahiller insanlarla dolar, denizin mavi rengi gökyüzüyle buluşur. Sıcak günlerin ardından gelen serin akşamlar huzur verir. Çocuklar parklarda oynar, aileler pikniğe gider ve hayat dışarıda yaşanır. Yaz tatili herkesin özlemle beklediği bir dönemdir.",
        "Sonbahar yaprakların dans ettiği bir mevsimdir. Ağaçlar sarıya, turuncuya ve kırmızıya bürünür. Rüzgar yaprakları savurur ve sokaklar rengarenk bir halıyla kaplanır. Hasat zamanı gelmiştir ve çiftçiler yılın emeğini toplamaya başlar. Günler kısalır ve akşamlar erken çöker. Sonbahar hüzünlü ama güzel bir mevsimdir.",
        "Kış geldiğinde doğa beyaz bir örtüyle kaplanır. Kar yağışı sessizce başlar ve her yeri bembeyaz yapar. Çocuklar kardan adam yapar, kızakla kayar ve kar topu oynar. Soğuk günlerde sıcak bir çorba ya da çay insanı içten ısıtır. Şöminenin başında oturmak kışın en güzel keyiflerinden biridir.",
        "Ormanlar gezegenimizin en değerli varlıklarıdır. Ağaçlar havayı temizler, toprağı korur ve sayısız canlıya ev sahipliği yapar. Bir ormanın içinde yürümek stresi azaltır ve insana huzur verir. Kuş sesleri, yaprak hışırtıları ve dere şırıltıları doğanın müziğini oluşturur. Ormanları korumak geleceğimiz için çok önemlidir.",
        "Deniz kenarında oturmak huzur verir. Dalgaların sesi rüzgarla birleşir. Kumun üzerinde yürümek ayaklara masaj yapar. Güneşin batışı deniz üzerinde altın rengi bir yol oluşturur. Balıkçı tekneleri ufukta süzülür. Deniz insana özgürlük hissi verir. Her dalga yeni bir başlangıçtır.",
        "Dağların zirvesinde hava soğuk ve temizdir. Bulutlar ayaklarınızın altında kalır. Zirveye ulaşmak zorlu bir yolculuktur ama manzara tüm yorgunluğu unutturur. Dağ çiçekleri kayaların arasından boy verir. Kartallar gökyüzünde süzülür. Dağlar doğanın en heybetli eserleridir.",

        # ════════════════════════════════════════
        # ATASÖZÜ VE DEYİMLER
        # ════════════════════════════════════════
        "Sakın kader deme, kaderin üstünde bir kader vardır. Gül dikensiz olmaz, emek vermeden yol alınmaz. Bir fincan kahvenin kırk yıl hatırı vardır. Damlaya damlaya göl olur, sabırla taş deler su. Rüzgar eken fırtına biçer, iyilik eden iyilik bulur. Karanlık gecenin ardından elbet bir sabah doğar. Yola çıkan yolunu bulur, duran su yosun tutar.",
        "Birlikten kuvvet doğar. Ağaç yaşken eğilir. Acele işe şeytan karışır. Ak akçe kara gün içindir. Bal tutan parmağını yalar. Boş çuval dik durmaz. Dost kara günde belli olur. El elden üstündür. Güneş balçıkla sıvanmaz. Her işin başı sağlık. Yuvarlanan taş yosun tutmaz. İşleyen demir pas tutmaz.",
        "Sabır acıdır ama meyvesi tatlıdır. Güzel söz yılanı deliğinden çıkarır. Körle yatan şaşı kalkar. Mum dibine ışık vermez. Nerede hareket orada bereket. Öğrenmenin yaşı yoktur. Roma bir günde kurulmadı. Su uyur düşman uyumaz. Tarlasını süren öküzünü doyurur. Üzüm üzüme baka baka kararır.",
        "Hayatta en hakiki mürşit ilimdir. Çalışmadan başarı gelmez, emek vermeden kazanç olmaz. Her zorluk bir kolaylığın habercisidir. Umudunu kaybetme, karanlığın sonu aydınlıktır. Düşen kalkar, yenilen öğrenir ve başarılı olan asla vazgeçmez. Azim ve kararlılık başarının anahtarıdır.",
        "Ağır olan gem, demir dayanmaz kenara. El el üstünde güç birlikte olur. Küçük taşlar büyük duvarlar yapar. Her yokuşun bir inişi vardır. Sabreden derviş muradına ermiş. Güneşi görmeyen gölgeyi bilmez. Gecenin en karanlık anı şafaktan hemen öncedir. Yol yürümekle tükenir.",
        "Bilgi güçtür ve bilgili insan her zaman bir adım öndedir. Kitap en iyi dosttur, sessiz ama bilge bir yoldaştır. Kalem kılıçtan keskindir, yazılan söz kalıcıdır. Okumak zihnin gıdasıdır, düşünmek ruhun egzersizidir. Cehalet karanlıktır, ilim ise aydınlıktır.",

        # ════════════════════════════════════════
        # BİLİM VE TEKNOLOJİ
        # ════════════════════════════════════════
        "Yapay zeka günümüzün en heyecan verici teknolojilerinden biridir. Makineler artık öğrenebilir, tahmin yapabilir ve insanlara yardımcı olabilir. Derin öğrenme algoritmaları büyük veri kümeleri üzerinde eğitilerek karmaşık örüntüleri keşfedebilmektedir. Doğal dil işleme sayesinde bilgisayarlar artık insan dilini anlayabilir ve üretebilir.",
        "Transformer mimarisi doğal dil işleme alanında devrim yaratmıştır. Dikkat mekanizması sayesinde modeller metnin farklı bölümleri arasındaki ilişkileri öğrenebilmektedir. Bu mimari sayesinde metin tamamlama, çeviri ve özetleme gibi görevlerde büyük başarılar elde edilmiştir. Yapay zeka her geçen gün daha gelişmiş hale gelmektedir.",
        "Bilgisayar biliminin temelleri matematik ve mantığa dayanır. Algoritmalar problemleri adım adım çözmek için tasarlanmış yöntemlerdir. Veri yapıları bilginin verimli şekilde saklanması ve işlenmesi için kullanılır. Programlama dilleri insanların bilgisayarlarla iletişim kurmasını sağlar. Her programcı bu temel kavramları iyi bilmelidir.",
        "İnternet dünyayı değiştiren en büyük icatlardan biridir. İnsanlar artık dünyanın her yerindeki bilgiye anında erişebilmektedir. Sosyal medya insanların iletişim biçimini kökten değiştirmiştir. Elektronik ticaret alışveriş alışkanlıklarını dönüştürmüştür. Dijital çağda yaşamak hem fırsatlar hem de zorluklar sunmaktadır.",
        "Uzay araştırmaları insanlığın en büyük macerasıdır. İlk uydu yörüngeye fırlatıldığında yeni bir çağ başlamıştır. İnsanın Ay'a ayak basması tarihte bir dönüm noktasıdır. Mars'a insan göndermek yakın geleceğin en büyük hedeflerinden biridir. Uzay teleskopu evrenin derinliklerini keşfetmemizi sağlamaktadır.",
        "Tıp bilimi insanlık tarihinin en önemli alanlarından biridir. Aşılar milyonlarca hayat kurtarmıştır. Antibiyotiklerin keşfi enfeksiyon hastalıklarıyla mücadelede devrim yaratmıştır. Genetik mühendisliği geleceğin tıbbını şekillendirmektedir. Yapay organlalar ve biyonik protezler hastaların yaşam kalitesini artırmaktadır.",

        # ════════════════════════════════════════
        # TÜRK MUTFAĞI
        # ════════════════════════════════════════
        "Türk mutfağı dünyanın en zengin mutfaklarından biridir. Kebaplar, mezeleler, börekler ve tatlılar Türk sofrasının vazgeçilmez lezzetleridir. Lahmacun, pide ve döner dünyaca ünlü yemeklerdir. Türk kahvesi ise kültürün önemli bir parçasıdır ve kırk yıllık hatırı vardır.",
        "Kahvaltı Türk kültüründe çok önemli bir yere sahiptir. Peynir, zeytin, domates, salatalık, bal, kaymak ve taze ekmek bir Türk kahvaltısının olmazsa olmazlarıdır. Çay ise her öğünde sofranın baş tacıdır. Türk çayı ince belli bardaklarda, demli ve sıcak içilir. Kahvaltı ailece yapılan bir ritüeldir.",
        "Adana kebabı Türk mutfağının en meşhur yemeklerinden biridir. Acılı kıyma ile yapılır ve lavash ekmek ile servis edilir. İskender kebap ise Bursa'nın ünlü lezzetidir. Döner kebap dünyada en çok bilinen Türk yemeğidir. Her bölgenin kendine has kebap çeşidi vardır.",
        "Baklava Türk tatlılarının sultanıdır. İnce yufka katları arasına ceviz veya fıstık konularak yapılır. Şerbet ile tatlandırılır ve üzerine kaymak eklenir. Künefe Hatay'ın meşhur tatlısıdır. Sütlaç, kazandibi ve tavuk göğsü de Türk mutfağının önemli tatlılarıdır.",
        "Türk çayı kültürün vazgeçilmez bir parçasıdır. Çay her zaman ve her yerde içilir. Sabah kahvaltıda, öğleden sonra sohbet sırasında, akşam yemekten sonra çay içilir. İnce belli çay bardağı Türk çay kültürünün simgesidir. Çay ocaklarında dostlar buluşur ve sohbet eder.",

        # ════════════════════════════════════════
        # EDEBİYAT
        # ════════════════════════════════════════
        "Türk edebiyatı köklü bir geçmişe sahiptir. Yunus Emre'nin şiirleri sevgi ve hoşgörüyü anlatır. Mevlana'nın eserleri evrensel barış mesajı verir. Nazım Hikmet modern Türk şiirinin öncülerindendir. Orhan Pamuk Nobel Edebiyat Ödülü'nü kazanan ilk Türk yazardır. Yaşar Kemal ise Anadolu insanının sesini dünyaya duyurmuştur.",
        "Hikâye anlatmak insanlığın en eski sanatlarından biridir. İyi bir hikâye okuyucuyu farklı dünyalara götürür, farklı yaşamları deneyimletir ve düşünmeye sevk eder. Her hikâyenin bir başlangıcı, bir gelişmesi ve bir sonucu vardır. Karakterler hikâyenin ruhunu oluşturur. İyi yazılmış bir karakter okuyucunun kalbinde yaşar.",
        "Şiir duyguların en saf ifadesidir. Kelimeler ritimle buluşur, anlam derinleşir ve ruh konuşur. Türk şiiri Divan edebiyatından modern şiire kadar uzanan zengin bir geleneğe sahiptir. Şairler toplumun vicdanıdır, kelimelerin mimarıdır ve duyguların tercümanıdır.",
        "Roman uzun soluklu bir edebiyat türüdür. İyi bir roman okuyucuyu başka hayatlara taşır. Karakterlerin gelişimi, olayların akışı ve mekanların tasvirli okuyucuyu hikayenin içine çeker. Türk romanı cumhuriyet döneminde büyük gelişme göstermiştir. Halide Edib, Reşat Nuri ve Sabahattin Ali Türk edebiyatının önemli romancılarıdır.",

        # ════════════════════════════════════════
        # FELSEFE VE HAYAT
        # ════════════════════════════════════════
        "Hayat bir yolculuktur ve her adım yeni bir deneyim getirir. Bazen yollar düz ve kolay, bazen engebeli ve zor olur. Önemli olan yolculuğun kendisidir, varılacak yer değil. Her düşüş yeni bir kalkış, her başarısızlık yeni bir ders demektir. Hayatı güzel kılan onun değerini bilmektir.",
        "İnsan düşünen bir varlıktır. Düşünce özgürlüğü en temel haklardan biridir. Felsefe insanın kendini ve evreni anlamaya çalışmasıdır. Bilgelik soru sormakla başlar. Sokrates bildiğim tek şey hiçbir şey bilmediğimdir demiştir. Soru sormak bilginin kapısını açar.",
        "Mutluluk dışarıda değil içeridedir. Sahip olduklarımızla değil bakış açımızla mutlu oluruz. Şükretmek mutluluğun anahtarıdır. Küçük şeylerde büyük huzur bulmak hayatın sırrıdır. Gülümsemek en güzel hediyedir. Mutlu insan çevresine de mutluluk yayar.",
        "Zaman en değerli kaynaktır çünkü geri gelmez. Her an bilinçli yaşanmalıdır. Geçmişe takılmak gelecekten çalmaktır. Şimdiki anı yaşamak bilgeliktir. Zamanı iyi kullanmak başarının temelidir. Erken kalkan yol alır, planlı çalışan hedefe ulaşır.",
        "Dostluk hayatın en güzel hediyelerinden biridir. Gerçek dost iyi günde de kötü günde de yanınızdadır. Dostluk güvene, saygıya ve sevgiye dayanır. İyi bir dost aynada görünemeyenleri gösterir. Dostlar hayatı güzelleştirir, zorlukları hafifletir ve mutlulukları çoğaltır.",
        "Sevgi evrenin en güçlü enerjisidir. İnsanı büyüten, iyileştiren ve güçlendiren bir duygudur. Sevgi vermekle çoğalır, paylaşmakla büyür. Anne sevgisi en saf ve koşulsuz sevgidir. Sevgi olmadan hayat anlamsızdır.",

        # ════════════════════════════════════════
        # TARİH
        # ════════════════════════════════════════
        "Osmanlı İmparatorluğu altı yüz yılı aşkın bir süre hüküm sürmüştür. Üç kıtaya yayılan bu büyük devlet sanattan bilime, mimariden edebiyata pek çok alanda önemli eserler bırakmıştır. Mimar Sinan'ın eserleri bugün hâlâ hayranlıkla izlenmektedir. Topkapı Sarayı imparatorluğun yönetim merkeziydi.",
        "Türkiye Cumhuriyeti yeni bir çağın başlangıcıdır. Modern eğitim sistemi, hukuk reformları ve demokratik değerler cumhuriyetin temel taşlarıdır. Bilim ve teknoloji alanında sürekli gelişen Türkiye dünya sahnesinde önemli bir yere sahiptir. Cumhuriyetin ilk yıllarında yapılan reformlar ülkeyi modernleştirmiştir.",
        "Selçuklular Anadolu'nun kapılarını Türklere açmıştır. Malazgirt Meydan Muharebesi tarihte önemli bir dönüm noktasıdır. Bu savaştan sonra Türkler Anadolu'ya yerleşmeye başlamıştır. Konya Selçuklu başkenti olarak önemli bir kültür merkezi haline gelmiştir. Alaeddin Tepesi ve Mevlana Müzesi bu dönemin izlerini taşır.",
        "Çanakkale Savaşı Türk tarihinin en önemli olaylarından biridir. Bu savaşta Türk askerleri büyük bir kahramanlık göstermiştir. Çanakkale geçilmez sözü bu savaşın simgesidir. Binlerce genç vatan savunması için canını feda etmiştir. Bu zafer milletin birlik ve beraberliğinin simgesidir.",

        # ════════════════════════════════════════
        # EĞİTİM
        # ════════════════════════════════════════
        "Eğitim toplumların geleceğini şekillendiren en önemli güçtür. Okumak ve öğrenmek insanın en değerli yatırımıdır. Bilgi güçtür ve bilgiye sahip olan toplumlar her zaman bir adım öndedir. Öğretmenler toplumun en değerli hazineleridir. İyi bir öğretmen öğrencisinin hayatını değiştirebilir.",
        "Kitap okumak zihnin egzersizidir. Her kitap yeni bir pencere açar, yeni ufuklar sunar. Okuma alışkanlığı küçük yaşta kazanılmalıdır. Kütüphaneler bilginin tapınaklarıdır ve herkesin erişimine açık olmalıdır. Dijital çağda bile kitapların yeri doldurulamaz.",
        "Üniversiteler bilginin ve araştırmanın merkezleridir. Öğrenciler burada sadece bilgi edinmez, aynı zamanda eleştirel düşünme becerisi kazanır. Akademik özgürlük bilimin gelişmesi için vazgeçilmezdir. İyi bir eğitim sistemi ülkenin geleceğini belirler.",
        "Çocuklar geleceğimizdir. Onlara iyi bir eğitim vermek en büyük sorumluluğumuzdur. Eğitim sadece okulda değil, evde ve toplumda da devam eder. Aileden öğrenilen değerler karakterin temelini oluşturur. Her çocuk eşit eğitim fırsatına sahip olmalıdır.",

        # ════════════════════════════════════════
        # SPOR
        # ════════════════════════════════════════
        "Futbol Türkiye'de en popüler spordur. Milyonlarca insan hafta sonu maçları heyecanla takip eder. Galatasaray, Fenerbahçe ve Beşiktaş Türk futbolunun üç büyük kulübüdür. Stadyumlardaki atmosfer dünyanın en coşkulu ortamlarından biridir. Futbol insanları bir araya getiren güçlü bir tutkudur.",
        "Spor sağlıklı bir yaşamın temel taşıdır. Düzenli egzersiz hem bedeni hem zihni güçlendirir. Yürüyüş, yüzme, bisiklet ve yoga en sağlıklı sporlar arasındadır. Takım sporları ise iş birliği ve dayanışmayı öğretir. Her gün en az otuz dakika hareket etmek sağlığın korunması için önemlidir.",
        "Olimpiyat oyunları spor dünyasının en büyük etkinliğidir. Dört yılda bir düzenlenen bu organizasyon dünya barışını simgeler. Türk sporcular olimpiyatlarda güreş, halter ve atletizm dallarında başarılar elde etmiştir. Spor ulusal gurur ve birlik duygusunu güçlendirir.",

        # ════════════════════════════════════════
        # MÜZİK VE SANAT
        # ════════════════════════════════════════
        "Türk müziği çok sesli bir gelenekten beslenir. Klasik Türk müziğinden halk müziğine, poptan rock'a geniş bir yelpaze sunar. Bağlama, ney ve ud Türk müziğinin temel enstrümanlarıdır. Aşık Veysel ve Barış Manço Türk müziğinin efsaneleri arasındadır. Müzik dil, din ve ırk ayrımı yapmaz.",
        "Sanat insanın en derin duygularını ifade etme biçimidir. Resim, müzik, edebiyat, tiyatro ve sinema sanatın farklı dallarıdır. Her sanat eseri yaratıcısının iç dünyasını yansıtır. Güzel sanatlar toplumların kültürel zenginliğinin göstergesidir. Sanat olmadan bir toplum eksik kalır.",
        "Tiyatro sahne sanatlarının en eski ve en etkili biçimlerinden biridir. Oyuncular sahnede karakterlere hayat verir. Seyirci hikayeye tanık olur ve duygularını paylaşır. Türk tiyatrosu geleneksel Karagöz ve Hacivat'tan modern tiyatroya kadar uzanan bir geçmişe sahiptir.",
        "Sinema yirminci yüzyılın en önemli sanat dallarından biridir. Görüntü ve ses bir araya gelerek güçlü hikayeler anlatır. Türk sineması Yeşilçam döneminden günümüze kadar büyük gelişme göstermiştir. Nuri Bilge Ceylan filmleriyle uluslararası ödüller kazanmıştır.",

        # ════════════════════════════════════════
        # DOĞA KORUMA VE ÇEVRE
        # ════════════════════════════════════════
        "Doğayı korumak gelecek nesillere karşı en büyük sorumluluğumuzdur. Ormanlar gezegenimizin ciğerleridir ve her yıl binlerce hektar orman yok olmaktadır. Su kaynakları tükenmekte, iklim değişikliği yaşam alanlarını tehdit etmektedir. Geri dönüşüm, enerji tasarrufu ve bilinçli tüketim ile doğayı koruyabiliriz.",
        "Temiz su dünyanın en değerli kaynağıdır. Su olmadan yaşam mümkün değildir. Nehirler, göller ve yeraltı suları korunmalıdır. Su tasarrufu herkesin sorumluluğudur. Kirli su hastalıklara neden olur. Temiz suya erişim temel bir insan hakkıdır.",
        "İklim değişikliği gezegenimizin en büyük tehdididir. Buzullar eriyor, deniz seviyeleri yükseliyor ve hava olayları şiddetleniyor. Yenilenebilir enerji kaynakları geleceğimiz için umut ışığıdır. Güneş enerjisi, rüzgar enerjisi ve hidroelektrik temiz enerji kaynaklarıdır.",

        # ════════════════════════════════════════
        # GÜNLÜK HAYAT
        # ════════════════════════════════════════
        "Sabah erkenden kalkmak güne iyi bir başlangıç yapmanın anahtarıdır. Sağlıklı bir kahvaltı, kısa bir egzersiz ve planlı bir gün insana enerji verir. Akşam olduğunda gün değerlendirilir ve ertesi güne hazırlık yapılır. Düzenli yaşam sağlığın temelidir.",
        "İnsanlar arası iletişim hayatın en önemli becerilerinden biridir. Dinlemek konuşmaktan daha değerlidir. Empati kurmak ilişkilerin temelini oluşturur. Saygı ve hoşgörü toplumsal barışın anahtarıdır. İyi iletişim kuran insan her ortamda başarılı olur.",
        "Aile toplumun en küçük ama en önemli yapı taşıdır. Ailede sevgi, saygı ve güven birlikte büyür. Anne ve baba çocuğun ilk öğretmenleridir. Aile bağları insanı güçlü kılar ve zor zamanlarda destek olur. Mutlu bir aile sağlıklı bir toplumun temelidir.",
        "Komşuluk ilişkileri Türk kültüründe çok değerlidir. Komşu komşunun külüne muhtaçtır sözü bu önemi anlatır. Bayramlarda komşu ziyaretleri yapılır. İhtiyaç olduğunda komşular birbirine yardım eder. İyi komşuluk hayatı güzelleştirir.",
        "Kadın hakları çağdaş toplumların temel değerlerinden biridir. Kadınlar toplumun her alanında eşit haklara sahip olmalıdır. Eğitimden iş hayatına, siyasetten sanata kadar kadınlar büyük başarılara imza atmaktadır. Toplumsal cinsiyet eşitliği herkes için daha iyi bir dünya demektir.",

        # ════════════════════════════════════════
        # UZAY VE EVREN
        # ════════════════════════════════════════
        "Evren sonsuz gizemlerle doludur. Yıldızlar, gezegenler, galaksiler ve kara delikler evrenin yapı taşlarıdır. İnsanlık uzayı keşfetme serüveninde büyük adımlar atmıştır. Güneş sistemimizde sekiz gezegen bulunmaktadır. Her gezegenin kendine has özellikleri vardır.",
        "Matematik evrenin dilidir. Sayılar, denklemler ve formüller doğanın sırlarını çözmemize yardımcı olur. Geometri uzayı anlamamızı sağlar. İstatistik belirsizliği ölçmemize ve karar vermemize yardımcı olur. Matematik olmadan bilim var olamaz.",
        "Yıldızlar evrenin en büyüleyici varlıklarıdır. Güneşimiz sıradan bir yıldızdır ama bizim için hayat kaynağıdır. Yıldızlar doğar, yaşar ve ölür. Süpernova patlamaları evrenin en güçlü olaylarıdır. Samanyolu galaksisinde milyarlarca yıldız bulunmaktadır.",

        # ════════════════════════════════════════
        # EKONOMİ VE İŞ DÜNYASI
        # ════════════════════════════════════════
        "Ekonomi bir ülkenin kalkınmasının temelidir. Üretim, ticaret ve yatırım ekonominin üç ayağıdır. Girişimcilik yeni iş fırsatları yaratır ve istihdamı artırır. Küçük işletmeler ekonominin bel kemiğidir. İnovasyon rekabet gücünün anahtarıdır.",
        "Para yönetimi hayatın önemli becerilerinden biridir. Birikim yapmak geleceğe yatırımdır. Gereksiz harcamalardan kaçınmak finansal özgürlüğün anahtarıdır. Bütçe planlaması ailelerin ekonomik güvenliğini sağlar. Tasarruf alışkanlığı küçük yaşta kazanılmalıdır.",

        # ════════════════════════════════════════
        # SAĞLIK
        # ════════════════════════════════════════
        "Sağlık en büyük zenginliktir. Sağlıklı yaşam dengeli beslenme, düzenli egzersiz ve yeterli uykudan oluşur. Stres yönetimi vücud ve zihin sağlığı için çok önemlidir. Düzenli sağlık kontrolleri hastalıkların erken teşhisini sağlar. Sağlıklı bir beden mutlu bir ruh demektir.",
        "Beslenme sağlığın temeldidir. Sebze ve meyve tüketimi hastalıklara karşı koruyucudur. Protein vücudun yapı taşıdır. Su yeterli miktarda içilmelidir. İşlenmiş gıdalardan uzak durmak sağlığı korur. Dengeli beslenme uzun ve sağlıklı bir yaşamın anahtarıdır.",
        "Uyku vücudun kendini yenilemesi için gereklidir. Yetişkinler günde yedi ila sekiz saat uyumalıdır. İyi uyku hafızayı güçlendirir ve bağışıklık sistemini destekler. Düzensiz uyku birçok sağlık sorununa yol açabilir. Uyku kalitesi için karanlık ve sessiz bir ortam önemlidir.",

        # ════════════════════════════════════════
        # TEKNOLOJİ VE DİJİTAL DÜNYA
        # ════════════════════════════════════════
        "Akıllı telefonlar hayatımızın ayrılmaz bir parçası haline gelmiştir. İletişimden eğitime, eğlenceden alışverişe kadar her alanda kullanılmaktadır. Mobil uygulamalar günlük hayatımızı kolaylaştırır. Ancak aşırı ekran süresi sağlığa zararlı olabilir. Teknolojiyi bilinçli kullanmak önemlidir.",
        "Robotlar gelecekte birçok işi insanların yerine yapacaktır. Fabrikalarda, hastanelerde ve evlerde robotlar kullanılmaya başlanmıştır. Yapay zeka destekli robotlar giderek daha akıllı hale gelmektedir. İnsan ve robot iş birliği geleceğin çalışma modelini belirleyecektir.",

        # ════════════════════════════════════════
        # KÜLTÜR VE GELENEK
        # ════════════════════════════════════════
        "Bayramlar Türk kültürünün en önemli geleneklerindendir. Ramazan Bayramı ve Kurban Bayramı dini bayramlardır. Bayramlarda büyüklerin eli öpülür, küçüklere harçlık verilir. Aileler bir araya gelir ve birlikte yemek yer. Bayram ziyaretleri toplumsal bağları güçlendirir.",
        "Düğünler Türk kültüründe büyük önem taşır. Kına gecesi gelinin en özel anlarından biridir. Düğün günü müzik, dans ve yemeklerle kutlanır. Her bölgenin kendine has düğün adetleri vardır. Düğünler iki ailenin birleşmesini simgeler.",
        "Türk el sanatları zengin bir geleneğe sahiptir. Çini, halı dokuma, ebru ve hat sanatı en önemli el sanatlarıdır. İznik çinileri dünyaca ünlüdür. Türk halıları yüzyıllardır evlerin vazgeçilmez süsüdür. El sanatları kültürel mirasın korunmasında önemli bir rol oynar.",
        "Misafirperverlik Türk kültürünün en belirgin özelliklerinden biridir. Eve gelen misafire çay ve ikram sunulur. Misafir ağırlamak bir onurdur. Sofra paylaşmak dostluğun ifadesidir. Türk insanı cömert ve sıcakkanlıdır.",

        # ════════════════════════════════════════
        # EK PARAGRAFLAR (ÇEŞİTLİLİK)
        # ════════════════════════════════════════
        "Denizcilik Türkiye'nin önemli sektörlerinden biridir. Üç tarafı denizlerle çevrili olan Türkiye zengin bir denizcilik geleneğine sahiptir. Ticaret gemileri dünya limanları arasında yük taşır. Balıkçılık kıyı bölgelerinde önemli bir geçim kaynağıdır. Deniz turizmi her yıl büyümektedir.",
        "Tarım Anadolu'nun en eski geçim kaynağıdır. Buğday, pamuk, tütün ve çay önemli tarım ürünleridir. Çay Doğu Karadeniz'de, zeytin Ege ve Akdeniz'de yetiştirilir. Fındık üretiminde Türkiye dünyada birinci sıradadır. Tarım ülke ekonomisinin önemli bir bütçesini oluşturur.",
        "Türk kahvesi hazırlanması ve sunulmasıyla bir sanattır. İnce öğütülmüş kahve cezveye konulur ve yavaş ateşte pişirilir. Köpüklü ve kıvamlı bir Türk kahvesi ustaca hazırlanır. Kahve falı bakmak ise eğlenceli bir gelenektir. Türk kahvesi dostluk ve sohbetin simgesidir.",
        "Göçebe yaşam Türk tarihinin önemli bir parçasıdır. Eski Türkler bozkırlarda at sırtında yaşamıştır. Yurt çadırı göçebe yaşamın simgesidir. Hayvancılık temel geçim kaynağı olmuştur. Bu göçebe kültür Anadolu'ya taşınarak yerleşik yaşamla harmanlanmıştır.",
        "Hamamlar Türk kültürünün önemli bir parçasıdır. Osmanlı döneminde inşa edilen tarihi hamamlar mimari harikalarıdır. Hamam sadece yıkanma yeri değil, sosyal buluşma mekanıdır. Kese ve köpük masajı geleneksel hamam ritüelinin bir parçasıdır.",
        "Türk kahvaltısı dünyanın en zengin kahvaltılarından biridir. Sofrada en az on çeşit yiyecek bulunur. Taze pişmiş ekmek, beyaz peynir, kaşar peyniri, zeytin, domates, salatalık, bal, kaymak, tereyağı ve yumurta olmazsa olmazlardır. Çay sürekli servis edilir. Aile bir arada oturur ve günü planlar.",
        "Ramazan ayı Müslümanlar için özel bir aydır. Oruç tutulur, iftarlar hazırlanır ve teravih namazları kılınır. İftar sofrasında aile bir araya gelir. Pide Ramazan'ın vazgeçilmez lezzetidir. Ramazan insanların birbirine yakınlaşmasını sağlar.",
        "Nevruz baharın gelişini kutlayan bir bayramdır. Ateş üzerinden atlanır ve yeni yıl dilekleri tutulur. Doğanın uyanışı kutlanır. Nevruz kutlamaları renkli kıyafetler ve halk danslarıyla yapılır. Bu gelenek yüzyıllardır sürmektedir.",
    ]

    # Paragrafları tekrarla ama farklı sıralamalarla
    import random
    rng = random.Random(42)
    extra = list(paragraphs)
    rng.shuffle(extra)
    all_text = paragraphs + extra  # ~2x corpus

    return "\n".join(all_text)
