import os
import json
import subprocess
import pandas as pd
import argparse
from os.path import exists

def prepare_input_for_AutoPhrase(category):
    """
    Prepare AutoPhrase library input
    Use local arxiv dataset for abstract extraction

    :param category: Abstract category
    :return: void
    """
    arxiv_json = open("arxiv-metadata-oai-snapshot.json", 'r', encoding='utf-8')
    file = open("../AutoPhrase/data/EN/arxiv_abstract.txt", 'w', encoding='utf-8')
    for line in arxiv_json:
        data = json.loads(line)
        if category in data["categories"]:
            abstract = data["abstract"]
            file.writelines(abstract + '\n')
            file.writelines(".\n")
    arxiv_json.close()
    file.close()
    print("Extracting category abstracts DONE")


def apply_auto_phrase():
    """
    Use Autophrase library for generating scores

    :return: void
    """
    cpp_command = "bash auto_phrase.sh"
    process = subprocess.run(cpp_command, shell=True, cwd='../AutoPhrase')
    print("AutoPhrase DONE")


def extract_keywords_from_AutoPhrase():
    """
    Transfer Autophrase library output into python list of keyphrase with score

    :return: Keyphrases extracted from Autophrase library with correspsonding score
    """
    file = open("../AutoPhrase/models/DBLP/AutoPhrase.txt", 'r', encoding='utf-8')
    data = file.readlines()
    symbols = ["\\", "~", "$", "_", "-", "*", ":"]  # exclude terms including symbols
    keywords_with_scores = []
    for line in data:
        check = 0
        for symbol in symbols:
            if symbol in line[13:-1]:
                check = 1
                break
        if check == 1:
            continue
        keywords_with_scores.append((line[13:-1], float(line[0:12])))
    file.close()
    print("Extracting from AutoPhrase done")
    # print(keywords_with_scores)
    return keywords_with_scores


def simplify_result_keywords(keywords_with_scores, threshold):
    """
    Filtering out Autophrase keyphrases with given threshold

    :param keywords_with_scores: python list of keyphrase and score
    :param threshold: float between (0, 1]
    :return: revised list of keyphrases and scores
    """
    keywords_with_scores.sort(reverse=True, key=lambda x: x[1])
    revised_keywords = []
    for pair in keywords_with_scores:
        if pair[1] >= threshold:
            revised_keywords.append(pair)
    return revised_keywords


def prepare_input_for_domain_relevance(keywords_with_scores):
    """
    Prepare Domain-relevance library input
    Use keyphrases from Autophrase library

    :param keywords_with_scores: revised list of keyphrases with scores
    :return: void
    """
    keywords = [pair[0] for pair in keywords_with_scores]
    f = open("../domain-relevance/input.txt", "w", encoding='utf-8')
    f.write(str(keywords))
    f.close()
    print("Preparation for Domain-relevance done")


def apply_domain_relevant():
    """
    Use Domain-relevance library for generating scores

    :return: void
    """
    command = "python3 query.py --domain cs --method cfl > output.txt"
    process = subprocess.run(command, shell=True, cwd='../domain-relevance')
    print("Domain Relevance Score DONE")


def extract_keywords_from_domain_relevance():
    """
    Transfer Domain-relevance library output into python list of keyphrase with score

    :return: Keyphrases extracted from Domain-relevance library with correspsonding score
    """
    file = open("../domain-relevance/output.txt", "r", encoding="utf-8")
    domain_scores = file.readlines()[2:]
    keywords_with_scores = [line.split(': ') for line in domain_scores]
    keywords_with_scores = [(pair[0], float(pair[1].split('\n')[0])) for pair in keywords_with_scores]
    print("Extracting from Domain-Relevance done")
    return keywords_with_scores



def join_autophrase_domain_relevace_score(autophrase_scores, domain_relevance_scores, autophrase_ratio, domain_relevance_ratio):
    """
    Given results from both Autophrase and Domain-relevance libraries, join two scores with given ratio

    :param autophrase_scores: python list of keyphrases and scores from Autophrase library
    :param domain_relevance_scores: python list of keyphrases and scores from Domain-relevance library
    :param autophrase_ratio: joining ratio for Autophrase score
    :param domain_relevance_ratio: jioning ratio for Domain-relevance score
    :return: python list of keyphrases and combined scores based on ratio
    """
    keywords_with_scores = []
    for i in range(len(autophrase_scores)):
        autophrase_score = autophrase_scores[i][1]
        domain_relevance_score = domain_relevance_scores[i][1]
        keyword = autophrase_scores[i][0]
        combined_score = (autophrase_score * autophrase_ratio + domain_relevance_score * domain_relevance_ratio) / (autophrase_ratio + domain_relevance_ratio)
        keywords_with_scores.append((keyword, combined_score))
    keywords_with_scores.sort(key = lambda x: x[1], reverse=True)
    return keywords_with_scores

def get_kewords_with_threshold(keywords_with_scores, threshold):
    """
    Filtering out final keyphrases with given threshold

    :param keywords_with_scores: Given keyphrases and scores
    :param threshold: Given threshold for score
    :return: revised python list of keyphrases and scores
    """
    keywords = []
    for pair in keywords_with_scores:
        if pair[1] >= threshold:
            keywords.append(pair)
    return keywords


def write_list_to_file(keywords_with_scores):
    file = open("output.txt", 'w', encoding='utf-8')
    for pair in keywords_with_scores:
        keyword = pair[0]
        score = pair[1]
        temp_str = f"{keyword}: {score}\n"
        file.writelines(temp_str)
    file.close()


def cleanup_autophrase():
    """
    Cleanup function for Autophrase library
    """
    file = "../AutoPhrase/data/EN/arxiv_abstract.txt"
    if os.path.exists(file):
        os.remove(file)


def cleanup_domain_relevance():
    """
    Cleanup function for Domain-relevance library
    """
    file = "../domain-relevance/input.txt"
    if os.path.exists(file):
        os.remove(file)


def cleanup_all():
    """
    Cleanup function for library usage
    """
    cleanup_autophrase()
    cleanup_domain_relevance()
    

def main():
    # Arguments for user input
    parser = argparse.ArgumentParser(description='Domain-Relevant Keyword Extraction.')
    parser.add_argument('-c', '--category', type=str, default='math', 
                        help='ArXiv dataset category for base data, could be choose from "CS", "math", "Phy", default as "math"')
    parser.add_argument('-d', '--use-prev-arxiv-data', type=bool, default=True,
                        help="Whether to use previous stored arxiv dataset")
    parser.add_argument('-t', '--threshold', type=float, default=0.88, 
                        help='Threshold for finding final combined score that is higher than the threshold, should be number in (0, 1], default as 0.88')
    parser.add_argument('-s', '--save-data-in-library', type=bool, default=False, 
                        help="Whether to save data for both libraries, default as False")
    parser.add_argument('-u', '--use-stored-data-in-library', type=bool, default=False, 
                        help="Whether to use stored data in libraries, default as False")
    parser.add_argument('-o', "--output", type=bool, default=False,
                        help="Whether to write result into output.txt file")
    args = parser.parse_args()

    # Check input category is in arxiv dataset categories.
    if args.category not in ["CS", "math", "Phy"]:
        raise Exception("Category input does not match requirement, please select from \n CS \n Math \n Phy")

    # Check given threshold is in correct range
    if args.threshold <= 0 or args.threshold > 1:
        raise Exception("Threshold input does not match requirement, please select number in (0, 1]")

    # Check whether there is previously stored ArXiv dataset abstract in AutoPhrase library
    if args.use_prev_arxiv_data:
        file_exists = exists("../AutoPhrase/data/EN/arxiv_abstract.txt")
        if not file_exists:
            raise Exception("There is no previous stored arxiv abstract data in Autophrase Library. Please modify input with -d False")

    # Check whether there is previously stored Autophrase and Domain-relevance data
    if args.use_stored_data_in_library:
        autophrase_output_exist = exists("../AutoPhrase/models/DBLP/AutoPhrase.txt")
        domain_relevance_output_exist = exists("../domain-relevance/output.txt")
        if not autophrase_output_exist:
            raise Exception("Autophrase Library does not have stored data")
        if not domain_relevance_output_exist:
            raise Exception("Domain-relevance Library does not have stored data")
    
    # Whether to extract new ArXiv dataset abstracts
    if not args.use_prev_arxiv_data:
        prepare_input_for_AutoPhrase(args.category)

    # Whether to use stored data in Autophrase library
    if not args.use_stored_data_in_library:
        apply_auto_phrase()
    # Get output from AutoPhrase library
    autophrase_scores = extract_keywords_from_AutoPhrase()
    autophrase_scores = simplify_result_keywords(autophrase_scores, 0.95)

    # Whether to use stored data in Domain-relevance library
    if not args.use_stored_data_in_library:
        prepare_input_for_domain_relevance(autophrase_scores)
        apply_domain_relevant()
    # Get output from Domain-relevance library
    domain_relevance_scores = extract_keywords_from_domain_relevance()

    # Join two scores and output final result
    combined_scores = join_autophrase_domain_relevace_score(autophrase_scores, domain_relevance_scores, 1, 15)

    final_outputs = get_kewords_with_threshold(combined_scores, args.threshold)

    for pair in final_outputs:
        print(f"{pair[0]}: {pair[1]}")

    if args.output:
        write_list_to_file(final_outputs)


    # Cleanup function for not storing output in corresponding libraries
    if not args.save_data_in_library:
        print("Cleanup")
        cleanup_all()


if __name__ == '__main__':
    main()
