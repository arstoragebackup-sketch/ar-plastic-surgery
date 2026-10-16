/* AR Plastic Surgery — Interactive Body Explorer + Recovery Timeline */
(function () {
  'use strict';

  var BODY_ZONES = [
    { id: 'hair', x: 50, y: 8, label: 'Hair', treatments: [
      { name: 'FUE Hair Transplant', link: 'procedures/fue-hair-transplant.html', desc: 'Permanent, natural hair restoration' },
      { name: 'PRP Therapy', link: 'procedures/prp-therapy.html', desc: 'Non-surgical hair regrowth support' } ] },
    { id: 'face', x: 50, y: 18, label: 'Face & Nose', treatments: [
      { name: 'Rhinoplasty', link: 'procedures/rhinoplasty.html', desc: 'Nose reshaping for form & function' },
      { name: 'Botox & Fillers', link: 'procedures/botox-treatment.html', desc: 'Wrinkle softening, volume restoration' },
      { name: 'Eyelid Surgery', link: 'procedures/eyelid-surgery-blepharoplasty.html', desc: 'Brighter, youthful eyes' } ] },
    { id: 'chest', x: 50, y: 32, label: 'Chest', treatments: [
      { name: 'Gynecomastia Surgery', link: 'procedures/gynecomastia-surgery.html', desc: 'Male chest contouring' },
      { name: 'Breast Augmentation', link: 'procedures/breast-augmentation.html', desc: 'Natural enhancement' },
      { name: 'Breast Reduction', link: 'procedures/breast-reduction.html', desc: 'Comfort & proportion' } ] },
    { id: 'abdomen', x: 50, y: 46, label: 'Abdomen', treatments: [
      { name: 'Liposuction', link: 'procedures/liposuction.html', desc: 'Stubborn fat removal & contouring' },
      { name: 'Tummy Tuck', link: 'procedures/tummy-tuck.html', desc: 'Excess skin removal, muscle tightening' } ] },
    { id: 'hand', x: 78, y: 42, label: 'Hand', treatments: [
      { name: 'Hand Trauma Surgery', link: 'procedures/hand-trauma-surgery.html', desc: 'Tendon, nerve & fracture repair' },
      { name: 'Carpal Tunnel Release', link: 'procedures/carpal-tunnel-release.html', desc: 'Numbness & pain relief' } ] },
    { id: 'skin', x: 22, y: 55, label: 'Skin', treatments: [
      { name: 'Scar Revision', link: 'procedures/scar-keloid-treatment.html', desc: 'Surgical & laser scar improvement' },
      { name: 'Lipoma Removal', link: 'procedures/lipoma-removal.html', desc: 'Quick lump removal' },
      { name: 'Burn Reconstruction', link: 'procedures/burn-reconstruction.html', desc: 'Function & appearance restoration' } ] }
  ];

  var RECOVERY = {
    'hair-transplant': [
      { w: 'Day 1–3', d: 'Mild redness & tiny scabs. Sleep with head elevated.' },
      { w: 'Week 1–2', d: 'Scabs fall off. Gentle hair wash as instructed.' },
      { w: 'Month 1–3', d: 'Transplanted hair sheds — this is normal.' },
      { w: 'Month 4–6', d: 'New hair starts growing visibly.' },
      { w: 'Month 9–12', d: 'Full, natural result. Final density achieved.' } ],
    'rhinoplasty': [
      { w: 'Day 1–7', d: 'Splint on nose. Swelling & bruising peak then fade.' },
      { w: 'Week 2', d: 'Splint removed. Return to desk work.' },
      { w: 'Month 1–3', d: 'Swelling reduces significantly.' },
      { w: 'Month 6–12', d: 'Final refined shape emerges.' } ],
    'liposuction': [
      { w: 'Day 1–3', d: 'Soreness like intense workout. Compression garment on.' },
      { w: 'Week 1–2', d: 'Light activity. Bruising fades.' },
      { w: 'Week 4–6', d: 'Back to full routine. Shape improving.' },
      { w: 'Month 3', d: 'Final contour visible.' } ],
    'default': [
      { w: 'Day 1–3', d: 'Rest & follow post-op instructions carefully.' },
      { w: 'Week 1–2', d: 'First follow-up. Gradual return to light activity.' },
      { w: 'Month 1–3', d: 'Continued healing. Attend all follow-ups.' },
      { w: 'Month 6+', d: 'Final results. Maintain with healthy habits.' } ]
  };

  function buildExplorer() {
    var el = document.getElementById('ar-body-explorer');
    if (!el) return;
    var svg = '<svg viewBox="0 0 100 100" class="ar-body-svg">' +
      '<ellipse cx="50" cy="12" rx="11" ry="13" class="ar-body-part" data-zone="hair"/>' +
      '<ellipse cx="50" cy="14" rx="8" ry="9" class="ar-body-part" data-zone="face"/>' +
      '<rect x="38" y="26" width="24" height="22" rx="8" class="ar-body-part" data-zone="chest"/>' +
      '<rect x="40" y="48" width="20" height="18" rx="6" class="ar-body-part" data-zone="abdomen"/>' +
      '<rect x="28" y="28" width="7" height="28" rx="3.5" class="ar-body-part" data-zone="skin"/>' +
      '<rect x="65" y="28" width="7" height="28" rx="3.5" class="ar-body-part" data-zone="hand"/>' +
      '<rect x="42" y="66" width="7" height="28" rx="3.5" class="ar-body-part" data-zone="skin"/>' +
      '<rect x="51" y="66" width="7" height="28" rx="3.5" class="ar-body-part" data-zone="skin"/>';
    BODY_ZONES.forEach(function (z) {
      svg += '<g class="ar-zone-dot" data-zone="' + z.id + '" style="cursor:pointer">' +
        '<circle cx="' + z.x + '" cy="' + z.y + '" r="4" class="ar-dot"/>' +
        '<circle cx="' + z.x + '" cy="' + z.y + '" r="7" class="ar-dot-ring"/>' +
        '<text x="' + (z.x + 9) + '" y="' + (z.y + 2) + '" class="ar-zone-label">' + z.label + '</text></g>';
    });
    svg += '</svg>';
    el.innerHTML = '<div class="ar-explorer-wrap"><div class="ar-explorer-svg">' + svg + '</div>' +
      '<div class="ar-explorer-info" id="ar-explorer-info">' +
      '<div class="ar-explorer-hint">👆 Tap a glowing point on the body to explore treatments for that area</div></div></div>';

    el.querySelectorAll('[data-zone]').forEach(function (node) {
      node.addEventListener('click', function () {
        var zone = BODY_ZONES.find(function (z) { return z.id === node.dataset.zone; });
        if (!zone) return;
        var info = document.getElementById('ar-explorer-info');
        var html = '<div class="ar-zone-title">' + zone.label + '</div>';
        zone.treatments.forEach(function (t) {
          html += '<a class="ar-treatment-link" href="' + t.link + '">' +
            '<span class="ar-t-name">' + t.name + ' →</span>' +
            '<span class="ar-t-desc">' + t.desc + '</span></a>';
        });
        info.innerHTML = html;
        // highlight
        el.querySelectorAll('.ar-dot').forEach(function (d) { d.classList.remove('active'); });
        el.querySelectorAll('.ar-zone-dot[data-zone="' + zone.id + '"] .ar-dot').forEach(function (d) {
          d.classList.add('active');
        });
      });
    });
  }

  function buildRecovery() {
    var el = document.getElementById('ar-recovery');
    if (!el) return;
    var proc = el.dataset.procedure || 'default';
    var steps = RECOVERY[proc] || RECOVERY['default'];
    var html = '<div class="ar-timeline">';
    steps.forEach(function (s, i) {
      html += '<div class="ar-tl-step">' +
        '<div class="ar-tl-dot">' + (i + 1) + '</div>' +
        '<div class="ar-tl-body"><div class="ar-tl-when">' + s.w + '</div><div class="ar-tl-what">' + s.d + '</div></div>' +
        '</div>';
    });
    html += '</div><div class="ar-tl-note">Every patient heals differently. Your surgeon will give you personalised guidance at each follow-up.</div>';
    el.innerHTML = html;
  }

  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', function () { buildExplorer(); buildRecovery(); });
  } else { buildExplorer(); buildRecovery(); }
})();
