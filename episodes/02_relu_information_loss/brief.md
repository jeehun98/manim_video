Create a portrait-format Manim Shorts video as the next episode in an “Activation Function Series”.

Topic:
ReLU and input-dependent information removal.

Target duration:
35–45 seconds.

Target audience:
Beginners who already know the basic ReLU rule:

f(x) = max(0, x)

Main message:
The rule of ReLU is fixed, but the actual effect of ReLU depends on the input data.

How many values disappear, and how large that removed portion is, depends on the size and distribution of the input values.

Do not focus on invertibility in this video.

Do not introduce entropy or mutual information yet.

The lesson should build from simple counting to a more subtle question:

“Is counting how many values become zero enough to measure information loss?”

This question should become the hook for the next video.

---

## Scene 1 — Same ReLU, different inputs

Start with the ReLU rule already known from the previous video:

f(x) = max(0, x)

Show a short caption:

“Same rule.”

Then introduce three different column vectors side by side or sequentially.

A:

[1, 2, 3, 4]^T

B:

[-1, 2, -3, 4]^T

C:

[-1, -2, -3, 1]^T

Apply exactly the same ReLU transformation to each vector.

A becomes:

[1, 2, 3, 4]^T

B becomes:

[0, 2, 0, 4]^T

C becomes:

[0, 0, 0, 1]^T

Animate the transformation element by element.

Use consistent colors so input and output elements can be tracked.

The important visual idea:

ReLU itself did not change.

Only the input changed.

Suggested narration:

“ReLU always follows the same rule.”

“But its effect can look very different depending on the input.”

---

## Scene 2 — Count how much was suppressed

Place the three transformed vectors in a clean comparison layout.

For each vector, count the number of negative values that became zero.

Show:

A:
0 / 4 removed
0%

B:
2 / 4 removed
50%

C:
3 / 4 removed
75%

Animate the percentages appearing from the vector entries themselves.

For example:
highlight each suppressed element,
then move or transform the highlight into the fraction and percentage.

Introduce a simple quantity:

Zeroed Ratio

number of values mapped to zero
divided by
total number of values

If mathematical notation is useful, show briefly:

Zeroed Ratio = #{x_i < 0} / N

Keep the notation secondary to the visual explanation.

Suggested narration:

“The simplest way to measure ReLU’s effect is to count how many values were suppressed.”

“In these examples, the same ReLU removes zero percent, fifty percent, and seventy-five percent of the activations.”

---

## Scene 3 — Move from vectors to distributions

Transition from individual vectors to simple activation distributions.

Show three stylized distributions centered differently relative to zero.

Distribution A:
mostly positive values

Distribution B:
roughly balanced around zero

Distribution C:
mostly negative values

Use a vertical line at x = 0.

The negative side should be visually distinct from the positive side.

Then apply ReLU conceptually.

Animate the entire negative side collapsing toward zero.

Keep the positive side unchanged.

Show:

mostly positive
→ small suppressed fraction

balanced
→ roughly half suppressed

mostly negative
→ large suppressed fraction

The distributions do not need to represent exact measured datasets.

They can be illustrative mathematical examples.

Suggested narration:

“The same idea applies to a whole distribution.”

“If most activations are positive, ReLU changes very little.”

“If many activations are negative, much more of the data is collapsed to zero.”

---

## Scene 4 — The effect can be predicted from the input distribution

Keep the zero threshold visible.

Highlight the area of the distribution where:

x < 0

Introduce:

P(X < 0)

Explain visually that this quantity tells us the expected fraction of values that ReLU will suppress.

Show an illustrative zero-centered symmetric distribution.

Divide it at x = 0.

Show approximately half of the distribution on each side.

Display:

P(X < 0) ≈ 0.5

Then shift the distribution to the right.

The negative area becomes smaller.

Then shift it to the left.

The negative area becomes larger.

Suggested narration:

“If we know the distribution before ReLU, we can estimate how many activations will become zero.”

“For a symmetric distribution centered around zero, that can be roughly half.”

“Shift the distribution, and the suppressed fraction changes with it.”

Do not present this as a universal assumption about neural-network activations.

Make it clear that this is an illustrative example.

---

## Scene 5 — But counting values is not the whole story

Return briefly to two small vectors.

Example:

A = [-0.01, -0.02, 3, 4]

B = [-10, -20, 3, 4]

After ReLU, both become:

[0, 0, 3, 4]

Now show:

Both:
2 / 4 removed
50%

Pause.

Highlight the removed values before ReLU:

A removed:
-0.01, -0.02

B removed:
-10, -20

Show that the Zeroed Ratio is identical.

But visually emphasize that the magnitudes of the removed values are dramatically different.

Suggested narration:

“But there is a problem.”

“These two inputs lose the same number of values.”

“Both have a fifty-percent zeroed ratio.”

“But did they really lose the same amount of information?”

Do not answer the question fully in this video.

---

## Scene 6 — Hook for the next episode

Place the two examples side by side.

Show:

Same zeroed ratio.

Different removed magnitude.

Then introduce the next question:

“How much of the input itself was removed?”

or:

“Should the size of the removed values matter?”

Optionally show the structure of a future metric without fully explaining it:

removed magnitude
——————————
total magnitude

or briefly preview:

Σ removed x_i²
──────────────
Σ all x_i²

Do not explain this formula yet.

It should appear as a visual teaser only.

End with:

“Counting zeros tells us how many activations disappeared.”

“But next, we’ll ask how much of the input was actually lost.”

Final title card:

ReLU — Information Loss #1

Next:
How much was removed?

---

## Visual style

Maintain the visual identity of the previous ReLU Short:

* portrait 1080 × 1920
* dark background
* minimal text
* clean mathematical visualization
* smooth transitions
* consistent accent colors
* colored vector elements that remain trackable
* avoid disconnected slide-like cuts
* reuse vector → graph/distribution transformations where possible

Prefer animation over explanation.

The viewer should first see the difference before the narration names it.

Use:

* Transform
* ReplacementTransform
* TransformFromCopy
* FadeIn
* FadeOut
* Indicate
* Create
* LaggedStart
* ValueTracker if useful for shifting distributions

Avoid:

* long paragraphs
* formal proofs
* excessive terminology
* detailed information-theory definitions

---

## Mathematical accuracy requirements

Preserve the distinction between:

1. fraction of activations mapped to zero
2. actual information loss

Do not claim that Zeroed Ratio directly equals information loss.

Describe it as a simple first indicator of how strongly ReLU suppresses a given input.

Make clear that ReLU’s mathematical rule is fixed:

f(x) = max(0, x)

but its observed effect depends on the input values and their distribution.

When discussing a symmetric zero-centered distribution, say that approximately half of values are negative only for that illustrative symmetric case.

Do not imply that all neural-network activations follow this distribution.

The ending should intentionally leave open the deeper question:

“If two inputs lose the same number of values but those values have very different magnitudes, did ReLU remove the same amount of information?”
