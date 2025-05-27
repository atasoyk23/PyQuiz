# PyQuiz – Console-Based Quiz Application with Performance Stats

## Project Summary
**PyQuiz** is a Python console application where users take timed quizzes from various categories (e.g., Python, Physics, Calculus). The application tracks user performance, provides detailed statistics, visualizes progress with bar charts, and ranks users on a leaderboard.

---

## How to Run the Project

1. Clone or unzip the project.
2. Make sure you have Python 3.10+ installed.
3. Install required libraries:
    ```bash
    pip install -r requirements.txt
    ```
4. Run the main script:
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

- Answer options must be A/B/C/D.
- Visual graphs require a graphical environment to display.
- All progress is saved locally in JSON files.
