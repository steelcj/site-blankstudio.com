---
title: "Pila Soberana — Independencia de Infraestructura para una Red de Salud Regional"
date: 2026-03-01
description: "Un cambio completo de infraestructura para alejarse del bloqueo de nube propietaria en una red de salud regional que atiende a 80.000 pacientes — reemplazando servicios gestionados por proveedores con sistemas reproducibles, auto-alojados y auditables bajo el control operativo propio de la organización."
draft: false
params:
  status: "Completo"
  areas:
    - infrastructure
    - privacy
"sat:work": "urn:uuid:f945766e-c68b-4adf-a847-adf054b17682"
---

## Panorama general

Una red de salud regional que operaba en seis sitios había acumulado profundas dependencias en tres plataformas de nube propietarias separadas a lo largo de ocho años de crecimiento. La infraestructura era funcional pero opaca: ninguna persona comprendía el sistema completo, los contratos con proveedores se renovaban automáticamente sin revisión, y los datos de los pacientes se procesaban en diferentes jurisdicciones de maneras que eran inconsistentes con los propios compromisos de privacidad de la organización.

Nos contrataron para diseñar e implementar un camino hacia la independencia operativa — uno que no requiriera una transición abrupta y que no introdujera nuevas categorías de fragilidad en el proceso de eliminar las antiguas.

## Enfoque

Comenzamos con una auditoría completa de infraestructura: cada servicio, cada flujo de datos, cada dependencia externa mapeada y documentada. A partir de esa línea base identificamos tres categorías de dependencias — las que podían eliminarse de inmediato, las que requerían migración por fases, y aquellas para las que una alternativa soberana aún no existía y tendría que construirse.

La migración se realizó durante catorce meses a través de cuatro fases. Priorizamos primero los datos de los pacientes, trasladando todos los registros clínicos a un sistema auto-alojado y conforme con la jurisdicción, con verificación automatizada de respaldos y un procedimiento de restauración probado. Reemplazamos el sistema de identidad gestionado por el proveedor con una alternativa abierta y auditable. Descomisionamos completamente dos plataformas SaaS consolidando sus funciones en herramientas que la organización ya operaba.

## Resultado

La red ahora opera una infraestructura completamente documentada y reproducible. Cada servicio puede reconstruirse a partir de configuración con control de versiones. El equipo de guardia puede comprender el sistema completo en un día hábil. Los costos anuales de contratos con proveedores se redujeron en un 68%. Los compromisos de privacidad de la organización y su infraestructura real son ahora consistentes entre sí.

## Lo que construimos

- Auditoría completa de infraestructura y mapa de dependencias
- Plan de migración por fases con procedimientos de reversión en cada etapa
- Sistema de registros clínicos auto-alojado con respaldo automatizado y pruebas de restauración
- Plataforma abierta de gestión de identidad y acceso
- Runbooks y documentación operativa para el equipo interno
- Programa de capacitación para tres niveles de personal operativo
