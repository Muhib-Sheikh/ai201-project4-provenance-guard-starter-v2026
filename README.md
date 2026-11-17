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

**Did it help, and how do I know:**

<!-- Widening the unsure band usually fixes one problem and creates another.
     Reporting that trade honestly is worth full credit. -->

Yes, raising the AI threshold reduced false positives from 2/10 to 0/10 across all three trials, and all five criteria are now met. FP02 and FP05 are no longer flagged as AI, but EV10 now avoids detection. The number of AI samples correctly labeled as AI also dropped from 2/5 to 1/5.

The system is less likely to falsely accuse human writers, but the trade-off is that more AI-generated writing gets through.

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
