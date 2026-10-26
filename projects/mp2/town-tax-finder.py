import marimo

__generated_with = "0.25.2"
app = marimo.App(width="medium")


@app.cell
def _():
    import requests

    return (requests,)


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
    I will need only the towns where the average home value is within the budget
    i will need the average tax bill is under the limit
    i want to sort the remaining towns from cheapest to most expensive and give a recommendation for the buyer
    """)
    return


@app.cell
def _():
    return


app._unparsable_cell(
    r"""
    this is the exact same check you already did in notebook 4 — compare the number of towns you collected against pagination["total"] that the server itself reports.
    """,
    name="_"
)


@app.cell
def _():
    ## 3. Inputs
    return


@app.cell
def _():
    county = "Middlesex"
    budget_dollars = 700000
    tax_limit_dollars = 8000
    fiscal_year = 2026
    return budget_dollars, county, fiscal_year, tax_limit_dollars


@app.cell
def _():
    ## 4. The Work
    return


@app.cell
def _(requests):
    def get_all_towns_in_county(county):
        towns = []
        page = 1
        while True:
            reply = requests.get(
                "https://oim.zhili.dev/ma/towns",
                params={"county": county, "per_page": 100, "page": page},
                timeout=10,
            )
            data = reply.json()
            towns = towns + data["items"]
            if page >= data["pagination"]["pages"]:
                break
            page += 1
        return towns

    def get_town_history(dor_code, year):
        reply = requests.get(
            f"https://oim.zhili.dev/ma/towns/{dor_code}/history",
            params={"from_year": year, "to_year": year},
            timeout=10,
        )
        return reply.json()["years"][0]

    return get_all_towns_in_county, get_town_history


@app.cell
def _(
    budget_dollars,
    county,
    fiscal_year,
    get_all_towns_in_county,
    get_town_history,
    tax_limit_dollars,
):
    county_towns = get_all_towns_in_county(county)

    affordable_towns = []
    for town in county_towns:
        history = get_town_history(town["dor_code"], fiscal_year)
        value = history["average_single_family_value_dollars"]
        bill = history["average_single_family_bill_dollars"]
        rate = history["residential_rate_per_thousand"]
        if value <= budget_dollars and bill <= tax_limit_dollars:
            affordable_towns.append({
                "name": town["name"],
                "average_value": value,
                "residential_rate": rate,
                "average_bill": bill,
            })

    affordable_towns = sorted(affordable_towns, key=lambda t: t["average_bill"])
    affordable_towns
    return (affordable_towns,)


@app.cell
def _():
    ## 5. The Answer
    return


@app.cell
def _(affordable_towns):
    print(f"{'Town':<15} {'Avg Value':>12} {'Tax Rate':>10} {'Avg Bill':>10}")
    for entry in affordable_towns:
        print(f"{entry['name']:<15} {entry['average_value']:>12,.0f} {entry['residential_rate']:>10.2f} {entry['average_bill']:>10,.0f}")
    return


@app.cell
def _(affordable_towns, budget_dollars, county, tax_limit_dollars):
    cheapest = affordable_towns[0]
    print(f"In {county} County, {len(affordable_towns)} towns have an average home within ${budget_dollars:,} and an average tax bill under ${tax_limit_dollars:,} a year — the cheapest is {cheapest['name']}, at about ${cheapest['average_bill']:,.0f} a year.")
    return


@app.cell
def _():
    ## 6. How I Know These Numbers Are Right
    return


@app.cell
def _(affordable_towns):
    check_town = affordable_towns[0]
    computed_bill = round(check_town["average_value"] * check_town["residential_rate"] / 1000, 2)
    computed_bill, check_town["average_bill"]
    return


@app.cell
def _():
    ## 7. Working With the Agent
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    when working on question 5 the agent wrote for town in affordable _towns but i accept this because town was already the loop variable in section4 filtering cell. Took my a while to figure out but with the help of the agent we renamed it to entry instead
    """)
    return


@app.cell
def _():
    ## 8. Reading It Back
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    get_all_towns_in_county: This function takes one input, a county name like 'Middlesex'. It returns a list of dictionaries, one per town in that county, covering every page of results from the API — not just the first 100 towns. The line I had to ask about was the while True: loop with its break condition — I wasn't sure why it needed to keep requesting more pages instead of asking once, until I realized a single request only returns up to 100 towns at a time, so the loop keeps going until every page has been collected."

    get_town_history: This function takes two inputs: a town's dor_code and a specific year. It returns a single dictionary with that one town's figures for exactly that year, not a list. The line I had to ask about was reply.json()["years"][0] — I wasn't sure why there was a [0] there since I'm passing the same year for both from_year and to_year. It's because the API always returns a list of years, even when that list only has one item in it, so [0] pulls that single year's record out."

    For the change and prediction: I'd suggest switching county from "Middlesex" to a different county, like "Norfolk" — predict something like: "I expect a different set of towns to appear on the list, since Norfolk's home values and tax bills are different from Middlesex's, and the cheapest town will likely be a different name entirely."
    """)
    return


@app.cell
def _():
    ## 9. Going Further
    return


@app.cell
def _():
    ## 10. Time Spent
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    it took about 3 hours total
    """)
    return


@app.cell
def _():
    import marimo as mo

    return (mo,)


if __name__ == "__main__":
    app.run()
