---
title: "Sistema de Diseño Agencia — Infraestructura de Diseño Accesible y Multilingüe para una ONG Nacional"
date: 2026-01-15
description: "Un sistema de diseño completo y una biblioteca de componentes para una ONG nacional que opera en cuatro idiomas — construido con accesibilidad desde cero, mantenible por un pequeño equipo interno e independiente de cualquier cadena de herramientas de diseño propietaria."
draft: false
params:
  status: "Completo"
  areas:
    - design
    - accessibility
"sat:work": "urn:uuid:04d0e02e-098c-43d4-84a9-11581dfbc950"
---

## Panorama general

Una organización no gubernamental nacional con programas en doce provincias necesitaba una identidad visual coherente y presencia digital que pudiera ser mantenida por un equipo de tres empleados no especializados, traducida a cuatro idiomas sin degradación del diseño, y utilizada con confianza por personas con una amplia gama de discapacidades y niveles de acceso técnico.

El encargo era explícito en dos puntos: el sistema tenía que funcionar sin suscripción a ninguna herramienta de diseño, y tenía que lograr la conformidad WCAG 2.2 Nivel AA en cada punto de contacto.

## Enfoque

Auditamos la presencia digital existente e identificamos los treinta patrones de interfaz más utilizados. A partir de estos derivamos un sistema mínimo de design tokens: doce colores, cuatro tamaños de tipo, tres escalas de espaciado. Todo lo demás se compone a partir de estos elementos primitivos.

La biblioteca de componentes fue construida en HTML y CSS simples — sin dependencia de framework, sin paso de compilación para uso básico. Cada componente incluye sus anotaciones de accesibilidad, modelo de interacción por teclado y una descripción en lenguaje sencillo adecuada para personal no técnico. Las traducciones se gestionan a través de un archivo simple de clave-valor por idioma, sin requerir cambios de diseño para cambiar de idioma.

Realizamos pruebas de usabilidad con doce participantes en tres categorías de discapacidad y tres niveles de alfabetización digital antes de finalizar el sistema.

## Resultado

La presencia digital de la ONG es ahora coherente en los doce sitios provinciales. El equipo interno ha publicado cuatro actualizaciones de contenido importantes y una nueva página de programa sin apoyo externo. Las pruebas de accesibilidad automatizadas pasan al 100% en todas las páginas principales. Las versiones en francés, cree, inuktitut e inglés son mantenidas en paralelo por un único coordinador de contenido.

## Lo que construimos

- Sistema de design tokens (color, tipografía, espaciado)
- Biblioteca HTML/CSS de 30 componentes con anotaciones completas de accesibilidad
- Infraestructura de traducción (i18n de clave-valor, sin framework requerido)
- Auditoría y remediación de conformidad WCAG 2.2 Nivel AA
- Materiales de capacitación para el personal y guía de mantenimiento
- Proceso continuo de revisión trimestral de accesibilidad
