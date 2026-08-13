---
title: "Sovereign Stack"
date: 2026-03-01
description: "A full infrastructure pivot away from proprietary cloud lock-in for a regional health network serving 80,000 patients — replacing vendor-managed services with reproducible, self-hosted, auditable systems under the organisation's own operational control."
draft: false
params:
  status: "Complete"
  areas:
    - infrastructure
    - privacy
"sat:work": "urn:uuid:f945766e-c68b-4adf-a847-adf054b17682"
---

## Overview

A regional health network operating across six sites had accumulated deep dependencies on three separate proprietary cloud platforms over eight years of growth. The infrastructure was functional but opaque: no single person understood the full system, vendor contracts were auto-renewing without review, and patient data was processed across jurisdictions in ways that were inconsistent with the organisation's own privacy commitments.

We were brought in to design and implement a path to operational independence — one that did not require a "big bang" cutover and did not introduce new categories of fragility in the process of removing old ones.

## Approach

We began with a full infrastructure audit: every service, every data flow, every external dependency mapped and documented. From that baseline we identified three categories of dependency — those that could be eliminated immediately, those requiring phased migration, and those where a sovereign alternative did not yet exist and would need to be built.

The migration ran over fourteen months across four phases. We prioritised patient data first, moving all clinical records to a self-hosted, jurisdiction-compliant system with automated backup verification and a tested restore procedure. We replaced the vendor-managed identity system with an open, auditable alternative. We decomissioned two SaaS platforms entirely by consolidating their functions into tools the organisation already operated.

## Outcome

The network now operates a fully documented, reproducible infrastructure. Every service can be rebuilt from version-controlled configuration. The on-call team can understand the full system in a single working day. Annual vendor contract costs were reduced by 68%. The organisation's privacy commitments and its actual infrastructure are now consistent with each other.

## What we built

- Full infrastructure audit and dependency map
- Phased migration plan with rollback procedures at each stage
- Self-hosted clinical records system with automated backup and restore testing
- Open identity and access management platform
- Runbooks and operational documentation for the internal team
- Training programme for three tiers of operational staff
