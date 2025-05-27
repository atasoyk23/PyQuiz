import random
import time
import json
from datetime import datetime
import os
import matplotlib.pyplot as plt

def main_menu():
    username = take_username_input()
    category = take_category_input()
    while category != None:
        if category == "Help":
            help_menu(username)
            category = take_category_input()
            continue
        operation = category_menu(category)
        if operation == "quiz":
            pat = file_path_finder(category)
            score, spent_time = quiz(pat)
            save_user_result(username, category, score, spent_time)
            avg_message, avg_score, total_quizzes = average_calculator(username, category)
            if total_quizzes == 0 or score <= avg_score:
                print(avg_message)
            else:
                print(f"Congratulations, you performed better than your average in {category}. {avg_message}")
            print_best_score_in_category(username, category)
        elif operation == "leaderboard":
            print_leaderboard_in_category(username, category)
        elif operation == "back":
            print("Going back to the main menu...\n")
            category = take_category_input()
            continue
        elif operation == "quit":
            print("Quitting the app...")
            return
        elif operation == "graph":
            visualizer(username, category)
        elif operation == "average":
            avg_message, avg_score, total_quizzes = average_calculator(username, category)

            print(avg_message)
        print(f"Going back to the {category} menu.\n")
    return

    
    
def category_menu(category):
    operation = ""
    while operation not in ("quiz", "leaderboard","back", "graph", "quit", "average"):
        operation = input(f"Choose an operation to continue: \n"
                            f"  Type 'quiz' to start the {category} quiz.\n"
                            f"  Type 'average' to learn your average statistics in {category} category.\n"
                            f"  Type 'graph' to see the visualization of your previous performance in {category}.\n"
                            f"  Type 'leaderboard' to see the {category} leaderboard.\n"
                            f"  Type 'back' to go back to the main menu.\n"
                            f"  Type 'quit' to quit the app.\n").lower()
                            
    return operation

def display_question(file_path):
    try:
        with open(file_path, 'r',encoding="utf-8") as file:
            lines = file.readlines()
    except FileNotFoundError:
        print(f"Question file '{file_path}' not found.")
        return ""
    for line in lines:
        if not line.strip().startswith("Answer:"):
            print(line.strip())
        else:
            return line
    

def file_path_finder(chosen_category):
    direc = f"questions/{chosen_category.lower()}_questions/question"
    return direc

def take_category_input():
    category = input("Welcome to main menu! Pick a category or an operation continue: \n"
                         f"   Type 'calculus' to choose Calculus. \n"
                         f"   Type 'python' to choose Python. \n"
                         f"   Type 'physics' to choose Physics.\n"
                         f"   Type 'help' to see the help menu.\n"
                         f"   Type 'quit' to quit the app.\n")
    while category.lower() not in ("calculus", "python", "physics","quit", "help"):
        category = input("Pick a valid category to continue: \n"
                         f"   Type 'calculus' to choose Calculus. \n"
                         f"   Type 'python' to choose Python. \n"
                         f"   Type 'physics' to choose Physics.\n"
                         f"   Type 'help' to see the help menu.\n"
                         f"   Type 'quit' to quit the app.\n")
    print("*" * 45)
    if category in ("calculus", "physics", "python"):
        print(f"Category has been correctly chosen as {category.lower().capitalize()}.")
        return category.lower().capitalize()
    elif category == "quit":
        print("Quitting the app...")
        return None
    else:
        print("Showing the 'help' menu...")
        return "Help"


def quiz(file_path):
    correct = 0
    shuffled_question_numbers = list(range(1,11))
    random.shuffle(shuffled_question_numbers)
    start_time = time.time()
    for j,i in enumerate(shuffled_question_numbers):
        print("*" * 45)
        print(f"Question {j+1}: ")
        try:
            ans = display_question(file_path + f"{i}.txt")[-1]
        except (FileNotFoundError, IndexError, TypeError):
            print(f"Failed to load question {j+1}. Skipping to next.")
            continue

        user_ans = input("Type your answer: \nA / B / C / D\n").capitalize()
        if user_ans in ("A", "B", "C", "D"):
            if user_ans == ans:
                print(f"Correct! Answer is {ans}")
                correct += 1
            else:
                print(f"Wrong! Answer was {ans}")
        else:
            print("Invalid Input! Please try again.")
            user_ans = input("Type your answer: \n  A / B / C / D  \n").capitalize()
            if user_ans in ("A", "B", "C", "D"):
                if user_ans == ans:
                    print(f"Correct! Answer is {ans}")
                    correct += 1
                else:
                    print(f"Wrong! Answer was {ans}")
            else:
                if i != 9:
                    print(f"Invalid input again! Answer was {ans}.\n"
                          f"   Please input A or B or C or D next time!\n"
                          f"Continuing with next question.")
                else:
                    print(f"Invalid input again! Finishing the quiz...")
    end_time = time.time()
    spent_time = end_time - start_time

    print(f"You got {correct} questions correctly in {spent_time:.2f} seconds!")
    return correct, spent_time

def take_username_input():
    username = input("Please type your username:\n")
    
    while len(username) < 3 or not username.isalnum():
        username = input("Please type your username. It must have at least 3 characters, all being alphanumeric.\n") 
    if not os.path.exists(f"user_data/{username}.json"):
        with open(f"user_data/{username}.json", "w", encoding="utf-8") as file:
            json.dump({"username": username, "quizzes": []}, file, indent= 4)
        print(f"Welcome {username}, registeration is successfully completed.")
    else:
        print(f"Welcome back {username}, you've successfully logged in.")
    
    return username

def save_user_result(username, category, score, spent_time, total_questions = 10):
    file_path = f"user_data/{username}.json"
    leaderboard_path = f"all_user_data/{category}/leaderboard.json"
    
    quiz_result = {
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "category": category,
        "score": score,
        "total_questions": total_questions,
        "spent_time": spent_time
    }

    if os.path.exists(file_path):
        try:
            with open(file_path, "r", encoding="utf-8") as file:
                data = json.load(file)
        except json.JSONDecodeError:
            print(f"User data file '{file_path}' is corrupted. Starting fresh.")
            data = {"username": username, "quizzes": []}
    else:
        data = {"username": username, "quizzes": []}


    if os.path.exists(leaderboard_path):
        try:
            with open(leaderboard_path, "r", encoding="utf-8") as file:
                leaderboard_data = json.load(file)
        except json.JSONDecodeError:
            print(f"Leaderboard file '{leaderboard_path}' is corrupted. Starting fresh.")
            leaderboard_data = []

    else:
        leaderboard_data = []

    data["quizzes"].append(quiz_result)
    leaderboard_data.append({"username": username, "quizzes": quiz_result})
    
    leaderboard_data = sorted(leaderboard_data, key= lambda x : ( - x["quizzes"]["score"] , x["quizzes"]["spent_time"]))

    with open(file_path, "w", encoding="utf-8") as file:
        json.dump(data, file, indent= 4)

    with open(leaderboard_path, "w", encoding="utf-8") as file:
        json.dump(leaderboard_data, file, indent= 4)



def load_user_data(username):
    file_path = f"user_data/{username}.json"
    if not os.path.exists(file_path):
        print(f"No data found: {file_path}")
        return None
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            return json.load(f)
    except json.JSONDecodeError:
        print(f"User data file '{file_path}' is corrupted.")
        return None

    
def print_best_score_in_category(username, category):
    data = load_user_data(username)
    this_quiz = data["quizzes"][-1]
    if data is None:
        return

    quizzes = [dic for dic in data["quizzes"] if dic["category"] == category]

    if not quizzes:
        print(f"{category} has no quiz data yet.")
        return
    

    best_quiz = sorted(quizzes, key= lambda x : ( - x["score"] , x["spent_time"]))
    if best_quiz[0] != this_quiz:
        print(f"\nYour best score in {category.upper()} category was:")
        print(f"   Score: {best_quiz[0]['score']}/{10}")
        print(f"   Time: {best_quiz[0]['spent_time']:.2f} seconds")
        print(f"   Date: {best_quiz[0]['timestamp']}\n")

    else:
        print(f"\nCongratulations! You broke your own record in {category.upper()} category!")
        print(f"   Score: {best_quiz[0]['score']}/{10}")
        print(f"   Time: {best_quiz[0]['spent_time']:.2f} seconds")
        print(f"   Date: {best_quiz[0]['timestamp']}\n")


def print_leaderboard_in_category(username, category):
    top10 = 0
    leaderboard_path = f"all_user_data/{category}/leaderboard.json"
    if os.path.exists(leaderboard_path):
        with open(leaderboard_path, "r", encoding="utf-8") as f:
            data =  json.load(f)
            if data  == None:
                return None
            leaderboard_len = min(len(data), 10)
            s = "s"
            if leaderboard_len > 0:
                if leaderboard_len == 1:
                    s = ""
                print(f"Top {leaderboard_len} quiz result{s} in {category.upper()} are:")
                for i in range(leaderboard_len):
                    if data[i]["username"] != username:
                        print(f"   {i+1}. {data[i]['username']} with a score of {data[i]['quizzes']['score']}/10 in {data[i]['quizzes']['spent_time']:.2f} seconds.")
                    else:
                        print(f"\033[1m   {i+1}. {data[i]['username']} with a score of {data[i]['quizzes']['score']}/10 in {data[i]['quizzes']['spent_time']:.2f} seconds. Congratz!\033[0m")
                        top10 += 1
                if top10 == 1:
                    print(f"\nYou made it to top {leaderboard_len} in {category} with a quiz!\n")
                elif top10 > 1:
                    print(f"\nYou made it to top {leaderboard_len} in {category} with {top10} different quizzes!\n")                    

            else:
                print(f"No leaderboard data exists in the {category} category.")
    else:
        with open(leaderboard_path, "a", encoding="utf-8") as f:
            print(f"No leaderboard data exists in the {category} category.")
    

def visualizer(username, category):
    user_file_path = f"user_data/{username}.json"
    if not os.path.exists(user_file_path):
        print(f"No data found for user: {username}")
        return
    
    try:
        with open(user_file_path, "r", encoding="utf-8") as f:
            data = json.load(f)
    except json.JSONDecodeError:
        print(f"User data file '{user_file_path}' is corrupted.")
        return

    quizzes = [quiz for quiz in data["quizzes"] if quiz["category"] == category]

    if len(quizzes) == 0:
        print(f"No quiz history found for {username} in {category}.")
        return
    scores = [quiz["score"] for quiz in quizzes]
    times = [quiz["spent_time"] for quiz in quizzes]
    nums = [f"#{i+1}" for i in range(len(quizzes))]

    print(f"Visualizing your previous record on {category}...")
    plt.figure(figsize=(10, 5))

    plt.subplot(1, 2, 1)
    plt.bar(nums, scores, color='blue')
    plt.title(f"{category} Scores for {username}")
    plt.xlabel("Quiz attempt")
    plt.ylabel("Score")
    plt.ylim(0, 10)
    plt.grid(axis="y")

    plt.subplot(1, 2, 2)
    plt.bar(nums, times, color='red')
    plt.title(f"{category} Time Spent for {username}")
    plt.xlabel("Quiz Attempt")
    plt.ylabel("Time (seconds)")
    plt.grid(axis="y")


    plt.suptitle(f"{username}'s {category} Quiz Performance", fontsize = 14)
    plt.tight_layout(rect=[0, 0, 1, 0.95])
    plt.show()


def average_calculator(username, category):
    user_file_path = f"user_data/{username}.json"
    if not os.path.exists(user_file_path):
        return f"No data found for user: {username}",None,None
    
    try:
        with open(user_file_path, "r", encoding="utf-8") as f:
            data = json.load(f)
    except json.JSONDecodeError:
        return f"User data file '{user_file_path}' is corrupted.", 0, 0

    quizzes = [quiz for quiz in data["quizzes"] if quiz["category"] == category]
    if len(quizzes) == 0:
        return f"No quiz history found for {username} in {category}.", 0, 0
    scores = [quiz["score"] for quiz in quizzes]
    times = [quiz["spent_time"] for quiz in quizzes]
    avg_score = sum(scores) / len(scores)
    avg_time = sum(times) / len(times)
    total_quizzes = len(scores)
    plural = (bool(total_quizzes - 1)) * "zes"
    return f"Your average score out of {total_quizzes} quiz{plural} in {category} is {avg_score:.2f}/10, your average time spent is {avg_time:.2f}.", avg_score, total_quizzes
        
def help_menu(username):
    print(f"\n\033[1mWELCOME TO PYQUIZ HELP MENU {username}\033[0m")
    print("Here's a list of available commands in category menus and what they do:\n")
    
    print(" = > \033[1mquiz\033[0m         - Start a new quiz in the selected category.")
    print(" = > \033[1maverage\033[0m      - View your average score and time in the current category.")
    print(" = > \033[1mgraph\033[0m        - See bar graph visualizations of your past performances.")
    print(" = > \033[1mleaderboard\033[0m  - View the top performers in the selected category.")
    print(" = > \033[1mback\033[0m         - Return to the main category selection menu.")
    print(" = > \033[1mquit\033[0m         - Exit the application.\n")

    print("\033[1mTIPS:\033[0m")
    print(" = > Try to beat your average score to improve.")
    print(" = > Keep your answers as A / B / C / D. (No problem to input lowercase)")
    print(" = > Make sure you have a stable question set in the appropriate folder before starting a quiz.\n")

    input("Press any key + 'enter' to go back to the main menu.\n")

main_menu()


