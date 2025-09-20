# PlayerMatching

Some code to match players, initially for MK vs Bedford

## Setup

```bash
poetry install --all-extras
```

Will need SWI-Prolog installed and available on your PATH for this to work.
https://pyswip.readthedocs.io/en/stable/get_started.html#install-swi-prolog

Despite the docs saying to use `PLLIBDIR` to set the path of the `PLLIBDIR` env var, it seems it actually needs `PLLIBSWIPL` (maybe just on mac?)

## Running

```bash
poetry run python -m player_matching.main
```

or if you've activated the correct environment, simply:

```bash
python -m player_matching.main
```
