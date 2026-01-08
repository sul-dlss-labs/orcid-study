# orcid-study

This repository contains code for analyzing the effectiveness of using ORCID for obtaining publications from research intelligence publications like OpenAlex, Dimensions, Web of Science, PubMed.  The analysis uses approval and rejection signals in [sulpub] to determine the precision of publications obtained from the different platforms.

The data isn't committed to the repository, but can be obtained by:

1. `cp env.example` `.env`
2. add the `SULPUB_KEY` to `.env`
3. `uv run python data.py`
