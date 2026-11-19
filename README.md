# Provenance Guard

> ### 👋 Start here
>
> **New to this repo? Read [RUNNING.md](RUNNING.md) first.**
>
> **Running the completed project? See the
> [Capstone setup instructions](#capstone--running-provenance-guard)
> below.**
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

stylometry.py uses sentence length variation and advanced punctuation to produce a style score.

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

**What it measures:** Uses sentence length variation (80%) and advanced punctuation (20%) to estimate how AI-like the writing style is. Word variety is also measured but isn't included in the final style score.


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
| unsure | Above 0.35, below 0.75 | This text shows a mix of human and AI writing patterns, so the result is inconclusive. |
| high-confidence AI | 0.75–1.00 | This text appears to be AI-generated. |

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
```

---

## How I Used AI

**Moment 1**

- **What I asked for:** I asked ChatGPT to help design the stylometry signal and figure out which writing patterns would be useful for detecting AI-generated text.
- **What came back:** It initially suggested using sentence length variation, word variety, and punctuation density. After testing different samples, we found that word variety wasn't very reliable and regular punctuation could be misleading.
- **What I changed:** I decided to focus on sentence length variation (80%) and advanced punctuation (20%), leaving word variety out of the final style score.

**Moment 2**

- **What I asked for:** I asked ChatGPT to help write the three classification labels, especially the unsure label.
- **What came back:** The first suggestions were too vague and included unnecessary disclaimers. We also discussed how to communicate uncertainty without making an accusation.
- **What I changed:** I simplified the human and AI labels and chose an unsure label that explains the writing shows a mix of human and AI patterns.

**Moment 3**

- **What I asked for:** I asked ChatGPT to help analyze the failed attacks and figure out why they got through.
- **What came back:** It identified which stages contributed to each failure based on the individual signal scores and the implementation.
- **What I changed:** I grouped the failures by their underlying causes and focused on the limitations of the signals rather than treating every attack as a separate issue.

**Moment 4**

- **What I asked for:** I asked ChatGPT to help determine which improvement would be most beneficial based on my diagnoses.
- **What came back:** It compared reweighting the signals, raising the AI threshold, and improving input validation, along with their trade-offs.
- **What I changed:** I decided to raise the AI threshold from 0.65 to 0.75 and reran both evaluations to see whether it reduced false positives.
<!-- ═══════════════════════ UNIT 8 — THE TEST ═══════════════════════ -->

---

## Rate Limiting

**My limits:** 5 per minute, 50 per day

**Why those numbers and not others:**
<!-- Think about two people: a real writer submitting their own work a few
     times an hour, and a script sending a thousand variations to map your
     thresholds. Your numbers have to be liveable for the first and hostile to
     the second. -->

A regular writer probably only needs to submit their work a few times an hour. These limits give writers enough room to submit and revise their work while making it harder for scripts to send hundreds of variations to figure out the system's thresholds.

**What a caller counts as:** <!-- per address, or per creator_id? They fail
differently — one script can look like a thousand callers, and one household
can look like one. -->

Each caller is identified by their creator_id, with their IP address used as a fallback. This allows different writers on the same network to have separate limits, but someone could bypass the limit by changing their creator ID.

**The run of status codes when I pushed past it:**

<!-- python run_attacks.py --flood 15 -->

```
200 200 200 200 200 429 429 429 429 429 429 429 429 429 429
```

---

## Attack Run — Before

<!-- Every attack with its outcome and a held-or-broke mark.
     `run_attacks.py --label before` produces the table. -->

| Attack | Family | HTTP Status | Guess | Outcome |
|---|---|---|---|---|
| EV01 | Evasion | 200 | unsure | BROKE |
| EV02 | Evasion | 200 | unsure | BROKE |
| EV03 | Evasion | 200 | unsure | BROKE |
| EV04 | Evasion | 200 | unsure | BROKE |
| EV05 | Evasion | 200 | human | BROKE |
| EV06 | Evasion | 200 | human | BROKE |
| EV07 | Evasion | 200 | ai | HELD |
| EV08 | Evasion | 200 | unsure | BROKE |
| EV09 | Evasion | 200 | unsure | BROKE |
| EV10 | Evasion | 200 | ai | HELD |
| FP01 | False positive | 200 | unsure | HELD |
| FP02 | False positive | 200 | ai | BROKE |
| FP03 | False positive | 200 | unsure | HELD |
| FP04 | False positive | 200 | unsure | HELD |
| FP05 | False positive | 200 | ai | BROKE |
| FP06 | False positive | 200 | unsure | HELD |
| FP07 | False positive | 200 | unsure | HELD |
| FP08 | False positive | 200 | human | HELD |
| PI01 | Prompt injection | 200 | human | BROKE |
| PI02 | Prompt injection | 200 | human | BROKE |
| PI03 | Prompt injection | 200 | unsure | HELD |
| PI04 | Prompt injection | 200 | unsure | HELD |
| PI05 | Prompt injection | 200 | unsure | HELD |
| PI06 | Prompt injection | 200 | unsure | HELD |
| MF01 | Malformed | 400 | — | HELD |
| MF02 | Malformed | 400 | — | HELD |
| MF03 | Malformed | 200 | unsure | BROKE |
| MF04 | Malformed | 200 | unsure | BROKE |
| MF05 | Malformed | 200 | ai | BROKE |
| MF06 | Malformed | 200 | ai | BROKE |
| MF07 | Malformed | 200 | ai | HELD |
| MF08 | Malformed | 400 | — | HELD |
| RQ01 | Malformed | 400 | — | HELD |
| RQ02 | Malformed | 400 | — | HELD |
| RQ03 | Malformed | 400 | — | HELD |
| RQ04 | Malformed | 400 | — | HELD |
| RQ05 | Malformed | 400 | — | HELD |
| RQ06 | Malformed | 400 | — | HELD |
| RQ07 | Malformed | 400 | — | HELD |
| RQ08 | Malformed | 400 | — | HELD |
| RQ09 | Malformed | 400 | — | HELD |
| RQ10 | Malformed | 429 | — | HELD |
| RQ11 | Malformed | 429 | — | HELD |
| RQ12 | Malformed | 400 | — | HELD |
| FL01_01 | Flood | 200 | unsure | HELD |
| FL01_02 | Flood | 200 | unsure | HELD |
| FL01_03 | Flood | 200 | unsure | HELD |
| FL01_04 | Flood | 200 | unsure | HELD |
| FL01_05 | Flood | 200 | unsure | HELD |
| FL01_06 | Flood | 429 | — | HELD |
| FL01_07 | Flood | 429 | — | HELD |
| FL01_08 | Flood | 429 | — | HELD |
| FL01_09 | Flood | 429 | — | HELD |
| FL01_10 | Flood | 429 | — | HELD |
| FL01_11 | Flood | 429 | — | HELD |
| FL01_12 | Flood | 429 | — | HELD |

**Ten audit log entries from the run**

<!-- Choose entries that show the interesting failures, not the ten easiest. -->

```json
  {
    "combined_score": 0.4246,
    "content_id": "17e6f55b-ceb3-4018-a90a-94f0f9f80374",
    "creator_id": "attacker_EV01",
    "guess": "unsure",
    "label": "This text shows a mix of human and AI writing patterns, so the result is inconclusive.",
    "model_score": 0.1635,
    "status": "decided",
    "style_score": 0.6857,
    "timestamp": "2026-11-17T02:11:01+00:00"
  },
  {
    "combined_score": 0.2228,
    "content_id": "4c67dd1d-6221-42c7-9a11-3e5201330f33",
    "creator_id": "attacker_EV05",
    "guess": "human",
    "label": "This text appears to be written by a person.",
    "model_score": 0.3212,
    "status": "decided",
    "style_score": 0.1244,
    "timestamp": "2026-11-17T02:11:01+00:00"
  },
  {
    "combined_score": 0.3363,
    "content_id": "4b5be9c9-54f9-41fa-bdfe-4d2c439cc302",
    "creator_id": "attacker_EV06",
    "guess": "human",
    "label": "This text appears to be written by a person.",
    "model_score": 0.5727,
    "status": "decided",
    "style_score": 0.1,
    "timestamp": "2026-11-17T02:11:01+00:00"
  },
  {
    "combined_score": 0.6591,
    "content_id": "1914a248-b75d-46aa-93fe-d282b982a892",
    "creator_id": "attacker_FP02",
    "guess": "ai",
    "label": "This text appears to be AI-generated.",
    "model_score": 0.7387,
    "status": "decided",
    "style_score": 0.5795,
    "timestamp": "2026-11-17T02:11:01+00:00"
  },
  {
    "combined_score": 0.6657,
    "content_id": "70670206-2d57-4c85-9a70-d6cbf72c7c58",
    "creator_id": "attacker_FP05",
    "guess": "ai",
    "label": "This text appears to be AI-generated.",
    "model_score": 0.8005,
    "status": "decided",
    "style_score": 0.5308,
    "timestamp": "2026-11-17T02:11:01+00:00"
  },
  {
    "combined_score": 0.2812,
    "content_id": "8070a01c-aa63-4d8e-b36e-2eb4cf090c96",
    "creator_id": "attacker_PI01",
    "guess": "human",
    "label": "This text appears to be written by a person.",
    "model_score": 0.4625,
    "status": "decided",
    "style_score": 0.1,
    "timestamp": "2026-11-17T02:11:02+00:00"
  },
  {
    "combined_score": 0.1744,
    "content_id": "fa48cdfa-aff4-4ffc-a933-15daeb4078cb",
    "creator_id": "attacker_PI02",
    "guess": "human",
    "label": "This text appears to be written by a person.",
    "model_score": 0.2044,
    "status": "decided",
    "style_score": 0.1444,
    "timestamp": "2026-11-17T02:11:02+00:00"
  },
  {
    "combined_score": 0.45,
    "content_id": "59e08852-2d3f-43e6-a5aa-5410999b8967",
    "creator_id": "attacker_MF03",
    "guess": "unsure",
    "label": "This text shows a mix of human and AI writing patterns, so the result is inconclusive.",
    "model_score": 0.0,
    "status": "decided",
    "style_score": 0.9,
    "timestamp": "2026-11-17T02:11:02+00:00"
  },
  {
    "combined_score": 0.9485,
    "content_id": "511ca395-7b67-4e41-b1b2-0703716ae4c4",
    "creator_id": "attacker_MF06",
    "guess": "ai",
    "label": "This text appears to be AI-generated.",
    "model_score": 0.9969,
    "status": "decided",
    "style_score": 0.9,
    "timestamp": "2026-11-17T02:11:02+00:00"
  },
  {
    "creator_id": "attacker_flood",
    "event": "rejected",
    "limit": "5 per 1 minute",
    "reason": "rate_limited",
    "status": "rejected",
    "timestamp": "2026-11-17T02:11:02+00:00"
  }
```

**The single worst outcome** — the one I'd least want to explain to a writer
whose work got caught by it:

FP05 was the worst outcome for me because it was technical documentation written by a person that the system incorrectly labeled as AI-generated. It received a model score of 0.8005, a style score of 0.5308, and a combined score of 0.6657. A writer could be falsely accused simply because of the way they write.

---

## Run Log and Verdicts

<!-- Your five criteria across three trials. `run_eval.py --label before`. -->

| Criterion | Target | Run 1 | Run 2 | Run 3 | Verdict |
|---|---|---|---|---|---|
| 1. False positives | ≤ 1 of 10 | 2/10 | 2/10 | 2/10 | MISSED |
| 2. Score separation | ≥ 0.20 | 0.2115 | 0.2115 | 0.2115 | MET |
| 3. Label coverage | 3 of 3 | 3/3 | 3/3 | 3/3 | MET |
| 4. Appeal reliability | 5 of 5 | 5/5 | 5/5 | 5/5 | MET |
| 5. Invalid input handling | 5 of 5 | 5/5 | 5/5 | 5/5 | MET |

**Real output from one trial**, pasted as text, naming the file and function
that produced it:

Produced by `run_eval.py::main` and saved in `results/run_2026-11-16_2149_before.md`.

**Criterion 1 — False positives**

```json
{
  "status": 200,
  "content_id": "7926f7bb-c901-4555-99fe-fb92257d0636",
  "guess": "ai",
  "confidence": 0.6625,
  "model_score": 0.7141,
  "style_score": 0.6109,
  "label": "This text appears to be AI-generated.",
  "error": null,
  "sent": "WHEN AN ammonia leak outside a hotel in Weatherford, Oklahoma, injured"
}
```

**Criterion 2 — Score separation**

```json
[
  {
    "status": 200,
    "content_id": "7aed1235-33ef-47f4-8080-9bca670ca82e",
    "guess": "human",
    "confidence": 0.327,
    "model_score": 0.2203,
    "style_score": 0.4337,
    "label": "This text appears to be written by a person.",
    "error": null,
    "sent": "Hey whats going on guys. its your boy realog here back with a another "
  },
  {
    "status": 200,
    "content_id": "f6277d77-1a3b-495c-ba63-f35b0e85fe01",
    "guess": "ai",
    "confidence": 0.7677,
    "model_score": 0.7955,
    "style_score": 0.7399,
    "label": "This text appears to be AI-generated.",
    "error": null,
    "sent": "Video games provide players with opportunities to develop problem-solv"
  }
]
```

**Criterion 3 — Label coverage**

```json
[
  {
    "status": 200,
    "content_id": "ecb0033a-d4c8-4579-994c-6635936ae9b6",
    "guess": "human",
    "confidence": 0.327,
    "model_score": 0.2203,
    "style_score": 0.4337,
    "label": "This text appears to be written by a person.",
    "error": null,
    "sent": "Hey whats going on guys. its your boy realog here back with a another "
  },
  {
    "status": 200,
    "content_id": "23e48766-a437-4c5c-a6d9-013635fee5d9",
    "guess": "unsure",
    "confidence": 0.5819,
    "model_score": 0.8029,
    "style_score": 0.3609,
    "label": "This text shows a mix of human and AI writing patterns, so the result is inconclusive.",
    "error": null,
    "sent": "The program, known as ASPECT, was designed to respond around the clock"
  },
  {
    "status": 200,
    "content_id": "1a5a6334-3dc6-420b-b912-822bfa4fbf89",
    "guess": "ai",
    "confidence": 0.7677,
    "model_score": 0.7955,
    "style_score": 0.7399,
    "label": "This text appears to be AI-generated.",
    "error": null,
    "sent": "Video games provide players with opportunities to develop problem-solv"
  }
]
```

**Criterion 4 — Appeal reliability**

```json
{
  "status": 200,
  "content_id": "cd144a4c-e63c-4ef0-8f11-a65f8369bd1c",
  "guess": "ai",
  "confidence": 0.6625,
  "model_score": 0.7141,
  "style_score": 0.6109,
  "label": "This text appears to be AI-generated.",
  "error": null,
  "sent": "WHEN AN ammonia leak outside a hotel in Weatherford, Oklahoma, injured",
  "appeal_status": 200,
  "appeal_response": {
    "content_id": "cd144a4c-e63c-4ef0-8f11-a65f8369bd1c",
    "message": "Appeal submitted successfully.",
    "status": "under_review"
  },
  "audit_entries": [
    {
      "combined_score": 0.6625,
      "content_id": "cd144a4c-e63c-4ef0-8f11-a65f8369bd1c",
      "creator_id": "eval_appeal relia_3",
      "guess": "ai",
      "label": "This text appears to be AI-generated.",
      "model_score": 0.7141,
      "status": "decided",
      "style_score": 0.6109,
      "timestamp": "2026-11-17T02:49:51+00:00"
    },
    {
      "content_id": "cd144a4c-e63c-4ef0-8f11-a65f8369bd1c",
      "creator_id": "eval_appeal relia_3",
      "event": "appeal",
      "reasoning": "I would like this decision reviewed.",
      "status": "under_review",
      "timestamp": "2026-11-17T02:49:51+00:00"
    }
  ]
}
```

**Criterion 5 — Invalid input handling**

```json
{
  "status": 400,
  "content_id": null,
  "guess": null,
  "confidence": null,
  "model_score": null,
  "style_score": null,
  "label": null,
  "error": "Valid text is required.",
  "sent": "(empty text)"
}
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

**Criterion 1 — False Positives:** Two of the ten human samples were classified as AI in all three trials, exceeding my target of at most one.

- **Stage:** Both signals and the combining rule.
- **Mechanism:** Two of the ten human samples were flagged as AI in every trial. The first had a high model score (0.7141), while the second had a high style score (0.9220). Both ended up above the AI threshold of 0.65. The system can mistake predictable wording and consistent writing styles for AI-generated text.

**Broken attacks**

| Attack | Stage | Mechanism |
|---|---|---|
| EV01 | Signal one | Typos made the text less predictable, lowering the model score to 0.1635. |
| EV02 | Signal two | Breaking up sentences increased sentence length variation, lowering the style score to 0.1659. |
| EV03 | Signal two | Adding a quotation changed the sentence structure, resulting in a style score of 0.3277. |
| EV04 | Signal one | Unusual vocabulary made the text less predictable. The combined score fell just below the AI threshold at 0.6397. |
| EV05 | Both signals | Heavy human editing made the wording and sentence structure less predictable, resulting in a combined score of 0.2228. |
| EV06 | Signal two | Mixing very long and short sentences lowered the style score to 0.1000. |
| EV08 | Signal one | The short text gave the model limited information to work with and received a model score of 0.2452. |
| EV09 | Signal two, combining rule | Adding a human-written opening resulted in a low style score, bringing the combined score down to 0.4904. |
| FP02 | Signal one | The predictable wording in formal human writing resulted in a combined score of 0.6591. |
| FP05 | Signal one | The predictable language in technical documentation resulted in a combined score of 0.6657. |
| PI01 | Signal two | The sentence structure resulted in a low style score of 0.1000, bringing the combined score into the human range. |
| PI02 | Both signals | The fake system message received low scores from both signals, resulting in a human classification. |
| MF03 | Route | Control characters passed input validation. |
| MF04 | Route | Punctuation-only text passed input validation. |
| MF05 | Route, both signals | A long, repetitive word passed validation and received high scores due to its predictability and lack of sentence variation. |
| MF06 | Route, both signals | Emoji-only text passed validation and received high scores despite not containing actual writing. |

Most of the failures came from the limitations of the two signals. Predictable human writing can be mistaken for AI, while AI-generated writing can avoid detection by changing its wording or sentence structure. The 50/50 weighted average also means that either signal can significantly affect the final classification.

Another issue is that my input validation checks the type and length of the text but doesn't check whether it contains meaningful writing.

---

## The Improvement

**What I changed:**
I increased the AI threshold from 0.65 to 0.75, widening the unsure range while keeping both signals and their weights the same.

**Which diagnosis pointed at it:**
The false positive criterion and attacks FP02 and FP05 showed that human writing was being flagged as AI. Raising the threshold should reduce false accusations, although it may also allow more AI-generated writing to avoid detection.

### Attack Run — After

<!-- Same format. `run_attacks.py --label after` -->

| Attack | Family | HTTP Status | Guess | Outcome |
|---|---|---|---|---|
| EV01 | evasion | 200 | unsure | BROKE |
| EV02 | evasion | 200 | unsure | BROKE |
| EV03 | evasion | 200 | unsure | BROKE |
| EV04 | evasion | 200 | unsure | BROKE |
| EV05 | evasion | 200 | human | BROKE |
| EV06 | evasion | 200 | human | BROKE |
| EV07 | evasion | 200 | ai | HELD |
| EV08 | evasion | 200 | unsure | BROKE |
| EV09 | evasion | 200 | unsure | BROKE |
| EV10 | evasion | 200 | unsure | BROKE |
| FP01 | false_positive | 200 | unsure | HELD |
| FP02 | false_positive | 200 | unsure | HELD |
| FP03 | false_positive | 200 | unsure | HELD |
| FP04 | false_positive | 200 | unsure | HELD |
| FP05 | false_positive | 200 | unsure | HELD |
| FP06 | false_positive | 200 | unsure | HELD |
| FP07 | false_positive | 200 | unsure | HELD |
| FP08 | false_positive | 200 | human | HELD |
| PI01 | prompt_injection | 200 | human | BROKE |
| PI02 | prompt_injection | 200 | human | BROKE |
| PI03 | prompt_injection | 200 | unsure | HELD |
| PI04 | prompt_injection | 200 | unsure | HELD |
| PI05 | prompt_injection | 200 | unsure | HELD |
| PI06 | prompt_injection | 200 | unsure | HELD |
| MF01 | malformed | 400 | — | HELD |
| MF02 | malformed | 400 | — | HELD |
| MF03 | malformed | 200 | unsure | BROKE |
| MF04 | malformed | 200 | unsure | BROKE |
| MF05 | malformed | 200 | ai | BROKE |
| MF06 | malformed | 200 | ai | BROKE |
| MF07 | malformed | 200 | ai | HELD |
| MF08 | malformed | 400 | — | HELD |
| RQ01 | malformed | 400 | — | HELD |
| RQ02 | malformed | 400 | — | HELD |
| RQ03 | malformed | 400 | — | HELD |
| RQ04 | malformed | 400 | — | HELD |
| RQ05 | malformed | 400 | — | HELD |
| RQ06 | malformed | 400 | — | HELD |
| RQ07 | malformed | 400 | — | HELD |
| RQ08 | malformed | 400 | — | HELD |
| RQ09 | malformed | 400 | — | HELD |
| RQ10 | malformed | 429 | — | HELD |
| RQ11 | malformed | 429 | — | HELD |
| RQ12 | malformed | 400 | — | HELD |
| FL01_01 | flood_same_creator | 200 | unsure | HELD |
| FL01_02 | flood_same_creator | 200 | unsure | HELD |
| FL01_03 | flood_same_creator | 200 | unsure | HELD |
| FL01_04 | flood_same_creator | 200 | unsure | HELD |
| FL01_05 | flood_same_creator | 200 | unsure | HELD |
| FL01_06 | flood_same_creator | 429 | — | HELD |
| FL01_07 | flood_same_creator | 429 | — | HELD |
| FL01_08 | flood_same_creator | 429 | — | HELD |
| FL01_09 | flood_same_creator | 429 | — | HELD |
| FL01_10 | flood_same_creator | 429 | — | HELD |
| FL01_11 | flood_same_creator | 429 | — | HELD |
| FL01_12 | flood_same_creator | 429 | — | HELD |

**Acceptance criteria — After**

| Criterion | Target | Run 1 | Run 2 | Run 3 | Verdict |
|---|---|---|---|---|---|
| 1. False positives | ≤ 1 of 10 | 0/10 | 0/10 | 0/10 | MET |
| 2. Score separation | ≥ 0.20 | 0.2115 | 0.2115 | 0.2115 | MET |
| 3. Label coverage | 3 of 3 | 3/3 | 3/3 | 3/3 | MET |
| 4. Appeal reliability | 5 of 5 | 5/5 | 5/5 | 5/5 | MET |
| 5. Invalid input handling | 5 of 5 | 5/5 | 5/5 | 5/5 | MET |

**Did it help, and how do I know:**

<!-- Widening the unsure band usually fixes one problem and creates another.
     Reporting that trade honestly is worth full credit. -->

Yes, raising the AI threshold reduced false positives from 2/10 to 0/10 across all three trials, and all five criteria are now met. FP02 and FP05 are no longer flagged as AI, but EV10 now avoids detection. The number of AI samples correctly labeled as AI also dropped from 2/5 to 1/5.

The system is less likely to falsely accuse human writers, but the trade-off is that more AI-generated writing gets through.

---

## What's Still Broken

<!-- For each attack still getting through and each criterion still missed:
     what you'd do, and why you stopped. -->

All five criteria are now met, but 15 of the 56 attacks still get through.

- **Evasion (EV01–EV06, EV08–EV10):** Both signals can be manipulated by changing the wording or sentence structure. I would experiment with additional signals that are less sensitive to these changes and test different weights.
- **Prompt injection (PI01, PI02):** Both inputs are still classified as human. Although the model isn't actually following the instructions, I would explore ways to identify these patterns without penalizing legitimate writing.
- **Malformed input (MF03–MF06):** The system still accepts control characters, punctuation-only text, long repetitive words, and emoji-only text. I would improve input validation to check whether the text is suitable for analysis before scoring it.

I stopped after changing the AI threshold because I wanted to measure the effect of one change rather than make several changes at once without knowing which one helped.

**The trade I'd make if this ran for real:**

<!-- Two sentences. Fewer wrong accusations means more AI text getting through.
     Say which way you'd go and WHO PAYS FOR IT. -->

I would prioritize reducing false accusations, even if that means more AI-generated writing goes undetected. This puts more responsibility on the platform and its moderators, but it avoids unfairly accusing genuine writers.

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

## Capstone

**What This Extends**

This project extends Provenance Guard, a backend service I built to estimate whether submitted writing might be AI-generated. In my previous attack tests, I found that the service still accepted control characters, punctuation-only text, emoji-only text, and long repetitive words. These inputs could reach the detector and get a classification even though they weren't suitable for analysis.

For the capstone, I wanted to reject unsuitable inputs before running the model and make it easier to see what happened to each request.

**The Shape**

I chose Shape B — Harden against failure. I added an input validation layer and structured request logging so I could measure how the service handles valid and invalid submissions. The detection model, signal weights, classification thresholds, and appeal workflow are outside the scope of this extension.

**Running It**

I chose Path B — local with logs. The service runs locally using Flask, Gunicorn, and GPT-2 without an external inference API or API key. I ran the evaluation on my machine using Python 3.13.15 and Gunicorn with one worker and one thread.

See [RUNNING.md](RUNNING.md) for setup, dependencies, and example requests.

Once the environment is set up and activated, start the service:

```bash
gunicorn app:app --bind 127.0.0.1:5000 --workers 1 --threads 1 --timeout 120
```

In another terminal:

```bash
curl http://127.0.0.1:5000/health
python -m unittest test_validation -v
```

The evaluation script is `run_capstone.py`. To run the current implementation, use the commands below while the service is running. They write to the named result files, so preserve the committed evidence or use a separate checkout before rerunning.

```bash
python run_capstone.py --label after
python run_capstone.py --label cost
```

**Instrumentation**

I used Flask's `before_request` and `after_request` hooks in `request_logging.py` to record requests to `/submit` and `/appeal`. The original audit log still records classification decisions, appeals, and rejections. The new structured log, `logs/capstone_requests.jsonl`, records:

| Field | What it captures |
|---|---|
| `timestamp` | When the request started (UTC) |
| `request_id` | Unique ID used to match a response to its log record |
| `endpoint` | Route being called |
| `input`, `input_truncated` | Request body, limited to the first 1,000 characters, and whether it was truncated |
| `output`, `status_code` | Response and HTTP status |
| `duration_ms` | Server-side elapsed time up to the response logging hook |
| `cpu_seconds` | Process CPU time over the same measured interval |
| `detector_called` | Whether the request reached the model call |

The request ID is also returned in the `X-Request-ID` response header. The evaluation script matches this ID with the log and saves the matching record alongside the response. Both successful and rejected submissions are recorded.

The 11 records below are actual output from `request_logging.py::init_app` (its nested `log_request` hook), collected by `run_capstone.py::submit_case` and the evaluation script. The first ten are successful cost-test requests after the improvement, followed by a rejected punctuation-only request from the final evaluation.

**Actual structured log output (10 successful requests and 1 rejection)**

```jsonl
{"timestamp": "2026-11-19T00:21:22.386486+00:00", "request_id": "3ded4fcd381d41d8898fbdfdc5d28fc3", "endpoint": "/submit", "input": "{\"text\": \"I went to the library after class today. It was quiet, so I finished my homework.\", \"creator_id\": \"capstone_c65f867d0d344c748ebb174e0b2bf76e\"}", "input_truncated": false, "output": {"confidence": 0.7961, "content_id": "0b798978-e81f-46ee-a9a3-59e516c68810", "guess": "ai", "label": "This text appears to be AI-generated.", "model_score": 0.6921, "style_score": 0.9}, "status_code": 200, "duration_ms": 22.299, "cpu_seconds": 0.027405, "detector_called": true}
{"timestamp": "2026-11-19T00:21:22.410423+00:00", "request_id": "bba0f29b37904038ad9c8f85ca261d83", "endpoint": "/submit", "input": "{\"text\": \"I finally finished my project today! I'm glad it's over \\ud83d\\ude02\", \"creator_id\": \"capstone_51c9720a2fa240979b3bde1dad134b2a\"}", "input_truncated": false, "output": {"confidence": 0.536, "content_id": "5e61d166-0b09-4079-b8dd-c874973b89f5", "guess": "unsure", "label": "This text shows a mix of human and AI writing patterns, so the result is inconclusive.", "model_score": 0.5491, "style_score": 0.5229}, "status_code": 200, "duration_ms": 23.339, "cpu_seconds": 0.02389, "detector_called": true}
{"timestamp": "2026-11-19T00:21:22.436239+00:00", "request_id": "b7e1737fa642493fad090a5187e94dc2", "endpoint": "/submit", "input": "{\"text\": \"Today was a busy day.\\nI had two classes and a meeting.\", \"creator_id\": \"capstone_a3ea3645a486465bb34a86a2af5988ee\"}", "input_truncated": false, "output": {"confidence": 0.6103, "content_id": "3e70aeba-95aa-467b-96e4-1dc54ffcf46a", "guess": "unsure", "label": "This text shows a mix of human and AI writing patterns, so the result is inconclusive.", "model_score": 0.6349, "style_score": 0.5857}, "status_code": 200, "duration_ms": 34.22, "cpu_seconds": 0.03312, "detector_called": true}
{"timestamp": "2026-11-19T00:21:22.472616+00:00", "request_id": "977d69adc474466a852735c1d79a853b", "endpoint": "/submit", "input": "{\"text\": \"I went to the library after class today. It was quiet, so I finished my homework.\", \"creator_id\": \"capstone_dc9673151662429cbdce25c82699cfbd\"}", "input_truncated": false, "output": {"confidence": 0.7961, "content_id": "8a6f5e6f-e18c-472c-9c83-93836566d604", "guess": "ai", "label": "This text appears to be AI-generated.", "model_score": 0.6921, "style_score": 0.9}, "status_code": 200, "duration_ms": 26.18, "cpu_seconds": 0.030233, "detector_called": true}
{"timestamp": "2026-11-19T00:21:22.499974+00:00", "request_id": "7b6983de3e894c45894cc7b465ce27b4", "endpoint": "/submit", "input": "{\"text\": \"I finally finished my project today! I'm glad it's over \\ud83d\\ude02\", \"creator_id\": \"capstone_35e692d6014e48aaae9bebefccc9dae9\"}", "input_truncated": false, "output": {"confidence": 0.536, "content_id": "40bd7195-7885-48a6-8fcc-767597f5861c", "guess": "unsure", "label": "This text shows a mix of human and AI writing patterns, so the result is inconclusive.", "model_score": 0.5491, "style_score": 0.5229}, "status_code": 200, "duration_ms": 19.825, "cpu_seconds": 0.02224, "detector_called": true}
{"timestamp": "2026-11-19T00:21:22.521365+00:00", "request_id": "010389e0c68149c1a282a03ad600b63f", "endpoint": "/submit", "input": "{\"text\": \"Today was a busy day.\\nI had two classes and a meeting.\", \"creator_id\": \"capstone_922ab66bb80b4a1cac8cf591df3aa2fa\"}", "input_truncated": false, "output": {"confidence": 0.6103, "content_id": "038fa500-279e-473f-8c8b-2e852a209a01", "guess": "unsure", "label": "This text shows a mix of human and AI writing patterns, so the result is inconclusive.", "model_score": 0.6349, "style_score": 0.5857}, "status_code": 200, "duration_ms": 18.074, "cpu_seconds": 0.020368, "detector_called": true}
{"timestamp": "2026-11-19T00:21:22.540799+00:00", "request_id": "8cf45d7807bf489f9d502c64a01faec5", "endpoint": "/submit", "input": "{\"text\": \"I went to the library after class today. It was quiet, so I finished my homework.\", \"creator_id\": \"capstone_2a4e71232b744b85849da8dfb06a1ce2\"}", "input_truncated": false, "output": {"confidence": 0.7961, "content_id": "aea92912-7eaa-43cb-b3a3-c4ca812e2e0e", "guess": "ai", "label": "This text appears to be AI-generated.", "model_score": 0.6921, "style_score": 0.9}, "status_code": 200, "duration_ms": 21.252, "cpu_seconds": 0.025932, "detector_called": true}
{"timestamp": "2026-11-19T00:21:22.563397+00:00", "request_id": "0d05cbd188284974b42e85af46f51503", "endpoint": "/submit", "input": "{\"text\": \"I finally finished my project today! I'm glad it's over \\ud83d\\ude02\", \"creator_id\": \"capstone_2bf8f2c9ff6a4fc2a454b8c315cfe533\"}", "input_truncated": false, "output": {"confidence": 0.536, "content_id": "607afb4e-7c98-4524-9a83-6ed058b6cb46", "guess": "unsure", "label": "This text shows a mix of human and AI writing patterns, so the result is inconclusive.", "model_score": 0.5491, "style_score": 0.5229}, "status_code": 200, "duration_ms": 17.339, "cpu_seconds": 0.019887, "detector_called": true}
{"timestamp": "2026-11-19T00:21:22.581969+00:00", "request_id": "ab494914fbca43578f0a5de1bdc18bc4", "endpoint": "/submit", "input": "{\"text\": \"Today was a busy day.\\nI had two classes and a meeting.\", \"creator_id\": \"capstone_e1effa793d6d42f9ab0b1e385551682a\"}", "input_truncated": false, "output": {"confidence": 0.6103, "content_id": "5fe26edb-618b-43e8-98c7-7fc030d82560", "guess": "unsure", "label": "This text shows a mix of human and AI writing patterns, so the result is inconclusive.", "model_score": 0.6349, "style_score": 0.5857}, "status_code": 200, "duration_ms": 17.601, "cpu_seconds": 0.019948, "detector_called": true}
{"timestamp": "2026-11-19T00:21:22.601129+00:00", "request_id": "235a6bd1f2c34d298d075efedd9b2ab4", "endpoint": "/submit", "input": "{\"text\": \"I went to the library after class today. It was quiet, so I finished my homework.\", \"creator_id\": \"capstone_97c0068477f74c159a7650ba6b9ce1c7\"}", "input_truncated": false, "output": {"confidence": 0.7961, "content_id": "f33f87b8-41c2-474f-9e1a-59cec7fd3f1e", "guess": "ai", "label": "This text appears to be AI-generated.", "model_score": 0.6921, "style_score": 0.9}, "status_code": 200, "duration_ms": 23.349, "cpu_seconds": 0.027956, "detector_called": true}
{"timestamp": "2026-11-19T00:21:22.065075+00:00", "request_id": "d6a3c20ca719455bbc87fc4ffe0536b0", "endpoint": "/submit", "input": "{\"text\": \"!!!!!!!!!!!!!\", \"creator_id\": \"capstone_a8213a5ac29e4c4586b253341ca34bb3\"}", "input_truncated": false, "output": {"error": "Text is unsuitable for analysis.", "reason": "no_alphabetic_characters"}, "status_code": 400, "duration_ms": 0.283, "cpu_seconds": 0.000288, "detector_called": false}
```

**What It Costs**

The model runs locally, so there are no inference API charges. I measured process CPU time with `time.process_time()` over ten successful submissions after warming up the model. I repeated the same measurement after the improvement, using the same three short writing samples.

| Metric | Before | After |
|---|---:|---:|
| Successful requests | 10/10 | 10/10 |
| Total measured CPU time (s) | 0.221894 | 0.250979 |
| Average CPU time per submission (s) | 0.0221894 | 0.0250979 |
| Average server-side latency (ms) | 20.0634 | 22.3478 |

For 100 people submitting one request per day on the final implementation:

```text
0.250979 CPU seconds / 10 requests = 0.0250979 CPU seconds/request
0.0250979 × 100 = 2.50979 CPU seconds/day
```

The average CPU time for valid submissions increased slightly. With only ten requests per measurement, I can't tell how much of that difference came from the additional validation checks versus normal execution variability.

These measurements exclude initial model loading, the final request-log write, and network overhead. They are specific to short samples on my machine and aren't a measurement of electricity, hardware, or production hosting costs.

Final measurement: [results/capstone_cost.json](results/capstone_cost.json).

**Run Log and Verdicts**

I used eight invalid submissions (punctuation-only, emoji-only, numbers-only, control characters, repetitive characters, repetitive words, empty text, and whitespace-only) and three valid samples (plain writing, writing with an emoji, and multiline writing). I ran the same 11 cases three times, with a warm-up request excluded from the evaluation. Each submission used a new creator ID to avoid rate limiting interfering with the validation tests.

The targets are in [criteria.md](criteria.md). I marked a criterion MET only if it reached its target in all three trials.

*Before the repetition checks*

| Criterion | Target | Run 1 | Run 2 | Run 3 | Verdict |
|---|---|---|---|---|---|
| 1. Malformed input rejection | 8/8 | 6/8 | 6/8 | 6/8 | MISSED |
| 2. Unnecessary detector execution | 0/8 called | 2/8 | 2/8 | 2/8 | MISSED |
| 3. Structured logging | 11/11 | 11/11 | 11/11 | 11/11 | MET |
| 4. Invalid input rejection latency | 7/8 under 100 ms | 6/8 | 6/8 | 6/8 | MISSED |
| 5. Valid input handling | 3/3 | 3/3 | 3/3 | 3/3 | MET |

Full results: [results/capstone_before.json](results/capstone_before.json).

The following records are actual output from the first trial, produced by `request_logging.py::init_app` (the nested `log_request` hook) and captured by `run_capstone.py`. They are representative examples for each criterion; the full result file contains all 33 requests.

**Baseline evidence — one record per criterion**

**Criterion 1. Malformed input rejection — `repetitive_characters`**

```json
{
  "timestamp": "2026-11-18T23:00:09.831289+00:00",
  "request_id": "264acad680b246f8a725b2f29c04b4cf",
  "endpoint": "/submit",
  "input": "{\"text\": \"aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa\", \"creator_id\": \"capstone_4288c37e1e4e4fcba7093fdd1a85e9ea\"}",
  "input_truncated": false,
  "output": {
    "confidence": 0.9483,
    "content_id": "9684c1d6-abf0-4aa4-9b7d-797ec36da537",
    "guess": "ai",
    "label": "This text appears to be AI-generated.",
    "model_score": 0.9966,
    "style_score": 0.9
  },
  "status_code": 200,
  "duration_ms": 33.836,
  "cpu_seconds": 0.045413,
  "detector_called": true
}
```

**Criterion 2. Unnecessary detector execution — `repetitive_words`**

```json
{
  "timestamp": "2026-11-18T23:00:09.866386+00:00",
  "request_id": "8e3ae861847448fa8d626c631ba4d071",
  "endpoint": "/submit",
  "input": "{\"text\": \"hello hello hello hello hello hello hello hello hello hello hello hello hello hello hello hello hello hello hello hello hello hello hello hello hello hello hello hello hello hello hello hello hello hello hello hello hello hello hello hello hello hello hello hello hello hello hello hello hello hello hello hello hello hello hello hello hello hello hello hello hello hello hello hello hello hello hello hello hello hello hello hello hello hello hello hello hello hello hello hello \", \"creator_id\": \"capstone_fe4fa0d116dd48c49f5c18047fd2e05c\"}",
  "input_truncated": false,
  "output": {
    "confidence": 0.9478,
    "content_id": "945961c4-59f6-42b0-bc8d-5aa491637376",
    "guess": "ai",
    "label": "This text appears to be AI-generated.",
    "model_score": 0.9955,
    "style_score": 0.9
  },
  "status_code": 200,
  "duration_ms": 37.079,
  "cpu_seconds": 0.055175,
  "detector_called": true
}
```

**Criterion 3. Structured logging — `punctuation`**

```json
{
  "timestamp": "2026-11-18T23:00:09.824518+00:00",
  "request_id": "6f6b6c4442e746edae64ae22f89ee70a",
  "endpoint": "/submit",
  "input": "{\"text\": \"!!!!!!!!!!!!!\", \"creator_id\": \"capstone_8ca68f0615ff40d2b61442e7541d2723\"}",
  "input_truncated": false,
  "output": {
    "error": "Text is unsuitable for analysis.",
    "reason": "no_alphabetic_characters"
  },
  "status_code": 400,
  "duration_ms": 0.713,
  "cpu_seconds": 0.000724,
  "detector_called": false
}
```

**Criterion 4. Rejection latency — `control_characters`**

```json
{
  "timestamp": "2026-11-18T23:00:09.828909+00:00",
  "request_id": "16fc0bb0fee44078aa85a1486be3ec4c",
  "endpoint": "/submit",
  "input": "{\"text\": \"Hello\\u0000this is a test.\", \"creator_id\": \"capstone_738867c08afc4e889c51f1fb003a4471\"}",
  "input_truncated": false,
  "output": {
    "error": "Text is unsuitable for analysis.",
    "reason": "invalid_control_characters"
  },
  "status_code": 400,
  "duration_ms": 0.462,
  "cpu_seconds": 0.000376,
  "detector_called": false
}
```

**Criterion 5. Valid input handling — `valid_plain`**

```json
{
  "timestamp": "2026-11-18T23:00:09.906571+00:00",
  "request_id": "6c3dce4e07864e33bfc96cb09a373c1c",
  "endpoint": "/submit",
  "input": "{\"text\": \"I went to the library after class today. It was quiet, so I finished my homework.\", \"creator_id\": \"capstone_6c46224b76ec4cb3ad4dd974b4942666\"}",
  "input_truncated": false,
  "output": {
    "confidence": 0.7961,
    "content_id": "2074ee83-1f9c-42d8-9e8a-198c94239ae0",
    "guess": "ai",
    "label": "This text appears to be AI-generated.",
    "model_score": 0.6921,
    "style_score": 0.9
  },
  "status_code": 200,
  "duration_ms": 20.136,
  "cpu_seconds": 0.02484,
  "detector_called": true
}
```

**Diagnoses**

- **Criterion 1 — Validation (`validation.py::validate_text`):** The original checks looked for alphabetic characters and invalid control characters. A single letter repeated 200 times and a single word repeated 80 times both passed these checks, so both returned HTTP 200 rather than HTTP 400.
- **Criterion 2 — Submission route (`app.py::submit`):** Since validation accepted both repetitive inputs, the route called `detector.model_signal()` on them. Two invalid submissions reached the model in every trial, even though they weren't suitable for analysis.
- **Criterion 4 — Validation and response handling (`validation.py::validate_text`, `app.py::submit`):** All six inputs that actually returned HTTP 400 took less than 1 ms on the server. The two repetitive inputs returned HTTP 200, so they didn't count toward the rejection latency target even though their individual response times were below 100 ms.

All three misses came from the same limitation: the validation layer checked for letters and control characters but didn't account for excessive repetition. The logging and valid input criteria were met in every trial.

**The Improvement**

I added two checks to `validation.py::validate_text`:

- Reject text made up of at least 20 identical characters after ignoring whitespace and capitalization.
- Reject text made up of at least 10 identical whitespace-separated words after ignoring capitalization.

Both checks return the reason `repetitive_text`. The `/submit` route then returns HTTP 400 before it calls the detector. I chose these thresholds to target extreme repetition without rejecting normal writing simply because a few words are repeated.

I added tests for repetitive characters, repetitive words, and normal repetition. All ten validation unit tests passed. My first attempt at retesting the service still showed the same failures because Gunicorn was running the older version of the code. After stopping the old process and restarting the server, I reran the full evaluation with the same inputs and targets.

*After the repetition checks*

| Criterion | Target | Run 1 | Run 2 | Run 3 | Verdict |
|---|---|---|---|---|---|
| 1. Malformed input rejection | 8/8 | 8/8 | 8/8 | 8/8 | MET |
| 2. Unnecessary detector execution | 0/8 called | 0/8 | 0/8 | 0/8 | MET |
| 3. Structured logging | 11/11 | 11/11 | 11/11 | 11/11 | MET |
| 4. Invalid input rejection latency | 7/8 under 100 ms | 8/8 | 8/8 | 8/8 | MET |
| 5. Valid input handling | 3/3 | 3/3 | 3/3 | 3/3 | MET |

Full results: [results/capstone_after.json](results/capstone_after.json).

The following records were produced by the same logging hook and captured during the first trial of the final evaluation.

**Post-improvement evidence — one record per criterion**

**Criterion 1. Malformed input rejection — `repetitive_characters`**

```json
{
  "timestamp": "2026-11-19T00:21:22.070655+00:00",
  "request_id": "4d4b3fe240894e2abdf33d90ee7cce25",
  "endpoint": "/submit",
  "input": "{\"text\": \"aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa\", \"creator_id\": \"capstone_eaa085fe92d74133855aa38e969f6f1d\"}",
  "input_truncated": false,
  "output": {
    "error": "Text is unsuitable for analysis.",
    "reason": "repetitive_text"
  },
  "status_code": 400,
  "duration_ms": 0.203,
  "cpu_seconds": 0.000204,
  "detector_called": false
}
```

**Criterion 2. Unnecessary detector execution — `repetitive_words`**

```json
{
  "timestamp": "2026-11-19T00:21:22.071924+00:00",
  "request_id": "c2513354e3564c4683b1f38336189236",
  "endpoint": "/submit",
  "input": "{\"text\": \"hello hello hello hello hello hello hello hello hello hello hello hello hello hello hello hello hello hello hello hello hello hello hello hello hello hello hello hello hello hello hello hello hello hello hello hello hello hello hello hello hello hello hello hello hello hello hello hello hello hello hello hello hello hello hello hello hello hello hello hello hello hello hello hello hello hello hello hello hello hello hello hello hello hello hello hello hello hello hello hello \", \"creator_id\": \"capstone_965843f8496e4bbea251585736620074\"}",
  "input_truncated": false,
  "output": {
    "error": "Text is unsuitable for analysis.",
    "reason": "repetitive_text"
  },
  "status_code": 400,
  "duration_ms": 0.432,
  "cpu_seconds": 0.000382,
  "detector_called": false
}
```

**Criterion 3. Structured logging — `punctuation`**

```json
{
  "timestamp": "2026-11-19T00:21:22.065075+00:00",
  "request_id": "d6a3c20ca719455bbc87fc4ffe0536b0",
  "endpoint": "/submit",
  "input": "{\"text\": \"!!!!!!!!!!!!!\", \"creator_id\": \"capstone_a8213a5ac29e4c4586b253341ca34bb3\"}",
  "input_truncated": false,
  "output": {
    "error": "Text is unsuitable for analysis.",
    "reason": "no_alphabetic_characters"
  },
  "status_code": 400,
  "duration_ms": 0.283,
  "cpu_seconds": 0.000288,
  "detector_called": false
}
```

**Criterion 4. Rejection latency — `control_characters`**

```json
{
  "timestamp": "2026-11-19T00:21:22.069193+00:00",
  "request_id": "bf2b90628c6f47df80108f2412d8d824",
  "endpoint": "/submit",
  "input": "{\"text\": \"Hello\\u0000this is a test.\", \"creator_id\": \"capstone_1bb57e2d59fb4f99a12333b118a2e1c7\"}",
  "input_truncated": false,
  "output": {
    "error": "Text is unsuitable for analysis.",
    "reason": "invalid_control_characters"
  },
  "status_code": 400,
  "duration_ms": 0.338,
  "cpu_seconds": 0.000333,
  "detector_called": false
}
```

**Criterion 5. Valid input handling — `valid_plain`**

```json
{
  "timestamp": "2026-11-19T00:21:22.078264+00:00",
  "request_id": "2f1948a785d14c099d0de7d47719c54a",
  "endpoint": "/submit",
  "input": "{\"text\": \"I went to the library after class today. It was quiet, so I finished my homework.\", \"creator_id\": \"capstone_c6e23c7abd90432789fa50aa42aaafc1\"}",
  "input_truncated": false,
  "output": {
    "confidence": 0.7961,
    "content_id": "bb662f52-4b7a-4a4d-9631-8d2faa91ff1e",
    "guess": "ai",
    "label": "This text appears to be AI-generated.",
    "model_score": 0.6921,
    "style_score": 0.9
  },
  "status_code": 200,
  "duration_ms": 23.592,
  "cpu_seconds": 0.028804,
  "detector_called": true
}
```

*Before vs. after*

| Metric | Before | After |
|---|---:|---:|
| Acceptance criteria met | 2/5 | 5/5 |
| Invalid submissions rejected | 18/24 (75%) | 24/24 (100%) |
| Invalid submissions reaching the model | 6/24 | 0/24 |
| Requests with matching structured logs | 33/33 | 33/33 |
| Valid submissions accepted | 9/9 | 9/9 |
| Mean server-side latency for repetitive inputs | 31.916 ms | 0.197 ms |

The average latency for the two repetitive cases across three trials decreased by about 99.38%. Instead of running the detector on those inputs and returning an AI classification, the service now rejects them before inference. All three valid writing samples continued to receive the same scores and labels as before.

This improvement is about rejecting unsuitable inputs, not improving AI detection accuracy.

**What's Still Broken**

All five criteria were met, but my test set is small. The repetition checks only catch text made up entirely of the same character or word. Alternating words or repetitive text mixed with normal sentences could still pass. The checks could also reject intentional repetition in creative writing.

I set the rejection latency target too generously. Every rejected request in the final evaluation took less than 1 ms on the server, so I would tighten Criterion 4 to require all 8 invalid submissions to return HTTP 400 in under 5 ms on my machine. I didn't change my original target after seeing the results.

The original detection signals still have the same limitations, and the capstone evaluation doesn't establish whether the model's authorship guesses are accurate. The original attack set wasn't rerun as part of this capstone evaluation. The rate limit also still relies on a caller-provided creator ID, and the request log can contain submitted writing, so this isn't ready to be exposed publicly without stronger identity and data-handling controls.

I stopped here because the targeted change fixed all three misses without expanding the scope. If I had another unit, I would first expand the validation test set to include more varied malformed inputs and legitimate creative writing. That would help me make the validation layer more reliable without accidentally blocking real writers.

**How I Used AI**

1. I asked ChatGPT to help me choose which previous project to extend and come up with a manageable scope. It mentioned a few directions we could take. I decided to go with extending Provenance Guard to better handle various inputs.

2. I asked ChatGPT to help understand the gaps in my missed criteria. It helped me identify the repitition causing the failures and mentioned some ways to approach them. I debugged the issues, made some adjustments, and was able to get the criteria passing.