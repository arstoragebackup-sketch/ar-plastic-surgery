# Daily district article engine for the AR Plastic Surgery website.
# Generates one substantive, unique article per day: (district x procedure).
# Each article combines in-depth procedure education with district-specific
# travel/planning guidance so no two articles are thin duplicates.

DISTRICTS = [
    # (slug, name, distance_km_from_karimnagar, local_note)
    ("karimnagar", "Karimnagar", 0, "home to AR Plastic Surgery itself — no travel needed"),
    ("jagtial", "Jagtial", 45, "a straightforward drive down NH63"),
    ("peddapalli", "Peddapalli", 35, "under an hour by road from the clinic"),
    ("sircilla", "Rajanna Sircilla", 40, "well connected by road via Vemulawada route"),
    ("siddipet", "Siddipet", 75, "about ninety minutes via the Karimnagar–Siddipet road"),
    ("warangal", "Warangal", 65, "an easy trip on NH563 via Hanamkonda"),
    ("hanamkonda", "Hanamkonda", 60, "the twin city of Warangal, under ninety minutes away"),
    ("nizamabad", "Nizamabad", 115, "around two hours on NH44 and connecting roads"),
    ("mancherial", "Mancherial", 70, "a direct run south on NH63"),
    ("nirmal", "Nirmal", 110, "about two hours via NH44"),
    ("adilabad", "Adilabad", 140, "roughly two and a half hours on NH44"),
    ("asifabad", "Komaram Bheem Asifabad", 160, "a half-day trip, worth planning an early start"),
    ("khammam", "Khammam", 180, "around three hours — many patients combine consultation with a day trip"),
    ("kothagudem", "Bhadradri Kothagudem", 210, "a longer journey, so plan an unhurried day"),
    ("nalgonda", "Nalgonda", 170, "about three hours via Hyderabad highway connections"),
    ("suryapet", "Suryapet", 150, "roughly two and a half hours on NH65 connectors"),
    ("yadadri", "Yadadri Bhuvanagiri", 130, "a comfortable drive of just over two hours"),
    ("jangaon", "Jangaon", 90, "under two hours via NH163"),
    ("mahabubabad", "Mahabubabad", 120, "about two hours on the Warangal route"),
    ("mulugu", "Mulugu", 100, "under two hours through scenic agency roads"),
    ("bhupalpally", "Jayashankar Bhupalpally", 85, "under two hours via Parkal"),
    ("kamareddy", "Kamareddy", 95, "about two hours on NH44"),
    ("medak", "Medak", 130, "roughly two and a half hours via Siddipet"),
    ("sangareddy", "Sangareddy", 160, "under three hours via the Hyderabad highway"),
    ("hyderabad", "Hyderabad", 165, "about three hours — many Hyderabad patients prefer Karimnagar's personal care"),
    ("medchal", "Medchal-Malkajgiri", 155, "under three hours on the Outer Ring Road connectors"),
    ("rangareddy", "Rangareddy", 170, "about three hours from most parts of the district"),
    ("vikarabad", "Vikarabad", 190, "a three-hour journey best started early"),
    ("mahabubnagar", "Mahabubnagar", 200, "over three hours — plan a full day"),
    ("narayanpet", "Narayanpet", 220, "a long but doable day trip"),
    ("gadwal", "Jogulamba Gadwal", 230, "the farthest major town — consider an overnight stay"),
    ("nagarkurnool", "Nagarkurnool", 210, "about three and a half hours"),
    ("wanaparthy", "Wanaparthy", 195, "around three hours via NH44"),
]

ARTICLE_PROCEDURES = {
    "hair-transplant": {
        "name": "Hair Transplant",
        "sections": [
            ("Is a Hair Transplant Right for You?",
             ["Not every kind of hair loss suits a transplant. The procedure moves your own permanent hair from the donor zone, usually the back of the scalp, to thinning areas — so you need a stable pattern of loss and a healthy donor supply. Diffuse thinning without a clear pattern, or very early aggressive shedding, may mean waiting or trying medical management first.",
              "Age matters too. Operating on a very young patient whose final pattern is unknown can produce a result that looks odd a decade later as native hair keeps receding around the transplanted grafts. A careful surgeon maps your likely future loss and plans conservatively, sometimes advising you to stabilise with medication before any surgery."]),
            ("How the FUE Procedure Works",
             ["FUE, or follicular unit extraction, harvests individual grafts one by one, leaving tiny dot scars rather than a linear strip scar. Each graft contains one to four hairs and is placed at natural angles so the hairline looks like hair, not like a transplant. The number of grafts depends on your degree of loss and your goals — density is always a trade-off with donor conservation.",
              "The day itself is long but comfortable: local anaesthesia, no overnight stay, and most people return to desk work within a few days. Transplanted hairs shed in the first month — this is normal — and begin regrowing from the third or fourth month, with the full picture visible around a year."]),
            ("What Determines a Natural Result",
             ["Three things separate a natural transplant from an obvious one: hairline design that suits your age and face, graft placement at correct angles and directions, and honest density planning that does not exhaust your donor area in one sitting. A surgeon who plans for your sixties, not just your thirties, is thinking correctly.",
              "Beware of anyone who quotes graft numbers without examining your donor area, or who promises a celebrity hairline regardless of your pattern. The consultation should include donor measurement, a discussion of what density is realistic, and a clear statement of what the procedure cannot do."]),
            ("Recovery and Aftercare",
             ["The first two weeks need gentle handling: no scratching, no harsh washing, sleeping slightly elevated. Mild swelling and scabbing are expected and settle quickly. Your clinic should give written aftercare instructions and remain reachable — the quality of follow-up says a lot about the quality of the practice.",
              "Long-term, transplanted hair behaves like the donor hair it came from and typically keeps growing permanently, but native hair around it may continue thinning. Many patients use maintenance medication to protect the rest. This should be discussed openly at consultation, not discovered later."]),
        ],
        "faqs": [
            ("How much does a hair transplant cost?",
             "Cost depends on the number of grafts and the complexity of your case, which is why honest clinics quote only after examining you. Be cautious of flat per-graft rates advertised without assessment — the cheapest quote often cuts corners on planning, graft handling, or surgeon involvement."),
            ("Will the transplanted hair fall out again?",
             "The transplanted hairs shed once after surgery and then regrow from the third or fourth month. Because they come from the permanent donor zone, they typically keep growing long-term, though surrounding native hair may still thin and need maintenance."),
            ("Can I get it done in one sitting?",
             "Most cases are completed in a single session of several hours, but extensive loss may need a second sitting months later. A surgeon who preserves donor hair for the future is protecting you, not upselling you."),
        ],
        "related": ["gynecomastia-surgery", "liposuction", "prp-therapy"],
    },
    "gynecomastia": {
        "name": "Gynecomastia Surgery",
        "sections": [
            ("Understanding Male Chest Enlargement",
             ["Gynecomastia is the enlargement of male breast tissue, and it is far more common than most men realise — studies suggest it affects a large share of men at some point. It can come from hormonal shifts during puberty, certain medications, or underlying conditions, and it often persists long after the cause has passed.",
              "The distress it causes is real and under-discussed: avoiding swimming, layered clothing in summer, poor posture to hide the chest. None of this is vanity — it is about feeling normal in your own body. The first step is an honest evaluation to confirm the tissue is glandular rather than simple fat, because the two need different treatment."]),
            ("How the Surgery Works",
             ["True gynecomastia usually needs gland excision, often combined with liposuction to contour the surrounding chest. The incisions are small and placed at the edge of the areola where scars fade well. In straightforward cases the whole procedure takes one to two hours under anaesthesia, and most patients go home the same day.",
              "The goal is a flat, masculine chest contour — not an over-scooped look. A surgeon experienced in this procedure knows how much tissue to leave for a natural transition, because removing everything can look as unnatural as leaving too much."]),
            ("Recovery: What to Expect",
             ["A compression garment is worn for several weeks to help the skin settle smoothly onto the new contour. Most men return to desk work within a week and to the gym within a month, with the final shape emerging over two to three months as swelling resolves.",
              "Scars at the areola edge typically fade to faint lines. The key aftercare rules are simple: wear the garment as advised, avoid chest strain early on, and attend follow-ups so any fluid collection or asymmetry is caught early."]),
            ("Choosing the Right Surgeon",
             ["Ask how many gynecomastia cases the surgeon performs and to see genuine results. The consultation should include a physical examination distinguishing gland from fat, a clear operative plan, and an honest discussion of risks such as contour irregularity or the need for revision.",
              "Be wary of anyone who promises a shirtless-beach-body outcome without examining you, or who quotes a price before assessment. This is a contouring operation where judgement matters more than speed."]),
        ],
        "faqs": [
            ("Will exercise alone fix gynecomastia?",
             "Exercise builds the muscle underneath but cannot remove glandular breast tissue. If the enlargement is true gland, no amount of chest workouts will flatten it — this is the most common misunderstanding that delays treatment for years."),
            ("Are the scars visible?",
             "The main incision sits at the border of the areola, where the colour change camouflages it well. In most patients it fades to a faint line within months."),
            ("Can it come back after surgery?",
             "Properly removed gland does not regrow, but significant weight gain or certain medications can cause new enlargement. Your surgeon will discuss the factors relevant to you."),
        ],
        "related": ["liposuction", "tummy-tuck", "fue-hair-transplant"],
    },
    "liposuction": {
        "name": "Liposuction",
        "sections": [
            ("What Liposuction Actually Does",
             ["Liposuction removes localised fat deposits that resist diet and exercise — the abdomen, flanks, thighs, arms or chin. It is a body-contouring procedure, not a weight-loss method: the best candidates are near their normal weight with specific stubborn areas.",
              "The technique uses thin cannulas through tiny incisions to break up and suction fat, sculpting the area rather than simply deflating it. Modern approaches are gentler than the aggressive liposuction of decades past, but the principle is unchanged — judgement about how much to remove, and where, is everything."]),
            ("The Procedure and Anaesthesia",
             ["Depending on the extent, liposuction is done under local anaesthesia with sedation or general anaesthesia, usually as a day-care procedure. Small areas take about an hour; larger multi-area sculpting takes longer. Tiny incisions are hidden in natural creases wherever possible.",
              "There are safe limits to how much fat should be removed in one session. A responsible surgeon will stage the work or decline to do everything at once rather than chase an unsafe volume — this restraint is a mark of quality, not reluctance."]),
            ("Recovery and Results",
             ["Expect swelling and bruising for two to three weeks, with a compression garment worn to help the skin redrape smoothly. Most people return to office work within a week. The refined contour emerges over two to three months as swelling settles.",
              "Removed fat cells do not return to the treated area, but remaining cells can still enlarge with major weight gain — so stable habits protect your result. The outcome should look like a better version of you, not like a different person."]),
            ("Safety and Surgeon Choice",
             ["Liposuction is safe in trained hands but it is real surgery with real risks, including contour irregularities and fluid shifts. The facility should be properly equipped and the surgeon qualified in plastic surgery — this procedure demands anatomical knowledge that goes far beyond operating a cannula.",
              "Ask about the surgeon's training, the anaesthesia plan, and how complications are managed. Anyone who treats it as a lunchtime beauty treatment is someone to walk away from."]),
        ],
        "faqs": [
            ("Is liposuction a weight-loss surgery?",
             "No. It contours specific areas in people near their target weight. Large-volume fat removal for obesity is a different medical matter and needs a different kind of evaluation."),
            ("Will the fat come back?",
             "Fat cells removed from an area are gone permanently, but the remaining cells can expand if you gain significant weight. Stable weight keeps the contour."),
            ("How visible are the scars?",
             "Incisions are a few millimetres and placed in hidden creases. They typically fade to faint marks within months."),
        ],
        "related": ["tummy-tuck", "gynecomastia-surgery", "breast-augmentation"],
    },
    "rhinoplasty": {
        "name": "Rhinoplasty",
        "sections": [
            ("More Than a Cosmetic Operation",
             ["The nose sits at the centre of the face and of breathing — rhinoplasty is therefore both an aesthetic and a functional operation. Many patients need a deviated septum corrected at the same time as reshaping, and a good surgeon plans both together rather than treating them as separate problems.",
              "Indian noses have their own anatomical features — thicker skin, weaker cartilage support — which need techniques adapted to them, not copied from Western textbooks. This is why surgeon experience with noses like yours matters more than any before-and-after gallery."]),
            ("Planning Your New Nose",
             ["The consultation should be unhurried: your breathing assessed, your skin thickness evaluated, your facial proportions studied. Digital imaging can illustrate possibilities, but an honest surgeon will tell you it is a guide, not a promise.",
              "The aim is a nose that fits your face and your ethnicity — not a copied celebrity nose. Over-reduction is the classic error; a nose that looks operated is a failed rhinoplasty even if the patient asked for dramatic change."]),
            ("Surgery and Recovery",
             ["Rhinoplasty is usually done under general anaesthesia through incisions hidden inside the nostrils, sometimes with a small external cut under the tip. A splint protects the new shape for about a week. Most swelling settles in a month, but the tip refines over a full year — patience is part of the process.",
              "Plan a week off work and avoid glasses resting on the bridge initially. Your surgeon should see you at defined intervals through the first year, because late changes can need small adjustments."]),
            ("Choosing Your Surgeon",
             ["Ask specifically about rhinoplasty experience with noses like yours, revision rates, and how breathing outcomes are protected. The surgeon's answers about function tell you as much as their aesthetic portfolio.",
              "Be cautious of anyone who guarantees a particular look or dismisses the breathing assessment. The nose has to work beautifully, not just photograph beautifully."]),
        ],
        "faqs": [
            ("Will rhinoplasty affect my breathing?",
             "In skilled hands it should improve or preserve breathing — septal correction is often done together. Worsened breathing after rhinoplasty usually signals overly aggressive reduction."),
            ("How long until I see the final result?",
             "About 80 percent of swelling resolves in the first month, but tip definition keeps refining for up to a year, especially with thicker skin."),
            ("Is there much scarring?",
             "Most incisions are inside the nostrils and invisible. If an external approach is used, the small scar under the tip typically fades well."),
        ],
        "related": ["eyelid-surgery-blepharoplasty", "facelift", "lipoma-removal"],
    },
    "breast-augmentation": {
        "name": "Breast Augmentation",
        "sections": [
            ("A Personal Decision, Planned Carefully",
             ["Women consider augmentation for many reasons — asymmetry, volume lost after pregnancy, or simply the shape they have always wanted. Whatever the reason, the consultation should start with listening, not selling. Your anatomy, skin quality and goals determine what is possible.",
              "There is no single ideal size. Implants are chosen by proportion to your frame, existing tissue and lifestyle — an athlete and a new mother may suit very different choices. A surgeon who asks about your life, not just your cup size, is asking the right questions."]),
            ("Implants and Placement",
             ["Modern implants come in shapes, profiles and surfaces matched to different anatomies, placed either under the breast tissue or under the muscle. Each option has trade-offs in feel, mammography and recovery that should be explained plainly.",
              "Fat transfer is an alternative for modest enhancement without implants, using your own tissue — but it has limits on volume and may need more than one session. An honest discussion covers both paths."]),
            ("Surgery and Recovery",
             ["The operation takes one to two hours under general anaesthesia, usually as day care. Expect tightness and soreness for a week, a support bra for several weeks, and a gradual return to exercise. Implants settle into their final position over two to three months.",
              "Long-term, implants are not lifetime devices — they may need exchange after a decade or more, and routine follow-up matters. This should be stated upfront, not discovered years later."]),
            ("Safety and Expectations",
             ["Augmentation is safe in qualified hands, but it is surgery: risks include capsular contracture, implant issues and the need for revision. Your surgeon should discuss these as openly as the benefits and explain how they are managed in their practice.",
              "The best result looks like you on your best day — proportionate, natural, and comfortable in your own skin. Anyone pushing you toward a size you did not ask for is serving someone else's idea of beauty."]),
        ],
        "faqs": [
            ("How long do implants last?",
             "Modern implants are durable but not lifetime devices. Many last well over a decade; plan for the possibility of an exchange procedure in the future and keep up routine follow-ups."),
            ("Can I breastfeed after augmentation?",
             "Most women can, especially with certain incision and placement choices. Discuss your family plans openly at consultation so the plan protects them."),
            ("Will there be visible scars?",
             "Incisions are placed in the breast fold, around the areola or in the armpit — all chosen to hide well. They fade significantly with time."),
        ],
        "related": ["breast-reduction", "breast-reconstruction", "tummy-tuck"],
    },
    "tummy-tuck": {
        "name": "Tummy Tuck",
        "sections": [
            ("When Diet and Exercise Are Not Enough",
             ["After pregnancy or major weight loss, the abdominal wall can remain stretched with separated muscles and loose skin that no workout will tighten. A tummy tuck — abdominoplasty — removes excess skin, repairs the muscle separation and recontours the waistline.",
              "It is worth being clear about what it is not: not a weight-loss operation, and not a substitute for fitness. The best candidates are at a stable weight with specific excess tissue. Operating on someone still losing weight risks a result that loosens again."]),
            ("What the Surgery Involves",
             ["Through a low incision hidden below the underwear line, excess skin and fat are removed, the abdominal muscles are tightened with internal sutures, and the remaining skin is redraped smoothly. Liposuction of the flanks is often added for a balanced contour.",
              "A mini tuck suits those with looseness below the navel only; a full tuck addresses the whole abdomen. Your surgeon should explain which you need and why — the smaller operation is not always the right one."]),
            ("Recovery: The Honest Timeline",
             ["This is a bigger recovery than most aesthetic procedures: expect to walk bent for the first days, take two to three weeks off work, and avoid core strain for six to eight weeks. Drains, if used, are temporary. The tightness surprises most patients more than the pain.",
              "Scars fade over a year but never vanish entirely — the trade is a flat abdomen for a hidden scar. Good aftercare, compression and patience determine how well you heal."]),
            ("Choosing a Safe Pair of Hands",
             ["Abdominoplasty demands respect for blood supply and wound healing — it is one of the procedures where surgeon training most visibly matters. Ask about the surgeon's abdominoplasty volume, complication management and the facility's standards.",
              "Be wary of anyone minimising the recovery or offering it as an add-on bargain. A surgeon who insists you reach a stable weight first is protecting your result."]),
        ],
        "faqs": [
            ("Will I lose weight from a tummy tuck?",
             "Some tissue weight is removed, but it is a contouring operation, not a weight-loss method. Stable weight before surgery gives the longest-lasting result."),
            ("How bad is the scar?",
             "It runs low across the abdomen, designed to hide under clothing, and fades considerably over a year. The trade-off is flatness for a scar most patients find well worth it."),
            ("Can I have more children after?",
             "Future pregnancy is possible but may loosen the repair — most surgeons advise completing your family first for the best long-term result."),
        ],
        "related": ["liposuction", "breast-augmentation", "gynecomastia-surgery"],
    },
    "burn-reconstruction": {
        "name": "Burn Reconstruction",
        "sections": [
            ("Beyond Survival: Restoring Life After Burns",
             ["Modern burn care saves lives; reconstructive surgery restores living. Contractures that freeze joints, scars that distort the face, tight skin that stops a child growing normally — these are the problems burn reconstruction addresses, often in carefully timed stages.",
              "Timing is a medical decision, not a calendar one. Some procedures must wait for scars to mature; others cannot wait because a joint is stiffening or an eyelid cannot close. A burn surgeon plans a sequence over months or years, always balancing the next operation against healing and growth."]),
            ("What Reconstruction Can Achieve",
             ["Techniques range from scar release with skin grafting to tissue expansion and microsurgical flaps for complex defects. Each is chosen for the specific problem — there is no single burn operation, only a toolkit applied with judgement.",
              "The goals are function first, appearance alongside: a hand that grips, an eyelid that closes, a neck that turns. Cosmetic improvement follows functional restoration, and honest counselling sets expectations for each stage."]),
            ("The Journey Is Staged",
             ["Families should understand that burn reconstruction is usually a series of operations, not one event. Between stages there is therapy, pressure garments and patience. The surgeon's role includes coordinating this long arc, not just operating.",
              "For children, timing must respect growth — operating too early on a growing area can mean redoing work. A surgeon experienced in paediatric burns plans with the child's future body in mind."]),
            ("Getting the Right Care Early",
             ["The first treatment of a burn shapes everything that follows. Proper early wound care, correct depth assessment and timely referral to a burn or plastic surgeon prevent many late deformities entirely.",
              "If you or your child has an old burn contracture, it is rarely too late to improve — but earlier evaluation always gives more options. Do not assume nothing can be done."]),
        ],
        "faqs": [
            ("How soon after a burn can reconstruction start?",
             "Some releases are urgent — for example when a contracture threatens joint function or eye closure. Most elective scar work waits until scars mature, typically several months. Your surgeon will map the sequence."),
            ("Will the scars disappear completely?",
             "Reconstruction dramatically improves function and appearance, but burn scars never vanish entirely. Honest surgeons promise improvement, staged realistically — never erasure."),
            ("Is it too late for an old burn injury?",
             "Often not. Even years-old contractures can frequently be released with major functional gain. An evaluation costs nothing but can change everything."),
        ],
        "related": ["scar-keloid-treatment", "cleft-lip-palate-repair", "hand-trauma-surgery"],
    },
    "scar-treatment": {
        "name": "Scar Treatment",
        "sections": [
            ("Why Scars Form — and Why Some Misbehave",
             ["Every cut that reaches the dermis heals with a scar; it is the body's repair, not a flaw. Most scars fade and flatten over a year. But some grow thick and raised (hypertrophic scars) or spread beyond the original wound (keloids), itching, paining and distressing far beyond their size.",
              "Your tendency to form such scars is partly genetic — keloids run in families and are more common in darker skin. Knowing this at the time of any surgery or injury lets your surgeon plan prevention rather than cure."]),
            ("Treatment Options, Honestly Explained",
             ["Treatment is matched to the scar: silicone therapy and pressure for early scars, steroid injections for thick ones, laser for redness and texture, and surgical revision — excising the scar and reclosing with meticulous technique — for the worst cases. Often these combine in a plan.",
              "Keloids are the hardest: they can recur even after perfect excision, so treatment usually pairs surgery with injections or radiation in a protocol. Anyone promising a keloid will never return is overselling."]),
            ("Surgical Scar Revision",
             ["Revision is not erasing a scar but exchanging a bad one for a better one — reorienting it along natural skin lines, releasing tension, or breaking a long scar into a less visible zigzag. The new scar still needs a year to mature.",
              "Timing matters: revising an immature, still-red scar is usually premature. A good surgeon will often ask you to wait, treating impatience as part of the counselling."]),
            ("Prevention Beats Cure",
             ["If you scar badly, tell every surgeon before any operation — elective or emergency. Preventive silicone, careful closure technique and early intervention change outcomes dramatically.",
              "For existing problem scars, an evaluation by a plastic surgeon — the specialty trained in wound healing — is the right first step, not another cream bought online."]),
        ],
        "faqs": [
            ("Can scars be completely removed?",
             "No scar can be erased entirely, but bad scars can often be made dramatically better — flatter, paler, less tight. Honest improvement, not invisibility, is the goal."),
            ("What is the difference between a keloid and a hypertrophic scar?",
             "A hypertrophic scar stays within the wound boundary and often improves with time; a keloid grows beyond it and rarely regresses alone. They need different strategies."),
            ("How long should I wait before scar revision?",
             "Usually until the scar matures — around a year — unless it is causing functional problems. Early assessment is still wise so a plan is ready."),
        ],
        "related": ["burn-reconstruction", "cleft-lip-palate-repair", "laser-treatments"],
    },
    "hand-surgery": {
        "name": "Hand Surgery",
        "sections": [
            ("Why Hand Injuries Need a Specialist",
             ["The hand packs bones, tendons, nerves and vessels into a tiny space — a cut that looks small can divide structures that determine whether a finger ever bends again. General wound closure is not hand surgery; the difference shows up months later in stiffness and lost function.",
              "Common injuries — kitchen knife slips, machine crushes, bike chain accidents, glass cuts — each threaten different structures. The first assessment decides everything: what is divided, what is the window for repair, and what the hand can ultimately recover."]),
            ("Tendons, Nerves and Microsurgery",
             ["Cut tendons must be repaired precisely and mobilised on a strict therapy schedule — too still and they stick, too early and they rupture. This balance is the art of hand surgery, and it needs a surgeon and therapist working as a team.",
              "Divided nerves and vessels need microsurgery: repair under the microscope with sutures finer than hair. Replantation of a severed finger is the most dramatic example, but the same skill repairs the nerve that restores feeling to a fingertip."]),
            ("Fractures and Stiffness",
             ["Hand fractures need exact alignment — a millimetre of rotation in a finger bone shows every time you make a fist. Many are fixed with tiny screws or wires so movement can start early, because a hand that stays still stiffens fast.",
              "Stiffness after injury or surgery is the commonest enemy of a good outcome, which is why hand therapy is not optional extras but half the treatment. Your surgeon's therapy protocol matters as much as their stitching."]),
            ("When to Rush, When to Plan",
             ["Clean cuts with suspected tendon or nerve injury, crush injuries and amputations are emergencies — hours matter for the best repair. Do not let a casualty dress it and send you home without a hand assessment if you cannot move or feel a finger properly.",
              "For older injuries with stiffness or deformity, it is often still worth an evaluation — secondary reconstruction can recover surprising function even months later."]),
        ],
        "faqs": [
            ("I cut my finger and it still bends — do I need a hand surgeon?",
             "Partial tendon injuries can still bend but worsen or rupture later. If the cut was deep or near a joint, get it assessed — a quick examination beats a missed injury."),
            ("How soon should a hand injury be treated?",
             "Tendon and nerve repairs are best within days; replantation within hours. Even so, older injuries often still benefit from evaluation."),
            ("Will my hand be normal again?",
             "Many injuries recover excellently with proper repair and therapy, but honesty matters: severe crush injuries may leave some deficit. Your surgeon should give a realistic forecast, not a blanket reassurance."),
        ],
        "related": ["microsurgery-free-flap", "tendon-repair", "nerve-repair-microsurgery"],
    },
    "botox-fillers": {
        "name": "Botox & Fillers",
        "sections": [
            ("What Injectables Can — and Cannot — Do",
             ["Botox relaxes the muscles that etch frown lines, forehead lines and crow's feet; fillers restore volume lost to age in cheeks, lips and under-eyes. Together they refresh without surgery — but they cannot lift significantly sagging skin or replace a facelift.",
              "The difference between natural and frozen lies entirely in dosing and placement. Conservative treatment that preserves expression always beats an aggressive session. A doctor who suggests less than you asked for is usually the one to trust."]),
            ("Safety Is About Who Holds the Syringe",
             ["These are medical procedures with real anatomy behind them — filler in the wrong plane can block a vessel with serious consequences. The injector must know facial vascular anatomy and have hyaluronidase and emergency protocols ready.",
              "In India, injectables are widely offered by underqualified providers. The product in the syringe matters less than the training of the hand holding it. Ask who will inject you, what their medical qualification is, and what happens if something goes wrong."]),
            ("What a Session Feels Like",
             ["Treatment takes minutes with numbing cream; Botox shows effect in a week and lasts three to four months, while fillers are immediate and last six to eighteen months depending on product and area. Mild swelling or bruising settles in days.",
              "There is no downtime worth the name — most people return to work the same day. That convenience is exactly why the provider's qualification matters more, not less."]),
            ("A Sensible Approach to Ageing",
             ["The best injectable work is invisible: you look rested, not different. Start conservatively, review in two weeks, and build a long-term plan rather than chasing each new trend.",
              "And know when injectables are the wrong answer — deep jowls or heavy neck laxity need surgery, and an honest doctor will say so instead of selling syringe after syringe."]),
        ],
        "faqs": [
            ("Is Botox safe?",
             "In qualified hands, with genuine product and correct dosing, Botox has a decades-long safety record. Problems almost always trace to unqualified injectors or counterfeit product."),
            ("Will fillers make my face look unnatural?",
             "Only if overdone or badly placed. Conservative, anatomy-respecting filler looks natural — the 'done' look comes from excess, not from the product itself."),
            ("How often do I need to repeat?",
             "Botox every three to four months, fillers every six to eighteen months depending on the area and product. Your doctor should plan maintenance honestly, not push top-ups."),
        ],
        "related": ["chemical-peels", "laser-treatments", "facelift"],
    },
    "facelift": {
        "name": "Facelift",
        "sections": [
            ("What a Facelift Actually Lifts",
             ["A facelift repositions sagging cheeks, softens deep folds around the mouth, firms the jawline and tightens a loose neck — it works on the deeper SMAS layer, not just the skin, which is why modern results look natural rather than pulled.",
              "What it does not do is change who you are. The goal is to look like yourself on a good day, several years ago — rested, not different. Anyone showing you dramatic celebrity transformations as the standard promise is selling, not counselling."]),
            ("Who Benefits Most — and Who Should Wait",
             ["The best candidates are typically in their forties to sixties with good skin elasticity and sagging that fillers can no longer camouflage. Bone structure matters too — strong cheekbones and a defined jaw hold a lift beautifully.",
              "Smokers face markedly higher complication rates and are usually asked to quit well before surgery. Equally, if your main concern is fine wrinkles or sun damage rather than sagging, resurfacing or injectables may serve you better — an honest surgeon will say so."]),
            ("The Surgery and Recovery, Honestly",
             ["Surgery takes three to five hours under general anaesthesia, with incisions hidden in the hairline and around the ear. Most patients go home the same day or the next morning.",
              "Expect bruising and swelling for about two weeks — the classic 'social downtime'. Numbness around the ears can linger for months, and scars, though well hidden, take a year to fully mature. Final softness of result arrives gradually, not on day one."]),
            ("Surgical vs Non-Surgical: the Honest Line",
             ["Fillers, threads and energy devices have real roles, but none of them replicate what surgery does for significant jowls or neck laxity. Non-surgical options buy time; they do not turn back the clock the way a lift does.",
              "A mini-lift suits early jowling with minimal neck involvement; heavier laxity needs a full approach. Be wary of anyone offering a 'lunchtime lift' for a neck that clearly needs surgery — the right operation matters more than the smallest scar."]),
        ],
        "faqs": [
            ("How long does a facelift last?",
             "Most patients enjoy the benefit for eight to twelve years, though ageing continues — a facelift resets the clock rather than stopping it. Skin quality, sun exposure and smoking influence longevity."),
            ("Will I look like a different person?",
             "No — a well-done facelift restores your own younger contours. The 'windswept' look comes from outdated skin-only techniques, not from modern deep-plane surgery."),
            ("What are the main risks?",
             "Bleeding under the skin (haematoma) is the commonest early issue and is treatable; temporary or rarely lasting weakness of a facial-nerve branch is the risk your surgeon should discuss openly. Choosing a qualified plastic surgeon is the single biggest risk reducer."),
        ],
        "related": ["eyelid-surgery-blepharoplasty", "botox-treatment", "chemical-peels"],
    },
    "cleft-lip-palate": {
        "name": "Cleft Lip & Palate",
        "sections": [
            ("What a Cleft Is",
             ["A cleft lip, cleft palate, or both occur when the face does not fully fuse during early pregnancy — among the commonest birth differences worldwide. It affects feeding, and later speech and hearing, but it is very treatable.",
              "It is nobody's fault: most clefts happen by chance, though a family history slightly raises the odds. What matters now is getting the child into a proper cleft-care pathway early."]),
            ("The Treatment Timeline",
             ["Lip repair usually happens at three to six months, palate repair between nine and eighteen months — timed to support feeding, hearing and speech development. This is staged care, not a single operation.",
              "Through childhood come speech therapy, orthodontics, and sometimes bone grafting or nasal refinement in the teens. The journey is long but mapped out; families should expect a team, not just a surgeon."]),
            ("Feeding and Early Care",
             ["Babies with cleft palate cannot create suction, so special bottles and teats make feeding possible — weight gain before surgery is the first milestone. A cleft team nurse or counsellor usually guides parents through this.",
              "Ear infections are common because palate muscles affect the middle ear; hearing checks belong in the routine. None of this needs panic — it needs a plan."]),
            ("Beyond Surgery: Speech and Confidence",
             ["Surgery closes the gap; speech therapy teaches the child to use the repaired palate well. Most children with good team care speak clearly and thrive in regular schools.",
              "As they grow, confidence matters as much as anatomy. Honest, age-appropriate conversations — and meeting other cleft-affected families — help enormously."]),
        ],
        "faqs": [
            ("When should cleft surgery be done?",
             "Lip repair at 3–6 months and palate repair at 9–18 months is the standard sequence, balancing anaesthesia safety with speech development. Your cleft team sets the exact dates."),
            ("Will my child's speech be normal?",
             "With timely palate repair and speech therapy, most children develop clear speech. Some need a secondary speech surgery later — your team monitors for this."),
            ("Will it happen again in a future pregnancy?",
             "The recurrence risk is modestly higher than the general population but still low for most families; a genetic counsellor can give you personalised odds."),
        ],
        "related": ["rhinoplasty", "scar-keloid-treatment", "burn-reconstruction"],
    },
    "lipoma-removal": {
        "name": "Lipoma Removal",
        "sections": [
            ("What Lipomas Are",
             ["Lipomas are benign lumps of fat under the skin — soft, mobile, usually painless, and very common from middle age onward. Most are harmless and many never need treatment.",
              "The key question at first visit is identification: a proper examination distinguishes a classic lipoma from cysts, and rarely from something needing deeper investigation. When in doubt, imaging or a biopsy settles it."]),
            ("When Removal Makes Sense",
             ["Consider removal if the lump is growing, painful, pressing on nearby structures, cosmetically bothersome, or if the diagnosis is uncertain. 'Watch and wait' is perfectly valid for small, stable, classic lipomas.",
              "Multiple lipomas run in some families (familial lipomatosis) — each is judged on its own merits, and removal of one does not prevent others appearing."]),
            ("The Procedure Itself",
             ["Most lipomas come out through a small excision under local anaesthesia as a day-care procedure — the lump is shelled out whole with its capsule. Larger or deep ones may need a bigger incision or sedation.",
              "Liposuction can shrink suitable lipomas through tiny openings, trading a smaller scar for a slightly higher chance of residual tissue. Your surgeon matches technique to the lump."]),
            ("After Removal",
             ["A small scar and a few days of soreness are the norm; stitches come out in about a week. The removed tissue is usually sent for histopathology — routine confirmation that it was indeed benign.",
              "True recurrence at the same spot is uncommon when the capsule is fully removed. Report any new or changing lump rather than assuming it is 'just another lipoma'."]),
        ],
        "faqs": [
            ("Can a lipoma turn cancerous?",
             "Essentially no — lipomas are benign. The rare malignant counterpart, liposarcoma, is a different tumour that is usually deep, large and fast-growing, which is why uncertain lumps get investigated."),
            ("Will it come back after removal?",
             "Recurrence at the same site is uncommon with complete excision. New lipomas elsewhere are possible, especially if you are prone to them."),
            ("Is surgery the only option?",
             "For a bothersome or uncertain lump, excision is the definitive option and gives tissue for diagnosis. Steroid injections can shrink some lipomas but do not remove them."),
        ],
        "related": ["liposuction", "scar-keloid-treatment", "laser-treatments"],
    },
    "prp-therapy": {
        "name": "PRP Therapy",
        "sections": [
            ("What PRP Actually Is",
             ["PRP — platelet-rich plasma — is made from your own blood: it is drawn, spun in a centrifuge to concentrate the platelets, and injected where needed. Platelets carry growth factors involved in healing, which is the biological rationale.",
              "Because it is autologous, allergy risk is negligible. It is used across hair restoration, skin rejuvenation, and some joint and tendon problems — with very different levels of evidence in each."]),
            ("Where the Evidence Is Strong — and Where It Is Thin",
             ["The most reasonable evidence is in early hair thinning, where PRP may improve density as an adjunct — not as a replacement for transplant or medication. Results vary person to person.",
              "For skin rejuvenation and 'vampire facials', the evidence is modest and heavily marketed beyond what studies support. Honest clinics present PRP as a possible enhancer, never a miracle. Anyone guaranteeing regrowth is overselling."]),
            ("What a Session Involves",
             ["A session takes under an hour: blood draw, preparation, and a series of small injections, usually with numbing. Mild soreness or swelling for a day or two is common.",
              "Protocols typically run three to four sessions spaced a month apart, then maintenance. One sitting is rarely the whole plan — ask for the full protocol and cost upfront."]),
            ("Who Should Skip It",
             ["PRP is unsuitable with platelet disorders, active scalp infection, or certain blood conditions. It also cannot create hair where follicles are long dead — slick bald areas do not respond.",
              "If your main problem is advanced baldness, a transplant consultation is the honest next step, not endless PRP packages."]),
        ],
        "faqs": [
            ("Does PRP regrow hair?",
             "It may improve density in early thinning as part of a plan, but it does not replace hair transplant surgery or proven medications. Slick bald scalp does not respond."),
            ("Is the procedure painful?",
             "With numbing cream or local anaesthesia it is uncomfortable rather than painful — a series of pinpricks. Most people tolerate it well."),
            ("How many sessions will I need?",
             "Typically three to four monthly sessions, then periodic maintenance. Be cautious of clinics selling large packages before assessing your first response."),
        ],
        "related": ["fue-hair-transplant", "chemical-peels", "laser-treatments"],
    },
    "chemical-peels": {
        "name": "Chemical Peels",
        "sections": [
            ("What Peels Do",
             ["Chemical peels apply a controlled acid solution to remove damaged outer skin layers — improving pigmentation, uneven texture, acne marks and fine lines as fresh skin regenerates.",
              "Depth matters: superficial peels (glycolic, salicylic) refresh with minimal downtime; medium peels (TCA) reach deeper with a week of peeling; deep peels are powerful but carry real risks and are rarely needed today."]),
            ("Matching the Peel to Indian Skin",
             ["Darker skin types scar and pigment differently — post-inflammatory hyperpigmentation is the main risk, so peels must be chosen and primed carefully. This is why the 'same peel for everyone' approach fails.",
              "A good clinic primes the skin for two to four weeks before stronger peels and insists on strict sun protection after. If nobody discusses your skin type before recommending a peel, walk away."]),
            ("What Treatment Feels Like",
             ["Expect tingling or warmth during the few minutes the peel is on, then tightness as peeling begins over two to five days. Superficial peels let you work through it; medium peels need social downtime.",
              "Aftercare is the treatment: gentle cleansing, moisturiser, and non-negotiable sunscreen. Picking at peeling skin is the fastest route to the pigmentation you came to fix."]),
            ("Peels vs Lasers vs Creams",
             ["Peels excel at surface pigmentation and texture at modest cost; lasers target deeper or vascular issues; creams maintain but rarely transform. Often they combine in a plan.",
              "No single modality fixes everything — a clinic offering only peels will recommend peels for everything. Look for a practice with options and the honesty to match the tool to the problem."]),
        ],
        "faqs": [
            ("Are peels safe for dark skin?",
             "Superficial peels are generally safe with proper priming and aftercare; medium and deep peels carry higher pigmentation risk and need an experienced hand. Your skin type should drive the choice."),
            ("How many sessions will I need?",
             "Superficial peels usually run as a course of four to six, spaced two to four weeks apart. Medium peels may need only one or two a year."),
            ("Can I do a peel at home?",
             "Mild home peels exist, but anything beyond superficial strength belongs in a clinic — burns and pigmentation from unsupervised peels are a regular sight in dermatology practice."),
        ],
        "related": ["laser-treatments", "prp-therapy", "botox-treatment"],
    },
    "laser-hair-removal": {
        "name": "Laser Hair Removal",
        "sections": [
            ("How It Works",
             ["Laser hair removal targets melanin in the hair shaft — light energy converts to heat and damages the follicle. Because only actively growing hairs are vulnerable, and only a fraction are growing at once, multiple sessions are a biological necessity, not a sales tactic.",
              "Different lasers suit different skin: Nd:YAG is generally the safer choice for darker Indian skin, while alexandrite and diode suit lighter types. The machine matters less than the operator's judgment."]),
            ("Who It Suits Best — and Its Limits",
             ["Dark, coarse hair responds best; fine, grey, blonde or white hair responds poorly because there is little melanin to target. Hormonal conditions like PCOS need medical management alongside laser, or regrowth outpaces treatment.",
              "It is hair reduction, not always total elimination — expect a large, lasting reduction with occasional maintenance, not a promise that no hair will ever return."]),
            ("What Sessions Feel Like",
             ["Most describe a rubber-band snap with each pulse; modern machines pair this with cooling. Redness for a few hours is normal; blistering is not and signals wrong settings for your skin.",
              "Sessions are quick — upper lip in minutes, full legs longer — spaced four to eight weeks apart as hair cycles dictate. Shave before; do not wax between sessions, since the root must be present."]),
            ("Safety and Choosing a Clinic",
             ["In trained hands with medical-grade machines, it is very safe. Burns and pigmentation changes almost always trace to underqualified operators, wrong wavelength for the skin type, or recent tanning.",
              "Ask who operates the laser, their medical qualification, and which machine they use for your skin type. Package deals are fine — but the per-session assessment matters more than the discount."]),
        ],
        "faqs": [
            ("Is laser hair removal permanent?",
             "It gives long-lasting reduction — most people see a major, durable decrease with occasional maintenance sessions. Fine regrowth can occur, especially with hormonal shifts."),
            ("Is it safe for Indian skin?",
             "Yes, with the right laser (Nd:YAG is preferred for darker skin) and conservative settings. Recent sun exposure or tanning should delay treatment."),
            ("How many sessions do I need?",
             "Typically six to eight for substantial reduction, sometimes more for hormonal areas. Anyone promising completion in two sessions is not being straight with you."),
        ],
        "related": ["chemical-peels", "botox-treatment", "scar-keloid-treatment"],
    },
    "skin-grafting": {
        "name": "Skin Grafting",
        "sections": [
            ("What a Skin Graft Is",
             ["A skin graft moves healthy skin from one part of your body (the donor site) to cover a wound elsewhere. Split-thickness grafts take the top layers; full-thickness grafts take all layers and suit visible areas like the face and hands.",
              "It is one of plastic surgery's foundational techniques — simple in concept, demanding in execution, because the graft survives only if conditions are exactly right."]),
            ("When Grafts Are Needed",
             ["Burns, road-traffic injuries, cancer excisions and non-healing ulcers are the common reasons — anywhere a wound is too large or too deep to close directly or heal alone.",
              "The decision balances the wound's needs against donor-site cost: grafting trades one wound for two, so it is chosen when the benefit clearly outweighs that trade."]),
            ("The Two Wounds",
             ["The graft site needs immobilisation, pressure dressings and infection control for the first critical week while new blood vessels grow in. The donor site — often the thigh — heals like a graze over two to three weeks.",
              "Both sites need care: the donor site can be surprisingly sore, and the graft must not be disturbed while it 'takes'. Follow the dressing protocol exactly."]),
            ("What Determines Success",
             ["Graft take depends on a clean wound bed, good contact, stillness and absence of infection — most grafts take well when these align. Partial loss happens occasionally and usually heals with dressings or a touch-up.",
              "Expect the graft to look different from surrounding skin at first — paler or pinker, with different texture. It settles over months but rarely matches perfectly; your surgeon should set this expectation upfront."]),
        ],
        "faqs": [
            ("Does the donor site leave a scar?",
             "Yes, though it usually fades to a pale patch over months. Split-thickness donor sites heal on their own; full-thickness ones need closure and leave a linear scar."),
            ("How long does healing take?",
             "The graft is most vulnerable in the first week; meaningful healing takes two to three weeks, with maturation over months. Dressing appointments are part of the plan."),
            ("Will the graft look like normal skin?",
             "Close, not identical — colour and texture differences are usual, more noticeable with split-thickness grafts. Full-thickness grafts match better on the face and hands."),
        ],
        "related": ["burn-reconstruction", "scar-keloid-treatment", "microsurgery-free-flap"],
    },
    "eyelid-surgery": {
        "name": "Eyelid Surgery",
        "sections": [
            ("What Blepharoplasty Addresses",
             ["Upper eyelid surgery removes hooded, overhanging skin that makes you look tired — and in severe cases actually blocks the upper visual field. Lower lid surgery addresses under-eye bags from fat prolapse and loose skin.",
              "It is worth distinguishing puffiness from dark circles: bags are structural and surgical; pigmentation is a skin issue needing different treatment. A good consultation tells you which you have."]),
            ("Upper vs Lower Lids",
             ["Upper blepharoplasty hides its scar in the natural eyelid crease. Lower lids are approached through the skin or from inside the lid (transconjunctival) when only fat needs addressing — the inside approach leaves no visible scar.",
              "Mild lid droop (ptosis) is a muscle problem, not an excess-skin problem, and needs a different operation. Conflating the two is a common source of disappointing results."]),
            ("Surgery and Recovery",
             ["The operation takes one to two hours, usually under local anaesthesia with sedation, as day care. Bruising and swelling peak in the first week and largely settle by two — sunglasses become your best friend.",
              "Scars mature over months but hide well. Dryness or tightness early on is common and temporary; your surgeon should warn you rather than letting you discover it."]),
            ("When It Is Medical, Not Cosmetic",
             ["When drooping lids obstruct vision, surgery is functional — visual-field testing can document this. Insurance and medical logic both recognise the distinction.",
              "Either way, the aim is the same: eyes that look like yours, rested. Over-resection gives the hollow, startled look — conservative, anatomy-respecting surgery avoids it."]),
        ],
        "faqs": [
            ("Will eyelid surgery change how I look?",
             "You should look like yourself, rested — not like a different person. The startled look comes from removing too much, which a conservative surgeon avoids."),
            ("How long do the results last?",
             "Upper lid results typically last many years; lower lids longer still. Ageing continues, so some change over the decades is natural."),
            ("What are the risks?",
             "Dry eyes and minor asymmetry are the commonest issues and usually temporary. Serious complications like vision problems are rare in qualified hands — which is why surgeon choice matters."),
        ],
        "related": ["facelift", "botox-treatment", "chemical-peels"],
    },
}


QUEUE_FILE = "/home/hatch/workspace/ar-website/district_article_queue.json"


def make_article(district_slug, proc_slug, date_str):
    dist = next(d for d in DISTRICTS if d[0] == district_slug)
    proc = ARTICLE_PROCEDURES[proc_slug]
    dslug, dname, dkm, dnote = dist
    pname = proc["name"]
    if dkm == 0:
        travel = (f"You are in luck — AR Plastic Surgery is right here in {dname}, {dnote}. "
                  "Consultation, procedure and follow-ups all happen minutes from home.")
    else:
        travel = (f"{dname} is about {dkm} km from Karimnagar — {dnote}. "
                  f"Patients from {dname} regularly make the trip: consultation and planning in one visit, "
                  "the procedure on a scheduled day, and follow-ups that respect your travel.")
    slug = f"{proc_slug}-{dslug}-guide"
    h1 = f"{pname} for {dname} Patients: A Complete Guide"
    title = f"{pname} in {dname}: Guide & Clinic | AR Plastic Surgery"
    if len(title) > 68:
        title = f"{pname}, {dname}: Patient Guide | AR Plastic Surgery"
    desc = (f"Considering {pname.lower()} and living in {dname}? Dr Ashok Reddy (MBBS, DNB, M.Ch, Gold Medalist) "
            f"explains candidacy, procedure, recovery and costs — plus travel planning from {dname} to Karimnagar.")
    if len(desc) > 168:
        desc = (f"Considering {pname.lower()} in {dname}? Dr Ashok Reddy explains candidacy, procedure and recovery, "
                f"plus travel planning from {dname} to Karimnagar.")
    lede = (f"If you live in {dname} and are thinking about {pname.lower()}, this guide covers everything: "
            f"whether you are a candidate, what the procedure involves, how recovery works, and how to plan "
            f"your visits from {dname} to AR Plastic Surgery in Karimnagar.")
    sections = [(h, list(ps)) for h, ps in proc["sections"]]
    sections.insert(2, (f"Getting Treated from {dname}",
        [travel,
         f"Tip: book a morning consultation so assessment, blood work and planning finish the same day. "
         f"For procedures needing an overnight stay, Karimnagar has comfortable lodging near the clinic — "
         f"ask the team when you book, and they will help you plan."]))
    sections.append((f"Why Patients from {dname} Choose AR Plastic Surgery",
        [f"Dr Ashok Reddy (MBBS, DNB Mumbai, M.Ch Delhi) was awarded the Gold Medal for Plastic & Reconstructive "
         f"Surgery at ABVIMS, Dr RML Hospital, New Delhi — training that shows in careful planning and honest counselling.",
         f"Every consultation starts with whether you actually need the procedure. Patients from {dname} and across "
         f"Telangana travel here for that honesty as much as for the surgery itself."]))
    return {
        "slug": slug,
        "h1": h1,
        "title": title,
        "desc": desc,
        "lede": lede,
        "date": date_str,
        "sections": sections,
        "faqs": proc["faqs"],
        "related_procedures": proc["related"],
    }


def next_queue_item():
    import json, os
    combos = [(d[0], p) for d in DISTRICTS for p in ARTICLE_PROCEDURES]
    done = set()
    if os.path.exists(QUEUE_FILE):
        done = set(tuple(x) for x in json.load(open(QUEUE_FILE)))
    for combo in combos:
        if combo not in done:
            return combo
    return None


def mark_done(district_slug, proc_slug):
    import json, os
    done = []
    if os.path.exists(QUEUE_FILE):
        done = json.load(open(QUEUE_FILE))
    done.append([district_slug, proc_slug])
    json.dump(done, open(QUEUE_FILE, "w"))
