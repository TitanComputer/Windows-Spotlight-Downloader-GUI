import traceback
import requests
import os
import re
import json
from time import sleep
from datetime import datetime
from bs4 import BeautifulSoup as BS
from gui_module import *

STATE_FILE = "state.json"
FirstRun = True
Counter = 0
url = "https://windows10spotlight.com"
proxies = {"http": "socks5://192.168.1.3:1080", "https": "socks5://192.168.1.3:1080"}
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
    "Accept-Language": "en-US,en;q=0.5",
    "Referer": "https://google.com",
    "Connection": "keep-alive",
}
timeout = 5


def load_state():
    if os.path.exists(STATE_FILE):
        with open(STATE_FILE, "r") as f:
            return json.load(f)
    return {}


def save_state(state):
    with open(STATE_FILE, "w") as f:
        json.dump(state, f, indent=4)


def URLGrabber(url):
    try:
        global request, TestStatus
        TestStatus = True
        request = requests.get(url, headers=headers, timeout=timeout)
        return request, TestStatus
    except:
        TestStatus = False
        app.add_log_line("Network Error. Please Check Your Connection And Try Again...")
        return TestStatus


def FileSaver(content, path):
    try:
        os.makedirs("Download\\%s" % Type)
    except:
        pass
    try:
        global Counter
        with open(path, "wb") as file:
            file.write(content)
            Counter += 1
            app.add_log_line("%i File(s) Saved" % Counter)
    except:
        app.add_log_line("File is locked or inaccessible.")


def HTMLParser(data):
    global soup, PageTitle
    data = request.text
    soup = BS(data, "html.parser")
    PageTitle = (
        re.sub("[^A-Za-z0-9]", " ", str(soup.find("h1").text).strip()).strip().replace("   ", " ").replace("  ", " ")
    )
    return soup, PageTitle


def main():
    global Type, url, FirstRun, state
    state = load_state()
    if state.get("full_run_done") == None:
        state["full_run_done"] = False
        state["last_post_date"] = "2000-01-01"
        save_state(state)

    if app.mode_var.get() == "landscape":
        mode = "Landscape"
        app.add_log_line("Landscape mode selected.")
    elif app.mode_var.get() == "portrait":
        mode = "Portrait"
        app.add_log_line("Portrait mode selected.")
    else:
        mode = "Default"
        app.add_log_line("Default mode selected. Both of Landscape and Portrait will be downloaded")

    start_time = datetime.now()
    app.add_log_line("The program started at " + datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
    while True:
        URLGrabber(url)
        if TestStatus == True:
            if request.status_code == 200:
                HTMLParser(request)
                if FirstRun == True:
                    LastPageNumber = str(
                        soup.find("div", class_="nav-links")
                        .find("span", class_="page-numbers dots")
                        .find_next("a", class_="page-numbers")
                        .text
                    ).replace(",", "")
                    RecentPostDate = soup.find("span", class_="date").text
                    FirstRun = False
                CurrentPageNumber = str(soup.find("span", class_="page-numbers current").text).replace(",", "")
                app.add_log_line("Page %s of %s " % (CurrentPageNumber, LastPageNumber))
                app.after(0, app.update_progress, int(CurrentPageNumber), int(LastPageNumber))
                PostsLinks = soup.find_all("a", class_="anons-thumbnail show")
                try:
                    NextPage = soup.find("a", class_="next page-numbers").get("href")
                    url = NextPage
                except:
                    url = None
                    pass
                PostURL = []
                for link in PostsLinks:
                    PostURL.append(link.get("href"))
                while len(PostURL) > 0:
                    Post = PostURL[0]
                    URLGrabber(Post)
                    if TestStatus == True:
                        if request.status_code == 200:
                            HTMLParser(request)
                            ImageLink = soup.find("div", class_="entry").find_all("a")
                            PostDate = soup.find("span", class_="date").text
                            isPortrait = True
                            while len(ImageLink) > 0:
                                if isPortrait:
                                    Type = "Portrait"
                                else:
                                    Type = "Landscape"
                                ContentURL = ImageLink[-1].get("href")
                                Extension = ContentURL.rsplit(".", 1)[-1]
                                if Extension.lower() in ["jpeg", "jpg", "png", "bmp", "tiff", "webp"]:
                                    Path = "Download\\%s\\%s-%s.%s" % (
                                        Type,
                                        PageTitle,
                                        Type,
                                        Extension,
                                    )
                                    if (mode == "Landscape" and Type == "Landscape") or mode == "Default":
                                        if not (
                                            os.path.isfile(Path)
                                            and os.access(Path, os.R_OK)
                                            and os.stat(Path).st_size > 10240
                                        ):
                                            URLGrabber(ContentURL)
                                            if TestStatus == True:
                                                if request.status_code == 200:
                                                    Content = request.content
                                                    FileSaver(Content, Path)
                                            else:
                                                app.add_log_line("Trying Again After 30 Seconds...")
                                                sleep(30)
                                                continue
                                        else:
                                            app.add_log_line("File already exists:", Path)
                                    elif (mode == "Portrait" and Type == "Portrait") or mode == "Default":
                                        if not (
                                            os.path.isfile(Path)
                                            and os.access(Path, os.R_OK)
                                            and os.stat(Path).st_size > 10240
                                        ):
                                            URLGrabber(ContentURL)
                                            if TestStatus == True:
                                                if request.status_code == 200:
                                                    Content = request.content
                                                    FileSaver(Content, Path)
                                            else:
                                                app.add_log_line("Trying Again After 30 Seconds...")
                                                sleep(30)
                                                continue
                                        else:
                                            app.add_log_line("File already exists:", Path)
                                    else:
                                        pass
                                ImageLink.pop(-1)
                                isPortrait = False
                                # sleep(1)
                            PostURL.pop(0)
                    else:
                        app.add_log_line("Trying Again After 30 Seconds...")
                        sleep(30)
                        continue
                if url == None:
                    app.add_log_line("That was last page.")
                    state["full_run_done"] = True
                    state["last_post_date"] = RecentPostDate
                    save_state(state)
                    break
                if PostDate < state["last_post_date"] and state["full_run_done"] == True:
                    app.add_log_line("All of New Images Has Been Downloaded")
                    state["last_post_date"] = RecentPostDate
                    save_state(state)
                    break
        else:
            app.add_log_line("Trying Again After 30 Seconds...")
            sleep(30)
            continue
    end_time = datetime.now()
    duration = end_time - start_time
    total_seconds = int(duration.total_seconds())
    hours = total_seconds // 3600
    minutes = (total_seconds % 3600) // 60
    seconds = total_seconds % 60
    app.add_log_line("The program ended at " + datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
    app.add_log_line(f"The program ran in {hours} hour(s), {minutes} minute(s), and {seconds} second(s).")
    app.after(0, app.update_progress, int(LastPageNumber), int(LastPageNumber))
    app.working_animation_running = False
    app.working_status = False
    app.start_button.config(state="disabled", text="Done!", style="done.TButton")
    pass


try:
    app = SpotlightDownloaderApp(start_callback=main)
    app.mainloop()
except Exception:
    app.add_log_line("An error occurred. Details are written to 'error.log'")
    # print("An error occurred. Details are written to 'error.log'")
    traceback.print_exc()
    with open("error.log", "a") as log_file:
        log_file.write("=== ERROR START ===\n")
        traceback.print_exc(file=log_file)
        log_file.write("=== ERROR END ===\n\n")
# finally:
#     input("Press Enter to exit...")
