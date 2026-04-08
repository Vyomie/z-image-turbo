STYLES: dict[str, dict] = {
    "biology": {
        "prefix": "simple flat 2D scientific diagram, top view or side view, biology textbook style, minimal detail, clean outlines, vibrant green and teal color palette, flat colors,",
        "suffix": "simple 2D diagram, flat illustration, white background, no shading, no gradients, no perspective, scientifically accurate, no text, no labels, no watermarks",
        "negative": "3D, perspective, depth, shading, shadows, gradients, realistic, photorealistic, complex, cluttered, text, words, letters, labels, watermark, blurry, dark",
        "guidance_scale": 1.5,
        "num_inference_steps": 4,
    },
    "chemistry": {
        "prefix": "simple flat 2D scientific diagram, top view, chemistry textbook style, minimal detail, clean outlines, vibrant blue and purple color palette, flat colors, ball-and-stick model,",
        "suffix": "simple 2D diagram, flat illustration, white background, no shading, no gradients, no perspective, correct molecular geometry, no text, no labels",
        "negative": "3D, perspective, depth, shading, shadows, gradients, realistic, photorealistic, complex, cluttered, text, words, letters, labels, watermark, blurry, dark",
        "guidance_scale": 1.5,
        "num_inference_steps": 4,
    },
    "physics": {
        "prefix": "simple flat 2D scientific diagram, side view, physics textbook style, minimal detail, clean outlines, vibrant orange and blue color palette, flat colors, arrows for forces,",
        "suffix": "simple 2D diagram, flat illustration, white background, no shading, no gradients, no perspective, physically accurate, no text, no labels",
        "negative": "3D, perspective, depth, shading, shadows, gradients, realistic, photorealistic, complex, cluttered, text, words, letters, labels, watermark, blurry, dark",
        "guidance_scale": 1.5,
        "num_inference_steps": 4,
    },
    "astronomy": {
        "prefix": "simple flat 2D scientific diagram, top view, astronomy textbook style, minimal detail, clean outlines, deep navy and purple color palette, flat colors, orbital paths,",
        "suffix": "simple 2D diagram, flat illustration, dark background, no shading, no gradients, no perspective, scale-accurate, no text, no labels",
        "negative": "3D, perspective, depth, shading, shadows, gradients, realistic, photorealistic, complex, cluttered, text, words, letters, labels, watermark, blurry, lens flare",
        "guidance_scale": 1.5,
        "num_inference_steps": 4,
    },
    "anatomy": {
        "prefix": "simple flat 2D scientific diagram, front view or side view, medical textbook style, minimal detail, clean outlines, warm coral and red color palette, flat colors, cross-section,",
        "suffix": "simple 2D diagram, flat illustration, white background, no shading, no gradients, no perspective, anatomically accurate, no text, no labels",
        "negative": "3D, perspective, depth, shading, shadows, gradients, realistic, photorealistic, complex, cluttered, text, words, letters, labels, watermark, blurry, gore, scary",
        "guidance_scale": 1.5,
        "num_inference_steps": 4,
    },
    "geology": {
        "prefix": "simple flat 2D scientific diagram, side view cross-section, geology textbook style, minimal detail, clean outlines, earthy brown and amber color palette, flat colors, layer stratigraphy,",
        "suffix": "simple 2D diagram, flat illustration, white background, no shading, no gradients, no perspective, stratigraphically accurate, no text, no labels",
        "negative": "3D, perspective, depth, shading, shadows, gradients, realistic, photorealistic, complex, cluttered, text, words, letters, labels, watermark, blurry, dark",
        "guidance_scale": 1.5,
        "num_inference_steps": 4,
    },
    "ecology": {
        "prefix": "simple flat 2D scientific diagram, side view, ecology textbook style, minimal detail, clean outlines, lush green and sky blue color palette, flat colors, food web arrows,",
        "suffix": "simple 2D diagram, flat illustration, white background, no shading, no gradients, no perspective, species-accurate, no text, no labels",
        "negative": "3D, perspective, depth, shading, shadows, gradients, realistic, photorealistic, complex, cluttered, text, words, letters, labels, watermark, blurry, cartoon faces on animals",
        "guidance_scale": 1.5,
        "num_inference_steps": 4,
    },
    "mathematics": {
        "prefix": "simple flat 2D scientific diagram, top view, math textbook style, minimal detail, clean outlines, vibrant mint and coral color palette, flat colors, geometric shapes,",
        "suffix": "simple 2D diagram, flat illustration, white background, no shading, no gradients, no perspective, geometrically precise, no text, no labels, no numbers",
        "negative": "3D, perspective, depth, shading, shadows, gradients, realistic, photorealistic, complex, cluttered, text, words, letters, numbers, equations, labels, watermark, blurry",
        "guidance_scale": 1.5,
        "num_inference_steps": 4,
    },
    "electronics": {
        "prefix": "simple flat 2D scientific diagram, top view, electronics textbook style, minimal detail, clean outlines, teal and yellow color palette, flat colors, circuit schematic,",
        "suffix": "simple 2D diagram, flat illustration, white background, no shading, no gradients, no perspective, accurate circuit components, no text, no labels",
        "negative": "3D, perspective, depth, shading, shadows, gradients, realistic, photorealistic, complex, cluttered, text, words, letters, labels, watermark, blurry, tangled",
        "guidance_scale": 1.5,
        "num_inference_steps": 4,
    },
    "microscopy": {
        "prefix": "simple flat 2D scientific diagram, top view, microscopy textbook style, minimal detail, clean outlines, neon magenta and cyan color palette, flat colors, cellular structures,",
        "suffix": "simple 2D diagram, flat illustration, dark background, no shading, no gradients, no perspective, biologically accurate, no text, no labels",
        "negative": "3D, perspective, depth, shading, shadows, gradients, realistic, photorealistic, complex, cluttered, text, words, letters, labels, watermark, blurry",
        "guidance_scale": 1.5,
        "num_inference_steps": 4,
    },
    "default": {
        "prefix": "simple flat 2D scientific diagram, top view or side view, textbook style, minimal detail, clean outlines, vibrant multicolor palette, flat colors,",
        "suffix": "simple 2D diagram, flat illustration, white background, no shading, no gradients, no perspective, scientifically accurate, no text, no labels, no watermarks",
        "negative": "3D, perspective, depth, shading, shadows, gradients, realistic, photorealistic, complex, cluttered, text, words, letters, numbers, labels, watermark, blurry, dark",
        "guidance_scale": 1.5,
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
