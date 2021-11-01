import os
import json
import subprocess
import pandas as pd
from helpers import string_to_float



def prepare_input_for_AutoPhrase(category):
    print("Extracting category abstracts .........")
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
    print("Start AutoPhrase")
    cpp_command = "bash auto_phrase.sh"
    process = subprocess.run(cpp_command, shell=True, cwd='../AutoPhrase')
    print("AutoPhrase DONE")


def extract_keywords_from_AutoPhrase():
    print("Start extracting keywords from AutoPhrase")
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
    print("Extracting done")
    # print(keywords_with_scores)
    return keywords_with_scores

def prepare_input_for_domain_relevance(keywords_with_scores):
    print("Prepare Input for Domain-relevance")
    keywords = [pair[0] for pair in keywords_with_scores]
    f = open("../domain-relevance/input.txt", "w", encoding='utf-8')
    f.write(str(keywords))
    f.close()
    print("Preparation done")


def apply_domain_relevant():
    print("Start Getting Domain Relevance Score")
    command = "python3 query.py --domain cs --method cfl > output.txt"
    process = subprocess.run(command, shell=True, cwd='../domain-relevance')
    print("Domain Relevance Score DONE")


def extract_keywords_from_domain_relevance():
    print("Start extracting keywords from Domain-relevance")
    file = open("../domain-relevance/output.txt", "r", encoding="utf-8")
    domain_scores = file.readlines()[2:]
    keywords_with_scores = [line.split(': ') for line in domain_scores]
    keywords_with_scores = [(pair[0], string_to_float(pair[1].split('\n')[0])) for pair in keywords_with_scores]
    print("Extracting done")
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


def cleanup():
    os.remove("../AutoPhrase/data/EN/arxiv_abstract.txt")
    os.remove("../domain-relevance/input.txt")
    os.remove("AutoPhrase_score.txt")

def main():
    # prepare_input_for_AutoPhrase("math")
    # apply_auto_phrase()
    autophrase_scores = extract_keywords_from_AutoPhrase()[:4000]
    prepare_input_for_domain_relevance(autophrase_scores)
    apply_domain_relevant()
    domain_relevance_scores = extract_keywords_from_domain_relevance()
    # print(domain_relevance_scores)
    combined_scores = join_autophrase_domain_relevace_score(autophrase_scores, domain_relevance_scores, 1, 15)
    print(combined_scores[:40])
    # cleanup()


if __name__ == '__main__':
    main()
