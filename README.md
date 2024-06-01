# What is this?
This downloads all your raid PGCRs (Post Game Carnage Report) from the Bungie.net api and builds some graphs.

Credit for graphs and PGCR collection goes to Mijago (Twitter: https://twitter.com/MijagoCoding/, GitHub: https://github.com/Mijago/). This was forked off their D2StatGenerator project.

# How to Use?
3) Install all required packages
   1) `python3 -m pip install pandas plotly pathos requests pretty_html_table bar-chart-race tqdm`
   2) You should use MP4 instead of GIF, install `python3 -m pip install python-ffmpeg` and put a [ffmpeg](https://www.ffmpeg.org/download.html) in your PATH variable. 
      1) You can use GIF but the file size will be generally much larger. Set the `VIDEO_TYPE` in `main.py` to `gif`.
      **I highly encourage you to use MP4 as the gifs tend to be 40mb in size whereas the mp4 is only around 1.5mb~2mb**.
   
4) Set your API key as an environemnt variable `BUNGIE_API_KEY`.  Get the key [here](https://www.bungie.net/en/Application).
   1) Alternatively: Add your api key to `main.py`. For this, edit `# API_KEY = "123456789"`.
5) Edit your user info in `main.py`. Alternatively, you can also use command line parameters to set this later.
   ```py
   MEMBERSHIP_MIJAGO = (3, 4611686018482684809)
   MEMBERSHIP_SUPERQ = (3, 4611686018472661350) # for example, add this
   USED_MEMBERSHIP = MEMBERSHIP_SUPERQ
   ```
6) Run the script `python3 main.py`.
   1) Complete Example: `BUNGIE_API_KEY=123456789012345   python3 main.py -p 3 -id 4611686018472661350`
   2) This may take a while

# Where do I get my user ID?
1) Go to https://www.bungie.net/7/en/Destiny (or any other similar page)
2) Search for your user, open your profile page
3) Look at the URL: `https://www.bungie.net/7/en/User/Profile/3/4611686018472661350`
   In this case, `3` is your MEMBERSHIP_TYPE and `4611686018472661350` is the MEMBERSHIP_ID, so you'll do something like `MEMBERSHIP_SUPERQ = (3, 4611686018472661350)`.
