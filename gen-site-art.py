#!/usr/bin/env python3
# Generate hero artwork for the Lumi support site — matches the app's clay/soft-vinyl + golden starlight style.
import os, json, base64, urllib.request

def load_key():
    k = os.environ.get("OPENAI_API_KEY", "").strip()
    if k: return k
    p = os.path.expanduser("~/.openai_key")
    return open(p).read().strip() if os.path.exists(p) else ""

API_KEY = load_key()
ROOT = os.path.dirname(os.path.abspath(__file__))

JOBS = [
    {
        "out": "mascot.png",
        "size": "1024x1024",
        "background": "transparent",
        "prompt": (
            "An adorable chibi bear cub mascot for a children's app, soft premium clay / soft-vinyl designer-toy texture "
            "with delicate subsurface softness and a gentle warm GOLDEN rim light. The bear is friendly and welcoming, "
            "waving one paw, big sparkly eyes, rosy cheeks, tiny golden star sparkles floating around it. Macaron-pink and "
            "gold accents, glassy highlights, polished collectible quality, centered, full body, facing forward, "
            "fully transparent background, soft cinematic studio lighting, no text, premium and heart-warming."
        ),
    },
    {
        "out": "hero-bg.png",
        "size": "1536x1024",
        "background": "opaque",
        "prompt": (
            "A dreamy cosmic background illustration for a children's learning brand, in soft lavender and cosmic violet "
            "gradients fading to a paler center, gentle aurora ribbons in pink and gold, scattered tiny twinkling stars and "
            "delicate golden sparkles, a few small softly-glowing pastel planets with thin elegant golden rings near the "
            "edges, lots of calm open empty space in the middle for text, soft bokeh, premium clay / soft-vinyl dreamy "
            "texture, ethereal cinematic lighting, no characters, no text, elegant and high-end, wide landscape."
        ),
    },
    {
        "out": "scene.png",
        "size": "1536x1024",
        "background": "transparent",
        "prompt": (
            "A row of three tiny adorable cosmic creatures as a children's brand illustration: a little glowing star "
            "creature, a small pastel planet with a golden ring, and a tiny crescent moon with a sleepy smile. Soft premium "
            "clay / soft-vinyl designer-toy texture, gentle golden rim light, macaron pastel colors with gold accents, "
            "glassy highlights, floating with tiny sparkles, fully transparent background, soft cinematic lighting, "
            "no text, premium and charming, evenly spaced."
        ),
    },
]

def gen(job):
    body = {"model": "gpt-image-1", "prompt": job["prompt"], "size": job["size"],
            "quality": "high", "background": job["background"], "n": 1}
    req = urllib.request.Request(
        "https://api.openai.com/v1/images/generations",
        data=json.dumps(body).encode(),
        headers={"Authorization": f"Bearer {API_KEY}", "Content-Type": "application/json"},
    )
    with urllib.request.urlopen(req, timeout=420) as r:
        resp = json.load(r)
    img = base64.b64decode(resp["data"][0]["b64_json"])
    out = os.path.join(ROOT, job["out"])
    open(out, "wb").write(img)
    print("saved ->", job["out"], len(img), "bytes")

def main():
    if not API_KEY:
        print("NO_KEY"); return
    for j in JOBS:
        try:
            gen(j)
        except Exception as e:
            print("FAIL", j["out"], repr(e)[:200])

main()
