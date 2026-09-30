import os
from pathlib import Path
from database.database import init_db
from modules.documents import add_document, list_documents, get_document
from modules.tutor import ask_studymate
from modules.quiz import generate_quiz, save_quiz_result
from modules.analytics import show_performance
from modules.assignments import add_assignment, list_assignments
from modules.study_planner import make_plan
from utils.pdf_reader import extract_pdf_text


def choose_module():
    docs = list_documents()
    if not docs:
        print("\nNo modules uploaded yet. Add a PDF first.")
        return None
    print("\nAvailable modules:")
    for d in docs:
        print(f"{d['id']}. {d['title']} ({d['pages']} pages)")
    while True:
        try:
            choice = int(input("Enter module ID (0 to cancel): "))
            if choice == 0:
                return None
            doc = get_document(choice)
            if doc:
                return doc
            print("Invalid module ID.")
        except ValueError:
            print("Please enter a number.")


def upload_module():
    path = input("\nEnter PDF path: ").strip().strip('"')
    if not os.path.isfile(path) or not path.lower().endswith(".pdf"):
        print("Please enter a valid PDF path.")
        return
    title = input("Enter module title: ").strip() or Path(path).stem
    try:
        text = extract_pdf_text(path)
        if len(text.strip()) < 50:
            print("The PDF does not contain enough readable text.")
            return
        doc_id = add_document(title, path, text)
        print(f"Module '{title}' added successfully. Module ID: {doc_id}")
    except Exception as e:
        print(f"Could not read PDF: {e}")


def study_assistant():
    doc = choose_module()
    if not doc:
        return
    question = input(f"\nAsk StudyMate about '{doc['title']}': ").strip()
    if question:
        print("\n--- StudyMate Answer ---")
        print(ask_studymate(question, doc["content"]))


def quiz():
    doc = choose_module()
    if not doc:
        return
    try:
        count = max(3, min(int(input("Number of questions (3-10): ")), 10))
    except ValueError:
        count = 5
    print("\nGenerating quiz with OpenAI...")
    questions = generate_quiz(doc["title"], doc["content"], count)
    if not questions:
        return
    score = 0
    for i, q in enumerate(questions, 1):
        print(f"\nQ{i}. {q['question']}")
        for letter, option in zip("ABCD", q["options"]):
            print(f"  {letter}. {option}")
        answer = input("Your answer (A/B/C/D): ").strip().upper()
        if answer == q["answer"]:
            score += 1
            print("Correct!")
        else:
            print(f"Incorrect. Correct answer: {q['answer']}")
    save_quiz_result(doc["title"], score, len(questions))
    print(f"\nFinal score: {score}/{len(questions)}")


def assignments():
    while True:
        print("\n--- Assignment Manager ---")
        print("1. Add assignment")
        print("2. View assignments")
        print("0. Back")
        choice = input("Choose: ").strip()
        if choice == "1":
            title = input("Assignment title: ").strip()
            subject = input("Subject/module: ").strip()
            due = input("Due date (DD-MM-YYYY): ").strip()
            if title:
                add_assignment(title, subject, due)
                print("Assignment saved.")
        elif choice == "2":
            rows = list_assignments()
            if not rows:
                print("No assignments found.")
            else:
                for r in rows:
                    print(f"{r['id']}. {r['title']} | {r['subject']} | Due: {r['due_date']} | {r['status']}")
        elif choice == "0":
            return
        else:
            print("Invalid choice.")


def planner():
    print("\n--- Study Planner ---")
    subjects = input("Enter subjects separated by commas: ").split(",")
    try:
        hours = float(input("Available study hours per day: "))
    except ValueError:
        print("Enter a valid number.")
        return
    print("\n" + make_plan(subjects, hours))


def view_modules():
    docs = list_documents()
    print("\n--- Uploaded Modules ---")
    if not docs:
        print("No modules uploaded.")
        return
    for d in docs:
        print(f"ID: {d['id']} | Title: {d['title']} | Pages: {d['pages']} | File: {d['file_path']}")
        print(f"     Added: {d['created_at']}")


def main():
    init_db()
    while True:
        print("\n" + "=" * 58)
        print("                 VIT STUDYMATE")
        print("       AI-Powered Academic Learning Assistant")
        print("                 OpenAI Edition")
        print("=" * 58)
        print("1. Upload/Add Module")
        print("2. Ask StudyMate")
        print("3. Generate Quiz")
        print("4. View Performance")
        print("5. Assignment Manager")
        print("6. Study Planner")
        print("7. View Modules")
        print("8. Exit")
        choice = input("\nEnter your choice: ").strip()
        try:
            if choice == "1": upload_module()
            elif choice == "2": study_assistant()
            elif choice == "3": quiz()
            elif choice == "4": show_performance()
            elif choice == "5": assignments()
            elif choice == "6": planner()
            elif choice == "7": view_modules()
            elif choice == "8": print("Thank you for using VIT StudyMate!"); break
            else: print("Invalid choice. Select 1-8.")
        except Exception as e:
            print(f"\nThis module encountered an error: {e}")
            print("The application is still running. Choose another menu option.")


if __name__ == "__main__":
    main()
