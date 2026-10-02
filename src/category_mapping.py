"""SmartCart category and retailer mapping."""
import re

CATEGORY_RULES = {
    "Laptops": [r"\blaptop\b", r"\bnotebook computer\b", r"\bchromebook\b", r"\bmacbook\b"],
    "Mobiles": [r"\bsmartphone\b", r"\bmobile phone\b", r"\bcell phone\b", r"\biphone\b", r"\bredmi\b", r"\boneplus\b", r"\brealme\b"],
    "Makeup": [r"\blipstick\b", r"\bmascara\b", r"\bfoundation\b", r"\bconcealer\b", r"\beyeliner\b", r"\bmakeup\b", r"\bcosmetic\b", r"\beyeshadow\b", r"\bnail polish\b"],
    "Shoes": [r"\bshoes?\b", r"\bsneakers?\b", r"\bsandals?\b", r"\bboots?\b", r"\bfootwear\b", r"\bheels?\b", r"\bslippers?\b", r"\bloafers?\b"],
    "Clothing": [r"\bshirt\b", r"\bt-?shirt\b", r"\bjeans?\b", r"\btrousers?\b", r"\bkurta\b", r"\bkurti\b", r"\bclothing\b", r"\bapparel\b", r"\bhoodie\b", r"\bjacket\b", r"\bdress\b", r"\bskirt\b"],
    "Electronics": [r"\bheadphones?\b", r"\bearbuds?\b", r"\bspeaker\b", r"\bmonitor\b", r"\bkeyboard\b", r"\bmouse\b", r"\btelevision\b", r"\btv\b", r"\bcamera\b", r"\bcharger\b", r"\bsmartwatch\b", r"\btablet\b", r"\belectronics?\b", r"\bpower bank\b"],
}
PLATFORMS_BY_CATEGORY = {
    "Clothing": ["Amazon", "Flipkart", "Myntra", "AJIO"],
    "Laptops": ["Amazon", "Flipkart", "Croma", "Reliance Digital"],
    "Makeup": ["Amazon", "Flipkart", "Nykaa", "Myntra"],
    "Mobiles": ["Amazon", "Flipkart", "Croma", "Reliance Digital"],
    "Electronics": ["Amazon", "Flipkart", "Croma", "Reliance Digital"],
    "Shoes": ["Amazon", "Flipkart", "Myntra", "AJIO"],
}
ALIASES = {
    "amazon.in": "Amazon", "amazon": "Amazon", "flipkart.com": "Flipkart",
    "flipkart": "Flipkart", "myntra.com": "Myntra", "myntra": "Myntra",
    "ajio.com": "AJIO", "ajio": "AJIO", "croma.com": "Croma", "croma": "Croma",
    "reliance digital": "Reliance Digital", "reliancedigital.in": "Reliance Digital",
    "nykaa.com": "Nykaa", "nykaa": "Nykaa",
}
def infer_category(*values):
    text = " ".join(str(v) for v in values if v is not None).lower()
    for category, patterns in CATEGORY_RULES.items():
        if any(re.search(p, text, re.I) for p in patterns):
            return category
    return "Uncategorized"
def normalize_platform(value):
    if value is None:
        return ""
    raw = str(value).strip()
    return ALIASES.get(raw.lower(), raw)
