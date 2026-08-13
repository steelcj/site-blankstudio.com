---
title: "Accessibility Procurement Checklist — What to Ask Before You Buy"
date: 2026-01-10
description: "A checklist for evaluating accessibility claims during software procurement — covering VPAT review, independent testing, contractual commitments, and what to do when a vendor cannot answer your questions."
draft: false
params:
  status: "Stable"
  version: "1.0.0"
"sat:work": "urn:uuid:bc2e6ae5-d921-4ff6-92c2-f72b1d1cee1a"
---

## Purpose

Most software vendors will tell you their product is accessible. This checklist helps you evaluate that claim before you sign a contract, not after you have committed to a platform your users cannot use.

## 1. Ask for the VPAT

A Voluntary Product Accessibility Template (VPAT) is a vendor's self-reported assessment of how their product conforms to accessibility standards. Ask for the VPAT for the specific version of the product you are evaluating, against WCAG 2.2 Level AA.

Red flags in a VPAT:

- It references WCAG 2.0 or 2.1 rather than 2.2
- Every criterion is listed as "Supports" with no explanation
- The evaluation was conducted by the vendor itself with no independent review
- It covers a version of the product that is more than one major release old

## 2. Test independently

Do not rely on the VPAT alone. Conduct or commission independent testing before purchase. At minimum:

- Run an automated scan using a current tool (Axe, WAVE, or equivalent)
- Navigate the core user flows using only a keyboard
- Test with a screen reader (NVDA on Windows, VoiceOver on macOS and iOS)
- Check colour contrast on all text and interactive elements

## 3. Ask contractual questions

Before signing, ask:

- What is the vendor's published accessibility conformance target?
- What is the process for reporting accessibility issues?
- What is the committed remediation timeframe for critical accessibility barriers?
- Are accessibility commitments included in the SLA?

A vendor who cannot answer these questions is a vendor who has not made accessibility a priority. That is useful information.

## 4. When a vendor cannot meet your requirements

If a vendor cannot demonstrate conformance and will not make contractual commitments, you have three options: require conformance as a condition of contract, require a remediation plan with milestones as a condition of contract, or choose a different vendor.

Accepting an inaccessible product because it meets other requirements is a decision that excludes some of your users. That decision should be made explicitly and documented, not absorbed quietly into a procurement process.
