"""
generar_demos.py — Genera 3 propuestas de demo (una por tema visual).
Ejecutar: python generar_demos.py
Los .docx quedan en outputs/
"""

import os
from docx.shared import RGBColor
from src.brand_loader import BrandConfig
from src.proposal_engine import generate_proposal, ProposalData

ROOT = os.path.dirname(os.path.abspath(__file__))
OUTPUT_DIR = os.path.join(ROOT, "outputs")
os.makedirs(OUTPUT_DIR, exist_ok=True)

# ── Contenido de propuesta inventado ─────────────────────────────────────────

MODULOS = [
    ("M1", "Semana 1\nDiagnóstico", "· Auditoría de procesos comerciales actuales\n· Entrevistas con el equipo de ventas\n· Benchmark de competidores directos"),
    ("M2", "Semana 2–3\nDiseño", "· Definición de flujo de automatización\n· Maquetado de secuencias de correo\n· Integración con CRM existente"),
    ("M3", "Semana 4\nImplementación", "· Configuración de herramientas\n· Capacitación del equipo (2 sesiones)\n· Pruebas piloto con 50 leads reales"),
    ("M4", "Semana 5\nEntrega", "· Dashboard de métricas en vivo\n· Manual operativo del sistema\n· Soporte post-lanzamiento (30 días)"),
]

DETALLES = [
    ("Modalidad",     "Remota con 2 sesiones presenciales en Bogotá"),
    ("Participantes", "Hasta 8 personas del equipo comercial"),
    ("Duración",      "5 semanas calendario"),
    ("Entregables",   "Flujo automatizado, manual operativo, dashboard"),
    ("Soporte",       "30 días vía WhatsApp y correo tras la entrega"),
]

PROPUESTA = dict(
    cliente       = "Distribuidora Andina S.A.S.",
    titulo        = "Automatización Comercial con IA",
    tagline       = "Más cierres, menos trabajo manual — su equipo enfocado en lo que importa",
    resumen       = (
        "Distribuidora Andina enfrenta el reto común de equipos comerciales: demasiado tiempo "
        "en tareas repetitivas y poco en conversaciones de valor. Esta propuesta plantea un sistema "
        "de automatización que califica leads automáticamente, genera seguimientos personalizados "
        "y centraliza la información en un solo lugar. Resultado esperado: 40% menos tiempo "
        "administrativo y 25% más tasa de cierre en los primeros 60 días."
    ),
    modulos       = MODULOS,
    detalles      = DETALLES,
    valor_total   = "$ 8.500.000",
    forma_pago    = "50% al confirmar · 50% al entregar el sistema",
    incluye       = "· Licencias de herramientas (primer mes)\n· Sesiones de capacitación\n· Dashboard de métricas\n· Soporte 30 días",
)

# ── Marca base (colores fijos, solo cambia el tema) ────────────────────────

def make_brand(theme_name: str) -> BrandConfig:
    """Crea un BrandConfig con datos de demo y el tema indicado."""
    return BrandConfig(
        company_name        = "Colmen IA",
        company_tagline     = "Inteligencia artificial aplicada a negocios reales",
        company_website     = "colmen.ai",

        proponent_name      = "Gabriel Rueda",
        proponent_id_label  = "C.C.",
        proponent_id_number = "1020834494",

        # Colores
        color_primary_dark  = RGBColor(0x0D, 0x0D, 0x0D),
        color_accent_1      = RGBColor(0x00, 0xFF, 0x57),
        color_accent_2      = RGBColor(0x22, 0x44, 0xFF),
        color_body_text     = RGBColor(0x1A, 0x1A, 0x1A),
        color_light_bg      = RGBColor(0xF0, 0xFF, 0xF4),
        color_mid_gray      = RGBColor(0x7A, 0x88, 0x99),
        color_white         = RGBColor(0xFF, 0xFF, 0xFF),

        hex_primary_dark    = "0D0D0D",
        hex_accent_1        = "00FF57",
        hex_accent_2        = "2244FF",

        font_primary        = "Calibri",
        font_fallback       = "Calibri",

        theme               = theme_name,

        logo_light_path     = None,
        logo_dark_path      = None,
        banner_path         = None,

        validity_days       = 30,
        output_dir          = OUTPUT_DIR,
        currency            = "COP",
    )


# ── Generar los 3 archivos ─────────────────────────────────────────────────

TEMAS = [
    ("ColmenIA_OscuroPrestige", "Demo_OscuroPrestige.docx"),
    ("ColmenIA_ClaroFormal",    "Demo_ClaroFormal.docx"),
    ("ColmenIA_DualDinamico",   "Demo_DualDinamico.docx"),
]

for tema, filename in TEMAS:
    brand    = make_brand(tema)
    proposal = ProposalData(**PROPUESTA, output_filename=filename)
    out      = generate_proposal(brand, proposal)
    print(f"  OK: {os.path.basename(out)}")

print("\nListo. Abre los 3 archivos en outputs/ para comparar.")
