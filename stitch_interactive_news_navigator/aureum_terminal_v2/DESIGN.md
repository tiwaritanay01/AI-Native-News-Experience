# Design System Specification: High-Density Financial Intelligence

## 1. Overview & Creative North Star: "The Sovereign Analyst"
The Creative North Star for this system is **"The Sovereign Analyst."** It rejects the playful, airy "SaaS" aesthetics of the last decade in favor of a high-authority, editorial-grade financial environment. It is built for power users who demand maximum information density without sacrificing the prestige of a luxury brand.

By blending the cold, mathematical precision of a **Bloomberg Terminal** with the high-end typographic soul of a **Financial Times** editorial, we create a "Technical-Luxury" hybrid. We break the standard "template" look through intentional asymmetry: expansive, serif-driven headers contrasted against hyper-dense, monospaced data grids. This is a workspace that feels like a private terminal in a high-rise executive suite—authoritative, dense, and uncompromisingly professional.

---

## 2. Colors & Tonal Depth
The palette is rooted in the depth of absolute darkness, punctuated by the high-vis brilliance of market indicators and the warmth of precious metal.

### Palette Strategy
*   **Base:** `surface` (#131313) and `surface_container_lowest` (#0E0E0E) provide a void-like depth, allowing data to "glow."
*   **Primary (Gold):** `primary` (#F2CA50) and `primary_container` (#D4AF37) are used for high-value highlights and brand-defining accents.
*   **Market Sentiment:** `secondary_container` (#13FF41 / Financial Green) and `tertiary_container` (#FF968B / Market Red) are reserved strictly for directional data.

### The "No-Line" Rule
Standard 1px solid borders for sectioning are strictly prohibited. Layouts must be defined through **Background Color Shifts**. To separate a sidebar from a main feed, transition from `surface` to `surface_container_low`. Use the `surface_container` tiers (Lowest to Highest) to create a sense of nested importance.

### The "Glass & Gradient" Rule
For floating modules or overlay panels, use **Glassmorphism**. Apply a `surface` color with 40-60% opacity and a `20px` to `40px` backdrop blur. To add "soul," use a subtle linear gradient on primary CTAs—moving from `primary` (#F2CA50) to `primary_container` (#D4AF37)—simulating the directional sheen of brushed gold.

---

## 3. Typography: The Dual-Identity System
We employ a high-contrast typographic pairing to signal both "The News" (Editorial) and "The Numbers" (Technical).

*   **Display & Headlines (Newsreader Serif):** Use for page titles and high-level section headers (`headline-lg` to `display-lg`). This brings an authoritative, "New York Times" sophistication to the terminal, humanizing the cold data.
*   **Data & Labels (Space Grotesk/Mono):** All quantitative data, tickers, and UI labels use `spaceGrotesk`. For raw data tables, prioritize a monospaced variant to ensure digits align vertically for rapid ocular scanning.
*   **Hierarchy Note:** Use `label-sm` (0.6875rem) for secondary metadata. High density doesn't mean "unreadable"—it means utilizing smaller font sizes with generous letter-spacing (0.05rem) to maintain legibility.

---

## 4. Elevation & Depth
Depth in this system is achieved through **Tonal Layering** rather than structural scaffolding.

*   **The Layering Principle:** Stack `surface-container` tiers. A `surface-container-highest` card should sit atop a `surface-container-low` section. This creates a soft, natural "lift" that mimics physical material without the clutter of shadows.
*   **The Ghost Border Fallback:** If a container requires definition against a similar background, use a **Ghost Border**. This is a 1px stroke using `outline_variant` at 20% opacity. 
*   **Signature Glow:** For active states or "Profit" indicators, replace shadows with a subtle outer glow using `on_secondary_container` at 10% opacity to simulate the luminescence of a high-end monitor.

---

## 5. Components & High-Density Patterns

### Buttons
*   **Primary:** Solid `primary_container` (#D4AF37) with `on_primary` (#3C2F00) text. Sharp 0px corners.
*   **Tertiary (Ghost):** No background, `primary` text, and a 1px `outline_variant` border at 20% opacity.
*   **Density:** Use `spacing.2` (0.3rem) for vertical padding and `spacing.4` (0.75rem) for horizontal padding.

### Data Tables (The Core Component)
*   **Forbid Dividers:** Do not use horizontal lines between rows. Use alternating row fills (`surface` vs `surface_container_low`) or simply vertical white space (`spacing.2`).
*   **Typography:** All values in `body-sm` (Space Grotesk).
*   **Alignment:** Numbers must be right-aligned; labels must be left-aligned. Use `secondary_fixed_dim` (#00E639) for positive percentage changes and `tertiary_fixed_dim` (#FFB4AB) for negative.

### Glass Tickers
*   **Structure:** Floating 1px gold-tinted (`outline_variant` at 15%) borders with a heavy backdrop blur.
*   **Animation:** Tickers should move with a slow, cinematic ease-out, rather than a linear crawl, to maintain the premium feel.

### Input Fields
*   **Style:** Minimalist. Only a bottom border (1px `outline_variant`). When focused, the border transitions to `primary` (#F2CA50) with a subtle `2px` glow.
*   **Density:** Labels use `label-sm` and are placed *inside* the input area to save vertical pixels.

---

## 6. Do's and Don'ts

### Do
*   **Do** prioritize information density. Professional users prefer seeing 50 rows of data at once over 10 rows with "breathing room."
*   **Do** use 0px border radii. This is a system of precision and sharp edges.
*   **Do** use `Newsreader` for narrative elements to break the "machine" feel.

### Don't
*   **Don't** use standard grey shadows. If you need a shadow, tint it with the `primary` or `secondary` hue at 5% opacity.
*   **Don't** use rounded corners (`0px` is the absolute rule).
*   **Don't** use 100% opaque borders to separate sections. Use background color shifts.
*   **Don't** use icons as primary navigation. Always accompany icons with `label-sm` text for professional clarity.