import random
import requests
import json

userInput = input("Which Difficulty Level You Want? Easy, Medium or Hard?\n")
url = "https://leetcode.com/graphql/"
payload = json.dumps({
    "query": "\n    query problemsetQuestionList($categorySlug: String, $limit: Int, $skip: Int, $filters: QuestionListFilterInput) {\n  problemsetQuestionList: questionList(\n    categorySlug: $categorySlug\n    limit: $limit\n    skip: $skip\n    filters: $filters\n  ) {\n    total: totalNum\n    questions: data {\n      acRate\n      difficulty\n      freqBar\n      frontendQuestionId: questionFrontendId\n      isFavor\n      paidOnly: isPaidOnly\n      status\n      title\n      titleSlug\n      topicTags {\n        name\n        id\n        slug\n      }\n      hasSolution\n      hasVideoSolution\n    }\n  }\n}\n    ",
    "variables": {
        "categorySlug": "",
        "filters": {
            "listId": "wpwgkgt",
            "difficulty": userInput.upper()
        },
        "limit": 145,
        "skip": 0
    },
    "operationName": "problemsetQuestionList"
})
headers = {
    'Content-Type': 'application/json',
}
response = requests.request("GET", url, headers=headers, data=payload)
response_json = (json.loads(response.text))
questions = (response_json['data']['problemsetQuestionList']['questions'])
all_question = []
for item in questions:
    dict = {"id": int(item['frontendQuestionId']), "slug": item['titleSlug'].strip()}
    all_question.append(dict)

solved_questions = open("solved.txt").read().splitlines()


def choose_question(all_question):
    ques = random.choice(all_question)
    if solved_questions.__contains__(str(ques['id'])):
        print("already solved", ques['id'])
        ques = choose_question(all_question)
    return ques


def solved(file_name, text_to_append):
    with open(file_name, "a+") as file_object:
        file_object.seek(0)
        data = file_object.read(100)
        if len(data) > 0:
            file_object.write("\n")
        file_object.write(text_to_append)


selected = choose_question(all_question)
solved('solved.txt', str(selected['id']))
print("Today's pick --- >> ", "https://leetcode.com/problems/" + selected['slug'])
