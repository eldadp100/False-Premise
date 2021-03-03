import json
import random
import os


def generate_questions_from_squad():
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

    to_file_path = '../datasets/our/questions.txt'
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


def prettify_squad():
    dataset_path = '../datasets/SQUAD/train-v1.1.json'
    with open(dataset_path, "r") as f:
        squad_data = json.load(f)

    qas = {}
    data = squad_data['data']
    for title_data in data:
        for par_data in title_data['paragraphs']:
            for qas_data in par_data['qas']:
                qas[qas_data['question']] = qas_data['answers'][0]['text']

    to_file_path = '../datasets/our/squad.json'
    if os.path.exists(to_file_path):
        x = input("are you sure you want to remove the previous file? [y/n]  ")
        if not (x.lower() == "y"):
            exit()
        os.remove(to_file_path)
    with open(to_file_path, "w") as f:
        json.dump(qas, f)


def generate_facts_list_from_fever():
    in_path = f"../datasets/Fever/fever.json"
    out_path = f"../datasets/our/facts.txt"
    fact_list = []
    with open(in_path) as f:
        for line in f:
            x = line[line.find("claim")+9:]
            x = x[:x.find('"')]
            fact_list.append(x)

    random.shuffle(fact_list)
    if os.path.exists(out_path):
        x = input("are you sure you want to remove the previous file? [y/n]  ")
        if not (x.lower() == "y"):
            exit()
        os.remove(out_path)
    fails = 0
    with open(out_path, "w") as f:
        for q in fact_list:
            try:
                f.write(q + "\n")
            except:
                print(f"couldn't print: {q}")
                fails += 1

# if __name__ == '__main__':
#     in_path = f"../datasets/Fever/fever.json"
#     out_path = f"../datasets/Fever/fever2.json"
#     with open(in_path) as f:
#         with open(out_path, "w") as f2:
#             for line in f:
#                 f2.write(line[:-1] + ',' + '\n')
#
#



if __name__ == '__main_1_':
    generate_questions_from_squad()
if __name__ == '__main_1_':
    prettify_squad()
if __name__ == '__main__':
    generate_facts_list_from_fever()