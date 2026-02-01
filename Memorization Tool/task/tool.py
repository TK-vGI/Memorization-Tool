from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.orm import sessionmaker, declarative_base

# Database setup
engine = create_engine('sqlite:///flashcard.db?check_same_thread=False')
Base = declarative_base()

class Flashcard(Base):
    __tablename__ = "flashcards"

    id = Column(Integer, primary_key=True)
    question = Column(String)
    answer = Column(String)

Base.metadata.create_all(engine)

Session = sessionmaker(bind=engine)
session = Session()

MAIN_MENU = """1. Add flashcards
2. Practice flashcards
3. Exit"""

ADD_SUBMENU = """1. Add a new flashcard
2. Exit"""


def user_input():
    return input()


def add_flashcard():
    # Question (must be non-empty)
    print()
    while True:
        print("Question:")
        q = input().strip()
        if q:
            break

    # Answer (must be non-empty)
    while True:
        print("Answer:")
        a = input().strip()
        if a:
            break

    new_card = Flashcard(question=q, answer=a)
    session.add(new_card)
    session.commit()
    print()


def add_submenu():
    while True:
        print(ADD_SUBMENU)
        choice = user_input()

        if choice == "1":
            add_flashcard()
        elif choice == "2":
            print()
            return
        else:
            print()
            print(f"{choice} is not an option\n")


def practice_flashcards():
    cards = session.query(Flashcard).all()
    if not cards:
        print("\nThere is no flashcard to practice!\n")
        return

    print()
    for card in cards:
        print(f"Question: {card.question}")
        print('Please press "y" to see the answer or press "n" to skip:')

        while True:
            choice = user_input().lower()
            if choice == "y":
                print(f"\nAnswer: {card.answer}\n")
                break
            elif choice == "n":
                print()
                break
            else:
                print()
                print(f"{choice} is not an option")

    return


def main():
    while True:
        print(MAIN_MENU)
        choice = user_input()

        if choice == "1":
            print()
            add_submenu()
        elif choice == "2":
            practice_flashcards()
        elif choice == "3":
            print("\nBye!")
            break
        else:
            print()
            print(f"{choice} is not an option\n")


if __name__ == "__main__":
    main()