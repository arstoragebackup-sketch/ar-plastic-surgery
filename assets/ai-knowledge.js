/* AR Plastic Surgery — Verified Clinic Knowledge Base
   All facts below are clinic-verified. Do not invent fees, availability, or credentials.
*/
var AR_KB = (function () {
  var CLINIC = {
    name: 'AR Plastic Surgery',
    doctor: 'Dr Ashok Reddy',
    qualifications: 'MBBS, DNB (Mumbai), M.Ch (Delhi), Gold Medalist',
    specialty: 'Plastic, Cosmetic & Hair Transplant Surgery',
    address: 'Dhruva Hospital, Karimnagar, Telangana, India',
    street: 'Opp. Reddy Gari Vantillu, Court Chowrasta, Karimnagar – 505001',
    phone: '+91 91826 56866',
    phoneDigits: '919182656866',
    hours: '10:00 AM – 8:00 PM, every day',
    rating: '4.9 stars on Google, 240+ patient reviews',
    bookingUrl: 'https://arstoragebackup-sketch.github.io/Booking/'
  };

  // Verified services. Each: names, explanation, why patients seek it,
  // process overview, recovery note, needs consultation, FAQs.
  var SERVICES = [
    {
      id: 'hair-transplant',
      names: { en: ['hair transplant', 'fue', 'hair loss', 'baldness'], te: ['జుట్టు', 'హెయిర్'], hi: ['बाल'] },
      title: { en: 'Hair Transplant', te: 'హెయిర్ ట్రాన్స్‌ప్లాంట్', hi: 'हेयर ट्रांसप्लांट' },
      explain: {
        en: 'Hair transplant moves your own healthy hair follicles to thinning or bald areas. We specialise in FUE, a minimally invasive technique with tiny dot scars.',
        te: 'మీ స్వంత ఆరోగ్యకరమైన జుట్టును తీసి పల్చని లేదా బట్టతల ప్రాంతంలో నాటుతాము. FUE పద్ధతిలో చిన్న మచ్చలు మాత్రమే ఉంటాయి.',
        hi: 'आपके अपने स्वस्थ बालों को लेकर पतले या गंजे हिस्सों में लगाया जाता है। FUE तकनीक से बहुत छोटे निशान रहते हैं।'
      },
      why: { en: 'Male pattern baldness, receding hairline, thinning crown.', te: 'బట్టతల, జుట్టు పల్చబడటం.', hi: 'गंजापन, बालों का पतला होना।' },
      process: { en: 'Consultation and hairline design, then a day procedure under local anaesthesia. Most patients return home the same day.', te: 'సంప్రదింపు తర్వాత లోకల్ అనస్థీషియాలో ఒక రోజు ప్రక్రియ.', hi: 'परामर्श के बाद लोकल एनेस्थीसिया में एक दिन की प्रक्रिया।' },
      recovery: { en: 'Mild redness for a few days. Transplanted hair sheds in 2–4 weeks, then regrows naturally over 6–12 months.', te: 'కొన్ని రోజులు ఎరుపు. 2–4 వారాల్లో జుట్టు రాలుతుంది, 6–12 నెలల్లో సహజంగా పెరుగుతుంది.', hi: 'कुछ दिनों तक हल्की लाली। 2–4 हफ्तों में बाल झड़ते हैं, फिर 6–12 महीनों में प्राकृतिक रूप से बढ़ते हैं।' },
      consultNeeded: true
    },
    {
      id: 'gynecomastia',
      names: { en: ['gynecomastia', 'male chest', 'chest enlargement', 'man boob'], te: ['ఛాతీ'], hi: ['छाती'] },
      title: { en: 'Gynecomastia Treatment', te: 'గైనకోమాస్టియా చికిత్స', hi: 'गाइनेकोमास्टिया उपचार' },
      explain: {
        en: 'Gynecomastia is enlargement of male breast tissue. It is treatable — usually with a small keyhole procedure combining liposuction and gland removal.',
        te: 'పురుషుల ఛాతీ పెరగడాన్ని గైనకోమాస్టియా అంటారు. చిన్న కీహోల్ ప్రక్రియతో చికిత్స చేయవచ్చు.',
        hi: 'पुरुषों में छाती का बढ़ना गाइनेकोमास्टिया कहलाता है। छोटी कीहोल प्रक्रिया से इसका इलाज संभव है।'
      },
      why: { en: 'Chest enlargement in men, embarrassment wearing fitted clothes.', te: 'పురుషుల ఛాతీ పెరుగుదల.', hi: 'पुरुषों में छाती का बढ़ना।' },
      process: { en: 'Assessment first — causes differ, so Dr Ashok Reddy examines you before recommending treatment.', te: 'ముందు పరీక్ష — కారణాలు వేర్వేరు కాబట్టి డాక్టర్ పరిశీలించాలి.', hi: 'पहले जांच — कारण अलग हो सकते हैं, इसलिए डॉक्टर जांच करेंगे।' },
      recovery: { en: 'Small incisions, quick recovery. A compression garment is usually worn for a few weeks.', te: 'చిన్న గాట్లు, త్వరగా కోలుకోవడం.', hi: 'छोटे चीरे, जल्दी ठीक होना।' },
      consultNeeded: true
    },
    {
      id: 'rhinoplasty',
      names: { en: ['rhinoplasty', 'nose job', 'nose surgery', 'nose shape'], te: ['ముక్కు'], hi: ['नाक'] },
      title: { en: 'Rhinoplasty (Nose Surgery)', te: 'రైనోప్లాస్టీ (ముక్కు సర్జరీ)', hi: 'राइनोप्लास्टी (नाक की सर्जरी)' },
      explain: {
        en: 'Rhinoplasty reshapes the nose — for appearance, breathing, or both. Each nose is different, so the plan is personalised.',
        te: 'ముక్కు ఆకారాన్ని సరిచేసే సర్జరీ — రూపం కోసం లేదా శ్వాస కోసం.',
        hi: 'नाक के आकार को ठीक करने की सर्जरी — रूप के लिए या सांस के लिए।'
      },
      why: { en: 'Hump, wide tip, asymmetry, breathing difficulty.', te: 'ముక్కు ఆకారం, శ్వాస సమస్య.', hi: 'नाक का आकार, सांस की समस्या।' },
      process: { en: 'Detailed consultation with photographs and measurements, then surgery under anaesthesia.', te: 'వివరణాత్మక సంప్రదింపు తర్వాత అనస్థీషియాలో సర్జరీ.', hi: 'विस्तृत परामर्श के बाद एनेस्थीसिया में सर्जरी।' },
      recovery: { en: 'Splint for about a week. Swelling settles over weeks; final shape refines over months.', te: 'ఒక వారం స్ప్లింట్. వాపు వారాల్లో తగ్గుతుంది.', hi: 'लगभग एक हफ्ते तक स्प्लिंट। सूजन हफ्तों में कम होती है।' },
      consultNeeded: true
    },
    {
      id: 'liposuction',
      names: { en: ['liposuction', 'lipo', 'fat removal', 'body contouring'], te: ['కొవ్వు'], hi: ['चर्बी'] },
      title: { en: 'Liposuction', te: 'లైపోసక్షన్', hi: 'लाइपोसक्शन' },
      explain: {
        en: 'Liposuction removes stubborn fat deposits that do not respond to diet and exercise. It shapes — it is not a weight-loss surgery.',
        te: 'ఆహారం, వ్యాయామంతో తగ్గని కొవ్వును తొలగిస్తాము. ఇది బరువు తగ్గే సర్జరీ కాదు.',
        hi: 'डाइट और व्यायाम से न घटने वाली चर्बी हटाई जाती है। यह वजन घटाने की सर्जरी नहीं है।'
      },
      why: { en: 'Stubborn belly, thigh, arm or chin fat.', te: 'మొండి కొవ్వు — పొట్ట, తొడలు.', hi: 'जिद्दी चर्बी — पेट, जांघें।' },
      process: { en: 'Assessment of fat distribution and skin quality, then a day procedure.', te: 'పరీక్ష తర్వాత ఒక రోజు ప్రక్రియ.', hi: 'जांच के बाद एक दिन की प्रक्रिया।' },
      recovery: { en: 'Compression garment for a few weeks. Light activity in days, full routine in 2–4 weeks.', te: 'కొన్ని వారాలు కంప్రెషన్ దుస్తులు.', hi: 'कुछ हफ्तों तक कंप्रेशन कपड़े।' },
      consultNeeded: true
    },
    {
      id: 'breast',
      names: { en: ['breast augmentation', 'breast reduction', 'breast surgery', 'breast implant'], te: ['బ్రెస్ట్', 'రొమ్ము'], hi: ['स्तन'] },
      title: { en: 'Breast Surgery', te: 'బ్రెస్ట్ సర్జరీ', hi: 'ब्रेस्ट सर्जरी' },
      explain: {
        en: 'We offer breast augmentation and breast reduction, planned carefully around your body and goals.',
        te: 'బ్రెస్ట్ ఆగ్మెంటేషన్ మరియు రిడక్షన్ చేస్తాము.',
        hi: 'ब्रेस्ट ऑग्मेंटेशन और रिडक्शन किया जाता है।'
      },
      why: { en: 'Size concerns, asymmetry, back pain from large breasts.', te: 'పరిమాణ సమస్యలు, నొప్పి.', hi: 'आकार की समस्या, दर्द।' },
      process: { en: 'In-depth consultation about options, then surgery under anaesthesia.', te: 'వివరణాత్మక సంప్రదింపు తర్వాత సర్జరీ.', hi: 'विस्तृत परामर्श के बाद सर्जरी।' },
      recovery: { en: 'Supportive garments, rest for 1–2 weeks, gradual return to activity.', te: '1–2 వారాలు విశ్రాంతి.', hi: '1–2 हफ्ते आराम।' },
      consultNeeded: true
    },
    {
      id: 'tummy-tuck',
      names: { en: ['tummy tuck', 'abdominoplasty', 'belly', 'abdomen'], te: ['పొట్ట'], hi: ['पेट'] },
      title: { en: 'Tummy Tuck (Abdominoplasty)', te: 'టమ్మీ టక్', hi: 'टमी टक' },
      explain: {
        en: 'A tummy tuck removes excess abdominal skin and tightens weakened muscles — often after pregnancy or major weight loss.',
        te: 'పొట్టలోని అదనపు చర్మాన్ని తొలగించి కండరాలను బిగిస్తాము.',
        hi: 'पेट की अतिरिक्त त्वचा हटाकर मांसपेशियों को कसा जाता है।'
      },
      why: { en: 'Loose skin after pregnancy or weight loss.', te: 'ప్రసవం లేదా బరువు తగ్గిన తర్వాత వదులు చర్మం.', hi: 'प्रसव या वजन घटने के बाद ढीली त्वचा।' },
      process: { en: 'Consultation and planning, then surgery under general anaesthesia with a short hospital stay.', te: 'సంప్రదింపు తర్వాత జనరల్ అనస్థీషియాలో సర్జరీ.', hi: 'परामर्श के बाद जनरल एनेस्थीसिया में सर्जरी।' },
      recovery: { en: 'Rest 2–3 weeks, avoid strain for 6 weeks. Scars fade over months.', te: '2–3 వారాలు విశ్రాంతి.', hi: '2–3 हफ्ते आराम।' },
      consultNeeded: true
    },
    {
      id: 'lipoma',
      names: { en: ['lipoma', 'lump', 'fat lump', 'cyst'], te: ['గడ్డ'], hi: ['गांठ'] },
      title: { en: 'Lipoma Removal', te: 'లైపోమా తొలగింపు', hi: 'लाइपोमा हटाना' },
      explain: {
        en: 'Lipomas are soft, harmless fat lumps under the skin. Small ones are removed easily under local anaesthesia.',
        te: 'చర్మం కింద కొవ్వు గడ్డలు. లోకల్ అనస్థీషియాలో సులభంగా తొలగించవచ్చు.',
        hi: 'त्वचा के नीचे चर्बी की गांठें। लोकल एनेस्थीसिया में आसानी से हटाई जाती हैं।'
      },
      why: { en: 'Visible or uncomfortable lumps.', te: 'కనిపించే లేదా ఇబ్బంది కలిగించే గడ్డలు.', hi: 'दिखने वाली या परेशान करने वाली गांठें।' },
      process: { en: 'Quick clinic procedure under local anaesthesia, usually under 30 minutes.', te: '30 నిమిషాల్లోపు క్లినిక్ ప్రక్రియ.', hi: '30 मिनट के अंदर क्लिनिक प्रक्रिया।' },
      recovery: { en: 'Tiny scar, back to routine the same day or next.', te: 'చిన్న మచ్చ, వెంటనే మామూలు జీవితం.', hi: 'छोटा निशान, तुरंत सामान्य जीवन।' },
      consultNeeded: true
    },
    {
      id: 'prp',
      names: { en: ['prp', 'platelet', 'hair treatment without surgery'], te: ['పీఆర్పీ'], hi: ['पीआरपी'] },
      title: { en: 'PRP Therapy', te: 'పీఆర్పీ చికిత్స', hi: 'पीआरपी थेरेपी' },
      explain: {
        en: 'PRP uses growth factors from your own blood to support hair regrowth and skin rejuvenation. Non-surgical, under an hour per session.',
        te: 'మీ స్వంత రక్తం నుండి జుట్టు పెరుగుదలకు చికిత్స. శస్త్రచికిత్స లేదు.',
        hi: 'आपके अपने खून से बालों के विकास के लिए उपचार। कोई सर्जरी नहीं।'
      },
      why: { en: 'Early hair thinning, as an adjunct — not a replacement for transplant.', te: 'ప్రారంభ జుట్టు పల్చబడటం.', hi: 'शुरुआती बाल पतला होना।' },
      process: { en: 'Blood drawn, spun in a centrifuge, injected. Usually 3–4 monthly sessions.', te: 'రక్తం తీసి, సెంట్రిఫ్యూజ్ చేసి ఇంజెక్ట్ చేస్తాము. 3–4 నెలవారీ సెషన్లు.', hi: 'खून लेकर, सेंट्रीफ्यूज करके इंजेक्ट किया जाता है। 3–4 मासिक सत्र।' },
      recovery: { en: 'No downtime. Mild redness for hours.', te: 'విశ్రాంతి అవసరం లేదు.', hi: 'आराम की जरूरत नहीं।' },
      consultNeeded: true
    },
    {
      id: 'hand-surgery',
      names: { en: ['hand surgery', 'hand injury', 'tendon', 'finger', 'fracture hand'], te: ['చేయి', 'వేలు'], hi: ['हाथ', 'उंगली'] },
      title: { en: 'Hand & Microvascular Surgery', te: 'హ్యాండ్ సర్జరీ', hi: 'हैंड सर्जरी' },
      explain: {
        en: 'Dr Ashok Reddy is also a trained hand and microvascular surgeon — treating tendon injuries, fractures, nerve injuries and fingertip replantation.',
        te: 'డా. అశోక్ రెడ్డి గారు హ్యాండ్ మరియు మైక్రోవాస్కులర్ సర్జన్ కూడా.',
        hi: 'डॉ. अशोक रेड्डी हैंड और माइक्रोवैस्कुलर सर्जन भी हैं।'
      },
      why: { en: 'Cuts, fractures, tendon or nerve injuries of the hand.', te: 'చేతి గాయాలు, ఎముక విరగడం.', hi: 'हाथ की चोटें, हड्डी टूटना।' },
      process: { en: 'Urgent assessment for injuries; planned surgery for old problems.', te: 'గాయాలకు తక్షణ పరీక్ష.', hi: 'चोटों के लिए तत्काल जांच।' },
      recovery: { en: 'Hand therapy is often part of recovery for best movement.', te: 'కోలుకోవడంలో హ్యాండ్ థెరపీ ముఖ్యం.', hi: 'ठीक होने में हैंड थेरेपी महत्वपूर्ण है।' },
      consultNeeded: true
    },
    {
      id: 'botox-fillers',
      names: { en: ['botox', 'filler', 'wrinkle', 'anti-ageing', 'dermal'], te: ['బోటాక్స్'], hi: ['बोटॉक्स'] },
      title: { en: 'Botox & Dermal Fillers', te: 'బోటాక్స్ & ఫిల్లర్లు', hi: 'बोटॉक्स और फिलर्स' },
      explain: {
        en: 'Botox softens dynamic wrinkles; fillers restore volume. Quick clinic treatments with natural-looking results.',
        te: 'ముడతలకు బోటాక్స్, వాల్యూమ్‌కు ఫిల్లర్లు. త్వరిత క్లినిక్ చికిత్సలు.',
        hi: 'झुर्रियों के लिए बोटॉक्स, वॉल्यूम के लिए फिलर्स। त्वरित क्लिनिक उपचार।'
      },
      why: { en: 'Forehead lines, frown lines, volume loss.', te: 'ముడతలు, వాల్యూమ్ తగ్గడం.', hi: 'झुर्रियां, वॉल्यूम घटना।' },
      process: { en: 'Consultation, then injections in minutes. Numbing cream used.', te: 'సంప్రదింపు తర్వాత నిమిషాల్లో ఇంజెక్షన్లు.', hi: 'परामर्श के बाद मिनटों में इंजेक्शन।' },
      recovery: { en: 'No downtime. Results last months; maintenance needed.', te: 'విశ్రాంతి అవసరం లేదు. ఫలితాలు నెలలు ఉంటాయి.', hi: 'आराम की जरूरत नहीं। परिणाम महीनों रहते हैं।' },
      consultNeeded: true
    },
    {
      id: 'scar',
      names: { en: ['scar', 'keloid', 'scar revision'], te: ['మచ్చ'], hi: ['निशान'] },
      title: { en: 'Scar Revision', te: 'స్కార్ చికిత్స', hi: 'निशान उपचार' },
      explain: {
        en: 'We improve scars from surgery, injury or burns — with revision surgery, laser, or injections depending on the scar.',
        te: 'సర్జరీ, గాయం లేదా కాలిన గాయాల మచ్చలను మెరుగుపరుస్తాము.',
        hi: 'सर्जरी, चोट या जलने के निशानों को सुधारा जाता है।'
      },
      why: { en: 'Raised, wide or discoloured scars.', te: 'ఎత్తైన లేదా వెడల్పాటి మచ్చలు.', hi: 'उभरे या चौड़े निशान।' },
      process: { en: 'Scar assessment first, then a tailored plan.', te: 'ముందు మచ్చ పరీక్ష, తర్వాత ప్రణాళిక.', hi: 'पहले निशान की जांच, फिर योजना।' },
      recovery: { en: 'Depends on treatment; most are minor procedures.', te: 'చికిత్సను బట్టి ఉంటుంది.', hi: 'उपचार पर निर्भर करता है।' },
      consultNeeded: true
    },
    {
      id: 'burn',
      names: { en: ['burn', 'burn reconstruction', 'contracture'], te: ['కాలిన'], hi: ['जलना'] },
      title: { en: 'Burn Reconstruction', te: 'బర్న్ పునర్నిర్మాణం', hi: 'बर्न पुनर्निर्माण' },
      explain: {
        en: 'We treat burn scars and contractures that limit movement — with skin grafting, flaps, and therapy.',
        te: 'కాలిన గాయాల మచ్చలు మరియు కదలికను పరిమితం చేసే సమస్యలకు చికిత్స.',
        hi: 'जलने के निशानों और गति सीमित करने वाली समस्याओं का इलाज।'
      },
      why: { en: 'Tight burn scars limiting movement.', te: 'కదలికను పరిమితం చేసే మచ్చలు.', hi: 'गति सीमित करने वाले निशान।' },
      process: { en: 'Assessment, then staged reconstruction as needed.', te: 'పరీక్ష తర్వాత దశలవారీ పునర్నిర్మాణం.', hi: 'जांच के बाद चरणबद्ध पुनर्निर्माण।' },
      recovery: { en: 'Physiotherapy is key after burn reconstruction.', te: 'ఫిజియోథెరపీ చాలా ముఖ్యం.', hi: 'फिजियोथेरेपी बहुत महत्वपूर्ण है।' },
      consultNeeded: true
    }
  ];

  var EMERGENCY_WORDS = [
    'breathing difficulty', 'uncontrolled bleeding', 'heavy bleeding',
    'major facial trauma', 'accident', 'emergency',
    'శ్వాస', 'రక్తస్రావం', 'అత్యవసర', 'प्राण', 'खून', 'आपात'
  ];

  function detectLang(text) {
    if (/[\u0C00-\u0C7F]/.test(text)) return 'te';
    if (/[\u0900-\u097F]/.test(text)) return 'hi';
    return 'en';
  }

  function findService(text) {
    var t = text.toLowerCase();
    for (var i = 0; i < SERVICES.length; i++) {
      var s = SERVICES[i];
      var keys = s.names.en.concat(s.names.te).concat(s.names.hi);
      for (var j = 0; j < keys.length; j++) {
        if (keys[j].length > 2 && t.indexOf(keys[j].toLowerCase()) !== -1) return s;
      }
    }
    return null;
  }

  function isEmergency(text) {
    var t = text.toLowerCase();
    for (var i = 0; i < EMERGENCY_WORDS.length; i++) {
      if (t.indexOf(EMERGENCY_WORDS[i].toLowerCase()) !== -1) return true;
    }
    return false;
  }

  return {
    CLINIC: CLINIC,
    SERVICES: SERVICES,
    detectLang: detectLang,
    findService: findService,
    isEmergency: isEmergency
  };
})();
