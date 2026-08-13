---
title: "Marco de Decisión para el Auto-Alojamiento — Cuándo Gestionarlo Usted Mismo y Cuándo No"
date: 2025-12-01
description: "Un marco práctico para decidir cuándo el auto-alojamiento de un servicio mejora la agencia de su organización y cuándo introduce complejidad sin un beneficio proporcional."
draft: false
params:
  status: "Estable"
  version: "1.0.0"
"sat:work": "urn:uuid:909abd2e-7f33-40fb-b3c0-41ba8d62179e"
---

## Propósito

El auto-alojamiento no es inherentemente mejor que usar un servicio gestionado. La pregunta es siempre si el auto-alojamiento, para este servicio, para esta organización, en este momento, produce un mejor resultado que las alternativas disponibles. Este marco ayuda a estructurar esa decisión.

## 1. Las cuatro preguntas

Antes de decidir auto-alojar cualquier servicio, responda cuatro preguntas:

**1. ¿Qué gana?**
Enumere los beneficios específicos: soberanía de datos, reducción de costos, eliminación de una dependencia de proveedor, alineación con un compromiso de privacidad, la capacidad de personalizar comportamientos que el proveedor no admitirá. Sea concreto. "Más control" no es suficiente — ¿control sobre qué, específicamente?

**2. ¿Cuánto cuesta operar?**
Los servicios auto-alojados requieren que alguien los mantenga: aplicando actualizaciones de seguridad, monitoreando fallos, gestionando respaldos y respondiendo cuando las cosas se rompen. ¿Quién hará esto? ¿Cuál es su capacidad? ¿Qué ocurre cuando no están disponibles?

**3. ¿Cuál es el modo de fallo?**
Si el servicio auto-alojado falla, ¿cuál es el impacto? ¿Con qué rapidez puede restaurarse? ¿Existe un procedimiento de recuperación probado? El modo de fallo de un servicio auto-alojado es típicamente un problema que usted debe resolver de una manera en que el modo de fallo de un servicio gestionado no lo es.

**4. ¿Cuál es el costo de salida?**
Si el auto-alojamiento resulta ser la decisión equivocada, ¿cuánto esfuerzo requiere migrar a un servicio gestionado? Un costo de salida bajo hace que la decisión sea reversible. Un costo de salida alto significa que necesita estar más seguro antes de comprometerse.

## 2. Cuándo el auto-alojamiento es claramente la elección correcta

El auto-alojamiento es claramente la elección correcta cuando:

- Los datos procesados por el servicio son sensibles y están sujetos a requisitos jurisdiccionales que los servicios gestionados no pueden satisfacer
- La organización tiene la capacidad operativa para mantener el servicio de manera confiable
- Las alternativas gestionadas son prohibitivamente costosas en relación con el valor entregado
- Las alternativas gestionadas tienen características de bloqueo inaceptables

## 3. Cuándo los servicios gestionados son claramente la elección correcta

Los servicios gestionados son claramente la elección correcta cuando:

- El costo operativo del auto-alojamiento supera el costo del servicio gestionado
- La organización no tiene la capacidad de responder a los fallos de manera confiable
- El servicio no forma parte de la competencia operativa central de la organización
- Los datos procesados no son sensibles y la jurisdicción no es una preocupación

## 4. La respuesta honesta la mayor parte del tiempo

La mayoría de las organizaciones deberían auto-alojar menos cosas de lo que los idealistas defienden y más cosas de lo que los proveedores prefieren. La respuesta correcta depende enteramente de la capacidad operativa, la sensibilidad de los datos y las alternativas específicas disponibles. Quien le dé una respuesta tajante no está abordando su situación real.
