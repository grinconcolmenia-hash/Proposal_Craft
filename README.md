# ProposalCraft

Agente especializado en crear propuestas comerciales elegantes en Word (`.docx`) con la identidad visual de tu empresa, impulsado por Claude (Anthropic).

---

## ¿Qué hace?

- Genera propuestas comerciales y cotizaciones en `.docx` listas para enviar
- Aplica automáticamente los colores, tipografía y logo de tu marca
- El agente (Claude) decide qué secciones incluir y en qué orden según el contenido
- Soporta cotizaciones de equipos, propuestas de servicio, formación, presupuestos y más

---

## Requisitos

- Python 3.11+
- [Claude Code](https://claude.ai/code) (CLI de Anthropic)
- Dependencias Python:

```bash
pip install python-docx
```

---

## Instalación

```bash
git clone https://github.com/grinconcolmenia-hash/Proposal_Craft.git
cd Proposal_Craft
pip install python-docx
```

---

## Configuración inicial (solo una vez)

Antes de generar propuestas, configura la identidad de tu marca ejecutando el comando en Claude Code:

```
/configurar-marca
```

El agente te hará preguntas sobre:
- Nombre de empresa, tagline y sitio web
- Nombre y documento del proponente
- Colores corporativos (hex)
- Logo y banner (opcionales)
- Tipografía preferida

Esto genera `brand.config.json` en la raíz del proyecto y `agent_docs/brand_identity.md` con la identidad lista para usar.

---

## Uso con Claude Code (flujo recomendado)

### 1. Abre el proyecto en Claude Code

```bash
cd Proposal_Craft
claude
```

### 2. Pide una propuesta

Describe lo que necesitas en lenguaje natural:

> "Necesito una cotización para el cliente Empresa ABC, NIT 900123456-1, por alquiler de 2 pantallas LED y sonido para 3 fechas. Total: $4.500.000, pago a 30 días."

> "Genera una propuesta de servicio para Distribuidora XYZ sobre implementación de automatización comercial, 5 semanas, $8.500.000."

### 3. Aprueba el preview

El agente muestra un resumen del documento antes de generarlo (`/preview-propuesta`).

### 4. Obtén el `.docx`

Al aprobar, el agente ejecuta `/generar-propuesta` y el archivo queda en `outputs/`.

---

## Uso programático (sin agente)

Puedes generar documentos directamente con Python usando el motor universal:

```python
from src.brand_loader import load_brand
from src.document_engine import (
    generate_document, DocumentSpec,
    HeaderSection, TextSection, TableSection,
    InversionSection, VigenciaFirmaSection,
    Column, Row,
)

brand = load_brand()

spec = DocumentSpec(
    output_filename = "Cotizacion_Cliente.docx",
    sections = [
        HeaderSection(
            cliente     = "Empresa ABC",
            nit_cliente = "NIT 900123456-1",
            subtitulo   = "Alquiler de equipos audiovisuales",
        ),
        TableSection(
            titulo  = "Equipos",
            columns = [
                Column("N°",          0.08, "center"),
                Column("Descripcion", 0.72, "left"),
                Column("Valor",       0.20, "right"),
            ],
            rows = [
                Row(["01", "Pantalla LED 3x5",   "$ 2.500.000"]),
                Row(["02", "Sistema de sonido",  "$ 2.000.000"], "alt"),
                Row(["",   "TOTAL",              "$ 4.500.000"], "total"),
            ],
        ),
        InversionSection(
            valor_total = "$ 4.500.000",
            forma_pago  = "Pago a 30 días",
        ),
        VigenciaFirmaSection(),
    ],
)

path = generate_document(brand, spec)
print(f"Documento generado: {path}")
```

---

## Generar propuestas de demo

Para ver ejemplos de los 3 temas visuales disponibles:

```bash
python generar_demos.py
```

Los archivos se guardan en `outputs/`:
- `Demo_OscuroPrestige.docx` — tema oscuro elegante
- `Demo_ClaroFormal.docx` — tema claro y profesional
- `Demo_DualDinamico.docx` — tema dinámico con contraste

---

## Secciones disponibles

| Sección | Descripción |
|---|---|
| `HeaderSection` | Logo + datos del cliente (siempre al inicio) |
| `TextSection` | Texto libre con título (resúmenes, condiciones) |
| `TableSection` | Tabla configurable: ítems, módulos, fechas, precios |
| `InversionSection` | Bloque visual de total + forma de pago + incluye |
| `VigenciaFirmaSection` | Vigencia de la propuesta + espacio de firma |

### Estilos de fila (`TableSection`)

| Estilo | Apariencia |
|---|---|
| `normal` | Fondo claro (alternancia base) |
| `alt` | Fondo blanco (alternancia con normal) |
| `dark` | Fondo oscuro, texto de acento (header de grupo) |
| `subtotal` | Fondo accent_2, negrita |
| `total` | Fondo primario oscuro, texto grande, negrita |

---

## Estructura del proyecto

```
ProposalCraft/
├── brand.config.json       # Identidad visual (se genera con /configurar-marca)
├── generar_demos.py        # Script para generar propuestas de demo
├── CLAUDE.md               # Instrucciones del agente
│
├── src/
│   ├── brand_loader.py     # Lee brand.config.json y expone BrandConfig
│   ├── document_engine.py  # Motor universal de documentos (.docx)
│   ├── proposal_engine.py  # Motor de propuestas de servicio
│   └── quote_engine.py     # Motor de cotizaciones de equipos
│
├── agent_docs/
│   └── brand_identity.md   # Identidad visual generada (para el agente)
│
├── activos_de_marca/       # Logo, banner y otros assets visuales
│
└── outputs/                # Documentos generados (.docx)
```

---

## Skills disponibles en Claude Code

| Comando | Cuándo usarlo |
|---|---|
| `/configurar-marca` | Primera vez — configura marca y genera identidad |
| `/generar-identidad` | Si cambia la marca — regenera `brand_identity.md` |
| `/preview-propuesta` | Antes de generar — muestra el contenido para aprobar |
| `/generar-propuesta` | Tras aprobar — genera el `.docx` final |

---

## Notas importantes

- No generes propuestas sin configurar la marca primero (`/configurar-marca`)
- Los colores, tipografía y rutas siempre se leen desde `brand.config.json` — nunca hardcodeados
- Si falta un dato del cliente, el agente preguntará antes de continuar
- Los archivos en `outputs/` pueden contener datos de clientes — no subir al repositorio

---

## Licencia

MIT
