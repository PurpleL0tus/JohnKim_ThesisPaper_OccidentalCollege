# Regular Expression Generation with Brute-Force Algorithm

**John Kim** — Occidental College

---

## Abstract

Regular expressions (regex) are sequences of symbols and characters that represent search patterns and text manipulations. They are highly versatile and widely supported across programming languages.

This project automates regex generation using a brute-force algorithm. Given a target regex pattern, the program pre-processes relevant keywords to simplify the search space, then uses a brute-force algorithm to find the correct pattern.

---

## Technical Background

### Byte Pair Encoding (BPE)

BPE is a tokenization algorithm from NLP. It finds and merges the most frequent adjacent character pairs in a corpus until tokens reach a target size. Here, BPE was applied to a corpus of regular expressions to identify common token pairs like `.*`. Some manual filtering was required since BPE was designed for natural language, not regex syntax.

### Standard Deviation in Token Count

Standard deviation is used to randomly determine how many tokens are assembled per attempt. The algorithm assumes a mean of 3 tokens and gradually widens the standard deviation over time. Once the distribution approaches a flat line, token count switches to a uniform random draw between 1 and 10.

### Regex-based Denial of Service (ReDoS)

Most regex engines use backtracking, which can have exponential worst-case time complexity. ReDoS attacks exploit this by crafting inputs that force catastrophic backtracking.

**2019 Cloudflare Outage** — Cloudflare's WAF contained this regex:

```
(?:(?:\"|'|\]|\}|\\|\d|(?:nan|infinity|true|false|null|undefined|symbol|math)|\`|\-|\+)+[)]*;?((?:\s|-|~|!|{}|\|\||\+)*.*(?:.*=.*)))
```

The malformed section `.*(?:.*=.*)` — simplified to `.*.*=.*` — caused exponential backtracking. A 20-character string with no `=` required over 4,000 steps. This took down Cloudflare's global network.

![Exponential time complexity of Cloudflare's malformed regex](Regular_Expression_Generation_with_Brute_Force_Algorithm/matching-x-x.png)

Since the outage, Cloudflare has moved to the Rust regex engine, which uses a DFA/NFA hybrid to guarantee linear `O(n)` time. Users of this tool are encouraged to validate generated patterns with a linear-time engine, as the brute-force algorithm can produce patterns with exponential worst-case complexity.

### Prior Work

Prior work on automated regex generation is limited. A team at the University of Trieste used genetic programming as a proof of concept, but their approach required manual post-processing and was only tested on two cases — failing to independently generate any coherent expression.

---

## How It Works

![Program overview](Regular_Expression_Generation_with_Brute_Force_Algorithm/Picture9.png)

1. **Keyword pre-processing** — similar keywords are merged into compact regex alternations (e.g. `guppies` + `guppy` → `gupp(ies|y)`, `Apple` + `apple` → `[Aa]pple`)
2. **Token pool** — BPE-derived tokens from a regex corpus define the building blocks
3. **Brute-force search** — tokens are assembled randomly, with token count drawn from a normal distribution centered at 3, widening over time
4. **Validation** — each candidate is checked against a user-defined acceptance function

![Keyword pre-processing examples](Regular_Expression_Generation_with_Brute_Force_Algorithm/Picture1.png)

---

## Results

Averaged over 10 trials:

| Target Pattern | Avg. Time (s) | Avg. Attempts |
|---|---|---|
| `\d[Gg]upp(ies\|y)?$` | 1.37 | 126,026 |
| `^d[Gg]upp(ies\|y)?$` | 28.33 | 2,610,318 |
| `\b\D[Gg]upp(ies\|y)?\b` | 37.57 | 3,389,479 |
| `^(John\|Han\|Luke\|Leia)$` | 0.05 | 4,435 |

The algorithm reliably finds correct patterns when non-keyword tokens are capped at 5. It struggles with longer, more complex targets.

---

## Installation

```bash
pip install -r requirements.txt
```

Requires Python 3.10+.

---

## Usage

**Run the generator:**
```bash
python main.py
```

Edit the keyword list and acceptance function in `main.py` to target a specific pattern.

**Run the brute-force experiment:**
```bash
python random_generate.py
```

Set `TARGET` and `KEYWORD` in `random_generate.py` to benchmark a specific pattern.

**Run the BPE tokenizer on the regex corpus:**
```bash
python BPEer.py
```

**Launch the GUI:**
```bash
python user_interface.py
```

![User interface](Regular_Expression_Generation_with_Brute_Force_Algorithm/UI%20pic.png)

---

## Project Structure

```
main.py              # entry point — keyword processing + brute-force loop
keywords.py          # keyword pre-processing and merging
tools.py             # token pool and regex validation
math_stuff.py        # normal distribution for token count sampling
regex_generator.py   # standalone valid-regex generator
random_generate.py   # brute-force benchmark experiment
BPEer.py             # byte pair encoding on regex corpus
corpus.py            # loads data.json and builds corpus.txt
user_interface.py    # tkinter GUI
tests.py             # test suite
```
