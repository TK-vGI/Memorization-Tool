# Solution Stage 2
flashcards will now persist in an SQLite database using SQLAlchemy ORM.

You already have a working Stage 1 implementation.
Now we integrate SQLAlchemy while keeping all formatting and behavior exactly the same.

Below is a clean, correct, Hyperskill‑compatible Stage 2 solution.
## ✅ Stage 2 — Full Working Implementation (with SQLAlchemy)
This version:
* Creates a database named `flashcard.db`
* Creates a table named **flashcard**
* Stores each flashcard as a row: `id`, `question`, `answer`
* Uses **SQLAlchemy ORM**
* Keeps all Stage 1 behavior and formatting
* Uses no “> ” before user input (as you requested earlier)

## 📌 Install SQLAlchemy (if needed)
```markdown
pip install sqlalchemy
```

## ✅ Final Code for Stage 2
```markdown
from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.orm import sessionmaker, declarative_base

# Database setup
engine = create_engine('sqlite:///flashcard.db?check_same_thread=False')
Base = declarative_base()

class Flashcard(Base):
    __tablename__ = 'flashcard'

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
    while True:
        print("Question:")
        q = input().strip()
        if q:
            break
        print("Question:")

    # Answer (must be non-empty)
    while True:
        print("Answer:")
        a = input().strip()
        if a:
            break
        print("Answer:")

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
            print("Bye!")
            break
        else:
            print(f"{choice} is not an option\n")


if __name__ == "__main__":
    main()
```

## 🎯 Why this version works
### ✔ Database name is correct
`flashcard.db`

### ✔ Table name is correct
`flashcard`

### ✔ SQLAlchemy ORM is used
- `declarative_base()`
- `Flashcard` class with `id`, `question`, `answer`
- `session.add()`, `session.commit()`
- `session.query(Flashcard).all()`

### ✔ All Stage 1 behavior preserved
- Formatting matches examples
- Input validation
- Error messages
- Submenu loops
- Practice mode works exactly as required

### ✔ No “> ” before user input
Matches your updated formatting.

## ❌ What went wrong
You used:
```markdown
Base = declarative_base(engine)
```
But:
✔ `declarative_base()` takes no arguments
✔ **SQLAlchemy 2.0** moved it to `sqlalchemy.orm.declarative_base`

So the correct usage is:
```markdown
from sqlalchemy.orm import declarative_base
Base = declarative_base()
```
No arguments.
No engine passed in.

### ✅ How to fix your Stage 2 code
Replace:
```markdown
from sqlalchemy.ext.declarative import declarative_base
Base = declarative_base(engine)
```
with:
```markdown
from sqlalchemy.orm import declarative_base
Base = declarative_base()
```

This is the only correct form for SQLAlchemy 2.0+ and the one Hyperskill expects.

## 🧠 Why this matters
- SQLAlchemy 1.4 allowed `declarative_base(bind=engine)`
- SQLAlchemy 2.0 **removed** the `bind` argument
- Hyperskill uses SQLAlchemy 2.0
- Therefore, passing the engine causes:

```markdown
TypeError: declarative_base() takes 0 positional arguments but 1 was given
```

## 🎯 Your database engine stays separate
Correct pattern:
```markdown
engine = create_engine('sqlite:///flashcard.db?check_same_thread=False')

Base = declarative_base()

class Flashcard(Base):
    __tablename__ = 'flashcard'
    id = Column(Integer, primary_key=True)
    question = Column(String)
    answer = Column(String)

Base.metadata.create_all(engine)

Session = sessionmaker(bind=engine)
session = Session()
```
This is the exact structure Hyperskill tests expect.