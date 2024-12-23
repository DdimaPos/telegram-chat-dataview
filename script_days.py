import json as js
from datetime import datetime, timedelta

import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch, Rectangle
### constants

def get_date(mess):
    # 4-year;7-months;10-days (number of symbols in date yyyy-mm-dd)
    return mess.get("date")[:10]


def stat_build(messages):
    start_date_str = messages[0].get("date")
    end_date_str = messages[-1].get("date")
    start_date = datetime.fromisoformat(start_date_str)
    end_date = datetime.fromisoformat(end_date_str)

    date_list = [
        start_date + timedelta(days=x) for x in range((end_date - start_date).days + 2)
    ]

    date_dict = {date.strftime("%Y-%m-%d"): 0 for date in date_list}
    for message in messages:
        date = get_date(message)
        date_dict[date] += 1

    return date_dict


def main():
    path = "Telegram_analysis/result.json"
    with open(path, "r", encoding="utf-8") as file:
        chat = js.load(file)
    messages = chat.get("messages")
    date_dict = stat_build(messages)
    date_list = list(date_dict.keys())
    frq_list = list(date_dict.values())

    fig, ax = plt.subplots()
    fig.patch.set_facecolor("#fff")
    ax.set_facecolor("#fff")

    bars = ax.bar(date_list, frq_list, color="#dd70e0", alpha=0.9, zorder=1)
    # try to round the bars
    for i, bar in enumerate(bars):
        ax.text(
            bar.get_x() + bar.get_width() / 2,
            bar.get_height() + 0.5,
            frq_list[i],
            ha="center",
            va="bottom",
            color="black",
            weight="light",
            fontsize=10,
        )

        if bar.get_height() > 0.15 * max(frq_list):  # rounding_size
            round_top = FancyBboxPatch(
                xy=bar.get_xy(),  # use the original bar's values to fill the new bar
                width=bar.get_width(),
                height=bar.get_height(),
                color=bar.get_facecolor(),
                boxstyle="round,pad=0,rounding_size=0.15",
                transform=ax.transData,
                mutation_scale=1.1,
                mutation_aspect=20,
            )
            # Over write the bottom half of the original bar with a Rectangle patch
            square_bottom = Rectangle(
                xy=bar.get_xy(),
                width=bar.get_width(),
                height=bar.get_height() / 15,
                color=bar.get_facecolor(),
                transform=ax.transData,
                alpha=0.9,
            )
            # remove the original bar from the plot
            bar.remove()
            # add the new artists to the plot
            ax.add_patch(round_top)
            ax.add_patch(square_bottom)

    #####
    ax.set_axisbelow(True)
    xticks = ax.get_xticks()
    # ax.set_xticks(xticks[::10])
    ax.set_xticklabels(
        [
            f"{date_list[i]}" if i % 1 == 0 else "" for i, x in enumerate(xticks)
        ]  # set the interval of labels on x-axis here
    )

    plt.xlabel("Day", color="black")
    plt.ylabel("Number of messages", color="black")
    # plt.title(", color="black")
    plt.xticks(rotation=50)
    plt.subplots_adjust(
        left=0.05, right=0.985, top=0.954, bottom=0.1, wspace=0.2, hspace=0.2
    )

    y_ticks = [i for i in range(0, 700, 50)]
    ax.set_yticks(y_ticks)

    for tick in ax.get_xticklabels() + ax.get_yticklabels():
        tick.set_color("#000")
    ax.grid(color="grey", alpha=0.8, zorder=0)

    plt.show()


if __name__ == "__main__":
    main()
