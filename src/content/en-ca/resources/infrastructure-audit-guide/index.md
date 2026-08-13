---
title: "Infrastructure Audit Guide — Mapping What You Have Before Changing It"
date: 2026-02-01
description: "A practical guide to conducting a full infrastructure audit: what to document, how to surface hidden dependencies, and how to produce a map that is actually useful for decision-making."
draft: false
params:
  status: "Stable"
  version: "1.0.0"
"sat:work": "urn:uuid:10c5df56-d52f-433f-9e21-ca874ab08fa1"
---

## Purpose

Before any infrastructure work begins, you need an accurate picture of what exists. This guide describes how to conduct a full infrastructure audit — not a theoretical inventory, but a working document that reflects the system as it actually operates.

## 1. What to capture

A useful infrastructure audit captures six categories of information:

1. **Services** — every running service, its purpose, its operator, and its dependencies
2. **Data flows** — where data originates, where it is processed, where it is stored, and where it leaves your control
3. **Access and credentials** — who has access to what, under what authentication model, and where credentials are stored
4. **External dependencies** — every third-party service, API, or platform the system depends on
5. **Contracts and costs** — every vendor contract, its renewal date, its cost, and what it would take to exit it
6. **Documentation** — what documentation exists, how current it is, and where it lives

## 2. How to surface hidden dependencies

Hidden dependencies are the most dangerous part of any infrastructure. They are things the system depends on that nobody has explicitly decided to depend on — accumulated through years of pragmatic decisions that were never revisited.

Common sources of hidden dependencies include:

- DNS records pointing to services that no longer exist but whose removal would break something
- Email delivery relying on a personal account held by a former employee
- Authentication flows that pass through a third-party service inserted years ago as a temporary measure
- Backup jobs that write to a location that has quietly run out of space
- SSL certificates managed by a person who has left the organisation

The most reliable way to surface hidden dependencies is to map data flows from the outside in: start from every public-facing URL and follow each request through the system until it reaches persistent storage or exits to a third party.

## 3. Producing a useful map

An infrastructure map is only useful if it reflects the actual system and can be read by someone who did not build it. It should include:

- A diagram showing major components and the connections between them
- A table of services with owner, dependencies, and last-verified date
- A list of external dependencies with contract and cost information
- A list of open questions that the audit surfaced but could not resolve

The map should be version-controlled alongside the infrastructure it describes and updated whenever a significant change is made.
