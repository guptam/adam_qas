from time import time
import warnings
from re import compile

import numpy as np
import enchant
from autocorrect import spell

from qas.qclassifier import classify_question
from qas.feature_extractor import extract_features
from qas.query_const import construct_query
from qas.fetch_wiki import fetch_wiki
from qas.doc_scorer import rank_docs
from qas.candidate_ans import get_candidate_answers

from qas.constants import EXAMPLE_QUESTIONS


def answer_question(input_question):

    en_doc = en_nlp(u'' + input_question)

    question_class = classify_question(en_doc)
    print("Class:", question_class)

    question_keywords = extract_features(question_class, en_doc)
    print("Question Features:", question_keywords)

    question_query = construct_query(question_keywords, en_doc)
    print("Question Query:", question_query)

    print("Fetching Knowledge source...")
    wiki_pages = fetch_wiki(question_keywords, number_of_search=3)
    print("Pages Fetched:", len(wiki_pages))

    # Anaphora Resolution

    ranked_wiki_docs = rank_docs(question_keywords)
    print("Ranked Pages:", ranked_wiki_docs)

    candidate_answers, split_keywords = get_candidate_answers(question_query, ranked_wiki_docs, en_nlp)
    print("Candidate Answer:", "(" + str(len(candidate_answers)) + ")", candidate_answers)

    print("Answer:", " ".join(candidate_answers))

    answer = " ".join(candidate_answers)

    return answer


def spell_check(input_question):

    pattern = "\w"
    prog = compile(pattern)

    input_question_word_list = input_question.split()
    en_dict = enchant.Dict("en_US")
    for word_index in range(len(input_question_word_list)):
        if (not en_dict.check(input_question_word_list[word_index]) and
                prog.match(input_question_word_list[word_index]) is None):
            correct_word = spell(input_question_word_list[word_index])
            input_question_word_list[word_index] = correct_word
    return " ".join(input_question_word_list)


if __name__ == '__main__':
    warnings.filterwarnings("ignore", category=UserWarning)

    # input_question = input("Q:>")
    q = EXAMPLE_QUESTIONS[np.random.randint(len(EXAMPLE_QUESTIONS))]
    q = spell_check(q)
    # input_question_c = spell_check(input_question)
    print("Question:", q)

    start_time = time()

    answer_output = answer_question(q)

    end_time = time()
    print("Total time :", end_time - start_time)
