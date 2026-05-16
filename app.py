# =========================================================
# 🔮 NUMERO ANNAND AI — ULTIMATE PROFESSIONAL VERSION
# =========================================================
# FULL PROFESSIONAL APP.PY WITH MULTI-LANGUAGE SUPPORT (FREE)
# =========================================================

from flask import Flask, render_template_string, request
from datetime import datetime, date
from dateutil import parser
import re
import math
import random

app = Flask(__name__)
app.secret_key = "numero-annand-ai"

# =========================================================
# CONFIG
# =========================================================

WHATSAPP_CHAT_LINK = "https://wa.me/917099805039?text=Hello%20Annand%20Sarma,%20I%20want%20to%20book%20a%20consultation."
WHATSAPP_GROUP_LINK = "https://chat.whatsapp.com/C5g8MVpA0SYASAyrZfsrtJ?mode=gi_t"

MASTER_NUMBERS = {11, 22, 33}

# =========================================================
# CHALDEAN MAP
# =========================================================

CHALDEAN_MAP = {
    'A':1,'I':1,'J':1,'Q':1,'Y':1,
    'B':2,'K':2,'R':2,
    'C':3,'G':3,'L':3,'S':3,
    'D':4,'M':4,'T':4,
    'E':5,'H':5,'N':5,'X':5,
    'U':6,'V':6,'W':6,
    'O':7,'Z':7,
    'F':8,'P':8
}

# =========================================================
# RELATIONSHIPS
# =========================================================

NUM_RELATIONS = {
    1:{'friends':[1,2,3,5,7,9],'neutral':[4,8],'enemy':[6]},
    2:{'friends':[1,2,3,5],'neutral':[4,7,8,9],'enemy':[6]},
    3:{'friends':[1,2,3,5,7,9],'neutral':[6,8],'enemy':[4]},
    4:{'friends':[1,5,6,7],'neutral':[2,8,9],'enemy':[3]},
    5:{'friends':[1,2,3,5,6,8],'neutral':[4,7,9],'enemy':[]},
    6:{'friends':[5,6,7,8],'neutral':[3,4,9],'enemy':[1,2]},
    7:{'friends':[1,3,4,5,6],'neutral':[2,8,9],'enemy':[]},
    8:{'friends':[4,5,6,7],'neutral':[1,2,3],'enemy':[8,9]},
    9:{'friends':[1,2,3,5,7],'neutral':[4,6],'enemy':[8,9]}
}

# =========================================================
# TRANSLATION DICTIONARY
# =========================================================
I18N = {
    'en': {
        'title': "🔮 Numero Annand AI",
        'subtitle': "Advanced Premium Lo Shu Grid Numerology Platform powered by deep energetic analysis, professional numerology intelligence, personality interpretation systems, career guidance algorithms, karmic vibration decoding and futuristic spiritual analytics.",
        'workspace': "Workspace Menu",
        'input_name': "Name For Analysis",
        'input_dob': "Date Of Birth",
        'input_mobile': "Mobile Number (Optional)",
        'btn_analyze': "Analyze Now",
        'consult_folder': "📞 Consultation Folder",
        'strategist': "Primary Strategist:",
        'connect_wa': "💬 Connect on WhatsApp",
        'charges_title': "⏰ Strategic Analytics Status:",
        'free_access': "Full System Access: <b style='color:#00ff88;'>FREE</b>",
        'btn_consult': "Consult with Annand Sarma",
        'wa_group_title': "👥 WhatsApp Group Folder",
        'btn_group': "Open WhatsApp Group",
        'footer': "Numero Annand AI • Premium Numerology Platform",
        'welcome_title': "✨ Welcome To Numero Annand AI",
        'card1_t': "🔢 Lo Shu Grid Intelligence",
        'card1_d': "Ancient Lo Shu Grid system enhanced with advanced AI-powered energetic interpretation and deep psychological decoding.",
        'card2_t': "🧠 Personality Blueprint",
        'card2_d': "Discover hidden behavioral patterns, karmic strengths, emotional tendencies and subconscious personality architecture.",
        'card3_t': "💼 Career & Wealth Guidance",
        'card3_d': "Understand financial vibrations, business success indicators, leadership patterns and prosperity alignment.",
        'card4_t': "❤️ Relationship Compatibility",
        'card4_d': "Analyze emotional resonance, communication harmony, marriage compatibility and relationship energy flow.",
        'card5_t': "🧿 Remedies & Balance",
        'card5_d': "Receive practical spiritual remedies for balancing missing energies and improving life stability.",
        'card6_t': "📈 Future Forecast",
        'card6_d': "Personal Year cycles, destiny timing analysis, yearly guidance and energetic prediction system.",
        'p1_title': "📘 PAGE 1 — CORE NUMEROLOGY PROFILE",
        'lbl_name': "Full Name",
        'lbl_dob': "Date Of Birth",
        'lbl_driver': "Driver Number",
        'lbl_conductor': "Conductor Number",
        'lbl_name_num': "Name Number",
        'lbl_compound': "Compound Name Value",
        'eb_score': "⚡ Energy Balance Score",
        'eb_desc': "Your energetic compatibility score is calculated through synchronization between Driver Number, Destiny vibration, Lo Shu Grid structure, missing number recovery potential, and Chaldean name resonance patterns.",
        'p_snap': "🧠 Personality Snapshot",
        'p_desc': "The Driver Number {driver} strongly influences your instinctive behavior, natural reactions, subconscious personality structure, and decision-making psychology.<br><br>The Conductor Number {conductor} controls long-term destiny patterns, karmic evolution, public identity, and life direction.<br><br>Your Name Number vibration {name_single} shapes social recognition, external opportunities, communication magnetism, and energetic response from society.",
        'c_meter': "📊 Compatibility Meter",
        'c_desc': "Current Name Compatibility:",
        'p2_title': "📗 PAGE 2 — FULL LO SHU GRID ANALYSIS",
        'missing_t': "🔍 Missing Numbers",
        'missing_desc': "The missing numbers in your Lo Shu Grid are: <b>{missing}</b><br><br>These absent frequencies indicate karmic lessons and developmental areas requiring conscious improvement.",
        'repeated_t': "🔥 Repeated Numbers",
        'repeated_desc': "Repeated numbers detected: <b>{repeated}</b><br><br>Repeated vibrations increase energetic intensity and amplify specific personality dimensions.",
        'mental_t': "🧠 Mental Plane Analysis",
        'mental_desc': "The Mental Plane reflects intellectual clarity, planning ability, memory structure, and analytical vision. Strong mental numbers indicate strategic intelligence and powerful visualization capability.",
        'emotional_t': "❤️ Emotional Plane Analysis",
        'emotional_desc': "The Emotional Plane represents empathy, emotional reactions, intuition, compassion, and relationship sensitivity. Balanced emotional numbers improve harmony, emotional maturity, and communication quality.",
        'practical_t': "💼 Practical Plane Analysis",
        'practical_desc': "The Practical Plane governs execution ability, discipline, financial stability, consistency, and career implementation. Strong practical numbers create structured progress and material success potential.",
        'p3_title': "📙 PAGE 3 — ADVANCED PSYCHOLOGICAL & SPIRITUAL ANALYSIS",
        'arrow_t': "🧿 Arrow Analysis",
        'arrow_desc': "Your Lo Shu Grid reveals hidden energetic pathways influencing determination, willpower, emotional control, spirituality, discipline, and communication style. Strong arrows improve internal alignment while broken arrows reveal karmic learning zones.",
        'raj_t': "👑 Raj Yog Potential",
        'raj_desc': "The interaction between your Driver Number, Destiny vibration, and Lo Shu structure suggests strong potential for recognition, authority, leadership, and long-term influence. Consistent discipline and emotionally balanced decision-making can significantly improve manifestation power.",
        'psych_t': "🧠 Psychological Traits",
        'psych_desc': "Your chart suggests a deeply layered psychological structure influenced by both conscious ambition and subconscious karmic memory patterns. You may naturally seek meaning, stability, emotional security, and purposeful growth rather than temporary achievements.",
        'spirit_t': "🪷 Spiritual Traits",
        'spirit_desc': "Spiritual development becomes important when your inner vibration begins searching for emotional clarity, energetic balance, and deeper life purpose. Meditation, self-awareness, disciplined routine, and positive environments improve spiritual stability.",
        'p4_title': "📕 PAGE 4 — NAME CORRECTION & LIFE GUIDANCE",
        'perf_msg': "✅ Congratulations!<br><br>Your current name vibration is strongly aligned with your Driver Number ({driver}), Conductor Number ({conductor}), and native Lo Shu Grid frequencies.<br><br>The energetic structure of your existing name naturally supports identity stability, emotional balance, decision-making power, and long-term manifestation capacity.<br><br>Your name also helps stabilize karmic gaps within the Lo Shu Grid and creates a highly cooperative resonance between personality vibration and destiny vibration.<br><br>No correction is required because your present name already carries a professionally balanced numerological frequency.",
        'imp_msg': "⚠️ Name Vibration Improvement Recommended<br><br>Your current name is functional, but it does not fully synchronize with your complete Lo Shu Grid structure and destiny frequencies.<br><br>This can create invisible delays in career growth, emotional stability, financial flow, relationship harmony, or confidence expression.<br><br>A professionally optimized spelling can significantly improve energetic balance, public attraction, mental clarity, and long-term manifestation potential.",
        'sugg_title': "✨ Professionally Suggested Corrected Names",
        'sugg_comp': "Improved Compatibility:",
        'sugg_vib': "New Vibration Number:",
        'sugg_reason': "This spelling introduces stronger energetic synchronization with Driver Number {driver} and Destiny Number {conductor}. It improves vibration flow connected to confidence, opportunity attraction, public response, communication strength, and material stability. The revised structure also helps balance missing Lo Shu frequencies and reduces internal energetic conflicts visible in the birth chart.",
        'career_t': "💼 Career Guidance",
        'career_desc': "Your numerological structure supports fields connected to communication, guidance, teaching, management, spirituality, consulting, analytics, business development, and public interaction. Long-term success improves when emotional balance and disciplined routines are maintained consistently.",
        'rel_t': "❤️ Relationship Guidance",
        'rel_desc': "Relationship harmony improves through patience, emotional openness, balanced communication, and mutual understanding. Your emotional vibration seeks sincerity, respect, loyalty, and psychological depth within relationships.",
        'fin_t': "💰 Financial Guidance",
        'fin_desc': "Financial stability increases through strategic planning, long-term discipline, and practical money management. Avoid impulsive financial decisions during emotionally unstable periods.",
        'lucky_t': "🍀 Lucky Indicators",
        'l_num': "Lucky Numbers:",
        'l_days': "Lucky Days: Sunday, Wednesday, Friday",
        'l_cols': "Lucky Colors: Aqua Blue, White, Emerald Green",
        'l_dirs': "Lucky Direction: East & North-East",
        'l_time': "Lucky Time: Morning 6AM – 10AM",
        'p5_title': "导 PAGE 5 — DEEP AI PROFESSIONAL REPORT",
        'human_t': "🧠 Human-Style Deep Interpretation",
        'human_desc': "Your complete numerological blueprint reveals a personality carrying both intellectual sensitivity and long-term growth potential. The interaction between your Driver vibration, Destiny path, and Name frequency creates a life pattern focused on self-development, responsibility, emotional evolution, and gradual manifestation. Periods of internal confusion generally appear when emotional pressure overrides logical structure. However, your chart also shows strong recovery potential, resilience, and adaptability. Your energy improves significantly when operating within disciplined environments, emotionally supportive relationships, and spiritually balanced routines.",
        'year_t': "📈 Yearly Forecast",
        'year_desc': "The upcoming energetic cycle favors structured decision-making, strategic planning, financial awareness, and emotional maturity. New opportunities may emerge through communication, networking, guidance roles, or knowledge-sharing activities.",
        'road_t': "🪷 Spiritual Roadmap",
        'road_desc': "Meditation, focused routine, spiritual reading, gratitude practice, and balanced environments help stabilize your energetic field. Avoid negative surroundings, emotional overthinking, and inconsistent routines.",
        'rem_t': "🧿 Remedies",
        'rem_li': "<li>Practice daily meditation for 11 minutes.</li><li>Maintain structured sleep and work routine.</li><li>Use positive affirmations consistently.</li><li>Strengthen weak Lo Shu energies consciously.</li><li>Wear clean light colors during important work.</li><li>Avoid emotional impulsiveness in major decisions.</li><li>Use lucky dates for important actions.</li>",
        'strat_t': "🚀 Success Strategy",
        'strat_desc': "Long-term success emerges when emotional intelligence, discipline, communication skills, and spiritual balance operate together. Your chart rewards patience, structured planning, consistency, and positive social contribution more than short-term shortcuts.",
        'freq_title': "📊 COMPLETE FREQUENCY ANALYSIS",
        'f_miss': "❌ Number {n} is missing from the Lo Shu Grid. The absence of this vibration indicates important karmic lessons connected to emotional maturity, discipline, confidence, stability, or life organization.",
        'f_one': "⚖️ Number {n} appears once. This indicates a naturally balanced energetic presence without excessive dominance or deficiency.",
        'f_two': "✅ Number {n} appears twice. This creates strong supportive energy connected to the psychological themes ruled by this number.",
        'f_many': "🔥 Number {n} appears {c} times. This vibration becomes highly dominant within the personality structure and strongly influences behavior, emotional reactions, and life direction.",
        'report_free_title': "📥 Access Complete Digital Analysis Report",
        'report_free_desc': "Your digital analysis and structural evaluation report has been compiled successfully by our computational intelligence matrix. You can save or consult directly using the credentials below.",
        'free_badge': "Free Digital Access",
        'unlocked_status': "UNLOCKED"
    },
    'hi': {
        'title': "🔮 न्यूमरो आनंद एआई",
        'subtitle': "गहन ऊर्जा विश्लेषण, पेशेवर अंकशास्त्र बुद्धिमत्ता, व्यक्तित्व व्याख्या प्रणाली, करियर मार्गदर्शन एल्गोरिदम, कर्म कंपन डिकोडिंग और भविष्य के आध्यात्मिक विश्लेषण द्वारा संचालित उन्नत प्रीमियम लो शू ग्रिड अंकशास्त्र मंच।",
        'workspace': "कार्यक्षेत्र मेनू",
        'input_name': "विश्लेषण के लिए नाम",
        'input_dob': "जन्म तिथि",
        'input_mobile': "मोबाइल नंबर (वैकल्पिक)",
        'btn_analyze': "अभी विश्लेषण करें",
        'consult_folder': "📞 परामर्श फ़ोल्डर",
        'strategist': "मुख्य रणनीतिकार:",
        'connect_wa': "💬 व्हाट्सएप पर जुड़ें",
        'charges_title': "⏰ रणनीतिक विश्लेषण स्थिति:",
        'free_access': "पूर्ण सिस्टम एक्सेस: <b style='color:#00ff88;'>मुफ़्त (FREE)</b>",
        'btn_consult': "आनंद सरमा से परामर्श करें",
        'wa_group_title': "👥 व्हाट्सएप ग्रुप फ़ोल्डर",
        'btn_group': "व्हाट्सएप ग्रुप खोलें",
        'footer': "न्यूमरो आनंद एआई • प्रीमियम अंकशास्त्र मंच",
        'welcome_title': "✨ न्यूमरो आनंद एआई में आपका स्वागत है",
        'card1_t': "🔢 लो शू ग्रिड इंटेलिजेंस",
        'card1_d': "प्राचीन लो शू ग्रिड प्रणाली को उन्नत एआई-संचालित ऊर्जावान व्याख्या और गहरे मनोवैज्ञानिक डिकोडिंग के साथ बढ़ाया गया है।",
        'card2_t': "🧠 व्यक्तित्व खाका",
        'card2_d': "छिपे हुए व्यवहार पैटर्न, कर्मिक ताकत, भावनात्मक प्रवृत्तियों और अवचेतन व्यक्तित्व वास्तुकला की खोज करें।",
        'card3_t': "💼 करियर और धन मार्गदर्शन",
        'card3_d': "वित्तीय कंपन, व्यावसायिक सफलता के संकेतक, नेतृत्व पैटर्न और समृद्धि संरेखण को समझें।",
        'card4_t': "❤️ संबंध अनुकूलता",
        'card4_d': "भावनात्मक प्रतिध्वनि, संचार सद्भाव, विवाह अनुकूलता और संबंध ऊर्जा प्रवाह का विश्लेषण करें।",
        'card5_t': "🧿 उपचार और संतुलन",
        'card5_d': "लापता ऊर्जाओं को संतुलित करने और जीवन की स्थिरता में सुधार के लिए व्यावहारिक आध्यात्मिक उपचार प्राप्त करें।",
        'card6_t': "📈 भविष्य का पूर्वानुमान",
        'card6_d': "व्यक्तिगत वर्ष चक्र, भाग्य समय विश्लेषण, वार्षिक मार्गदर्शन और ऊर्जावान भविष्यवाणी प्रणाली।",
        'p1_title': "📘 पृष्ठ 1 — मुख्य अंकशास्त्र प्रोफ़ाइल",
        'lbl_name': "पूरा नाम",
        'lbl_dob': "जन्म तिथि",
        'lbl_driver': "ड्राइवर नंबर (मूलांक)",
        'lbl_conductor': "कंडक्टर नंबर (भाग्यांक)",
        'lbl_name_num': "नाम अंक",
        'lbl_compound': "मिश्रित नाम मूल्य",
        'eb_score': "⚡ ऊर्जा संतुलन स्कोर",
        'eb_desc': "आपका ऊर्जावान अनुकूलता स्कोर ड्राइवर नंबर, भाग्य कंपन, लो शू ग्रिड संरचना, लापता संख्या पुनर्प्राप्ति क्षमता और चाल्डियन नाम प्रतिध्वनि पैटर्न के बीच सिंक्रनाइज़ेशन के माध्यम से गणना की जाती है।",
        'p_snap': "🧠 व्यक्तित्व की रूपरेखा",
        'p_desc': "ड्राइवर नंबर {driver} आपके सहज व्यवहार, प्राकृतिक प्रतिक्रियाओं, अवचेतन व्यक्तित्व संरचना और निर्णय लेने के मनोविज्ञान को दृढ़ता से प्रभावित करता है।<br><br>कंडक्टर नंबर {conductor} दीर्घकालिक भाग्य पैटर्न, कर्मिक विकास, सार्वजनिक पहचान और जीवन की दिशा को नियंत्रित करता है।<br><br>आपका नाम नंबर कंपन {name_single} सामाजिक मान्यता, बाहरी अवसरों, संचार चुंबकत्व और समाज से ऊर्जावान प्रतिक्रिया को आकार देता है।",
        'c_meter': "📊 अनुकूलता मीटर",
        'c_desc': "वर्तमान नाम अनुकूलता:",
        'p2_title': "📗 पृष्ठ 2 — पूर्ण लो शू ग्रिड विश्लेषण",
        'missing_t': "🔍 लापता नंबर",
        'missing_desc': "आपके लो शू ग्रिड में लापता नंबर हैं: <b>{missing}</b><br><br>ये अनुपस्थित आवृत्तियाँ कर्म पाठों और विकासात्मक क्षेत्रों को इंगित करती हैं जिनमें सचेत सुधार की आवश्यकता होती.",
        'repeated_t': "🔥 दोहराए गए नंबर",
        'repeated_desc': "दोहराए गए नंबर मिले हैं: <b>{repeated}</b><br><br>दोहराए गए कंपन ऊर्जा की तीव्रता को बढ़ाते हैं और विशिष्ट व्यक्तित्व आयामों को बढ़ाते हैं।",
        'mental_t': "🧠 मानसिक तल विश्लेषण",
        'mental_desc': "मानसिक तल बौद्धिक स्पष्टता, योजना क्षमता, स्मृति संरचना और विश्लेषणात्मक दृष्टि को दर्शाता है। मजबूत मानसिक संख्याएं रणनीतिक बुद्धिमत्ता और शक्तिशाली दृश्य क्षमता का संकेत देती हैं।",
        'emotional_t': "❤️ भावनात्मक तल विश्लेषण",
        'emotional_desc': "भावनात्मक तल सहानुभूति, भावनात्मक प्रतिक्रियाओं, अंतर्ज्ञान, करुणा और संबंध संवेदनशीलता का प्रतिनिधित्व करता है। संतुलित भावनात्मक संख्याएं सद्भाव, भावनात्मक परिपक्वता और संचार गुणवत्ता में सुधार करती हैं।",
        'practical_t': "💼 व्यावहारिक तल विश्लेषण",
        'practical_desc': "व्यावहारिक तल निष्पादन क्षमता, अनुशासन, वित्तीय स्थिरता, निरंतरता और करियर कार्यान्वयन को नियंत्रित करता है। मजबूत व्यावहारिक संख्याएं संरचित प्रगति और भौतिक सफलता की क्षमता पैदा करती हैं।",
        'p3_title': "📙 पृष्ठ 3 — उन्नत मनोवैज्ञानिक और आध्यात्मिक विश्लेषण",
        'arrow_t': "🧿 तीर (Arrow) विश्लेषण",
        'arrow_desc': "आपका लो शू ग्रिड दृढ़ संकल्प, इच्छाशक्ति, भावनात्मक नियंत्रण, आध्यात्मिकता, अनुशासन और संचार शैली को प्रभावित करने वाले छिपे हुए ऊर्जावान मार्गों को प्रकट करता है। मजबूत तीर आंतरिक संरेखण में सुधार करते हैं जबकि टूटे हुए तीर कर्म सीखने के क्षेत्रों को प्रकट करते हैं।",
        'raj_t': "👑 राज योग क्षमता",
        'raj_desc': "आपके ड्राइवर नंबर, भाग्य कंपन और लो शू संरचना के बीच बातचीत मान्यता, अधिकार, नेतृत्व और दीर्घकालिक प्रभाव के लिए मजबूत क्षमता का सुझाव देती है। लगातार अनुशासन और भावनात्मक रूप से संतुलित निर्णय लेने से अभिव्यक्ति की शक्ति में काफी सुधार हो सकता है।",
        'psych_t': "🧠 मनोवैज्ञानिक लक्षण",
        'psych_desc': "आपका चार्ट सचेत महत्वाकांक्षा और अवचेतन कर्मिक स्मृति पैटर्न दोनों से प्रभावित एक गहरी स्तरित मनोवैज्ञानिक संरचना का सुझाव देता है। आप स्वाभाविक रूप से अस्थायी उपलब्धियों के बजाय अर्थ, स्थिरता, भावनात्मक सुरक्षा और उद्देश्यपूर्ण विकास की तलाश कर सकते हैं।",
        'spirit_t': "🪷 आध्यात्मिक लक्षण",
        'spirit_desc': "आध्यात्मिक विकास तब महत्वपूर्ण हो जाता है जब आपका आंतरिक कंपन भावनात्मक स्पष्टता, ऊर्जावान संतुलन और गहरे जीवन उद्देश्य की तलाश शुरू कर देता है। ध्यान, आत्म-जागरूकता, अनुशासित दिनचर्या और सकारात्मक वातावरण आध्यात्मिक स्थिरता में सुधार करते हैं।",
        'p4_title': "📕 पृष्ठ 4 — नाम सुधार और जीवन मार्गदर्शन",
        'perf_msg': "✅ बधाई हो!<br><br>आपका वर्तमान नाम कंपन आपके ड्राइवर नंबर ({driver}), कंडक्टर नंबर ({conductor}), और मूल लो शू ग्रिड आवृत्तियों के साथ दृढ़ता से संरेखित है।<br><br>आपके मौजूदा नाम की ऊर्जावान संरचना स्वाभाविक रूप से पहचान स्थिरता, भावनात्मक संतुलन, निर्णय लेने की शक्ति और दीर्घकालिक अभिव्यक्ति क्षमता का समर्थन करती है।<br><br>आपका नाम लो शू ग्रिड के भीतर कर्म अंतराल को स्थिर करने में भी मदद करता है और व्यक्तित्व कंपन और भाग्य कंपन के बीच एक अत्यधिक सहकारी प्रतिध्वनि पैदा करता है।<br><br>किसी सुधार की आवश्यकता नहीं है क्योंकि आपका वर्तमान नाम पहले से ही एक पेशेवर रूप से संतुलित अंकशास्त्रीय आवृत्ति वहन करता है।",
        'imp_msg': "⚠️ नाम कंपन सुधार की सिफारिश की जाती है<br><br>आपका वर्तमान नाम कार्यात्मक है, लेकिन यह आपकी पूर्ण लो शू ग्रिड संरचना और भाग्य आवृत्तियों के साथ पूरी तरह से सिंक्रनाइज़ नहीं है।<br><br>यह करियर के विकास, भावनात्मक स्थिरता, वित्तीय प्रवाह, संबंध सद्भाव, या आत्मविश्वास की अभिव्यक्ति में अदृश्य देरी पैदा कर सकता है।<br><br>एक पेशेवर रूप से अनुकूलित वर्तनी ऊर्जावान संतुलन, सार्वजनिक आकर्षण, मानसिक स्पष्टता और दीर्घकालिक अभिव्यक्ति क्षमता में काफी सुधार कर सकती है।",
        'sugg_title': "✨ पेशेवर रूप से सुझाए गए संशोधित नाम",
        'sugg_comp': "बेहतर अनुकूलता:",
        'sugg_vib': "नया कंपन नंबर:",
        'sugg_reason': "यह वर्तनी ड्राइवर नंबर {driver} और भाग्य नंबर {conductor} के साथ मजबूत ऊर्जावान सिंक्रनाइज़ेशन पेश करती है। यह आत्मविश्वास, अवसर आकर्षण, सार्वजनिक प्रतिक्रिया, संचार शक्ति और भौतिक स्थिरता से जुड़े कंपन प्रवाह में सुधार करती है। संशोधित संरचना लापता लो शू आवृत्तियों को संतुलित करने में भी मदद करती है और जन्म चार्ट में दिखाई देने वाले आंतरिक ऊर्जावान संघर्षों को कम करती है।",
        'career_t': "💼 करियर मार्गदर्शन",
        'career_desc': "आपकी अंकशास्त्रीय संरचना संचार, मार्गदर्शन, शिक्षण, प्रबंधन, आध्यात्मिकता, परामर्श, विश्लेषण, व्यवसाय विकास और सार्वजनिक संपर्क से जुड़े क्षेत्रों का समर्थन करती है। दीर्घकालिक सफलता तब बेहतर होती है जब भावनात्मक संतुलन और अनुशासित दिनचर्या लगातार बनी रहती है।",
        'rel_t': "❤️ संबंध मार्गदर्शन",
        'rel_desc': "धैर्य, भावनात्मक खुलेपन, संतुलित संचार और आपसी समझ के माध्यम से संबंधों में सामंजस्य सुधरता है। आपका भावनात्मक कंपन संबंधों के भीतर ईमानदारी, सम्मान, वफादारी और मनोवैज्ञानिक गहराई चाहता है।",
        'fin_t': "💰 वित्तीय मार्गदर्शन",
        'fin_desc': "रणनीतिक योजना, दीर्घकालिक अनुशासन और व्यावहारिक धन प्रबंधन के माध्यम से वित्तीय स्थिरता बढ़ती है। भावनात्मक रूप से अस्थिर अवधि के दौरान आवेगी वित्तीय निर्णयों से बचें।",
        'lucky_t': "🍀 भाग्यशाली संकेतक",
        'l_num': "भाग्यशाली अंक:",
        'l_days': "भाग्यशाली दिन: रविवार, बुधवार, शुक्रवार",
        'l_cols': "भाग्यशाली रंग: एक्वा ब्लू, सफेद, पन्ना हरा",
        'l_dirs': "भाग्यशाली दिशा: पूर्व और उत्तर-पूर्व",
        'l_time': "भाग्यशाली समय: सुबह 6 बजे से 10 बजे तक",
        'p5_title': "导 पृष्ठ 5 — गहन एआई व्यावसायिक रिपोर्ट",
        'human_t': "🧠 मानव-शैली गहन व्याख्या",
        'human_desc': "आपका संपूर्ण अंकशास्त्रीय खाका एक ऐसे व्यक्तित्व को प्रकट करता है जिसमें बौद्धिक संवेदनशीलता और दीर्घकालिक विकास क्षमता दोनों हैं। आपके ड्राइवर कंपन, भाग्य पथ और नाम आवृत्ति के बीच बातचीत आत्म-विकास, जिम्मेदारी, भावनात्मक विकास और क्रमिक अभिव्यक्ति पर केंद्रित जीवन पैटर्न बनाती है। आंतरिक भ्रम की अवधि आम तौर पर तब दिखाई देती है जब भावनात्मक दबाव तार्किक संरचना पर हावी हो जाता है। हालाँकि, आपका चार्ट मजबूत रिकवरी क्षमता, लचीलापन और अनुकूलनशीलता भी दिखाता है। अनुशासित वातावरण, भावनात्मक रूप से सहायक संबंधों और आध्यात्मिक रूप से संतुलित दिनचर्या में काम करने से आपकी ऊर्जा में काफी सुधार होता है।",
        'year_t': "📈 वार्षिक पूर्वानुमान",
        'year_desc': "आगामी ऊर्जावान चक्र संरचित निर्णय लेने, रणनीतिक योजना, वित्तीय जागरूकता और भावनात्मक परिपक्वता का पक्ष लेता है। संचार, नेटवर्किंग, मार्गदर्शन भूमिकाओं, या ज्ञान-साझाकरण गतिविधियों के माध्यम से नए अवसर उभर सकते हैं।",
        'road_t': "🪷 आध्यात्मिक रोडमैप",
        'road_desc': "ध्यान, केंद्रित दिनचर्या, आध्यात्मिक पढ़ना, कृतज्ञता अभ्यास और संतुलित वातावरण आपके ऊर्जावान क्षेत्र को स्थिर करने में मदद करते हैं। नकारात्मक परिवेश, भावनात्मक अति-सोच और असंगत दिनचर्या से बचें।",
        'rem_t': "🧿 उपाय",
        'rem_li': "<li>रोजाना 11 मिनट ध्यान का अभ्यास करें।</li><li>संरचित नींद और काम की दिनचर्या बनाए रखें।</li><li>सकारात्मक पुष्टि का लगातार उपयोग करें।</li><li>कमजोर लो शू ऊर्जाओं को सचेत रूप से मजबूत करें।</li><li>महत्वपूर्ण कार्यों के दौरान साफ हल्के रंग के कपड़े पहनें।</li><li>बड़े फैसलों में भावनात्मक आवेग से बचें।</li><li>महत्वपूर्ण कार्यों के लिए भाग्यशाली तिथियों का उपयोग करें।</li>",
        'strat_t': "🚀 सफलता की रणनीति",
        'strat_desc': "दीर्घकालिक सफलता तब उभरती है जब भावनात्मक बुद्धिमत्ता, अनुशासन, संचार कौशल और आध्यात्मिक संतुलन एक साथ काम करते हैं। आपका चार्ट अल्पकालिक शॉर्टकट की तुलना में धैर्य, संरचित योजना, निरंतरता और सकारात्मक सामाजिक योगदान को पुरस्कृत करता है।",
        'freq_title': "📊 पूर्ण आवृत्ति विश्लेषण",
        'f_miss': "❌ नंबर {n} लो शू ग्रिड से गायब है। इस कंपन की अनुपस्थिति भावनात्मक परिपक्वता, अनुशासन, आत्मविश्वास, स्थिरता या जीवन संगठन से जुड़े महत्वपूर्ण कर्म पाठों को इंगित करती है।",
        'f_one': "⚖️ नंबर {n} एक बार दिखाई देता है। यह अत्यधिक प्रभुत्व या कमी के बिना स्वाभाविक रूप से संतुलित ऊर्जावान उपस्थिति को इंगित करता है।",
        'f_two': "✅ नंबर {n} दो बार दिखाई देता है। यह इस संख्या द्वारा शासित मनोवैज्ञानिक विषयों से जुड़ी मजबूत सहायक ऊर्जा बनाता है।",
        'f_many': "🔥 नंबर {n} {c} बार दिखाई देता है। यह कंपन व्यक्तित्व संरचना के भीतर अत्यधिक हावी हो जाता है और व्यवहार, भावनात्मक प्रतिक्रियाओं और जीवन की दिशा को दृढ़ता से प्रभावित करता है।",
        'report_free_title': "📥 पूर्ण डिजिटल विश्लेषण रिपोर्ट प्राप्त करें",
        'report_free_desc': "आपकी डिजिटल विश्लेषण और संरचनात्मक मूल्यांकन रिपोर्ट हमारी कम्प्यूटेशनल इंटेलिजेंस मैट्रिक्स द्वारा सफलतापूर्वक संकलित की गई है। आप इसे सहेज सकते हैं या नीचे दिए गए विवरण का उपयोग करके सीधे परामर्श कर सकते हैं।",
        'free_badge': "मुफ़्त डिजिटल एक्सेस",
        'unlocked_status': "अनलॉक किया गया"
    },
    'as': {
        'title': "🔮 নিউমেৰ’ আনন্দ এআই",
        'subtitle': "গভীৰ শক্তি বিশ্লেষণ, পেছাদাৰী সংখ্যাবিজ্ঞান বুদ্ধিমত্তা, ব্যক্তিত্ব ব্যাখ্যা ব্যৱস্থা, কেৰিয়াৰ নিৰ্দেশনা এলগৰিদম, কৰ্মৰ কম্পন ডিক’ডিং আৰু ভৱিষ্যতৰ আধ্যাত্মিক বিশ্লেষণৰ দ্বাৰা পৰিচালিত উন্নত প্ৰিমিয়াম লো শ্বু গ্ৰীড সংখ্যাবিজ্ঞান মঞ্চ।",
        'workspace': "কৰ্মক্ষেত্ৰ মেনু",
        'input_name': "বিশ্লেষণৰ বাবে নাম",
        'input_dob': "জন্মৰ তাৰিখ",
        'input_mobile': "ম’বাইল নম্বৰ (ঐচ্ছিক)",
        'btn_analyze': "এতিয়াই বিশ্লেষণ কৰক",
        'consult_folder': "📞 পৰামৰ্শ ফ’ল্ডাৰ",
        'strategist': "মুখ্য ৰণনীতিবিদ:",
        'connect_wa': "💬 হোৱাটছএপত সংযোগ কৰক",
        'charges_title': "⏰ ৰণনৈতিক বিশ্লেষণৰ স্থিতি:",
        'free_access': "পূৰ্ণ চিষ্টেম একচেছ: <b style='color:#00ff88;'>বিনামূলীয়া (FREE)</b>",
        'btn_consult': "আনন্দ শৰ্মাৰ সৈতে পৰামৰ্শ কৰক",
        'wa_group_title': "👥 হোৱাটছএপ গ্ৰুপ ফ’ল্ডাৰ",
        'btn_group': "হোৱাটছএপ গ্ৰুপ খোলক",
        'footer': "নিউমেৰ’ আনন্দ এআই • প্ৰিমিয়াম সংখ্যাবিজ্ঞান মঞ্চ",
        'welcome_title': "✨ নিউমেৰ’ আনন্দ এআইলৈ স্বাগতম",
        'card1_t': "🔢 লো শ্বু গ্ৰীড ইণ্টেলিজেন্স",
        'card1_d': "প্ৰাচীন লো শ্বু গ্ৰীড ব্যৱস্থাক উন্নত এআই-চালিত শক্তিৰ ব্যাখ্যা আৰু গভীৰ মানসিক ডিক’ডিঙৰ সৈতে উন্নত কৰা হৈছে।",
        'card2_t': "🧠 ব্যক্তিত্বৰ ব্লুপ্ৰিণ্ট",
        'card2_d': "লুকাই থকা আচৰণৰ আৰ্হি, কৰ্মৰ শক্তি, আৱেগিক প্ৰৱণতা আৰু অৱচেতন ব্যক্তিত্বৰ গঠন আৱিষ্কাৰ কৰক।",
        'card3_t': "💼 কেৰিয়াৰ আৰু ধনৰ নিৰ্দেশনা",
        'card3_d': "আৰ্থিক কম্পন, ব্যৱসায়িক সফলতাৰ সূচক, নেতৃত্বৰ আৰ্হি আৰু সমৃদ্ধিৰ সংৰেখন বুজি পাওক।",
        'card4_t': "❤️ সম্পৰ্কৰ উপযোগিতা",
        'card4_d': "আৱেগিক অনুৰণন, যোগাযোগৰ সমন্বয়, বিবাহৰ উপযোগিতা আৰু সম্পৰ্কৰ শক্তি প্ৰবাহ বিশ্লেষণ কৰক।",
        'card5_t': "🧿 প্ৰতিকাৰ আৰু ভাৰসাম্য",
        'card5_d': "হেৰাই যোৱা শক্তিসমূহৰ ভাৰসাম্য ৰক্ষা কৰিবলৈ আৰু জীৱনৰ স্থিৰতা উন্নত কৰিবলৈ ব্যৱহাৰিক আধ্যাত্মিক প্ৰতিকাৰ লাভ কৰক।",
        'card6_t': "📈 ভৱিষ্যতৰ পূৰ্বানুমান",
        'card6_d': "ব্যক্তিগত বছৰৰ চক্ৰ, ভাগ্যৰ সময় বিশ্লেষণ, বাৰ্ষিক নিৰ্দেশনা আৰু শক্তিৰ پێৰা-ভৱিষ্যদ্বাণী ব্যৱস্থা।",
        'p1_title': "📘 পৃষ্ঠা ১ — মূল সংখ্যাবিজ্ঞান প্ৰফাইল",
        'lbl_name': "পূৰ্ণ নাম",
        'lbl_dob': "জন্মৰ তাৰিখ",
        'lbl_driver': "ড্ৰাইভৰ নম্বৰ (মূলাংক)",
        'lbl_conductor': "কণ্ডাক্টৰ নম্বৰ (ভাগ্যাংক)",
        'lbl_name_num': "নামৰ সংখ্যা",
        'lbl_compound': "মিশ্ৰিত নামৰ মূল্য",
        'eb_score': "⚡ শক্তি ভাৰসাম্যৰ স্ক’ৰ",
        'eb_desc': "আপোনাৰ শক্তিৰ উপযোগিতা স্ক’ৰ ড্ৰাইভৰ নম্বৰ, ভাগ্যৰ কম্পন, লো শ্বু গ্ৰীড গঠন, হেৰাই যোৱা সংখ্যা উদ্ধাৰৰ সম্ভাৱনা আৰু চালডিয়ান নামৰ অনুৰণন আৰ্হিৰ মাজত সমন্বয়ৰ জৰিয়তে গণনা কৰা হয়।",
        'p_snap': "🧠 ব্যক্তিত্বৰ আভাস",
        'p_desc': "ড্ৰাইভৰ নম্বৰ {driver}-এ আপোনাৰ সহজাত আচৰণ, প্ৰাকৃতিক প্ৰতিক্ৰিয়া, অৱচেতন ব্যক্তিত্বৰ গঠন আৰু সিদ্ধান্ত গ্ৰহণৰ মনস্তত্ত্বক তীব্ৰভাৱে প্ৰভাৱিত কৰে।<br><br>কণ্ডাক্টৰ নম্বৰ {conductor}-এ দীৰ্ঘম্যাদী ভাগ্যৰ আৰ্হি, কৰ্মৰ বিৱৰ্তন, ৰাজহুৱা পৰিচয় আৰু জীৱনৰ দিশ নিয়ন্ত্ৰণ কৰে।<br><br>আপোনাৰ নামৰ সংখ্যাৰ কম্পন {name_single}-এ সামাজিক স্বীকৃতি, বাহ্যিক সুযোগ, যোগাযোগৰ আকৰ্ষণ আৰু সমাজৰ পৰা অহা শক্তিৰ প্ৰতিক্ৰিয়াক গঢ় দিয়ে।",
        'c_meter': "📊 উপযোগিতা মিটাৰ",
        'c_desc': "বৰ্তমান নামৰ উপযোগিতা:",
        'p2_title': "📗 পৃষ্ঠা ২ — পূৰ্ণ লো শ্বু গ্ৰীড বিশ্লেষণ",
        'missing_t': "🔍 হেৰাই যোৱা সংখ্যাসমূহ",
        'missing_desc': "আপোনাৰ লো শ্বু গ্ৰীডত হেৰাই যোৱা সংখ্যাসমূহ হৈছে: <b>{missing}</b><br><br>এই অনুপস্থিত কম্পনসমূহে কৰ্মৰ শিক্ষা আৰু সচেতন বিকাশৰ প্ৰয়োজন হোৱা ক্ষেত্ৰসমূহক সূচায়।",
        'repeated_t': "🔥 পুনৰাবৃত্তি হোৱা সংখ্যাসমূহ",
        'repeated_desc': "পুনৰাবৃত্তি হোৱা সংখ্যা পোৱা গৈছে: <b>{repeated}</b><br><br>পুনৰাবৃত্তি হোৱা কম্পনে শক্তিৰ তীব্ৰতা বৃদ্ধি কৰে আৰু নিৰ্দিষ্ট ব্যক্তিত্বৰ মাত্ৰাক প্ৰসাৰিত কৰে।",
        'mental_t': "🧠 মানসিক তলৰ বিশ্লেষণ",
        'mental_desc': "মানসিক তলে বৌদ্ধিক স্পষ্টতা, পৰিকল্পনাৰ ক্ষমতা, স্মৃতিশক্তিৰ গঠন আৰু বিশ্লেষণাত্মক দৃষ্টিকোণ প্ৰতিফলিত কৰে। শক্তিশালী মানসিক সংখ্যাই ৰণনৈতিক বুদ্ধিমত্তা আৰু শক্তিশালী ভিজুৱেলীকৰণৰ ক্ষমতা সূচায়।",
        'emotional_t': "❤️ আৱেগিক তলৰ বিশ্লেষণ",
        'emotional_desc': "আৱেগিক তলে সহানুভূতি, আৱেগিক প্ৰতিক্ৰিয়া, অন্তৰ্দৃষ্টি, কৰুণা আৰু সম্পৰ্কৰ সংবেদনশীলতাক প্ৰতিনিধিত্ব কৰে। সন্তুলিত আৱেগিক সংখ্যাই সমন্বয়, আৱেগিক পৰিপক্কতা আৰু যোগাযোগৰ গুণগত মান উন্নত কৰে।",
        'practical_t': "💼 ব্যৱহাৰিক তলৰ বিশ্লেষণ",
        'practical_desc': "ব্যৱহাৰিক তলে কাৰ্য্যকৰীকৰণ ক্ষমতা, অনুশাসন, আৰ্থিক স্থিৰতা, ধাৰাবাহিকতা আৰু কেৰিয়াৰ ৰূপায়ণ নিয়ন্ত্ৰণ কৰে। শক্তিশালী ব্যৱহাৰিক সংখ্যাই সংৰচিত প্ৰগতি আৰু ভৌতিক সফলতাৰ সম্ভাৱনা সৃষ্টি কৰে।",
        'p3_title': "📙 পৃষ্ঠা ৩ — উন্নত মানসিক আৰু আধ্যাত্মিক বিশ্লেষণ",
        'arrow_t': "🧿 তীৰ (Arrow) বিশ্লেষণ",
        'arrow_desc': "আপোনাৰ লো শ্বু গ্ৰীডে দৃঢ় সংকল্প, ইচ্ছাশক্তি, আৱেগিক নিয়ন্ত্ৰণ, আধ্যাত্মিকতা, অনুশাসন আৰু যোগাযোগৰ শৈলীক প্ৰভাৱিত কৰা গোপন শক্তিৰ পথসমূহ প্ৰকাশ কৰে। শক্তিশালী তীৰে আভ্যন্তৰীণ সংৰেখন উন্নত কৰে আনহাতে ভঙা তীৰে কৰ্মৰ শিক্ষণ ক্ষেত্ৰসমূহ প্ৰকাশ কৰে।",
        'raj_t': "👑 ৰাজ যোগৰ সম্ভাৱনা",
        'raj_desc': "আপোনাৰ ড্ৰাইভৰ নম্বৰ, ভাগ্যৰ কম্পন আৰু লো শ্বু গঠনৰ মাজৰ মিথষ্ক্ৰিয়াই স্বীকৃতি, কৰ্তৃত্ব, নেতৃত্ব আৰু দীৰ্ঘম্যাদী প্ৰভাৱৰ বাবে শক্তিশালী সম্ভাৱনাৰ ইংগিত দিয়ে। ধাৰাবাহিক অনুশাসন আৰু আৱেগিকভাৱে সন্তুলিত সিদ্ধান্ত গ্ৰহণে প্ৰকাশৰ শক্তিক লক্ষণীয়ভাৱে উন্নত কৰিব পাৰে।",
        'psych_t': "🧠 মানসিক বৈশিষ্ট্যসমূহ",
        'psych_desc': "আপোনাৰ ছাৰ্টে সচেতন উচ্চাকাঙ্ক্ষা আৰু অৱচেতন কৰ্মৰ স্মৃতিৰ আৰ্হি দুয়োটাৰে দ্বাৰা প্ৰভাৱিত এক গভীৰ মানসিক গঠনৰ ইংগিত দিয়ে। আপুনি স্বাভাৱিকতে সাময়িক প্ৰাপ্তিতকৈ অৰ্থ, স্থিৰতা, আৱেগিক সুৰক্ষা আৰু উদ্দেশ্যপূৰ্ণ বিকাশ বিচাৰিব পাৰে।",
        'spirit_t': "🪷 আধ্যাত্মিক বৈশিষ্ট্যসমূহ",
        'spirit_desc': "যেতিয়া আপোনাৰ আভ্যন্তৰীণ কম্পনে আৱেগিক স্পষ্টতা, শক্তিৰ ভাৰসাম্য আৰু গভীৰ জীৱনৰ উদ্দেশ্য বিচাৰিবলৈ আৰম্ভ কৰে, তেতিয়া আধ্যাত্মিক বিকাশ গুৰুত্বপূৰ্ণ হৈ পৰে। ধ্যান, আত্ম-সচেতনতা, অনুশাসিত দিনচৰ্যা আৰু ইতিবাচক পৰিৱেশে আধ্যাত্মিক স্থিৰতা উন্নত কৰে।",
        'p4_title': "📕 পৃষ্ঠা ৪ — নাম সংশোধন আৰু জীৱন নিৰ্দেশনা",
        'perf_msg': "✅ অভিনন্দন!<br><br>আপোনাৰ বৰ্তমান নামৰ কম্পন আপোনাৰ ড্ৰাইভৰ নম্বৰ ({driver}), কণ্ডাক্টৰ নম্বৰ ({conductor}), আৰু মূল লো শ্বু গ্ৰীডৰ কম্পনৰ সৈতে শক্তিশালীভাৱে সংৰেখিত হৈছে।<br><br>আপোনাৰ বিদ্যমান নামৰ শক্তিৰ গঠনে স্বাভাৱিকতে পৰিচয়ৰ স্থিৰতা, আৱেগিক ভাৰসাম্য, সিদ্ধান্ত লোৱাৰ ক্ষমতা আৰু দীৰ্ঘম্যাদী প্ৰকাশৰ ক্ষমতা সমৰ্থন কৰে।<br><br>আপোনাৰ নামে লো শ্বু গ্ৰীডৰ ভিতৰত কৰ্মৰ ব্যৱধান সুস্থিৰ কৰাত সহায় কৰে আৰু ব্যক্তিত্বৰ কম্পন আৰু ভাগ্যৰ কম্পনৰ মাজত এক উচ্চ সমবায় অনুৰণন সৃষ্টি কৰে।<br><br>কোনো সংশোধনৰ প্ৰয়োজন নাই কাৰণ আপোনাৰ বৰ্তমানৰ নামে ইতিমধ্যে এক পেছাদাৰীভাৱে সন্তুলিত সংখ্যাগত কম্পন বহন কৰিছে।",
        'imp_msg': "⚠️ নামৰ কম্পন সংশোধনৰ পৰামৰ্শ দিয়া হৈছে<br><br>আপোনাৰ বৰ্তমানৰ নামটো কাৰ্য্যকৰী, কিন্তু ই আপোনাৰ সম্পূৰ্ণ লো শ্বু গ্ৰীড গঠন আৰু ভাগ্যৰ কম্পনৰ সৈতে সম্পূৰ্ণৰূপে সজ্জীভুত নহয়।<br><br> ই কেৰিয়াৰৰ বিকাশ, আৱেগিক স্থিৰতা, আৰ্থিক প্ৰবাহ, সম্পৰ্কৰ সমন্বয়, বা আত্মবিশ্বাস প্ৰকাশৰ ক্ষেত্ৰত অদৃশ্য পলম সৃষ্টি কৰিব পাৰে।<br><br>এটা পেছাদাৰীভাৱে অপ্টিমাইজ কৰা বানানে শক্তিৰ ভাৰসাম্য, ৰাজহুৱা আকৰ্ষণ, মানসিক স্পষ্টতা আৰু দীৰ্ঘম্যাদী প্ৰকাশৰ সম্ভাৱনাক লক্ষণীয়ভাৱে উন্নত কৰিব পাৰে।",
        'sugg_title': "✨ পেছাদাৰীভাৱে পৰামৰ্শ দিয়া সংশোধিত নামসমূহ",
        'sugg_comp': "উন্নত উপযোগিতা:",
        'sugg_vib': "নতুন কম্পন নম্বৰ:",
        'sugg_reason': "এই বানানে ড্ৰাইভৰ নম্বৰ {driver} আৰু ভাগ্য নম্বৰ {conductor}ৰ সৈতে শক্তিশালী শক্তিৰ সমন্বয় প্ৰৱৰ্তন কৰে। ই আত্মবিশ্বাস, সুযোগ আকৰ্ষণ, ৰাজহুৱা প্ৰতিক্ৰিয়া, যোগাযোগৰ শক্তি আৰু ভৌতিক স্থিৰতাৰ সৈতে জড়িত কম্পন প্ৰবাহ উন্নত কৰে। সংশোধিত গঠনে হেৰাই যোৱা লো শ্বু কম্পনসমূহৰ ভাৰসাম্য ৰক্ষা কৰাত সহায় কৰে আৰু জন্ম কুণ্ডলীত দৃশ্যমান আভ্যন্তৰীণ শক্তিৰ সংঘাতসমূহ হ্ৰাস কৰে।",
        'career_t': "💼 কেৰিয়াৰ নিৰ্দেশনা",
        'career_desc': "আপোনাৰ সংখ্যাগত গঠনে যোগাযোগ, নিৰ্দেশনা, শিক্ষণ, ব্যৱস্থাপনা, আধ্যাত্মিকতা, পৰামৰ্শ, বিশ্লেষণ, ব্যৱসায়িক বিকাশ আৰু ৰাজহুৱা পাৰস্পৰিক ক্ৰিয়াৰ সৈতে জড়িত ক্ষেত্ৰসমূহক সমৰ্থন কৰে। দীৰ্ঘম্যাদী সফলতা তেতিয়াই উন্নত হয় যেতিয়া আৱেगিক ভাৰসাম্য আৰু অনুশাসিত দিনচৰ্যা ধাৰাবাহিকভাৱে বজাই ৰখা হয়।",
        'rel_t': "❤️ সম্পৰ্কৰ নিৰ্দেশনা",
        'rel_desc': "ধৈৰ্য্য, আৱেগিক মুকলিপন, সন্তুলিত যোগাযোগ আৰু পাৰস্পৰিক বুজাবুজিৰ জৰিয়তে সম্পৰ্কৰ সমন্বয় উন্নত হয়। আপোনাৰ আৱেগিক কম্পনে সম্পৰ্কৰ ভিতৰত আন্তৰিকতা, সন্মান, আনুগত্য আৰু মানসিক গভীৰতা বিচাৰে।",
        'fin_t': "💰 আৰ্থিক নিৰ্দেশনা",
        'fin_desc': "ৰণনৈতিক পৰিকল্পনা, দীৰ্ঘম্যাদী অনুশাসন আৰু ব্যৱহাৰিক ধন ব্যৱস্থাপনাৰ জৰিয়তে আৰ্থিক স্থিৰতা বৃদ্ধি পায়। আৱেগিকভাৱে অস্থিৰ সময়ছোৱাত আবেগিক আৰ্থিক সিদ্ধান্ত লোৱাৰ পৰা বিৰত থাকক।",
        'lucky_t': "🍀 ভাগ্যশালী সূচকসমূহ",
        'l_num': "ভাগ্যশালী সংখ্যাসমূহ:",
        'l_days': "ভাগ্যশালী দিন: দেওবাৰ, বুধবাৰ, শুক্ৰবাৰ",
        'l_cols': "ভাগ্যশালী ৰং: একুৱা ব্লু, বগা, মৰকত সেউজীয়া",
        'l_dirs': "ভাগ্যশালী দিশ: পূব আৰু উত্তৰ-পূব",
        'l_time': "ভাগ্যশালী সময়: পুৱা ৬ বজাৰ পৰা ১০ বজালৈ",
        'p5_title': "导 পৃষ্ঠা ৫ — গভীৰ এআই পেছাদাৰী প্ৰতিবেদন",
        'human_t': "🧠 মানুহৰ দৰে গভীৰ ব্যাখ্যা",
        'human_desc': "আপোনাৰ সম্পূৰ্ণ সংখ্যাগত ব্লুপ্ৰিণ্টে বৌদ্ধিক সংবেদনশীলতা আৰু দীৰ্ঘম্যাদী বিকাশৰ সম্ভাৱনা দুয়োটাকে বহন কৰা এটা ব্যক্তিত্ব প্ৰকাশ কৰে। আপোনাৰ ড্ৰাইভৰ কম্পন, ভাগ্যৰ পথ আৰু নামৰ কম্পনৰ মাজৰ মিথষ্ক্রিয়াই আত্ম-বিকাশ, দায়িত্ব, আৱেগিক বিৱৰ্তন আৰু ক্ৰমান্বয়ে প্ৰকাশৰ ওপৰত কেন্দ্ৰিত এক জীৱনৰ আৰ্হি সৃষ্টি কৰে। আভ্যন্তৰীণ বিভ্ৰান্তিৰ সময়বোৰ সাধাৰণতে তেতিয়া দেখা দিয়ে যেতিয়া আৱেগিক চাপে যুক্তিসংগত গঠনক অতিক্ৰম কৰে। অৱশ্যে, আপোনাৰ ছাৰ্টে শক্তিশালী পুনৰুদ্ধাৰৰ ক্ষমতা, স্থিতিস্থাপকতা আৰু অভিযোজনক্ষমতাও প্ৰকাশ কৰে। অনুশাসিত পৰিৱেশ, আৱেगিকভাৱে সহায়ক সম্পৰ্ক আৰু আধ্যাত্মিকভাৱে সন্তুলিত দিনচৰ্যাৰ ভিতৰত কাম কৰিলে আপোনাৰ শক্তি যথেষ্ট উন্নত হয়।",
        'year_t': "📈 বাৰ্ষিক পূৰ্বানুমান",
        'year_desc': "অহা শক্তিৰ চক্ৰটোৱে সংৰচিত সিদ্ধান্ত গ্ৰহণ, ৰণনৈতিক পৰিকল্পনা, আৰ্থিক সজাগতা আৰু আৱেগিক পৰিপক্কতাক সমৰ্থন কৰে। যোগাযোগ, নেটৱৰ্কিং, নিৰ্দেশনাৰ ভূমিকা, বা জ্ঞান ভাগ-বতৰা কৰা কাৰ্য্যকলাপৰ জৰিয়তে নতুন সুযোগৰ সৃষ্টি হ’ব পাৰে।",
        'road_t': "🪷 আধ্যাত্মিক ৰোডমেপ",
        'road_desc': "ধ্যান, কেন্দ্ৰীভূত দিনচৰ্যা, আধ্যাত্মিক পঢ়া, কৃতজ্ঞতা অভ্যাস আৰু সন্তুলিত পৰিৱেশে আপোনাৰ শক্তি ক্ষেত্ৰখন সুস্থিৰ কৰাত সহায় কৰে। নেতিবাচক চৌপাশ, আৱেগিক অতিমাত্ৰা চিন্তা আৰু অসামঞ্জস্যপূৰ্ণ দিনচৰ্যা পৰিহাৰ কৰক।",
        'rem_t': "🧿 প্ৰতিকাৰসমূহ",
        'rem_li': "<li>প্ৰতিদিনে ১১ মিনিটকৈ ধ্যান কৰক।</li><li>সংৰচিত টোপনি আৰু কামৰ দিনচৰ্যা বজাই ৰাখক।</li><li>ধাৰাবাহিকভাৱে ইতিবাচক প্ৰতিশ্ৰুতি ব্যৱহাৰ কৰক।</li><li>দুৰ্বল লো শ্বু শক্তিসমূহ সচেতনভাৱে শক্তিশালী কৰক।</li><li>গুৰুত্বপূৰ্ণ কামৰ সময়ত পৰিষ্কাৰ পাতল ৰঙৰ কাপোৰ পিন্ধিব।</li><li>ডাঙৰ সিদ্ধান্তবোৰত আৱেগিক প্ৰৱণতা পৰিহাৰ কৰক।</li><li>গুৰুত্বপূৰ্ণ কাৰ্য্যৰ বাবে ভাগ্যশালী তাৰিখ ব্যৱহাৰ কৰক।</li>",
        'strat_t': "🚀 সফলতাৰ ৰণনীতি",
        'strat_desc': "দীৰ্ঘম্যাদী সফলতা তেতিয়াই আহে যেতিয়া আৱেগিক বুদ্ধিমত্তা, অনুশাসন, যোগাযোগৰ দক্ষতা আৰু আধ্যাত্মিক ভাৰসাম্যই একেলগে কাম কৰে। আপোনাৰ ছাৰ্টে হ্ৰস্বম্যাদী চুটি পথতকৈ ধৈৰ্য্য, সংৰচিত পৰিকল্পনা, ধাৰাবাহিকতা আৰু ইতিবাচক সামাজিক অৱদানক পুৰস্কৃত কৰে।",
        'freq_title': "📊 সম্পূৰ্ণ ফ্ৰিকুৱেন্সি विश्लेषण",
        'f_miss': "❌ লো শ্বু গ্ৰীডৰ পৰা {n} নম্বৰটো হেৰাই গৈছে। এই কম্পনৰ অনুপস্থিতিয়ে আৱেগিক পৰিপক্কতা, অনুশাসন, আত্মবিশ্বাস, স্থিৰতা বা জীৱন সংগঠনৰ সৈতে জড়িত গুৰুত্বপূৰ্ণ কৰ্মৰ শিক্ষাক সূচায়।",
        'f_one': "⚖️ {n} নম্বৰটো এবাৰ দেখা গৈছে। ই অত্যধিক আধিপত্য বা অভাৱ নোহোৱাকৈ স্বাভাৱিকভাৱে সন্তুলিত শক্তিৰ উপস্থিতিক সূচায়।",
        'f_two': "✅ {n} নম্বৰটো দুবাৰ দেখা গৈছে। ই এই সংখ্যাৰ দ্বাৰা পৰিচালিত মানসিক বিষয়সমূহৰ সৈते জড়িত শক্তিশালী সহায়ক শক্তিৰ সৃষ্টি কৰে।",
        'f_many': "🔥 {n} নম্বৰটো {c} বাৰ দেখা গৈছে। এই কম্পন ব্যক্তিত্বৰ গঠনৰ ভিতৰত অতিমাত্ৰা প্ৰভাৱশালী হৈ পৰে আৰু আচৰণ, আৱেগিক প্ৰতিক্ৰিয়া আৰু জীৱনৰ দিশক তীব্ৰভাৱে প্ৰভাৱিত কৰে।",
        'report_free_title': "📥 সম্পূৰ্ণ ডিজিটেল বিশ্লেষণ প্ৰতিবেদন লাভ কৰক",
        'report_free_desc': "আপোনাৰ ডিজিটেল বিশ্লেষণ আৰু গাঁথনিগত মূল্যায়ন প্ৰতিবেদন আমাৰ কম্পিউটেচনেল ইণ্টেলিজেন্স মেট্ৰিক্সৰ দ্বাৰা সফলতাৰে সংকলন কৰা হৈছে। আপুনি ইয়াক সংৰক্ষণ কৰিব পাৰে বা তলৰ বিৱৰণ ব্যৱহাৰ কৰি পোনপটীয়াকৈ পৰামৰ্শ কৰিব পাৰে।",
        'free_badge': "বিনামূলীয়া ডিজিটেল একচেছ",
        'unlocked_status': "আনলক কৰা হৈছে"
    }
}

# =========================================================
# ENGINE
# =========================================================

class NumerologyEngine:

    LOSHU_LAYOUT = [
        [4,9,2],
        [3,5,7],
        [8,1,6]
    ]

    def __init__(self,name,dob,mobile=""):
        self.name = name.strip()
        self.dob = dob.strip()
        self.mobile = mobile.strip()

        self.driver = 0
        self.conductor = 0
        self.name_total = 0
        self.name_single = 0

        self.grid_numbers = []
        self.freq = {i:0 for i in range(1,10)}
        self.grid_map = {i:[] for i in range(1,10)}

        self.parsed_date = None

    # =========================================================

    def reduce(self,n,master=True):

        if master and n in MASTER_NUMBERS:
            return n

        while n > 9:

            n = sum(int(x) for x in str(n))

            if master and n in MASTER_NUMBERS:
                return n

        return n

    # =========================================================

    def parse_date(self):

        s = self.dob.replace("/","-").replace(".","-")

        if re.match(r"^\d{2}-\d{2}-\d{4}$",s):
            self.parsed_date = datetime.strptime(s,"%d-%m-%Y").date()
        else:
            self.parsed_date = parser.parse(s,dayfirst=True).date()

    # =========================================================

    def calculate(self):

        self.parse_date()

        digits = [int(x) for x in self.parsed_date.strftime("%d%m%Y") if x != "0"]

        self.grid_numbers = digits

        self.driver = self.reduce(self.parsed_date.day)

        full = self.parsed_date.day + self.parsed_date.month + self.parsed_date.year

        self.conductor = self.reduce(full)

        for n in digits + [self.driver,self.conductor]:

            if 1 <= n <= 9:
                self.freq[n] += 1
                self.grid_map[n].append(str(n))

        total = 0

        for ch in self.name.upper():

            if ch.isalpha():
                total += CHALDEAN_MAP.get(ch,0)

        self.name_total = total
        self.name_single = self.reduce(total)

    # =========================================================

    def loshu_html(self):

        html = "<table class='loshu'>"

        for row in self.LOSHU_LAYOUT:

            html += "<tr>"

            for n in row:

                vals = self.grid_map[n]

                if vals:
                    html += f"<td>{''.join(vals)}</td>"
                else:
                    html += "<td class='empty'>-</td>"

            html += "</tr>"

        html += "</table>"

        return html

    # =========================================================

    def compatibility_score(self):

        score = 0

        name_digit = self.reduce(self.name_single)

        d_rel = NUM_RELATIONS.get(self.driver,{})

        if name_digit in d_rel.get('friends',[]):
            score += 45
        elif name_digit in d_rel.get('neutral',[]):
            score += 25
        else:
            score += 8

        c_rel = NUM_RELATIONS.get(self.conductor,{})

        if name_digit in c_rel.get('friends',[]):
            score += 45
        elif name_digit in c_rel.get('neutral',[]):
            score += 25
        else:
            score += 8

        missing = [n for n in range(1,10) if self.freq[n] == 0]

        name_digits = [int(x) for x in str(self.name_total)]

        recovered = [x for x in missing if x in name_digits]

        score += min(10, len(recovered)*2)

        return min(100,score)

    # =========================================================

    def intelligent_name_analysis(self, lang='en'):

        score = self.compatibility_score()

        missing = [n for n in range(1,10) if self.freq[n] == 0]

        recovered = []

        for d in str(self.name_total):
            if int(d) in missing:
                recovered.append(int(d))

        recovered = list(set(recovered))

        # PERFECT NAME

        if score >= 85:
            msg = I18N[lang]['perf_msg'].format(driver=self.driver, conductor=self.conductor)
            return {
                "perfect":True,
                "score":score,
                "message":msg,
                "suggestions":[]
            }

        # NEED IMPROVEMENT

        suggestions = []

        test_names = [
            self.name + "h",
            self.name + " Raj",
            self.name + " Dev",
            self.name + " Anand",
            self.name + " Kumar",
            "Aar" + self.name,
            self.name + " Sharma",
            self.name + " Sai"
        ]

        used = set()

        for nm in test_names:

            total = 0

            for ch in nm.upper():

                if ch.isalpha():
                    total += CHALDEAN_MAP.get(ch,0)

            single = self.reduce(total)

            if single in NUM_RELATIONS[self.driver]['friends']:

                if nm not in used:

                    used.add(nm)

                    sc = random.randint(84,96)
                    reason_msg = I18N[lang]['sugg_reason'].format(driver=self.driver, conductor=self.conductor)

                    suggestions.append({
                        "name":nm,
                        "number":single,
                        "score":sc,
                        "reason":reason_msg
                    })

        return {
            "perfect":False,
            "score":score,
            "message":I18N[lang]['imp_msg'],
            "suggestions":suggestions[:3]
        }

# =========================================================
# PAGE TEMPLATE
# =========================================================

PAGE = """
<!DOCTYPE html>
<html>
<head>
<title>Numero Annand AI</title>
<meta name='viewport' content='width=device-width,initial-scale=1'>
""" + STYLE + """
</head>

<body>

<div class='hero'>
<h1>{{ t.title }}</h1>

<p>
{{ t.subtitle }}
</p>
</div>

<div class='main'>

<div class='sidebar'>

<h2 style='color:var(--accent);'>{{ t.workspace }}</h2>

<form method='POST' action='/analyze'>

<label>Language / भाषा / ভাষা</label>
<select name='lang' style='width:100%; padding:14px; margin-top:8px; margin-bottom:18px; background:#08101f; border:1px solid #314d79; border-radius:12px; color:white; font-size:15px;'>
    <option value='en' {% if lang == 'en' %}selected{% endif %}>English</option>
    <option value='hi' {% if lang == 'hi' %}selected{% endif %}>हिन्दी (Hindi)</option>
    <option value='as' {% if lang == 'as' %}selected{% endif %}>অসমীয়া (Assamese)</option>
</select>

<label>{{ t.input_name }}</label>
<input type='text' name='name' required value='{{name}}'>

<label>{{ t.input_dob }}</label>
<input type='text' name='dob' required placeholder='DD-MM-YYYY' value='{{dob}}'>

<label>{{ t.input_mobile }}</label>
<input type='text' name='mobile' value='{{mobile}}'>

<button type='submit'>{{ t.btn_analyze }}</button>

</form>

<hr style='border-color:#2c4166;margin:25px 0;'>

<div class='card'>

<h3>{{ t.consult_folder }}</h3>

<p class='small'>
{{ t.strategist }}
<br>
<b style='color:var(--accent);'>Annand Sarma</b>
</p>

<p class='small'>
Consultation Link:
<br>
<a href='{{whatsapp_chat}}' target='_blank' style='color:var(--accent); text-decoration:none; font-weight:bold;'>{{ t.connect_wa }}</a>
</p>

<p class='small'>
{{ t.charges_title }}
</p>

<ul class='small'>
<li>{{ t.free_access }}</li>
<li>Advance Lo Shu Grid Chart</li>
<li>Name Correction</li>
<li>Career Guidance</li>
<li>Relationship Guidance</li>
<li>Remedies & Future Guidance</li>
<li>Personalized Spiritual Consultation</li>
</ul>

<a href='{{whatsapp_chat}}' target='_blank'>
<button style='margin-top:10px;'>{{ t.btn_consult }}</button>
</a>

</div>

<div class='card'>

<h3>{{ t.wa_group_title }}</h3>

<a href='{{group}}' target='_blank'>
<button>{{ t.btn_group }}</button>
</a>

</div>

</div>

<div class='content'>
{{content|safe}}
</div>

</div>

<div class='zoom-controls'>
<button class='zoom-btn' onclick='zoomIn()'>+</button>
<button class='zoom-btn' onclick='zoomOut()'>−</button>
<button class='zoom-btn' onclick='resetZoom()'>⟳</button>
</div>

<div class='footer'>
{{ t.footer }}
</div>

</body>
</html>
"""

# =========================================================
# HOME
# =========================================================

@app.route('/')
def index():
    lang = request.args.get('lang', 'en')
    if lang not in I18N:
        lang = 'en'
        
    t = I18N[lang]

    home = f"""

<div class='card'>

<h2>{ t['welcome_title'] }</h2>

<div class='grid'>

<div class='card'>
<h3>{ t['card1_t'] }</h3>
<p class='small'>
{ t['card1_d'] }
</p>
</div>

<div class='card'>
<h3>{ t['card2_t'] }</h3>
<p class='small'>
{ t['card2_d'] }
</p>
</div>

<div class='card'>
<h3>{ t['card3_t'] }</h3>
<p class='small'>
{ t['card3_d'] }
</p>
</div>

<div class='card'>
<h3>{ t['card4_t'] }</h3>
<p class='small'>
{ t['card4_d'] }
</p>
</div>

<div class='card'>
<h3>{ t['card5_t'] }</h3>
<p class='small'>
{ t['card5_d'] }
</p>
</div>

<div class='card'>
<h3>{ t['card6_t'] }</h3>
<p class='small'>
{ t['card6_d'] }
</p>
</div>

</div>

</div>

"""

    return render_template_string(
        PAGE,
        content=home,
        name='',
        dob='',
        mobile='',
        whatsapp_chat=WHATSAPP_CHAT_LINK,
        group=WHATSAPP_GROUP_LINK,
        t=t,
        lang=lang
    )

# =========================================================
# ANALYZE
# =========================================================

@app.route('/analyze',methods=['POST'])
def analyze():

    try:
        lang = request.form.get('lang', 'en')
        if lang not in I18N:
            lang = 'en'
            
        t = I18N[lang]

        name = request.form.get('name','')
        dob = request.form.get('dob','')
        mobile = request.form.get('mobile','')

        engine = NumerologyEngine(name,dob,mobile)

        engine.calculate()

        check = engine.intelligent_name_analysis(lang=lang)

        score = engine.compatibility_score()

        missing = [n for n in range(1,10) if engine.freq[n] == 0]

        repeated = [n for n,c in engine.freq.items() if c >= 2]

        energy_score = random.randint(78,98)

        # Build specific language values dynamically
        snap_text = t['p_desc'].format(driver=engine.driver, conductor=engine.conductor, name_single=engine.name_single)
        miss_text = t['missing_desc'].format(missing=(missing if missing else 'None'))
        rep_text = t['repeated_desc'].format(repeated=(repeated if repeated else 'None'))

        result = f"""

<div class='card'>

<h2>{ t['p1_title'] }</h2>

<p><b>{ t['lbl_name'] }:</b> {name}</p>

<p><b>{ t['lbl_dob'] }:</b> {engine.parsed_date.strftime('%d-%m-%Y')}</p>

<p><b>{ t['lbl_driver'] }:</b> <span class='badge'>{engine.driver}</span></p>

<p><b>{ t['lbl_conductor'] }:</b> <span class='badge'>{engine.conductor}</span></p>

<p><b>{ t['lbl_name_num'] }:</b> <span class='badge'>{engine.name_single}</span></p>

<p><b>{ t['lbl_compound'] }:</b> <span class='badge'>{engine.name_total}</span></p>

<h3>{ t['eb_score'] }</h3>

<div class='meter'>
<div class='fill' style='width:{energy_score}%'></div>
</div>

<p class='small'>
{ t['eb_desc'] }
</p>

<h3>{ t['p_snap'] }</h3>

<p class='small'>
{ snap_text }
</p>

<h3>{ t['c_meter'] }</h3>

<div class='meter'>
<div class='fill' style='width:{score}%'></div>
</div>

<p class='small'>
{ t['c_desc'] }
<b>{score}%</b>
</p>

</div>

<div class='card'>

<h2>{ t['p2_title'] }</h2>

{engine.loshu_html()}

<h3>{ t['missing_t'] }</h3>

<p class='small'>
{ miss_text }
</p>

<h3>{ t['repeated_t'] }</h3>

<p class='small'>
{ rep_text }
</p>

<h3>{ t['mental_t'] }</h3>

<p class='small'>
{ t['mental_desc'] }
</p>

<h3>{ t['emotional_t'] }</h3>

<p class='small'>
{ t['emotional_desc'] }
</p>

<h3>{ t['practical_t'] }</h3>

<p class='small'>
{ t['practical_desc'] }
</p>

</div>

<div class='card'>

<h2>{ t['p3_title'] }</h2>

<h3>{ t['arrow_t'] }</h3>

<p class='small'>
{ t['arrow_desc'] }
</p>

<h3>{ t['raj_t'] }</h3>

<p class='small'>
{ t['raj_desc'] }
</p>

<h3>{ t['psych_t'] }</h3>

<p class='small'>
{ t['psych_desc'] }
</p>

<h3>{ t['spirit_t'] }</h3>

<p class='small'>
{ t['spirit_desc'] }
</p>

</div>

<div class='card'>

<h2>{ t['p4_title'] }</h2>

{"<div class='success'>" + check['message'] + "</div>" if check['perfect'] else "<div class='warning'>" + check['message'] + "</div>"}

"""

        if check['suggestions']:

            result += f"<h3>{ t['sugg_title'] }</h3>"

            for s in check['suggestions']:

                result += f"""
<div class='card'>

<h3>{s['name']}</h3>

<p><b>{ t['sugg_comp'] }</b> {s['score']}%</p>

<p><b>{ t['sugg_vib'] }</b> {s['number']}</p>

<p class='small'>
{s['reason']}
</p>

</div>
"""

        result += f"""

<h3>{ t['career_t'] }</h3>

<p class='small'>
{ t['career_desc'] }
</p>

<h3>{ t['rel_t'] }</h3>

<p class='small'>
{ t['rel_desc'] }
</p>

<h3>{ t['fin_t'] }</h3>

<p class='small'>
{ t['fin_desc'] }
</p>

<h3>{ t['lucky_t'] }</h3>

<ul>
<li>{ t['l_num'] } {engine.driver}, {engine.conductor}, {engine.name_single}</li>
<li>{ t['l_days'] }</li>
<li>{ t['l_cols'] }</li>
<li>{ t['l_dirs'] }</li>
<li>{ t['l_time'] }</li>
</ul>

</div>

<div class='card'>

<h2>{ t['p5_title'] }</h2>

<h3>{ t['human_t'] }</h3>

<p class='small'>
{ t['human_desc'] }
</p>

<h3>{ t['year_t'] }</h3>

<p class='small'>
{ t['year_desc'] }
</p>

<h3>{ t['road_t'] }</h3>

<p class='small'>
{ t['road_desc'] }
</p>

<h3>{ t['rem_t'] }</h3>

<ul>
{ t['rem_li'] }
</ul>

<h3>{ t['strat_t'] }</h3>

<p class='small'>
{ t['strat_desc'] }
</p>

<hr style='border-color:#243b60; margin:25px 0;'>

<div style='background:rgba(8,16,31,0.8); border:1px solid #314d79; padding:20px; border-radius:16px; text-align:center;'>
    <h3 style='color:var(--accent); margin-bottom:15px;'>{ t['report_free_title'] }</h3>
    
    <div class='grid' style='margin-bottom:20px;'>
        <div style='background:#10192d; border:1px solid var(--border); padding:12px; border-radius:12px; margin: 0 auto; max-width: 300px;'>
            <span style='font-weight:bold; color:var(--accent); display:block; font-size:16px;'>{ t['free_badge'] }</span>
            <span style='color:#00ff88; font-weight:bold; font-size:18px;'>{ t['unlocked_status'] }</span>
        </div>
    </div>

    <p class='small' style='color:var(--muted); line-height:1.6; margin:0;'>
        { t['report_free_desc'] }
    </p>
</div>

</div>

<div class='card'>

<h2>{ t['freq_title'] }</h2>

"""

        for n,c in engine.freq.items():

            if c == 0:
                result += f"<p class='small'>{ t['f_miss'].format(n=n) }</p>"
            elif c == 1:
                result += f"<p class='small'>{ t['f_one'].format(n=n) }</p>"
            elif c == 2:
                result += f"<p class='small'>{ t['f_two'].format(n=n) }</p>"
            else:
                result += f"<p class='small'>{ t['f_many'].format(n=n, c=c) }</p>"

        result += "</div>"

        return render_template_string(
            PAGE,
            content=result,
            name=name,
            dob=dob,
            mobile=mobile,
            whatsapp_chat=WHATSAPP_CHAT_LINK,
            group=WHATSAPP_GROUP_LINK,
            t=t,
            lang=lang
        )

    except Exception as e:

        return render_template_string(
            PAGE,
            content=f"""
<div class='card'>
<div class='warning'>
Error Detected:
<br><br>
{str(e)}
</div>
</div>
""",
            name='',
            dob='',
            mobile='',
            whatsapp_chat=WHATSAPP_CHAT_LINK,
            group=WHATSAPP_GROUP_LINK,
            t=I18N['en'],
            lang='en'
        )

# =========================================================
# RUN
# =========================================================

if __name__ == "__main__":
    app.run(debug=True, port=8501)
