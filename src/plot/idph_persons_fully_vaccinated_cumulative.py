from matplotlib import dates
import pandas as pd


def plot(df):
    ax = df.plot(
        kind="bar",
        figsize=(18, 12),
        rot=0,
        title="Persons Fully Vaccinated",
        xlabel="",
        ylabel="Persons fully vaccinated (tens of millions)",
        legend=False,
    )
    ax.xaxis.set_major_locator(dates.MonthLocator())
    ax.xaxis.set_major_formatter(dates.DateFormatter("%B"))
    fig = ax.get_figure()
    return fig


# SINCE JANUARY
df = pd.read_csv("output/idph_fully_vaccinated_total_cumulative_daily.csv")
fig = plot(df)
filename = "output/img/idph_persons_fully_vaccinated_cumulative_jan21_present"
fig.savefig(f"{filename}.svg", facecolor="white")
fig.savefig(f"{filename}.png", facecolor="white")

# LAST 7 DAYS
df["report_date"] = pd.to_datetime(df.report_date)
df = df[df.report_date >= pd.Timestamp.today() - pd.Timedelta(days=7)].copy()
df["report_date"] = df.report_date.dt.strftime("%Y-%m-%d")
fig = plot(df)
filename = "output/img/idph_persons_fully_vaccinated_cumulative_last_7_days"
fig.savefig(f"{filename}.svg", facecolor="white")
fig.savefig(f"{filename}.png", facecolor="white")
