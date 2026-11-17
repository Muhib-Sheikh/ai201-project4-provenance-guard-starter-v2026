# Provenance Guard

> ### 👋 Start here
>
> **New to this repo? Read [RUNNING.md](RUNNING.md) first.**
>
> Once `python test.py` passes, in one terminal:
>
> ```bash
> python app.py
> ```
>
> and in another:
>
> ```bash
> curl -X POST http://127.0.0.1:5000/ping \
>   -H "Content-Type: application/json" \
>   -d '{"message": "hello"}'
> ```
>
> That's a web service. Something sent it text and it sent something back.
> Everything this unit is filling in the middle.
>
> **The rest of this file is your submission.** Fill it in as you go.

---

<!-- ─────────────────────────────────────────────────────────────────────────
     Unit 7 asks for the first five sections. Unit 8 adds the five below.

     Everything is pasted as TEXT. A pasted curl response gets full credit;
     a picture of your terminal gets none.
     ───────────────────────────────────────────────────────────────────────── -->

<!-- ═══════════════════════ UNIT 7 — THE BUILD ═══════════════════════ -->

## What This Does

<!-- The path a submission takes, from arriving to the label a reader sees.
     Six or seven steps — this is the trace you wrote in Milestone 1. -->

Provenance Guard is a backend service that checks whether submitted writing might be AI-generated. It uses two different signals to produce a score and label, and lets writers appeal decisions they disagree with.

### Path

A writer submits their text and creator_id through POST /submit.

app.py reads the input and generates a unique content_id.

detector.py uses GPT-2 to measure how predictable the text is and returns a model score.

stylometry.py measures writing patterns like sentence length, word variety, and punctuation to produce a style score.

scoring.py::combine_signals combines both scores into one AI-likelihood score.

scoring.py::score_to_label turns that score into a label: likely human, unsure, or likely AI.

The result is saved in the audit log and returned as JSON for the website to display.

### False Positive Example

A real writer submits their own work, but the system gives it a combined score of 0.85 and labels it as likely AI-generated. The writer can submit an appeal through POST /appeal with their content_id and an explanation. The system records the appeal and changes the status to under_review.

### Endpoint Shapes

POST /submit

Input:

- text (string): The submitted writing.
- creator_id (string): The writer's identifier.

Output:

- content_id (string): Unique submission ID.
- guess (string): human, ai, or unsure.
- confidence (float): Combined score from 0 to 1.
- label (string): The label shown to readers.
- model_score (float): Score from detector.py.
- style_score (float): Score from stylometry.py.

POST /appeal

Input:

- content_id (string): The submission being appealed.
- reasoning (string): Why the writer disagrees.

Output:

- content_id (string): The appealed submission.
- status (string): under_review.
- message (string): Confirmation that the appeal was recorded.

---

## Signals and Scoring

<!-- For each signal: what property it measures, why that might differ between
     human and AI writing, and WHAT IT CAN'T SEE.

     The blind spot is not optional. If you can't name it you don't understand
     the signal yet — and unit 8's attack set is built out of blind spots. -->

### Signal one — the model signal

**What it measures:** How predictable the text is through perplexity. More predictable text gets a higher AI likelihood score.

**Why that might differ between human and AI writing:** AI generated writing can be more predictable because language models generate text by predicting likely next words.

**What it can't see:** It can't tell who actually wrote the text. Someone writing in simple, predictable sentences could be incorrectly flagged as AI.

### Signal two — the style signal

**What it measures:** Looks at sentence length variation, word variety, and punctuation patterns.

**Why that might differ between human and AI writing:** AI writing can have more consistent sentence structures, while human writing may vary more.

**What it can't see:** It doesn't understand the meaning or authorship of the text. Small changes like typos or different punctuation can affect its score.

### The combining rule

<!-- Write the rule in words, then give the numbers. What happens when the two
     signals disagree? -->

**The rule:** I use a weighted average of both signals. If they disagree, the combined score moves toward the middle instead of relying entirely on one signal.

**The numbers:** 50% model signal and 50% style signal.

**Where it lives:** `scoring.py::combine_signals`

<!-- ⚠️ The grader checks your code against that line. If your rule lives
     somewhere else, say where. -->

**A case where my two signals split, and what my rule does with it:**

A simple, repetitive writing sample had a model score of 0.8342 but a style score of 0.4861. The two signals disagreed, so my 50/50 weighted average brought the combined score down to about 0.6602 instead of relying entirely on the model.

---

## Label Variants

<!-- The exact text of all three labels, as a reader would see them, and the
     score range each covers.

     Write them for someone who has never heard the word "threshold". -->

| Label | Score range | The exact text a reader sees |
|---|---|---|
| high-confidence human | 0.00–0.35 | This text appears to be written by a person. |
| unsure | Above 0.35, below 0.65 | This text shows a mix of human and AI writing patterns, so the result is inconclusive. |
| high-confidence AI | 0.65–1.00 | This text appears to be AI-generated. |

**Why I worded the "unsure" one this way:**
<!-- It's the hardest of the three. It has to admit uncertainty without
     sounding like an accusation, because the person reading it may well have
     written every word themselves. -->

I wanted the label to explain why the system couldn't make a confident decision, without accusing the writer.

---

## Sample Run

<!-- One submission and one appeal, pasted as text: the request, the response,
     and the log entries. -->



**A submission**

<!-- The response needs content_id, guess, confidence, label, AND both
     signal scores - model_score and style_score. Unit 8's tools read those
     two off the response, so leaving them out costs you next unit's
     diagnostics. -->


```bash
curl -X POST http://127.0.0.1:5000/submit \
  -H "Content-Type: application/json" \
  -d '{"text": "Hey whats going on guys. its your boy realog here back with a another warzone video. today i will be showing you guys have to get the secret neutral ground camo. Basically a special delivery drone will spawn at some point during the match. you have to shoot it down, retrieve the camo, and survive for the 3 minute camo, which then unlocks it.", "creator_id": "writer_human"}'
```

```json
{
  "confidence": 0.2776,
  "content_id": "0a4b561e-e408-4033-9000-fc059c6a2ddc",
  "guess": "human",
  "label": "This text appears to be human-written.",
  "model_score": 0.2275,
  "style_score": 0.3276
}
```

**An appeal**

```bash
curl -X POST http://127.0.0.1:5000/appeal \
  -H "Content-Type: application/json" \
  -d '{"content_id": "0a4b561e-e408-4033-9000-fc059c6a2ddc", "reasoning": "I wrote this myself and want the classification reviewed."}'
```

```json
{
  "content_id": "0a4b561e-e408-4033-9000-fc059c6a2ddc",
  "message": "Appeal submitted successfully.",
  "status": "under_review"
}
```

**What the log shows afterwards**

```bash
curl "http://127.0.0.1:5000/log?limit=5"
```

```json
{
  "count": 5,
  "entries": [
    {
      "combined_score": 0.7436,
      "content_id": "b6e3bde4-d846-4119-b314-22f3d24ce0db",
      "creator_id": "writer_001",
      "guess": "unsure",
      "label": "Not evaluated yet.",
      "model_score": 0.8585,
      "status": "decided",
      "style_score": 0.6286,
      "timestamp": "2026-11-17T01:09:03+00:00"
    },
    {
      "combined_score": 0.7436,
      "content_id": "0a07a406-4bac-4757-ae32-f82b4baa5f1c",
      "creator_id": "writer_ai",
      "guess": "ai",
      "label": "This text appears to be AI-generated.",
      "model_score": 0.8585,
      "status": "decided",
      "style_score": 0.6286,
      "timestamp": "2026-11-17T01:32:32+00:00"
    },
    {
      "combined_score": 0.2776,
      "content_id": "0a4b561e-e408-4033-9000-fc059c6a2ddc",
      "creator_id": "writer_human",
      "guess": "human",
      "label": "This text appears to be human-written.",
      "model_score": 0.2275,
      "status": "decided",
      "style_score": 0.3276,
      "timestamp": "2026-11-17T01:32:41+00:00"
    },
    {
      "combined_score": 0.5467,
      "content_id": "dce4610e-6854-4177-9211-1886bf910470",
      "creator_id": "writer_unsure",
      "guess": "unsure",
      "label": "This text shows a mix of human and AI writing patterns, so the result is inconclusive.",
      "model_score": 0.6388,
      "status": "decided",
      "style_score": 0.4546,
      "timestamp": "2026-11-17T01:32:45+00:00"
    },
    {
      "content_id": "0a4b561e-e408-4033-9000-fc059c6a2ddc",
      "creator_id": "writer_human",
      "event": "appeal",
      "reasoning": "I wrote this myself and want the classification reviewed.",
      "status": "under_review",
      "timestamp": "2026-11-17T01:34:43+00:00"
    }
  ]
}

---

## How I Used AI

**Moment 1**

- *What I asked for:*
- *What came back:*
- *What I changed:*

**Moment 2**

- *What I asked for:*
- *What came back:*
- *What I changed:*

<!-- ═══════════════════════ UNIT 8 — THE TEST ═══════════════════════ -->

---

## Rate Limiting

**My limits:** ___ per minute, ___ per day

**Why those numbers and not others:**
<!-- Think about two people: a real writer submitting their own work a few
     times an hour, and a script sending a thousand variations to map your
     thresholds. Your numbers have to be liveable for the first and hostile to
     the second. -->

**What a caller counts as:** <!-- per address, or per creator_id? They fail
differently — one script can look like a thousand callers, and one household
can look like one. -->

**The run of status codes when I pushed past it:**

<!-- python run_attacks.py --flood 15 -->

```

```

---

## Attack Run — Before

<!-- Every attack with its outcome and a held-or-broke mark.
     `run_attacks.py --label before` produces the table. -->



**Ten audit log entries from the run**

<!-- Choose entries that show the interesting failures, not the ten easiest. -->

```json

```

**The single worst outcome** — the one I'd least want to explain to a writer
whose work got caught by it:



---

## Run Log and Verdicts

<!-- Your five criteria across three trials. `run_eval.py --label before`. -->

| Criterion | Target | Run 1 | Run 2 | Run 3 | Verdict |
|---|---|---|---|---|---|
| 1.  |  |  |  |  |  |
| 2.  |  |  |  |  |  |
| 3.  |  |  |  |  |  |
| 4.  |  |  |  |  |  |
| 5.  |  |  |  |  |  |

**Real output from one trial**, pasted as text, naming the file and function
that produced it:

```json

```

**Diagnoses**

<!-- For each miss AND each broken attack: the stage and the mechanism.

     Your service has five stages: the route, signal one, signal two, the
     combining rule, and the label mapping.

     Not a diagnosis:  "The evasion attacks got through."
     A diagnosis:      "Four evasion inputs got through. All four had typos
                        added to AI-generated text. My second signal measures
                        word variety, and typos raise word variety — so it read
                        them as more human. My combining rule weights that
                        signal at 0.6, so it dragged the whole score down."

     Look for a pattern. Five failures on one signal is one problem, not five. -->



---

## The Improvement

**What I changed:**

**Which diagnosis pointed at it:**

### Attack Run — After

<!-- Same format. `run_attacks.py --label after` -->



**Did it help, and how do I know:**

<!-- Widening the unsure band usually fixes one problem and creates another.
     Reporting that trade honestly is worth full credit. -->



---

## What's Still Broken

<!-- For each attack still getting through and each criterion still missed:
     what you'd do, and why you stopped. -->



**The trade I'd make if this ran for real:**

<!-- Two sentences. Fewer wrong accusations means more AI text getting through.
     Say which way you'd go and WHO PAYS FOR IT. -->



<!-- ═════════════════════════════════════════════════════════════════════

     SUBMISSION CHECKLIST — unit 7

       [ ] criteria.md has five numbered criteria, each naming a target
       [ ] Each has a reason underneath
       [ ] POST /submit returns content_id, guess, confidence, label,
           model_score and style_score
       [ ] Two signals that measure DIFFERENT things, each with a named blind spot
       [ ] Three label variants, all reachable, written out in full
       [ ] POST /appeal changes status and writes to the log
       [ ] Signals and Scoring names scoring.py::combine_signals
       [ ] Sample Run: a submission AND an appeal, as pasted text
       [ ] At least four new commits
       [ ] Repository URL submitted — WRITE IT DOWN

     SUBMISSION CHECKLIST — unit 8

       [ ] Rate limiting on /submit, with your numbers justified
       [ ] The pasted run of status codes showing 429
       [ ] Audit log with all nine fields, recording rejections too
       [ ] The attack set run IN FULL, every input with an outcome
       [ ] Ten audit log entries pasted as text
       [ ] Five criteria across three trials
       [ ] A diagnosis for every miss and every broken attack — stage AND mechanism
       [ ] One improvement, with Attack Run — After
       [ ] What's Still Broken, including the production trade
       [ ] At least four new commits
       [ ] The SAME repository URL as last unit

     Do not delete and recreate this repository.
     ═════════════════════════════════════════════════════════════════════ -->

---

📖 **How to run this project: [RUNNING.md](RUNNING.md)**
