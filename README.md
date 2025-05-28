# PyQuiz – Console-Based Quiz Application with Performance Stats

## Project Summary
**PyQuiz** is a Python console application where users take timed quizzes from various categories (Python, Physics, Calculus). The application tracks user performance, provides detailed statistics, visualizes progress with bar charts, and ranks users on a leaderboard.

---

## How to Run the Project

1. Download the zip project file.
2. Unzip the project.
3. Make sure you have Python 3.10+ installed.
4. Install required libraries:
    ```bash
    pip install -r requirements.txt
    ```
5. Make sure to use correct directory:
    ```bash
    cd PyQuiz
    ```
6. Run the main script:
    ```bash
    python main.py
    ```

---

## Folder Structure

- `main.py`: Main application logic.
- `user_data/`: Stores each user's quiz history in JSON.
- `all_user_data/`: Stores leaderboard data for each category.
- `questions/`: Contains question files for each category (e.g., `python_questions/question1.txt`).
- `requirements.txt`: Lists required libraries.
- `readme.md`: This file.

---

## Requirements

- Python version: `3.10` or later
- Dependencies:
  - `matplotlib==3.7.1`

---

## Notes

- Answer options must be A / B / C / D. If any wrong input is given two times in a row, passes to the next question
- Visual graphs require a graphical environment to display.
- All progress is saved locally in JSON files.
- Inputs are not case sensitive.
- Can use 'help' command at main menu to get help.