from collections import namedtuple
from sys import exit as sys_exit
from requests import get as requests_get
from re import findall as re_findall
from math import sqrt as math_sqrt

"""
    SecretSauce's concerns are:
        the concept of 'meaningful'
        the concept of 'term'
        schema of data in an Etsy listing
        the algorithm that maps raw Etsy text to a 'meaningful' score
        generating an easy-to-use in-memory collection of results

    Its inputs are:
        text information about listings in shops, organized as a nested dictionary
            dict<{shop},dict<{item},[{title}, {description}]>>
        configuration (currently, "hard defaults")
            - relative importance of 'title' terms vs 'description' terms
            - how many 'meaningful terms' to report, per shop
            - minimum word length
            - list of 'weak' words to exclude

    Its outputs are:
        for each shop, its most 'meaningful' N terms

    Limits and restrictions
        Error processing and reporting are naive and rudimentary
        all heuristics and tuning are very quick and dirty. e.g.
            the list of 'weak words' is pretty weak itself
"""

class SecretSauce():
    def __init__(self):
        self.MEANINGFUL_TERM_COUNT = 5
        self.MINIMUM_WORD_LENGTH = 3
        self.TITLE_TERM_WEIGHT = 3
        self.WEAK_WORDS = set([
            'a',
            'an',
            'and',
            'it',
            'quot',
            'the',
            'this'
        ])
        pass

    def get_most_meaningful_terms(self, listings_by_shop):
        all_shops = list(listings_by_shop.keys())

        term_weights_by_shop = {}
        for shop in all_shops:
            term_weights = self.get_term_weights(listings_by_shop[shop])
            term_weights_by_shop[shop] = term_weights

        most_meaningful_terms_by_shop = {}

        # grades terms for each shop, and selects the most "meaningful" ones
        for shop in all_shops:
            sorted_terms = self.get_terms_sorted_by_meaning(shop, all_shops, term_weights_by_shop)
            most_meaningful_terms_by_shop[shop] = sorted_terms[-self.MEANINGFUL_TERM_COUNT:]

        return most_meaningful_terms_by_shop    # dict<shop, [term1, term2, ...]>

    # creates dictionary "<term, weighted-count-of-occurrences>"
    def get_term_weights(self, listings):
        term_weights = {}
        for listing in listings:
            self.add_term_weights_from_text(listing.get('title', ''),
                                            self.TITLE_TERM_WEIGHT,
                                            term_weights)
            self.add_term_weights_from_text(listing.get('description', ''),
                                            1,
                                            term_weights)
        return term_weights

    def add_term_weights_from_text(self, text, weight, term_weights):
        raw_words = re_findall('[\w]+', text.lower())
        strong_words = []
        for word in raw_words:
            if len(word) >= self.MINIMUM_WORD_LENGTH and word not in self.WEAK_WORDS:
                strong_words.append(word)

        # a term is either a single word or a N  words separated by spaces (currently N==2)
        terms = []
        for i in range(0, len(strong_words)):
            terms.append(strong_words[i])
            if i > 0:
                terms.append(strong_words[i-1] + ' ' + strong_words[i])

        for term in terms:
            term_weights[term] = term_weights.get(term, 0) + weight

    # process all terms for a single shop, and selects those that are most 'meaningful'
    def get_terms_sorted_by_meaning(self, shop, all_shops, term_weights_by_shop):
        meaning_scores = self.get_term_meaning_scores_this_shop(shop,
                                                                all_shops,
                                                                term_weights_by_shop)

        sorted_meaning_scores = sorted(meaning_scores.items(), key=lambda kv: kv[1])
        most_meaningful_score_kvps = sorted_meaning_scores[-self.MEANINGFUL_TERM_COUNT:]
        return list(map(lambda x: x[0], most_meaningful_score_kvps))

    def get_term_meaning_scores_this_shop(self, shop, all_shops, term_weights_by_shop):
        term_weights = term_weights_by_shop[shop]

        term_meaning_scores = {}
        for term in term_weights:
            weight_this_shop = term_weights[term]
            weight_other_shops = 0
            other_shops = [s for s in all_shops if shop != s]
            for other_shop in other_shops:
                weight_other_shops += term_weights_by_shop[other_shop].get(term, 0)
            term_meaning_scores[term] = self.get_term_meaning_score(term,
                                                                    weight_this_shop,
                                                                    weight_other_shops,
                                                                    len(other_shops))

        return term_meaning_scores

    # uses a few naive heuristics to assign a 'meaningful' score to a term
    def get_term_meaning_score(self, term, weight_this_shop, weight_other_shops, number_of_other_shops):
        # 'longer' and 'multi-word' are better
        length_score = math_sqrt(len(term)) * len(term.split(' '))
        # less popular is better
        average_weight_other_shops = weight_other_shops/number_of_other_shops
        relative_popularity_score = (weight_this_shop /
                                     math_sqrt((average_weight_other_shops) + 1))
        score = length_score * relative_popularity_score
        return score
