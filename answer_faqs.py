#!/usr/bin/env python3
"""Answer-shaped Q&As appended to every procedure page (AI-visibility upgrade, 2026-11-01).

Each procedure gets three short questions with direct, quotable answers:
(1) cost in Karimnagar, (2) who performs it and where, (3) how to book a consultation.
Prices come ONLY from the clinic's approved published ranges. Breast augmentation
has NO published price — its cost answer says the figure is confirmed at
consultation. Procedures without an approved published range likewise state
that the exact cost is confirmed at consultation after examination.
Liposuction is deliberately absent: no Q&A is ever generated for it.
"""

DOCTOR_LINE = ("Dr Ashok Reddy — MBBS, DNB (Mumbai), M.Ch (Delhi), Gold Medalist; "
               "Plastic, Cosmetic, Hair Transplant, Hand & Microvascular Surgeon")
ADDRESS = "Opp. Reddy Gari Vantillu, Court Chowrasta, Karimnagar, Telangana 505001"
PHONE = "9182656866"

# slug -> (question name, sentence name, mid-sentence name, cost range or None, cost factor, verb)
_PROC = {
    "fue-hair-transplant": (
        "a FUE hair transplant", "FUE hair transplant", "FUE hair transplant",
        "₹40,000–₹1,50,000+ (about ₹35–₹60 per graft)",
        "the number of grafts needed to cover the area of hair loss", "performed"),
    "gynecomastia-surgery": (
        "gynecomastia surgery", "Gynecomastia surgery", "gynecomastia surgery",
        "₹60,000–₹1,20,000",
        "the grade of enlargement and the amount of gland and fat to be removed", "performed"),
    "rhinoplasty": (
        "rhinoplasty", "Rhinoplasty", "rhinoplasty",
        "₹80,000–₹1,80,000",
        "whether the surgery is cosmetic, functional, or a combination of both", "performed"),
    "tummy-tuck": (
        "a tummy tuck", "A tummy tuck (abdominoplasty)", "a tummy tuck (abdominoplasty)",
        "₹1,00,000–₹2,50,000",
        "the extent of skin removal and muscle repair required", "performed"),
    "botox-treatment": (
        "Botox treatment", "Botox treatment", "Botox treatment",
        "₹8,000–₹20,000 per area",
        "the areas treated and the amount required for each area", "carried out"),
    "prp-therapy": (
        "PRP therapy", "PRP therapy", "PRP therapy",
        "₹5,000–₹12,000 per session",
        "the area treated and the number of sessions in the recommended course", "carried out"),
    "lipoma-removal": (
        "lipoma removal", "Lipoma removal", "lipoma removal",
        "₹15,000–₹40,000",
        "the size, number and position of the lipomas", "performed"),
    "breast-augmentation": (
        "breast augmentation", "Breast augmentation", "breast augmentation",
        None,
        "the implant type, size and placement chosen, the anaesthesia, and what is included in the quote", "performed"),
    "breast-reconstruction": (
        "breast reconstruction", "Breast reconstruction", "breast reconstruction",
        None,
        "the reconstruction method advised and whether it is completed in one stage or several", "performed"),
    "breast-reduction": (
        "breast reduction surgery", "Breast reduction surgery", "breast reduction surgery",
        None,
        "the amount of tissue to be removed and the technique used", "performed"),
    "burn-reconstruction": (
        "burn reconstruction", "Burn reconstruction", "burn reconstruction",
        None,
        "the area involved, the type of reconstruction advised and the number of stages needed", "performed"),
    "carpal-tunnel-release": (
        "carpal tunnel release", "Carpal tunnel release", "carpal tunnel release",
        None,
        "whether one hand or both hands are treated and the technique used", "performed"),
    "chemical-peels": (
        "a chemical peel", "A chemical peel", "a chemical peel",
        None,
        "the type and depth of peel advised and the number of sessions in the course", "carried out"),
    "cleft-lip-palate-repair": (
        "cleft lip and palate repair", "Cleft lip and palate repair", "cleft lip and palate repair",
        None,
        "the type of cleft and the stage of repair planned", "performed"),
    "dermal-fillers": (
        "dermal filler treatment", "Dermal filler treatment", "dermal filler treatment",
        None,
        "the areas treated and the amount of filler required", "carried out"),
    "eyelid-surgery-blepharoplasty": (
        "eyelid surgery", "Eyelid surgery (blepharoplasty)", "eyelid surgery (blepharoplasty)",
        None,
        "whether the upper eyelids, the lower eyelids, or both are treated", "performed"),
    "facelift": (
        "a facelift", "A facelift (rhytidectomy)", "a facelift (rhytidectomy)",
        None,
        "the extent of correction planned and the areas included", "performed"),
    "fingertip-replantation": (
        "fingertip replantation", "Fingertip and digit replantation", "fingertip and digit replantation",
        None,
        "the level of the injury and the number of digits involved", "performed"),
    "hand-trauma-surgery": (
        "hand trauma surgery", "Hand trauma surgery", "hand trauma surgery",
        None,
        "the type of injury and the structures — bone, tendon, nerve or skin — involved", "performed"),
    "laser-treatments": (
        "laser treatment", "Laser treatment", "laser treatment",
        None,
        "the area treated, the concern being addressed and the number of sessions needed", "carried out"),
    "microsurgery-free-flap": (
        "microsurgery and free flap reconstruction", "Microsurgery and free flap reconstruction", "microsurgery and free flap reconstruction",
        None,
        "the size and site of the defect and the type of flap required", "performed"),
    "nerve-repair-microsurgery": (
        "nerve repair and microsurgery", "Nerve repair and microsurgery", "nerve repair and microsurgery",
        None,
        "the nerve involved, the gap to be bridged and whether a nerve graft is needed", "performed"),
    "scar-keloid-treatment": (
        "scar and keloid treatment", "Scar and keloid treatment", "scar and keloid treatment",
        None,
        "the size and type of the scar and whether injections, surgical revision, or a combination is advised", "carried out"),
    "skin-grafting": (
        "skin grafting", "Skin grafting", "skin grafting",
        None,
        "the size of the area to be covered and the type of graft required", "performed"),
    "tendon-repair": (
        "tendon repair", "Tendon repair", "tendon repair",
        None,
        "the tendon involved and the zone of the injury", "performed"),
}


def _build():
    out = {}
    for slug, (qname, sname, cname, price, factor, verb) in _PROC.items():
        cost_a = None
        if price:
            cost_a = (f"At AR Plastic Surgery, Karimnagar, {cname} typically "
                      f"costs {price}. The exact cost is confirmed at consultation after examination "
                      f"by Dr Ashok Reddy, because it depends on {factor}.")
        else:
            cost_a = (f"AR Plastic Surgery, Karimnagar does not publish a fixed price for "
                      f"{cname}, because the cost depends on {factor}. "
                      f"The exact cost is confirmed at consultation after examination by "
                      f"Dr Ashok Reddy, before any treatment is planned.")
        who_q = f"Who performs {qname} at AR Plastic Surgery, Karimnagar?"
        if verb == "carried out":
            who_q = f"Who carries out {qname} at AR Plastic Surgery, Karimnagar?"
        who_a = (f"{sname} at AR Plastic Surgery, Karimnagar is {verb} by {DOCTOR_LINE}. "
                 f"The clinic is at {ADDRESS}.")
        book_a = (f"You can book a consultation for {qname} at AR Plastic Surgery, Karimnagar "
                  f"online through the clinic's booking page or by calling {PHONE}. The clinic is "
                  f"open Monday to Sunday, 10:00 AM – 8:00 PM, and consultations are by appointment. "
                  f"At the consultation, Dr Ashok Reddy examines you and explains the options, "
                  f"the cost and the recovery before anything is decided.")
        out[slug] = [
            (f"How much does {qname} cost in Karimnagar?", cost_a),
            (who_q, who_a),
            (f"How do I book a consultation for {qname} in Karimnagar?", book_a),
        ]
    return out


ANSWER_FAQS = _build()
