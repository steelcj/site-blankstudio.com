---
layout: layouts/home.njk
title: "Vishpala — technology, design, and infrastructure for greater agency"
description: "We are a studio of practitioners in technology, design, and infrastructure — working with individuals and organisations who want to operate with greater agency."
draft: false
"sat:work": "urn:uuid:4894cc28-2a5b-4775-babb-cd27c2993eec"

# The words of the designed home page. They sit here, in the content tree,
# rather than in src/_locales/<locale>.json: the bundle is not content, the
# ingress tool does not carry it, and the CMS cannot reach it. A French home
# page is a French file beside this one, not a second template.
#
# Section headings, card titles and card text are NOT here. Those come from the
# pages themselves — content/en-ca/areas/*/index.md and resources/*/index.md —
# so a card cannot fall out of step with the page it points at.
home:
  hero:
    eyebrow: "Technology &middot; Design &middot; Infrastructure"
    titleLines:
      - "Technology, design,"
      - "and infrastructure"
      - "for greater agency."
    sub: "We are a studio of practitioners working with individuals and organisations who want to operate with greater agency."
    body: "We take our name from the Rigvedic figure Vishpala — a warrior who loses a leg in battle and is given an iron prosthetic by the Ashvins so she can return to the field. We are interested in the idea of prosthetics: tools and infrastructure that extend capability, restore agency, and allow people to do what they came to do."
    ctaPrimary: "Start a conversation"
    ctaSecondary: "See what we practice"
    micro: "We work in English and French."

  # The facts panel. Every row is a statement the site already makes somewhere
  # else in the tree; nothing here is a claim this page invents.
  spec:
    version: "Facts"
    rows:
      - key: "Practice"
        value: "Technology, design, infrastructure"
      - key: "Languages"
        value: "English, French"
      - key: "Accessibility"
        value: "WCAG 2.2 AA, as a floor"
      - key: "Collaboration"
        value: "Throughout, not at handover"
    shippingKey: "How we size the work"
    shipping:
      - "Fewer things at once"
      - "Sized to whoever maintains it"
      - "No work we cannot do well"

  areas:
    eyebrow: "Areas"
    titleLine1: "The disciplines"
    titleEm: "we practice"
    titleLine2: ""
    link: "All areas"
    cardCta: "Read more"

  why:
    eyebrow: "What we believe"
    titleLine1: "Positions we"
    titleEm: "hold to"
    body: "These commitments decide what we take on, how we size it, and what we decline."
    cta: "About the studio"
    pillars:
      - title: "Sovereignty matters"
        body: "Organisations that depend entirely on infrastructure they do not control are fragile in ways that are not always visible until something breaks. We help organisations understand their dependencies and, where it serves them, reduce them."
      - title: "Accessibility is not optional"
        body: "We do not build things that exclude people with disabilities, and we do not help other organisations build them. WCAG 2.2 Level AA is our floor on every project."
      - title: "Complexity should be proportionate"
        body: "The right infrastructure for a community organisation is not the right infrastructure for a national one. We size solutions to the actual operational capacity of the people who will maintain them."
      - title: "Excellence takes time"
        body: "We work on fewer things at once than most studios. We do not take on work we cannot do well."

  resources:
    eyebrow: "Resources"
    titleLine1: "Guides and materials"
    titleEm: "from our practice"
    titleLine2: ""
    link: "All resources"
    cardCta: "Read more"

  cta:
    title: "Tell us what you are trying to <em>do</em>."
    sub: "We work in close collaboration with our clients throughout a project — not in isolation with periodic check-ins."
    btn1Label: "Start a conversation"
    btn2Label: "See our projects"
    micro: "We work in English and French."
---
