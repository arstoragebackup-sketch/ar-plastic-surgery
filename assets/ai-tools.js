/* AR Plastic Surgery — AI Smart Tools
   1. Treatment Finder Quiz  2. Cost Estimator  3. Before/After Slider
*/
(function () {
  'use strict';

  /* ============ 1. TREATMENT FINDER ============ */
  var QUIZ = [
    { q: { en: 'What is your main concern?', te: 'మీ ప్రధాన సమస్య ఏమిటి?', hi: 'आपकी मुख्य चिंता क्या है?' },
      opts: [
        { t: { en: 'Hair loss / baldness', te: 'జుట్టు రాలడం', hi: 'बाल झड़ना' }, tag: 'hair' },
        { t: { en: 'Body shape / excess fat', te: 'శరీర ఆకారం / కొవ్వు', hi: 'शरीर का आकार / चर्बी' }, tag: 'body' },
        { t: { en: 'Face / nose / skin', te: 'ముఖం / ముక్కు / చర్మం', hi: 'चेहरा / नाक / त्वचा' }, tag: 'face' },
        { t: { en: 'Hand injury / problem', te: 'చేతి గాయం', hi: 'हाथ की चोट' }, tag: 'hand' },
        { t: { en: 'Lumps / scars / burns', te: 'గడ్డలు / మచ్చలు', hi: 'गांठ / निशान' }, tag: 'repair' }
      ] },
    { q: { en: 'How soon are you looking for treatment?', te: 'ఎప్పుడు చికిత్స కావాలి?', hi: 'इलाज कब चाहिए?' },
      opts: [
        { t: { en: 'As soon as possible', te: 'వీలైనంత త్వరగా', hi: 'जितनी जल्दी हो सके' }, tag: 'urgent' },
        { t: { en: 'Within a few months', te: 'కొన్ని నెలల్లో', hi: 'कुछ महीनों में' }, tag: 'soon' },
        { t: { en: 'Just exploring options', te: 'కేవలం తెలుసుకుంటున్నాను', hi: 'बस विकल्प देख रहा हूं' }, tag: 'explore' }
      ] },
    { q: { en: 'Surgery or non-surgical preference?', te: 'సర్జరీ లేదా శస్త్రచికిత్స లేని చికిత్స?', hi: 'सर्जरी या बिना सर्जरी?' },
      opts: [
        { t: { en: 'Open to surgery', te: 'సర్జరీకి సిద్ధం', hi: 'सर्जरी के लिए तैयार' }, tag: 'surgery' },
        { t: { en: 'Prefer non-surgical', te: 'శస్త్రచికిత్స లేనిది', hi: 'बिना सर्जरी' }, tag: 'nonsurgical' },
        { t: { en: 'Not sure — advise me', te: 'తెలియదు — సలహా ఇవ్వండి', hi: 'पता नहीं — सलाह दें' }, tag: 'any' }
      ] }
  ];

  var RESULTS = {
    hair: { surgery: ['hair-transplant', 'Hair Transplant', 'procedures/fue-hair-transplant.html'],
            nonsurgical: ['prp', 'PRP Therapy', 'procedures/prp-therapy.html'] },
    body: { surgery: ['liposuction', 'Liposuction', 'procedures/liposuction.html'],
            nonsurgical: ['liposuction', 'Liposuction', 'procedures/liposuction.html'] },
    face: { surgery: ['rhinoplasty', 'Rhinoplasty', 'procedures/rhinoplasty.html'],
            nonsurgical: ['botox-fillers', 'Botox & Fillers', 'procedures/botox-treatment.html'] },
    hand: { surgery: ['hand-surgery', 'Hand Surgery', 'procedures/hand-trauma-surgery.html'],
            nonsurgical: ['hand-surgery', 'Hand Surgery', 'procedures/hand-trauma-surgery.html'] },
    repair: { surgery: ['scar', 'Scar Treatment', 'procedures/scar-keloid-treatment.html'],
              nonsurgical: ['scar', 'Scar Treatment', 'procedures/scar-keloid-treatment.html'] }
  };

  function buildQuiz() {
    var el = document.getElementById('ar-quiz');
    if (!el) return;
    var lang = document.documentElement.lang === 'te' ? 'te' : 'en';
    var step = 0, answers = {};

    function render() {
      if (step >= QUIZ.length) { showResult(); return; }
      var q = QUIZ[step];
      var html = '<div class="ar-quiz-q">' + q.q[lang] + '</div><div class="ar-quiz-opts">';
      q.opts.forEach(function (o, i) {
        html += '<button class="ar-quiz-opt" data-i="' + i + '">' + o.t[lang] + '</button>';
      });
      html += '</div><div class="ar-quiz-progress">' + (step + 1) + ' / ' + QUIZ.length + '</div>';
      el.innerHTML = html;
      el.querySelectorAll('.ar-quiz-opt').forEach(function (b) {
        b.onclick = function () {
          answers[step] = q.opts[+b.dataset.i].tag;
          step++; render();
        };
      });
    }
    function showResult() {
      var concern = answers[0] || 'hair';
      var pref = answers[2] === 'nonsurgical' ? 'nonsurgical' : 'surgery';
      var r = RESULTS[concern][pref];
      var urgency = answers[1] === 'urgent'
        ? (lang === 'te' ? 'మీరు త్వరగా చికిత్స కోరుకుంటున్నారు — వెంటనే సంప్రదింపు బుక్ చేయండి.' : 'You want treatment soon — book a consultation right away.')
        : (lang === 'te' ? 'మీకు అనుకూలమైన సమయంలో సంప్రదింపు బుక్ చేయండి.' : 'Book a consultation at your convenience.');
      el.innerHTML = '<div class="ar-quiz-result"><div class="ar-quiz-label">' +
        (lang === 'te' ? '🤖 AI సిఫార్సు' : '🤖 AI Recommendation') + '</div>' +
        '<div class="ar-quiz-treatment">' + r[1] + '</div>' +
        '<p>' + urgency + '</p>' +
        '<div class="btn-row" style="justify-content:center">' +
        '<a class="btn btn-gold" href="' + r[2] + '">' + (lang === 'te' ? 'మరింత తెలుసుకోండి' : 'Learn More') + '</a>' +
        '<a class="btn btn-outline" href="https://arstoragebackup-sketch.github.io/Booking/" target="_blank">' +
        (lang === 'te' ? 'బుక్ చేయండి' : 'Book Now') + '</a></div>' +
        '<button class="ar-quiz-restart">' + (lang === 'te' ? '↻ మళ్లీ ప్రయత్నించండి' : '↻ Retake Quiz') + '</button></div>';
      el.querySelector('.ar-quiz-restart').onclick = function () { step = 0; answers = {}; render(); };
    }
    render();
  }

  /* ============ 2. COST ESTIMATOR ============ */
  var COSTS = [
    { id: 'hair', name: 'Hair Transplant (FUE)', range: '₹40,000 – ₹1,50,000+', note: 'Depends on grafts needed' },
    { id: 'gyn', name: 'Gynecomastia Surgery', range: '₹60,000 – ₹1,20,000', note: 'Keyhole procedure' },
    { id: 'lipo', name: 'Liposuction', range: '₹70,000 – ₹2,00,000', note: 'Depends on areas treated' },
    { id: 'rhino', name: 'Rhinoplasty', range: '₹80,000 – ₹1,80,000', note: 'Cosmetic / functional' },
    { id: 'tummy', name: 'Tummy Tuck', range: '₹1,00,000 – ₹2,50,000', note: 'Depends on extent' },
    { id: 'prp', name: 'PRP Therapy (per session)', range: '₹5,000 – ₹12,000', note: '3–4 sessions typical' },
    { id: 'botox', name: 'Botox (per area)', range: '₹8,000 – ₹20,000', note: 'Lasts 4–6 months' },
    { id: 'lipoma', name: 'Lipoma Removal', range: '₹15,000 – ₹40,000', note: 'Day procedure' }
  ];

  function buildEstimator() {
    var el = document.getElementById('ar-estimator');
    if (!el) return;
    var html = '<select id="ar-est-select" class="ar-est-select"><option value="">— Select a treatment —</option>';
    COSTS.forEach(function (c) { html += '<option value="' + c.id + '">' + c.name + '</option>'; });
    html += '</select><div id="ar-est-result" class="ar-est-result" style="display:none"></div>';
    el.innerHTML = html;
    document.getElementById('ar-est-select').onchange = function () {
      var c = COSTS.find(function (x) { return x.id === this.value; }, this);
      var r = document.getElementById('ar-est-result');
      if (!c) { r.style.display = 'none'; return; }
      r.style.display = 'block';
      r.innerHTML = '<div class="ar-est-range">' + c.range + '</div>' +
        '<div class="ar-est-note">' + c.note + '</div>' +
        '<div class="ar-est-disc">Indicative range only. Final cost depends on your individual assessment during consultation.</div>';
    };
  }

  /* ============ 3. BEFORE/AFTER SLIDER ============ */
  function buildSliders() {
    document.querySelectorAll('.ar-ba').forEach(function (el) {
      var before = el.dataset.before, after = el.dataset.after;
      if (!before || !after) return;
      el.innerHTML =
        '<div class="ar-ba-after"><img src="' + after + '" alt="After"></div>' +
        '<div class="ar-ba-before" style="width:50%"><img src="' + before + '" alt="Before"></div>' +
        '<div class="ar-ba-handle" style="left:50%"><div class="ar-ba-knob">⟨⟩</div></div>' +
        '<span class="ar-ba-tag tag-b">Before</span><span class="ar-ba-tag tag-a">After</span>';
      var handle = el.querySelector('.ar-ba-handle');
      var beforeDiv = el.querySelector('.ar-ba-before');
      var dragging = false;
      function move(x) {
        var rect = el.getBoundingClientRect();
        var pct = Math.max(2, Math.min(98, (x - rect.left) / rect.width * 100));
        beforeDiv.style.width = pct + '%';
        handle.style.left = pct + '%';
      }
      el.addEventListener('pointerdown', function (e) { dragging = true; move(e.clientX); });
      window.addEventListener('pointermove', function (e) { if (dragging) move(e.clientX); });
      window.addEventListener('pointerup', function () { dragging = false; });
    });
  }

  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', function () { buildQuiz(); buildEstimator(); buildSliders(); });
  } else { buildQuiz(); buildEstimator(); buildSliders(); }
})();
