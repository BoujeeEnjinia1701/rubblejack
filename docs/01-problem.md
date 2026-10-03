---
doc_id: RBJ-PRB-001
title: RubbleJack problem statement
project: RubbleJack
doc_type: Problem statement
version: "0.2"
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
  change: TRL 2 update; budget stated as a value-engineering target, co-design candidate recorded, open questions answered by RBJ-DDR-001 and RBJ-CAL-001, safety note added
---

# RubbleJack problem statement

Neighbours and local crews reach trapped people first, often within minutes, but without tools they can only dig by hand. Powered rescue tools exist, and most crews in the places that need them cannot afford them.

> **Safety:** This problem involves lifting and spreading heavy loads with high-pressure hydraulics inside unstable structures. Any answer to it is safety-critical; RubbleJack is published as an open engineering reference, not as certified rescue equipment.

## The problem

Most live rescues after earthquakes are made locally, often by relatives and neighbours ([Rom and Kelman, 2020](https://pmc.ncbi.nlm.nih.gov/articles/PMC7745699/)), and reporting from Turkey in 2023 and Myanmar in 2025 describes people digging by hand and waiting for machines ([Euronews, 2023](https://www.euronews.com/2023/02/07/we-could-hear-their-voices-digging-with-bare-hands-for-earthquake-survivors); [Al Jazeera, 2025](https://www.aljazeera.com/news/2025/3/29/lack-of-equipment-stalls-race-to-save-earthquake-survivors-in-myanmar)). Even in wealthy countries, small volunteer departments depend on grants to buy powered tools ([Texas A&M Forest Service, 2017](https://tfsweb.tamu.edu/?p=12405)).

Certified rescue tools are compliant with standards such as EN 13204 and NFPA 1960 ([Holmatro](https://www.holmatro.com/en/rescue/spreader-psp40)) and priced accordingly. At the other end, 10-tonne hydraulic body repair kits with a hand pump, hose and ram are sold as commodity tools ([Porto-Power](https://www.amazon.com/Porto-Power-B65115-Black-Hydraulic-Repair/dp/B000XMI1RO)). The gap is an open, documented kit that turns commodity hydraulics into spreading, lifting and cutting tools, with published proof-load data and clear limits.

## Users and context

| User | Need | Context |
| --- | --- | --- |
| Volunteer and rural fire crews | Spread, lift and cut at a fraction of the cost of branded tools | Vehicle incidents and structure collapses far from larger stations |
| Community emergency response teams | A kit they can carry to a collapse and use after basic training | First hours after an earthquake, before specialist teams arrive |
| Disaster NGOs and civil protection agencies | Kits they can preposition and maintain with local parts | Earthquake-prone cities and districts |
| Local hydraulic workshops | Drawings and specifications to build and repair jaws and fittings | Towns with truck, construction and body repair trades |

## Operating environment

- Collapsed masonry and reinforced concrete buildings, with dust, unstable debris and aftershocks.
- Night work, rain, heat or freezing cold; no power on site.
- Kit carried by hand over rubble, often by two to four people.
- Loads from lightweight masonry to heavy concrete slabs; reinforcing bar and timber to cut.
- Work in confined voids with little room to swing a pump handle.

## Constraints

- Value-engineering target of USD 3,500 for pump, hoses, ram, spreader and cutter: a hypothetical control target that keeps the design thinking along a value-engineering lens, not a spending limit.
- Hand pump only; no engine or battery power unit in the first version.
- Commodity hydraulic parts (standard hand pump, hoses, couplers and cylinders) wherever possible.
- Carried in loads of 25 kg (55 lb) or less each (target).
- Open design: hardware under CERN-OHL-S-2.0.
- Not certified to NFPA or EN rescue tool standards; published as an engineering reference.

## Out of scope

- Search and detection (see VoidScope for void search).
- Shoring systems and cribbing design beyond guidance on their use.
- Heavy machinery such as excavators and cranes.
- Powered or battery hydraulic units.
- Vehicle extrication certification.

## Prior work

| Prior work | What it does | Gap for these users | Source |
| --- | --- | --- | --- |
| Porto-Power 10-tonne hydraulic body repair kit | Commodity hand pump, hose, ram and attachments for body repair | No purpose-built rescue spreader or cutter jaws, and no rescue proof-load data | [link](https://www.amazon.com/Porto-Power-B65115-Black-Hydraulic-Repair/dp/B000XMI1RO) |
| Holmatro PSP40 spreader | Battery rescue spreader, 280 kN maximum spreading force, 19.5 kg, EN 13204 and NFPA 1960 compliant | Certified and costly; out of reach for many volunteer crews | [link](https://www.holmatro.com/en/rescue/spreader-psp40) |
| Holmatro HCT-3120 hand pump spreader and cutter | Hand-pumped combination tool, about 11,690 lbf spreading force, 23 lb | Proprietary and costly even second-hand | [link](https://www.fentonfire.com/equipment/holmatro-hct-3120-hand-pump-spreader-cutter-a1758/) |
| US7937838B2 hydraulic rescue tool with quick-change head | Rescue tool with detachable head on a hydraulic cylinder | Patent lapsed in 2019 for unpaid fees; free prior art for interchangeable heads | [link](https://patents.google.com/patent/US7937838?oq=hurst+jaws+of+life) |

## Co-design

A volunteer fire service or community emergency response programme in an earthquake-prone region, working with a local hydraulic workshop, so jaws and fittings are shaped by real training scenarios and can be made and serviced locally. The first candidate to approach is a volunteer search and rescue association in southern Turkey (AKUT is the first candidate), in the region hit in February 2023, with a local hydraulic workshop; this is a first candidate, not an agreement (RBJ-DDR-001, D12).

- [ ] Partner approached and willing to review the kit
- [ ] Training scenarios and typical loads confirmed with the partner
- [ ] Local workshop able to make the jaws, blades and plates identified

## Open questions

The scaffold's questions are answered on paper; none remain open.

- Can bolt-on jaws on standard cylinders reach useful forces? Yes on paper: a 15 t cylinder gives 49 to 64 kN at the spreader tips and shears 16 mm bar with a ratio of 1.36 (RBJ-CAL-001).
- Proof load and inspection: every made tool is proof-loaded on CalRig at 1.5 times the force at 700 bar and crack-checked before use; the routine between uses is set with the co-design partner at TRL 4 (RBJ-DDR-001, D9).
- Cribbing and shoring: cribbing is required and guidance is given, but cribbing is not designed or supplied (RBJ-DDR-001, D11).
- First drills: the first candidate host is recorded under Co-design.
