# jif

The `if` statement, finally powered by AI.

For 70 years, conditional branching has been held back by a primitive technology: the CPU.
`jif` replaces it with [Jev](https://www.datacamp.com/blog/system-one-models-jev), a frontier *System One* model
that returns calibrated, typed decisions. Every branch in your program is now evaluated by a model.

```python
# coding: jif
jif temperature > 30:
    print("it's hot")
eljif mood == "hangry":
    print("serve snickers")
else:
    print("serve water")
```

Yes, that's real syntax. No, you don't need to import anything.

## Why jif?

| | `if` (legacy) | `jif` |
|---|---|---|
| Latency | ~1 ns | 70 to 500 ms (enterprise grade) |
| Cost per branch | $0 | ~$0.0004 |
| Accuracy | 100% (boring) | 67.8%\* |
| Understands intent | no | yes |
| Calibrated confidence | no | yes, `jif.last_probability` |
| Needs internet to branch | no | yes |
| Deterministic | yes | we don't talk about that |

\* Jev's reported score on TypeSafe's benchmark, statistically indistinguishable from GPT-5.6 Terra.

### It understands natural language

Legacy `if` makes you write *code*. `jif` just gets it:

```python
# coding: jif
message = "I have been waiting 3 weeks for my refund. This is unacceptable."

jif message sounds like the customer is angry:
    escalate_to_human()
```

Your PM can now write conditions. Should they? Not our problem.

### Zero type errors, guaranteed

Jev *mathematically cannot* return anything but a probability. That's a stronger type guarantee than your codebase has.

## Install

```bash
pip install git+https://github.com/ChristopherKotthoff/jif-py
export AI_GATEWAY_API_KEY=...   # Vercel AI Gateway key, branching is a premium feature
```

Add `# coding: jif` as the first line of any file and start using `jif` / `eljif`.

Not ready to commit to a new keyword? The function form works in plain Python and reads your local variables automatically:

```python
from jif import jif

if jif("x > 5"):
    ...
```

Feeling risky? `JIF_THRESHOLD=0.3` makes your program more optimistic.

## How it works

1. A `.pth` file registers a source codec named `jif` when Python starts.
2. `# coding: jif` makes Python run your file through that codec, which rewrites `jif <expr>:` into `if jif("<expr>"):`.
3. At runtime, `jif` takes the expression text and the values of every variable it mentions,
   then sends them to `typesafe-ai/jev` via the Vercel AI Gateway.
4. Jev returns the probability that the condition is true, and we branch on it.
   Python never evaluates your expression itself. That's what the AI is for.

## FAQ

**Is this production ready?** It has tests.

**Should I use this?** Your cloud bill says yes.

**Is it deterministic?** No.

**Isn't this shooting pigeons with a cannon?** The pigeons have never been shot this accurately, at least 67.8% of the time.

## Tests

```bash
python test_jif.py   # offline checks; with AI_GATEWAY_API_KEY set it also asks Jev for real
```

MIT. Also available for JavaScript: [jif-js](https://github.com/ChristopherKotthoff/jif-js).
