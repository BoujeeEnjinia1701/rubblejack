---
doc_id: RBJ-REQ-001
title: RubbleJack requirements
project: RubbleJack
doc_type: Requirements
version: "0.3"
status: Draft
date: '2026-10-03'
author: Amish Chadha
license: CERN-OHL-S-2.0
revisions:
- version: "0.1"
  date: '2026-09-30'
  author: Amish Chadha
  change: Initial scaffold
- version: "0.2"
  date: '2026-10-03'
  author: Amish Chadha
  change: TRL 2; targets made measurable, R11 (strength margin) and R12 (cribbing) added from RBJ-DDR-001, cost requirement stated against the value-engineering target
- version: "0.3"
  date: '2026-10-03'
  author: Amish Chadha
  change: TRL 3 status of every requirement from RBJ-CAL-001 and the constructable design
---

# RubbleJack requirements

Every requirement is checked on paper at TRL 3 in RBJ-CAL-001; the status column gives the result. Measured verification is TRL 4 work. All requirements apply at the pump's 700 bar relief pressure, the highest pressure any part can see.

> **Safety:** These are design targets for a safety-critical kit. Meeting them on paper does not make the kit safe to use. Every tool must be proof-loaded and inspected before any use, and the kit is not certified to NFPA 1936, NFPA 1960 or EN 13204.

*Table 1. Requirements and their TRL 3 status.*

| ID | Requirement | Target | Verification (TRL 4 or later) | TRL 3 result (RBJ-CAL-001) | Status |
| --- | --- | --- | --- | --- | --- |
| R1 | Lifting capacity | Lift at least 10 t (22,000 lb) with the ram | CalRig proof load at 1.5 times rated load | 14.5 t at 700 bar; cylinder rated 15 t | Met on paper |
| R2 | Spreading force | At least 40 kN (9,000 lbf) between the jaw tips over the whole opening | Load cell between the tips at five openings | 48.6 kN closed to 64.1 kN open | Met on paper |
| R3 | Spreading opening | At least 250 mm (10 in) of tip opening | Measurement | 262 mm open; tips 32 mm thick closed | Met on paper |
| R4 | Cutting | Cut 16 mm (5/8 in) steel reinforcing bar, B500B or ASTM A615 grade 60 | Cut test on sample bar | About 105 kN needed, 142 kN available, ratio 1.36 | Met on paper |
| R5 | Pressure safety | Every pressurised part rated at or above the 700 bar relief; hoses at least 4 to 1 burst to working | Parts rating review and relief valve test | All parts specified at 700 bar; hoses 2,800 bar burst | Met by specification; ratings to confirm when parts are bought |
| R6 | Portable | No single packed load over 25 kg (55 lb) | Weigh each packed load | 15.9, 24.8, 22.0 and 23.7 kg | Met on paper; the spreader has 0.2 kg in hand |
| R7 | Fast setup | Pump connected and a tool working within 3 minutes of arrival | Timed drill | Two coupler connections, no tools; estimated 1 to 2 min | Met on paper |
| R8 | Tool change | Swap between spreader, cutter and ram in under 1 minute | Timed changeover | One coupler off and one on, about 20 s | Met by design |
| R9 | Commodity parts | Pump, hoses, couplers, gauge and cylinders all standard catalogue parts from at least two suppliers | BOM review | All in a class at least two makers offer | Met by specification |
| R10 | Value engineering | Estimated cost reported against the USD 3,500 value-engineering target | Costed BOM | USD 5,895 | Over the value-engineering target by USD 2,395 |
| R11 | Strength margin | Every made load-bearing part at least 1.5 on minimum yield at 700 bar | Strain-gauged proof load on CalRig | Lowest 1.60, the jaw arm tail at the link slot | Met on paper |
| R12 | Lifting on cribbing | The ram never lifts on bare rubble: base plate on hardwood cribbing; ground bearing under the sleepers 1 MPa or less | Drill with the co-design partner | 0.79 MPa on three 100 mm sleepers 600 mm long | Met by design and procedure |

## Requirements not met

None fails on paper. R10 is reported against the value-engineering target, not as a failure: the estimate is USD 2,395 over it, mainly because each tool has its own cylinder and the made parts use high-strength steel (RBJ-DEC-001, Value engineering). R6 is met with little margin on the spreader (0.2 kg).

## Assumptions

- Commodity 700 bar hand pumps and 15 t cylinders are available in target regions from at least two makers (checked against catalogues, not against regional stock).
- Local workshops can waterjet or laser cut, machine and have parts heat-treated to the stated hardness.
- Crews use hardwood cribbing, which is widely available, and receive basic training with the kit.
- Strength figures use minimum catalogue yield values and conservative hand calculations; proof loads at TRL 4 confirm them.
