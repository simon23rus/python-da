#!/usr/bin/env python3
import numpy as np
from scipy.linalg import norm


def create_page_rank_markov_chain(links, damping_factor=0.15):

    links = np.array(links)
    N = links.max() + 1
    link_list = [[] for i in range(N)]
    for elem in links:
        link_list[elem[0]].append(elem[1])

    prob_matrix = []
    for from_, page_links in (enumerate(link_list)):
        row = [1. / N] * N
        if len(page_links) == 0:
            prob_matrix.append(row)
            continue
        for to_ in range(len(link_list)):
            row[to_] = (1. - damping_factor) \
                * ((1. / len(link_list[from_])) if to_ in page_links else 0) \
                + damping_factor / N
        prob_matrix.append(row)
    return np.matrix(prob_matrix)


def page_rank(links, start_distribution, damping_factor=0.15,
              tolerance=10 ** (-7), return_trace=False):

    prob_matrix = create_page_rank_markov_chain(links,
                                                damping_factor=damping_factor)
    distribution = np.matrix(start_distribution)

    last, current = distribution, np.dot(distribution, prob_matrix)
    trace = [last]
    while norm(current - last) > tolerance:
        last, current = current, np.dot(current, prob_matrix)
        trace.append(last)

    if return_trace:
        return np.array(np.matrix(current)).ravel(), np.array(trace)
    else:
        return np.array(np.matrix(current)).ravel()
