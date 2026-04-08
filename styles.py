STYLES: dict[str, dict] = {
    "cinematic": {
        "prefix": "cinematic film still, dramatic lighting, shallow depth of field, anamorphic lens flare, 35mm film grain, color graded,",
        "suffix": "directed by Roger Deakins, IMAX quality, 8k resolution",
        "negative": "cartoon, anime, drawing, low quality, blurry, oversaturated",
        "guidance_scale": 1.5,
        "num_inference_steps": 4,
    },
    "anime": {
        "prefix": "anime masterpiece, Studio Ghibli style, cel shaded, vibrant colors, detailed background,",
        "suffix": "trending on pixiv, best quality, ultra detailed anime illustration",
        "negative": "photorealistic, 3d render, low quality, blurry, deformed",
        "guidance_scale": 1.5,
        "num_inference_steps": 4,
    },
    "photorealistic": {
        "prefix": "professional photograph, DSLR, natural lighting, sharp focus, high detail,",
        "suffix": "shot on Canon EOS R5, 85mm f/1.4, RAW photo, 8k uhd",
        "negative": "cartoon, painting, illustration, drawing, artificial, blurry",
        "guidance_scale": 1.5,
        "num_inference_steps": 4,
    },
    "pixel_art": {
        "prefix": "pixel art, 16-bit retro game style, clean pixels, limited color palette,",
        "suffix": "pixelated, retro gaming aesthetic, crisp edges, nostalgic",
        "negative": "blurry, smooth, photorealistic, 3d render, high resolution photo",
        "guidance_scale": 1.5,
        "num_inference_steps": 4,
    },
    "watercolor": {
        "prefix": "delicate watercolor painting, soft washes, wet-on-wet technique, visible paper texture,",
        "suffix": "fine art watercolor, museum quality, translucent pigments, artistic",
        "negative": "digital art, photorealistic, sharp edges, 3d render, cartoon",
        "guidance_scale": 1.5,
        "num_inference_steps": 4,
    },
    "comic_book": {
        "prefix": "comic book art, bold ink outlines, halftone dots, dynamic composition, vibrant flat colors,",
        "suffix": "Marvel Comics style, Jack Kirby inspired, splash page, high contrast",
        "negative": "photorealistic, blurry, soft, watercolor, 3d render",
        "guidance_scale": 1.5,
        "num_inference_steps": 4,
    },
    "cyberpunk": {
        "prefix": "cyberpunk aesthetic, neon lights, rain-slicked streets, holographic displays, futuristic,",
        "suffix": "Blade Runner inspired, synthwave colors, dystopian megacity, volumetric fog, 8k",
        "negative": "nature, pastoral, bright daylight, cartoon, low quality",
        "guidance_scale": 1.5,
        "num_inference_steps": 4,
    },
    "oil_painting": {
        "prefix": "classical oil painting, thick impasto brushstrokes, rich pigments, chiaroscuro lighting,",
        "suffix": "museum masterpiece, Rembrandt style, canvas texture visible, fine art",
        "negative": "digital, photorealistic, flat colors, cartoon, low quality",
        "guidance_scale": 1.5,
        "num_inference_steps": 4,
    },
    "raw": {
        "prefix": "",
        "suffix": "",
        "negative": "low quality, blurry, deformed, distorted",
        "guidance_scale": 1.0,
        "num_inference_steps": 4,
    },
}


def build_prompt(user_prompt: str, style_name: str) -> dict:
    """Combine user prompt with style system prompt."""
    style = STYLES.get(style_name)
    if style is None:
        raise ValueError(
            f"Unknown style '{style_name}'. Available: {list(STYLES.keys())}"
        )

    parts = [p for p in [style["prefix"], user_prompt, style["suffix"]] if p]
    return {
        "prompt": " ".join(parts),
        "negative_prompt": style["negative"],
        "guidance_scale": style["guidance_scale"],
        "num_inference_steps": style["num_inference_steps"],
    }
