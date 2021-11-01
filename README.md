
# Domain-related Keyword Extraction
This is a document based on the previous iteration work on this topic

## Functional Design

-   Initialization function, takes category and writes abstracts file to AutoPhrase library
``` python
    def prepare_input_for_AutoPhrase(category):
        ...
        return void
```
-   Run AutoPhrase library shell command with subprocess
``` python
    def apply_auto_phrase():
        ... 
        return void
```
-   Get keywords from AutoPhrase library and clean-up function for eliminating keywords that have symbols
``` python
    def extract_keywords_from_library():
        return revised keyword_list
```
Initialization function, takes a list of keywords and writes into a file to Domain-Relevance library
``` python
    def prepare_input_for_domain_relevance(keywords_with_scores):
        ...
        return void
```
-   Run Domain-Relevance library command with subprocess
``` python
    def apply_domain_relevant():
        ... 
        return void
```
-   Get keywords from Domina-Relevance library
``` python
    def extract_keywords_from_domain_relevance():
        ...
        return revised keyword_list
```

-   Join two scores from two libraries with weighting.
``` python
    def join_autophrase_domain_relevace_score(autophrase_scores,     domain_relevance_scores, autophrase_ratio, domain_relevance_ratio):
        ...
        return keywords_with_scores
```

## Algorithmic Design
#### Extracting data from arXiv dataset
 - Input: Local json dataset name
 - Output: Extracted data from json file
 
#### Use Autophrase library to get important terms and scores
- Input: List of data from previous step
- Output: List of important terms and score

#### Use Domain-relevance library to cleanup list of import terms and score
- Input: Keyphrase from arXiv dataset
- Output: Keyphrase with its domain-relevance score

#### Combine Important score and domain-relevance score
- Input: List of important terms and score, Keyphrase with its domain-relevance score
- Output: Joined keyphrase and both scores

#### Calculate the precision rate based on the keyword list in fields
- Input: Joined keyphrase and scores
- Output: void
- Print presicion rate

![flow chart](Domain-relevant%20keywords%20extraction.png)