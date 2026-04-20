import marimo

app = marimo.App()


@app.cell
def _():
    import marimo as mo
    import pandas as pd
    import plotly.express as px
    return mo, pd, px


@app.cell
def _(pd):
    csv_url = "https://gist.githubusercontent.com/DrAYim/80393243abdbb4bfe3b45fef58e8d3c8/raw/ed5cfd9f210bf80cb59a5f420bf8f2b88a9c2dcd/sp500_ZScore_AvgCostofDebt.csv"
    df = pd.read_csv(csv_url)

    df = df.dropna(
        subset=["AvgCost_of_Debt", "Z_Score_lag", "Sector_Key", "Market_Cap", "Name"]
    ).copy()
    df = df[df["AvgCost_of_Debt"] < 5].copy()

    df["Debt_Cost_Percent"] = df["AvgCost_of_Debt"] * 100
    df["Market_Cap_B"] = df["Market_Cap"] / 1e9

    return (df,)


@app.cell
def _(df, mo):
    sectors = sorted(df["Sector_Key"].unique().tolist())

    sector_dropdown = mo.ui.multiselect(
        options=sectors,
        value=sectors[:4],
        label="Filter by Sector",
    )

    cap_slider = mo.ui.slider(
        start=0,
        stop=200,
        step=10,
        value=20,
        label="Minimum Market Cap ($bn)",
    )

    return cap_slider, sector_dropdown


@app.cell
def _(cap_slider, df, sector_dropdown):
    filtered_df = df[
        (df["Sector_Key"].isin(sector_dropdown.value))
        & (df["Market_Cap_B"] >= cap_slider.value)
    ].copy()

    count = len(filtered_df)
    return count, filtered_df


@app.cell
def _(count, filtered_df, mo, px):
    fig = px.scatter(
        filtered_df,
        x="Z_Score_lag",
        y="Debt_Cost_Percent",
        color="Sector_Key",
        size="Market_Cap_B",
        hover_name="Name",
        title=f"Cost of Debt vs Altman Z-Score ({count} companies)",
        labels={
            "Z_Score_lag": "Altman Z-Score",
            "Debt_Cost_Percent": "Average Cost of Debt (%)",
            "Sector_Key": "Sector",
            "Market_Cap_B": "Market Cap ($bn)",
        },
        template="presentation",
        width=900,
        height=600,
    )

    fig.add_vline(x=1.81, line_dash="dash", line_color="red")
    fig.add_vline(x=2.99, line_dash="dash", line_color="green")

    chart = mo.ui.plotly(fig)
    return (chart,)


@app.cell
def _(mo, pd, px):
    travel_data = pd.DataFrame(
        {
            "City": ["London", "Mumbai", "Marrakesh", "Dubai", "Paris"],
            "Lat": [51.5074, 19.0760, 31.6295, 25.2048, 48.8566],
            "Lon": [-0.1278, 72.8777, -7.9811, 55.2708, 2.3522],
            "Category": ["Study", "Family", "Travel", "Travel", "Culture"],
        }
    )

    fig_travel = px.scatter_geo(
        travel_data,
        lat="Lat",
        lon="Lon",
        hover_name="City",
        color="Category",
        projection="natural earth",
        title="Places Connected to My Interests",
    )

    fig_travel.update_traces(marker=dict(size=12))
    travel_chart = mo.ui.plotly(fig_travel)
    return (travel_chart,)


@app.cell
def _(mo):
    tab_about = mo.md(
        """
### Ceron D’Souza  
Aspiring Investment Banking & Finance Professional

**Summary:**  
First-year Accounting & Finance student at Bayes Business School with a strong interest in financial markets, company analysis, and data-driven decision-making. I am developing practical skills in Python, data visualisation, and financial analysis to better understand how market data translates into real-world investment decisions.

**Education:**  
- **BSc Accounting & Finance**, Bayes Business School

**Skills:**  
- Python  
- pandas  
- Plotly  
- Data visualisation  
- GitHub  
- marimo  

**Experience:**  
- **Amplify Trading:** Real-time trading and M&A simulations using macroeconomic news and market data  
- **Sobell Rhodes LLP:** Financial data processing, reconciliations, and Excel-based reporting  
- **Ernst & Young Insight Day:** Exposure to M&A advisory, transaction services, and due diligence  
- **Automotive Reselling Venture:** Cost analysis, pricing strategy, and profit optimisation  

**Interests:**  
Financial markets, investing, business, MMA, and personal development.
"""
    )
    return (tab_about,)


@app.cell
def _(cap_slider, chart, mo, sector_dropdown):
    tab_project = mo.vstack(
        [
            mo.md("## Passion Project: Credit Risk & Cost of Debt Analysis"),
            mo.callout(
                mo.md(
                    "This dashboard analyses how a company's financial health (Altman Z-score) affects its cost of borrowing. It highlights how riskier firms tend to face higher debt costs across sectors."
                ),
                kind="info",
            ),
            mo.hstack([sector_dropdown, cap_slider], justify="center", gap=2),
            chart,
            mo.md(
                """
### Key Insight
Companies with lower Z-scores, which indicate greater financial distress, generally face higher borrowing costs. This shows how lenders price risk into debt and why credit analysis matters in finance.
"""
            ),
        ]
    )
    return (tab_project,)


@app.cell
def _(mo, travel_chart):
    tab_personal = mo.vstack(
        [
            mo.md("## Personal Interests"),
            mo.md(
                "Outside academics, I am interested in travel, markets, business, fitness, and personal development."
            ),
            travel_chart,
        ]
    )
    return (tab_personal,)


@app.cell
def _(mo, tab_about, tab_personal, tab_project):
    tabs = mo.ui.tabs(
        {
            "About Me": tab_about,
            "Passion Project": tab_project,
            "Personal Interests": tab_personal,
        }
    )

    page = mo.md(
        f"""
# **Ceron Dsouza**
---
{tabs}
"""
    )
    return (page,)


@app.cell
def _(page):
    page
    return


if __name__ == "__main__":
    app.run()