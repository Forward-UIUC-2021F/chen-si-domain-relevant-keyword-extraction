import os
import json
import subprocess
import pandas as pd
from helpers import string_to_float
import argparse

# write this more like a module for more function usage


def prepare_input_for_AutoPhrase(category):
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
    cpp_command = "bash auto_phrase.sh"
    process = subprocess.run(cpp_command, shell=True, cwd='../AutoPhrase')
    print("AutoPhrase DONE")


def extract_keywords_from_AutoPhrase():
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
    keywords_with_scores.sort(reverse=True, key=lambda x: x[1])
    revised_keywords = []
    for pair in keywords_with_scores:
        if pair[1] >= threshold:
            revised_keywords.append(pair)
    return revised_keywords


def prepare_input_for_domain_relevance(keywords_with_scores):
    keywords = [pair[0] for pair in keywords_with_scores]
    f = open("../domain-relevance/input.txt", "w", encoding='utf-8')
    f.write(str(keywords))
    f.close()
    print("Preparation for Domain-relevance done")


def apply_domain_relevant():
    command = "python3 query.py --domain cs --method cfl > output.txt"
    process = subprocess.run(command, shell=True, cwd='../domain-relevance')
    print("Domain Relevance Score DONE")


def extract_keywords_from_domain_relevance():
    file = open("../domain-relevance/output.txt", "r", encoding="utf-8")
    domain_scores = file.readlines()[2:]
    keywords_with_scores = [line.split(': ') for line in domain_scores]
    keywords_with_scores = [(pair[0], string_to_float(pair[1].split('\n')[0])) for pair in keywords_with_scores]
    print("Extracting from Domain-Relevance done")
    return keywords_with_scores



def join_autophrase_domain_relevace_score(autophrase_scores, domain_relevance_scores, autophrase_ratio, domain_relevance_ratio):
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
    keywords = []
    for pair in keywords_with_scores:
        if pair[1] >= threshold:
            keywords.append(pair)
    return keywords


def cleanup_autophrase():
    file = "../AutoPhrase/data/EN/arxiv_abstract.txt"
    if os.path.exists(file):
        os.remove(file)


def cleanup_domain_relevance():
    file = "../domain-relevance/input.txt"
    if os.path.exists(file):
        os.remove(file)


def cleanup_all():
    cleanup_autophrase()
    cleanup_domain_relevance()
    

def main():
    parser = argparse.ArgumentParser(description='Domain-Relevant Keyword Extraction.')
    parser.add_argument('-c', '--category', type=str, default='math', 
                        help='ArXiv dataset category for base data, could be choose from "CS", "math", "Phy", default as "math"')
    parser.add_argument('-t', '--threshold', type=float, default=0.88, 
                        help='Threshold for finding final combined score that is higher than the threshold, should be number in (0, 1], default as 0.88')
    parser.add_argument('-s', '--save-data-in-library', type=bool, default=False, 
                        help="Whether to save data for both libraries, default as False")
    parser.add_argument('-u', '--use-stored-data', type=bool, default=False, 
                        help="Whether to use stored data in libraries, default as False")
    # parser.add_argument('-w', "--combined_weight")

    args = parser.parse_args()

    if args.restart:
        cleanup_all()
    if args.category not in ["CS", "math", "Phy"]:
        raise Exception("Category input does not match requirement, please select from \n CS \n Math \n Phy")
    if args.threshold <= 0 or args.threshold > 1:
        raise Exception("Threshold input does not match requirement, please select number in (0, 1]")

    if not args.use_stored_data:
        prepare_input_for_AutoPhrase(args.category)
    if not args.use_stored_data:
        apply_auto_phrase()
    autophrase_scores = extract_keywords_from_AutoPhrase()
    autophrase_scores = simplify_result_keywords(autophrase_scores, 0.85)

    if not args.use_stored_data:
        prepare_input_for_domain_relevance(autophrase_scores)
        apply_domain_relevant()
    domain_relevance_scores = extract_keywords_from_domain_relevance()

    combined_scores = join_autophrase_domain_relevace_score(autophrase_scores, domain_relevance_scores, 1, 15)
    print(get_kewords_with_threshold(combined_scores, args.threshold))
    if not args.save_data_in_library:
        cleanup_all()


if __name__ == '__main__':
    main()
