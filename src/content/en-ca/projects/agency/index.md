---
title: "Agency"
date: 2026-01-15
description: "A complete design system and component library for a national NGO operating in four languages — built for accessibility from the ground up, maintainable by a small internal team, and independent of any proprietary design toolchain."
draft: false
params:
  status: "Complete"
  areas:
    - design
    - accessibility
"sat:work": "urn:uuid:04d0e02e-098c-43d4-84a9-11581dfbc950"
---

## Overview

A national non-governmental organisation with programmes across twelve provinces needed a coherent visual identity and digital presence that could be maintained by a team of three non-specialist staff, translated into four languages without design degradation, and used confidently by people with a wide range of disabilities and technical access levels.

The brief was explicit on two points: the system had to work without a subscription to any design tool, and it had to achieve WCAG 2.2 Level AA conformance at every touchpoint.

## Approach

We audited the existing digital presence and identified the thirty most frequently used interface patterns. From these we derived a minimal design token system: twelve colours, four type sizes, three spacing scales. Everything else is composed from these primitives.

The component library was built in plain HTML and CSS — no framework dependency, no build step for basic use. Each component ships with its accessibility annotations, keyboard interaction model, and a plain-language description suitable for non-technical staff. Translations are managed through a simple key-value file per language, requiring no design changes to switch languages.

We ran usability testing with twelve participants across three disability categories and three levels of digital literacy before finalising the system.

## Outcome

The NGO's digital presence is now consistent across all twelve provincial sites. The internal team has shipped four major content updates and one new programme page without external support. Automated accessibility testing passes at 100% on all core pages. The French, Cree, Inuktitut, and English versions are maintained in parallel by a single content coordinator.

## What we built

- Design token system (colour, type, spacing)
- 30-component HTML/CSS library with full accessibility annotations
- Translation infrastructure (key-value i18n, no framework required)
- WCAG 2.2 Level AA conformance audit and remediation
- Staff training materials and maintenance guide
- Ongoing quarterly accessibility review process
