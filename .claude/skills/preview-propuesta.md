---
name: preview-propuesta
description: Muestra un preview en texto del documento antes de generar el Word. El preview se adapta al tipo de documento — no hay estructura fija. Úsalo para que el usuario apruebe el contenido.
---

Presenta el preview del documento adaptado al tipo de contenido.
Lee `brand.config.json` para obtener datos del proponente.

## Instrucción

Analiza qué se vende y muestra el preview en markdown con la estructura
que vas a generar. No hay un formato fijo — el preview debe reflejar
exactamente las secciones y tablas que usarás en el Word.

### Principios del preview

1. **Muestra lo que vas a generar** — si vas a usar una tabla de 3 columnas, muéstrala con esas 3 columnas.
2. **Incluye los valores reales** — no placeholders ni "XYZ".
3. **Indica los totales** — cualquier subtotal o total debe ser visible.
4. **Adapta el formato al contenido** — una cotización de equipos se ve diferente a una propuesta de formación.

### Ejemplos de estructura según tipo

**Cotización de equipos con fechas:**
```
══════════════════════════════════════════════
  [Empresa] → [Cliente]  |  NIT XXXXXXXXX
  [Subtítulo del evento]
══════════════════════════════════════════════

FECHAS DEL SERVICIO
  Partido 1  |  Uzbekistán vs Colombia   |  17 jun · 9:00 p.m.
  Partido 2  |  Colombia vs RD Congo     |  23 jun · 9:00 p.m.
  Partido 3  |  Colombia vs Portugal     |  27 jun · 6:30 p.m.

EQUIPOS  —  precio por fecha
  01  |  Pantalla 3×5                  |  $ 3.750.000
  02  |  4 QSC relevos                 |  $   800.000
  ...
  ────────────────────────────────────────────
      |  SUBTOTAL POR FECHA            |  $ 6.550.000
      |  TOTAL 3 FECHAS                |  $ 19.650.000

INVERSIÓN
  TOTAL: $ 19.650.000
  Pago a 30 días. Precio aplica por cada fecha.
  Incluye: Pantalla 3×5 · 4 QSC · ...

VIGENCIA: [fecha emisión] → [fecha vigencia]
PROPONENTE: [nombre] | [NIT]
══════════════════════════════════════════════
```

**Propuesta de servicio:**
```
══════════════════════════════════════════════
  [Empresa] → [Cliente]
  [Nombre del servicio]
══════════════════════════════════════════════

RESUMEN EJECUTIVO
  [2-3 oraciones describiendo el servicio]

MÓDULOS
  Módulo 1  |  [Tema]     |  [Descripción]
  Módulo 2  |  [Tema]     |  [Descripción]

DETALLES
  Modalidad   |  [Presencial / Virtual]
  Duración    |  [X horas]
  Incluye     |  [...]

INVERSIÓN  $ X.XXX.XXX
  ...
══════════════════════════════════════════════
```

---

## Después del preview

Pregunta:

> **¿El contenido está correcto?**
> 1. Sí, generar el Word → usa `/generar-propuesta`
> 2. Necesito ajustar algo → indica qué cambiar

No generes el `.docx` hasta recibir confirmación del usuario.
