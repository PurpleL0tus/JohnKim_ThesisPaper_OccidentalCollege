# Regular Expression Generation with Brute-Force Algorithm

**John Kim** — Occidental College

[Full paper (PDF)](paper.pdf)

---

## Abstract

Regular Expression, also known as Regex, is a sequence of symbols, numbers, and characters that represents a search pattern and/or text manipulations. It is highly versatile and widely supported across many programming languages.

This project aims to automate the task of generating regex utilizing a brute force algorithm. Given an example of a regex output, the code will conduct pre-processing of relevant keywords to simplify the task and find the search-pattern utilizing a brute force algorithm.

---

## Technical Background

### Byte Pair Encoding

In natural language processing, tokenization is the process of converting text to smaller interchangeable units called tokens. These tokens can then be re-arranged to form completely new sentences.

Byte Pair Encoding is a well established tokenization algorithm. It finds and merges the most common pairs of adjacent characters in a given corpus until the word reaches a set size, creating tokens that efficiently represent text. BPE is an algorithm designed with Natural Language Processing in mind and did not perform seamlessly as you could expect from a text based corpus. BPE algorithm was utilized in a corpus of regular expressions. Some manual filtering was required afterwards, but it was able to recognize common token pairs such as `.*`

### Standard Deviation

Standard deviation is a statistical measurement that quantifies the amount of variation in a set of values. A low standard deviation indicates that the data points tend to be close to the mean, whereas a high standard deviation indicates that the values are more spread out over a wider range. Standard Deviation was utilized in conjunction with the brute force algorithm. Its purpose is to randomly determine the number of tokens used in the algorithm with a statistical focus on the mean. The algorithm assumes a mean of 3 tokens and gradually increases the value of standard deviation. Eventually, as the graph nears a flat line, a random number between 1 and 10 is chosen as the token count.

### Regex-based Denial of Service (ReDoS)

ReDoS is a DoS attack caused by algorithmic complexity that drains a given web-service's resources due to its costly time complexity. The time complexity can grow exponentially or polynomially as its input size increases linearly.

Most regex functions have an exponential time worst-case complexity but they are often overlooked during development as they are often, but not always, rarely triggered with genuine inputs. ReDoS failures occur when such a regex function is given a maliciously crafted input or a genuine input that triggers exponential/polynomial backtracking. Programming languages predominantly use backtracking for their regex search algorithm — most notable examples are C#, Java, JavaScript, and Python. Its computational cost is negligible in most use cases, but it can sometimes be detrimental.

#### 2019 Cloudflare Outage

Sometimes a regular expression function can consistently cause ReDoS failures even on genuine inputs. One such example is the 2019 Cloudflare global outage. Cloudflare is a company that provides a number of internet services, one of which is Content Delivery Network (CDN) services. To combat Cross-site Scripting attacks through their CDN, they implemented a regular expression to their firewall that detects any JavaScript and HTML code appended to URLs.

```
(?:(?:\"|'|\]|\}|\\|\d|(?:nan|infinity|true|false|null|undefined|symbol|math)|\`|\-|\+)+[)]*;?((?:\s|-|~|!|{}|\|\||\+)*.*(?:.*=.*)))
```

The malformed section that caused the outage was `.*(?:.*=.*)`. Disregarding the non-capturing group `(?:)`, we are left with:

```
.*.*=.*
```

<img src="Regular_Expression_Generation_with_Brute_Force_Algorithm/matching-x-x.png" width="500"/>

*Exponential time complexity of Cloudflare's malformed regex*

The first two `.*` will match greedily and then both would backtrack, iterating backwards one unit at a time until it finds an equal-sign or until all possibilities are exhausted. It takes 23 steps to match a string as simple as `x=x`, 33 steps for `x=xx`, and 45 for `x=xxx`. The complexity is exponential and much worse if the string does not contain an equal-sign — it will take 4,067 steps to compute a string that is 20 characters long without one. Considering how long URLs can get, you can see how this would cause an outage.

The outage demonstrates the disastrous potential of ReDoS failures and how inconspicuous they can be to users. Unfortunately, the program is not able to detect and mitigate ReDoS failures.

#### Linear Time Regular Expression

Since the 2019 outage, Cloudflare has switched to the Rust regex engine for their regex needs. The Rust engine is deterministic and runs in linear time: O(N).

Deterministic regular expressions such as re2 and the Rust regex engine achieve linear time complexity by utilizing a combination of Deterministic Finite Automata (DFA) and Non-Deterministic Finite Automata (NFA), allowing them to avoid backtracking. The primary limitation of such engines is the high memory requirements for complex regexes.

Users are encouraged to use a linear time engine. It is possible for the brute force algorithm to generate regex with exponential time worst-case complexity which may lead to a ReDoS failure.

### Prior Work

Prior works in the field of automated Regular Expression generation is limited. This may speak to its difficulty or insignificance even if successfully implemented.

#### Genetic Programming for Regex Generation

A team of researchers at the University of Trieste in Italy utilized genetic programming to automate regular expression generation as a so-called proof of concept. Their findings were limited. Their research did demonstrate an abstract potential for such an algorithm. However, it only demonstrated that it's able to utilize genetic programming to generate regular expressions with manual post-processing. Their proof of concept failed to independently generate any coherent regular expression. Furthermore, their algorithm was tested on a very limited sample size of two.

---

## Methods

<img src="Regular_Expression_Generation_with_Brute_Force_Algorithm/Picture9.png" width="500"/>

*Program overview*

The program conducts pre-processing of keywords provided based on user inputs in order to simplify them as much as possible. Then the brute force algorithm, utilizing both Byte Pair Encoded tokens and Standard Deviation number generation, generates potential regular expressions. Once the correct regex is found, it is then outputted.

The shorter token list is used for the Brute Force Algorithm, which contains the most common regular expression tokens. When the list fails to generate the correct regex, the complete list is used.

<img src="Regular_Expression_Generation_with_Brute_Force_Algorithm/Picture1.png" width="380"/>

*Keyword pre-processing examples*

---

## Results

Results were averaged from 10 trials. The results show that the brute force algorithm is able to consistently generate the correct regular expression when the non-keyword tokens are limited to 5 maximum. The algorithm, however, was not able to reliably generate longer, more complex regular expressions.

| Target Pattern | Avg. Time (s) | Avg. Attempts |
|---|---|---|
| `\d[Gg]upp(ies\|y)?$` | 1.37 | 126,026 |
| `^d[Gg]upp(ies\|y)?$` | 28.33 | 2,610,318 |
| `\b\D[Gg]upp(ies\|y)?\b` | 37.57 | 3,389,479 |
| `^(John\|Han\|Luke\|Leia)$` | 0.05 | 4,435 |

---

## User Interface

<img src="Regular_Expression_Generation_with_Brute_Force_Algorithm/UI pic.png" width="320"/>

---

## Quick Start

```bash
pip install -r requirements.txt
python main.py
```

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
