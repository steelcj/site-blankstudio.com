---
title: "Introducción a los Design Tokens — Lo Mínimo que Necesita Saber"
date: 2025-11-15
description: "Una introducción en lenguaje sencillo a los design tokens: qué son, por qué importan para el diseño multilingüe y accesible, y cómo implementar un sistema mínimo de tokens sin suscripción a una herramienta de diseño."
draft: false
params:
  status: "Estable"
  version: "1.0.0"
"sat:work": "urn:uuid:1af4d01e-f7af-4f7f-8376-ed1a038865f5"
---

## ¿Qué es un design token?

Un design token es un valor con nombre que codifica una decisión de diseño. En lugar de escribir `color: #0033cc` en quinientos lugares, define un token — `--colour-primary: #0033cc` — y referencia el token en todas partes. Cuando la decisión cambia, la cambia en un solo lugar.

Los design tokens son la capa de infraestructura de un sistema de diseño. No son una característica de una herramienta de diseño ni un requisito de framework. Son propiedades personalizadas CSS, y funcionan en cualquier navegador.

## Por qué los tokens importan para el diseño accesible y multilingüe

**Accesibilidad** — los tokens hacen tractable la verificación del contraste de color en todo un sistema. Si el color de texto y el color de fondo son ambos tokens, puede verificar cada combinación en un solo lugar en lugar de buscar en toda la base de código valores codificados directamente.

**Diseño multilingüe** — los tokens facilitan ajustar las decisiones tipográficas para idiomas específicos. Una interfaz en francés puede necesitar una altura de línea ligeramente más generosa que una en inglés. Un sistema basado en tokens permite anular un único valor por idioma en lugar de reescribir las reglas de maquetación.

**Mantenibilidad** — un equipo pequeño puede mantener un sistema basado en tokens porque los cambios están localizados. Reemplazar el color principal toma dos minutos, no dos días.

## Un sistema mínimo de tokens

Un sistema mínimo de tokens para una organización pequeña típicamente necesita cuatro categorías:

**Color** — tres a cinco colores como máximo. Un color primario, un color de texto, un color de fondo, un color de borde y un color semántico (para errores o advertencias si es necesario). Todos los demás colores del sistema deben derivarse de estos o ser negro o blanco.

**Tipografía** — dos a tres tamaños de fuente para el texto del cuerpo, uno o dos para los encabezados, y uno para etiquetas pequeñas. Una altura de línea para cada uno. Una pila de fuentes por tipo de letra utilizado.

**Espaciado** — cuatro a seis valores de espaciado en una escala consistente. Recomendamos: 0,25rem, 0,5rem, 1rem, 2rem, 4rem. Todo lo demás se compone a partir de estos.

**Maquetación** — un ancho máximo de contenido (usamos `70ch` como predeterminado para el texto del cuerpo) y un valor de separación estándar para las maquetaciones en cuadrícula.

## Implementación

En CSS:

```css
:root {
  --colour-primary:    #0033cc;
  --colour-text:       #000000;
  --colour-background: #ffffff;
  --colour-border:     #d0d0d0;

  --font-body:    "IBM Plex Sans", system-ui, sans-serif;
  --font-display: "Space Grotesk", system-ui, sans-serif;

  --size-sm:   0.875rem;
  --size-base: 1rem;
  --size-lg:   1.25rem;
  --size-xl:   1.75rem;

  --space-sm:  0.5rem;
  --space-md:  1rem;
  --space-lg:  2rem;
  --space-xl:  4rem;

  --measure:   70ch;
}
```

Ese es el sistema completo de tokens para este sitio. Todo lo demás es composición.
