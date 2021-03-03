import json
import random
import os

dataset_path = '../datasets/SQUAD/train-v1.1.json'
with open(dataset_path, "r") as f:
    squad_data = json.load(f)

questions = []
data = squad_data['data']
for title_data in data:
    for par_data in title_data['paragraphs']:
        for qas_data in par_data['qas']:
            questions.append(qas_data['question'])

random.shuffle(questions)

to_file_path = 'questions.txt'
if os.path.exists(to_file_path):
    x = input("are you sure you want to remove the previous file? [y/n]  ")
    if not (x.lower() == "y"):
        exit()
    os.remove(to_file_path)
fails = 0
with open(to_file_path, "w") as f:
    for q in questions:
        try:
            f.write(q + "\n")
        except:
            print(f"couldn't print: {q}")
            fails += 1
print(f"Failed to export {fails} / {len(questions)} of the questions")
# print(len(questions))
# print(questions[10200])
#
#
# for i, q in enumerate(questions[:10]):
#     print(f"{i}. {q}")
