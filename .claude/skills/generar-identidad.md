---
name: generar-identidad
description: Genera el documento de identidad visual de marca del usuario (agent_docs/brand_identity.md) leyendo brand.config.json y los activos en activos_de_marca/. Ejecutar una vez después de completar setup_brand.py.
---

Tu tarea es generar el archivo `agent_docs/brand_identity.md` personalizado para el usuario.
Este documento será la referencia maestra de marca que el agente leerá antes de generar cualquier propuesta.

---

## Paso 1 — Leer la configuración

Lee el archivo `brand.config.json` en la raíz del proyecto.

Si hay campos con valor `TODO:`, detente y pide al usuario que ejecute primero:
```
python setup_brand.py
```

Extrae estos valores:
- `company.name` → nombre de la empresa
- `company.tagline` → slogan
- `proponent.name` → nombre del proponente
- `proponent.id_label` + `proponent.id_number` → identificación
- `brand.colors.*` → los 6 colores HEX
- `brand.fonts.primary` → fuente principal
- `brand.theme` → tema activo
- `assets.*` → nombres de archivos de logo y banner
- `defaults.validity_days` → vigencia

---

## Paso 2 — Inspeccionar activos_de_marca/

Lista los archivos presentes en la carpeta `activos_de_marca/` usando un comando bash o glob.

Identifica qué hay disponible:
- Logos (PNG, JPG, SVG)
- Banners
- Fuentes (TTF, OTF)
- Otros archivos de identidad

---

## Paso 3 — Generar agent_docs/brand_identity.md

Crea el archivo con esta estructura exacta, reemplazando todos los valores con los del usuario:

```markdown
# Identidad Visual — [company.name]
> Referencia maestra para el agente de propuestas. Leer antes de generar cualquier documento.

---

## Esencia de Marca

**[company.name]** — [company.tagline]

- **Tono visual:** [inferir del tema activo y colores: ej. "Tech · Moderno · Confiable"]
- **Personalidad:** [inferir de la paleta elegida]
- **Sitio web:** [company.website si está definido]

---

## Paleta de Colores

| Rol | HEX | Uso en documentos |
|---|---|---|
| Color oscuro principal | `[primary_dark]` | Fondos de headers, tablas oscuras, separadores |
| Acento principal | `[accent_1]` | Títulos de sección, valor de inversión, badges |
| Acento secundario | `[accent_2]` | Elementos de soporte, gradientes |
| Texto cuerpo | `[body_text]` | Todo el texto corriente |
| Fondo claro | `[light_bg]` | Filas alternas de tablas |
| Gris medio | `[mid_gray]` | Textos secundarios, pie de página |

### Regla de balance (60 · 30 · 10)
- **60%** — [primary_dark]: fondos, headers, zonas de autoridad
- **30%** — [accent_2 o light_bg]: soporte estructural, cuerpo
- **10%** — [accent_1]: acento puntual — inversión, títulos clave

### En python-docx
```python
from docx.shared import RGBColor

COLOR_DARK    = RGBColor(0x__, 0x__, 0x__)   # [primary_dark]
COLOR_ACCENT  = RGBColor(0x__, 0x__, 0x__)   # [accent_1]
COLOR_ACCENT2 = RGBColor(0x__, 0x__, 0x__)   # [accent_2]
COLOR_TEXT    = RGBColor(0x__, 0x__, 0x__)   # [body_text]
COLOR_LIGHT   = RGBColor(0x__, 0x__, 0x__)   # [light_bg]
COLOR_GRAY    = RGBColor(0x__, 0x__, 0x__)   # [mid_gray]
WHITE         = RGBColor(0xFF, 0xFF, 0xFF)
```
*(Llenar los valores hex como pares de bytes)*

---

## Tipografía

| Fuente | Rol | Instalada |
|---|---|---|
| **[font_primary]** | Principal — todo el documento | [verificar en activos_de_marca/] |
| **[font_fallback]** | Alternativa si la principal no carga | Sí (fuente del sistema) |

**Jerarquía en propuestas:**
- Título principal: [font_primary] Bold, 16–18 pt, [primary_dark]
- Secciones: [font_primary] SemiBold, 8.5–9 pt, [accent_1]
- Cuerpo: [font_primary] Regular, 9–9.5 pt, [body_text]
- Secundario: [font_primary] Regular, 8 pt, [mid_gray]

---

## Assets de Marca

Todos los activos en: `activos_de_marca/`

### Logos
[listar todos los archivos de logo encontrados en activos_de_marca/ con descripción de cuándo usar cada uno]

| Archivo | Cuándo usar |
|---|---|
| [assets.logo_light] | Sobre fondos OSCUROS (versión clara/blanca) |
| [assets.logo_dark] | Sobre fondos CLAROS (versión normal/color) |

### Banner de cierre
| Archivo | Descripción |
|---|---|
| [assets.banner] | Insertar al final del documento, ~17 cm ancho |

### Fuentes
[listar archivos .ttf / .otf encontrados en activos_de_marca/]

---

## Tema Activo: [brand.theme]

[Inferir la descripción del tema a partir del nombre almacenado en `brand.theme` y los colores configurados. No usar nombres hardcodeados — describir según lo que los colores comunican:]

- Si el nombre contiene "Oscuro" o "Prestige": fondo [primary_dark] dominante, acento puntual en [accent_1]. Máximo contraste. Propuestas de alto valor.
- Si el nombre contiene "Claro" o "Formal": estructura blanca/clara como base, [primary_dark] en jerarquía y bordes, [accent_1] como acento puntual. Aspecto limpio y corporativo.
- Si el nombre contiene "Dual" o "Dinamico": alternancia entre bloques oscuros y claros, [accent_1] y [accent_2] combinados. Energético y moderno.
- Si el nombre no indica estilo claramente: inferir del ratio de luminosidad entre [primary_dark] y [accent_1].

Describe en 2–3 líneas cómo se ve el documento con ese tema y para qué tipo de clientes es ideal.

### Distribución de colores en el documento (tema activo)

| Zona | Color | HEX |
|---|---|---|
| Fondos de header / tablas oscuras | [primary_dark] | `[hex]` |
| Títulos de sección | [accent_1] | `[hex]` |
| Valor de inversión (hero) | [accent_1] | `[hex]` |
| Filas alternas de tabla | [light_bg] | `[hex]` |
| Filas base | Blanco | `#FFFFFF` |
| Texto sobre fondos oscuros | Blanco | `#FFFFFF` |
| Texto secundario | [mid_gray] | `[hex]` |
| Separadores | [primary_dark] | `[hex]` |
| Pie de página — línea | [accent_1] | `[hex]` |

---

## Proponente y Datos Fijos

Estos valores aparecen automáticamente en toda propuesta generada.
No preguntar al usuario — vienen de `brand.config.json`.

| Campo | Valor |
|---|---|
| Empresa | [company.name] |
| Proponente | [proponent.name] |
| Identificación | [proponent.id_label] [proponent.id_number] |
| Vigencia por defecto | [defaults.validity_days] días calendario |

---

## Cómo usar este documento

1. El agente lee este archivo antes de generar cualquier propuesta
2. Todos los colores y assets referenciados aquí están disponibles en `activos_de_marca/`
3. Si cambia la marca, ejecutar `/generar-identidad` para regenerar este archivo

*Generado por ProposalCraft · [fecha de generación]*
```

---

## Paso 4 — Escribir el archivo

Escribe el contenido generado en `agent_docs/brand_identity.md`.

Asegúrate de:
- Reemplazar **todos** los placeholders con valores reales del config
- Calcular los valores RGB en bytes para el bloque python-docx (ej. `#12F280` → `RGBColor(0x12, 0xF2, 0x80)`)
- Listar solo los archivos que realmente existen en `activos_de_marca/`
- Inferir el tono visual a partir de la combinación de colores (oscuro + neón = tech/bold, azul + gris = corporativo, etc.)

---

## Paso 5 — Confirmar al usuario y continuar

Reporta:
- Ruta del archivo generado: `agent_docs/brand_identity.md`
- Colores registrados (muestra la tabla de paleta)
- Assets encontrados en `activos_de_marca/`
- Si falta algún asset (logo o banner no encontrado), avisar con instrucción clara de dónde colocarlo

**Luego continúa automáticamente al flujo de propuesta** — no esperes que el usuario pida el siguiente paso:

> "Identidad de marca configurada. Ahora dime: ¿para qué cliente y qué servicio quieres generar la primera propuesta?"

Esto inicia la **Ruta B** del flujo (recopilación de datos de la propuesta).

---

## Antipatrones — no hacer

- No inventar rutas de assets — solo listar lo que realmente existe en `activos_de_marca/`
- No generar el documento si hay campos `TODO:` sin completar en el config
- No quedarse esperando después de generar el MD — continuar activamente al flujo de propuesta
