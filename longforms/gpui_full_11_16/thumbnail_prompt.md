# GPU 개론3부 썸네일

Mode: built-in image_gen (generation followed by targeted edit).

## Initial prompt

Use case: scientific-educational / ads-marketing. Create a finished Korean YouTube thumbnail for GPU Architecture Part 3, landscape 16:9, high resolution. Match the visual character of an elegant dark navy scientific lecture cover: deep ink-blue background with a subtle evenly spaced cyan blueprint grid, very clean flat fine-line diagrams, lots of intentional negative space, restrained pale cyan and white with tiny warm-yellow accents. No photographs, no 3D processors, no dramatic glow, no clutter.

Composition: left 46% is beautiful large Korean typography with generous left margins; right 50% contains a coherent small collection of computer architecture diagrams. Clearly readable at thumbnail size. Strong editorial hierarchy, precise crisp Korean sans-serif type.

Exact left text:
small widely tracked pale-cyan English overline: "GPU ARCHITECTURE"
large bold white first title line: "하나의 명령어에서"
large bold pale-cyan second title line: "병렬 실행까지"
smaller white subtitle: "메모리 · 파이프라인 · 다중 실행 유닛"
small warm-yellow footer: "GPU 개론 3부"

Right-side diagrams should visually explain the progression to parallel execution, rather than just contain labels:
At upper right, a compact memory array drawn with thin white/cyan lines, three cells containing 5, 3, 8, linked with a small understated arrow to an arithmetic circuit.
In middle right, the clearest main motif: a neat pipeline timing diagram, column headers F D E M W, three staggered rows of tiny outlined stage rectangles with cyan, lavender, and pale cyan highlights progressing diagonally. Clearly depict several instructions overlapping in different stages. Small label "Pipeline" is sufficient; avoid any dense text.
At lower right, a tasteful thin-line register-file bank on the left feeding two parallel small geometric ALU circuit symbols on the right through separate input lines. One path cyan with inputs 5 and 3 and result 8, one path lavender with inputs 9 and 2 and result 7. Each ALU is a simple classic notched arithmetic-logic schematic shape with a small + / − glyph inside, NOT a generic large computer-chip icon and NOT giant ALU lettering. Two output lines on the far right carry 8 and 7. A faint green bypass arc near the arithmetic input can subtly suggest forwarding. Small labels only, all mathematics correct (5+3=8, 9−2=7); do not use a false equality or imply the two ALUs are dedicated add/sub hardware.
Keep the right diagrams elegant, airy, and aligned on an invisible grid. The lower dual-execution diagram should be the most visually substantial structure, with the upper memory and pipeline motifs supporting it. No extra prose, equations unrelated to computer architecture, logos, watermark, badges, arrows crossing title, border, or photoreal textures. The overall impression is the same premium navy-grid academic cover style as a quantum mechanics explainer, but entirely about instruction pipelines and multiple execution units.

## Final correction prompt

Edit this thumbnail with exactly two small technical corrections. Preserve all Korean title typography, exact wording, navy grid background, palette, composition, memory box, arithmetic symbols, register-file bank, sizes, positions and all other content.

1. DELETE the entire green curved bypass arrow that runs from the upper arithmetic-unit output toward the lower arithmetic-unit input. There must be no green connection between the two arithmetic units. These are independent computations: upper 5 and 3 make 8; lower 9 and 2 make 7. Keep the cyan and lavender register-file input wires and both output wires exactly intact. No substitute new line.

2. Correct ONLY the Pipeline timing chart, keeping its approximate location and total footprint. It must be a proper THREE-ROW, SEVEN-CLOCK timeline. Replace the top headers F D E M W with the seven cycle numbers "1 2 3 4 5 6 7", evenly spaced over the full chart width. First cyan instruction row: exactly FIVE cells labelled "F D E M W", occupying cycles1–5. Second lavender instruction row: exactly FIVE cells labelled "F D E M W", occupying cycles2–6. Third pale-cyan instruction row: exactly FIVE cells labelled "F D E M W", occupying cycles3–7. Thus each row has five stages and is shifted right one clock compared with the row above. There must be NO duplicated E, NO six-cell row and NO sixth stage. Keep the chart clean and the existing "Pipeline" label.

No changes anywhere else.

