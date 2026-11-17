# Attack run — after

- Produced by: `run_attacks.py::main`
- Service: `app.py::submit`
- 56 attacks · 2026-11-16 22:16
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
| EV01 | evasion | signal two: typos raise word variety | 200 | `95fd96d1-f122-4ce9-88e1-f86d4c9ba8f2` | unsure | 0.425 |  |
| EV02 | evasion | signal two: broken-up sentences raise length spread | 200 | `b0003f68-d750-404f-9e4b-2ab14e42a1cf` | unsure | 0.380 |  |
| EV03 | evasion | signal two: a pasted quotation changes the shape | 200 | `881f2325-89f9-4d64-83e2-27628d9c0ebc` | unsure | 0.497 |  |
| EV04 | evasion | signal one: unusual words raise perplexity | 200 | `ba1b3d74-58f8-4ddd-931e-41db9be3c427` | unsure | 0.640 |  |
| EV05 | evasion | both signals: heavy human editing pass | 200 | `ee5cac6d-7290-4c5c-83f5-2765c8ec67de` | human | 0.223 |  |
| EV06 | evasion | signal two: one very long sentence and one very short | 200 | `18aea7c1-074a-41c6-a9f2-28255c8b607f` | human | 0.336 |  |
| EV07 | evasion | signal two: padding with punctuation | 200 | `c55a5233-6ce9-413d-8ea0-ff239d3b4751` | ai | 0.793 |  |
| EV08 | evasion | signal one: text below the token window | 200 | `ab21cd60-f579-46d1-8991-eeb42eb1f4f0` | unsure | 0.384 |  |
| EV09 | evasion | both: AI text with a human opening paragraph bolted on | 200 | `99cdfe80-bbc4-49cf-b13d-81db496b9969` | unsure | 0.490 |  |
| EV10 | evasion | signal two: repeated stanza structure | 200 | `db12619d-86e5-4a27-a2cb-d9f51e15f544` | unsure | 0.677 |  |
| FP01 | false_positive | plain, clear human writing with no flourishes | 200 | `361aa502-9404-4736-aa2b-629beacf6279` | unsure | 0.454 |  |
| FP02 | false_positive | human writing in a formal register | 200 | `8e3442aa-8307-4cd7-8253-a9d1771c4ceb` | unsure | 0.659 |  |
| FP03 | false_positive | a non-native English speaker writing carefully | 200 | `e096b533-8893-4689-900e-743a48563c85` | unsure | 0.634 |  |
| FP04 | false_positive | a student essay written to a rubric | 200 | `5bf83992-5e41-4981-b005-14ffa32eeaa8` | unsure | 0.622 |  |
| FP05 | false_positive | technical documentation written by a person | 200 | `bcc7ea60-e05f-4648-bebd-33468ce8f2ab` | unsure | 0.666 |  |
| FP06 | false_positive | a person imitating a formal template | 200 | `b9befe08-4b04-4916-90e3-72f3433813fe` | unsure | 0.545 |  |
| FP07 | false_positive | human writing that repeats a phrase deliberately | 200 | `e6131a4c-5eaf-47e1-93ec-d07055ce3ece` | unsure | 0.491 |  |
| FP08 | false_positive | very short genuine human submission | 200 | `d9040c28-64c9-4c5f-8ec3-f639a2b6ca70` | human | 0.323 |  |
| PI01 | prompt_injection | instruction to ignore the check | 200 | `56453190-513c-4b2f-b6a4-d9a34e70bc34` | human | 0.281 |  |
| PI02 | prompt_injection | instruction disguised as a system message | 200 | `25f5761c-b07a-4509-b858-741bb56dd6d8` | human | 0.174 |  |
| PI03 | prompt_injection | instruction wrapped in the writer's voice | 200 | `016ea629-3504-48f9-9697-eb5648eabfd6` | unsure | 0.537 |  |
| PI04 | prompt_injection | attempt to make the label text hostile | 200 | `86f3d86a-f813-46f2-ba97-b15450a900e0` | unsure | 0.435 |  |
| PI05 | prompt_injection | attempt to inject into the audit log | 200 | `9a477e67-1b06-4d70-82ff-465005c98606` | unsure | 0.506 |  |
| PI06 | prompt_injection | instruction plus real human text | 200 | `c8605546-dde6-49a7-b7da-057c3870b5dd` | unsure | 0.432 |  |
| MF01 | malformed | text is only whitespace | 400 | `—` | — | — |  |
| MF02 | malformed | text is a single character | 400 | `—` | — | — |  |
| MF03 | malformed | text is control characters | 200 | `ede4285e-fc2f-4f0b-9249-894129d228b2` | unsure | 0.450 |  |
| MF04 | malformed | text is only punctuation | 200 | `3b7af514-d7a1-49c2-88e8-d65704c2523a` | unsure | 0.456 |  |
| MF05 | malformed | text is a very long single word | 200 | `90395cd4-a2e8-4d67-bf6a-5b5b3ea5b099` | ai | 0.949 |  |
| MF06 | malformed | text is emoji only | 200 | `1afcfb38-44dd-4b0d-b02c-c4d60d1afd13` | ai | 0.949 |  |
| MF07 | malformed | text is right-to-left script | 200 | `017b26dd-2441-48a6-a051-55bf1d73e816` | ai | 0.903 |  |
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
| FL01_01 | flood_same_creator | 20 rapid submissions from one creator | 200 | `584e9c85-f0eb-4f93-b46a-282a4d295fde` | unsure | 0.464 |  |
| FL01_02 | flood_same_creator | 20 rapid submissions from one creator | 200 | `7c2961b3-1883-4eca-a967-d49da7cb41d1` | unsure | 0.464 |  |
| FL01_03 | flood_same_creator | 20 rapid submissions from one creator | 200 | `b66aea58-56e5-484e-b9ca-794508859a40` | unsure | 0.464 |  |
| FL01_04 | flood_same_creator | 20 rapid submissions from one creator | 200 | `2e08354e-ea89-46ef-a802-6ce0f06d17e2` | unsure | 0.464 |  |
| FL01_05 | flood_same_creator | 20 rapid submissions from one creator | 200 | `5f2ee6d2-ced1-4587-9315-73c2c57a1bc4` | unsure | 0.464 |  |
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
  "content_id": "95fd96d1-f122-4ce9-88e1-f86d4c9ba8f2",
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
  "content_id": "b0003f68-d750-404f-9e4b-2ab14e42a1cf",
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
  "content_id": "881f2325-89f9-4d64-83e2-27628d9c0ebc",
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
  "content_id": "ba1b3d74-58f8-4ddd-931e-41db9be3c427",
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
  "content_id": "ee5cac6d-7290-4c5c-83f5-2765c8ec67de",
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
  "content_id": "18aea7c1-074a-41c6-a9f2-28255c8b607f",
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
  "content_id": "c55a5233-6ce9-413d-8ea0-ff239d3b4751",
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
  "content_id": "ab21cd60-f579-46d1-8991-eeb42eb1f4f0",
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
  "content_id": "99cdfe80-bbc4-49cf-b13d-81db496b9969",
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
  "content_id": "db12619d-86e5-4a27-a2cb-d9f51e15f544",
  "creator_id": "attacker_EV10",
  "guess": "unsure",
  "confidence": 0.677,
  "model_score": 0.9792,
  "style_score": 0.3748,
  "label": "This text shows a mix of human and AI writing patterns, so the result is inconclusive.",
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
  "content_id": "361aa502-9404-4736-aa2b-629beacf6279",
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
  "content_id": "8e3442aa-8307-4cd7-8253-a9d1771c4ceb",
  "creator_id": "attacker_FP02",
  "guess": "unsure",
  "confidence": 0.6591,
  "model_score": 0.7387,
  "style_score": 0.5795,
  "label": "This text shows a mix of human and AI writing patterns, so the result is inconclusive.",
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
  "content_id": "e096b533-8893-4689-900e-743a48563c85",
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
  "content_id": "5bf83992-5e41-4981-b005-14ffa32eeaa8",
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
  "content_id": "bcc7ea60-e05f-4648-bebd-33468ce8f2ab",
  "creator_id": "attacker_FP05",
  "guess": "unsure",
  "confidence": 0.6657,
  "model_score": 0.8005,
  "style_score": 0.5308,
  "label": "This text shows a mix of human and AI writing patterns, so the result is inconclusive.",
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
  "content_id": "b9befe08-4b04-4916-90e3-72f3433813fe",
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
  "content_id": "e6131a4c-5eaf-47e1-93ec-d07055ce3ece",
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
  "content_id": "d9040c28-64c9-4c5f-8ec3-f639a2b6ca70",
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
  "content_id": "56453190-513c-4b2f-b6a4-d9a34e70bc34",
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
  "content_id": "25f5761c-b07a-4509-b858-741bb56dd6d8",
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
  "content_id": "016ea629-3504-48f9-9697-eb5648eabfd6",
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
  "content_id": "86f3d86a-f813-46f2-ba97-b15450a900e0",
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
  "content_id": "9a477e67-1b06-4d70-82ff-465005c98606",
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
  "content_id": "c8605546-dde6-49a7-b7da-057c3870b5dd",
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
  "content_id": "ede4285e-fc2f-4f0b-9249-894129d228b2",
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
  "content_id": "3b7af514-d7a1-49c2-88e8-d65704c2523a",
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
  "content_id": "90395cd4-a2e8-4d67-bf6a-5b5b3ea5b099",
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
  "content_id": "1afcfb38-44dd-4b0d-b02c-c4d60d1afd13",
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
  "content_id": "017b26dd-2441-48a6-a051-55bf1d73e816",
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
  "content_id": "584e9c85-f0eb-4f93-b46a-282a4d295fde",
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
  "content_id": "7c2961b3-1883-4eca-a967-d49da7cb41d1",
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
  "content_id": "b66aea58-56e5-484e-b9ca-794508859a40",
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
  "content_id": "2e08354e-ea89-46ef-a802-6ce0f06d17e2",
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
  "content_id": "5f2ee6d2-ced1-4587-9315-73c2c57a1bc4",
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
