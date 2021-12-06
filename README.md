
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
    def join_autophrase_domain_relevace_score(autophrase_scores,    domain_relevance_scores, autophrase_ratio, domain_relevance_ratio):
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

## Instruction
#### Installing ArXiv dataset
- https://www.kaggle.com/Cornell-University/arxiv
- Move this file into the **current directory**

#### Installing Library of AutoPhrase
- https://github.com/shangjingbo1226/AutoPhrase
- Clone this library to the **exterior folder** that contain this directory 
- After cloning, go to *AutoPhrase/auto_phrase.sh* **line 24**, change it to the following:
    ``` sh
    DEFAULT_TRAIN=${DATA_DIR}/EN/arxiv_abstract.txt
    ```

#### Installing Library of Domain-Relevance
- https://github.com/jeffhj/domain-relevance
- Clone this library to the **exterior folder** that contain this directory 
- After cloning, go to *domain-relevance/query.py* **line 129**, get rid of *query_terms* list and add the following code:
    ``` python
    f = open("input.txt", "r")
    query_terms = f.read()
    f.close()
    query_terms = eval(query_terms)
    ```

#### Running Commands
- **-c** or **--category** for pass in ArXiv dataset category for base data, could be choose from "CS", "math", "Phy", default as "math"
- **-t** or **--threshold** for threshold for finding final combined score that is higher than the threshold, should be number in (0, 1], default as 0.88
- **-d** or **--use-prev-arxiv-data** for whether to use previous stored arxiv dataset, default as True
- **-s** or **--save-data-in-library** for whether to save data for both libraries, default as False
- **-u** or **--use-stored-data** for whether to use stored data in libraries, default as False
- Example: 
    ``` sh
    python keyword_extraction.py -c math -t 0.9 -s true
    ```
    ``` sh
    python3 keyword_extraction.py -t 0.9 -u true -s true
    ```
- Please see -h for any description of argument. Weighting of Autophrase and Domain-relevance score need to be manually changed in code.

#### Some Bugs Fix
- When using domain-relevance library, there exist a possibility that **print** statements of **epoch** might be stored in the output file that could cause error in code. The quick way to fix the bug is to delete **epoch** progress printing statements directly.