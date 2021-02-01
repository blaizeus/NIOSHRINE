from flask import Flask, render_template

app=Flask(__name__)

@app.route("/")
def home():

    from pandas_datareader import data
    from datetime import datetime, timedelta
    from bokeh.plotting import figure, show, output_file
    from bokeh.embed import components
    from bokeh.resources import CDN
    import requests
    from bs4 import BeautifulSoup
    
    end = datetime.today() - timedelta(1)
    lastMonth = end - timedelta(30)
    lastYear = end - timedelta(365)

    df=data.DataReader(name="NIO", data_source="yahoo", start=lastMonth, end=end)
    df2=data.DataReader(name="NIO", data_source="yahoo", start=lastYear, end=end)

    def inc_dec(c, o):
        if c > o:
            value="Increase"
        elif c < o:
            value="Decrease"
        else:
            value="Equal"
        return value

    df["Status"]=[inc_dec(c, o) for c,o in zip(df.Close, df.Open)]
    df2["Status"]=[inc_dec(c, o) for c,o in zip(df2.Close, df2.Open)]

    df["Middle"]=(df.Open+df.Close)/2
    df2["Middle"]=(df2.Open+df2.Close)/2

    df["Height"]=abs(df.Close-df.Open)
    df2["Height"]=abs(df2.Close-df2.Open)

    p=figure(x_axis_type='datetime', width=1000, height=300, sizing_mode="scale_width")
    p.title.text="NIO Inc."
    p.grid.grid_line_alpha = 0.3

    p2=figure(x_axis_type='datetime', width=1000, height=300, sizing_mode="scale_width")
    p2.title.text="NIO Inc."
    p2.grid.grid_line_alpha = 0.3

    hours_12 = 12 * 60 * 60 * 1000

    p.segment(df.index, df.High, df.index, df.Low, color="black")
    p2.segment(df2.index, df2.High, df2.index, df2.Low, color="black")

    p.rect(df.index[df.Status=="Increase"], df.Middle[df.Status=="Increase"],
        hours_12, df.Height[df.Status=="Increase"],
        fill_color="#3CB371", line_color="black")
    p.rect(df.index[df.Status=="Decrease"], df.Middle[df.Status=="Decrease"],
        hours_12, df.Height[df.Status=="Decrease"],
        fill_color="#DC143C", line_color="black")

    p2.rect(df2.index[df2.Status=="Increase"], df2.Middle[df2.Status=="Increase"],
        hours_12, df2.Height[df2.Status=="Increase"],
        fill_color="#3CB371", line_color="black")
    p2.rect(df2.index[df2.Status=="Decrease"], df2.Middle[df2.Status=="Decrease"],
        hours_12, df2.Height[df2.Status=="Decrease"],
        fill_color="#DC143C", line_color="black")

    script1, div1 = components(p)
    script2, div2 = components(p2)

    cdn_js=CDN.js_files[0]

    r = requests.get("https://www.marketwatch.com/investing/stock/nio?mod=over_search",  headers={'User-agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:61.0) Gecko/20100101 Firefox/61.0'})
    c = r.content
    soup = BeautifulSoup(c, "html.parser")
    articles_latest = soup.find_all("div", {"class": "element--article"})[:3]
    article_content_list = [obj.find("div", {"class": "article__content"}) for obj in articles_latest]
    article_headline_list = [obj.find("h3", {"class": "article__headline"}) for obj in article_content_list]
    article_link_list = [obj.find("a", {"class": "link"}).get("href") for obj in article_headline_list]

    def rm_xtra_spaces(line):
        outputLst = []
        pos = 0
        for char in line:
            if char != " " or line[pos - 1] != " ":
                outputLst.append(char)          
            pos += 1
        return "".join(outputLst)[:-1]

    article_headline_list = [rm_xtra_spaces(obj.find("a", {"class": "link"}).text.replace("\r\n", "")) for obj in article_headline_list]
    article_time_list = [obj.find("span", {"class": "article__timestamp"}).text for obj in article_content_list]

    reddit = 'https://www.reddit.com'

    r2 = requests.get("https://www.reddit.com/r/wallstreetbets/search?q=nio&restrict_sr=1&t=week",  headers={'User-agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:61.0) Gecko/20100101 Firefox/61.0'}) 
    c2 = r2.content
    soup2 = BeautifulSoup(c2, "html.parser")
    body = soup2.find_all("div")[36]
    post_lst = body.contents[:3]
    post_content_lst = [obj.contents[0].contents[0].contents[1].contents[0].contents[1] for obj in post_lst]
    post_header_lst = [obj.contents[0].contents[0].find("span").text for obj in post_content_lst]
    post_link_list = [(reddit + obj.contents[0].contents[0].contents[0].get("href")) for obj in post_content_lst]
    post_posted_list = [obj.contents[1].contents[2].find("a").text for obj in post_content_lst]



    return render_template("plot.html",
     script1=script1,
      div1=div1,
      script2=script2,
      div2=div2,
      cdn_js=cdn_js,
      arty_h=article_headline_list,
      arty_l=article_link_list,
      arty_d=article_time_list,
      post_h=post_header_lst,
      post_l=post_link_list,
      post_d=post_posted_list
      )

@app.route("/about")
def about():
    return render_template("about.html")



if __name__ == "__main__":
    app.run(debug=True)

