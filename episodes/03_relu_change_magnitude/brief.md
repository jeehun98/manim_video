Create a portrait-format Manim Shorts video as the next episode in the ReLU / Activation Function series.

Target duration:
30–40 seconds.

Main concept:
In the previous video, ReLU’s effect was measured by counting how many values became zero.

Now shift the perspective.

Instead of asking only:

“How many values changed?”

ask:

“How large was the change in the data itself?”

The entire video should focus on this transition from count-based measurement to magnitude-based measurement.

Do not focus on entropy, mutual information, invertibility, or formal information theory.

Do not overcomplicate the math.

The core idea should be visually obvious before any formula is introduced.

---

## Scene 1 — Recall the previous metric

Begin with a short callback to the previous episode.

Show a column vector such as:

x = [-0.1, -0.2, 3, 4]^T

Apply ReLU:

ReLU(x) = [0, 0, 3, 4]^T

Highlight the two values that became zero.

Show:

2 / 4 changed

Zeroed Ratio = 50%

Suggested narration:

“Previously, we measured ReLU’s change by counting how many values became zero.”

Keep this recap very short.

---

## Scene 2 — Same count, different amount of change

Now introduce another vector:

y = [-10, -20, 3, 4]^T

Apply ReLU:

ReLU(y) = [0, 0, 3, 4]^T

Again show:

2 / 4 changed

Zeroed Ratio = 50%

Place both examples side by side.

Make the identical 50% labels visually clear.

Then pause.

Highlight the original negative values:

First vector:
-0.1, -0.2

Second vector:
-10, -20

Suggested narration:

“But these two transformations do not feel equally large.”

“Both changed the same number of values…”

“…but the values that changed were very different in size.”

---

## Scene 3 — Change the visual representation

Transform the scalar entries into magnitude bars.

For the first vector, show very short bars for:

0.1
0.2

and larger bars for:

3
4

For the second vector, show much larger bars for:

10
20

and smaller retained bars for:

3
4

Then apply ReLU visually.

The negative bars should disappear.

The first example should lose only a small amount of total visual size.

The second example should lose a much larger amount.

The key visual message:

same count of changed elements

different size of change

Show a short on-screen contrast:

“How many changed?”
vs
“How much changed?”

Suggested narration:

“So counting changed elements tells us how often ReLU acted.”

“But it does not tell us how large the actual change was.”

---

## Scene 4 — Measure the size of the change

Introduce the idea of measuring the difference between the input and output vectors.

Show:

input
→
ReLU
→
output

Then visually isolate the difference:

Δx = x - ReLU(x)

For example:

## [-0.1, -0.2, 3, 4]

[0, 0, 3, 4]

becomes:

[-0.1, -0.2, 0, 0]

For the second vector:

## [-10, -20, 3, 4]

[0, 0, 3, 4]

becomes:

[-10, -20, 0, 0]

Do not make the algebra the main point.

The important idea is:

the removed part can itself be treated as a vector.

Suggested narration:

“If we subtract the output from the input, we can directly see what ReLU removed.”

---

## Scene 5 — Compare the size of the removed vectors

Show the two removed parts side by side:

A_removed = [-0.1, -0.2, 0, 0]

B_removed = [-10, -20, 0, 0]

Convert them into magnitude bars or simple vector-length indicators.

Show visually:

A_removed → small

B_removed → large

Then introduce a simple measurement:

“size of removed part”

Optionally show:

||x - ReLU(x)||

Do not explain norm theory in detail.

If useful, briefly mention:

“one way is to measure the length of this difference vector.”

Suggested narration:

“Now the difference becomes measurable.”

“Instead of only counting changed values, we can measure the size of the removed part itself.”

---

## Scene 6 — Core comparison

Create a clean summary:

Example A

Changed values:
50%

Change size:
small

Example B

Changed values:
50%

Change size:
large

Then show:

Same change ratio
≠
Same change magnitude

Suggested narration:

“The ratio tells us how many values changed.”

“The magnitude tells us how much the data changed.”

---

## Scene 7 — Closing hook

Show the progression:

Count
→
Ratio
→
Magnitude

Then ask:

“If the removed part is large, does that always mean more information was lost?”

Do not answer yet.

End with:

“Next: change magnitude and information loss.”

or:

“Next: does a larger change mean more information is lost?”

---

## Visual style

Maintain continuity with the previous ReLU videos:

* portrait 1080 × 1920
* dark background
* minimal text
* same color palette
* smooth transformations
* vector values should transform into bars rather than disappearing and being recreated
* use strong visual correspondence between input, output, and removed part
* avoid disconnected slides

Useful Manim techniques:

* Transform
* ReplacementTransform
* TransformFromCopy
* VGroup
* Brace
* Rectangle
* Indicate
* FadeIn
* FadeOut
* LaggedStart

The visual language should emphasize:

input
→ output
→ difference

Then:

difference
→ magnitude

---

## Mathematical framing

The previous metric was count-based:

Zeroed Ratio

This video introduces a magnitude-based view:

how large is

x - ReLU(x)

Do not claim that the magnitude of this difference is itself the full definition of information loss.

Present it as:

“a better measure of how strongly ReLU changed this particular input.”

Possible compact notation:

Δx = x - ReLU(x)

Change Magnitude = ||Δx||

Use the formula only after the visual meaning has already been established.

The central message should be:

Two inputs can have the same percentage of changed elements, while the actual size of the change can be very different.
