"""
ProposalCraft — Brand Loader
Lee brand.config.json y expone un objeto BrandConfig con todos los
atributos de marca listos para usar en el motor de propuestas.
"""

import json
import os
from dataclasses import dataclass, field
from docx.shared import RGBColor


# ── Ruta del config (siempre en la raíz del proyecto) ─────────────────────────
_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CONFIG_PATH = os.path.join(_ROOT, "brand.config.json")
ASSETS_DEFAULT = os.path.join(_ROOT, "assets")


# ── Helpers ───────────────────────────────────────────────────────────────────

def _hex_to_rgb(hex_str: str) -> RGBColor:
    """Convierte '#RRGGBB' o 'RRGGBB' a RGBColor de python-docx."""
    h = hex_str.lstrip('#')
    if len(h) != 6:
        raise ValueError(f"Color inválido: '{hex_str}'. Usa formato #RRGGBB")
    r, g, b = int(h[0:2], 16), int(h[2:4], 16), int(h[4:6], 16)
    return RGBColor(r, g, b)


def _resolve_asset(filename: str, base_path: str) -> str | None:
    """Resuelve la ruta absoluta de un asset. Retorna None si no existe."""
    if not filename or filename.startswith("TODO"):
        return None
    # Si ya es ruta absoluta, usarla directamente
    if os.path.isabs(filename):
        path = filename
    else:
        path = os.path.join(base_path, filename)
    if os.path.exists(path):
        return path
    print(f"  [AVISO] Asset no encontrado: {path} — se omitirá en el documento.")
    return None


# ── Dataclass de configuración ─────────────────────────────────────────────────

@dataclass
class BrandConfig:
    # Empresa
    company_name: str
    company_tagline: str
    company_website: str

    # Proponente
    proponent_name: str
    proponent_id_label: str
    proponent_id_number: str

    # Colores (RGBColor listos para python-docx)
    color_primary_dark: RGBColor
    color_accent_1: RGBColor
    color_accent_2: RGBColor
    color_body_text: RGBColor
    color_light_bg: RGBColor
    color_mid_gray: RGBColor
    color_white: RGBColor

    # Colores hex (para funciones que los piden como string)
    hex_primary_dark: str
    hex_accent_1: str
    hex_accent_2: str

    # Tipografía
    font_primary: str
    font_fallback: str

    # Tema visual
    theme: str

    # Assets (rutas absolutas o None si no existen)
    logo_light_path: str | None
    logo_dark_path: str | None
    banner_path: str | None

    # Defaults
    validity_days: int
    output_dir: str
    currency: str

    # ── Propiedad útil: fuente a usar (primary si está instalada, si no fallback)
    @property
    def layout_preset(self) -> str:
        """Deriva el preset de layout desde el nombre del tema activo."""
        name = (self.theme or "").lower()
        if "claro" in name or "formal" in name:
            return "light"
        if "dual" in name or "dinamico" in name:
            return "dual"
        return "dark"

    @property
    def font(self) -> str:
        return self.font_primary or self.font_fallback or "Calibri"

    @property
    def proponent_full(self) -> str:
        """Línea completa del proponente para pie de página y firma."""
        parts = [self.company_name]
        if self.proponent_name:
            parts.append(self.proponent_name)
        return " · ".join(filter(None, parts))

    @property
    def proponent_id_full(self) -> str:
        """Ej: 'C.C. 1020834494'"""
        if self.proponent_id_label and self.proponent_id_number:
            return f"{self.proponent_id_label} {self.proponent_id_number}"
        return self.proponent_id_number


# ── Función principal ──────────────────────────────────────────────────────────

def load_brand(config_path: str = CONFIG_PATH) -> BrandConfig:
    """
    Lee brand.config.json y retorna un BrandConfig validado.
    Lanza ValueError si faltan campos obligatorios con valor 'TODO:...'.
    """
    if not os.path.exists(config_path):
        raise FileNotFoundError(
            f"No se encontró brand.config.json en: {config_path}\n"
            "Ejecuta primero: python setup_brand.py"
        )

    with open(config_path, encoding="utf-8") as f:
        cfg = json.load(f)

    # Validar campos obligatorios (no deben empezar con "TODO")
    _required = {
        "company.name":        cfg.get("company", {}).get("name", ""),
        "proponent.name":      cfg.get("proponent", {}).get("name", ""),
        "proponent.id_number": cfg.get("proponent", {}).get("id_number", ""),
    }
    missing = [k for k, v in _required.items() if not v or str(v).startswith("TODO")]
    if missing:
        raise ValueError(
            f"brand.config.json tiene campos sin completar: {missing}\n"
            "Edita brand.config.json o ejecuta: python setup_brand.py"
        )

    # Assets
    assets_cfg = cfg.get("assets", {})
    assets_base = assets_cfg.get("assets_base_path", "./assets/")
    if not os.path.isabs(assets_base):
        assets_base = os.path.join(_ROOT, assets_base.lstrip("./"))

    logo_light = _resolve_asset(assets_cfg.get("logo_light", ""), assets_base)
    logo_dark  = _resolve_asset(assets_cfg.get("logo_dark", ""), assets_base)
    banner     = _resolve_asset(assets_cfg.get("banner", ""), assets_base)

    # Colores — soporta estructura nueva (brand.themes.options) y antigua (brand.colors)
    brand_cfg = cfg.get("brand", {})
    themes_cfg = brand_cfg.get("themes", {})
    if themes_cfg:
        active = themes_cfg.get("active", "")
        options = themes_cfg.get("options", {})
        colors = options.get(active, next(iter(options.values()), {})).get("colors", {})
        active_theme = active
    else:
        colors = brand_cfg.get("colors", {})
        active_theme = brand_cfg.get("theme", "default")

    _c = lambda key, default: _hex_to_rgb(colors.get(key, default))

    hex_dark    = colors.get("primary_dark", "#0D0D0D").lstrip("#")
    hex_accent1 = colors.get("accent_1", "#00FF57").lstrip("#")
    hex_accent2 = colors.get("accent_2", "#2244FF").lstrip("#")

    # Defaults
    defaults = cfg.get("defaults", {})
    output_dir = defaults.get("output_dir", "./outputs/")
    if not os.path.isabs(output_dir):
        output_dir = os.path.join(_ROOT, output_dir.lstrip("./"))
    os.makedirs(output_dir, exist_ok=True)

    fonts = brand_cfg.get("fonts", {})

    return BrandConfig(
        company_name     = cfg["company"]["name"],
        company_tagline  = cfg["company"].get("tagline", ""),
        company_website  = cfg["company"].get("website", ""),

        proponent_name     = cfg["proponent"]["name"],
        proponent_id_label = cfg["proponent"].get("id_label", ""),
        proponent_id_number= cfg["proponent"]["id_number"],

        color_primary_dark = _c("primary_dark", "#0D0D0D"),
        color_accent_1     = _c("accent_1", "#00FF57"),
        color_accent_2     = _c("accent_2", "#2244FF"),
        color_body_text    = _c("body_text", "#1A1A1A"),
        color_light_bg     = _c("light_bg", "#F0FFF4"),
        color_mid_gray     = _c("mid_gray", "#7A8899"),
        color_white        = RGBColor(0xFF, 0xFF, 0xFF),

        hex_primary_dark = hex_dark,
        hex_accent_1     = hex_accent1,
        hex_accent_2     = hex_accent2,

        font_primary  = fonts.get("primary", "Poppins"),
        font_fallback = fonts.get("fallback", "Calibri"),

        theme = active_theme,

        logo_light_path = logo_light,
        logo_dark_path  = logo_dark,
        banner_path     = banner,

        validity_days = int(defaults.get("validity_days", 30)),
        output_dir    = output_dir,
        currency      = defaults.get("currency", "COP"),
    )
