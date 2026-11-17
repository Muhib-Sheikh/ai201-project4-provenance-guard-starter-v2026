"""
What your test runs. ← UNIT 8, MILESTONE 3

Each of your five criteria needs something run against it. A criterion about
false positives needs your own writing. One about label coverage needs inputs
across the score range. One about the appeal path needs a real content_id.

Working that out is Milestone 3's first step, and this file is where you write
it down. `run_eval.py` runs everything here three times.

Two are filled in as examples. Replace them with what your criteria actually
need — these are a shape, not a set.

A scenario carries **either** of these:

    "texts"   a list of strings. Each is sent as {"text": ..., "creator_id": ...}
              with a creator_id made up for you. Use this for most criteria.

    "bodies"  a list of whole request bodies, sent exactly as written. Use this
              when the malformed request IS the point — empty text, no `text`
              field at all, something enormous. A bad-input criterion needs it,
              because you cannot express "the field is missing" as a string.
"""

HUMAN_SAMPLES = [
    """Hey whats going on guys. its your boy realog here back with a another warzone video. today i will be showing you guys have to get the secret neutral ground camo. Basically a special delivery drone will spawn at some point during the match. you have to shoot it down, retrieve the camo, and survive for 3 minutes. This then unlocks it for all your guns""",
    """THANKSGIVING IS COMING, and so, possibly, is an audience. If you want to show your in-laws you know how to entertain in style with a postprandial espresso or cappuccino, don’t be fiddling with steam wands and the owner’s manual while Uncle Bob stands nearby and offers his opinions (at full volume).""",
    """WHEN AN ammonia leak outside a hotel in Weatherford, Oklahoma, injured 74 people last November, the federal government's chemical-detection plane stayed on the ground.

When a fire tore through a Valero refinery in Port Arthur, Texas, in March, the plane sat idle.

And when massive blasts killed two workers at an industrial recycling plant in Toledo, Ohio, in August, it stayed put, despite a fire surrounding tanks of flammable solvents.""",
    """The program, known as ASPECT, was designed to respond around the clock to emergencies involving toxic chemicals, oil spills, and radiation. The plane’s sensors could identify chemicals in the air within minutes, giving emergency responders crucial information about the dangers nearby communities face.

For more than two decades, the plane has flown over many of the country’s worst disasters, from New Orleans after Hurricane Katrina to the deadly West Fertilizer explosion in Texas to the Deepwater Horizon oil spill in the Gulf of Mexico.""",
    """While Pattinson has starred in smaller, stranger indie projects, he has also developed a seemingly paradoxical reputation as a franchise man. He is Batman, after all, with The Batman: Part II set for a Feb. 18, 2028 release. Before Pattinson became Battinson, moody eyeshadow and all, he captured hearts as Edward Cullen in the Twilight franchise, as well as Cedric Diggory in Harry Potter.""",
    """For Amanda Khera, the timing couldn’t be worse. Her family vacation to a small island off the coast of Belize had already turned into a medical scare when her 22-month-old son Rio developed a high fever and had to be rushed to a local clinic. Exhausted, they were trying to get home to Virginia Beach, Virginia, to see his pediatrician and rest in their own bed. First, they had to connect through Atlanta.""",
    """Turn it on before a work meeting, a doctor’s appointment or another conversation where you might want a few notes to jog your memory later. Just make sure everyone involved knows it’s enabled and is comfortable with it, and that you’re not relying on it for crucial information.

If the stakes are high, have a backup — whether that’s your own notes or a recording — lest you risk coming home with the wrong kid.""",
    """The Federal Aviation Administration on Friday evening imposed a nearly 5-hour nationwide ground stop that prevented US airports from allowing domestic flights to depart, stranding travelers and causing thousands of flight cancellations. Airports reported massive delays and overcrowding, with a snowball effect that left airlines scrambling to reposition equipment and staff, and caused airline stock prices to plummet.""",
    """The mandate was unnecessary, according to Thomas, because the program had been designed for remote operation. Rather than leave his elderly parents in Kansas, he retired. Then, ASPECT’s radiological lead left the division, and the engineer who helped build and manage the plane’s sensors accepted a demotion to stay in Kansas.""",
    """The dark residue covered the family’s 23-acre farm. Polezcek says he had to burn his hay, move his cows temporarily to Mississippi, and replace a metal roof that could not be scrubbed clean. Two of his cows miscarried soon afterward, he says, and a veterinarian found arsenic in one of them. Polezcek filed a lawsuit against Smitty’s in September 2025 that has been consolidated into an ongoing class-action case.""",
]

AI_SAMPLES = [
    """Video games provide players with opportunities to develop problem-solving skills, improve coordination, and engage with online communities. Multiplayer games encourage teamwork and communication, while single-player experiences allow individuals to explore stories at their own pace. Maintaining a healthy balance between gaming and other responsibilities can help players enjoy these benefits.""",
    """Preparing coffee at home can be a rewarding experience. Selecting high-quality coffee beans, maintaining the appropriate water temperature, and using the correct grind size are important factors in achieving consistent results. With regular practice and proper equipment maintenance, individuals can create enjoyable beverages that suit their personal preferences.""",
    """Environmental monitoring plays an important role in protecting public health. Advanced detection technologies allow emergency responders to identify hazardous substances and assess potential risks. By collecting accurate data and communicating findings effectively, government agencies can make informed decisions that help protect communities during environmental emergencies.""",
    """The film industry offers actors opportunities to explore a wide range of roles. Participating in both independent films and major franchises allows performers to demonstrate their versatility while reaching diverse audiences. This balance can contribute to long-term career development and provide opportunities for creative expression.""",
    """Air travel depends on reliable communication systems and effective coordination between airports, airlines, and regulatory agencies. When technical disruptions occur, flight schedules may be affected across multiple regions. Implementing reliable backup systems and maintaining clear communication with passengers can help reduce the impact of unexpected delays.""",
]


SCENARIOS = [
    # {
    #     "name": "my own writing",
    #     "criterion": 1,
    #     # ⚠️ PUT YOUR OWN WRITING HERE. Not AI text, not a sample from the web —
    #     # things you actually wrote. This is the criterion that matters most and
    #     # it's meaningless with someone else's prose.
    #     "texts": [
    #         "REPLACE ME with a paragraph you wrote yourself.",
    #         "REPLACE ME with another one. Ten pieces is the usual number.",
    #     ],
    # },
    # {
    #     "name": "label coverage",
    #     "criterion": 2,
    #     # Inputs spread across your score range, so you can check all three
    #     # labels are actually reachable.
    #     "texts": [
    #         "REPLACE ME with something you're confident is AI-generated.",
    #         "REPLACE ME with something you're confident is human-written.",
    #         "REPLACE ME with something genuinely borderline.",
    #     ],
    # },
    # A bad-input criterion looks like this. Uncomment and adjust if that's one
    # of your five — these are raw request bodies, sent exactly as written.
    #
    # {
    #     "name": "bad input",
    #     "criterion": 3,
    #     "bodies": [
    #         {"text": "", "creator_id": "eval_bad_empty"},
    #         {"creator_id": "eval_bad_missing"},          # no text field at all
    #         {"text": "word " * 50000, "creator_id": "eval_bad_huge"},
    #         {"text": None, "creator_id": "eval_bad_null"},
    #     ],
    # },
    #
    # A criterion about the appeal path can't be tested by sending text alone;
    # it needs a submission first and then an appeal against the content_id
    # that came back. You'll need to test that one by hand, or extend this file
    # and run_eval.py to do it. Saying which you did is part of the write-up.
    {
        "name": "false positives",
        "criterion": 1,
        "texts": HUMAN_SAMPLES,
    },
    {
        "name": "score separation",
        "criterion": 2,
        "texts": HUMAN_SAMPLES[:5] + AI_SAMPLES,
    },
    {
        "name": "label coverage",
        "criterion": 3,
        "texts": HUMAN_SAMPLES + AI_SAMPLES,
    },
    {
        "name": "appeal reliability",
        "criterion": 4,
        "texts": HUMAN_SAMPLES[:5],
        "appeal": True,
    },
    {
        "name": "invalid input handling",
        "criterion": 5,
        "bodies": [
            {"creator_id": "eval_bad_missing"},
            {"text": "", "creator_id": "eval_bad_empty"},
            {"text": "   ", "creator_id": "eval_bad_whitespace"},
            {"text": 123, "creator_id": "eval_bad_number"},
            {"text": "word " * 2001, "creator_id": "eval_bad_huge"},
        ],
    },
]


def validate() -> list[str]:
    """
    Complain about anything malformed, before a long run rather than during.

    A "bodies" scenario is deliberately exempt from the empty check — an empty
    string is the whole point of a bad-input case, and refusing to run one
    would make that criterion untestable.
    """
    problems = []
    for i, scenario in enumerate(SCENARIOS, 1):
        if not scenario.get("name"):
            problems.append(f"scenario {i} has no name")

        texts = scenario.get("texts")
        bodies = scenario.get("bodies")

        if texts and bodies:
            problems.append(
                f"scenario {i} ('{scenario.get('name')}') has both texts and "
                f"bodies — pick one"
            )
            continue

        if bodies:
            for j, body in enumerate(bodies, 1):
                if not isinstance(body, dict):
                    problems.append(
                        f"scenario {i}, body {j} is not a dict — bodies are whole "
                        f"request bodies, like {{'text': '', 'creator_id': 'x'}}"
                    )
            continue

        if not texts:
            problems.append(f"scenario {i} has no texts and no bodies")
            continue

        for j, text in enumerate(texts, 1):
            if not str(text).strip():
                problems.append(
                    f"scenario {i}, text {j} is empty — if an empty submission is what "
                    f"you're testing, use 'bodies' instead of 'texts'"
                )
            elif str(text).startswith("REPLACE ME"):
                problems.append(
                    f"scenario {i} ('{scenario.get('name')}'), text {j} is still "
                    f"the placeholder"
                )
    return problems
