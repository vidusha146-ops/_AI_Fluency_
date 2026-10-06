from config import COURSE_FEES, QUESTIONS, banner


def workflow(question):
    q = question.lower()

    if "fee" in q and "ai202" in q:
        return f"The fee for AI202 is ₹{COURSE_FEES['AI202']:,}."

    if (
        "cs101" in q
        and "ai202" in q
        and "10%" in q
        and "scholarship" in q
    ):
        total = COURSE_FEES["CS101"] + COURSE_FEES["AI202"]
        final_fee = total * 0.90

        return (
            f"Total fee = ₹{total:,}. "
            f"After 10% scholarship = ₹{final_fee:,.0f}."
        )

    if (
        "ds303" in q
        and "cs101" in q
        and "more expensive" in q
    ):
        difference = COURSE_FEES["DS303"] - COURSE_FEES["CS101"]

        return (
            f"Yes. DS303 is more expensive than CS101 "
            f"by ₹{difference:,}."
        )

    if "welcome" in q and "ai students" in q:
        return (
            "Welcome to the AI program!\n"
            "We are excited to have you join our learning community."
        )

    return "Sorry, I do not have a predefined rule for this question."


if __name__ == "__main__":
    banner("SYSTEM 2: RULE-BASED WORKFLOW")

    for question in QUESTIONS:
        print("Q:", question)
        print("A:", workflow(question))
        print("-" * 70)