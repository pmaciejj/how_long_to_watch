import tkinter as tk
import tkinter.ttk as ttk
import requests
from bs4 import BeautifulSoup
import datetime


def get_info():
    global title
    global ep_lenght
    global ep_num
    # url = r"https://www.imdb.com/title/tt1266020/"
    # url =r"https://www.imdb.com/title/tt0411008/"

    url = ent_url.get()
    if "www.imdb.com" in url:

        try:
            s = requests.session()
            req = s.get(url)

            soup = BeautifulSoup(req.text, "html.parser")

            title = soup.find("h1",class_ = "sc-b73cd867-0 eKrKux").text
            print(title)
            att_list = soup.find("ul",class_ = "ipc-inline-list ipc-inline-list--show-dividers sc-8c396aa2-0 kqWovI baseAlt")
            ep_lenght = att_list.findAll("li")[-1:][0].text
            print(ep_lenght)

            ep_num =  soup.find("h3",class_ = "ipc-title__text").text
            ep_num = ep_num.replace("Episodes","")
            print(ep_num)

            info = "Title: " + title  + "\nNumber of episodes: " + ep_num + "\nEpisode lenght: " + ep_lenght
            lbl_info = tk.Label(text=info)
            lbl_info.grid(row=1,columnspan=3)
        except Exception as e:
            print(str(e))

    elif "test" in url:

        ep_lenght = "40m"
        ep_num = "100"

def show_split_option():
    
    if watch_by.get() == "h":
        
        lbl_split.grid(row=3,column=2)
        rd_y.grid(row=4,column=2)
        rd_n.grid(row=5,column=2)
        
def hide_split_option():

    if watch_by.get() != "h":
        
        lbl_split.grid_remove()
        rd_y.grid_remove()
        rd_n.grid_remove()


def calculate():

    split_v = watch_split.get()
    if split_v is None or split_v =="":
        split_v = "unknown"

    if "m" in ep_lenght:
        ep_lenght_v = int(ep_lenght.replace("m",""))
    elif "h" in ep_lenght:
        ep_lenght_v = float(ep_lenght.replace("h","")) * 60
    ep_num_v = int(ep_num)
    watch_interval_v = watch_interval.get()
    watch_by_v = watch_by.get()
    v = int(ent_value.get()) 
    # print(f"watch_interval_v {watch_interval_v}")
    # print(f"watch_by_v {watch_by_v}")
    # print(f"split {split_v}")
    # print(f"ep_lenght {ep_lenght_v}")
    # print(f"ep_num {ep_num_v}")

    total_time = ep_lenght_v * ep_num_v


    if total_time >= 1440:
        d  = int(total_time/1440)
    else:
        d = 0

    h = int((total_time - (d * 1440))/60)
    m = total_time - d * 1440 - h * 60
    total_time_txt = str(h) + " hours " + str(m) + " mins"
    if d>0:
         total_time_txt = str(d) + " days " + total_time_txt

    print(total_time_txt)

    if watch_by_v == "e":
        if watch_interval_v =="d":
            end_date = ts + datetime.timedelta(days=int(ep_num_v/v))
        elif watch_interval_v =="w":
            end_date = ts + datetime.timedelta(days=int(ep_num_v/v)*7)
    elif watch_by_v == "h":
        v = v * 60
        if split_v == "n":
            num_ep_per_int =   int(v / ep_lenght_v)
        elif split_v == "y":
            num_ep_per_int =   v / ep_lenght_v
        if watch_interval_v == "d":
            end_date = ts + datetime.timedelta(days=int(ep_num_v/num_ep_per_int))
        if watch_interval_v == "w":
            end_date = ts + datetime.timedelta(days=int(ep_num_v/num_ep_per_int) * 7)
    end_date = datetime.datetime.strftime(end_date,format("%Y-%m-%d"))
    print(end_date)

    lbl_result = tk.Label(text="Results",font = "bold")
    lbl_result.grid(row=7,columnspan=3,pady=8)

    lbl_total_time = tk.Label(text = "Total lenght")
    lbl_finish = tk.Label(text= "Finish date")

    lbl_total_time_v = tk.Label(text = total_time_txt)
    lbl_finish_v = tk.Label(text=end_date)


    lbl_total_time.grid(row=8,column=0)
    lbl_finish.grid(row=9,column=0)

    lbl_total_time_v.grid(row=8,column=1,columnspan=2)
    lbl_finish_v.grid(row=9,column=1,columnspan=2)


ts = datetime.date.today()

window = tk.Tk()


window.title("how long to watch")
window.geometry("400x400")
window.resizable(False,False)

# row in url input and button to webscrap lenght and num of episodes
lbl_url = tk.Label(text="Imdb link: ",width=20)
lbl_url.grid(row=0,column=0,pady=5,sticky=tk.W)

ent_url = tk.Entry(width=20)
ent_url.grid(row=0,column=1)

btn_get_info = tk.Button(text="Get info",width=10,command=get_info)
btn_get_info.grid(row=0,column=2,padx=10)


lbl_watch_plan = tk.Label(text="Watch plan",font="bold")
lbl_watch_plan.grid(row=2,columnspan=3,pady=8)


# row with headers (Interval,By, Split) for radiobuttons
lbl_interval = tk.Label(text="Interval")
lbl_interval.grid(row=3,column=0)

lbl_by = tk.Label(text="By")
lbl_by.grid(row=3,column=1)

lbl_split = tk.Label(text="Split episodes")

## 2 rows with radiobuttons
watch_interval = tk.StringVar()
rd_week = ttk.Radiobutton(text="Weekly", value="w",variable=watch_interval)
rd_daily = ttk.Radiobutton(text="Daily",value = "d",variable=watch_interval)


rd_week.grid(row=4,column=0)
rd_daily.grid(row=5,column=0)


watch_split = tk.StringVar()

rd_y = ttk.Radiobutton(text="Yes",value = "y",variable=watch_split)
rd_n = ttk.Radiobutton(text="No", value="n",variable=watch_split)


watch_by = tk.StringVar()
rd_episodes = ttk.Radiobutton(text="Episodes",value = "e",variable=watch_by,command=hide_split_option)
rd_hour = ttk.Radiobutton(text="Hour", value="h",variable=watch_by,command= show_split_option)

rd_episodes.grid(row=4,column=1)
rd_hour.grid(row=5,column=1)

# row from eps/hours value and calc button

lbl_value = tk.Label(text="Num of eps/hours")
lbl_value.grid(row = 6,column=0,pady=8)

ent_value = tk.Entry()
ent_value.grid(row=6,column=1,pady=8)

btn_cal = tk.Button(text="Calculate",command=calculate)
btn_cal.grid(row=6,column=2,pady=8)

window.mainloop()