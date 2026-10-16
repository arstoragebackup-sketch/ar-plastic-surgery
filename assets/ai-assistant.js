/* AR Plastic Surgery — Telugu Voice AI Assistant
   Auto-launches on page load, speaks politely in Telugu,
   answers about services, guides booking: mobile number -> select service -> booking site.
*/
(function () {
  'use strict';

  var BOOKING_URL = 'https://arstoragebackup-sketch.github.io/Booking/';
  var CLINIC_PHONE = '+91 91826 56866';
  var lang = 'te'; // default Telugu
  var voiceOn = true;
  var booking = { step: 0, mobile: '', service: '' };

  var SERVICES_TE = [
    'హెయిర్ ట్రాన్స్‌ప్లాంట్', 'గైనకోమాస్టియా', 'లైపోసక్షన్',
    'రైనోప్లాస్టీ', 'బ్రెస్ట్ సర్జరీ', 'టమ్మీ టక్',
    'బోటాక్స్ & ఫిల్లర్లు', 'స్కార్ ట్రీట్‌మెంట్', 'బర్న్ పునర్నిర్మాణం',
    'హ్యాండ్ సర్జరీ', 'చీలిన పెదవి', 'పీఆర్పీ చికిత్స'
  ];
  var SERVICES_EN = [
    'Hair Transplant', 'Gynecomastia', 'Liposuction',
    'Rhinoplasty', 'Breast Surgery', 'Tummy Tuck',
    'Botox & Fillers', 'Scar Treatment', 'Burn Reconstruction',
    'Hand Surgery', 'Cleft Lip & Palate', 'PRP Therapy'
  ];

  var STR = {
    te: {
      greeting: 'నమస్కారం! 🙏 AR ప్లాస్టిక్ సర్జరీకి స్వాగతం. నేను మీ సహాయకుడిని — నేను వింటున్నాను, మీరు మాట్లాడవచ్చు! డా. అశోక్ రెడ్డి గారి క్లినిక్ గురించి, మా సేవల గురించి అడగండి, లేదా అపాయింట్‌మెంట్ బుక్ చేసుకోండి.',
      about: 'AR ప్లాస్టిక్ సర్జరీ కరీంనగర్‌లోని ప్రముఖ క్లినిక్. డా. అశోక్ రెడ్డి గారు — MBBS, DNB (ముంబై), M.Ch (ఢిల్లీ), గోల్డ్ మెడలిస్ట్. ప్లాస్టిక్, కాస్మెటిక్, హెయిర్ ట్రాన్స్‌ప్లాంట్ మరియు హ్యాండ్ సర్జరీలో నిపుణులు. మా సమయం: ప్రతిరోజూ ఉదయం 10 నుండి రాత్రి 8 వరకు.',
      servicesIntro: 'మా ప్రధాన సేవలు ఇవి. దేని గురించి తెలుసుకోవాలనుకుంటున్నారు?',
      hours: 'మేము ప్రతిరోజూ ఉదయం 10:00 నుండి రాత్రి 8:00 వరకు తెరిచి ఉంటాము. ఆదివారం కూడా!',
      location: 'మా చిరునామా: రెడ్డి గారి వంటిల్లు ఎదురుగా, కోర్ట్ చౌరస్తా, కరీంనగర్, తెలంగాణ — 505001.',
      doctor: 'డా. అశోక్ రెడ్డి గారు గోల్డ్ మెడలిస్ట్ ప్లాస్టిక్ సర్జన్. MBBS, DNB (ముంబై), M.Ch (ఢిల్లీ) చేశారు. 4.9 స్టార్ గూగుల్ రేటింగ్‌తో వందలాది మంది రోగుల నమ్మకాన్ని పొందారు.',
      askMobile: 'అపాయింట్‌మెంట్ బుక్ చేయడానికి, దయచేసి మీ మొబైల్ నంబర్ ఇవ్వండి (10 అంకెలు).',
      badMobile: 'క్షమించండి, అది సరైన మొబైల్ నంబర్‌లా లేదు. దయచేసి 10 అంకెల నంబర్ ఇవ్వండి.',
      askService: 'ధన్యవాదాలు! ఇప్పుడు మీకు కావలసిన సేవను ఎంచుకోండి:',
      confirm: 'మీ వివరాలు నమోదయ్యాయి! బుకింగ్ పేజీకి తీసుకెళ్తున్నాను...',
      fallback: 'క్షమించండి, నాకు అర్థం కాలేదు. సేవలు, డాక్టర్, సమయం, చిరునామా గురించి అడగండి — లేదా "బుక్" అని టైప్ చేసి అపాయింట్‌మెంట్ బుక్ చేసుకోండి.',
      chips: ['సేవలు', 'డాక్టర్ గురించి', 'సమయం', 'చిరునామా', 'బుక్ చేయండి'],
      placeholder: 'మీ సందేశం టైప్ చేయండి...',
      voiceOn: 'వాయిస్ ఆన్', voiceOff: 'వాయిస్ ఆఫ్',
      cost: 'చికిత్స ఖర్చు మీ కేసును బట్టి ఉంటుంది. ఖచ్చితమైన అంచనా కోసం దయచేసి అపాయింట్‌మెంట్ బుక్ చేయండి — డా. అశోక్ రెడ్డి గారు పరిశీలించి అన్నీ స్పష్టంగా వివరిస్తారు. కాల్ చేయండి: ' + CLINIC_PHONE,
      reviews: 'గూగుల్‌లో మాకు 4.9 స్టార్ రేటింగ్ ఉంది — తెలంగాణ నలుమూలల నుండి 240కి పైగా సంతోషకరమైన రోగుల సమీక్షలు.',
      emergency: 'చేతి గాయాలు లేదా అత్యవసర పరిస్థితుల్లో వెంటనే కాల్ చేయండి: ' + CLINIC_PHONE + ' — లేదా నేరుగా క్లినిక్‌కు రండి. ప్రతిరోజూ ఉదయం 10 నుండి రాత్రి 8 వరకు తెరిచి ఉంటాము.'
    },
    en: {
      greeting: 'Hello! 🙏 Welcome to AR Plastic Surgery. I am your assistant — I\'m listening, just speak! Ask me about Dr Ashok Reddy\'s clinic, our services, or book an appointment.',
      about: 'AR Plastic Surgery is Karimnagar\'s leading clinic. Dr Ashok Reddy — MBBS, DNB (Mumbai), M.Ch (Delhi), Gold Medalist — specialises in plastic, cosmetic, hair transplant and hand surgery. Open daily 10 AM to 8 PM.',
      servicesIntro: 'Here are our main services. Which would you like to know about?',
      hours: 'We are open every day from 10:00 AM to 8:00 PM, including Sundays!',
      location: 'Our address: Opp. Reddy Gari Vantillu, Court Chowrasta, Karimnagar, Telangana — 505001.',
      doctor: 'Dr Ashok Reddy is a Gold Medalist plastic surgeon — MBBS, DNB (Mumbai), M.Ch (Delhi). Trusted by hundreds of patients with a 4.9-star Google rating.',
      askMobile: 'To book an appointment, please share your 10-digit mobile number.',
      badMobile: 'Sorry, that doesn\'t look like a valid mobile number. Please share a 10-digit number.',
      askService: 'Thank you! Now please choose the service you need:',
      confirm: 'Details recorded! Taking you to the booking page...',
      fallback: 'Sorry, I didn\'t understand. Ask about services, the doctor, timings, or address — or type "book" to make an appointment.',
      chips: ['Services', 'About Doctor', 'Timings', 'Address', 'Book Now'],
      placeholder: 'Type your message...',
      voiceOn: 'Voice on', voiceOff: 'Voice off',
      cost: 'Treatment costs depend on your specific case. For an accurate estimate, please book a consultation — Dr Ashok Reddy will assess and explain everything clearly. Call ' + CLINIC_PHONE + '.',
      reviews: 'We have a 4.9-star rating on Google with over 240 reviews from happy patients across Telangana.',
      emergency: 'For hand injuries or emergencies, please call us immediately at ' + CLINIC_PHONE + ' or visit the clinic directly. We are open daily 10 AM to 8 PM.'
    }
  };

  var SERVICE_INFO_TE = {
    'హెయిర్ ట్రాన్స్‌ప్లాంట్': 'FUE హెయిర్ ట్రాన్స్‌ప్లాంట్‌లో మేము నిపుణులం. మీ స్వంత జుట్టును తీసి అవసరమైన చోట నాటుతాము. సహజమైన ఫలితాలు, శాశ్వత పరిష్కారం.',
    'గైనకోమాస్టియా': 'పురుషుల ఛాతీ సమస్యకు కీహోల్ సర్జరీ. చిన్న గాటు, త్వరగా కోలుకోవడం.',
    'లైపోసక్షన్': 'శరీరంలోని అదనపు కొవ్వును తొలగించే ప్రక్రియ. సురక్షితమైన, ఆధునిక పద్ధతులు.',
    'రైనోప్లాస్టీ': 'ముక్కు ఆకారాన్ని సరిచేసే సర్జరీ. రూపం మరియు శ్వాస రెండింటికీ.',
    'పీఆర్పీ చికిత్స': 'మీ స్వంత రక్తం నుండి ప్లేట్‌లెట్లను తీసి జుట్టు పెరుగుదలకు ఉపయోగిస్తాము. శస్త్రచికిత్స లేని చికిత్స.'
  };

  function speak(text) {
    if (!voiceOn || !('speechSynthesis' in window)) return;
    try {
      speechSynthesis.cancel();
      var u = new SpeechSynthesisUtterance(text.replace(/[🙏•]/g, ''));
      u.lang = lang === 'te' ? 'te-IN' : 'en-IN';
      u.rate = 0.95;
      speechSynthesis.speak(u);
    } catch (e) {}
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

  function typing(on) {
    var box = document.getElementById('ar-ai-messages');
    var t = document.getElementById('ar-typing');
    if (on && !t) {
      t = document.createElement('div');
      t.className = 'ar-msg bot'; t.id = 'ar-typing';
      t.innerHTML = '<span class="typing"><span></span><span></span><span></span></span>';
      box.appendChild(t); box.scrollTop = box.scrollHeight;
    } else if (!on && t) { t.remove(); }
  }

  function showChips() {
    var row = document.getElementById('ar-ai-quick');
    row.innerHTML = '';
    STR[lang].chips.forEach(function (c) {
      var b = document.createElement('button');
      b.className = 'ar-chip'; b.textContent = c;
      b.onclick = function () { sendUser(c); };
      row.appendChild(b);
    });
  }

  function showServiceChips() {
    var row = document.getElementById('ar-ai-quick');
    row.innerHTML = '';
    var list = lang === 'te' ? SERVICES_TE : SERVICES_EN;
    list.forEach(function (s) {
      var b = document.createElement('button');
      b.className = 'ar-chip'; b.textContent = s;
      b.onclick = function () { chooseService(s); };
      row.appendChild(b);
    });
  }

  function matchIntent(text) {
    var t = text.toLowerCase();
    if (booking.step === 1) {
      var digits = t.replace(/\D/g, '');
      if (digits.length === 10 || (digits.length === 12 && digits.indexOf('91') === 0)) {
        booking.mobile = digits.slice(-10);
        booking.step = 2;
        return 'askService';
      }
      return 'badMobile';
    }
    if (/(cost|price|fee|ఖర్చు|ధర|ఫీజు)/.test(t)) return 'cost';
    if (/(review|rating|రేటింగ్|సమీక్ష)/.test(t)) return 'reviews';
    if (/(emergency|urgent|injury|అత్యవసర|గాయం)/.test(t)) return 'emergency';
    if (/(book|appointment|అపాయింట్|బుక్)/.test(t)) return 'book';
    if (/(service|సేవ)/.test(t)) return 'services';
    if (/(doctor|ashok|డాక్టర్|అశోక్)/.test(t)) return 'doctor';
    if (/(time|hour|open|timing|సమయ|వేళ)/.test(t)) return 'hours';
    if (/(address|location|where|చిరునామ|ఎక్కడ)/.test(t)) return 'location';
    if (/(about|clinic|hospital|గురించి)/.test(t)) return 'about';
    if (/(hai|hello|hi\b|నమస్కారం|హలో)/.test(t)) return 'greeting';
    // service-specific
    var list = lang === 'te' ? SERVICES_TE : SERVICES_EN;
    for (var i = 0; i < list.length; i++) {
      if (t.indexOf(list[i].toLowerCase().slice(0, 4)) !== -1 && list[i].length > 4) return 'serviceInfo:' + list[i];
    }
    if (/(hair|జుట్టు)/.test(t)) return 'serviceInfo:' + list[0];
    return 'fallback';
  }

  function respond(intent) {
    typing(true);
    setTimeout(function () {
      typing(false);
      var S = STR[lang];
      if (intent === 'book' || intent === 'askMobile') {
        booking.step = 1; addMsg(S.askMobile, 'bot');
      } else if (intent === 'badMobile') {
        addMsg(S.badMobile, 'bot');
      } else if (intent === 'askService') {
        addMsg(S.askService, 'bot'); showServiceChips(); return;
      } else if (intent === 'services') {
        addMsg(S.servicesIntro, 'bot'); showServiceChips(); return;
      } else if (intent === 'doctor') { addMsg(S.doctor, 'bot'); }
      else if (intent === 'hours') { addMsg(S.hours, 'bot'); }
      else if (intent === 'location') { addMsg(S.location, 'bot'); }
      else if (intent === 'about') { addMsg(S.about, 'bot'); }
      else if (intent === 'cost') { addMsg(S.cost, 'bot'); }
      else if (intent === 'reviews') { addMsg(S.reviews, 'bot'); }
      else if (intent === 'emergency') { addMsg(S.emergency, 'bot'); }
      else if (intent === 'greeting') { addMsg(S.greeting, 'bot'); }
      else if (intent.indexOf('serviceInfo:') === 0) {
        var svc = intent.split(':')[1];
        var info = (lang === 'te' ? SERVICE_INFO_TE[svc] : null) ||
          (lang === 'te' ? svc + ' గురించి మరింత తెలుసుకోవడానికి క్లినిక్‌కు రండి లేదా కాల్ చేయండి: ' + CLINIC_PHONE :
           'Visit the clinic or call ' + CLINIC_PHONE + ' to learn more about ' + svc + '.');
        addMsg(info, 'bot');
      }
      else { addMsg(S.fallback, 'bot'); }
      showChips();
    }, 700);
  }

  function chooseService(svc) {
    addMsg(svc, 'user');
    booking.service = svc;
    booking.step = 0;
    var S = STR[lang];
    typing(true);
    setTimeout(function () {
      typing(false);
      addMsg(S.confirm, 'bot');
      setTimeout(function () {
        var url = BOOKING_URL + '?mobile=' + encodeURIComponent(booking.mobile) +
          '&service=' + encodeURIComponent(svc);
        window.open(url, '_blank');
      }, 1200);
      showChips();
    }, 700);
  }

  function sendUser(text) {
    addMsg(text, 'user');
    respond(matchIntent(text));
  }

  function setLang(l) {
    lang = l;
    document.querySelectorAll('#ar-ai-lang button').forEach(function (b) {
      b.classList.toggle('active', b.dataset.lang === l);
    });
    document.getElementById('ar-ai-input').placeholder = STR[l].placeholder;
    showChips();
  }

  function build() {
    if (document.getElementById('ar-ai-panel')) return;
    var css = document.createElement('link');
    css.rel = 'stylesheet'; css.href = 'assets/ai-assistant.css';
    // fix path for nested pages
    var depth = (location.pathname.match(/\//g) || []).length - 1;
    if (depth > 1) css.href = '../'.repeat(depth - 1) + 'assets/ai-assistant.css';
    document.head.appendChild(css);

    var launcher = document.createElement('div');
    launcher.id = 'ar-ai-launcher';
    launcher.innerHTML = '💬<span class="ping"></span>';
    launcher.title = 'Chat with us';
    document.body.appendChild(launcher);

    var panel = document.createElement('div');
    panel.id = 'ar-ai-panel';
    panel.innerHTML =
      '<div id="ar-ai-header">' +
        '<img src="' + (depth > 1 ? '../'.repeat(depth - 1) : '') + 'assets/logo.png" alt="AR">' +
        '<div class="t"><b>AR సహాయకుడు</b><span>AI Assistant</span><div class="online">● Online</div></div>' +
        '<button id="ar-ai-voice-toggle" title="Toggle voice">🔊</button>' +
        '<button id="ar-ai-close">×</button>' +
      '</div>' +
      '<div id="ar-ai-lang"><button data-lang="te" class="active">తెలుగు</button><button data-lang="en">English</button></div>' +
      '<div id="ar-ai-messages"></div>' +
      '<div id="ar-ai-quick"></div>' +
      '<div id="ar-ai-input-row"><input id="ar-ai-input" placeholder="మీ సందేశం టైప్ చేయండి..."><button id="ar-ai-send">➤</button></div>';
    document.body.appendChild(panel);

    launcher.onclick = function () {
      var p = document.getElementById('ar-ai-panel');
      var opening = !p.classList.contains('open');
      p.classList.toggle('open');
      launcher.querySelector('.ping').style.display = 'none';
      if (opening && !document.getElementById('ar-ai-messages').children.length) {
        setTimeout(function () { addMsg(STR[lang].greeting, 'bot'); showChips(); }, 400);
      }
    };
    document.getElementById('ar-ai-close').onclick = function () {
      document.getElementById('ar-ai-panel').classList.remove('open');
    };
    document.getElementById('ar-ai-voice-toggle').onclick = function () {
      voiceOn = !voiceOn;
      this.textContent = voiceOn ? '🔊' : '🔇';
      this.classList.toggle('off', !voiceOn);
      if (!voiceOn && 'speechSynthesis' in window) speechSynthesis.cancel();
    };
    document.querySelectorAll('#ar-ai-lang button').forEach(function (b) {
      b.onclick = function () { setLang(b.dataset.lang); };
    });
    var input = document.getElementById('ar-ai-input');
    var send = function () {
      var v = input.value.trim();
      if (!v) return;
      input.value = '';
      sendUser(v);
    };
    document.getElementById('ar-ai-send').onclick = send;
    input.onkeydown = function (e) { if (e.key === 'Enter') send(); };

    // Always-on voice listening — starts automatically, no button needed
    var SR = window.SpeechRecognition || window.webkitSpeechRecognition;
    var recog = null, wantListen = true, heardOnce = false;
    function startListen() {
      if (!SR || !wantListen) return;
      try {
        if (recog) { try { recog.stop(); } catch (e) {} }
        recog = new SR();
        recog.lang = lang === 'te' ? 'te-IN' : 'en-IN';
        recog.continuous = true;
        recog.interimResults = false;
        recog.maxAlternatives = 1;
        recog.onresult = function (e) {
          var txt = e.results[e.results.length - 1][0].transcript;
          if (txt && txt.trim()) {
            heardOnce = true;
            sendUser(txt.trim());
          }
        };
        recog.onerror = function (e) {
          // permission denied — stop trying silently after first failure
          if (e.error === 'not-allowed' || e.error === 'service-not-allowed') wantListen = false;
        };
        recog.onend = function () {
          // auto-restart so listening never stops
          if (wantListen) setTimeout(startListen, 400);
        };
        recog.start();
      } catch (e) {
        if (wantListen) setTimeout(startListen, 2000);
      }
    }
    // begin listening when panel first opens
    var _origLauncher = launcher.onclick;
    launcher.onclick = function () {
      _origLauncher();
      if (document.getElementById('ar-ai-panel').classList.contains('open')) {
        wantListen = true;
        startListen();
      }
    };
    // keep language in sync if user switches mid-session
    var _origSetLang = setLang;
    setLang = function (l) {
      _origSetLang(l);
      if (recog) { try { recog.stop(); } catch (e) {} }
    };

    // Auto-launch after 3 seconds on first visit
    setTimeout(function () {
      if (!document.getElementById('ar-ai-panel').classList.contains('open')) {
        launcher.click();
      }
    }, 3000);
  }

  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', build);
  } else { build(); }
})();
