import marimo

__generated_with = "0.25.2"
app = marimo.App(width="medium")


@app.cell
def _():
    ## 1. The Question
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    This tool will help homebuyers find towns where homes fit the budget and the tax bill stays under a limit, ranked from cheapest to most expensive
    """)
    return


@app.cell
def _():
    ## 2. My Plan Before AI
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    I will need to pull data from the state of MA that stays within the budget.
    I will need to get every town in middlesex county
    I will need only the towns where the average home value and average tax bill are within the budget of 708000
    i want to sort the remaining towns from cheapest to most expensive and give a recommendation for the buyer
    """)
    return


@app.cell
def _():
    county = "Middlesex"
    budget_dollars = 700000
    tax_limit_dollars = 8000
    fiscal_year = 2026
    return


@app.cell
def _():
    ## 3. Inputs
    return


@app.cell
def _():
    ## 4. The Work
    return


@app.cell
def _():
    ## 5. The Answer
    return


@app.cell
def _():
    ## 6. How I Know These Numbers Are Right
    return


@app.cell
def _():
    ## 7. Working With the Agent
    return


@app.cell
def _():
    ## 8. Reading It Back
    return


@app.cell
def _():
    ## 9. Going Further
    return


@app.cell
def _():
    ## 10. Time Spent
    return


@app.cell
def _():
    import marimo as mo

    return (mo,)


if __name__ == "__main__":
    app.run()
