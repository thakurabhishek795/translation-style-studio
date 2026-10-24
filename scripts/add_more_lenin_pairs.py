#!/usr/bin/env python3
"""
Adds an additional batch of 25 aligned sentences from Lenin's political economy writings
(Imperialism Chapters 2-7, Banks, Financial Capital, and Colonial Division).
"""

import os, sys

BASE_DIR = "/Users/athakur/Documents/General Things/translation-style-studio"
if BASE_DIR not in sys.path:
    sys.path.insert(0, BASE_DIR)

from app.core.memory import TranslationMemory

extra_pairs = [
    {
        "source": "The primary and fundamental function of banks is to serve as an intermediary in the making of payments.",
        "target": "बैंकों का प्राथमिक और बुनियादी कार्य भुगतानों के निपटान में मध्यस्थ के रूप में काम करना है।",
        "bad_literal": "बैंक का पहला काम पेमेंट करने में बीच का काम करना है।",
        "category": "banks_and_finance",
        "notes": "Use 'प्राथमिक और बुनियादी कार्य' for 'primary and fundamental function'."
    },
    {
        "source": "In doing so they transform inactive money capital into active, that is, into capital yielding a profit.",
        "target": "ऐसा करके वे निष्क्रिय मुद्रा-पूंजी को सक्रिय पूंजी में, यानी मुनाफा देने वाली पूंजी में बदल देते हैं।",
        "bad_literal": "ऐसा करके वे सोई हुई मुद्रा पूंजी को काम करने वाली पूंजी में बदलते हैं।",
        "category": "banks_and_finance",
        "notes": "Use 'निष्क्रिय मुद्रा-पूंजी' (inactive money capital) and 'मुनाफा देने वाली पूंजी'."
    },
    {
        "source": "As banking develops and becomes concentrated in a small number of establishments, the banks grow from modest middlemen into powerful monopolies.",
        "target": "जैसे-जैसे बैंकिंग का विकास होता है और वह कुछ गिने-चुने संस्थानों में संकेंद्रित होती है, बैंक साधारण बिचौलियों से बढ़कर शक्तिशाली एकाधिकार बन जाते हैं।",
        "bad_literal": "जैसे बैंक बढ़ते हैं वे छोटे बिचौलियों से शक्तिशाली मोनोपॉली बन जाते हैं।",
        "category": "banks_and_finance",
        "notes": "Use 'साधारण बिचौलियों से बढ़कर शक्तिशाली एकाधिकार बन जाना'."
    },
    {
        "source": "A steadily increasing proportion of capital in industry ceases to belong to the industrialists who employ it.",
        "target": "उद्योग में पूंजी का लगातार बढ़ता हुआ हिस्सा उन उद्योगपतियों का नहीं रह जाता जो उसका उपयोग करते हैं।",
        "bad_literal": "उद्योग की पूंजी का बढ़ता हिस्सा उन उद्योगपतियों का नहीं रहता जो काम करते हैं।",
        "category": "banks_and_finance",
        "notes": "Fluid Hindi phrasing avoiding awkward calque."
    },
    {
        "source": "They can obtain the use of it only through the bank, which represents the owners of the capital.",
        "target": "वे इस पूंजी का उपयोग केवल बैंक के माध्यम से ही प्राप्त कर सकते हैं, जो पूंजी के स्वामियों का प्रतिनिधित्व करता है।",
        "bad_literal": "वे इसे केवल बैंक से ले सकते हैं जो पूंजी मालिकों को दिखाता है।",
        "category": "banks_and_finance",
        "notes": "Use 'पूंजी के स्वामियों का प्रतिनिधित्व'."
    },
    {
        "source": "Finance capital is bank capital transformed into industrial capital and dominated by a handful of the biggest financiers.",
        "target": "वित्तीय पूंजी औद्योगिक पूंजी में रूपांतरित और मुट्ठी भर सबसे बड़े वित्तीय शासकों द्वारा नियंत्रित बैंक पूंजी है।",
        "bad_literal": "फाइनेंस कैपिटल बैंक कैपिटल है जो इंडस्ट्री में बदलकर बड़े बैंकरों के हाथ में है।",
        "category": "banks_and_finance",
        "notes": "Editorial rule: 'वित्तीय पूंजी' (finance capital)."
    },
    {
        "source": "Finance capital is such a great, such a decisive force in all economic and in all international relations, that it is capable of subjecting to itself even states enjoying the fullest political independence.",
        "target": "वित्तीय पूंजी सभी आर्थिक और सभी अंतर्राष्ट्रीय संबंधों में इतनी विशाल, इतनी निर्णायक शक्ति है कि वह पूर्ण राजनीतिक स्वतंत्रता का उपभोग करने वाले राज्यों को भी अपने अधीन करने में सक्षम है।",
        "bad_literal": "वित्तीय पूंजी इतनी बड़ी ताकत है कि वह स्वतंत्र देशों को भी अपने नीचे ले आती है।",
        "category": "banks_and_finance",
        "notes": "Use 'पूर्ण राजनीतिक स्वतंत्रता का उपभोग करने वाले राज्य'."
    },
    {
        "source": "Under the old capitalism, when free competition prevailed, the export of goods was the most typical feature. Under modern capitalism, when monopolies prevail, the export of capital has become the typical feature.",
        "target": "पुराने पूंजीवाद के दौर में, जब मुक्त प्रतिस्पर्धा का बोलबाला था, वस्तुओं का निर्यात सबसे विशिष्ट लक्षण था। आधुनिक पूंजीवाद के दौर में, जब एकाधिकारों का वर्चस्व है, पूंजी का निर्यात विशिष्ट लक्षण बन चुका है।",
        "bad_literal": "पुराने पूंजीवाद में जब खुली प्रतियोगिता थी माल का एक्सपोर्ट लक्षण था, नए पूंजीवाद में पूंजी का एक्सपोर्ट लक्षण है।",
        "category": "imperialism_and_capital",
        "notes": "Classic comparative formulation: 'वस्तुओं का निर्यात' vs 'पूंजी का निर्यात'."
    },
    {
        "source": "The necessity for exporting capital arises from the fact that in a few countries capitalism has become \"overripe\" and capital cannot find \"profitable\" investment.",
        "target": "पूंजी के निर्यात की आवश्यकता इस तथ्य से पैदा होती है कि कुछ देशों में पूंजीवाद 'अति-परिपक्व' हो चुका है और पूंजी को 'लाभकारी' निवेश के अवसर नहीं मिल पा रहे हैं।",
        "bad_literal": "पूंजी एक्सपोर्ट की जरूरत इसलिए आती है क्योंकि पूंजीवाद बहुत पक चुका है और मुनाफा नहीं मिलता।",
        "category": "imperialism_and_capital",
        "notes": "Use 'अति-परिपक्व' for 'overripe' and 'लाभकारी निवेश'."
    },
    {
        "source": "As long as capitalism remains what it is, surplus capital will be utilised not for the purpose of raising the standard of living of the masses in a given country, but for the purpose of increasing profits by exporting capital abroad to the backward countries.",
        "target": "जब तक पूंजीवाद का स्वरूप जैसा है वैसा बना रहेगा, अधिशेष पूंजी का उपयोग किसी देश में जनता के जीवन स्तर को ऊंचा उठाने के लिए नहीं, बल्कि पिछड़े देशों में पूंजी का निर्यात करके मुनाफे को बढ़ाने के लिए किया जाएगा।",
        "bad_literal": "जब तक पूंजीवाद रहेगा, बचा हुआ पैसा जनता का जीवन सुधारने में नहीं बल्कि बाहर एक्सपोर्ट करके मुनाफा बढ़ाने में लगेगा।",
        "category": "imperialism_and_capital",
        "notes": "Editorial rule: 'अधिशेष पूंजी' (surplus capital) and 'जीवन स्तर'."
    },
    {
        "source": "In these backward countries profits are usually high, for capital is scarce, the price of land is relatively low, wages are low, raw materials are cheap.",
        "target": "इन पिछड़े देशों में मुनाफे की दर आमतौर पर बहुत ऊंची होती है, क्योंकि पूंजी दुर्लभ होती है, जमीन की कीमत अपेक्षाकृत कम होती है, मजदूरी कम होती है और कच्चा माल सस्ता होता है।",
        "bad_literal": "इन पिछड़े देशों में मुनाफा ऊंचा होता है क्योंकि पूंजी कम है, जमीन सस्ती है, मजदूरी कम है और कच्चा माल सस्ता है।",
        "category": "imperialism_and_capital",
        "notes": "Distinguish 'मुनाफे की दर', 'कीमत', and 'मजदूरी'."
    },
    {
        "source": "Monopolist capitalist combines, cartels, syndicates and trusts divide among themselves, first of all, the domestic market, and seize more or less complete possession of the industry of their own country.",
        "target": "एकाधिकारवादी पूंजीवादी गुट, कार्टेल, सिंडिकेट और ट्रस्ट सबसे पहले घरेलू बाजार को आपस में बांटते हैं, और अपने देश के उद्योग पर कमोबेश पूरा कब्जा कर लेते हैं।",
        "bad_literal": "मोनोपॉलिस्ट ग्रुप और कार्टेल पहले घरेलू बाजार बांटते हैं और देश के उद्योग पर कब्जा करते हैं।",
        "category": "imperialism_and_capital",
        "notes": "Use 'घरेलू बाजार' (domestic market) and 'कमोबेश पूरा कब्जा'."
    },
    {
        "source": "But under capitalism the domestic market is inevitably bound up with the foreign market. Capitalism long ago created a world market.",
        "target": "लेकिन पूंजीवाद के तहत घरेलू बाजार अनिवार्य रूप से विदेशी बाजार से जुड़ा होता है। पूंजीवाद ने बहुत पहले ही एक विश्व बाजार का निर्माण कर दिया था।",
        "bad_literal": "लेकिन पूंजीवाद में घरेलू बाजार विदेशी बाजार से बंधा है। पूंजीवाद ने पहले ही विश्व बाजार बनाया था।",
        "category": "imperialism_and_capital",
        "notes": "Use 'घरेलू बाजार' vs 'विदेशी बाजार' and 'विश्व बाजार'."
    },
    {
        "source": "The epoch of the latest stage of capitalism shows us that certain relations between capitalist associations grow up, based on the economic division of the world; while parallel to this, based on the territorial division of the world, of the struggle for colonies, of the \"struggle for spheres of influence\".",
        "target": "पूंजीवाद के नवीनतम चरण का युग हमें दिखाता है कि पूंजीवादी संघों के बीच कुछ ऐसे संबंध विकसित होते हैं जो दुनिया के आर्थिक बंटवारे पर आधारित होते हैं; जबकि इसके समानांतर, दुनिया के क्षेत्रीय बंटवारे, उपनिवेशों के लिए संघर्ष और 'प्रभाव-क्षेत्रों के लिए संघर्ष' पर आधारित संबंध भी उभरते हैं।",
        "bad_literal": "पूंजीवाद का नया युग दिखाता है कि दुनिया के आर्थिक विभाजन पर संबंध बनते हैं और इसके साथ दुनिया के जमीन के बंटवारे और उपनिवेशों की लड़ाई होती है।",
        "category": "imperialism_and_capital",
        "notes": "Use 'दुनिया का आर्थिक बंटवारा' vs 'दुनिया का क्षेत्रीय बंटवारा' and 'प्रभाव-क्षेत्र'."
    },
    {
        "source": "Finance capital and the trusts do not diminish the differences in the rate of growth of the various parts of the world economy; on the contrary, they increase them.",
        "target": "वित्तीय पूंजी और ट्रस्ट विश्व अर्थव्यवस्था के विभिन्न हिस्सों के विकास की दर में अंतर को घटाते नहीं हैं; इसके विपरीत, वे इस अंतर को और बढ़ा देते हैं।",
        "bad_literal": "फाइनेंस कैपिटल और ट्रस्ट दुनिया की अर्थव्यवस्था के बढ़ने के अंतर को कम नहीं करते बल्कि बढ़ाते हैं।",
        "category": "imperialism_and_capital",
        "notes": "Use 'विकास की दर' (rate of growth) and 'इसके विपरीत'."
    },
    {
        "source": "Once the relation of forces is changed, what other solution of the contradiction can be found under capitalism than that of force?",
        "target": "जब शक्तियों का संतुलन बदल जाता है, तो पूंजीवाद के तहत बल प्रयोग के अलावा अन्तर्विरोध का और क्या समाधान तलाशा जा सकता है?",
        "bad_literal": "जब ताकतों का रिश्ता बदलता है तो पूंजीवाद में ताकत के अलावा झगड़े का क्या हल है?",
        "category": "party_and_revolution",
        "notes": "Editorial rule: Use 'अन्तर्विरोध का समाधान' (solution of the contradiction) and 'शक्तियों का संतुलन'."
    },
    {
        "source": "The question is: what means other than war could there be under capitalism to overcome the disparity between the development of productive forces and the accumulation of capital on the one side, and the division of colonies and spheres of influence for finance capital on the other?",
        "target": "प्रश्न यह है कि एक ओर उत्पादक शक्तियों के विकास तथा पूंजी के संचय और दूसरी ओर वित्तीय पूंजी के लिए उपनिवेशों तथा प्रभाव-क्षेत्रों के बंटवारे के बीच की विषमता को पाटने के लिए पूंजीवाद के तहत युद्ध के अलावा अन्य कौन-सा साधन हो सकता है?",
        "bad_literal": "सवाल यह है कि उत्पादक शक्तियों और पूंजी संचय तथा उपनिवेशों के बंटवारे की विषमता को खत्म करने के लिए युद्ध के बिना क्या रास्ता है?",
        "category": "imperialism_and_capital",
        "notes": "Editorial rule: 'उत्पादक शक्तियों का विकास' and 'पूंजी का संचय'."
    },
    {
        "source": "Imperialism is a striving for annexations—this is what the political part of the definition of imperialism amounts to.",
        "target": "साम्राज्यवाद अन्य भूभागों को हड़पने की ललक है—साम्राज्यवाद की राजनीतिक परिभाषा का मूल निचोड़ यही है।",
        "bad_literal": "साम्राज्यवाद हड़पने की कोशिश है, यह साम्राज्यवाद की राजनीतिक परिभाषा है।",
        "category": "imperialism_and_capital",
        "notes": "Precision: 'अन्य भूभागों को हड़पने की ललक' (striving for annexations)."
    },
    {
        "source": "The distinctive feature of imperialism is not the domination of industrial capital, but the domination of finance capital, the striving to annex not only agrarian, but every kind of country.",
        "target": "साम्राज्यवाद की विशिष्ट पहचान औद्योगिक पूंजी का वर्चस्व नहीं, बल्कि वित्तीय पूंजी का वर्चस्व है, न केवल कृषि प्रधान बल्कि हर प्रकार के देश को अपने अधीन करने की ललक है।",
        "bad_literal": "साम्राज्यवाद का लक्षण औद्योगिक पूंजी का राज नहीं बल्कि वित्तीय पूंजी का राज है जो हर देश को हड़पना चाहता है।",
        "category": "imperialism_and_capital",
        "notes": "Contrast: 'औद्योगिक पूंजी का वर्चस्व' vs 'वित्तीय पूंजी का वर्चस्व'."
    },
    {
        "source": "An essential feature of imperialism is the rivalry between several great powers in the striving for hegemony, i.e., for the conquest of territory, not so much directly for themselves as to weaken the adversary and undermine his hegemony.",
        "target": "साम्राज्यवाद का एक अनिवार्य लक्षण आधिपत्य स्थापित करने की होड़ में कई महाशक्तियों के बीच की प्रतिद्वंद्विता है, यानी केवल अपने सीधे लाभ के लिए नहीं बल्कि प्रतिद्वंद्वी को कमजोर करने और उसके आधिपत्य को ध्वस्त करने के लिए क्षेत्रों पर कब्जा करना।",
        "bad_literal": "साम्राज्यवाद का लक्षण बड़ी ताकतों की होड़ है ताकि विरोधी को कमजोर किया जा सके।",
        "category": "imperialism_and_capital",
        "notes": "Use 'आधिपत्य स्थापित करने की होड़' (striving for hegemony) and 'प्रतिद्वंद्विता'."
    },
    {
        "source": "Capitalism has been transformed into imperialism, and for this reason the war on the part of both coalitions of belligerents was an imperialist war, a war for the division of the world, for the sharing of the spoils of capitalism.",
        "target": "पूंजीवाद साम्राज्यवाद में रूपांतरित हो चुका है, और इसी कारण युद्धरत दोनों गठबंधनों की ओर से लड़ा गया युद्ध एक साम्राज्यवादी युद्ध था—दुनिया के बंटवारे और पूंजीवाद की लूट के माले-गनीमत को आपस में बांटने का युद्ध।",
        "bad_literal": "पूंजीवाद साम्राज्यवाद बन गया है और दोनों तरफ का युद्ध साम्राज्यवादी युद्ध था जो दुनिया बांटने के लिए लड़ा गया।",
        "category": "imperialism_and_capital",
        "notes": "Use 'साम्राज्यवादी युद्ध' and 'लूट के माले-गनीमत को बांटना'."
    },
    {
        "source": "The income of the rentiers is five times greater than the income obtained from the foreign trade of the biggest \"trading\" country in the world!",
        "target": "सूदखोरों की आय दुनिया के सबसे बड़े 'व्यापारी' देश के विदेशी व्यापार से प्राप्त होने वाली आय से पांच गुना अधिक है!",
        "bad_literal": "सूदखोरों की कमाई दुनिया के सबसे बड़े व्यापारी देश के विदेश व्यापार की कमाई से पांच गुना ज्यादा है!",
        "category": "imperialism_and_capital",
        "notes": "Use 'सूदखोरों की आय' (income of the rentiers)."
    },
    {
        "source": "This is the essence of imperialism and imperialist parasitism.",
        "target": "यही साम्राज्यवाद और साम्राज्यवादी परजीविता का सारतत्व है।",
        "bad_literal": "यह साम्राज्यवाद और उसके परजीवी होने का सार है।",
        "category": "imperialism_and_capital",
        "notes": "Use 'साम्राज्यवादी परजीविता का सारतत्व'."
    },
    {
        "source": "For that reason the term \"rentier state\", or usurer state, is becoming of common use in the economic literature that deals with imperialism.",
        "target": "इसी कारण से साम्राज्यवाद का विवेचन करने वाले आर्थिक साहित्य में 'सूदखोर राज्य' शब्द का प्रयोग आम होता जा रहा है।",
        "bad_literal": "इसलिए सूदखोर राज्य का नाम साम्राज्यवाद के साहित्य में आम हो रहा है।",
        "category": "imperialism_and_capital",
        "notes": "Use 'सूदखोर राज्य' (rentier state or usurer state)."
    },
    {
        "source": "The world has become divided into a handful of usurer states and a vast majority of debtor states.",
        "target": "दुनिया मुट्ठी भर सूदखोर राज्यों और भारी बहुसंख्यक कर्जदार राज्यों के बीच बंट चुकी है।",
        "bad_literal": "दुनिया कुछ सूदखोर देशों और ज्यादातर कर्जदार देशों में बंट गई है।",
        "category": "imperialism_and_capital",
        "notes": "Stark contrast: 'मुट्ठी भर सूदखोर राज्य' vs 'भारी बहुसंख्यक कर्जदार राज्य'."
    }
]

def main():
    tm = TranslationMemory(storage_path=os.path.join(BASE_DIR, "data", "tm_store.json"))
    count = tm.import_pairs(extra_pairs)
    print(f"Added {count} additional Lenin political economy sentence pairs.")
    print(f"Total Translation Memory pairs in studio now: {len(tm.get_all())}")

if __name__ == "__main__":
    main()
