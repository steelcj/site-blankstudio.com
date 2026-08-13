---
title: "Guía de Auditoría de Infraestructura — Mapear lo que Tiene Antes de Cambiarlo"
date: 2026-02-01
description: "Una guía práctica para realizar una auditoría completa de infraestructura: qué documentar, cómo descubrir dependencias ocultas y cómo producir un mapa que sea realmente útil para la toma de decisiones."
draft: false
params:
  status: "Estable"
  version: "1.0.0"
"sat:work": "urn:uuid:10c5df56-d52f-433f-9e21-ca874ab08fa1"
---

## Propósito

Antes de que comience cualquier trabajo de infraestructura, necesita una imagen precisa de lo que existe. Esta guía describe cómo realizar una auditoría completa de infraestructura — no un inventario teórico, sino un documento de trabajo que refleja el sistema tal como opera realmente.

## 1. Qué capturar

Una auditoría de infraestructura útil captura seis categorías de información:

1. **Servicios** — cada servicio en ejecución, su propósito, su operador y sus dependencias
2. **Flujos de datos** — dónde se origina cada dato, dónde se procesa, dónde se almacena y dónde sale de su control
3. **Acceso y credenciales** — quién tiene acceso a qué, bajo qué modelo de autenticación y dónde se almacenan las credenciales
4. **Dependencias externas** — cada servicio de terceros, API o plataforma de la que depende el sistema
5. **Contratos y costos** — cada contrato con proveedor, su fecha de renovación, su costo y lo que implicaría salir de él
6. **Documentación** — qué documentación existe, qué tan actualizada está y dónde reside

## 2. Cómo descubrir dependencias ocultas

Las dependencias ocultas son la parte más peligrosa de cualquier infraestructura. Son cosas de las que el sistema depende que nadie ha decidido explícitamente depender — acumuladas a través de años de decisiones pragmáticas que nunca se revisaron.

Las fuentes comunes de dependencias ocultas incluyen:

- Registros DNS que apuntan a servicios que ya no existen pero cuya eliminación rompería algo
- Entrega de correo electrónico que depende de una cuenta personal de un exempleado
- Flujos de autenticación que pasan a través de un servicio de terceros insertado hace años como medida temporal
- Trabajos de respaldo que escriben en una ubicación que silenciosamente se ha quedado sin espacio
- Certificados SSL gestionados por una persona que ha dejado la organización

La forma más confiable de descubrir dependencias ocultas es mapear los flujos de datos de afuera hacia adentro: comenzar desde cada URL pública y seguir cada solicitud a través del sistema hasta que llega al almacenamiento persistente o sale hacia un tercero.

## 3. Producir un mapa útil

Un mapa de infraestructura solo es útil si refleja el sistema real y puede ser leído por alguien que no lo construyó. Debe incluir:

- Un diagrama que muestre los componentes principales y las conexiones entre ellos
- Una tabla de servicios con propietario, dependencias y fecha de última verificación
- Una lista de dependencias externas con información de contrato y costo
- Una lista de preguntas abiertas que la auditoría planteó pero no pudo resolver

El mapa debe estar bajo control de versiones junto con la infraestructura que describe y actualizarse cada vez que se realice un cambio significativo.
