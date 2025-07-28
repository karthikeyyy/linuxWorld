from pywebcopy import save_webpage

url = "https://openai.com/index/chatgpt/"
download_folder = "downloaded_site"

save_webpage(
    url=url,
    project_folder=download_folder,
    open_in_browser=False,
    delay=None,
    threaded=False,
)
print("Webpage and resources downloaded successfully.")
