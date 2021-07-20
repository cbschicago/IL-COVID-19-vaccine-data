from matplotlib import dates
import pandas as pd


def plot(df, month_format):
    def plot_subplot(df, kind, ax=None, color="#1F77B4", month_format=month_format):
        if not month_format:
            df.index = df.index.map(lambda d: d.strftime("%b %d"))
        ax = df.plot(
            kind=kind,
            figsize=(18, 12),
            rot=0,
            title="Persons Fully Vaccinated",
            xlabel="",
            ylabel="Persons fully vaccinated",
            legend=False,
            ax=ax,
            color=color,
        )
        if month_format:
            ax.xaxis.set_major_locator(dates.MonthLocator())
            ax.xaxis.set_major_formatter(dates.DateFormatter("%B"))
        return ax

    if month_format:
        bar_ax = plot_subplot(df[["persons_fully_vaccinated_change"]], "bar")
        plot_subplot(
            df[["persons_fully_vaccinated_7_day_avg"]],
            "line",
            ax=bar_ax,
            color="orange",
        )
        fig = bar_ax.get_figure()
    else:
        line_ax = plot_subplot(
            df[["persons_fully_vaccinated_7_day_avg"]],
            "line",
            color="orange",
        )
        plot_subplot(
            df[["persons_fully_vaccinated_change"]],
            "bar",
            ax=line_ax,
        )
        fig = line_ax.get_figure()
    return fig


df = pd.read_csv("output/idph_vaccine_administration_data_daily_statewide.csv")[
    ["report_date", "persons_fully_vaccinated_change"]
].drop_duplicates()
df["persons_fully_vaccinated_7_day_avg"] = (
    df.persons_fully_vaccinated_change.rolling(7).mean().shift(-18)
)
# SINCE JANUARY
df["report_date"] = pd.to_datetime(df.report_date)
df = df[df.report_date >= "2021-01-01"]
fig = plot(df, True)
filename = "output/img/idph_persons_fully_vaccinated_daily_jan21_present"
fig.savefig(f"{filename}.svg", facecolor="white")
fig.savefig(f"{filename}.png", facecolor="white")

# LAST 7 DAYS
df["report_date"] = pd.to_datetime(df.report_date)
df = df.set_index("report_date")
df = df.tail(7)
fig = plot(df, False)
filename = "output/img/idph_persons_fully_vaccinated_daily_last_7_days"
fig.savefig(f"{filename}.svg", facecolor="white")
fig.savefig(f"{filename}.png", facecolor="white")
