---
title: "Typographie — Polices système et Atkinson Hyperlegible"
date: 2026-06-15
description: "L'approche typographique de vishpala.com : system-ui par défaut, avec Atkinson Hyperlegible disponible comme alternative accessible choisie par l'utilisateur, auto-hébergée sans dépendances externes."
draft: false
params:
  status: "En vigueur"
  version: "1.1.0"
"sat:work": "urn:uuid:a93c44cd-7489-410b-8c4f-c7a76f3dba63"
---

## L'approche

Ce site utilise `system-ui, sans-serif` — la pile typographique native de l'appareil — comme typographie par défaut. Aucune police n'est chargée depuis des sources externes. Comme alternative sélectionnable par l'utilisateur, Atkinson Hyperlegible est disponible et auto-hébergée : tous les fichiers de polices sont servis directement depuis ce site, sans requêtes vers des tiers.

Le sélecteur de police (`Aa`) dans l'en-tête du site permet de choisir entre les deux options. Votre préférence est sauvegardée et appliquée à chaque visite ultérieure.

## System-ui — la valeur par défaut

Les polices système sont celles que les fournisseurs de systèmes d'exploitation ont le plus optimisées pour la lisibilité à l'écran, quelle que soit la taille, la densité d'affichage ou les paramètres d'accessibilité. San Francisco sur macOS et iOS, Segoe UI sur Windows et Roboto sur Android sont chacune le fruit d'un investissement important en matière d'hinting, d'espacement et de rendu.

Les polices système respectent les préférences typographiques propres à l'utilisateur. Si un utilisateur a configuré son système d'exploitation pour utiliser une taille de police plus grande ou une police spécifique pour des raisons de lisibilité, `system-ui` hérite de ces préférences. Pour les utilisateurs qui dépendent de ces préférences, cet héritage est important.

`system-ui` n'introduit aucune dépendance externe et n'impose aucune charge de maintenance d'infrastructure.

## Atkinson Hyperlegible — l'alternative accessible

Atkinson Hyperlegible a été conçue par le Braille Institute spécifiquement pour les lecteurs malvoyants. Chaque caractère est formé de manière unique pour éviter les erreurs de lecture — les formes des lettres souvent confondues (1/l/I, 0/O, rn/m) sont délibérément différenciées. Le Braille Institute l'a publiée sous la licence SIL Open Font Licence 1.1, autorisant l'utilisation et la redistribution libres.

La police est servie entièrement depuis l'infrastructure propre à ce site. Les huit fichiers de polices — normale, italique, grasse et grasse italique en latin et latin étendu — ne sont chargés que lorsque vous choisissez Atkinson, et uniquement depuis ce domaine. Aucune requête vers un tiers n'est effectuée.

Le Centre de recherche en design inclusif de l'Université OCAD, dont les travaux informent directement notre pratique de l'accessibilité, documente Atkinson Hyperlegible comme police recommandée pour l'accessibilité des malvoyants.

## Souveraineté et performance

Aucune des deux options typographiques ne charge des polices depuis Google Fonts ou toute autre source externe. Il n'y a pas de connexion à un réseau de distribution de polices tiers et aucune divulgation des adresses IP des visiteurs à des fournisseurs de polices.

Lorsque system-ui est actif, le texte s'affiche immédiatement en utilisant une police déjà présente sur l'appareil — sans requête réseau, sans flash de texte invisible, sans décalage de mise en page. Lorsqu'Atkinson Hyperlegible est actif, les fichiers de polices sont chargés depuis ce serveur lors de la première utilisation, puis mis en cache par le navigateur.

## Historique des versions

| Version | Date | Notes |
|---------|------|-------|
| 1.1.0 | 2026-06-28 | Mise à jour pour refléter l'ajout d'Atkinson Hyperlegible comme option sélectionnable par l'utilisateur |
| 1.0.0 | 2026-06-15 | Version initiale |
