---
name: generar-propuesta
description: Genera el archivo Word (.docx) final. Analiza qué se vende, decide las secciones del documento, construye el DocumentSpec y llama al motor universal. NO usa estructura fija — el agente decide el layout.
---

Lee la conversación. Entiende qué se vende. Decide qué secciones necesita el documento y en qué orden. Genera el Word.

## Prerequisitos

- `brand.config.json` sin campos `TODO:`
- `agent_docs/brand_identity.md` existe
- Datos de la propuesta confirmados por el usuario

---

## Motor a usar

```python
import sys
sys.path.insert(0, ".")

from src.brand_loader import load_brand
from src.document_engine import (
    generate_document, DocumentSpec,
    HeaderSection, TextSection, TableSection,
    InversionSection, VigenciaFirmaSection,
    Column, Row,
)

brand = load_brand()
spec  = DocumentSpec(
    output_filename = "...",
    sections = [ ... ],   # decidir según el tipo de documento
)
path = generate_document(brand, spec)
print("Generado:", path)
```

---

## Cómo decidir las secciones

Analiza qué se vende y elige la combinación de secciones:

| Tipo de documento       | Secciones recomendadas |
|-------------------------|------------------------|
| Cotización de equipos   | Header → Tabla fechas (si hay) → Tabla ítems con totales → Inversión → Firma |
| Propuesta de servicio   | Header → Texto resumen → Tabla módulos → Tabla detalles → Inversión → Firma |
| Propuesta de formación  | Header → Texto → Tabla programa → Tabla logística → Inversión → Firma |
| Presupuesto simple      | Header → Tabla líneas → Inversión → Firma |
| Solo texto + condiciones| Header → Texto → Tabla condiciones → Firma |

No hay combinación incorrecta. Usa las secciones que el contenido necesita.

---

## Reglas para TableSection

### Columnas (Column)

- `width_pct` = proporción del ancho total. **Todas las columnas deben sumar exactamente 1.0.**
- Guías de ancho:
  - Columna índice / número: `0.07` – `0.10`
  - Columna descripción larga: `0.50` – `0.72`
  - Columna valor / precio: `0.18` – `0.25`
  - Columna hora / detalle corto: `0.25` – `0.35`
  - Columna label / categoría: `0.10` – `0.18`

### Estilos de fila (Row.style)

| style    | Visual | Cuándo usarlo |
|----------|--------|---------------|
| `normal`   | Fondo claro                         | Filas estándar impares |
| `alt`      | Fondo blanco                        | Filas estándar pares (alternancia) |
| `dark`     | Fondo oscuro, texto acento          | Header de grupo dentro de tabla |
| `subtotal` | Fondo accent_2, texto acento, bold  | Subtotales intermedios |
| `total`    | Fondo oscuro, texto acento, bold grande | Fila de total final |

---

## Reglas para InversionSection

- `valor_total`: string con el valor formateado: `"$ 19.650.000"`
- `incluye`: texto libre con saltos de línea `\n` para listar ítems:
  `"- Ítem 1\n- Ítem 2\n- Ítem 3"`

---

## Confirmar al usuario

Después de generar, reporta:
- Ruta del archivo: `outputs/[nombre].docx`
- Tipo de documento generado y secciones usadas
- Invita a revisar y pedir ajustes

---

## Reglas globales

- Colores, logo y fuente vienen de `brand.config.json` — nunca hardcodear
- No inventar datos — si falta algún dato, preguntar antes de generar
- El archivo se guarda en `outputs/` — no subir al repo si contiene datos de clientes
