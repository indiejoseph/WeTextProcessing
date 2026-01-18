# GitHub Copilot / AI Agent Instructions for WeTextProcessing

**Purpose:** Short, actionable guidance to help an AI coding agent be productive in this repository.

**Repository origin:** This project is a fork of https://github.com/wenet-e2e/WeTextProcessing and includes additional Cantonese support.

## Quick Architecture (big picture)
- Two main Python modules for text processing:
  - `tn/` (text normalization) — rule-based FST pipeline (tagger -> verbalizer -> processors).
  - `itn/` (inverse normalization) — complementary pipeline and tests.
- Each language lives under `tn/<language>` and follows the same pattern:
  - `normalizer.py` orchestrates `PreProcessor`, `Tagger`, `Verbalizer`, `PostProcessor`.
  - `rules/` contains modular rule classes (e.g., `cardinal.py`, `money.py`) with `.tagger` and `.verbalizer` FSTs.
  - `data/` contains TSV-driven mappings (consumed via `pynini.string_file`).
- FSTs are constructed via Pynini and cached; regenerating them can be expensive but necessary after changes.

## Key files and patterns to look at (examples)
- `tn/processor.py` — base `Processor` and helper `build_rule` used across languages.
- `tn/<lang>/normalizer.py` — Normalizer class exposing `normalize()` and how cache / OpenCC flags are handled.
- `tn/<lang>/rules/*.py` — rule classes that expose `tagger` and `verbalizer` FSTs.
- `tn/<lang>/data/*.tsv` — canonical place for string mappings (e.g., `simple_to_traditional.tsv`, `cantonese_overrides.tsv`).
- `tools/` — scripts to convert data/tests/code (e.g., `convert_to_traditional.py`, `generate_simple_to_traditional.py`).

## Developer workflows (commands) ✅
- Install deps: `python -m venv .venv && source .venv/bin/activate && pip install -r requirements.txt`.
- Optional extras (Cantonese tools): `pip install -e .[cantonese]` or `pip install opencc-python-reimplemented`.
- Run unit tests (single language): `./.venv/bin/pytest -q tn/cantonese/test`.
- Run full Python test suite: `./.venv/bin/python -m pytest -q`.
- Rebuild FST cache quickly during dev: instantiate Normalizer with `overwrite_cache=True`, e.g.
  - `n = Normalizer(overwrite_cache=True, simple_to_traditional=True)`
- Use the notebook `test.ipynb` for quick interactive checks (has Cantonese examples).

## Project-specific conventions and gotchas ⚠️
- Rule classes always expose `.tagger` and `.verbalizer` FSTs; they are assembled in `normalizer.build_tagger` / `build_verbalizer`.
- `PreProcessor` / `PostProcessor` are Pynini-based FSTs and applied via `build_rule(...)`.
- Data-driven mapping format: TSV files consumed with `pynini.string_file(...)` (one-to-one mapping lines).
- OpenCC is used for Simplified→Traditional conversions in Cantonese (`s2hk`). It is optional and invoked via `Normalzer(simple_to_traditional=True)`.
- When adding cross/insert/delete rules, remember to import the required Pynini helpers (`cross`, `accep`, `insert`, `delete`) to avoid runtime NameError.
- When converting language data/code to Traditional, prefer `tools/convert_to_traditional.py` and `tools/convert_code_to_traditional.py` to keep deterministic results.

## How to add or scaffold a new language (explicit steps)
1. Copy an existing language (example: `cp -a tn/chinese tn/<newlang>`).
2. Update package imports and identifiers in `tn/<newlang>/normalizer.py` and `tn/<newlang>/rules/*`.
3. Add/convert `data/` mappings; for Cantonese we used `OpenCC('s2hk')` + a `cantonese_overrides.tsv` for deterministic choices.
4. Add tests to `tn/<newlang>/test/` and update `test.ipynb` examples.
5. Run `pytest -q tn/<newlang>/test` and iterate — tests are the fast feedback loop.

## Debugging and common failure modes 🔍
- Pynini FSTOpError: often due to unexpected characters/inputs not covered in `data/` or wrong mapping direction. Inspect failing test phrase and add mapping or adjust pre/post-processor.
- NameError for Pynini helpers: ensure rule files include `from pynini import cross, accep, difference` and `from pynini.lib.pynutil import delete, insert` when used.
- Variant/lexical mismatches (e.g., Simplified vs Traditional): run the conversion tools and/or add an override TSV entry.
- Rebuild cache via `normalize(..., overwrite_cache=True)` when making FST changes.

## Tests & Examples to reference
- Unit tests: `tn/<lang>/test/normalizer_test.py` (contains parameterized examples used as the canonical spec for behavior).
- Notebook: `test.ipynb` (interactive usage notes and Cantonese examples).

## Integration & C/C++ runtime notes
- The repo contains runtime/processor C++ code and tests (`runtime/`, `processor/`) — changes in Python FSTs typically do not require editing C++ unless embedding consumers change.

## Useful file references (quick links)
- `tn/processor.py`, `tn/cantonese/normalizer.py`, `tn/cantonese/rules/postprocessor.py`, `tools/convert_to_traditional.py`, `test.ipynb`, `requirements.txt`, `setup.py`.

---

If any of these sections should be expanded with code snippets (e.g., example of a `cross` rule or an end-to-end add-language checklist), tell me which part you want more detail on and I'll iterate. ✅
