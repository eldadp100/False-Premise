import requests


def query_wikidata(relation, limit):
    url = 'https://query.wikidata.org/sparql'
    query = f"""
    
        SELECT ?x ?xLabel ?y $yLabel
        WHERE
        {{
          ?x  wdt:P{relation}   ?y.
          SERVICE wikibase:label {{ bd:serviceParam wikibase:language "en"}} 
        }}
        LIMIT {limit}
    """
    r = requests.get(url, params={'format': 'json', 'query': query})
    data = r.json()
    parsed_data = [(x['xLabel']['value'], x['yLabel']['value']) for x in data['results']['bindings']]
    return parsed_data





type_1_question_relations = [
    (61, "invented"),

]
type_2_question_relations = []
type_3_question_relations = []



print(query_wikidata(61, 10))
