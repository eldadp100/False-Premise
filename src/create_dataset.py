"""
    1. Read LIMIT first questions
    2. On each apply parser to extract a premise
"""
import os

import UDP
import json

paths = {
    'questions': '../datasets/our/questions.txt',
    'output_json': '../datasets/our/qp_dataset.json'
}

LIMIT = 50000  # dataset size

if __name__ == '__main__':
    questions = []
    with open(paths["questions"]) as f:
        for _ in range(LIMIT):
            q = f.readline()
            if q[-1] == '\n':
                q = q[:-1]
            questions.append(q)

    nlp, _ = UDP.setup()
    dataset = {}
    errors = 0
    for q in questions:
        try:
            premise_lst = UDP.parse(q, nlp)
            dataset[q] = premise_lst
        except:
            print(f"error in {q}")
            errors += 1
    if os.path.exists(paths["output_json"]):
        os.remove(paths["output_json"])
    with open(paths["output_json"], "w") as f:
        json.dump(dataset, f)

    print(f"Failed to parse {errors}/{LIMIT} questions")
