# Acceptance criteria — Provenance Guard

Five criteria that say what "working" means for this service, written in unit 7
**before** you built it.

**All five are yours.** None are given.

An acceptance criterion names a number or something plainly observable. *"The
detector is accurate"* is an opinion — and perfect AI detection isn't possible
anyway, so it's an opinion about something nobody can deliver. *"Of 10 pieces I
wrote myself, at most 1 is labelled high-confidence AI"* is a criterion.

Under each, write a sentence or two on **why that target**. *"I allow at most 1
false positive in 10 because on a writing site a wrong accusation costs more
than a missed detection"* is a real answer.

> Missing your own targets next unit costs you nothing. Setting a target so
> easy you can't miss it does.

---

## Pick numbers you can defend

**Cover at least three of these five areas.** They're prompts, not a form.

| Area | A question it could answer |
|---|---|
| False positives | How often may a human's writing get called AI? |
| Score spread | How far apart should clearly-AI and clearly-human text score? |
| Label coverage | Is every one of your three labels actually reachable? |
| The appeal path | Does an appeal always change status and always get recorded? |
| Bad input | What happens when `text` is missing, empty, or enormous? |

Two things worth knowing before you pick numbers:

- **The expensive mistake is one-sided.** Missing some AI text costs the site a
  little. Accusing a real writer costs that person a lot. A criterion that
  treats both errors as equally bad is describing a system nobody would ship.
- **Unit 8 tests across three trials, and the target has to hold across all
  three.** Your first signal runs a model, so identical input can score
  differently twice. A target of "at most 1 in 10" against trials of 2, 1, 2 is
  a **miss**.

---
## 1. False positives

<!-- Your criterion. It must name a number. -->

At most 1 of 10 human samples should receive the high confidence AI label.

**Why this target:** A false accusation could hurt a real writer, so I want the system to be cautious about labeling something as AI-generated. I'm allowing a small margin for error since the signals aren't perfect.

---

## 2. Score Seperation

<!-- Your criterion. -->

Across 5 AI generated and 5 human samples, the average combined AI score should be at least 0.20 higher for the AI samples.

**Why this target:** The two signals should be able to distinguish between different types of writing. A 0.20 gap would show some meaningful separation without expecting perfect detection.

---

## 3. Label Coverage

<!-- Your criterion. -->

All three labels (`human`, `unsure`, and `ai`) should each be produced by at least one test input.

**Why this target:** Every label needs to actually work, especially `unsure`, since the system should have an option when it can't make a confident decision.

---

## 4. Appreal reliability

<!-- Your criterion. -->

All 5 valid appeals should return a confirmation, update the submission's status to `under_review`, and create a matching entry in the audit log.

**Why this target:** Writers need a reliable way to challenge incorrect decisions. Since false positives can affect someone's reputation, appeals should never be silently lost.

---

## 5. Invalid input handling

<!-- Your criterion. -->

All 5 invalid submissions (missing `text`, empty text, whitespace-only text, non-string text, and text over 10,000 characters) should return HTTP `400` with a JSON error message instead of crashing.

**Why this target:** The service shouldn't produce unreliable results from invalid input. Limiting text length also matters because the model only processes a fixed number of tokens.

---

<!-- ─────────────────────────────────────────────────────────────────────────
     UNIT 8 — read this before you change anything above.

     If a criterion turns out to be BROKEN rather than merely unmet, you can
     revise it, and that earns credit. But never delete or edit the original
     line. Add the revision underneath, like this:

         ## 2. Uncertain cases land in the unsure band

         The system handles uncertain cases well.

         **Why this target:** ...

         > **Revised in unit 8:** Text I judged borderline scores between
         > 0.4 and 0.6 in at least 4 of 5 cases.
         >
         > **Why revised:** "well" gave me nothing to check. I couldn't
         > reach a verdict from it at all.

     That's a revision because the criterion couldn't be MEASURED.

     Lowering a target because you missed it is not a revision, and it costs
     you the point:

         ✗ "At most 1 of 10 of my own pieces flagged as AI" → "at most 3
            of 10", because 1 of 10 turned out to be hard.

     A number you missed stays where it is, gets diagnosed, and gets a fix
     attempted. That's where the points are.
     ───────────────────────────────────────────────────────────────────────── -->

## Capstone

### 1. Malformed Input Rejection

All 8 invalid submissions (punctuation-only text, emoji-only text, numbers-only text, invalid control characters, repetitive characters, repetitive words, empty text, and whitespace-only text) should return HTTP `400` with a JSON error message.

**Why this target:** The detector should only analyze text that is suitable for analysis. Returning a detection result for malformed text could mislead users and produce meaningless scores.

### 2. Unnecessary Detector Execution

The detector should not be called for any of the 8 invalid submissions, as indicated by the `detector_called` field in the request log.

**Why this target:** Running the local model uses computing resources. Invalid submissions should be rejected before reaching the model, rather than wasting resources analyzing unsuitable text.

### 3. Structured Logging

All 11 submissions in each trial should have a matching structured request log entry containing a timestamp, request ID, input, output, HTTP status code, duration, CPU time, and whether the detector was called.

**Why this target:** I want to be able to trace every submission, including rejected ones. Missing log entries would make it harder to identify failures and understand how the system is behaving.

### 4. Invalid Input Rejection Latency

At least 7 of the 8 invalid submissions should return HTTP `400` in under 100 milliseconds, measured using the server-side request duration after the model has been warmed up.

**Why this target:** Input validation is much less computationally expensive than running the detector, so invalid submissions should be rejected quickly. I'm allowing one exception to account for occasional variations in execution time.

### 5. Valid Input Handling

All 3 valid writing samples (plain text, text containing emojis, and multiline text) should return HTTP `200` with a content ID, guess, confidence, label, model score, and style score.

**Why this target:** I don't want stricter input validation to prevent legitimate writers from submitting their work. The extension should improve how invalid submissions are handled without breaking the original detection process.