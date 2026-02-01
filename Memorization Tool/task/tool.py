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
    box = Column(Integer, default=1)


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

    new_card = Flashcard(question=q, answer=a, box=1)
    session.add(new_card)
    session.commit()
    print()


def update_flashcard(card):
    while True:
        print('press "d" to delete the flashcard:')
        print('press "e" to edit the flashcard:')
        choice = input().strip()

        if choice == "d":
            session.delete(card)
            session.commit()
            return "deleted"

        elif choice == "e":
            # Edit question
            print(f"\ncurrent question: {card.question}")
            print("please write a new question:")
            new_q = input().strip()
            if new_q:
                card.question = new_q

            # Edit answer
            print(f"\ncurrent answer: {card.answer}")
            print("please write a new answer:")
            new_a = input().strip()
            if new_a:
                card.answer = new_a

            session.commit()
            print()
            return "edited"

        else:
            print(f"{choice} is not an option")


def box_function(card):
    while True:
        print('press "y" if your answer is correct:')
        print('press "n" if your answer is wrong:')
        choice = input().strip().lower()

        if choice == "y":
            if card.box == 3:
                session.delete(card)
                session.commit()
                return "deleted"
            else:
                card.box += 1
                session.commit()
                return "updated"

        elif choice == "n":
            # move card to box 1
            card.box = 1
            session.commit()
            print()
            return "updated"

        else:
            print(f"{choice} is not an option")


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
        # Card might have been deleted earlier in this session
        if session.get(Flashcard, card.id) is None:
            continue

        while True:
            print(f"\nQuestion: {card.question}")
            print('press "y" to see the answer:')
            print('press "n" to skip:')
            print('press "u" to update:')
            choice = input().strip().lower()

            if choice == "y":
                print(f"\nAnswer: {card.answer}\n")
                box_function(card)
                print()
                break
            elif choice == "n":
                # Skip, do not change box, no learning menu
                print()
                break
            elif choice == "u":
                update_flashcard(card)
                # Edited: go back to question menu for this card
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
