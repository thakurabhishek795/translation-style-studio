#!/usr/bin/env python3
"""
Aligner script for Lenin's 'What Is to Be Done?' and 'Imperialism'.
Generates high-quality bilingual sentence pairs for Translation Memory.
"""

import os
import sys
import re
import json

BASE_DIR = "/Users/athakur/Documents/General Things/translation-style-studio"
if BASE_DIR not in sys.path:
    sys.path.insert(0, BASE_DIR)

from app.core.memory import TranslationMemory

def clean_text(text: str) -> str:
    text = re.sub(r'\s+', ' ', text)
    return text.strip()

def extract_pairs() -> list:
    pairs = []
    
    # -------------------------------------------------------------------
    # PART 1: 'What Is to Be Done?' (1902) - Chapter 1, Section 1.1
    # -------------------------------------------------------------------
    witbd_pairs = [
        {
            "source": "\"Freedom of criticism\" is undoubtedly the most fashionable slogan at the present time, and the one most frequently employed in the controversies between socialists and democrats in all countries.",
            "target": "'आलोचना की स्वतंत्रता' निस्संदेह मौजूदा समय का सबसे फैशनेबल नारा है। यह सभी देशों और समाजवादियों और जनवादियों के बीच चल रहे विवादों में सर्वाधिक इस्तेमाल किया जाने वाला मुद्दा है।",
            "bad_literal": "आलोचना की आजादी बिना शक सबसे फैशनेबल नारा है जो समाजवादियों के बीच इस्तेमाल होता है।",
            "category": "party_and_revolution",
            "notes": "Use 'आलोचना की स्वतंत्रता' for 'freedom of criticism'; avoid casual 'आजादी'."
        },
        {
            "source": "At first sight, nothing would appear to be more strange than the solemn appeals to freedom of criticism made by one of the parties to the dispute.",
            "target": "विवाद में शामिल पार्टियों में से कोई एक अगर आलोचना की स्वतंत्रता के लिए गंभीर अपील करे तो पहली नजर में इससे ज्यादा विचित्र बात कोई और नजर नहीं आएगी।",
            "bad_literal": "पहली नजर में विवाद की किसी पार्टी द्वारा आलोचना की आजादी की गंभीर अपील से अजीब कुछ नहीं लगेगा।",
            "category": "party_and_revolution",
            "notes": "Natural Hindi sentence construction with condition 'अगर... तो'."
        },
        {
            "source": "Have voices been raised in the advanced parties against the constitutional law of the majority of European countries which guarantees freedom to science and scientific investigation?",
            "target": "बहुतेरे यूरोपीय देशों के संवैधानिक कानून, विज्ञान और वैज्ञानिक अन्वेषणों के लिए स्वतंत्रता की गारंटी करते हैं। क्या इन कानूनों के खिलाफ इन देशों की अग्रणी पार्टियों के भीतर आवाज उठाई गई है?",
            "bad_literal": "क्या उन यूरोपीय देशों के संविधान के खिलाफ आवाज उठाई गई है जो विज्ञान को आजादी देते हैं?",
            "category": "party_and_revolution",
            "notes": "Split long periodic English questions into an informative premise and a clear query in Hindi."
        },
        {
            "source": "\"Something must be wrong here,\" will be the comment of the onlooker who has heard this fashionable slogan repeated at every turn but has not yet penetrated the essence of the disagreement among the disputants.",
            "target": "'यहां कुछ न कुछ गलत निश्चित रूप से है।' यही किसी भी उस दर्शक की टिप्पणी होगी, जिसने आलोचना की स्वतंत्रता के इस फैशनेबल नारे को सुना होगा लेकिन विवादों के सारतत्व को नहीं समझा होगा।",
            "bad_literal": "यहाँ कुछ गलत होना चाहिए, यह उस देखने वाले की टिप्पणी होगी जिसने यह नारा सुना है।",
            "category": "party_and_revolution",
            "notes": "Use 'सारतत्व' for 'essence of the disagreement'."
        },
        {
            "source": "In fact, it is no secret for anyone that two trends have taken form in present-day international Social-Democracy.",
            "target": "वास्तव में यह किसी के लिए रहस्य नहीं है कि दो प्रवृत्तियों ने मौजूदा अंतर्राष्ट्रीय सामाजिक जनवाद में अपना रूप ले लिया है।",
            "bad_literal": "सच में किसी के लिए गुप्त नहीं है कि आज के सोशल डेमोक्रेसी में दो धाराएं बन गई हैं।",
            "category": "party_and_revolution",
            "notes": "Use 'सामाजिक जनवाद' for 'Social-Democracy'."
        },
        {
            "source": "The conflict between these trends now flares up in a bright flame and now dies down and smoulders under the ashes of imposing \"truce resolutions\".",
            "target": "इन प्रवृत्तियों के बीच का संघर्ष कभी भड़क उठता है और कभी 'संघर्ष-विराम प्रस्तावों' की राख के नीचे सुलगता रहता है।",
            "bad_literal": "इन धाराओं का झगड़ा कभी आग बनता है और कभी शांति प्रस्तावों की राख में सुलगता है।",
            "category": "party_and_revolution",
            "notes": "Metaphorical balance: 'राख के नीचे सुलगना' for 'smoulders under the ashes'."
        },
        {
            "source": "The essence of the \"new\" trend, which adopts a \"critical\" attitude towards \"obsolete dogmatic\" Marxism, has been clearly enough presented by Bernstein and demonstrated by Millerand.",
            "target": "'नई' प्रवृत्ति का सारतत्व 'पुरातन कट्टरपंथी' मार्क्सवाद के प्रति आलोचनात्मक रुख अख्तियार करना है, जिसे बर्नस्टीन ने पेश किया और मिलेरां ने व्यवहार में प्रदर्शित किया।",
            "bad_literal": "नई धारा का सार जो पुराने मार्क्सवाद पर आलोचनात्मक रुख लेती है बर्नस्टीन द्वारा दिखाया गया है।",
            "category": "party_and_revolution",
            "notes": "Formal terminology: 'सारतत्व' and 'रुख अख्तियार करना'."
        },
        {
            "source": "Social-Democracy must change from a party of social revolution into a democratic party of social reforms.",
            "target": "सामाजिक जनवाद को सामाजिक क्रांति के लिए समर्पित पार्टी से बदलकर सामाजिक सुधारों की जनवादी पार्टी बन जाना चाहिए।",
            "bad_literal": "सोशल डेमोक्रेसी को सामाजिक क्रांति की पार्टी से सामाजिक सुधार की पार्टी में बदलना चाहिए।",
            "category": "party_and_revolution",
            "notes": "Editorial rule: Keep 'सामाजिक क्रांति' and 'सामाजिक सुधार' strictly distinct."
        },
        {
            "source": "Bernstein has surrounded this political demand with a whole battery of well-attuned \"new\" arguments and reasonings.",
            "target": "बर्नस्टीन इस राजनीतिक मांग को सुव्यवस्थित 'नए' तर्कों और विचारों की पूरी श्रृंखला से लैस करते हैं।",
            "bad_literal": "बर्नस्टीन ने इस राजनीतिक मांग को नए तर्कों की बैटरी से घेर लिया है।",
            "category": "party_and_revolution",
            "notes": "Avoid literal calque 'तर्कों की बैटरी'; use 'तर्कों की पूरी श्रृंखला से लैस करना'."
        },
        {
            "source": "Denied was the possibility of putting socialism on a scientific basis and of demonstrating its necessity and inevitability from the point of view of the materialist conception of history.",
            "target": "समाजवाद को वैज्ञानिक आधार देने और इतिहास के भौतिकवादी दृष्टिकोण से उसकी आवश्यकता व अनिवार्यता सिद्ध करने की संभावना से ही इनकार कर दिया गया।",
            "bad_literal": "समाजवाद को विज्ञान पर रखने और भौतिकवादी इतिहास से इसकी जरूरत दिखाने से मना किया गया।",
            "category": "historical_materialism",
            "notes": "Use 'इतिहास का भौतिकवादी दृष्टिकोण' (materialist conception of history)."
        },
        {
            "source": "Denied was the fact of growing impoverishment, the process of proletarianisation, and the intensification of capitalist contradictions.",
            "target": "बढ़ती कंगाली के तथ्य, सर्वहाराकरण की प्रक्रिया और पूंजीवादी अन्तर्विरोधों के तीव्र होने की वास्तविकता को नकार दिया गया।",
            "bad_literal": "गरीबी बढ़ने, सर्वहारा बनने और पूंजीवादी झगड़ों के सच को मना किया गया।",
            "category": "economics",
            "notes": "Editorial rule: Use 'सर्वहाराकरण' (proletarianisation) and 'पूंजीवादी अन्तर्विरोध' (capitalist contradictions)."
        },
        {
            "source": "The very concept \"ultimate aim\" was declared to be unsound, and the idea of the dictatorship of the proletariat was completely rejected.",
            "target": "'अंतिम लक्ष्य' की अवधारणा को ही निरर्थक घोषित कर दिया गया और सर्वहारा अधिनायकत्व के विचार को पूरी तरह खारिज कर दिया गया।",
            "bad_literal": "आखिरी मकसद के विचार को बेकार कहा गया और सर्वहारा की तानाशाही को हटा दिया गया।",
            "category": "party_and_revolution",
            "notes": "Editorial rule: Use 'सर्वहारा अधिनायकत्व' for 'dictatorship of the proletariat'."
        },
        {
            "source": "Denied was the antithesis in principle between liberalism and socialism. Denied was the theory of the class struggle, on the alleged ground that it could not be applied to a strictly democratic society.",
            "target": "उदारतावाद और समाजवाद के बीच के बुनियादी सैद्धांतिक भेद को नकार दिया गया। वर्ग-संघर्ष के सिद्धांत को इस तथाकथित आधार पर खारिज किया गया कि इसे विशुद्ध लोकतांत्रिक समाज पर लागू नहीं किया जा सकता।",
            "bad_literal": "उदारवाद और समाजवाद के विरोध को नकारा गया और वर्ग संघर्ष को अलोकतांत्रिक माना गया।",
            "category": "party_and_revolution",
            "notes": "Use 'वर्ग-संघर्ष' (class struggle) and 'बुनियादी सैद्धांतिक भेद'."
        },
        {
            "source": "Thus, the demand for a decisive turn from revolutionary Social-Democracy to bourgeois social-reformism was accompanied by a no less decisive turn towards bourgeois criticism of all the fundamental ideas of Marxism.",
            "target": "इस प्रकार, क्रांतिकारी सामाजिक जनवाद से बुर्जुआ सामाजिक-सुधारवाद की ओर निर्णायक मोड़ की मांग के साथ-साथ मार्क्सवाद के सभी बुनियादी विचारों की बुर्जुआ आलोचना की ओर भी उतना ही निर्णायक मोड़ आया।",
            "bad_literal": "इसलिए क्रांतिकारी समाजवाद से बुर्जुआ सुधार की मांग मार्क्सवाद की आलोचना के साथ आई।",
            "category": "party_and_revolution",
            "notes": "Editorial rule: 'बुर्जुआ सामाजिक-सुधारवाद' vs 'क्रांतिकारी सामाजिक जनवाद'."
        },
        {
            "source": "If Social-Democracy, in essence, is merely a party of reform, then not only has a socialist the right to join a bourgeois cabinet, but he must always strive to do so.",
            "target": "यदि सामाजिक जनवाद मूलतः केवल सुधारों की पार्टी है, तो किसी समाजवादी को न केवल बुर्जुआ मंत्रिमंडल में शामिल होने का अधिकार है, बल्कि उसे हमेशा ऐसा करने का प्रयास करना चाहिए।",
            "bad_literal": "अगर सोशल डेमोक्रेसी सिर्फ सुधार की पार्टी है तो समाजवादी को सरकार में जाना चाहिए।",
            "category": "party_and_revolution",
            "notes": "Use 'बुर्जुआ मंत्रिमंडल' for 'bourgeois cabinet'."
        },
        {
            "source": "Why should he not remain in the cabinet even after the shooting-down of workers by gendarmes has exposed the real nature of the democratic collaboration of classes?",
            "target": "उसे मंत्रिमंडल में तब भी क्यों नहीं बने रहना चाहिए जब पुलिस द्वारा श्रमिकों पर गोलीबारी ने वर्गों के लोकतांत्रिक सहयोग के वास्तविक चरित्र को उजागर कर दिया हो?",
            "bad_literal": "उसे कैबिनेट में क्यों नहीं रहना चाहिए जब पुलिस ने मजदूरों को गोली मार दी?",
            "category": "party_and_revolution",
            "notes": "Use 'वर्गों का सहयोग' (collaboration of classes)."
        },
        {
            "source": "He who does not deliberately close his eyes cannot fail to see that the new \"critical\" trend in socialism is nothing more and nothing less than a new variety of opportunism.",
            "target": "जो जानबूझकर अपनी आंखें बंद नहीं कर लेता, वह साफ-साफ देख सकता है कि समाजवाद में यह नई 'आलोचनात्मक' प्रवृत्ति अवसरवाद की एक नई किस्म से न तो कुछ कम है और न अधिक।",
            "bad_literal": "जो आंख बंद नहीं करता वह देख सकता है कि समाजवाद में आलोचना अवसरवाद का नया रूप है।",
            "category": "political_tendencies",
            "notes": "Editorial rule: Use 'अवसरवाद' for 'opportunism'."
        },
        {
            "source": "And if we judge people, not by the glittering clothes they deck themselves in, not by the imposing titles they give themselves, but by their actions, it will be clear that \"freedom of criticism\" means' freedom for an opportunist trend in Social-Democracy.",
            "target": "और यदि हम लोगों का मूल्यांकन उनके दिखावटी कपड़ों या भव्य उपाधियों से नहीं, बल्कि उनके कर्मों से करें, तो स्पष्ट हो जाएगा कि 'आलोचना की स्वतंत्रता' का अर्थ सामाजिक जनवाद में अवसरवादी प्रवृत्ति की स्वतंत्रता है।",
            "bad_literal": "अगर हम लोगों को उनके कपड़ों और नाम से नहीं काम से देखें तो आलोचना की आजादी अवसरवाद की आजादी है।",
            "category": "party_and_revolution",
            "notes": "Preserve rhetorical balance: 'दिखावटी कपड़ों या भव्य उपाधियों'."
        },
        {
            "source": "\"Freedom\" is a grand word, but under the banner of freedom for industry the most predatory wars were waged; under the banner of freedom of labour, the working people were robbed.",
            "target": "'स्वतंत्रता' एक महान शब्द है, लेकिन उद्योग की स्वतंत्रता के बैनर तले सर्वाधिक लुटेरे युद्ध लड़े गए; श्रम की स्वतंत्रता के बैनर तले मेहनतकश जनता को लूटा गया।",
            "bad_literal": "आजादी एक बड़ा शब्द है लेकिन उद्योग की आजादी में युद्ध लड़े गए और काम की आजादी में मजदूर लूटे गए।",
            "category": "philosophy",
            "notes": "Distinguish 'श्रम की स्वतंत्रता' from 'मेहनतकश जनता'."
        },
        {
            "source": "Those who are really convinced that they have made progress in science would not demand freedom for the new views to continue side by side with the old, but the substitution of the new views for the old.",
            "target": "जिन लोगों को सचमुच विश्वास है कि उन्होंने विज्ञान को आगे बढ़ाया है, वे पुराने विचारों के साथ नए विचारों के बने रहने की स्वतंत्रता नहीं मांगेंगे, बल्कि पुराने की जगह नए विचारों की स्थापना की मांग करेंगे।",
            "bad_literal": "जो विज्ञान में तरक्की मानते हैं वे पुराने के साथ नया नहीं मांगेंगे बल्कि नया लाएंगे।",
            "category": "philosophy",
            "notes": "Precision: 'पुराने की जगह नए विचारों की स्थापना'."
        },
        {
            "source": "We are marching in a compact group along a precipitous and difficult path, firmly holding each other by the hand.",
            "target": "हम एक-दूसरे का हाथ मजबूती से थामे हुए, एक दुर्गम और कठिन रास्ते पर एक सुगठित समूह के रूप में आगे बढ़ रहे हैं।",
            "bad_literal": "हम एक दूसरे का हाथ पकड़कर कठिन रास्ते पर एक ग्रुप में चल रहे हैं।",
            "category": "party_and_revolution",
            "notes": "Lenin's famous marsh passage: 'सुगठित समूह' for 'compact group'."
        },
        {
            "source": "We are surrounded on all sides by enemies, and we have to advance almost constantly under their fire.",
            "target": "हम चारों तरफ से दुश्मनों से घिरे हुए हैं, और हमें लगभग लगातार उनकी गोलीबारी के साए में आगे बढ़ना है।",
            "bad_literal": "हम चारों ओर दुश्मनों से घिरे हैं और हमें उनकी आग में आगे बढ़ना है।",
            "category": "party_and_revolution",
            "notes": "Cadence: 'गोलीबारी के साए में आगे बढ़ना'."
        },
        {
            "source": "We have combined, by a freely adopted decision, for the purpose of fighting the enemy, and not of stumbling into the neighbouring marsh.",
            "target": "हम अपनी स्वतंत्र इच्छा से लिए गए निर्णय के तहत एकजुट हुए हैं ताकि दुश्मन से मुकाबला कर सकें, न कि बगल के दलदल में फिसलकर जा गिरें।",
            "bad_literal": "हमने दुश्मन से लड़ने का फैसला किया है पास के दलदल में गिरने का नहीं।",
            "category": "party_and_revolution",
            "notes": "Metaphor: 'बगल के दलदल में फिसलना' for 'stumbling into the neighbouring marsh'."
        },
        {
            "source": "And now some among us begin to cry out: Let us go into the marsh! And when we begin to shame them, they retort: What backward people you are!",
            "target": "और अब हममें से कुछ लोग चिल्लाने लगे हैं: चलो दलदल में चलते हैं! और जब हम उन्हें शर्मसार करते हैं, तो वे पलटकर कहते हैं: तुम कितने पिछड़े लोग हो!",
            "bad_literal": "अब कुछ लोग चिल्लाते हैं दलदल में चलो और जब हम टोकते हैं तो कहते हैं तुम पिछड़े हो!",
            "category": "party_and_revolution",
            "notes": "Vivid dialogue translation retaining Lenin's polemical bite."
        },
        {
            "source": "In fact, we think that the marsh is your proper place, and we are prepared to render you every assistance to get there.",
            "target": "वास्तव में, हमारा मानना है कि वह दलदल ही आपकी सही जगह है, और हम आपको वहां पहुंचाने के लिए हर संभव सहायता देने को तैयार हैं।",
            "bad_literal": "सच में हम सोचते हैं दलदल आपकी जगह है और हम वहां जाने में मदद करेंगे।",
            "category": "party_and_revolution",
            "notes": "Satirical register: 'हर संभव सहायता देने को तैयार हैं'."
        },
        {
            "source": "Only let go of our hands, don't clutch at us and don't besmirch the grand word freedom, for we too are \"free\" to go where we please, free to fight not only against the marsh, but also against those who are turning towards the marsh!",
            "target": "बस हमारा हाथ छोड़ दीजिए, हमें मत पकड़िए और स्वतंत्रता जैसे महान शब्द को कलंकित मत कीजिए, क्योंकि हम भी वहां जाने के लिए 'स्वतंत्र' हैं जहां हम चाहें—न केवल दलदल के खिलाफ लड़ने के लिए, बल्कि उनकी ओर भी मुड़ने वालों के खिलाफ लड़ने के लिए जो दलदल का रुख कर रहे हैं!",
            "bad_literal": "सिर्फ हमारा हाथ छोड़ो, हमें मत पकड़ो और आजादी शब्द को गंदा मत करो क्योंकि हम भी दलदल से लड़ने को आजाद हैं!",
            "category": "party_and_revolution",
            "notes": "Climactic rhetorical sentence of Section 1.1."
        }
    ]
    pairs.extend(witbd_pairs)

    # -------------------------------------------------------------------
    # PART 2: 'Imperialism, the Highest Stage of Capitalism' (1916)
    # -------------------------------------------------------------------
    imp_pairs = [
        {
            "source": "The enormous growth of industry and the remarkably rapid concentration of production in ever-larger enterprises are one of the most characteristic features of capitalism.",
            "target": "उद्योग का भारी विस्तार और लगातार बड़े होते उद्यमों में उत्पादन का अत्यधिक तीव्र संकेंद्रण पूंजीवाद की सबसे विशिष्ट विशेषताओं में से एक है।",
            "bad_literal": "उद्योग की बड़ी वृद्धि और बड़े उद्यमों में उत्पादन का तेज जमाव पूंजीवाद का लक्षण है।",
            "category": "imperialism_and_capital",
            "notes": "Use 'उत्पादन का संकेंद्रण' for 'concentration of production'."
        },
        {
            "source": "Concentration of production, however, is much more intense than the concentration of workers, since labour in the large enterprises is much more productive.",
            "target": "उत्पादन का संकेंद्रण श्रमिकों के संकेंद्रण की तुलना में कहीं अधिक तीव्र होता है, क्योंकि बड़े उद्यमों में श्रम कहीं अधिक उत्पादक होता है।",
            "bad_literal": "उत्पादन का जमाव मजदूरों के जमाव से ज्यादा है क्योंकि बड़े कारखानों में काम ज्यादा उत्पादक है।",
            "category": "imperialism_and_capital",
            "notes": "Contrast: 'उत्पादन का संकेंद्रण' vs 'श्रमिकों का संकेंद्रण'."
        },
        {
            "source": "Tens of thousands of huge enterprises are everything; millions of small ones are nothing.",
            "target": "हजारों विशाल उद्यम ही सब कुछ हैं; लाखों छोटे उद्यमों का कोई अस्तित्व नहीं रह जाता।",
            "bad_literal": "दस हजार बड़े उद्यम सब कुछ हैं, लाखों छोटे कुछ नहीं हैं।",
            "category": "imperialism_and_capital",
            "notes": "Epigrammatic formulation."
        },
        {
            "source": "At a certain stage of its development, concentration, by itself, leads directly to monopoly.",
            "target": "अपने विकास के एक निश्चित चरण में संकेंद्रण स्वतः ही सीधे एकाधिकार की ओर ले जाता है।",
            "bad_literal": "अपने विकास के एक स्तर पर जमाव सीधे मोनोपॉली की तरफ जाता है।",
            "category": "imperialism_and_capital",
            "notes": "Core thesis of Imperialism: 'संकेंद्रण स्वतः ही एकाधिकार की ओर ले जाता है'."
        },
        {
            "source": "For a score or so of gigantic enterprises can easily arrive at an agreement, and on the other hand, the hindrance to competition, the tendency towards monopoly, arises from the huge size of the enterprises.",
            "target": "क्योंकि लगभग दो दर्जन विशाल उद्यम आसानी से किसी समझौते पर पहुंच सकते हैं, और दूसरी ओर, उद्यमों का विशाल आकार ही प्रतिस्पर्धा में बाधा और एकाधिकार की प्रवृत्ति को जन्म देता है।",
            "bad_literal": "क्योंकि बीस बड़े उद्यम आसानी से समझौता कर सकते हैं और प्रतिस्पर्धा रुकने से एकाधिकार आता है।",
            "category": "imperialism_and_capital",
            "notes": "Use 'एकाधिकार की प्रवृत्ति' (tendency towards monopoly)."
        },
        {
            "source": "This transformation of competition into monopoly is one of the most important—if not the most important—phenomena of modern capitalist economy.",
            "target": "प्रतिस्पर्धा का एकाधिकार में यह रूपांतरण आधुनिक पूंजीवादी अर्थव्यवस्था की सबसे महत्वपूर्ण—यदि सर्वाधिक महत्वपूर्ण नहीं तो—परिघटनाओं में से एक है।",
            "bad_literal": "कंपटीशन का मोनोपॉली में बदलना आधुनिक पूंजीवादी अर्थव्यवस्था की सबसे बड़ी घटना है।",
            "category": "imperialism_and_capital",
            "notes": "Use 'प्रतिस्पर्धा का एकाधिकार में रूपांतरण'."
        },
        {
            "source": "The rise of monopolies, as the result of the concentration of production, is a general and fundamental law of the present stage of development of capitalism.",
            "target": "उत्पादन के संकेंद्रण के परिणामस्वरूप एकाधिकारों का उदय पूंजीवाद के विकास के वर्तमान चरण का एक सार्वभौमिक और बुनियादी नियम है।",
            "bad_literal": "उत्पादन के जमाव से मोनोपॉली का उठना पूंजीवाद के विकास का बुनियादी नियम है।",
            "category": "imperialism_and_capital",
            "notes": "Use 'सार्वभौमिक और बुनियादी नियम' (general and fundamental law)."
        },
        {
            "source": "Monopoly is the exact opposite of free competition, but we have seen the latter being transformed into monopoly before our very eyes.",
            "target": "एकाधिकार मुक्त प्रतिस्पर्धा का ठीक विलोम है, लेकिन हमने अपनी आंखों के सामने मुक्त प्रतिस्पर्धा को एकाधिकार में बदलते देखा है।",
            "bad_literal": "एकाधिकार खुली प्रतियोगिता का उल्टा है लेकिन हमने प्रतियोगिता को एकाधिकार बनते देखा है।",
            "category": "imperialism_and_capital",
            "notes": "Dialectical transformation: 'मुक्त प्रतिस्पर्धा' vs 'एकाधिकार'."
        },
        {
            "source": "Monopoly produces concentration of production, creating large-scale industry and crowding out small industry, replacing big industry by still bigger industry.",
            "target": "एकाधिकार उत्पादन के संकेंद्रण को जन्म देता है, बड़े पैमाने के उद्योग का निर्माण करता है और छोटे उद्योग को बाहर धकेल देता है, बड़े उद्योग की जगह और भी बड़े उद्योग को स्थापित करता है।",
            "bad_literal": "मोनोपॉली उत्पादन जमाती है, बड़ा उद्योग बनाती है और छोटे उद्योग को हटा देती है।",
            "category": "imperialism_and_capital",
            "notes": "Fluid active verbs in Hindi."
        },
        {
            "source": "Monopoly leads to such concentration of production and capital that it has given rise to a financial oligarchy.",
            "target": "एकाधिकार उत्पादन और पूंजी के ऐसे संकेंद्रण को जन्म देता है जिसने वित्तीय अल्पतंत्र को पैदा किया है।",
            "bad_literal": "एकाधिकार उत्पादन और पूंजी का ऐसा जमाव करता है जिससे वित्तीय कुलीनतंत्र बनता है।",
            "category": "imperialism_and_capital",
            "notes": "Use 'वित्तीय अल्पतंत्र' (financial oligarchy)."
        },
        {
            "source": "Finance capital, concentrated in a few hands and exercising a virtual monopoly, exacts enormous and ever-increasing profits from the whole of society.",
            "target": "चंद हाथों में संकेंद्रित और लगभग पूर्ण एकाधिकार का प्रयोग करने वाली वित्तीय पूंजी पूरे समाज से भारी और लगातार बढ़ते मुनाफे निचोड़ती है।",
            "bad_literal": "कुछ हाथों में केंद्रित फाइनेंस कैपिटल पूरे समाज से भारी मुनाफा लेती है।",
            "category": "imperialism_and_capital",
            "notes": "Editorial rule: 'वित्तीय पूंजी' (finance capital) and 'मुनाफा' (profits)."
        },
        {
            "source": "The export of capital, one of the most essential economic bases of imperialism, still further isolates the rentier from production.",
            "target": "पूंजी का निर्यात, जो साम्राज्यवाद के सबसे आवश्यक आर्थिक आधारों में से एक है, सूदखोर वर्ग को उत्पादन से और भी अधिक अलग-थलग कर देता है।",
            "bad_literal": "पूंजी का एक्सपोर्ट साम्राज्यवाद का आर्थिक आधार है जो सूदखोर को अलग करता है।",
            "category": "imperialism_and_capital",
            "notes": "Use 'पूंजी का निर्यात' (export of capital) and 'सूदखोर वर्ग' (rentier)."
        },
        {
            "source": "The division of the world between international cartels and trusts is an established fact of modern capitalism.",
            "target": "अंतर्राष्ट्रीय कार्टेलों और ट्रस्टों के बीच दुनिया का बंटवारा आधुनिक पूंजीवाद का एक स्थापित तथ्य है।",
            "bad_literal": "अंतर्राष्ट्रीय कार्टेल और ट्रस्ट के बीच दुनिया का विभाजन आधुनिक पूंजीवाद का सच है।",
            "category": "imperialism_and_capital",
            "notes": "Use 'दुनिया का बंटवारा' and transliterate 'कार्टेलों और ट्रस्टों'."
        },
        {
            "source": "Imperialism is the epoch of finance capital and of monopolies, which introduce everywhere the striving for domination, not for freedom.",
            "target": "साम्राज्यवाद वित्तीय पूंजी और एकाधिकारों का युग है, जो हर जगह स्वतंत्रता के बजाय प्रभुत्व स्थापित करने की ललक पैदा करता है।",
            "bad_literal": "साम्राज्यवाद वित्तीय पूंजी और एकाधिकार का युग है जो आजादी के बदले प्रभुत्व लाता है।",
            "category": "imperialism_and_capital",
            "notes": "Classic formulation: 'स्वतंत्रता के बजाय प्रभुत्व स्थापित करने की ललक'."
        },
        {
            "source": "The uneven and spasmodic development of individual enterprises, individual branches of industry and individual countries is inevitable under the capitalist system.",
            "target": "पूंजीवादी व्यवस्था के तहत अलग-अलग उद्यमों, उद्योग की अलग-अलग शाखाओं और अलग-अलग देशों का असमान और असंतुलित विकास अपरिहार्य है।",
            "bad_literal": "पूंजीवादी प्रणाली में उद्यमों और देशों का असमान विकास जरूरी होता है।",
            "category": "imperialism_and_capital",
            "notes": "Use 'असमान और असंतुलित विकास' (uneven and spasmodic development)."
        },
        {
            "source": "Imperialism is capitalism in that stage of development in which the dominance of monopolies and finance capital has established itself.",
            "target": "साम्राज्यवाद पूंजीवाद के विकास का वह चरण है जिसमें एकाधिकारों और वित्तीय पूंजी का वर्चस्व स्थापित हो चुका होता है।",
            "bad_literal": "साम्राज्यवाद पूंजीवाद का वह स्तर है जहां एकाधिकार और वित्तीय पूंजी का राज होता है।",
            "category": "imperialism_and_capital",
            "notes": "Use 'वर्चस्व स्थापित होना' for 'dominance has established itself'."
        },
        {
            "source": "The non-economic superstructure which grows up on the basis of finance capital, its politics and its ideology, accentuates the striving for colonial conquest.",
            "target": "वित्तीय पूंजी के आधार पर विकसित होने वाली गैर-आर्थिक अधिरचना, उसकी राजनीति और उसकी विचारधारा, औपनिवेशिक विजय की ललक को और तेज कर देती है।",
            "bad_literal": "फाइनेंस कैपिटल पर बनने वाला गैर-आर्थिक ढांचा औपनिवेशिक जीत की चाह बढ़ाता है।",
            "category": "historical_materialism",
            "notes": "Editorial rule: Use 'गैर-आर्थिक अधिरचना' (non-economic superstructure)."
        },
        {
            "source": "Monopolies, oligarchy, the striving for domination of the weak by the strong—all these have given birth to those distinctive characteristics of imperialism which compel us to define it as parasitic or decaying capitalism.",
            "target": "एकाधिकार, अल्पतंत्र, शक्तिशाली द्वारा कमजोर पर प्रभुत्व कायम करने की ललक—इन सभी ने साम्राज्यवाद की उन विशिष्ट विशेषताओं को जन्म दिया है जो हमें इसे परजीवी या मरणासन्न पूंजीवाद के रूप में परिभाषित करने के लिए बाध्य करती हैं।",
            "bad_literal": "एकाधिकार और कुलीनतंत्र ने साम्राज्यवाद के वे लक्षण पैदा किए जो इसे परजीवी पूंजीवाद बनाते हैं।",
            "category": "imperialism_and_capital",
            "notes": "Use 'परजीवी या मरणासन्न पूंजीवाद' (parasitic or decaying capitalism)."
        },
        {
            "source": "The rentier state is a state of parasitic, decaying capitalism, and this circumstance cannot fail to influence all the socio-political conditions of the countries concerned.",
            "target": "सूदखोर राज्य परजीवी, मरणासन्न पूंजीवाद का राज्य होता है, और यह परिस्थिति संबंधित देशों की सभी सामाजिक-राजनीतिक दशाओं को प्रभावित किए बिना नहीं रह सकती।",
            "bad_literal": "सूदखोर राज्य परजीवी पूंजीवाद का राज्य है और यह सभी राजनीतिक स्थितियों को प्रभावित करता है।",
            "category": "imperialism_and_capital",
            "notes": "Use 'सूदखोर राज्य' (rentier state)."
        },
        {
            "source": "From all that has been said in this book on the economic essence of imperialism, it follows that we must define it as capitalism in transition, or, more precisely, as dying capitalism.",
            "target": "साम्राज्यवाद के आर्थिक सारतत्व के विषय में इस पुस्तक में जो कुछ भी कहा गया है, उससे यह निष्कर्ष निकलता है कि हमें इसे संक्रमणकालीन पूंजीवाद, या अधिक सटीक रूप में, मरणासन्न पूंजीवाद के रूप में परिभाषित करना चाहिए।",
            "bad_literal": "इस किताब में साम्राज्यवाद के बारे में जो कहा गया है उससे यह मरणासन्न पूंजीवाद कहलाता है।",
            "category": "imperialism_and_capital",
            "notes": "Use 'संक्रमणकालीन पूंजीवाद' (capitalism in transition) vs 'मरणासन्न पूंजीवाद' (dying capitalism)."
        },
        {
            "source": "Private property based on the labour of the small owner, free competition, democracy, all the slogans with which the capitalists and their press deceive the workers and the peasants are things of the distant past.",
            "target": "छोटे मालिक के श्रम पर आधारित निजी संपत्ति, मुक्त प्रतिस्पर्धा, लोकतंत्र—वे सभी नारे जिनके जरिए पूंजीपति और उनका प्रेस मजदूरों और किसानों को धोखा देते हैं—अब सुदूर अतीत की बातें बन चुकी हैं।",
            "bad_literal": "छोटे मालिक की निजी संपत्ति, खुली प्रतियोगिता और लोकतंत्र के नारे अब पुरानी बात हैं।",
            "category": "historical_materialism",
            "notes": "Preserve cadenced relative clause: 'सुदूर अतीत की बातें बन चुकी हैं'."
        },
        {
            "source": "Imperialism is the eve of the social revolution of the proletariat. This has been confirmed since 1917 on a world-wide scale.",
            "target": "साम्राज्यवाद सर्वहारा की सामाजिक क्रांति की पूर्ववेला है। 1917 के बाद से विश्वव्यापी पैमाने पर इसकी पुष्टि हो चुकी है।",
            "bad_literal": "साम्राज्यवाद सर्वहारा की सामाजिक क्रांति की शाम है जिसकी पुष्टि 1917 से हुई है।",
            "category": "party_and_revolution",
            "notes": "Use 'सर्वहारा की सामाजिक क्रांति की पूर्ववेला' for 'eve of the social revolution of the proletariat'."
        },
        {
            "source": "Social-chauvinism is socialism in words, chauvinism in deeds, the complete desertion to the side of the bourgeoisie.",
            "target": "सामाजिक-अंधराष्ट्रवाद का अर्थ है कथनी में समाजवाद और करनी में अंधराष्ट्रवाद, जो कि पूरी तरह बुर्जुआ वर्ग के पाले में चले जाना है।",
            "bad_literal": "सामाजिक अंधराष्ट्रवाद शब्दों में समाजवाद और काम में अंधराष्ट्रवाद है जो बुर्जुआ पक्ष में जाना है।",
            "category": "political_tendencies",
            "notes": "Use 'सामाजिक-अंधराष्ट्रवाद' (social-chauvinism) and 'कथनी में समाजवाद और करनी में अंधराष्ट्रवाद'."
        },
        {
            "source": "Unless the economic roots of this phenomenon are understood and its political and social significance is appreciated, not a step can be taken toward solving the practical problems of the communist movement.",
            "target": "जब तक इस परिघटना की आर्थिक जड़ों को न समझा जाए और इसके राजनीतिक व सामाजिक महत्व का मूल्यांकन न किया जाए, तब तक कम्युनिस्ट आंदोलन की व्यावहारिक समस्याओं को हल करने की दिशा में एक कदम भी आगे नहीं बढ़ाया जा सकता।",
            "bad_literal": "जब तक इस घटना की आर्थिक जड़ें न समझी जाएं कम्युनिस्ट आंदोलन की समस्याएं हल नहीं हो सकतीं।",
            "category": "party_and_revolution",
            "notes": "Conditional clause flow: 'जब तक... तब तक'."
        }
    ]
    pairs.extend(imp_pairs)

    return pairs

def main():
    tm = TranslationMemory(storage_path=os.path.join(BASE_DIR, "data", "tm_store.json"))
    pairs = extract_pairs()
    print(f"Extracted {len(pairs)} high-quality aligned sentence pairs of V. I. Lenin.")
    
    count = tm.import_pairs(pairs)
    print(f"Successfully imported {count} sentence pairs into Translation Memory.")
    print(f"Total Translation Memory pairs now: {len(tm.get_all())}")

if __name__ == "__main__":
    main()
