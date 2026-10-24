#!/usr/bin/env python3
"""
Batch 3: The 5 Basic Features of Imperialism & State Monopoly Capitalism (17 pairs).
Brings total Translation Memory to 100 pairs.
"""

import os, sys

BASE_DIR = "/Users/athakur/Documents/General Things/translation-style-studio"
if BASE_DIR not in sys.path:
    sys.path.insert(0, BASE_DIR)

from app.core.memory import TranslationMemory

batch3_pairs = [
    {
        "source": "If it were necessary to give the briefest possible definition of imperialism we should have to say that imperialism is the monopoly stage of capitalism.",
        "target": "यदि साम्राज्यवाद की संक्षिप्ततम संभव परिभाषा देना आवश्यक हो, तो हमें कहना होगा कि साम्राज्यवाद पूंजीवाद का एकाधिकारवादी चरण है।",
        "bad_literal": "अगर साम्राज्यवाद की सबसे छोटी परिभाषा देनी हो तो हमें कहना चाहिए कि यह पूंजीवाद का एकाधिकार स्तर है।",
        "category": "imperialism_definition",
        "notes": "Classic definition: 'पूंजीवाद का एकाधिकारवादी चरण' (monopoly stage of capitalism)."
    },
    {
        "source": "Such a definition would include what is most important, for, on the one hand, finance capital is the bank capital of a few very big monopolist banks, merged with the capital of the monopolist combines of industrialists.",
        "target": "ऐसी परिभाषा में सबसे महत्वपूर्ण बात शामिल होगी, क्योंकि एक ओर, वित्तीय पूंजी कुछ विशाल एकाधिकारवादी बैंकों की बैंक-पूंजी है, जो उद्योगपतियों के एकाधिकारवादी गुटों की पूंजी में विलीन हो चुकी है।",
        "bad_literal": "ऐसी परिभाषा में सबसे बड़ा सच होगा क्योंकि वित्तीय पूंजी बैंक पूंजी है जो उद्योगपतियों से मिली है।",
        "category": "imperialism_definition",
        "notes": "Use 'विलीन हो चुकी है' for 'merged with'."
    },
    {
        "source": "And, on the other hand, the division of the world is the transition from a colonial policy which has extended without hindrance to territories unseized by any capitalist power, to a colonial policy of the monopolistic possession of the territory of the globe.",
        "target": "और दूसरी ओर, दुनिया का बंटवारा उस औपनिवेशिक नीति से एक संक्रमण है जो किसी भी पूंजीवादी शक्ति द्वारा अनधिकृत क्षेत्रों तक बिना किसी बाधा के फैली थी, उस औपनिवेशिक नीति की ओर जिसके तहत पूरी दुनिया के भूभाग पर एकाधिकारवादी कब्जा कायम कर लिया गया है।",
        "bad_literal": "दूसरी ओर दुनिया का बंटवारा उस औपनिवेशिक नीति से उस नीति में बदलाव है जो पूरी दुनिया पर एकाधिकार रखती है।",
        "category": "imperialism_definition",
        "notes": "Contrast: 'अनधिकृत क्षेत्र' vs 'एकाधिकारवादी कब्जा'."
    },
    {
        "source": "We must give a definition of imperialism that will include the following five of its basic features.",
        "target": "हमें साम्राज्यवाद की ऐसी परिभाषा देनी चाहिए जिसमें उसके निम्नलिखित पांच बुनियादी लक्षण शामिल हों।",
        "bad_literal": "हमें साम्राज्यवाद की ऐसी परिभाषा देनी चाहिए जिसमें पांच लक्षण हों।",
        "category": "imperialism_definition",
        "notes": "Formal: 'पांच बुनियादी लक्षण' (five basic features)."
    },
    {
        "source": "First: the concentration of production and capital has developed to such a high stage that it has created monopolies which play a decisive role in economic life.",
        "target": "पहला: उत्पादन और पूंजी का संकेंद्रण इतने उच्च स्तर तक विकसित हो चुका है कि उसने ऐसे एकाधिकारों का निर्माण किया है जो आर्थिक जीवन में निर्णायक भूमिका निभाते हैं।",
        "bad_literal": "पहला: उत्पादन और पूंजी का जमाव इतना बढ़ गया है कि उसने एकाधिकार बना दिया है जो आर्थिक जीवन तय करते हैं।",
        "category": "imperialism_definition",
        "notes": "First feature of imperialism: 'निर्णायक भूमिका निभाते हैं'."
    },
    {
        "source": "Second: the merging of bank capital with industrial capital, and the creation, on the basis of this \"finance capital\", of a financial oligarchy.",
        "target": "दूसरा: औद्योगिक पूंजी के साथ बैंक-पूंजी का विलय, और इस 'वित्तीय पूंजी' के आधार पर एक वित्तीय अल्पतंत्र का निर्माण।",
        "bad_literal": "दूसरा: बैंक पूंजी का उद्योग पूंजी से मिलना और वित्तीय पूंजी पर वित्तीय कुलीनतंत्र का बनना।",
        "category": "imperialism_definition",
        "notes": "Second feature of imperialism: 'औद्योगिक पूंजी के साथ बैंक-पूंजी का विलय' and 'वित्तीय अल्पतंत्र'."
    },
    {
        "source": "Third: the export of capital as distinguished from the export of commodities acquires exceptional importance.",
        "target": "तीसरा: वस्तुओं के निर्यात से भिन्न, पूंजी का निर्यात असाधारण महत्व प्राप्त कर लेता है।",
        "bad_literal": "तीसरा: माल के निर्यात से अलग पूंजी का निर्यात बहुत महत्वपूर्ण हो जाता है।",
        "category": "imperialism_definition",
        "notes": "Third feature of imperialism: 'वस्तुओं के निर्यात से भिन्न, पूंजी का निर्यात'."
    },
    {
        "source": "Fourth: the formation of international monopolist capitalist combines which share the world among themselves.",
        "target": "चौथा: अंतर्राष्ट्रीय एकाधिकारवादी पूंजीवादी गुटों का गठन, जो दुनिया को आपस में बांटते हैं।",
        "bad_literal": "चौथा: अंतर्राष्ट्रीय एकाधिकारवादी पूंजीवादी समूहों का बनना जो दुनिया को बांटते हैं।",
        "category": "imperialism_definition",
        "notes": "Fourth feature of imperialism: 'अंतर्राष्ट्रीय एकाधिकारवादी पूंजीवादी गुट'."
    },
    {
        "source": "Fifth: the territorial division of the whole world among the biggest capitalist powers is completed.",
        "target": "पांचवां: सबसे बड़ी पूंजीवादी महाशक्तियों के बीच पूरी दुनिया का क्षेत्रीय बंटवारा पूरा हो चुका है।",
        "bad_literal": "पांचवां: सबसे बड़ी पूंजीवादी ताकतों के बीच पूरी दुनिया की जमीन का विभाजन पूरा हो गया है।",
        "category": "imperialism_definition",
        "notes": "Fifth feature of imperialism: 'पूरी दुनिया का क्षेत्रीय बंटवारा पूरा हो चुका है'."
    },
    {
        "source": "Imperialism is capitalism at that stage of development at which the dominance of monopolies and finance capital is established.",
        "target": "साम्राज्यवाद पूंजीवाद के विकास का वह चरण है जिसमें एकाधिकारों और वित्तीय पूंजी का वर्चस्व स्थापित हो चुका है।",
        "bad_literal": "साम्राज्यवाद पूंजीवाद का वह स्तर है जहां एकाधिकार और वित्तीय पूंजी का राज कायम है।",
        "category": "imperialism_definition",
        "notes": "Consolidated summary definition."
    },
    {
        "source": "The economic essence of imperialism is the substitution of monopoly for free competition.",
        "target": "साम्राज्यवाद का आर्थिक सारतत्व मुक्त प्रतिस्पर्धा की जगह एकाधिकार की स्थापना है।",
        "bad_literal": "साम्राज्यवाद का आर्थिक सार खुली प्रतियोगिता की जगह एकाधिकार का आना है।",
        "category": "imperialism_definition",
        "notes": "Precision: 'मुक्त प्रतिस्पर्धा की जगह एकाधिकार की स्थापना'."
    },
    {
        "source": "Free competition is the basic feature of capitalism, and of commodity production generally; monopoly is the exact opposite of free competition.",
        "target": "मुक्त प्रतिस्पर्धा पूंजीवाद और आम तौर पर जिंस-उत्पादन का बुनियादी लक्षण है; एकाधिकार मुक्त प्रतिस्पर्धा का ठीक विलोम है।",
        "bad_literal": "खुली प्रतियोगिता पूंजीवाद और माल उत्पादन का लक्षण है; एकाधिकार खुली प्रतियोगिता का उल्टा है।",
        "category": "imperialism_definition",
        "notes": "Distinction: 'जिंस-उत्पादन' (commodity production) vs 'मुक्त प्रतिस्पर्धा' (free competition)."
    },
    {
        "source": "At the same time the monopolies, which have grown out of free competition, do not eliminate the latter, but exist above it and alongside it, and thereby give rise to a number of very acute, intense antagonisms, frictions and conflicts.",
        "target": "इसके साथ ही, मुक्त प्रतिस्पर्धा से उपजे एकाधिकार उसे पूरी तरह समाप्त नहीं करते, बल्कि उसके ऊपर और उसके समानांतर मौजूद रहते हैं, और इस तरह अत्यंत तीखे, तीव्र विरोधों, तनावों और संघर्षों को जन्म देते हैं।",
        "bad_literal": "उसी समय एकाधिकार जो खुली प्रतियोगिता से आए हैं उसे खत्म नहीं करते बल्कि उसके साथ रहते हैं और झगड़े पैदा करते हैं।",
        "category": "imperialism_definition",
        "notes": "Dialectical relationship: 'उसके ऊपर और उसके समानांतर मौजूद रहना'."
    },
    {
        "source": "Monopoly is the transition from capitalism to a higher system.",
        "target": "एकाधिकार पूंजीवाद से एक उच्चतर सामाजिक व्यवस्था की ओर संक्रमण है।",
        "bad_literal": "एकाधिकार पूंजीवाद से ऊंचे सिस्टम की तरफ बदलाव है।",
        "category": "historical_materialism",
        "notes": "Historical category: 'उच्चतर सामाजिक व्यवस्था की ओर संक्रमण'."
    },
    {
        "source": "Production becomes social, but appropriation remains private.",
        "target": "उत्पादन सामाजिक बन जाता है, लेकिन हथियाना (स्वामित्व) निजी बना रहता है।",
        "bad_literal": "उत्पादन सामाजिक होता है लेकिन कब्जा निजी रहता है।",
        "category": "historical_materialism",
        "notes": "Marxian fundamental contradiction: 'उत्पादन सामाजिक बन जाता है, लेकिन स्वामित्व निजी बना रहता है'."
    },
    {
        "source": "The social means of production remain the private property of a few.",
        "target": "उत्पादन के सामाजिक साधन मुट्ठी भर लोगों की निजी संपत्ति बने रहते हैं।",
        "bad_literal": "उत्पादन के सामाजिक साधन कुछ लोगों की निजी प्रॉपर्टी रहते हैं।",
        "category": "historical_materialism",
        "notes": "Editorial rule: 'उत्पादन के सामाजिक साधन' (social means of production)."
    },
    {
        "source": "The general framework of formally recognised free competition remains, and the yoke of a few monopolists on the rest of the population becomes a hundred times heavier, more burdensome and intolerable.",
        "target": "औपचारिक रूप से मान्यता प्राप्त मुक्त प्रतिस्पर्धा का सामान्य ढांचा बना रहता है, और शेष आबादी पर मुट्ठी भर एकाधिकारवादियों का जुआ सौ गुना अधिक भारी, अधिक कष्टदायक और असहनीय हो जाता है।",
        "bad_literal": "मान्यता प्राप्त खुली प्रतियोगिता का ढांचा रहता है और लोगों पर कुछ एकाधिकारों का बोझ सौ गुना भारी हो जाता है।",
        "category": "imperialism_definition",
        "notes": "Use 'मुट्ठी भर एकाधिकारवादियों का जुआ' for 'yoke of a few monopolists'."
    }
]

def main():
    tm = TranslationMemory(storage_path=os.path.join(BASE_DIR, "data", "tm_store.json"))
    count = tm.import_pairs(batch3_pairs)
    print(f"Added {count} pairs from Batch 3 (Lenin's Five Features of Imperialism).")
    print(f"🎉 Total Translation Memory pairs in studio now: {len(tm.get_all())}")

if __name__ == "__main__":
    main()
