from datetime import datetime, timedelta
import json as js
import matplotlib.pyplot as plt
def get_date(mess):
    return mess.get('date')[:7] #4-year;7-months;10-days
def stat_build(messages):
    start_date_str=messages[0].get('date')
    end_date_str=messages[-1].get('date')
    start_date=datetime.fromisoformat(start_date_str)
    end_date=datetime.fromisoformat(end_date_str)
    
    date_list = [start_date + timedelta(days=x*30) for x in range((end_date - start_date).days//30 + 1)]

    date_dict={date.strftime('%Y-%m'): 0 for date in date_list}
    for message in messages:
        date=get_date(message)
        date_dict[date]+=1
        
    return date_dict

def main():
    path="Telegram_analysis/result.json"
    with open(path, "r",encoding="utf-8") as file:
        chat=js.load(file)
    messages=chat.get("messages")
    date_dict = stat_build(messages)
    date_list=list(date_dict.keys())
    frq_list=list(date_dict.values())
    
    fig, ax = plt.subplots()
    fig.patch.set_facecolor('#424242')
    ax.set_facecolor('#424242')
    
    ax.bar(date_list, frq_list, color='lightblue', alpha=0.8, zorder=1)
    ax.set_axisbelow(True)
    
    plt.xlabel("Months", color="white")
    plt.ylabel("Number of messages", color="white")
    plt.title("Вот столько мы общались Биба", color="white")
    plt.xticks(rotation=50)
    plt.subplots_adjust(left=0.05, right=0.985, top=0.954, bottom=0.082, wspace=0.2, hspace=0.2)

    
    #y_ticks = [i for i in range(0, 6001, 500)]
    #ax.set_yticks(y_ticks)
    
    for tick in ax.get_xticklabels() + ax.get_yticklabels():
        tick.set_color('white')
    ax.grid(color="black", zorder=0)
    
    plt.show()
    
if __name__=="__main__":
    main()