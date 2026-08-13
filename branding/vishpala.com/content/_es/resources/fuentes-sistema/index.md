---
title: "Tipografía — Fuentes del sistema y Atkinson Hyperlegible"
date: 2026-06-15
description: "El enfoque tipográfico de vishpala.com: system-ui por defecto, con Atkinson Hyperlegible disponible como alternativa accesible elegida por el usuario, auto-alojada sin dependencias externas."
draft: false
params:
  status: "Estable"
  version: "1.1.0"
"sat:work": "urn:uuid:a93c44cd-7489-410b-8c4f-c7a76f3dba63"
---

## El enfoque

Este sitio usa `system-ui, sans-serif` — la pila tipográfica nativa del dispositivo — como tipografía por defecto. No se cargan fuentes desde fuentes externas. Como alternativa seleccionable por el usuario, Atkinson Hyperlegible está disponible y auto-alojada: todos los archivos de fuentes se sirven directamente desde este sitio sin solicitudes a terceros.

El selector de fuentes (`Aa`) en el encabezado del sitio permite elegir entre las dos opciones. Tu preferencia se guarda y se aplica en cada visita posterior.

## System-ui — la opción por defecto

Las fuentes del sistema son las que los fabricantes de sistemas operativos han optimizado más para la legibilidad en pantalla en cada tamaño, densidad de visualización y configuración de accesibilidad. San Francisco en macOS e iOS, Segoe UI en Windows y Roboto en Android son cada una el resultado de una inversión significativa en hinting, espaciado y renderizado.

Las fuentes del sistema respetan las preferencias tipográficas propias del usuario. Si un usuario ha configurado su sistema operativo para usar un tamaño de fuente mayor o un tipo de letra específico por razones de legibilidad, `system-ui` hereda esas preferencias. Para los usuarios que dependen de esas preferencias, esa herencia es importante.

`system-ui` no introduce ninguna dependencia externa y no impone ninguna carga de mantenimiento de infraestructura.

## Atkinson Hyperlegible — la alternativa accesible

Atkinson Hyperlegible fue diseñada por el Braille Institute específicamente para lectores con baja visión. Cada carácter está formado de manera única para evitar errores de lectura — las formas de las letras comúnmente confundidas (1/l/I, 0/O, rn/m) están deliberadamente diferenciadas. El Braille Institute la publicó bajo la SIL Open Font Licence 1.1, que permite el uso y la redistribución libres.

La fuente se sirve íntegramente desde la infraestructura propia de este sitio. Los ocho archivos de fuentes — normal, cursiva, negrita y negrita cursiva en rangos latin y latin extendido — solo se cargan cuando eliges Atkinson, y únicamente desde este dominio. No se realizan solicitudes a terceros.

El Centro de Investigación en Diseño Inclusivo de la Universidad OCAD, cuyo trabajo informa directamente nuestra práctica de accesibilidad, documenta Atkinson Hyperlegible como tipo de letra recomendado para la accesibilidad de baja visión.

## Soberanía y rendimiento

Ninguna de las dos opciones tipográficas carga fuentes desde Google Fonts ni ninguna otra fuente externa. No hay conexión a una red de distribución de fuentes de terceros ni divulgación de direcciones IP de visitantes a proveedores de fuentes.

Cuando system-ui está activo, el texto se renderiza inmediatamente usando una fuente ya presente en el dispositivo — sin solicitud de red, sin destello de texto invisible, sin desplazamiento de maquetación. Cuando Atkinson Hyperlegible está activo, los archivos de fuentes se cargan desde este servidor en el primer uso y el navegador los almacena en caché.

## Historial de versiones

| Versión | Fecha | Notas |
|---------|-------|-------|
| 1.1.0 | 2026-06-28 | Actualizado para reflejar la adición de Atkinson Hyperlegible como opción seleccionable por el usuario |
| 1.0.0 | 2026-06-15 | Versión inicial |
