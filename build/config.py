# -*- coding: utf-8 -*-
"""
Controlled Climate Heating & Air — site content model.

EVERYTHING editable lives in this file. Change a value here, run `python3
build/build.py`, and every page, sitemap entry, schema block and internal link
updates itself. No page-by-page find-and-replace.

Items marked  ⚠️ CONFIRM  are best guesses and must be verified with Andrew
before launch.
"""

# ---------------------------------------------------------------------------
# 1. BUSINESS
# ---------------------------------------------------------------------------
BIZ = {
    "name": "Controlled Climate Heating & Air",
    "short_name": "Controlled Climate",
    "tagline": "Owner-operated. Straight answers, honest pricing, work that holds up.",
    "phone_display": "(801) 680-7406",
    "phone_e164": "+18016807406",
    "email": "andrewscogganhvac@gmail.com",
    "domain": "https://controlledclimatehvac.com",
    "street": "",                                        # ⚠️ CONFIRM (leave blank if service-area only)
    "city": "Taylorsville",
    "region": "UT",
    "region_full": "Utah",
    "postal": "84129",                                   # ⚠️ CONFIRM
    "country": "US",
    "lat": 40.6677,
    "lng": -111.9388,
    "owner": "Andrew Scoggan",
    # Drop Andrew's real logo into src/assets/img/ and put the filename here
    # (e.g. "logo.png"). Leave blank to use the built-in vector mark.
    "logo_file": "",
    "founded": "",                                       # ⚠️ CONFIRM year founded
    "license": "",                                       # ⚠️ CONFIRM Utah DOPL license #
    "facebook": "https://www.facebook.com/p/Controlled-Climate-Heating-Air-61576416968209/",
    "google_profile": "",                                # ⚠️ paste the GBP share link
    # Real, verified numbers from the Google Business Profile
    "rating": "5.0",
    "review_count": "40",
}

# Confirmed from the live site footer: Mon–Sat, 7am–9pm.
HOURS = [
    ("Monday", "07:00", "21:00"),
    ("Tuesday", "07:00", "21:00"),
    ("Wednesday", "07:00", "21:00"),
    ("Thursday", "07:00", "21:00"),
    ("Friday", "07:00", "21:00"),
    ("Saturday", "07:00", "21:00"),
    ("Sunday", None, None),
]

EMERGENCY_LINE = "After-hours calls answered for no-heat and no-cool emergencies."

# ---------------------------------------------------------------------------
# 2. TRACKING  — fill these in, everything else is already wired
# ---------------------------------------------------------------------------
TRACKING = {
    "ga4_id": "",            # e.g. "G-XXXXXXXXXX"
    "gtm_id": "",            # e.g. "GTM-XXXXXXX"  (use GTM *or* GA4, not both)
    "google_ads_id": "",     # e.g. "AW-XXXXXXXXX"
    "call_conversion_label": "",   # e.g. "AW-XXXXXXXXX/AbC-D_efGh"
    "form_conversion_label": "",
    "meta_pixel_id": "",
    "form_endpoint": "",     # Formspree / GHL inbound webhook / Netlify — see README
}

# ---------------------------------------------------------------------------
# 3. REVIEWS
#    ⚠️ These are PLACEHOLDERS. Paste real Google review text, then set
#    REVIEWS_ARE_PLACEHOLDER = False to remove the warning banner.
# ---------------------------------------------------------------------------
REVIEWS_ARE_PLACEHOLDER = True

REVIEWS = [
    {
        "quote": "Furnace quit on the coldest night of the year. Called first thing "
                 "in the morning and had heat back before lunch. Showed me the bad "
                 "part instead of just telling me about it.",
        "author": "Homeowner",
        "city": "Taylorsville, UT",
        "service": "Furnace repair",
    },
    {
        "quote": "Got three bids on a full system swap. Theirs wasn't the cheapest or "
                 "the most expensive, but it was the only one that explained why the "
                 "size they quoted was the right size.",
        "author": "Homeowner",
        "city": "West Jordan, UT",
        "service": "System replacement",
    },
    {
        "quote": "Older house, no ductwork upstairs. They put in mini-splits and the "
                 "bedrooms are finally usable in July. Clean install, no mess left "
                 "behind.",
        "author": "Homeowner",
        "city": "Salt Lake City, UT",
        "service": "Ductless mini-split",
    },
    {
        "quote": "AC went out during a heat wave. They were straight with me that it "
                 "was a repair, not a replacement, and it cost a fraction of what I "
                 "was braced for.",
        "author": "Homeowner",
        "city": "Murray, UT",
        "service": "AC repair",
    },
]

# ---------------------------------------------------------------------------
# 4. SERVICES
# ---------------------------------------------------------------------------
# temp: "hot" (ember accent) | "cold" (frost accent) | "both" (seam accent)
SERVICES = [
    {
        "slug": "furnace-repair",
        "name": "Furnace repair",
        "temp": "hot",
        "nav": "Furnace repair",
        "title": "Furnace Repair in {city}, UT | {biz}",
        "meta": "No heat? Furnace repair in {city} and across the Salt Lake Valley. "
                "Diagnostics, ignitors, blower motors, heat exchangers. Call {phone}.",
        "h1": "Furnace repair",
        "lede": "When the heat quits in January, you don't need a sales pitch. You need "
                "someone to find the fault, tell you what it costs, and fix it.",
        "photo": "furnace-service",
        "photo_alt": "Gas furnace and water heater in a Salt Lake Valley basement during a service call",
        "body": [
            ("What we actually check",
             "A no-heat call gets a full sequence-of-operation check, not a parts swap "
             "on a hunch. Thermostat call, ignition, gas valve, flame sensor, pressure "
             "switch, limit switches, blower, and flue draw. We test the heat exchanger "
             "for cracks on every furnace over ten years old, because that's a safety "
             "issue whether or not it's the reason you called."),
            ("Common faults on Utah furnaces",
             "Dirty flame sensors and failed hot-surface ignitors cause most short-cycling "
             "and no-light calls. Pressure switch faults usually trace back to a blocked "
             "intake or condensate line. Blower capacitors fail quietly and cost you "
             "efficiency for months before the motor gives out."),
            ("When repair stops making sense",
             "We'll tell you straight. If the repair is more than about a third of a new "
             "system and the furnace is past fifteen years, replacing it is usually the "
             "better spend. If it isn't, we'll say that too — most furnaces we look at "
             "get fixed, not replaced."),
        ],
        "faqs": [
            ("My furnace turns on then shuts off after a minute. What is that?",
             "That's short-cycling, and it's most often a dirty flame sensor, a blocked "
             "flue or intake, or an overheating limit trip from a clogged filter. Change "
             "the filter first — if it keeps doing it, it needs a technician."),
            ("Do you charge a diagnostic fee?",
             "Yes, and we tell you the number before we drive out. It covers the visit "
             "and the diagnosis, and you get a repair price before any work starts."),
            ("How fast can you get here for a no-heat call?",
             "Same day in most cases during heating season. Call the office and we'll "
             "tell you a real window, not a guess."),
        ],
    },
    {
        "slug": "furnace-installation",
        "name": "Furnace replacement",
        "temp": "hot",
        "nav": "Furnace replacement",
        "title": "Furnace Replacement & Installation in {city}, UT | {biz}",
        "meta": "High-efficiency furnace installation in {city} and the Salt Lake Valley. "
                "Right-sized equipment, permitted work, clean installs. Call {phone}.",
        "h1": "Furnace replacement & installation",
        "lede": "A furnace that's too big is worse than one that's too small. We size the "
                "system to the house, not to the label on the old one.",
        "photo": "furnace-install",
        "photo_alt": "New Goodman gas furnace installed in a Salt Lake Valley basement",
        "body": [
            ("Sizing comes before pricing",
             "Most replacement quotes are written off the nameplate of the unit being "
             "removed — which may have been oversized by a previous contractor. We look "
             "at square footage, insulation, window area, and what the existing ductwork "
             "can actually move before we quote a tonnage or BTU rating."),
            ("What the install includes",
             "New furnace, matched controls, sheet metal transitions built for the space, "
             "correct flue and combustion air, condensate handling for high-efficiency "
             "units, gas line and electrical verification, and permit and inspection "
             "where the city requires it. Startup includes gas pressure and temperature "
             "rise set to spec, in writing."),
            ("Efficiency worth paying for",
             "In this climate, a 95%+ AFUE furnace pays for the upgrade over an 80% model "
             "on a full winter of runtime. Two-stage and variable-speed blowers matter "
             "more in older homes with uneven upstairs rooms than the AFUE number does."),
        ],
        "faqs": [
            ("How long does a furnace replacement take?",
             "Most single-furnace swaps are one day. Add time if the flue, gas line, or "
             "return duct has to be reworked to meet current code."),
            ("Do you pull permits?",
             "Yes, where the jurisdiction requires one. An unpermitted install can "
             "complicate a home sale and can void manufacturer warranty coverage."),
            ("Should I replace the AC at the same time?",
             "If the AC is the same age and the coil is matched to the furnace, doing "
             "both at once saves a second labor charge and gets you a properly matched "
             "system. If the AC has years left, we'll say so."),
        ],
    },
    {
        "slug": "ac-repair",
        "name": "AC repair",
        "temp": "cold",
        "nav": "AC repair",
        "title": "AC Repair in {city}, UT | {biz}",
        "meta": "Air conditioning repair in {city} and across the Salt Lake Valley. "
                "Refrigerant, capacitors, compressors, frozen coils. Call {phone}.",
        "h1": "Air conditioning repair",
        "lede": "Blowing warm air is a symptom, not a diagnosis. There are about six "
                "things that cause it and they cost wildly different amounts to fix.",
        "photo": "ac-install",
        "photo_alt": "Goodman air conditioning condenser on a pad outside a Utah home",
        "body": [
            ("The diagnosis actually matters",
             "A failed run capacitor is an inexpensive part. A seized compressor is a "
             "system decision. A frozen evaporator coil is usually airflow, not "
             "refrigerant. We measure superheat and subcool, check static pressure, and "
             "read the actual amp draw before quoting anything."),
            ("On refrigerant",
             "If your system is low on refrigerant, it has a leak — refrigerant isn't "
             "consumed. We'll find the leak and price the repair instead of selling you "
             "a top-off every summer. Older R-22 systems are a separate conversation; "
             "the refrigerant cost alone often makes replacement the smarter move."),
            ("Utah summers are hard on condensers",
             "Cottonwood, dust, and lawn clippings pack condenser coils and push head "
             "pressure up until the compressor overheats. A coil wash and a clear three "
             "feet around the unit prevents a large share of the failures we see in July."),
        ],
        "faqs": [
            ("My AC is running but the house isn't cooling. What's wrong?",
             "Most often a dirty filter or coil restricting airflow, a failed capacitor "
             "on the outdoor unit, or a refrigerant leak. Check the filter and make sure "
             "the outdoor fan is spinning, then call."),
            ("There's ice on the copper line. Should I turn it off?",
             "Yes. Switch the system to fan-only to melt the ice and call us. Running a "
             "frozen system can send liquid refrigerant back to the compressor and turn "
             "a small repair into a large one."),
            ("Is it worth repairing an older AC?",
             "Under ten years, usually yes. Over fifteen with an R-22 charge, the repair "
             "cost plus refrigerant often approaches a down payment on a new system."),
        ],
    },
    {
        "slug": "ac-installation",
        "name": "AC installation",
        "temp": "cold",
        "nav": "AC installation",
        "title": "AC Installation & Replacement in {city}, UT | {biz}",
        "meta": "Air conditioner replacement in {city} and the Salt Lake Valley. Matched "
                "systems, correct line sets, verified charge. Call {phone}.",
        "h1": "AC replacement & installation",
        "lede": "Two identical air conditioners can perform very differently. The "
                "difference is almost always the install.",
        "photo": "ac-install",
        "photo_alt": "New Goodman condenser set on a level pad with copper line set",
        "body": [
            ("Matched systems, not mixed parts",
             "The condenser, evaporator coil, and blower have to be rated as a system to "
             "hit the SEER2 number on the sticker. Pairing a new condenser to an old coil "
             "is cheaper on the invoice and worse in every other way — capacity, "
             "efficiency, and warranty."),
            ("The parts nobody sees",
             "Level pad, correct line-set size, a proper vacuum before charging, weighed-in "
             "refrigerant verified against superheat and subcool, sealed and insulated "
             "suction line, and a disconnect that meets code. That's where an install "
             "either lasts fifteen years or starts leaking in three."),
            ("Dry climate, real load",
             "Salt Lake summers are hot but dry, which means sizing for sensible load "
             "rather than blindly following square-foot rules of thumb. Oversized units "
             "cool fast, shut off, and leave the house uneven."),
        ],
        "faqs": [
            ("How long does an AC replacement take?",
             "A straight condenser-and-coil replacement is typically a single day."),
            ("Do I need a new furnace to get a new AC?",
             "Not always — but the indoor coil and blower have to work with the new "
             "condenser. If your furnace is near end of life, doing both is usually the "
             "better long-run cost."),
            ("What SEER2 rating should I get?",
             "For most Salt Lake Valley homes the sweet spot is a mid-tier two-stage "
             "system. The jump to the highest-efficiency tier rarely pays back here "
             "unless you run cooling heavily."),
        ],
    },
    {
        "slug": "ductless-mini-splits",
        "name": "Ductless mini-splits",
        "temp": "both",
        "nav": "Mini-splits",
        "title": "Ductless Mini-Split Installation in {city}, UT | {biz}",
        "meta": "Ductless mini-split heat pump installation in {city} and the Salt Lake "
                "Valley. Additions, basements, garages, and older homes. Call {phone}.",
        "h1": "Ductless mini-splits",
        "lede": "For the room that's always ten degrees off — the finished basement, the "
                "addition, the upstairs bedroom the ductwork never reached.",
        "photo": "mini-split-indoor",
        "photo_alt": "LG ductless mini-split head mounted on an interior wall",
        "body": [
            ("Where they make sense",
             "Older Salt Lake City homes with no second-floor ductwork. Converted "
             "basements and garages. Additions where extending the trunk line would mean "
             "opening ceilings. Any room where you'd rather control temperature "
             "independently than fight the rest of the house for it."),
            ("Heating too, not just cooling",
             "Modern inverter heat pumps hold usable capacity well below freezing, which "
             "makes a mini-split a genuine year-round solution here rather than a summer "
             "appliance. In a space with no ducted heat, that's often the whole answer."),
            ("Install quality is visible",
             "Line-set routing, a level wall bracket, sealed penetrations, and a "
             "condensate path that actually drains. A mini-split is mounted in the room "
             "you live in, so a sloppy install is something you look at every day."),
        ],
        "faqs": [
            ("How many indoor heads can one outdoor unit run?",
             "Typically one to five, depending on the system. Multi-zone setups let each "
             "room hold its own temperature."),
            ("Are mini-splits loud?",
             "The indoor head runs quieter than a refrigerator on low. The outdoor unit "
             "is quieter than a conventional condenser."),
            ("Can a mini-split heat a space through a Utah winter?",
             "A properly sized cold-climate inverter unit, yes. We'll confirm the model's "
             "rated capacity at design temperature rather than assuming."),
        ],
    },
    {
        "slug": "ductwork-new-construction",
        "name": "Ductwork & new construction",
        "temp": "both",
        "nav": "Ductwork",
        "title": "Ductwork & New Construction HVAC in {city}, UT | {biz}",
        "meta": "Custom sheet metal, duct design, and new construction HVAC rough-in in "
                "{city} and the Salt Lake Valley. Call {phone}.",
        "h1": "Ductwork & new construction",
        "lede": "Equipment gets the credit. Ductwork decides whether the house is "
                "comfortable.",
        "photo": "ductwork-trunk",
        "photo_alt": "Custom sheet metal trunk line and takeoffs during a new construction rough-in",
        "body": [
            ("New construction rough-in",
             "We work from the plans: load calculation, trunk and branch layout, register "
             "placement, and return sizing before a single piece of metal gets hung. "
             "Coordinated with framing and plumbing so nothing gets rerouted twice."),
            ("Retrofit and repair",
             "Undersized returns, crushed flex, disconnected boots in the crawlspace, and "
             "leaky joints in an unconditioned attic all cost real capacity. Sealing and "
             "resizing existing duct is frequently a better spend than a bigger furnace."),
            ("Custom sheet metal",
             "Transitions, plenums, and offsets fabricated for the space instead of forced "
             "in with tape and hope. If a duct has to make an awkward turn around a beam, "
             "it gets built to make that turn."),
        ],
        "faqs": [
            ("Some rooms never get warm. Is that the furnace?",
             "Usually not. It's more often duct sizing, a return-air shortage, or leakage "
             "in unconditioned space. That's a measurable problem with a fixable cause."),
            ("Do you work with builders and general contractors?",
             "Yes. New construction rough-in and trim-out are a regular part of what we do."),
            ("Can you seal existing ductwork?",
             "Yes — mastic and mechanical sealing at joints and boots, prioritizing runs "
             "in attics, crawlspaces, and garages where losses are largest."),
        ],
    },
    {
        "slug": "commercial-refrigeration",
        "name": "Commercial refrigeration",
        "temp": "cold",
        "nav": "Refrigeration",
        "title": "Commercial Refrigeration Repair in {city}, UT | {biz}",
        "meta": "Walk-in cooler and freezer repair, reach-ins, and commercial refrigeration "
                "service across the Salt Lake Valley. Call {phone}.",
        "h1": "Commercial refrigeration",
        "lede": "A walk-in that drifts five degrees is an inventory problem before it's a "
                "repair problem. We treat it that way.",
        "photo": "mini-split-outdoor",
        "photo_alt": "Outdoor condensing unit mounted on brackets against a building wall",
        "body": [
            ("Walk-ins, reach-ins, and prep tables",
             "Coolers and freezers for restaurants, convenience stores, and food service. "
             "Compressors, condensers, evaporators, defrost timers, door gaskets, and "
             "controls. If it holds temperature and you're losing product when it doesn't, "
             "we work on it."),
            ("Why refrigeration isn't just cold air conditioning",
             "Refrigeration runs far lower suction temperatures and lives or dies on defrost "
             "strategy and superheat control. Plenty of HVAC contractors won't touch it. "
             "We do both, which means one call instead of two vendors."),
            ("Response time is the whole product",
             "Nobody schedules a walk-in failure. Call and we'll tell you a real window — "
             "and if it's a stopgap that keeps product cold until a part arrives, we'll do "
             "that first and fix it properly after."),
        ],
        "faqs": [
            ("My walk-in is running but the temperature is climbing. What's happening?",
             "Most often an iced evaporator from a failed defrost cycle, a low charge from "
             "a leak, or a condenser packed with grease and dust. All three are findable in "
             "one visit."),
            ("Do you service restaurant equipment after hours?",
             "Call and ask. Refrigeration failures don't wait for business hours and we "
             "know what's sitting in that box."),
            ("Can you do preventive maintenance on commercial refrigeration?",
             "Yes — coil cleaning, gasket inspection, defrost verification, and charge "
             "checks on a schedule. It costs a fraction of an emergency call plus lost "
             "product."),
        ],
    },
    {
        "slug": "gas-lines",
        "name": "Gas lines",
        "temp": "hot",
        "nav": "Gas lines",
        "title": "Gas Line Installation & Repair in {city}, UT | {biz}",
        "meta": "Gas line installation, extensions, and leak repair in {city} and the Salt "
                "Lake Valley. Piped, pressure-tested, and permitted. Call {phone}.",
        "h1": "Gas lines",
        "lede": "New runs for a range, a firepit, a garage heater, or a generator — piped, "
                "pressure-tested, and inspected.",
        "photo": "furnace-service",
        "photo_alt": "Gas piping and shutoff valve at a residential appliance connection",
        "body": [
            ("New runs and extensions",
             "Adding a gas range, a dryer, an outdoor grill or firepit, a garage heater, or "
             "a standby generator. We size the pipe for the total connected load, not just "
             "the appliance you're adding — undersizing a run starves everything downstream."),
            ("Leak detection and repair",
             "If you smell gas, leave and call the utility first. Once it's safe, we'll "
             "find the leak, repair it, and pressure-test the system before it's put back "
             "in service."),
            ("Permitted and tested",
             "Gas work gets pulled, pressure-tested, and inspected where the jurisdiction "
             "requires it. This is one area where the shortcut is never worth it."),
        ],
        "faqs": [
            ("Can you run a gas line to my outdoor firepit or grill?",
             "Yes — that's one of the most common requests we get. We'll size the run and "
             "handle the permit."),
            ("How do I know if my existing gas line can handle another appliance?",
             "It's a load calculation against the pipe size and length. We'll check before "
             "adding anything rather than finding out when the furnace starves."),
            ("I smell gas. What should I do?",
             "Leave the building and call your gas utility from outside. Once they've made "
             "it safe, call us for the repair."),
        ],
    },
    {
        "slug": "indoor-air-quality",
        "name": "Indoor air quality",
        "temp": "both",
        "nav": "Air quality",
        "title": "Indoor Air Quality & Filtration in {city}, UT | {biz}",
        "meta": "Air filtration, purification, and humidity control for Salt Lake Valley "
                "homes — built for inversion season. Call {phone}.",
        "h1": "Indoor air quality",
        "lede": "Salt Lake spends part of every winter under an inversion. Your filter is "
                "the last thing between that and your living room.",
        "body": [
            ("Filtration that actually fits",
             "A one-inch filter jammed into a return grille restricts airflow and catches "
             "very little. A properly sized media cabinet catches far more and costs the "
             "system less static pressure. In a valley that traps PM2.5 for weeks at a "
             "time, that difference is worth having."),
            ("Humidity, both directions",
             "Utah air is dry enough that winter humidification is a comfort and a "
             "woodwork issue, not a luxury. Whole-home humidifiers tied to the duct system "
             "beat running units room by room."),
            ("Purification, honestly",
             "Some air purification products do real work and some are marketing. We'll "
             "tell you which is which for your house rather than attaching whatever has "
             "the best spiff."),
        ],
        "photo": "ductwork-rough-in",
        "photo_alt": "Duct system and return air pathways in a home under construction",
        "faqs": [
            ("Will a better filter help during inversion season?",
             "A properly sized media filter or higher-MERV cabinet makes a real difference "
             "on fine particulate. Cramming a high-MERV one-inch filter into an undersized "
             "slot does not — it just chokes airflow."),
            ("Do I need a whole-home humidifier in Utah?",
             "Most homes here benefit through the winter. It helps with static, dry sinuses, "
             "and hardwood and trim that shrinks every January."),
            ("What MERV rating should I use?",
             "It depends on what your blower can push. We'll check static pressure before "
             "recommending a rating rather than guessing."),
        ],
    },
    {
        "slug": "maintenance",
        "name": "Tune-ups & maintenance",
        "temp": "both",
        "nav": "Maintenance",
        "title": "Furnace & AC Tune-Ups in {city}, UT | {biz}",
        "meta": "Seasonal furnace and air conditioner maintenance in {city} and the Salt "
                "Lake Valley. Catch failures before the weather does. Call {phone}.",
        "h1": "Tune-ups & maintenance",
        "lede": "Almost every emergency call we run was visible three months earlier as a "
                "reading slightly out of spec.",
        "photo": "furnace-service",
        "photo_alt": "Technician's view of a furnace and water heater during a maintenance visit",
        "body": [
            ("Heating tune-up",
             "Combustion analysis, gas pressure, temperature rise, flame sensor cleaning, "
             "ignitor resistance, blower amp draw, capacitor test, safety and limit "
             "verification, and a heat exchanger inspection. You get the readings, not "
             "just a checkmark."),
            ("Cooling tune-up",
             "Condenser coil wash, refrigerant charge verification by superheat and "
             "subcool, capacitor and contactor test, condensate drain clearing, and "
             "static pressure check across the air handler."),
            ("Why it's worth the visit",
             "Capacitors, contactors, and ignitors give measurable warning before they "
             "fail. Catching them in September costs a part. Catching them in January "
             "costs an emergency call in the cold."),
        ],
        "faqs": [
            ("How often should I service my system?",
             "Heating in the fall, cooling in the spring. If you only do one, do the "
             "furnace — that's the one with combustion safety involved."),
            ("How often do I change the filter?",
             "One-inch filters every 60–90 days, sooner with pets or during inversion "
             "season. A restricted filter is the single most common cause of the calls "
             "we run."),
            ("Do you offer a maintenance plan?",
             "Ask when you call — we'll walk you through what's covered and what it costs."),
        ],
    },
]

# ---------------------------------------------------------------------------
# 5. SERVICE AREA
# ---------------------------------------------------------------------------
LOCATIONS = [
    {
        "slug": "taylorsville",
        "name": "Taylorsville",
        "primary": True,
        "lede": "We're based here. Most Taylorsville calls get same-day service in "
                "heating and cooling season.",
        "context": "Taylorsville's housing runs heavily to 1970s and 1980s ranch and "
                   "split-level homes, plus newer infill west toward Bangerter. That "
                   "generation of house is now on its second or third furnace, and the "
                   "original ductwork was frequently sized for equipment that no longer "
                   "exists. We see a lot of oversized replacements installed by whoever "
                   "came before, and a lot of undersized returns.",
        "landmarks": "Redwood Road, Bangerter Highway, 4700 South, Taylorsville-Bennion "
                     "Heritage Park, Salt Lake Community College",
    },
    {
        "slug": "salt-lake-city",
        "name": "Salt Lake City",
        "lede": "From the Avenues to Sugar House and out to Glendale — including the "
                "older houses that make HVAC interesting.",
        "context": "Salt Lake City has some of the oldest housing stock in the valley. "
                   "Avenues bungalows and Sugar House brick homes often started with "
                   "gravity furnaces and got ducted later, which means undersized returns, "
                   "second floors that never quite get conditioned, and basements that "
                   "swallow all the airflow. Ductless mini-splits solve upstairs comfort "
                   "in these homes more cleanly than rebuilding the duct system.",
        "landmarks": "The Avenues, Sugar House, Liberty Wells, Glendale, Rose Park, "
                     "Downtown, 9th and 9th",
    },
    {
        "slug": "west-valley-city",
        "name": "West Valley City",
        "lede": "Utah's second-largest city, and a large share of it was built in the "
                "same two decades.",
        "context": "Much of West Valley went up between the 1970s and the 1990s, so a "
                   "big share of the systems here are hitting replacement age at "
                   "roughly the same time. The upside is predictability — we know these "
                   "floor plans and where the return-air shortcuts usually are. The "
                   "downside is that a lot of homeowners are getting their first "
                   "replacement quote and have nothing to compare it to.",
        "landmarks": "3500 South, 5600 West, Valley Fair Mall, Maverik Center, Hunter, "
                     "Granger",
    },
    {
        "slug": "west-jordan",
        "name": "West Jordan",
        "lede": "Newer builds, larger footprints, and two-story homes that fight to stay "
                "even.",
        "context": "West Jordan's growth means a mix of 1990s-and-newer two-story homes "
                   "with plenty of square footage on a single system. The recurring "
                   "complaint is upstairs bedrooms running hot in summer while the main "
                   "floor is fine — usually a zoning, return, or balance problem rather "
                   "than an equipment problem.",
        "landmarks": "Jordan Landing, 7000 South, Bangerter Highway, Redwood Road, "
                     "Gardner Village",
    },
    {
        "slug": "murray",
        "name": "Murray",
        "lede": "Older central neighborhoods and newer development, sometimes on the "
                "same block.",
        "context": "Murray runs from pre-war homes near the city center out to newer "
                   "construction, which means we're diagnosing 1950s duct layouts and "
                   "commissioning brand-new systems in the same week. Tight mechanical "
                   "rooms are common in the older core — sheet metal that has to be "
                   "fabricated to fit rather than pulled off a shelf.",
        "landmarks": "State Street, Murray Park, Fashion Place, Vine Street, Intermountain "
                     "Medical Center",
    },
    {
        "slug": "kearns",
        "name": "Kearns",
        "lede": "Small homes, tight mechanical spaces, and systems that have been worked "
                "on a lot.",
        "context": "Kearns grew out of wartime-era housing, and a lot of those homes are "
                   "compact with equipment squeezed into a closet or a corner of the "
                   "basement. Clearance and combustion air are real considerations here, "
                   "not paperwork — and past repairs have often left a layer of "
                   "improvisation to work around.",
        "landmarks": "5400 South, 4015 West, Utah Olympic Oval, Kearns Junior High area",
    },
    {
        "slug": "millcreek",
        "name": "Millcreek",
        "lede": "Mid-century homes near the canyon, with the temperature swings that "
                "come with elevation.",
        "context": "Millcreek's mid-century housing sits close enough to the canyon that "
                   "evening temperature drops are noticeably sharper than down in the "
                   "valley. Systems here cycle more, and homes on the bench frequently "
                   "have additions where somebody extended the duct run further than it "
                   "wanted to go.",
        "landmarks": "3300 South, Millcreek Canyon, Wasatch Boulevard, Canyon Rim, "
                     "East Millcreek",
    },
    {
        "slug": "holladay",
        "name": "Holladay",
        "lede": "Larger, older homes where system design matters more than equipment "
                "brand.",
        "context": "Holladay has bigger footprints on mature lots, often with additions "
                   "layered on over decades. Multiple zones, dual systems, and "
                   "long duct runs are common, and comfort problems are almost always a "
                   "design question rather than a broken part. Worth doing the load "
                   "calculation properly before anyone quotes equipment.",
        "landmarks": "Holladay Village, 6200 South, Highland Drive, Cottonwood Lane",
    },
    {
        "slug": "sandy",
        "name": "Sandy",
        "lede": "Bench homes, elevation, and afternoon sun loads on the east side.",
        "context": "Sandy's east-bench homes take real solar gain in the afternoon and "
                   "cool off fast at night, which is hard on a single-stage system that "
                   "only knows full blast or off. Two-stage and variable-speed equipment "
                   "earns its price difference here more than almost anywhere else in "
                   "the valley.",
        "landmarks": "Sandy Village, 9400 South, 1300 East, Little Cottonwood, "
                     "South Towne",
    },
    {
        "slug": "south-jordan",
        "name": "South Jordan",
        "lede": "Some of the newest housing stock in the valley — including Daybreak, where "
                "the systems are modern but the comfort complaints still show up.",
        "context": "South Jordan skews new, and Daybreak in particular is built tighter than "
                   "the rest of the valley. Tight envelopes change the math: smaller heating "
                   "loads, more sensitivity to duct balance, and humidity that behaves "
                   "differently than it does in a 1970s house. When a nearly new system "
                   "isn't keeping a room even, it's almost never the equipment.",
        "landmarks": "Daybreak, District at South Jordan, 10600 South, Bangerter Highway, "
                     "Oquirrh Lake",
    },
    {
        "slug": "draper",
        "name": "Draper",
        "lede": "East-bench elevation, big temperature swings, and homes that ask a lot of "
                "a single-stage system.",
        "context": "Draper climbs fast east of I-15, and elevation plus afternoon sun means "
                   "wide daily swings — hot at 4pm, cold by 10pm. Suncrest sits high enough "
                   "that design temperatures differ meaningfully from the valley floor. "
                   "Two-stage and variable-speed equipment earns its cost here, and heat "
                   "pump sizing needs to be checked against the actual elevation, not a "
                   "county-wide assumption.",
        "landmarks": "Suncrest, Corner Canyon, 12300 South, Traverse Ridge, Draper Park",
    },
    {
        "slug": "riverton",
        "name": "Riverton",
        "lede": "Larger lots, a wide mix of build years, and plenty of detached shops and "
                "garages that want conditioning.",
        "context": "Riverton runs from older properties on bigger parcels to newer "
                   "subdivisions, so there's no single typical system here. The recurring "
                   "job is a detached garage, shop, or finished basement that the original "
                   "ductwork was never meant to reach — usually a mini-split or a dedicated "
                   "gas line and unit heater rather than an extension of the main system.",
        "landmarks": "Riverton Main Street, 12600 South, Redwood Road, Western Springs, "
                     "Riverton City Park",
    },
]

# Additional cities listed but without dedicated pages (yet)
ALSO_SERVED = [
    "Herriman", "South Salt Lake", "Midvale", "Cottonwood Heights",
    "Magna", "Bluffdale", "West Bountiful", "Park City",
]

# ---------------------------------------------------------------------------
# 6. GALLERY  (real job photos)
# ---------------------------------------------------------------------------
GALLERY = [
    ("ductwork-trunk", "Custom sheet metal trunk line and takeoffs, new construction rough-in",
     "Ductwork", "Salt Lake Valley"),
    ("furnace-install", "New Goodman gas furnace installed with custom sheet metal transition",
     "Furnace replacement", "Salt Lake County"),
    ("ac-install", "Goodman condenser set level on a new pad with insulated line set",
     "AC installation", "Salt Lake County"),
    ("mini-split-indoor", "LG ductless mini-split head mounted in a finished room",
     "Mini-split", "Salt Lake City"),
    ("ductwork-rough-in", "Overhead duct layout coordinated with framing before drywall",
     "New construction", "Salt Lake Valley"),
    ("mini-split-outdoor", "LG mini-split condenser wall-mounted on brackets",
     "Mini-split", "Salt Lake City"),
]

# ---------------------------------------------------------------------------
# 7. HOMEPAGE FAQs
# ---------------------------------------------------------------------------
HOME_FAQS = [
    ("Who actually shows up?",
     "Andrew. Controlled Climate is owner-operated — the person who quotes the job is the "
     "person who runs it. No dispatcher, no rotating subcontractor."),
    ("What areas do you serve?",
     "We're based in Taylorsville and cover Salt Lake City and the surrounding valley — "
     "West Valley City, West Jordan, South Jordan, Murray, Kearns, Sandy, Draper, "
     "Riverton, Millcreek, Holladay, and the cities around them."),
    ("Do you do commercial work?",
     "Yes. Rooftop units, commercial refrigeration, walk-in coolers and freezers, and "
     "new-construction rough-in alongside the residential side."),
    ("Do you charge for estimates?",
     "Estimates are free, always. If your system is down and needs to be diagnosed first, "
     "ask about the service call when you phone in — you'll get that number up front, "
     "before anyone drives out."),
    ("How fast can someone get here?",
     "Same-day service in most cases for no-heat and no-cool calls. Call and we'll give "
     "you a real arrival window."),
    ("What brands do you install and service?",
     "We service every major brand. On replacements we install equipment we can stand "
     "behind and get parts for quickly — that matters more than the badge on the front."),
    ("Do you pull permits?",
     "Yes, where the jurisdiction requires one. Unpermitted work can cause problems at "
     "resale and can affect manufacturer warranty coverage."),
]
