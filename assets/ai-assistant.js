/* AR Plastic Surgery — Voice AI Engine
   State machine: idle -> listening -> thinking -> speaking
   Interruption: user speech stops assistant speech immediately.
   Languages: English, Telugu, Hindi with auto-detection.
*/
(function () {
  'use strict';
  var KB = null;
  var CLINIC = null;
  function ensureKB() {
    if (!KB && window.AR_KB) { KB = window.AR_KB; CLINIC = KB.CLINIC; }
    return KB;
  }

  var state = 'idle';           // idle | listening | thinking | speaking
  var lang = 'te';
  var voiceOn = true;
  var wantListen = true;
  var recog = null;
  var femaleVoice = null;
  var context = { service: null, name: '', mobile: '', datePref: '', apptStep: 0 };
  var greeted = false;

  /* ---------- STRINGS ---------- */
  var S = {
    te: {
      greeting: "నమస్కారం! AR ప్లాస్టిక్ సర్జరీకి స్వాగతం. నేను మీ వర్చువల్ క్లినిక్ అసిస్టెంట్‌ని. మా చికిత్సల గురించి తెలుసుకోవచ్చు, లేదా డా. అశోక్ రెడ్డి గారితో అపాయింట్‌మెంట్ అభ్యర్థించవచ్చు. నేను వింటున్నాను — మీరు మాట్లాడవచ్చు. మీకు ఎలా సహాయపడగలను?",
      listening: 'వింటున్నాను...', thinking: 'ఆలోచిస్తున్నాను...', speaking: 'మాట్లాడుతున్నాను...',
      askService: 'మీకు ఏ సేవ కావాలో చెప్పండి — ఉదాహరణకు హెయిర్ ట్రాన్స్‌ప్లాంట్, గైనకోమాస్టియా, లైపోసక్షన్.',
      askName: 'మీ పేరు చెప్పగలరా?',
      askMobile: 'ధన్యవాదాలు {name} గారు. మీ 10 అంకెల మొబైల్ నంబర్ చెప్పండి.',
      badMobile: 'క్షమించండి, అది సరైన నంబర్‌లా లేదు. దయచేసి 10 అంకెల మొబైల్ నంబర్ చెప్పండి.',
      askDate: 'మీకు ఎప్పుడు రావడం సౌకర్యంగా ఉంటుంది? — ఉదాహరణకు "రేపు సాయంత్రం" లేదా "శనివారం ఉదయం".',
      confirmAppt: 'సరే, నిర్ధారిస్తున్నాను: {name} గారు, {service} కోసం, మొబైల్ {mobile}, ఇష్టమైన సమయం: {date}. ఇది అపాయింట్‌మెంట్ అభ్యర్థన — క్లినిక్ సిబ్బంది నిర్ధారిస్తారు. బుకింగ్ పేజీకి తీసుకెళ్తున్నాను.',
      consultNote: 'ఖచ్చితమైన సలహా కోసం డాక్టర్‌ను కలవడం అవసరం. ప్రతి రోగి వేరు — పరీక్ష తర్వాతే సరైన చికిత్స నిర్ణయించగలము.',
      costHonest: 'ఖర్చు మీ కేసును బట్టి మారుతుంది. తప్పుడు ధర చెప్పడం నాకు ఇష్టం లేదు. సంప్రదింపులో డాక్టర్ ఖచ్చితంగా వివరిస్తారు.',
      scared: 'అర్థం చేసుకోగలను — సర్జరీ అంటే భయంగా ఉండటం సహజం. సంప్రదింపులో ఎంపికలు, ప్రయోజనాలు, నష్టాలు, కోలుకోవడం గురించి అన్నీ తెలుసుకోవచ్చు, నిర్ణయం తర్వాత.',
      emergency: 'దయచేసి వెంటనే అత్యవసర వైద్య సహాయం తీసుకోండి లేదా దగ్గరి ఆసుపత్రికి వెళ్లండి. తీవ్రమైన లక్షణాలకు వేచి ఉండకండి. మా క్లినిక్ నంబర్: ' + '{PHONE}',
      dontKnow: 'దీని గురించి నాకు ఖచ్చితమైన సమాచారం లేదు. క్లినిక్ సిబ్బందిని అడగమని సూచిస్తున్నాను: ' + '{PHONE}',
      fallback: 'క్షమించండి, సరిగ్గా అర్థం కాలేదు. సేవలు, డాక్టర్, సమయం, ఖర్చు గురించి అడగండి — లేదా "అపాయింట్‌మెంట్" అని చెప్పండి.',
      hours: 'మేము ప్రతిరోజూ ఉదయం 10 నుండి రాత్రి 8 వరకు తెరిచి ఉంటాము.',
      location: 'మా చిరునామా: ధ్రువ హాస్పిటల్, కరీంనగర్. ' + '{STREET}',
      doctor: 'డా. అశోక్ రెడ్డి గారు — MBBS, DNB ముంబై, M.Ch ఢిల్లీ, గోల్డ్ మెడలిస్ట్. ప్లాస్టిక్, కాస్మెటిక్ మరియు హెయిర్ ట్రాన్స్‌ప్లాంట్ నిపుణులు. గూగుల్‌లో 4.9 స్టార్ రేటింగ్.',
      whatsappOffer: 'వాట్సాప్‌లో మాట్లాడాలనుకుంటున్నారా? "వాట్సాప్" అని చెప్పండి, లింక్ ఇస్తాను.',
      whatsappMsg: 'వాట్సాప్ తెరుస్తున్నాను — మీరు సిద్ధంగా ఉన్న సందేశాన్ని పంపవచ్చు.',
      endSession: 'ధన్యవాదాలు! మీకు సహాయం కావాలంటే మళ్లీ రండి. ఆరోగ్యంగా ఉండండి. 🙏',
      micDenied: 'మైక్రోఫోన్ అనుమతి అవసరం. దయచేసి బ్రౌజర్‌లో అనుమతించండి, లేదా టైప్ చేయండి.'
    },
    en: {
      greeting: "Hello! Welcome to AR Plastic Surgery. I'm your virtual clinic assistant. I can help you learn about our treatments, or request an appointment with Dr Ashok Reddy. I'm listening — how can I help you today?",
      listening: 'Listening...', thinking: 'Thinking...', speaking: 'Speaking...',
      askService: 'Which service do you need — for example hair transplant, gynecomastia, or liposuction?',
      askName: 'May I have your name, please?',
      askMobile: 'Thank you, {name}. Please share your 10-digit mobile number.',
      badMobile: "Sorry, that doesn't look right. Please share a 10-digit mobile number.",
      askDate: 'When would you prefer to come? For example "tomorrow evening" or "Saturday morning".',
      confirmAppt: 'Let me confirm: {name}, {service}, mobile {mobile}, preferred time: {date}. This is an appointment request — our staff will confirm it. Taking you to the booking page.',
      consultNote: 'For accurate advice, an in-person consultation is needed. Every patient is different — only an examination can decide the right treatment.',
      costHonest: "The cost depends on your individual case. I don't want to give you a wrong figure. The doctor will explain clearly during consultation.",
      scared: "That's completely understandable — feeling nervous about surgery is natural. A consultation lets you understand the options, benefits, risks and recovery before deciding anything.",
      emergency: 'Please seek immediate emergency medical care or go to the nearest hospital right away. Do not wait. Our clinic number is ' + '{PHONE}',
      dontKnow: "I don't have verified information about that. I'd suggest asking our clinic staff: " + '{PHONE}',
      fallback: 'Sorry, I didn\'t quite catch that. Ask about services, the doctor, timings, or cost — or say "appointment".',
      hours: "We're open every day from 10 AM to 8 PM.",
      location: 'Our address: Dhruva Hospital, Karimnagar. ' + '{STREET}',
      doctor: 'Dr Ashok Reddy — MBBS, DNB Mumbai, M.Ch Delhi, Gold Medalist. Specialist in plastic, cosmetic and hair transplant surgery. 4.9 stars on Google.',
      whatsappOffer: 'Would you like to chat on WhatsApp? Say "WhatsApp" and I\'ll share the link.',
      whatsappMsg: 'Opening WhatsApp — you can send the ready message.',
      endSession: 'Thank you! Come back anytime you need help. Take care. 🙏',
      micDenied: 'I need microphone permission. Please allow it in your browser, or type instead.'
    },
    hi: {
      greeting: 'नमस्ते! AR प्लास्टिक सर्जरी में आपका स्वागत है। मैं आपकी वर्चुअल क्लिनिक असिस्टेंट हूं। मैं सुन रही हूं — आज मैं आपकी कैसे मदद कर सकती हूं?',
      listening: 'सुन रही हूं...', thinking: 'सोच रही हूं...', speaking: 'बोल रही हूं...',
      askService: 'आपको कौन सी सेवा चाहिए — जैसे हेयर ट्रांसप्लांट, गाइनेकोमास्टिया, या लाइपोसक्शन?',
      askName: 'कृपया अपना नाम बताइए?',
      askMobile: 'धन्यवाद {name} जी। अपना 10 अंकों का मोबाइल नंबर बताइए।',
      badMobile: 'क्षमा करें, यह सही नहीं लग रहा। कृपया 10 अंकों का मोबाइल नंबर बताइए।',
      askDate: 'आप कब आना चाहेंगे? जैसे "कल शाम" या "शनिवार सुबह"।',
      confirmAppt: 'पुष्टि करती हूं: {name} जी, {service}, मोबाइल {mobile}, पसंदीदा समय: {date}। यह अपॉइंटमेंट अनुरोध है — हमारा स्टाफ पुष्टि करेगा। बुकिंग पेज पर ले जा रही हूं।',
      consultNote: 'सटीक सलाह के लिए डॉक्टर से मिलना जरूरी है। हर मरीज अलग है — जांच के बाद ही सही इलाज तय हो सकता है।',
      costHonest: 'खर्च आपके केस पर निर्भर करता है। गलत कीमत नहीं बताना चाहती। परामर्श में डॉक्टर स्पष्ट रूप से बताएंगे।',
      scared: 'यह बिल्कुल समझ में आता है — सर्जरी से डरना स्वाभाविक है। परामर्श में आप विकल्प, फायदे, जोखिम और ठीक होने के बारे में सब जान सकते हैं।',
      emergency: 'कृपया तुरंत आपातकालीन चिकित्सा सहायता लें या नजदीकी अस्पताल जाएं। इंतजार न करें। हमारा क्लिनिक नंबर: ' + '{PHONE}',
      dontKnow: 'इसके बारे में मेरे पास सत्यापित जानकारी नहीं है। कृपया क्लिनिक स्टाफ से पूछें: ' + '{PHONE}',
      fallback: 'क्षमा करें, ठीक से समझ नहीं आया। सेवाओं, डॉक्टर, समय या खर्च के बारे में पूछें — या "अपॉइंटमेंट" कहें।',
      hours: 'हम रोज़ सुबह 10 से रात 8 बजे तक खुले हैं।',
      location: 'हमारा पता: ध्रुवा हॉस्पिटल, करीमनगर। ' + '{STREET}',
      doctor: 'डॉ. अशोक रेड्डी — MBBS, DNB मुंबई, M.Ch दिल्ली, गोल्ड मेडलिस्ट। प्लास्टिक, कॉस्मेटिक और हेयर ट्रांसप्लांट विशेषज्ञ। Google पर 4.9 स्टार रेटिंग।',
      whatsappOffer: 'क्या आप WhatsApp पर बात करना चाहेंगे? "WhatsApp" कहें, लिंक देती हूं।',
      whatsappMsg: 'WhatsApp खोल रही हूं — आप तैयार संदेश भेज सकते हैं।',
      endSession: 'धन्यवाद! जब भी मदद चाहिए, वापस आइए। अपना ख्याल रखिए। 🙏',
      micDenied: 'मुझे माइक्रोफोन की अनुमति चाहिए। कृपया ब्राउज़र में अनुमति दें, या टाइप करें।'
    }
  };

  function t(key, vars) {
    var s = (S[lang] && S[lang][key]) || S.en[key] || key;
    if (vars) for (var k in vars) s = s.replace('{' + k + '}', vars[k]);
    if (CLINIC) {
      s = s.split('{PHONE}').join(CLINIC.phone).split('{STREET}').join(CLINIC.street);
    }
    return s;
  }

  /* ---------- VOICE SELECTION (prefer female) ---------- */
  function pickVoice() {
    try {
      var voices = speechSynthesis.getVoices();
      if (!voices.length) return;
      var langTag = lang === 'te' ? 'te-IN' : lang === 'hi' ? 'hi-IN' : 'en-IN';
      var cands = voices.filter(function (v) { return v.lang && v.lang.indexOf(langTag.slice(0, 2)) === 0; });
      if (!cands.length) cands = voices.filter(function (v) { return v.lang && v.lang.indexOf('en') === 0; });
      // prefer female-sounding voice names
      var female = cands.find(function (v) {
        return /female|zira|samantha|veena|lekha|kanya|google uk english female|microsoft.*(zira|eva|aria)/i.test(v.name);
      });
      femaleVoice = female || cands[0] || voices[0];
    } catch (e) {}
  }
  if ('speechSynthesis' in window) {
    pickVoice();
    speechSynthesis.onvoiceschanged = pickVoice;
  }

  function speak(text) {
    if (!voiceOn || !('speechSynthesis' in window)) return;
    try {
      speechSynthesis.cancel();
      var clean = text.replace(/[🙏•]/g, '');
      // keep spoken turns short: first 2 sentences
      var short = clean.split(/(?<=[.!?।])/).slice(0, 2).join(' ').trim() || clean;
      var u = new SpeechSynthesisUtterance(short);
      u.lang = lang === 'te' ? 'te-IN' : lang === 'hi' ? 'hi-IN' : 'en-IN';
      u.rate = 0.95; u.pitch = 1.05;
      if (femaleVoice) u.voice = femaleVoice;
      u.onstart = function () {
        setState('speaking');
        var av = document.getElementById('ar-ai-avatar');
        if (av) av.classList.add('talking');
      };
      u.onend = function () {
        var av = document.getElementById('ar-ai-avatar');
        if (av) av.classList.remove('talking');
        if (state === 'speaking') setState('listening');
      };
      speechSynthesis.speak(u);
    } catch (e) {}
  }

  // Interruption: user speech stops assistant speech immediately
  function handleInterruption() {
    if (state === 'speaking' && 'speechSynthesis' in window) {
      speechSynthesis.cancel();
    }
  }

  /* ---------- UI ---------- */
  function setState(s) {
    state = s;
    var pill = document.getElementById('ar-ai-state');
    if (pill) {
      pill.textContent = t(s === 'listening' ? 'listening' : s === 'thinking' ? 'thinking' : s === 'speaking' ? 'speaking' : '');
      pill.className = 'ar-state ' + s;
      pill.style.display = s === 'idle' ? 'none' : 'inline-block';
    }
    var wave = document.getElementById('ar-ai-wave');
    if (wave) wave.className = 'ar-wave ' + s;
  }

  function addMsg(text, who) {
    var box = document.getElementById('ar-ai-messages');
    var div = document.createElement('div');
    div.className = 'ar-msg ' + who;
    div.textContent = text;
    box.appendChild(div);
    box.scrollTop = box.scrollHeight;
    if (who === 'bot') speak(text);
  }

  function showChips(items, cb) {
    var row = document.getElementById('ar-ai-quick');
    row.innerHTML = '';
    items.forEach(function (c) {
      var b = document.createElement('button');
      b.className = 'ar-chip'; b.textContent = c.label || c;
      b.onclick = function () { cb ? cb(c) : handleUserText(c.label || c); };
      row.appendChild(b);
    });
  }

  var SERVICE_ICONS = {
    'hair-transplant': '💇', 'gynecomastia': '👔', 'rhinoplasty': '👃',
    'liposuction': '⚖️', 'breast': '👚', 'tummy-tuck': '👗',
    'lipoma': '🔵', 'prp': '💉', 'hand-surgery': '🤲',
    'botox-fillers': '✨', 'scar': '🩹', 'burn': '🔥'
  };

  function showServiceCards() {
    var box = document.getElementById('ar-ai-messages');
    var wrap = document.createElement('div');
    wrap.className = 'ar-cards';
    KB.SERVICES.forEach(function (s) {
      var c = document.createElement('div');
      c.className = 'ar-card';
      c.innerHTML = '<div class="ic">' + (SERVICE_ICONS[s.id] || '🏥') + '</div>' +
        '<div class="nm">' + (s.title[lang] || s.title.en) + '</div>';
      c.onclick = function () { handleUserText(s.title[lang] || s.title.en); };
      wrap.appendChild(c);
    });
    box.appendChild(wrap);
    box.scrollTop = box.scrollHeight;
  }

  function showWelcomeHero() {
    var box = document.getElementById('ar-ai-messages');
    var h = document.createElement('div');
    h.className = 'ar-hero';
    var t1 = lang === 'te' ? 'AR ప్లాస్టిక్ సర్జరీకి <gold>స్వాగతం</gold>'
      : lang === 'hi' ? 'AR प्लास्टिक सर्जरी में <gold>स्वागत</gold>'
      : 'Welcome to <gold>AR Plastic Surgery</gold>';
    var t2 = lang === 'te' ? 'డా. అశోక్ రెడ్డి గారు • గోల్డ్ మెడలిస్ట్ • కరీంనగర్'
      : lang === 'hi' ? 'डॉ. अशोक रेड्डी • गोल्ड मेडलिस्ट • करीमनगर'
      : 'Dr Ashok Reddy • Gold Medalist • Karimnagar';
    h.innerHTML = '<div class="t1">' + t1 + '</div><div class="t2">' + t2 + '</div>';
    box.appendChild(h);
    box.scrollTop = box.scrollHeight;
  }

  function defaultChips() {
    var labels = {
      te: ['సేవలు', 'అపాయింట్‌మెంట్', 'డాక్టర్', 'సమయం', 'వాట్సాప్'],
      en: ['Services', 'Appointment', 'Doctor', 'Timings', 'WhatsApp'],
      hi: ['सेवाएं', 'अपॉइंटमेंट', 'डॉक्टर', 'समय', 'WhatsApp']
    };
    showChips(labels[lang] || labels.en);
  }

  /* ---------- CONVERSATION LOGIC ---------- */
  function handleUserText(text) {
    handleInterruption();
    if (!ensureKB()) { addMsg(t('dontKnow'), 'bot'); return; }
    addMsg(text, 'user');
    // auto-detect language from what they said
    var detected = KB.detectLang(text);
    if (detected !== lang && text.trim().length > 3) {
      lang = detected; pickVoice();
      syncLangButtons();
    }
    setState('thinking');
    setTimeout(function () { respond(text); }, 600);
  }

  function respond(text) {
    var tLow = text.toLowerCase();

    // Emergency first — always
    if (KB.isEmergency(text)) { say(t('emergency')); return; }

    // Appointment flow steps
    if (context.apptStep === 1) { // waiting for name
      context.name = text.trim().split(' ').slice(0, 2).join(' ');
      context.apptStep = 2;
      say(t('askMobile', { name: context.name })); return;
    }
    if (context.apptStep === 2) { // waiting for mobile
      var digits = text.replace(/\D/g, '');
      if (digits.length === 10 || (digits.length === 12 && digits.indexOf('91') === 0)) {
        context.mobile = digits.slice(-10);
        context.apptStep = 3;
        say(t('askDate')); return;
      }
      say(t('badMobile')); return;
    }
    if (context.apptStep === 3) { // waiting for date preference
      context.datePref = text.trim();
      context.apptStep = 0;
      var svcName = context.service ? context.service.title[lang] || context.service.title.en : t('askService');
      say(t('confirmAppt', { name: context.name, service: svcName, mobile: context.mobile, date: context.datePref }));
      setTimeout(function () {
        var url = CLINIC.bookingUrl + '?name=' + encodeURIComponent(context.name) +
          '&mobile=' + encodeURIComponent(context.mobile) +
          '&service=' + encodeURIComponent(svcName) +
          '&when=' + encodeURIComponent(context.datePref);
        window.open(url, '_blank');
      }, 2500);
      return;
    }

    // Intent matching
    if (/(appointment|book|అపాయింట్|బుక్|अपॉइंटमेंट|बुक)/.test(tLow)) {
      context.apptStep = 0; context.service = null;
      // if they mentioned a service, capture it
      var s0 = KB.findService(text);
      if (s0) context.service = s0;
      context.apptStep = 1;
      say(t('askName'));
      return;
    }
    if (/(whatsapp|వాట్సాప్)/.test(tLow)) {
      var msg = encodeURIComponent('Hello, I would like to enquire about a consultation at AR Plastic Surgery.');
      say(t('whatsappMsg'));
      setTimeout(function () {
        window.open('https://wa.me/' + CLINIC.phoneDigits + '?text=' + msg, '_blank');
      }, 1500);
      return;
    }
    if (/(cost|price|fee|ఖర్చు|ధర|कीमत|खर्च)/.test(tLow)) { say(t('costHonest') + ' ' + t('consultNote')); return; }
    if (/(scared|fear|afraid|worried|భయం|डर)/.test(tLow)) { say(t('scared')); return; }
    if (/(time|hour|open|timing|సమయం|వేళ|समय|खुल)/.test(tLow)) { say(t('hours')); return; }
    if (/(address|location|where|చిరునామ|ఎక్కడ|पता|कहां)/.test(tLow)) { say(t('location')); return; }
    if (/(doctor|ashok|డాక్టర్|అశోక్|डॉक्टर)/.test(tLow)) { say(t('doctor')); return; }
    if (/(review|rating|రేటింగ్|रेटिंग)/.test(tLow)) {
      say(lang === 'te' ? 'గూగుల్‌లో మాకు 4.9 స్టార్ రేటింగ్, 240కి పైగా సమీక్షలు ఉన్నాయి.' :
          lang === 'hi' ? 'Google पर हमारी 4.9 स्टार रेटिंग है, 240 से ज़्यादा समीक्षाएं।' :
          'We have a 4.9-star Google rating with over 240 patient reviews.');
      return;
    }
    var svc = KB.findService(text);
    if (svc) {
      context.service = svc;
      var ex = svc.explain[lang] || svc.explain.en;
      say(ex + ' ' + t('consultNote'));
      // follow-up chips
      setTimeout(function () {
        showChips([
          { label: lang === 'te' ? 'అపాయింట్‌మెంట్ బుక్ చేయండి' : lang === 'hi' ? 'अपॉइंटमेंट बुक करें' : 'Book appointment' },
          { label: lang === 'te' ? 'వాట్సాప్' : 'WhatsApp' }
        ], function (c) { handleUserText(c.label); });
      }, 500);
      return;
    }
    if (/(service|treatment|సేవ|चिकित्सा|सेवा)/.test(tLow)) {
      say(t('askService'));
      setTimeout(showServiceCards, 900);
      return;
    }
    if (/(thank|ధన్యవాద|धन्यवाद)/.test(tLow)) {
      say(lang === 'te' ? 'మీకు స్వాగతం! 😊' : lang === 'hi' ? 'आपका स्वागत है! 😊' : "You're welcome! 😊");
      return;
    }
    if (/(bye|టాటా|अलविदा)/.test(tLow)) { say(t('endSession')); return; }

    say(t('fallback'));
  }

  function say(text) {
    setState('speaking');
    addMsg(text, 'bot'); // addMsg triggers speak() which sets state
    defaultChips();
  }

  /* ---------- SPEECH RECOGNITION ---------- */
  function startListening() {
    var SR = window.SpeechRecognition || window.webkitSpeechRecognition;
    if (!SR) {
      addMsg(t('micDenied'), 'bot');
      return;
    }
    if (!wantListen) return;
    try {
      if (recog) { try { recog.abort(); } catch (e) {} }
      recog = new SR();
      recog.lang = lang === 'te' ? 'te-IN' : lang === 'hi' ? 'hi-IN' : 'en-IN';
      recog.continuous = true;
      recog.interimResults = false;
      recog.maxAlternatives = 1;
      var gotResult = false;
      recog.onresult = function (e) {
        gotResult = true;
        handleInterruption(); // stop our speech the moment they speak
        var txt = e.results[e.results.length - 1][0].transcript;
        if (txt && txt.trim()) handleUserText(txt.trim());
      };
      recog.onerror = function (e) {
        if (e.error === 'not-allowed' || e.error === 'service-not-allowed') {
          wantListen = false;
          addMsg(t('micDenied'), 'bot');
        }
      };
      recog.onend = function () {
        // auto-restart unless we got a result being processed
        if (wantListen && state !== 'thinking') setTimeout(startListening, 300);
        else if (wantListen) setTimeout(startListening, 2500);
      };
      recog.start();
      if (state === 'idle' || state === 'speaking') setState('listening');
    } catch (e) {
      if (wantListen) setTimeout(startListening, 2000);
    }
  }

  /* ---------- BUILD UI ---------- */
  function syncLangButtons() {
    document.querySelectorAll('#ar-ai-lang button').forEach(function (b) {
      b.classList.toggle('active', b.dataset.lang === lang);
    });
    var inp = document.getElementById('ar-ai-input');
    if (inp) inp.placeholder = lang === 'te' ? 'మీ సందేశం టైప్ చేయండి...' : lang === 'hi' ? 'अपना संदेश लिखें...' : 'Type your message...';
  }

  function build() {
    if (document.getElementById('ar-ai-panel')) return;
    var depth = (location.pathname.match(/\//g) || []).length - 1;
    var root = depth > 1 ? '../'.repeat(depth - 1) : '';

    var css = document.createElement('link');
    css.rel = 'stylesheet'; css.href = root + 'assets/ai-assistant.css';
    document.head.appendChild(css);
    var kb = document.createElement('script');
    kb.src = root + 'assets/ai-knowledge.js';
    document.head.appendChild(kb);

    var launcher = document.createElement('div');
    launcher.id = 'ar-ai-launcher';
    launcher.innerHTML = '💬<span class="ping"></span>';
    document.body.appendChild(launcher);

    var panel = document.createElement('div');
    panel.id = 'ar-ai-panel';
    panel.innerHTML =
      '<div id="ar-ai-header">' +
        '<div id="ar-ai-avatar">👩‍⚕️</div>' +
        '<div class="t"><b>' + 'AR Assistant' + '</b><div class="sub">Dr Ashok Reddy\'s Clinic</div><span id="ar-ai-state" class="ar-state" style="display:none"></span><div class="online">● Online</div></div>' +
        '<button id="ar-ai-mute" title="Mute">🔊</button>' +
        '<button id="ar-ai-end" title="End">📞</button>' +
        '<button id="ar-ai-close">×</button>' +
      '</div>' +
      '<div id="ar-ai-wave" class="ar-wave idle"><span></span><span></span><span></span><span></span><span></span><span></span><span></span></div>' +
      '<div id="ar-ai-lang">' +
        '<button data-lang="te" class="active">తెలుగు</button>' +
        '<button data-lang="hi">हिंदी</button>' +
        '<button data-lang="en">English</button>' +
      '</div>' +
      '<div id="ar-ai-messages"></div>' +
      '<div id="ar-ai-quick"></div>' +
      '<div id="ar-ai-privacy">🔒 Voice is processed in your browser. We don\'t record or store your conversations.</div>' +
      '<div id="ar-ai-input-row"><input id="ar-ai-input" placeholder="మీ సందేశం టైప్ చేయండి..."><button id="ar-ai-send">➤</button></div>';
    document.body.appendChild(panel);

    // wait for knowledge base if needed
    var bootTimer = setInterval(function () {
      if (window.AR_KB) { clearInterval(bootTimer); wireUp(); }
    }, 100);
    setTimeout(function () { clearInterval(bootTimer); if (!window.AR_KB) wireUp(); }, 3000);

    function wireUp() {
      if (window.AR_KB) { KB = window.AR_KB; CLINIC = KB.CLINIC; }
      launcher.onclick = function () {
        var p = document.getElementById('ar-ai-panel');
        var opening = !p.classList.contains('open');
        p.classList.toggle('open');
        var ping = launcher.querySelector('.ping');
        if (ping) ping.style.display = 'none';
        if (opening) {
          wantListen = true;
          if (!greeted) {
            greeted = true;
            setTimeout(function () {
              showWelcomeHero();
              say(t('greeting'));
              setTimeout(showServiceCards, 2500);
            }, 500);
          } else {
            startListening();
          }
        } else {
          wantListen = false;
          if ('speechSynthesis' in window) speechSynthesis.cancel();
          try { recog && recog.abort(); } catch (e) {}
          setState('idle');
        }
      };
      document.getElementById('ar-ai-close').onclick = function () {
        document.getElementById('ar-ai-panel').classList.remove('open');
        wantListen = false;
        if ('speechSynthesis' in window) speechSynthesis.cancel();
        try { recog && recog.abort(); } catch (e) {}
      };
      document.getElementById('ar-ai-end').onclick = function () {
        say(t('endSession'));
        setTimeout(function () {
          document.getElementById('ar-ai-panel').classList.remove('open');
          wantListen = false;
          if ('speechSynthesis' in window) speechSynthesis.cancel();
          try { recog && recog.abort(); } catch (e) {}
          setState('idle');
        }, 3000);
      };
      document.getElementById('ar-ai-mute').onclick = function () {
        voiceOn = !voiceOn;
        this.textContent = voiceOn ? '🔊' : '🔇';
        if (!voiceOn && 'speechSynthesis' in window) speechSynthesis.cancel();
      };
      document.querySelectorAll('#ar-ai-lang button').forEach(function (b) {
        b.onclick = function () {
          lang = b.dataset.lang; pickVoice(); syncLangButtons();
          try { recog && recog.abort(); } catch (e) {}
          if (wantListen) startListening();
        };
      });
      var input = document.getElementById('ar-ai-input');
      var send = function () {
        var v = input.value.trim();
        if (!v) return;
        input.value = '';
        handleUserText(v);
      };
      document.getElementById('ar-ai-send').onclick = send;
      input.onkeydown = function (e) { if (e.key === 'Enter') send(); };

      // Auto-launch after 3 seconds
      setTimeout(function () {
        if (!document.getElementById('ar-ai-panel').classList.contains('open')) {
          launcher.click();
        }
      }, 3000);
    }
  }

  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', build);
  } else { build(); }
})();
