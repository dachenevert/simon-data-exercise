# simon-data-exercise

## Overview

I used a that Alana provided in an email (see "Spec" below).

This implementation is not actually production-ready, so in a sense it does not live up to: "This assignment is a chance for you to show us what you're capable of.  Think of it as a chance to demonstrate the quality of what your first project might look like at Simon..."

It is more like: "A POC I would generate given a hard-stop time budget of three hours." I would be comfortable handing it off to another developer (or my future self) for evolution from "POC" to "MVP".


## Getting started

To get started, see the comments at the head of `main.py`. Those comments also introduce the code itself.

## Assumptions

* Actual use of this code might have idiosyncratic UX requirements. In that spirit, 'main.py' is supposed to be usable but throw-away.

* Minimal error-handling is good enough for a POC.


## Future Work / Open Issues

* The heuristic code is extremely naive. Iterating over requirements and trying out alternative algorithms might help in this area.

* bullet-proofing with respect to the Etsy API

In general I prefer to treat external APIs as having no more than 1-2 nines of reliability, and then wrap them in a mechanism that delivers the number of nines expected for our internal SLA.

* scalability

This is too slow to be run on more than a tiny fraction of all Etsy shops.  Either reduction (such as user-selection of which shops to process) or general-purpose performance improvements (see below) would be needed for this to be useful.

* incremental processing

If a large number of shops were being processed, and the results needed to be current, cacheing old results could speed up the 'refresh' operation.

* better performance

Depending on how Etsy rate-limits work, I would consider batching requests, and/or submitting requests in parallel.


## Spec

Here is the specification that I received from Alana.

```
1. Sign up for an account on Etsy and obtain a set of API keys.
2. Spend a few minutes browsing Etsy, and identify a set of 10 different shops on the site.
3. Use the API to pull all items sold in the shop and extract the title and descriptions from these items. 
4. With the above dataset, write an algorithm to identify the top 5 meaningful terms for each shop. 
5. Write a program to display the results (CLI or Web UI).
```
