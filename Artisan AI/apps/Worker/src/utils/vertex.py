def generate_description(product: dict, tone: str, lang: str) -> str:
    title = product.get("title", "Handcrafted Item")
    materials = ", ".join(product.get("materials", []))
    return f"# {title} ({lang}, {tone})\n\nMaterials: {materials}\n\nA lovingly crafted piece..."
