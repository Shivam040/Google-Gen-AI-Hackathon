# apps/api/src/services/text_templates.py
from __future__ import annotations
from typing import Dict, Any, List

def _take_first(xs: List[str] | None) -> str:
    return (xs or [None])[0] or ""

def _clean(s: str) -> str:
    return " ".join(str(s).split()).strip()

def compose_short_description(p: Dict[str, Any]) -> str:
    """
    e.g., `Panting 1 — Traditional Drawing. Thoughtfully crafted with love.`
    """
    title = _clean(p.get("title") or "Untitled")
    style = _take_first(p.get("materials"))  # you store Theme here
    ptype = _clean(p.get("category") or "")
    bits = [title, "—"]
    if style:
        bits.append(style)
    if ptype:
        bits.append(ptype)
    line = " ".join(bits)
    return f"{_clean(line)}. Thoughtfully crafted with love."

def compose_quick_history(p: Dict[str, Any]) -> str:
    """
    Compact provenance/history built only from user-entered fields.
    Uses: title, materials(theme), category(type), region, artisan_name,
    attributes (size,color,technique,material,care), provenance (year,origin,inspiration,technique,...)
    """
    title = _clean(p.get("title") or "Untitled Piece")
    style = _take_first(p.get("materials"))
    ptype = _clean(p.get("category") or "")
    region = _clean(p.get("region") or "")
    artisan = _clean(p.get("artisan_name") or p.get("artisan") or "")

    attrs = p.get("attributes") or {}
    prov  = p.get("provenance") or {}

    year       = _clean(prov.get("year") or prov.get("date") or prov.get("made") or "")
    technique  = _clean(attrs.get("technique") or prov.get("technique") or "")
    material   = _clean(attrs.get("material") or prov.get("material") or "")
    size       = _clean(attrs.get("size") or attrs.get("dimensions") or "")
    color      = _clean(attrs.get("color") or "")
    origin     = _clean(prov.get("origin") or "")
    inspiration= _clean(prov.get("inspiration") or "")
    care       = _clean(prov.get("care") or attrs.get("care") or "")

    opener_parts = [f"“{title}” is a"]
    if style: opener_parts.append(style.lower())
    if ptype: opener_parts.append(ptype.lower())
    opener_parts.append("crafted")
    if artisan: opener_parts.append(f"by {artisan}")
    if region:  opener_parts.append(f"in {region}")
    if year:    opener_parts.append(f"in {year}")
    opener = _clean(" ".join(opener_parts)) + "."

    facts = " • ".join(
        [f"Technique: {technique}" if technique else "",
         f"Materials: {material}"  if material  else "",
         f"Size: {size}"           if size      else "",
         f"Palette: {color}"       if color     else "",
         f"Origin: {origin}"       if origin    else "",
         f"Inspiration: {inspiration}" if inspiration else ""]
    ).strip(" •")

    bits = [opener]
    if facts: bits.append(facts + ".")
    if care:  bits.append(f"Care: {care}.")
    return _clean(" ".join([b for b in bits if b]))
