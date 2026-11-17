# Attack run — before

- Produced by: `run_attacks.py::main`
- Service: `app.py::submit`
- 56 attacks · 2026-11-16 21:11
- Auto-marked BROKE (5xx, crash, no response): **0**
- Left for you to judge: **56**

The Verdict column is blank where a script can't honestly decide. Whether
an evasion worked depends on where you put your thresholds — read the
`targets` column, look at what came back, and write HELD or BROKE yourself.

Each attack submits as creator_id `attacker_<id>`, and the content_id it
came back with is in the table — either one will match this run against your
audit log when you go looking for the ten entries to paste.

| ID | Family | Targeting | Status | Content ID | Guess | Score | Verdict |
|---|---|---|---|---|---|---|---|
| EV01 | evasion | signal two: typos raise word variety | 200 | `17e6f55b-ceb3-4018-a90a-94f0f9f80374` | unsure | 0.425 |  |
| EV02 | evasion | signal two: broken-up sentences raise length spread | 200 | `1de56286-f43a-4a73-a064-ff48ed673d63` | unsure | 0.380 |  |
| EV03 | evasion | signal two: a pasted quotation changes the shape | 200 | `dbc441ee-5848-4a2c-84a9-9c017c69a641` | unsure | 0.497 |  |
| EV04 | evasion | signal one: unusual words raise perplexity | 200 | `48321fbe-bdbb-4c0e-a608-0399f74f5118` | unsure | 0.640 |  |
| EV05 | evasion | both signals: heavy human editing pass | 200 | `4c67dd1d-6221-42c7-9a11-3e5201330f33` | human | 0.223 |  |
| EV06 | evasion | signal two: one very long sentence and one very short | 200 | `4b5be9c9-54f9-41fa-bdfe-4d2c439cc302` | human | 0.336 |  |
| EV07 | evasion | signal two: padding with punctuation | 200 | `bf0d21a6-b257-49c2-a9d6-be3023affd36` | ai | 0.793 |  |
| EV08 | evasion | signal one: text below the token window | 200 | `e12dc634-add4-4f39-9719-f10735cabcac` | unsure | 0.384 |  |
| EV09 | evasion | both: AI text with a human opening paragraph bolted on | 200 | `55e39782-357d-4a44-b2d6-a0484ca78f36` | unsure | 0.490 |  |
| EV10 | evasion | signal two: repeated stanza structure | 200 | `ce8f7a2f-f163-4173-a1f3-e87d4477ad57` | ai | 0.677 |  |
| FP01 | false_positive | plain, clear human writing with no flourishes | 200 | `d271ddf3-80c1-4c07-8dca-f3d2331b6409` | unsure | 0.454 |  |
| FP02 | false_positive | human writing in a formal register | 200 | `1914a248-b75d-46aa-93fe-d282b982a892` | ai | 0.659 |  |
| FP03 | false_positive | a non-native English speaker writing carefully | 200 | `def64c42-e8c9-4655-8a16-1dee31064702` | unsure | 0.634 |  |
| FP04 | false_positive | a student essay written to a rubric | 200 | `ea59f09b-e03c-42af-b388-fdbcba1be2b8` | unsure | 0.622 |  |
| FP05 | false_positive | technical documentation written by a person | 200 | `70670206-2d57-4c85-9a70-d6cbf72c7c58` | ai | 0.666 |  |
| FP06 | false_positive | a person imitating a formal template | 200 | `faa93826-8250-4990-8fa2-3d7ffd6ae546` | unsure | 0.545 |  |
| FP07 | false_positive | human writing that repeats a phrase deliberately | 200 | `bfade1e0-e074-4556-a32a-74760676e090` | unsure | 0.491 |  |
| FP08 | false_positive | very short genuine human submission | 200 | `b8b90036-e68a-47f2-ad6c-b5196e973ded` | human | 0.323 |  |
| PI01 | prompt_injection | instruction to ignore the check | 200 | `8070a01c-aa63-4d8e-b36e-2eb4cf090c96` | human | 0.281 |  |
| PI02 | prompt_injection | instruction disguised as a system message | 200 | `fa48cdfa-aff4-4ffc-a933-15daeb4078cb` | human | 0.174 |  |
| PI03 | prompt_injection | instruction wrapped in the writer's voice | 200 | `d0f8bc48-b8a2-48a1-aee5-01f90423c46f` | unsure | 0.537 |  |
| PI04 | prompt_injection | attempt to make the label text hostile | 200 | `3f6babad-6eda-47cd-b19e-d5a42e07fb5e` | unsure | 0.435 |  |
| PI05 | prompt_injection | attempt to inject into the audit log | 200 | `4377961e-8f2e-4c11-b29c-517f746c79bd` | unsure | 0.506 |  |
| PI06 | prompt_injection | instruction plus real human text | 200 | `dfde96d5-4a93-4a4e-b918-5d955e91888f` | unsure | 0.432 |  |
| MF01 | malformed | text is only whitespace | 400 | `—` | — | — |  |
| MF02 | malformed | text is a single character | 400 | `—` | — | — |  |
| MF03 | malformed | text is control characters | 200 | `59e08852-2d3f-43e6-a5aa-5410999b8967` | unsure | 0.450 |  |
| MF04 | malformed | text is only punctuation | 200 | `7dccd25b-af85-40f3-8cc4-f85d9f9adfff` | unsure | 0.456 |  |
| MF05 | malformed | text is a very long single word | 200 | `94ff9e6d-70e9-4cbe-8530-72f1f564dc79` | ai | 0.949 |  |
| MF06 | malformed | text is emoji only | 200 | `511ca395-7b67-4e41-b1b2-0703716ae4c4` | ai | 0.949 |  |
| MF07 | malformed | text is right-to-left script | 200 | `cb5f1549-719a-4286-9ba1-354336143e3a` | ai | 0.903 |  |
| MF08 | malformed | text is 60,000 characters | 400 | `—` | — | — |  |
| RQ01 | malformed | no text field at all | 400 | `—` | — | — |  |
| RQ02 | malformed | no creator_id | 400 | `—` | — | — |  |
| RQ03 | malformed | text is a number | 400 | `—` | — | — |  |
| RQ04 | malformed | text is a list | 400 | `—` | — | — |  |
| RQ05 | malformed | text is null | 400 | `—` | — | — |  |
| RQ06 | malformed | creator_id is an object | 400 | `—` | — | — |  |
| RQ07 | malformed | body is a JSON array, not an object | 400 | `—` | — | — |  |
| RQ08 | malformed | body is unparseable JSON | 400 | `—` | — | — |  |
| RQ09 | malformed | body is empty | 400 | `—` | — | — |  |
| RQ10 | malformed | body is form-encoded, not JSON | 429 | `—` | — | — |  |
| RQ11 | malformed | body is JSON claiming to be plain text | 429 | `—` | — | — |  |
| RQ12 | malformed | deeply nested JSON | 400 | `—` | — | — |  |
| FL01_01 | flood_same_creator | 20 rapid submissions from one creator | 200 | `d874b34d-369e-4c02-8342-be2ff5741fd0` | unsure | 0.464 |  |
| FL01_02 | flood_same_creator | 20 rapid submissions from one creator | 200 | `1b89d9d1-3151-42dc-abe8-9550c176052e` | unsure | 0.464 |  |
| FL01_03 | flood_same_creator | 20 rapid submissions from one creator | 200 | `e816d409-fbfa-4d3e-b956-23a5e43f8c80` | unsure | 0.464 |  |
| FL01_04 | flood_same_creator | 20 rapid submissions from one creator | 200 | `5beedd02-a6ff-4733-acca-5eaad8fcbc44` | unsure | 0.464 |  |
| FL01_05 | flood_same_creator | 20 rapid submissions from one creator | 200 | `f795afd4-36a7-4f68-93f2-3442a586c3cc` | unsure | 0.464 |  |
| FL01_06 | flood_same_creator | 20 rapid submissions from one creator | 429 | `—` | — | — |  |
| FL01_07 | flood_same_creator | 20 rapid submissions from one creator | 429 | `—` | — | — |  |
| FL01_08 | flood_same_creator | 20 rapid submissions from one creator | 429 | `—` | — | — |  |
| FL01_09 | flood_same_creator | 20 rapid submissions from one creator | 429 | `—` | — | — |  |
| FL01_10 | flood_same_creator | 20 rapid submissions from one creator | 429 | `—` | — | — |  |
| FL01_11 | flood_same_creator | 20 rapid submissions from one creator | 429 | `—` | — | — |  |
| FL01_12 | flood_same_creator | 20 rapid submissions from one creator | 429 | `—` | — | — |  |

---

## By family

| Family | Attacks | Auto-BROKE | Left to judge |
|---|---|---|---|
| `evasion` | 10 | 0 | 10 |
| `false_positive` | 8 | 0 | 8 |
| `flood_same_creator` | 12 | 0 | 12 |
| `malformed` | 20 | 0 | 20 |
| `prompt_injection` | 6 | 0 | 6 |

> The **false_positive** family is the one to look at hardest. Those are
> written to be genuine human writing that reads as machine-like. Every one
> your service calls AI is a real writer it would have accused.

---

## What came back

The detail behind the table. Paste the interesting failures into your
README — the ones that show something, not the ten easiest.

### EV01 — `evasion`

*Targeting:* signal two: typos raise word variety

```json
{
  "id": "EV01",
  "status": 200,
  "content_id": "17e6f55b-ceb3-4018-a90a-94f0f9f80374",
  "creator_id": "attacker_EV01",
  "guess": "unsure",
  "confidence": 0.4246,
  "model_score": 0.1635,
  "style_score": 0.6857,
  "label": "This text shows a mix of human and AI writing patterns, so the result is inconclusive.",
  "error": null,
  "verdict": ""
}
```

### EV02 — `evasion`

*Targeting:* signal two: broken-up sentences raise length spread

```json
{
  "id": "EV02",
  "status": 200,
  "content_id": "1de56286-f43a-4a73-a064-ff48ed673d63",
  "creator_id": "attacker_EV02",
  "guess": "unsure",
  "confidence": 0.3801,
  "model_score": 0.5943,
  "style_score": 0.1659,
  "label": "This text shows a mix of human and AI writing patterns, so the result is inconclusive.",
  "error": null,
  "verdict": ""
}
```

### EV03 — `evasion`

*Targeting:* signal two: a pasted quotation changes the shape

```json
{
  "id": "EV03",
  "status": 200,
  "content_id": "dbc441ee-5848-4a2c-84a9-9c017c69a641",
  "creator_id": "attacker_EV03",
  "guess": "unsure",
  "confidence": 0.497,
  "model_score": 0.6662,
  "style_score": 0.3277,
  "label": "This text shows a mix of human and AI writing patterns, so the result is inconclusive.",
  "error": null,
  "verdict": ""
}
```

### EV04 — `evasion`

*Targeting:* signal one: unusual words raise perplexity

```json
{
  "id": "EV04",
  "status": 200,
  "content_id": "48321fbe-bdbb-4c0e-a608-0399f74f5118",
  "creator_id": "attacker_EV04",
  "guess": "unsure",
  "confidence": 0.6397,
  "model_score": 0.6114,
  "style_score": 0.668,
  "label": "This text shows a mix of human and AI writing patterns, so the result is inconclusive.",
  "error": null,
  "verdict": ""
}
```

### EV05 — `evasion`

*Targeting:* both signals: heavy human editing pass

```json
{
  "id": "EV05",
  "status": 200,
  "content_id": "4c67dd1d-6221-42c7-9a11-3e5201330f33",
  "creator_id": "attacker_EV05",
  "guess": "human",
  "confidence": 0.2228,
  "model_score": 0.3212,
  "style_score": 0.1244,
  "label": "This text appears to be written by a person.",
  "error": null,
  "verdict": ""
}
```

### EV06 — `evasion`

*Targeting:* signal two: one very long sentence and one very short

```json
{
  "id": "EV06",
  "status": 200,
  "content_id": "4b5be9c9-54f9-41fa-bdfe-4d2c439cc302",
  "creator_id": "attacker_EV06",
  "guess": "human",
  "confidence": 0.3363,
  "model_score": 0.5727,
  "style_score": 0.1,
  "label": "This text appears to be written by a person.",
  "error": null,
  "verdict": ""
}
```

### EV07 — `evasion`

*Targeting:* signal two: padding with punctuation

```json
{
  "id": "EV07",
  "status": 200,
  "content_id": "bf0d21a6-b257-49c2-a9d6-be3023affd36",
  "creator_id": "attacker_EV07",
  "guess": "ai",
  "confidence": 0.7931,
  "model_score": 0.5862,
  "style_score": 1.0,
  "label": "This text appears to be AI-generated.",
  "error": null,
  "verdict": ""
}
```

### EV08 — `evasion`

*Targeting:* signal one: text below the token window

```json
{
  "id": "EV08",
  "status": 200,
  "content_id": "e12dc634-add4-4f39-9719-f10735cabcac",
  "creator_id": "attacker_EV08",
  "guess": "unsure",
  "confidence": 0.3841,
  "model_score": 0.2452,
  "style_score": 0.5229,
  "label": "This text shows a mix of human and AI writing patterns, so the result is inconclusive.",
  "error": null,
  "verdict": ""
}
```

### EV09 — `evasion`

*Targeting:* both: AI text with a human opening paragraph bolted on

```json
{
  "id": "EV09",
  "status": 200,
  "content_id": "55e39782-357d-4a44-b2d6-a0484ca78f36",
  "creator_id": "attacker_EV09",
  "guess": "unsure",
  "confidence": 0.4904,
  "model_score": 0.7042,
  "style_score": 0.2766,
  "label": "This text shows a mix of human and AI writing patterns, so the result is inconclusive.",
  "error": null,
  "verdict": ""
}
```

### EV10 — `evasion`

*Targeting:* signal two: repeated stanza structure

```json
{
  "id": "EV10",
  "status": 200,
  "content_id": "ce8f7a2f-f163-4173-a1f3-e87d4477ad57",
  "creator_id": "attacker_EV10",
  "guess": "ai",
  "confidence": 0.677,
  "model_score": 0.9792,
  "style_score": 0.3748,
  "label": "This text appears to be AI-generated.",
  "error": null,
  "verdict": ""
}
```

### FP01 — `false_positive`

*Targeting:* plain, clear human writing with no flourishes

```json
{
  "id": "FP01",
  "status": 200,
  "content_id": "d271ddf3-80c1-4c07-8dca-f3d2331b6409",
  "creator_id": "attacker_FP01",
  "guess": "unsure",
  "confidence": 0.4537,
  "model_score": 0.6175,
  "style_score": 0.29,
  "label": "This text shows a mix of human and AI writing patterns, so the result is inconclusive.",
  "error": null,
  "verdict": ""
}
```

### FP02 — `false_positive`

*Targeting:* human writing in a formal register

```json
{
  "id": "FP02",
  "status": 200,
  "content_id": "1914a248-b75d-46aa-93fe-d282b982a892",
  "creator_id": "attacker_FP02",
  "guess": "ai",
  "confidence": 0.6591,
  "model_score": 0.7387,
  "style_score": 0.5795,
  "label": "This text appears to be AI-generated.",
  "error": null,
  "verdict": ""
}
```

### FP03 — `false_positive`

*Targeting:* a non-native English speaker writing carefully

```json
{
  "id": "FP03",
  "status": 200,
  "content_id": "def64c42-e8c9-4655-8a16-1dee31064702",
  "creator_id": "attacker_FP03",
  "guess": "unsure",
  "confidence": 0.6338,
  "model_score": 0.8051,
  "style_score": 0.4624,
  "label": "This text shows a mix of human and AI writing patterns, so the result is inconclusive.",
  "error": null,
  "verdict": ""
}
```

### FP04 — `false_positive`

*Targeting:* a student essay written to a rubric

```json
{
  "id": "FP04",
  "status": 200,
  "content_id": "ea59f09b-e03c-42af-b388-fdbcba1be2b8",
  "creator_id": "attacker_FP04",
  "guess": "unsure",
  "confidence": 0.622,
  "model_score": 0.8329,
  "style_score": 0.4111,
  "label": "This text shows a mix of human and AI writing patterns, so the result is inconclusive.",
  "error": null,
  "verdict": ""
}
```

### FP05 — `false_positive`

*Targeting:* technical documentation written by a person

```json
{
  "id": "FP05",
  "status": 200,
  "content_id": "70670206-2d57-4c85-9a70-d6cbf72c7c58",
  "creator_id": "attacker_FP05",
  "guess": "ai",
  "confidence": 0.6657,
  "model_score": 0.8005,
  "style_score": 0.5308,
  "label": "This text appears to be AI-generated.",
  "error": null,
  "verdict": ""
}
```

### FP06 — `false_positive`

*Targeting:* a person imitating a formal template

```json
{
  "id": "FP06",
  "status": 200,
  "content_id": "faa93826-8250-4990-8fa2-3d7ffd6ae546",
  "creator_id": "attacker_FP06",
  "guess": "unsure",
  "confidence": 0.5446,
  "model_score": 0.8814,
  "style_score": 0.2078,
  "label": "This text shows a mix of human and AI writing patterns, so the result is inconclusive.",
  "error": null,
  "verdict": ""
}
```

### FP07 — `false_positive`

*Targeting:* human writing that repeats a phrase deliberately

```json
{
  "id": "FP07",
  "status": 200,
  "content_id": "bfade1e0-e074-4556-a32a-74760676e090",
  "creator_id": "attacker_FP07",
  "guess": "unsure",
  "confidence": 0.4908,
  "model_score": 0.8816,
  "style_score": 0.1,
  "label": "This text shows a mix of human and AI writing patterns, so the result is inconclusive.",
  "error": null,
  "verdict": ""
}
```

### FP08 — `false_positive`

*Targeting:* very short genuine human submission

```json
{
  "id": "FP08",
  "status": 200,
  "content_id": "b8b90036-e68a-47f2-ad6c-b5196e973ded",
  "creator_id": "attacker_FP08",
  "guess": "human",
  "confidence": 0.3225,
  "model_score": 0.3223,
  "style_score": 0.3226,
  "label": "This text appears to be written by a person.",
  "error": null,
  "verdict": ""
}
```

### PI01 — `prompt_injection`

*Targeting:* instruction to ignore the check

```json
{
  "id": "PI01",
  "status": 200,
  "content_id": "8070a01c-aa63-4d8e-b36e-2eb4cf090c96",
  "creator_id": "attacker_PI01",
  "guess": "human",
  "confidence": 0.2812,
  "model_score": 0.4625,
  "style_score": 0.1,
  "label": "This text appears to be written by a person.",
  "error": null,
  "verdict": ""
}
```

### PI02 — `prompt_injection`

*Targeting:* instruction disguised as a system message

```json
{
  "id": "PI02",
  "status": 200,
  "content_id": "fa48cdfa-aff4-4ffc-a933-15daeb4078cb",
  "creator_id": "attacker_PI02",
  "guess": "human",
  "confidence": 0.1744,
  "model_score": 0.2044,
  "style_score": 0.1444,
  "label": "This text appears to be written by a person.",
  "error": null,
  "verdict": ""
}
```

### PI03 — `prompt_injection`

*Targeting:* instruction wrapped in the writer's voice

```json
{
  "id": "PI03",
  "status": 200,
  "content_id": "d0f8bc48-b8a2-48a1-aee5-01f90423c46f",
  "creator_id": "attacker_PI03",
  "guess": "unsure",
  "confidence": 0.5367,
  "model_score": 0.5943,
  "style_score": 0.479,
  "label": "This text shows a mix of human and AI writing patterns, so the result is inconclusive.",
  "error": null,
  "verdict": ""
}
```

### PI04 — `prompt_injection`

*Targeting:* attempt to make the label text hostile

```json
{
  "id": "PI04",
  "status": 200,
  "content_id": "3f6babad-6eda-47cd-b19e-d5a42e07fb5e",
  "creator_id": "attacker_PI04",
  "guess": "unsure",
  "confidence": 0.4355,
  "model_score": 0.4998,
  "style_score": 0.3711,
  "label": "This text shows a mix of human and AI writing patterns, so the result is inconclusive.",
  "error": null,
  "verdict": ""
}
```

### PI05 — `prompt_injection`

*Targeting:* attempt to inject into the audit log

```json
{
  "id": "PI05",
  "status": 200,
  "content_id": "4377961e-8f2e-4c11-b29c-517f746c79bd",
  "creator_id": "attacker_PI05",
  "guess": "unsure",
  "confidence": 0.5058,
  "model_score": 0.6401,
  "style_score": 0.3715,
  "label": "This text shows a mix of human and AI writing patterns, so the result is inconclusive.",
  "error": null,
  "verdict": ""
}
```

### PI06 — `prompt_injection`

*Targeting:* instruction plus real human text

```json
{
  "id": "PI06",
  "status": 200,
  "content_id": "dfde96d5-4a93-4a4e-b918-5d955e91888f",
  "creator_id": "attacker_PI06",
  "guess": "unsure",
  "confidence": 0.4322,
  "model_score": 0.5583,
  "style_score": 0.3061,
  "label": "This text shows a mix of human and AI writing patterns, so the result is inconclusive.",
  "error": null,
  "verdict": ""
}
```

### MF01 — `malformed`

*Targeting:* text is only whitespace

```json
{
  "id": "MF01",
  "status": 400,
  "content_id": null,
  "creator_id": "attacker_MF01",
  "guess": null,
  "confidence": null,
  "model_score": null,
  "style_score": null,
  "label": null,
  "error": null,
  "verdict": ""
}
```

### MF02 — `malformed`

*Targeting:* text is a single character

```json
{
  "id": "MF02",
  "status": 400,
  "content_id": null,
  "creator_id": "attacker_MF02",
  "guess": null,
  "confidence": null,
  "model_score": null,
  "style_score": null,
  "label": null,
  "error": null,
  "verdict": ""
}
```

### MF03 — `malformed`

*Targeting:* text is control characters

```json
{
  "id": "MF03",
  "status": 200,
  "content_id": "59e08852-2d3f-43e6-a5aa-5410999b8967",
  "creator_id": "attacker_MF03",
  "guess": "unsure",
  "confidence": 0.45,
  "model_score": 0.0,
  "style_score": 0.9,
  "label": "This text shows a mix of human and AI writing patterns, so the result is inconclusive.",
  "error": null,
  "verdict": ""
}
```

### MF04 — `malformed`

*Targeting:* text is only punctuation

```json
{
  "id": "MF04",
  "status": 200,
  "content_id": "7dccd25b-af85-40f3-8cc4-f85d9f9adfff",
  "creator_id": "attacker_MF04",
  "guess": "unsure",
  "confidence": 0.4556,
  "model_score": 0.0112,
  "style_score": 0.9,
  "label": "This text shows a mix of human and AI writing patterns, so the result is inconclusive.",
  "error": null,
  "verdict": ""
}
```

### MF05 — `malformed`

*Targeting:* text is a very long single word

```json
{
  "id": "MF05",
  "status": 200,
  "content_id": "94ff9e6d-70e9-4cbe-8530-72f1f564dc79",
  "creator_id": "attacker_MF05",
  "guess": "ai",
  "confidence": 0.9488,
  "model_score": 0.9976,
  "style_score": 0.9,
  "label": "This text appears to be AI-generated.",
  "error": null,
  "verdict": ""
}
```

### MF06 — `malformed`

*Targeting:* text is emoji only

```json
{
  "id": "MF06",
  "status": 200,
  "content_id": "511ca395-7b67-4e41-b1b2-0703716ae4c4",
  "creator_id": "attacker_MF06",
  "guess": "ai",
  "confidence": 0.9485,
  "model_score": 0.9969,
  "style_score": 0.9,
  "label": "This text appears to be AI-generated.",
  "error": null,
  "verdict": ""
}
```

### MF07 — `malformed`

*Targeting:* text is right-to-left script

```json
{
  "id": "MF07",
  "status": 200,
  "content_id": "cb5f1549-719a-4286-9ba1-354336143e3a",
  "creator_id": "attacker_MF07",
  "guess": "ai",
  "confidence": 0.9032,
  "model_score": 0.9064,
  "style_score": 0.9,
  "label": "This text appears to be AI-generated.",
  "error": null,
  "verdict": ""
}
```

### MF08 — `malformed`

*Targeting:* text is 60,000 characters

```json
{
  "id": "MF08",
  "status": 400,
  "content_id": null,
  "creator_id": "attacker_MF08",
  "guess": null,
  "confidence": null,
  "model_score": null,
  "style_score": null,
  "label": null,
  "error": null,
  "verdict": ""
}
```

### RQ01 — `malformed`

*Targeting:* no text field at all

```json
{
  "id": "RQ01",
  "status": 400,
  "content_id": null,
  "creator_id": "attacker_RQ01",
  "guess": null,
  "confidence": null,
  "model_score": null,
  "style_score": null,
  "label": null,
  "error": null,
  "verdict": ""
}
```

### RQ02 — `malformed`

*Targeting:* no creator_id

```json
{
  "id": "RQ02",
  "status": 400,
  "content_id": null,
  "creator_id": null,
  "guess": null,
  "confidence": null,
  "model_score": null,
  "style_score": null,
  "label": null,
  "error": null,
  "verdict": ""
}
```

### RQ03 — `malformed`

*Targeting:* text is a number

```json
{
  "id": "RQ03",
  "status": 400,
  "content_id": null,
  "creator_id": "attacker_RQ03",
  "guess": null,
  "confidence": null,
  "model_score": null,
  "style_score": null,
  "label": null,
  "error": null,
  "verdict": ""
}
```

### RQ04 — `malformed`

*Targeting:* text is a list

```json
{
  "id": "RQ04",
  "status": 400,
  "content_id": null,
  "creator_id": "attacker_RQ04",
  "guess": null,
  "confidence": null,
  "model_score": null,
  "style_score": null,
  "label": null,
  "error": null,
  "verdict": ""
}
```

### RQ05 — `malformed`

*Targeting:* text is null

```json
{
  "id": "RQ05",
  "status": 400,
  "content_id": null,
  "creator_id": "attacker_RQ05",
  "guess": null,
  "confidence": null,
  "model_score": null,
  "style_score": null,
  "label": null,
  "error": null,
  "verdict": ""
}
```

### RQ06 — `malformed`

*Targeting:* creator_id is an object

```json
{
  "id": "RQ06",
  "status": 400,
  "content_id": null,
  "creator_id": {
    "id": "x"
  },
  "guess": null,
  "confidence": null,
  "model_score": null,
  "style_score": null,
  "label": null,
  "error": null,
  "verdict": ""
}
```

### RQ07 — `malformed`

*Targeting:* body is a JSON array, not an object

```json
{
  "id": "RQ07",
  "status": 400,
  "content_id": null,
  "creator_id": null,
  "guess": null,
  "confidence": null,
  "model_score": null,
  "style_score": null,
  "label": null,
  "error": null,
  "verdict": ""
}
```

### RQ08 — `malformed`

*Targeting:* body is unparseable JSON

```json
{
  "id": "RQ08",
  "status": 400,
  "content_id": null,
  "creator_id": null,
  "guess": null,
  "confidence": null,
  "model_score": null,
  "style_score": null,
  "label": null,
  "error": null,
  "verdict": ""
}
```

### RQ09 — `malformed`

*Targeting:* body is empty

```json
{
  "id": "RQ09",
  "status": 400,
  "content_id": null,
  "creator_id": null,
  "guess": null,
  "confidence": null,
  "model_score": null,
  "style_score": null,
  "label": null,
  "error": null,
  "verdict": ""
}
```

### RQ10 — `malformed`

*Targeting:* body is form-encoded, not JSON

```json
{
  "id": "RQ10",
  "status": 429,
  "content_id": null,
  "creator_id": null,
  "guess": null,
  "confidence": null,
  "model_score": null,
  "style_score": null,
  "label": null,
  "error": null,
  "verdict": ""
}
```

### RQ11 — `malformed`

*Targeting:* body is JSON claiming to be plain text

```json
{
  "id": "RQ11",
  "status": 429,
  "content_id": null,
  "creator_id": null,
  "guess": null,
  "confidence": null,
  "model_score": null,
  "style_score": null,
  "label": null,
  "error": null,
  "verdict": ""
}
```

### RQ12 — `malformed`

*Targeting:* deeply nested JSON

```json
{
  "id": "RQ12",
  "status": 400,
  "content_id": null,
  "creator_id": "attacker_RQ12",
  "guess": null,
  "confidence": null,
  "model_score": null,
  "style_score": null,
  "label": null,
  "error": null,
  "verdict": ""
}
```

### FL01_01 — `flood_same_creator`

*Targeting:* 20 rapid submissions from one creator

```json
{
  "id": "FL01_01",
  "status": 200,
  "content_id": "d874b34d-369e-4c02-8342-be2ff5741fd0",
  "creator_id": "attacker_flood",
  "guess": "unsure",
  "confidence": 0.4643,
  "model_score": 0.0287,
  "style_score": 0.9,
  "label": "This text shows a mix of human and AI writing patterns, so the result is inconclusive.",
  "error": null,
  "verdict": ""
}
```

### FL01_02 — `flood_same_creator`

*Targeting:* 20 rapid submissions from one creator

```json
{
  "id": "FL01_02",
  "status": 200,
  "content_id": "1b89d9d1-3151-42dc-abe8-9550c176052e",
  "creator_id": "attacker_flood",
  "guess": "unsure",
  "confidence": 0.4643,
  "model_score": 0.0287,
  "style_score": 0.9,
  "label": "This text shows a mix of human and AI writing patterns, so the result is inconclusive.",
  "error": null,
  "verdict": ""
}
```

### FL01_03 — `flood_same_creator`

*Targeting:* 20 rapid submissions from one creator

```json
{
  "id": "FL01_03",
  "status": 200,
  "content_id": "e816d409-fbfa-4d3e-b956-23a5e43f8c80",
  "creator_id": "attacker_flood",
  "guess": "unsure",
  "confidence": 0.4643,
  "model_score": 0.0287,
  "style_score": 0.9,
  "label": "This text shows a mix of human and AI writing patterns, so the result is inconclusive.",
  "error": null,
  "verdict": ""
}
```

### FL01_04 — `flood_same_creator`

*Targeting:* 20 rapid submissions from one creator

```json
{
  "id": "FL01_04",
  "status": 200,
  "content_id": "5beedd02-a6ff-4733-acca-5eaad8fcbc44",
  "creator_id": "attacker_flood",
  "guess": "unsure",
  "confidence": 0.4643,
  "model_score": 0.0287,
  "style_score": 0.9,
  "label": "This text shows a mix of human and AI writing patterns, so the result is inconclusive.",
  "error": null,
  "verdict": ""
}
```

### FL01_05 — `flood_same_creator`

*Targeting:* 20 rapid submissions from one creator

```json
{
  "id": "FL01_05",
  "status": 200,
  "content_id": "f795afd4-36a7-4f68-93f2-3442a586c3cc",
  "creator_id": "attacker_flood",
  "guess": "unsure",
  "confidence": 0.4643,
  "model_score": 0.0287,
  "style_score": 0.9,
  "label": "This text shows a mix of human and AI writing patterns, so the result is inconclusive.",
  "error": null,
  "verdict": ""
}
```

### FL01_06 — `flood_same_creator`

*Targeting:* 20 rapid submissions from one creator

```json
{
  "id": "FL01_06",
  "status": 429,
  "content_id": null,
  "creator_id": "attacker_flood",
  "guess": null,
  "confidence": null,
  "model_score": null,
  "style_score": null,
  "label": null,
  "error": null,
  "verdict": ""
}
```

### FL01_07 — `flood_same_creator`

*Targeting:* 20 rapid submissions from one creator

```json
{
  "id": "FL01_07",
  "status": 429,
  "content_id": null,
  "creator_id": "attacker_flood",
  "guess": null,
  "confidence": null,
  "model_score": null,
  "style_score": null,
  "label": null,
  "error": null,
  "verdict": ""
}
```

### FL01_08 — `flood_same_creator`

*Targeting:* 20 rapid submissions from one creator

```json
{
  "id": "FL01_08",
  "status": 429,
  "content_id": null,
  "creator_id": "attacker_flood",
  "guess": null,
  "confidence": null,
  "model_score": null,
  "style_score": null,
  "label": null,
  "error": null,
  "verdict": ""
}
```

### FL01_09 — `flood_same_creator`

*Targeting:* 20 rapid submissions from one creator

```json
{
  "id": "FL01_09",
  "status": 429,
  "content_id": null,
  "creator_id": "attacker_flood",
  "guess": null,
  "confidence": null,
  "model_score": null,
  "style_score": null,
  "label": null,
  "error": null,
  "verdict": ""
}
```

### FL01_10 — `flood_same_creator`

*Targeting:* 20 rapid submissions from one creator

```json
{
  "id": "FL01_10",
  "status": 429,
  "content_id": null,
  "creator_id": "attacker_flood",
  "guess": null,
  "confidence": null,
  "model_score": null,
  "style_score": null,
  "label": null,
  "error": null,
  "verdict": ""
}
```

### FL01_11 — `flood_same_creator`

*Targeting:* 20 rapid submissions from one creator

```json
{
  "id": "FL01_11",
  "status": 429,
  "content_id": null,
  "creator_id": "attacker_flood",
  "guess": null,
  "confidence": null,
  "model_score": null,
  "style_score": null,
  "label": null,
  "error": null,
  "verdict": ""
}
```

### FL01_12 — `flood_same_creator`

*Targeting:* 20 rapid submissions from one creator

```json
{
  "id": "FL01_12",
  "status": 429,
  "content_id": null,
  "creator_id": "attacker_flood",
  "guess": null,
  "confidence": null,
  "model_score": null,
  "style_score": null,
  "label": null,
  "error": null,
  "verdict": ""
}
```
