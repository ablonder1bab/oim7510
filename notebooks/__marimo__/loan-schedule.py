# /// script
# requires-python = ">=3.12"
# dependencies = [
#     "marimo",
# ]
# ///
"""Mini Project 1.
"""

import marimo

__generated_with = "0.25.1"
app = marimo.App(width="medium", sql_output="polars")


@app.cell
def _():
    import marimo as mo

    return (mo,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    # Mini Project 1

    Your choice of option, what each one asks for, the due date and how it is graded are on the Mini Project 1 page of the course site, linked from the calendar. This notebook is the shape to build it in. Keep the headings, and replace each line in italics with your own.

    Save it in your course repository as `projects/mp1/<your-tool>.py`, named for what it does, such as `loan-schedule.py`, and open it with `uv run marimo edit`.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## 1. The Question

    *Who would use this, and what decision does it help them make? Two or three sentences, in words somebody outside this course would understand.*
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    This project is for someone buying a house and needing a loan. They will need to understand the loan repayment schedule to see if they can afford this house
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## 2. My Plan Before AI

    *Before you ask your agent anything, write how you would solve it: the steps, in order, in plain words, in five lines or more. Then answer these two questions:*

    - *What does your loop carry from one step to the next, the way a running total carries its sum?*
    - *Which check will you use in section 6, and which two numbers should agree?*

    *Commit this notebook with the message `mp1: plan before AI`.*
    """)
    return


@app.cell
def _():
    plan = [
        "Step 1: The inputs are a $400000 loan and two rates - 0.0703 over 30 years and 0.0642% over 15 years."
        "step 2: Convert each annual rate to a monthly rate by dividing by 12, and set n to the number of months (years times 12) - 360 months for 30 year laon and 180 months for the 15-year loan. "
        "step 3: Before looping, I compute one fixed monthly payment per loan using loan_amount * r / (1 - (1+r)**-n), rounded to the cent. "
        "step 4: For each month from 1 to n, I calculate that month's interest as the current balance times r, rounded to the cent, then principal paid as payment minus interest, and reduce the balance by that principal."
        "step 5: I repeat step 4 for every month using range(1, n+1); on the last month I adjust the payment so the balance lands at exactly $0.00, then sum the interest column to get total interest for each loan and write one sentence comparing the 30-year and 15-year totals. "
    ]
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## 3. Inputs

    Every number the project starts from goes in the cell below, and nowhere else, so that changing one input changes every result after it.

    Copy in the default inputs for your option from the Mini Project 1 page. If you chose D, your own option, type your data in here, or ask your agent to generate it with `faker`. The required part reads no file.
    """)
    return


@app.cell
def _():
    loan_amount = 400000
    annual_rates = {30: 0.0703, 15: 0.0642}
    return annual_rates, loan_amount


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## 4. The Work

    Add as many cells as you need. Try each step yourself before you ask your agent, and commit as you go.
    """)
    return


@app.cell
def _():
    def monthly_payment(loan_amount, annual_rate, years):
        r = annual_rate / 12
        n = years * 12
        payment = loan_amount * r / (1 - (1 + r) ** -n)
        return round(payment, 2)

    monthly_payment(400000, 0.0703, 30)
    return (monthly_payment,)


@app.cell
def _(monthly_payment):
    monthly_payment(400000, 0.0642, 15)
    return


app._unparsable_cell(
    r"""
    amortization_schedule(loan_amount, annual_rate, years)
    List monthly payment
    range(1, n + 1)
    interest = round(balance * r, 2)
    principal = payment - interest
    Balance- principal
    """,
    name="_"
)


@app.cell
def _(annual_rates, loan_amount, monthly_payment):
    def amortization_schedule(loan_amount, annual_rate, years):
        r = annual_rate / 12
        n = years * 12
        payment = monthly_payment(loan_amount, annual_rate, years)
        balance = loan_amount
        rows = []
        for month in range(1, n + 1):
            interest = round(balance * r, 2)
            principal = payment - interest
            if month == n:
                principal = balance
            balance = round(balance - principal, 2)
            rows.append({"month": month, "payment": round(principal + interest, 2),
                          "interest": interest, "principal": round(principal, 2), "balance": balance})
        return rows

    schedule_30 = amortization_schedule(loan_amount, annual_rates[30], 30)
    return amortization_schedule, schedule_30


@app.cell
def _(schedule_30):
    schedule_30[-1]
    return


@app.cell
def _(amortization_schedule, annual_rates, loan_amount):
    schedule_15 = amortization_schedule(loan_amount, annual_rates[15], 15)
    return (schedule_15,)


@app.cell
def _(schedule_30):
    total_interest_30 = round(sum(row["interest"] for row in schedule_30), 2)
    return (total_interest_30,)


@app.cell
def _(schedule_15):
    total_interest_15 = round(sum(row["interest"] for row in schedule_15), 2)
    return (total_interest_15,)


@app.cell
def _(total_interest_15, total_interest_30):
    total_interest_30, total_interest_15
    return


@app.cell
def _(
    annual_rates,
    loan_amount,
    monthly_payment,
    total_interest_15,
    total_interest_30,
):
    comparison = (
        f"The 15-year loan has a higher monthly payment (${monthly_payment(loan_amount, annual_rates[15], 15):,.2f}) "
        f"than the 30-year loan (${monthly_payment(loan_amount, annual_rates[30], 30):,.2f}), "
        f"but saves ${total_interest_30 - total_interest_15:,.2f} in total interest over the life of the loan."
    )
    comparison
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## 5. The Answer

    *A table of your results in the cell below, printed with `print` and f-strings, then one sentence here that answers the question in section 1, with the number in it.*
    """)
    return


@app.cell
def _(schedule_30):
    print(f"{'Month':>5} {'Payment':>10} {'Interest':>10} {'Principal':>10} {'Balance':>10}")
    for row in schedule_30:
        print(f"{row['month']:>5} {row['payment']:>10.2f} {row['interest']:>10.2f} {row['principal']:>10.2f} {row['balance']:>10.2f}")
    return


@app.cell
def _(schedule_15):
    print(f"{'Month':>5} {'Payment':>10} {'Interest':>10} {'Principal':>10} {'Balance':>10}")
    for row in schedule_15:
        print(f"{row['month']:>5} {row['payment']:>10.2f} {row['interest']:>10.2f} {row['principal']:>10.2f} {row['balance']:>10.2f}")
    return


@app.cell
def _(schedule_15):
    print(f"{'Month':>5} {'Payment':>10} {'Interest':>10} {'Principal':>10} {'Balance':>10}")
    for entry in schedule_15:
        print(f"{entry['month']:>5} {entry['payment']:>10.2f} {entry['interest']:>10.2f} {entry['principal']:>10.2f} {entry['balance']:>10.2f}")
    return


@app.cell
def _(
    annual_rates,
    loan_amount,
    monthly_payment,
    total_interest_15,
    total_interest_30,
):
    print(f"Your friend can take on the ${loan_amount:,} loan either way, but choosing the 15-year term over the 30-year term saves them ${total_interest_30 - total_interest_15:,.2f} in total interest, at the cost of a monthly payment that's about ${monthly_payment(loan_amount, annual_rates[15], 15) - monthly_payment(loan_amount, annual_rates[30], 30):,.2f} higher.")
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## 6. How I Know These Numbers Are Right

    *At least one check that reaches a result a second, independent way. Name what you compared and what came out.*
    """)
    return


@app.cell
def _(schedule_15, schedule_30):
    final_balance_30 = schedule_30[-1]["balance"]
    final_balance_15 = schedule_15[-1]["balance"]
    print(f"30-year schedule ends at: ${final_balance_30:.2f} (expected $0.00)")
    print(f"15-year schedule ends at: ${final_balance_15:.2f} (expected $0.00)")
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## 7. Working With the Agent

    *Pick one piece of AI output you did not accept as-is. What did it give you, what did you change, and how did you know? Point to the commit or the cell.*

    *If the agent got it right the first time: what did you do to verify that?*
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    When i went to print the 15 year schedule the AI suggested reusing "for row in schedule 15", this was the same one i used in 30 year printing cell. There were a number of errors the AI made and refused to run. Marimo required every correct variables names. i changed the loop variable from row to entry. I should note the constant error i got was the pydantic_ ai which was never resolved after 2+ hours.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## 8. Going Further

    *Take at least one step past the main task, in any direction, and use your agent as much as you like. It does not have to work. State what you tried, what you found, and where it is in this notebook.*
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    Maybe by adding a payment to each payment schedule. if i made 1 extra payment per year directly to the principle how much could i save?
    """)
    return


@app.cell
def _(monthly_payment):
    def amortization_with_extra_annual(loan_amount, annual_rate, years, extra_annual_payment):
        r = annual_rate / 12
        payment = monthly_payment(loan_amount, annual_rate, years)
        balance = loan_amount
        month = 0
        rows = []
        while balance > 0:
            month += 1
            interest = round(balance * r, 2)
            principal = payment - interest
            if principal > balance:
                principal = balance
            balance = round(balance - principal, 2)
            extra = 0
            if month % 12 == 0 and balance > 0:
                extra = min(extra_annual_payment, balance)
                balance = round(balance - extra, 2)
            rows.append({"month": month, "interest": interest, "principal": round(principal + extra, 2), "balance": balance})
        return rows

    return (amortization_with_extra_annual,)


@app.cell
def _(
    amortization_with_extra_annual,
    annual_rates,
    loan_amount,
    monthly_payment,
    total_interest_30,
):
    extra_payment_30 = monthly_payment(loan_amount, annual_rates[30], 30)
    rows_extra_30 = amortization_with_extra_annual(loan_amount, annual_rates[30], 30, extra_payment_30)
    months_saved_30 = 360 - len(rows_extra_30)
    interest_extra_30 = round(sum(r["interest"] for r in rows_extra_30), 2)
    print(f"With one extra ${extra_payment_30:,.2f} payment to principal each year, the 30-year loan pays off in {len(rows_extra_30)} months instead of 360 (saving {months_saved_30} months), and total interest drops from ${total_interest_30:,.2f} to ${interest_extra_30:,.2f} — a savings of ${total_interest_30 - interest_extra_30:,.2f}.")
    return


@app.cell
def _(
    amortization_with_extra_annual,
    annual_rates,
    loan_amount,
    monthly_payment,
    total_interest_15,
):
    extra_payment_15 = monthly_payment(loan_amount, annual_rates[15], 15)
    rows_extra_15 = amortization_with_extra_annual(loan_amount, annual_rates[15], 15, extra_payment_15)
    months_saved_15 = 180 - len(rows_extra_15)
    interest_extra_15 = round(sum(r["interest"] for r in rows_extra_15), 2)
    print(f"With one extra ${extra_payment_15:,.2f} payment to principal each year, the 15-year loan pays off in {len(rows_extra_15)} months instead of 180 (saving {months_saved_15} months), and total interest drops from ${total_interest_15:,.2f} to ${interest_extra_15:,.2f} — a savings of ${total_interest_15 - interest_extra_15:,.2f}.")
    return


if __name__ == "__main__":
    app.run()
