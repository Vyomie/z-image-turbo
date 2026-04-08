STYLES: dict[str, dict] = {
    "biology": {
        "prefix": "scientifically accurate biological illustration, clean cartoon style, vibrant green and teal color palette, labeled diagram without text, cross-section view, soft cell shading,",
        "suffix": "educational scientific illustration, anatomically correct, no text, no labels, no watermarks, white background, clean vector-like art, bright pastel colors",
        "negative": "text, words, letters, labels, watermark, signature, photorealistic, blurry, dark, scary, gore, inaccurate anatomy",
        "guidance_scale": 1.5,
        "num_inference_steps": 4,
    },
    "chemistry": {
        "prefix": "scientifically accurate chemistry illustration, clean cartoon style, molecular structures, vibrant blue and purple color palette, soft shading,",
        "suffix": "educational scientific illustration, correct molecular geometry, no text, no labels, white background, clean vector-like art, colorful atoms and bonds",
        "negative": "text, words, letters, labels, watermark, signature, photorealistic, blurry, incorrect bonds, dark, messy",
        "guidance_scale": 1.5,
        "num_inference_steps": 4,
    },
    "physics": {
        "prefix": "scientifically accurate physics illustration, clean cartoon style, force diagrams, vibrant orange and blue color palette, clean lines, soft cel shading,",
        "suffix": "educational scientific illustration, physically accurate, no text, no labels, white background, vector-like art, colorful arrows and fields",
        "negative": "text, words, letters, labels, watermark, signature, photorealistic, blurry, dark, inaccurate physics",
        "guidance_scale": 1.5,
        "num_inference_steps": 4,
    },
    "astronomy": {
        "prefix": "scientifically accurate space illustration, clean cartoon style, deep navy and cosmic purple palette, glowing celestial objects, soft shading,",
        "suffix": "educational astronomical illustration, scale-accurate, no text, no labels, clean vector-like art, vivid nebula colors, accurate star fields",
        "negative": "text, words, letters, labels, watermark, signature, photorealistic photo, blurry, alien faces, sci-fi fantasy, inaccurate orbits",
        "guidance_scale": 1.5,
        "num_inference_steps": 4,
    },
    "anatomy": {
        "prefix": "scientifically accurate human anatomy illustration, clean cartoon style, warm coral and soft red palette, medical-grade accuracy, cross-section view, soft cel shading,",
        "suffix": "educational medical illustration, anatomically precise, no text, no labels, white background, clean vector-like art, friendly colorful organs",
        "negative": "text, words, letters, labels, watermark, signature, photorealistic, blurry, gore, scary, dark, inaccurate anatomy",
        "guidance_scale": 1.5,
        "num_inference_steps": 4,
    },
    "geology": {
        "prefix": "scientifically accurate geological illustration, clean cartoon style, earthy brown and amber color palette, rock layer cross-sections, soft shading,",
        "suffix": "educational geology illustration, stratigraphically accurate, no text, no labels, white background, clean vector-like art, colorful mineral layers",
        "negative": "text, words, letters, labels, watermark, signature, photorealistic, blurry, dark, fantasy landscape",
        "guidance_scale": 1.5,
        "num_inference_steps": 4,
    },
    "ecology": {
        "prefix": "scientifically accurate ecosystem illustration, clean cartoon style, lush green and sky blue palette, food web diagram, habitat cross-section, soft cel shading,",
        "suffix": "educational ecology illustration, species-accurate, no text, no labels, white background, clean vector-like art, vibrant natural colors",
        "negative": "text, words, letters, labels, watermark, signature, photorealistic, blurry, dark, anthropomorphic, cartoon faces on animals",
        "guidance_scale": 1.5,
        "num_inference_steps": 4,
    },
    "mathematics": {
        "prefix": "clean geometric illustration, cartoonish yet precise, vibrant mint and coral color palette, 3D shapes, mathematical curves, soft shading,",
        "suffix": "educational math visualization, geometrically precise, no text, no labels, white background, clean vector-like art, colorful gradients on surfaces",
        "negative": "text, words, letters, numbers, equations, labels, watermark, signature, photorealistic, blurry, dark, messy",
        "guidance_scale": 1.5,
        "num_inference_steps": 4,
    },
    "electronics": {
        "prefix": "scientifically accurate electronics illustration, clean cartoon style, teal and yellow circuit color palette, component diagrams, soft shading,",
        "suffix": "educational electronics illustration, accurate circuit components, no text, no labels, white background, clean vector-like art, colorful wires and chips",
        "negative": "text, words, letters, labels, watermark, signature, photorealistic, blurry, dark, tangled, messy",
        "guidance_scale": 1.5,
        "num_inference_steps": 4,
    },
    "microscopy": {
        "prefix": "scientifically accurate microscope view illustration, clean cartoon style, neon magenta and cyan staining palette, cellular structures, soft glowing edges,",
        "suffix": "educational microscopy illustration, biologically accurate cell structures, no text, no labels, dark field background, clean vector-like art, fluorescence-inspired colors",
        "negative": "text, words, letters, labels, watermark, signature, photorealistic photo, blurry, inaccurate organelles, messy",
        "guidance_scale": 1.5,
        "num_inference_steps": 4,
    },
    "raw": {
        "prefix": "scientifically accurate illustration, clean cartoon style, educational,",
        "suffix": "no text, no labels, white background, clean vector-like art, colorful, scientifically precise",
        "negative": "text, words, letters, labels, watermark, signature, blurry, dark, inaccurate, low quality",
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
