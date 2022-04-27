
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

## Project Structure
    Domain-relevant-keyword-extraction/
        - requirements.txt
        - keyword_extraction.py
        - arXiv dataset (instruction below)
    Domain-relevance (instruction below)
    AutoPhrase (instruction below)
    
## Instruction

#### Clone/ pull of this repository using:
```
git clone --recurse-submodules https://github.com/Forward-UIUC-2021F/chen-si-domain-relevant-keyword-extraction/

git pull --recurse-submodules 
```

#### Run setup.sh
```
sh setup.sh
```
#### Python Library Install
``` sh
pip install -r requirements.txt 
```

#### Setting up Autophrase:
- Follow the instructions listed in https://github.com/Forward-UIUC-2022S/edu-today-AutoPhrase to setup AutoPhrase
NOTE: a folder named AutoPhrase would be created in parent directory.

#### Setting up Domain-relevance:
- Follow the instructions listed in https://github.com/Forward-UIUC-2022S/edu-today-domain-relevance to setup domain-relevance
NOTE: a folder named domain-relevance would be created in the parent directory.
#### Website to extract abstracts from:
> SCOPUS Website to download Abstracts:
    https://www-scopus-com.proxy2.library.illinois.edu/

#### Aditional instructions on installing C++ for AutoPhrase on a VM:

Steps:
1. installing g++4.8 in ubuntu: Follow commands in:
    https://stackoverflow.com/questions/61945439/how-to-install-compiler-g-4-8-5-in-ubuntu-20-04

    mkdir educationtoday
    cd educationtoday

    - sudo dpkg --add-architecture i386
    - sudo apt update
    - sudo apt upgrade
    - sudo apt-get install gcc-multilib libstdc++6:i386
    - wget https://ftp.gnu.org/gnu/gcc/gcc-4.8.5/gcc-4.8.5.tar.bz2 --no-check-certificate
    - tar xf gcc-4.8.5.tar.bz2
    - cd gcc-4.8.5
    - ./contrib/download_prerequisites
    - cd ..
    - sed -i -e 's/__attribute__/\/\/__attribute__/g' gcc-4.8.5/gcc/cp/cfns.h
    sed -i 's/struct ucontext/ucontext_t/g' gcc-4.8.5/libgcc/config/i386/linux-unwind.h
    - mkdir xgcc-4.8.5
    - pushd xgcc-4.8.5
    $PWD/../gcc-4.8.5/configure --enable-languages=c,c++ --prefix=/usr --enable-shared --enable-plugin --program-suffix=-4.8.5
    - make MAKEINFO="makeinfo --force" -j
    - sudo make install -j

    REF: https://askubuntu.com/questions/583171/bin-bash-g-command-not-found-error-127

2. sudo apt install gcc-4.8 g++-4.8
3. sudo apt-get install build-essential

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

#### Runtime (without GPU accelerating)
- About 20 mins, higher threshold in AutoPhrase reduces runtime

#### Demo
<video autosize: true controls>
  <source src="Library_Intro.mp4" type="video/mp4">
</video>


## Reference
- Dataset: https://www.kaggle.com/Cornell-University/arxiv
- AutoPhrase Library: https://github.com/shangjingbo1226/AutoPhrase
- Domain-relevance Library: https://github.com/jeffhj/domain-relevance