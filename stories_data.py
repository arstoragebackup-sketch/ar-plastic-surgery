# Google Web Stories content — one story per uploaded YouTube Short.
# Each story: cover + content slides + CTA. Keep text short (stories are visual).
# Fields: slug, title, desc, youtube_id, color (theme), slides[(heading, text)]

BASE_CTA = ("Book Your Consultation",
            "AR Plastic Surgery, Karimnagar — Dr Ashok Reddy (MBBS, DNB, M.Ch, Gold Medalist). "
            "Open all 7 days, 10 AM – 8 PM.")

STORIES = [
    {
        "slug": "hair-transplant-5-checks",
        "title": "5 Checks Before a Hair Transplant",
        "desc": "Planning a hair transplant in Karimnagar? Dr Ashok Reddy explains 5 things to verify before choosing a clinic. Web story by AR Plastic Surgery.",
        "youtube_id": "CWpc34EG0mY",
        "color": "#0f2a4a",
        "slides": [
            ("Who does the surgery?", "A qualified plastic surgeon should plan and perform it — not just a technician."),
            ("See real results", "Ask for genuine before-and-after cases, not stock photos."),
            ("An honest plan", "Grafts matched to your hair loss pattern — not a one-size package."),
            ("Safety first", "Proper clinic, sterile OT, emergency readiness. Never compromise."),
            ("Aftercare matters", "A clear follow-up plan — not 'pay and disappear'."),
        ],
    },
    {
        "slug": "torn-earlobe-repair",
        "title": "Torn Earlobe? Lobuloplasty Can Repair It",
        "desc": "Split earlobe from heavy earrings? Dr Ashok Reddy explains lobuloplasty — a quick repair under local anaesthesia. Web story by AR Plastic Surgery, Karimnagar.",
        "youtube_id": "nbgdqfFb4Lo",
        "color": "#5b2a6e",
        "slides": [
            ("Why earlobes split", "Years of heavy earrings can slowly tear the earlobe."),
            ("A simple repair", "Lobuloplasty is done under local anaesthesia — you're awake, no pain."),
            ("About 30 minutes", "A short, precise procedure with fine stitches."),
            ("Wear earrings again", "After healing, you can pierce and wear earrings normally."),
        ],
    },
    {
        "slug": "breast-augmentation-guide",
        "title": "Breast Augmentation: What to Know First",
        "desc": "Considering breast augmentation? Dr Ashok Reddy on proportion, implant choice, and honest expectations. Web story by AR Plastic Surgery, Karimnagar.",
        "youtube_id": "Q6K8kjZdLTk",
        "color": "#7a2d4a",
        "slides": [
            ("It's about proportion", "The right size fits your frame and your comfort — never a 'standard size'."),
            ("Implant choice matters", "Shape, size, and placement are planned around your body and goals."),
            ("Honest discussion", "A good surgeon explains risks as clearly as benefits."),
            ("Recovery", "Most patients return to routine in 1–2 weeks."),
        ],
    },
    {
        "slug": "child-burns-first-aid",
        "title": "Child Burns: First Aid That Matters",
        "desc": "Hot water burn on a child? Cool it, cover it, and get care fast. Dr Ashok Reddy's essential first-aid guide for parents. AR Plastic Surgery, Karimnagar.",
        "youtube_id": "l7njhImsCWo",
        "color": "#a33b1f",
        "slides": [
            ("Cool it fast", "Hold the burn under cool running water for 20 minutes."),
            ("Don't apply these", "No toothpaste, oil, butter, or ice — they worsen the injury."),
            ("Cover loosely", "Use a clean, non-fluffy cloth. Don't pop blisters."),
            ("Children burn deeper", "A child's thin skin burns faster and deeper — see a doctor quickly."),
        ],
    },
    {
        "slug": "childhood-burns-care",
        "title": "Childhood Burns: Right Care, Right Time",
        "desc": "Burns in children heal differently from adults. Dr Ashok Reddy on timed care that prevents lifelong scars and contractures. Web story by AR Plastic Surgery, Karimnagar.",
        "youtube_id": "9v-7iTb2hSQ",
        "color": "#a33b1f",
        "slides": [
            ("Children heal differently", "Growing skin responds to burns unlike adult skin."),
            ("Early care prevents contractures", "Timely treatment stops scars from tightening joints."),
            ("Surgery is timed", "Some corrections are planned as the child grows."),
            ("Don't wait years", "Hoping it improves on its own can cost function later."),
        ],
    },
    {
        "slug": "facial-trauma-care",
        "title": "Facial Trauma Needs a Plastic Surgeon's Eye",
        "desc": "Facial trauma from road accidents needs expert repair. Dr Ashok Reddy on treating facial injuries. Web story by AR Plastic Surgery, Karimnagar.",
        "youtube_id": "z9l6l6ku6G0",
        "color": "#1f5a5a",
        "slides": [
            ("Road accidents lead", "Most serious facial injuries come from bike and road crashes."),
            ("More than skin", "Bones, nerves, and soft tissue may all need repair together."),
            ("Early treatment wins", "The first repair gives the best functional and cosmetic result."),
            ("Beyond stitches", "Deep facial cuts deserve layered plastic-surgical closure."),
        ],
    },
    {
        "slug": "bike-chain-hand-safety",
        "title": "Cleaning Your Bike? Protect Your Hands",
        "desc": "A moving bike chain can crush fingers in seconds. Hand safety tips from Dr Ashok Reddy, hand & microvascular surgeon. Web story by AR Plastic Surgery.",
        "youtube_id": "e4EKtoJL9nM",
        "color": "#3d3d3d",
        "slides": [
            ("Seconds to disaster", "A moving chain and sprocket can crush a finger instantly."),
            ("Never bare-handed", "Don't clean a running bike's chain with your hands."),
            ("Engine off, every time", "Switch off before your fingers go near the chain."),
            ("Crush injuries are complex", "A crushed finger may need microvascular surgery to save."),
        ],
    },
    {
        "slug": "hydrafacial-guide",
        "title": "HydraFacial: Deep Cleanse & Hydration",
        "desc": "What is HydraFacial and is it right for your skin? Dr Ashok Reddy explains this gentle, no-downtime treatment. Web story by AR Plastic Surgery, Karimnagar.",
        "youtube_id": "9hwA1da26cY",
        "color": "#2a6e5b",
        "slides": [
            ("Gentle and non-invasive", "No needles, no harsh peeling — suitable for most skin types."),
            ("Three steps in one", "Cleanses, exfoliates, and hydrates in a single session."),
            ("Zero downtime", "Walk out glowing — back to your day immediately."),
            ("Doctor-led is safer", "Skin treatments belong under medical supervision."),
        ],
    },
    {
        "slug": "choose-plastic-surgeon-red-flags",
        "title": "Choosing a Plastic Surgeon? 4 Red Flags",
        "desc": "How to choose a plastic surgeon safely — 4 red flags Dr Ashok Reddy says every patient should know before deciding. Web story by AR Plastic Surgery, Karimnagar.",
        "youtube_id": "QQKyFMLzUCc",
        "color": "#6e2a2a",
        "slides": [
            ("Promises of certain results", "No honest surgeon ever promises you a certain outcome."),
            ("Hidden credentials", "Check for real qualifications — MBBS, MS/M.Ch in plastic surgery."),
            ("Pressure to decide now", "Good clinics inform you; they never rush you."),
            ("No proof of work", "Ask for genuine results and patient reviews."),
        ],
    },
    {
        "slug": "what-is-plastic-surgery",
        "title": "What Is Plastic Surgery, Really?",
        "desc": "Plastic surgery is far more than cosmetic procedures. Dr Ashok Reddy explains the full scope of this surgical specialty. Web story by AR Plastic Surgery, Karimnagar.",
        "youtube_id": "2gnvQx7rSgk",
        "color": "#0f2a4a",
        "slides": [
            ("'Plastic' means to reshape", "The word comes from 'plastikos' — to mould, not plastic material."),
            ("Burns and trauma", "Burn reconstruction and injury repair are core plastic surgery."),
            ("Hands and birth defects", "Hand surgery, cleft repair — restoring function and form."),
            ("Cosmetic is one branch", "Aesthetic surgery is part of a vast reconstructive specialty."),
        ],
    },
    {
        "slug": "consultation",
        "title": "Book a Consultation",
        "desc": "Book a consultation with Dr Ashok Reddy at AR Plastic Surgery, Karimnagar. Web story — book your slot today.",
        "youtube_id": "b6W3XKb2cXM",
        "color": "#8a6d1f",
        "slides": [
            ("Meet the surgeon", "Dr Ashok Reddy — MBBS, DNB, M.Ch, Gold Medalist plastic surgeon."),
            ("Any concern welcome", "Hair, skin, burns, scars, hand injuries — ask anything."),
            ("Book a consultation", "Meet Dr Ashok Reddy to discuss your concern and options."),
            ("Open all 7 days", "Clinic hours: 10 AM – 8 PM, Monday to Sunday."),
        ],
    },
]
