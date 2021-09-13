
# Domain-related Keyword Extraction
This is a document based on the previous iteration work on this topic

## Functional Design

-   No input needed, initialization function, output corpus in python list
``` python
	def init_corpus():
		return { "Algorithm", "Artificial Intelligence", "Database", ... }
```
-   Takes input as string, and output list of keywords that are relevant to domain.
``` python
    def keyword_extraction(string):
        ... 
        return { "Algorithm", "Artificial Intelligence", "Database" }
```
-  Autophrase method, use library and cli comands for autophrased importance keywords from init_corpus
- Clean-up function for eliminating keywords that have symbols
``` python
	def eliminate_invalid_keywords(keyword_list):
		return revised keyword_list
```
- Domain relevance score calculate function, using library
``` python
	def get_domain_relevance_score(keyword, domain):
		return score
```