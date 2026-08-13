---
title: "Self-Hosting Decision Framework — When to Run It Yourself and When Not To"
date: 2025-12-01
description: "A practical framework for deciding when self-hosting a service improves your organisation's agency and when it introduces complexity without commensurate benefit."
draft: false
params:
  status: "Stable"
  version: "1.0.0"
"sat:work": "urn:uuid:909abd2e-7f33-40fb-b3c0-41ba8d62179e"
---

## Purpose

Self-hosting is not inherently better than using a managed service. The question is always whether self-hosting, for this service, for this organisation, at this moment, produces a better outcome than the available alternatives. This framework helps structure that decision.

## 1. The four questions

Before deciding to self-host any service, answer four questions:

**1. What do you gain?**
Enumerate the specific benefits: data sovereignty, reduced cost, elimination of a vendor dependency, alignment with a privacy commitment, the ability to customise behaviour the vendor will not support. Be concrete. "More control" is not sufficient — control over what, specifically?

**2. What does it cost to operate?**
Self-hosted services require someone to maintain them: applying security updates, monitoring for failures, managing backups, and responding when things break. Who will do this? What is their capacity? What happens when they are unavailable?

**3. What is the failure mode?**
If the self-hosted service fails, what is the impact? How quickly can it be restored? Is there a tested recovery procedure? The failure mode of a self-hosted service is typically your problem to solve in a way that a managed service's failure mode is not.

**4. What is the exit cost?**
If self-hosting turns out to be the wrong decision, how much effort does it take to migrate to a managed service? Low exit cost makes the decision reversible. High exit cost means you need to be more confident before you commit.

## 2. When self-hosting is clearly the right choice

Self-hosting is clearly the right choice when:

- The data processed by the service is sensitive and subject to jurisdiction requirements that managed services cannot satisfy
- The organisation has the operational capacity to maintain the service reliably
- The managed alternatives are prohibitively expensive relative to the value delivered
- The managed alternatives have unacceptable lock-in characteristics

## 3. When managed services are clearly the right choice

Managed services are clearly the right choice when:

- The operational cost of self-hosting exceeds the cost of the managed service
- The organisation does not have the capacity to respond to failures reliably
- The service is not part of the organisation's core operational competence
- The data processed is not sensitive and jurisdiction is not a concern

## 4. The honest answer most of the time

Most organisations should self-host fewer things than idealists advocate and more things than vendors prefer. The right answer depends entirely on operational capacity, data sensitivity, and the specific alternatives available. Anyone who gives you a blanket answer is not engaging with your actual situation.
