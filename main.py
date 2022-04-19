import discord
import requests
from bs4 import BeautifulSoup
import json
import asyncio
import lxml
import asyncio
from discord.ext import commands
import re
from discord.ui import Button, View, Select
import urllib.parse
from time import time, sleep
import collections
from discord.ext import tasks
bot = commands.Bot(command_prefix=".")
client = discord.Client()


# forsencord user list
kill_list = ['ND', 'v1darr', 'azaelwu1', 'betr8byhumanity', 'v1darr', 'thomasrobin91', 'apr292000', 'jerooo159']

# TMDB
api = 'bb1c3b1185ad7a94b4426faf3d96f304'

@bot.slash_command(
    name="cast",
    description="Search for a cast member",
    guild_ids=[847169717689122816])
async def embed(ctx, cast):
    print(f"Searched cast: {cast}")
    URL = f'https://letterboxd.com/search/cast-crew/{cast}/'

    # getting the data from page mentioned above
    r = requests.get(URL)
    soup = BeautifulSoup(r.content, 'html.parser')
    test = soup.find("h2", class_="title-2 prettify")
    if test is None:
        await ctx.respond(f"No cast member found with search {cast}")
    else:
        URL = test.a['href']
        castt = URL
        castt = castt.replace("-", " ")
        castt = castt.replace("director", "")
        castt = castt.replace("actor", "")
        for line in castt:
            castt = castt.replace("/", "")
        casturl = f"https://letterboxd.com{URL}/"
        URL = f'https://api.themoviedb.org/3/search/person?api_key={api}&language=en-US&query={castt}&page=1&include_adult=false'

        # getting the data from page mentioned above
        r = requests.get(URL)
        r = r.text
        r = json.loads(r)

        # creating lists in which to store first, most popular person in case of multiple people with similar names
        iddd = []
        pfpp = []

        # scraping ID from TMDB api
        for id in r['results']:
            idd = id['id']
            # adding ID's to list
            iddd.append(idd)

        # scraping pfp from TMDB api
        for cast1 in r['results']:
            pfp = cast1['profile_path']
            # adding pfp's to list
            pfpp.append(pfp)

        pfp_url = f"https://image.tmdb.org/t/p/w342/{pfpp[0]}"
        URL = f"https://api.themoviedb.org/3/person/{iddd[0]}?api_key={api}&language=en-US"

        # sending GET requests to API page for requested person and scraping text
        r = requests.get(URL)
        r = r.text
        # turning text into JSON
        r = json.loads(r)

        # scraping different kinds of information from JSON
        deathday = r['deathday']
        birthday = r['birthday']
        pob = r['place_of_birth']
        bio = r['biography']
        name = r['name']

        # checking if person is dead, if true it sends death data.
        if deathday != None:
            embed = discord.Embed(title=f"{name}", url=f"{casturl}", description=
            f"**Birthday:** {birthday}\n"
            f"**Date of death:** {deathday}\n"
            f"**Place of Birth:** {pob}",
                                  color=0x57e389)
            embed.set_thumbnail(url=f"{pfp_url}")
            await ctx.respond(embed=embed)
        else:
            embed = discord.Embed(title=f"{name}", url=f"{casturl}", description=
            f"**Birthday:** {birthday}\n"
            f"**Place of Birth:** {pob}",
                                  color=0x57e389)
            embed.set_thumbnail(url=f"{pfp_url}")
            await ctx.respond(embed=embed)

@bot.slash_command(
    name="diary",
    description="Fetch users last 5 diary entries",
    guild_ids=[847169717689122816])
async def embed(ctx, user):
    print(f"Diary search for: {user}")
    acc = user
    user = f"https://letterboxd.com/{user}/rss/"
    r = requests.get(user)
    soup = BeautifulSoup(r.content, "xml")
    entries = soup.find_all('item')
    if "[]" == str(entries):
        await ctx.respond(f"No user found with search {user}")
    else:
        diary = []
        titles = []
        date = []
        username = []
        years = []
        rewatch = []
        fuck = []
        for entry in entries:
            hng = entry.title.text.split("-")[-1]
            rewtch = entry.rewatch
            title = entry.filmTitle
            year = entry.filmYear
            link = entry.link.text
            usr = entry.creator.text
            watch = entry.watchedDate
            rewatch.append(rewtch)
            date.append(watch)
            username.append(usr)
            titles.append(title)
            years.append(year)
            diary.append(link)
            fuck.append(hng)
        print(fuck)
        rewatch[0] = str(rewatch[0])
        rewatch[1] = str(rewatch[1])
        rewatch[2] = str(rewatch[2])
        rewatch[3] = str(rewatch[3])
        rewatch[4] = str(rewatch[4])

        titles[0] = str(titles[0])
        titles[1] = str(titles[1])
        titles[2] = str(titles[2])
        titles[3] = str(titles[3])
        titles[4] = str(titles[4])

        titles[0] = titles[0].replace("</letterboxd:filmTitle>", "").replace("<letterboxd:filmTitle>", "")
        titles[1] = titles[1].replace("</letterboxd:filmTitle>", "").replace("<letterboxd:filmTitle>", "")
        titles[2] = titles[2].replace("</letterboxd:filmTitle>", "").replace("<letterboxd:filmTitle>", "")
        titles[3] = titles[3].replace("</letterboxd:filmTitle>", "").replace("<letterboxd:filmTitle>", "")
        titles[4] = titles[4].replace("</letterboxd:filmTitle>", "").replace("<letterboxd:filmTitle>", "")

        years[0] = str(years[0])
        years[1] = str(years[1])
        years[2] = str(years[2])
        years[3] = str(years[3])
        years[4] = str(years[4])

        years[0] = years[0].replace("</letterboxd:filmYear>", "").replace("<letterboxd:filmYear>", "")
        years[1] = years[1].replace("</letterboxd:filmYear>", "").replace("<letterboxd:filmYear>", "")
        years[2] = years[2].replace("</letterboxd:filmYear>", "").replace("<letterboxd:filmYear>", "")
        years[3] = years[3].replace("</letterboxd:filmYear>", "").replace("<letterboxd:filmYear>", "")
        years[4] = years[4].replace("</letterboxd:filmYear>", "").replace("<letterboxd:filmYear>", "")

        date[0] = str(date[0])
        date[1] = str(date[1])
        date[2] = str(date[2])
        date[3] = str(date[3])
        date[4] = str(date[4])

        date[0] = date[0].replace("</letterboxd:watchedDate>", "").replace("<letterboxd:watchedDate>", "")
        date[1] = date[1].replace("</letterboxd:watchedDate>", "").replace("<letterboxd:watchedDate>", "")
        date[2] = date[2].replace("</letterboxd:watchedDate>", "").replace("<letterboxd:watchedDate>", "")
        date[3] = date[3].replace("</letterboxd:watchedDate>", "").replace("<letterboxd:watchedDate>", "")
        date[4] = date[4].replace("</letterboxd:watchedDate>", "").replace("<letterboxd:watchedDate>", "")

        if "Yes" in rewatch[0]:
            date[0] = f"↺ {date[0]}"
        if "Yes" in rewatch[1]:
            date[1] = f"↺ {date[1]}"
        if "Yes" in rewatch[0]:
            date[2] = f"↺ {date[2]}"
        if "Yes" in rewatch[0]:
            date[3] = f"↺ {date[3]}"
        if "Yes" in rewatch[4]:
            date[4] = f"↺ {date[4]}"

        if "★" in fuck[0]:
            date[0] = f"{fuck[0]}  -  {date[0]}"
        elif "½" in fuck[0]:
            date[0] = f"{fuck[0]}  -  {date[0]}"
        if "★" in fuck[1]:
            date[1] = f"{fuck[1]}  -  {date[1]}"
        elif "½" in fuck[1]:
            date[1] = f"{fuck[1]}  -  {date[1]}"
        if "★" in fuck[2]:
            date[2] = f"{fuck[2]}  -  {date[2]}"
        elif "½" in fuck[2]:
            date[2] = f"{fuck[2]}  -  {date[2]}"
        if "★" in fuck[3]:
            date[3] = f"{fuck[3]}  -  {date[3]}"
        elif "½" in fuck[3]:
            date[3] = f"{fuck[3]}  -  {date[3]}"
        if "★" in fuck[4]:
            date[4] = f"{fuck[4]}  -  {date[4]}"
        elif "½" in fuck[4]:
            date[4] = f"{fuck[4]}  -  {date[4]}"

        r = requests.get(f'https://letterboxd.com/{acc}')
        # making data easier to read
        soup = BeautifulSoup(r.content, 'html.parser')
        picture = soup.find("span", class_="avatar -a110 -large")
        picture = picture.img['src']
        picture = picture.replace("avtr-0-220-0-220-crop.jpg?k=ce5e63fd91", 'avtr-0-1000-0-1000-crop.jpg')
        embed = discord.Embed(title=f"{username[0]}'s latest diary entries", url=f"https://letterboxd.com/{acc}",
                              description=
                              f"\n**-[{titles[0]} ({years[0]})]({diary[0]})\n{date[0]}"
                              f"\n-[{titles[1]} ({years[1]})]({diary[1]})\n{date[1]}"
                              f"\n-[{titles[2]} ({years[2]})]({diary[2]})\n{date[2]}"
                              f"\n-[{titles[3]} ({years[3]})]({diary[3]})\n{date[3]}"
                              f"\n-[{titles[4]} ({years[4]})]({diary[4]})\n{date[4]}**", color=0x57e389)
        embed.set_thumbnail(url=f"{picture}")
        await ctx.respond(embed=embed)

@bot.slash_command(
    name="search",
    description="Search for a movie",
    guild_ids=[847169717689122816])
async def embed(ctx, film):
    print(f"Movie search: {film}")
    URL = f"https://letterboxd.com/search/films/{film}/?adult"

    # getting the data from page mentioned above
    r = requests.get(URL)
    soup = BeautifulSoup(r.content, 'html.parser')
    check = soup.find("h2", class_="section-heading")
    if "No results" in str(check):
        embed = discord.Embed(description=f"No movie found with search '{film}'", color=0x57e389)
        await ctx.respond(embed=embed)
    elif 'films matching “' or "film matching" in str(check):
        test = soup.find("span", class_="film-title-wrapper")
        URL = test.a['href']
        filmpage = "https://letterboxd.com" + URL + ""
        # parsing URL to movie page
        r = requests.get(filmpage)
        soup = BeautifulSoup(r.content, 'html.parser')

        # working on removing extra data from title string, which shall only include title and year
        title = soup.title.text
        temptitle = title.split(" (", 1)
        temptitle = temptitle[0]
        # extracting year from original string that contained too much information
        year = title.split("(", 1)
        year = year[1]
        year = year.split(")", 1)
        year = year[0]
        year = year.replace(year, "(" + year + ")")
        # fully working title, name + year
        title = f"{temptitle} {year}"

        # stats page that can be accessed by adding title of movie as seen below
        stats = f'https://letterboxd.com/esi{URL}stats/'

        # exctracting movies views on letterboxd
        r = requests.get(stats)
        stats = BeautifulSoup(r.content, 'html.parser')
        watches = stats.find('a', class_="has-icon icon-watched icon-16 tooltip")
        watches = watches.text

        crew = soup.find('div', {'id': "tab-crew"})
        crew = crew.find('span')

        # removing extra data from tag that contains runtime, only includes minutes  + "mins"
        runtime = soup.find('p', class_="text-link text-footer")
        runtime = (runtime.text)
        runtime = " ".join(runtime.split())
        runtime = runtime.replace('More at IMDb TMDb Report this film', '')

        # find scipt that include statistics
        info = soup.find('script', type="application/ld+json")
        # removing extra data from tag that includes information for easier exctraction
        info = info.string
        info = info.replace('/* <![CDATA[ */', '')
        info = info.replace('/* ]]> */', '')

        # extracting image
        image = json.loads(info)
        if "image" in str(image):
            image = image['image']
        else:
            image = "https://s.ltrbxd.com/static/img/empty-poster-230.876e6b8e.png"


        # extracting rating
        rating = json.loads(info)
        if 'aggregateRating' not in rating:
            rating = "none"
        else:
            rating = json.dumps(rating['aggregateRating'])
            rating = json.loads(rating)
            rating = rating['ratingValue']

        # scraping genre
        info = json.loads(info)
        if "countryOfOrigin" not in info:
            country = "none"
        else:
            country = info
            country = str([country["name"] for country in country["countryOfOrigin"]])
            country = country.replace(']', '')
            country = country.replace('[', '')
            country = country.replace("'", '')
        if "genre" not in info:
            genre = "none"
        else:
            genre = json.dumps(info['genre'])
            for i in genre:
                genre = genre.replace('"', '')
                genre = genre.replace('[', '')
                genre = genre.replace(']', '')

        # scraping tag that includes directors name from the original film page.

        director = soup.find("span", class_="prettify")
        director = director.text
        if genre == "none":
            genre = ""
        else:
            genre = f'\n**Genres:** {genre}\n'
        rating = f'**Rating:** {rating}/5'
        if runtime == "none":
            runtime = ""
        else:
            runtime = f'**Runtime:** {runtime}\n'
        if "," in country:
            country = f'**Countries:** {country}\n'
        if "," not in country and country != "none":
            country = f'**Country:** {country}\n'
        if country == "none":
            country = ""
        embed = discord.Embed(title=f"{title}",
                              url=f"{filmpage}",
                              description=f"**Director:** {director}\n{rating}{genre}{country}Watched by **{watches}** members",
                              color=0x57e389)
        embed.set_thumbnail(url=f"{image}")
        await ctx.respond(embed=embed)
    else:
        embed = discord.Embed(description=f"An error has occured! Please contact ND#0661 with the following message: `{check}`", color=0x57e389)
        await ctx.respond(embed=embed)

@bot.slash_command(
    name="user",
    description="Look up a Letterboxd user",
    guild_ids=[847169717689122816])
async def embed(ctx, user):
    print(f"Searched for profile: {user}")
    profileurl = f'https://letterboxd.com/{user}/'

    # sending GET request to URL
    r = requests.get(profileurl)
    # making data easier to read
    soup = BeautifulSoup(r.content, 'html.parser')

    # parsing follow/followers information
    follow_stats = soup.find("div", "profile-stats js-profile-stats")
    if follow_stats is None:
        embed = discord.Embed(description=f"No user found with search {user}", color=0x57e389)
        await ctx.respond(embed=embed)
    else:
        follow_stats = soup.find_all("h4", class_="profile-statistic statistic")
        follow_stats = soup.find("div", "profile-stats js-profile-stats")
        follow_stats = soup.find_all("h4", class_="profile-statistic statistic")

        followers = follow_stats[4]
        followers = followers.text.replace("Followers", "")

        following = follow_stats[3]
        following = following.text.replace("Following", "")

        lists_made = follow_stats[2]
        lists_made = lists_made.text.replace("Lists", "")

        this_year = follow_stats[1]
        this_year = this_year.text.replace("This year", "")
        this_year = this_year.partition('This')[0]

        total_watched = follow_stats[0]
        total_watched = total_watched.text.replace("Films", "")

        # scraping username because it has correct capitalizing and some info
        usernamee = soup.find("meta", property="og:title")
        usernamee = usernamee['content']

        # getting users profile picture
        picture = soup.find("span", class_="avatar -a110 -large")
        picture = picture.img['src']
        picture = picture.replace("avtr-0-220-0-220-crop.jpg?k=ce5e63fd91", 'avtr-0-1000-0-1000-crop.jpg')

        favs = soup.find("meta", property="og:description")
        favs = str(favs)
        check = "Favorites:"

        # scrapes movies watched
        watched = favs.partition('lists. ')[2]
        watched = watched.partition(' watched.')[0]

        if check in favs:
            favs = str(favs)

            favorites = soup.find("section", class_="section")
            favorites = favorites.find_all("li", class_="poster-container")

            # scrapes top 4
            favs = favs.partition('Favorites: ')[2]
            favs = favs.partition('. B')[0]
            favs = favs.replace(")", "))")
            favs = str(favs)
            string = favs
            print(string)
            lst = string.split('),')

            lst[3] = lst[3].replace("))", ")")

            # adding favorites to a list
            lolfav = []
            for lines in favorites:
                favorites = lines.div['data-film-slug']
                favorites = favorites
                lolfav.append(favorites)

            # getting top 4 url's and adding them to list
            movieurl = []
            for lines in lolfav:
                URL = f"https://letterboxd.com{lines}"
                movieurl.append(URL)
            embed = discord.Embed(title=f"{usernamee}", url=f"{profileurl}",
                                  description=
                                  f"**Films watched: {total_watched} ({this_year} this year)**"
                                  f"\n-[{lst[0]}]({movieurl[0]})\n"
                                  f"-[{lst[1]}]({movieurl[1]})\n"
                                  f"-[{lst[2]}]({movieurl[2]})\n"
                                  f"-[{lst[3]}]({movieurl[3]})",
                                  color=0x57e389)
            embed.set_thumbnail(url=f"{picture}")
            embed.set_footer(text=f"Followers: {followers} | Following: {following}")
            await ctx.respond(embed=embed)

        else:
            embed = discord.Embed(title=f"{usernamee}", url=f"{profileurl}",
                                  description=
                                  f"**Films watched: {total_watched} ({this_year} this year)**",
                                  color=0x57e389)
            embed.set_thumbnail(url=f"{picture}")
            embed.set_footer(text=f"Followers: {followers} | Following: {following}")
            await ctx.respond(embed=embed)

@bot.slash_command(
    name="review",
    description="Search for a users reivew of a movie",
    guild_ids=[847169717689122816])
async def embed(ctx, user, film):
    print(f"Searched for {user}'s review of {film}")
    URL = f"https://letterboxd.com/search/films/{film}/?adult"
    # getting the data from page mentioned above
    r = requests.get(URL)
    soup = BeautifulSoup(r.content, 'html.parser')
    test = soup.find("span", class_="film-title-wrapper")
    if "No results" in str(test):
        await ctx.respond(f"No movie found with the title{film}")
    if 'href="/film/' in str(test):
        # finding URL from top result to redirect to the movie
        URL = test.a['href']
        r = requests.get(f'https://letterboxd.com/{user}{URL}')
        soup = BeautifulSoup(r.content, 'html.parser')
        avt = soup.find("img", height="24")
        if avt is None:
            embed = discord.Embed(description=f"{user} is either entered incorrect or hasn't logged {URL}", color=0x57e389)
            await ctx.respond(embed=embed)
        if '<img alt="' in str(avt):
            usr = avt['alt']
            avt = avt["src"]  # .split("-", 1)[0].replace("resized/", "")
            title = soup.title.text.replace(' • Letterboxd', '')
            print(title)
            review = soup.find('script', type="application/ld+json")
            test = soup.find("p", class_="view-date date-links")
            test = test.text
            test = " ".join(test.split())
            if review is None:
                poster = f"https://letterboxd.com/{URL}"
                r = requests.get(poster)
                soup = BeautifulSoup(r.content, 'html.parser')

                # find scipt that include statistics
                info = soup.find('script', type="application/ld+json")
                # removing extra data from tag that includes information for easier exctraction
                info = info.string
                info = info.replace('/* <![CDATA[ */', '')
                info = info.replace('/* ]]> */', '')

                # extracting image
                image = json.loads(info)
                if "image" in str(image):
                    image = image['image']


                embed = discord.Embed(title=f"{title}", url=f"{r.url}", color=0x57e389)
                embed.add_field(name=f"{test}", value=f'test', inline=False)
                embed.set_thumbnail(url=f"{image}")
                embed.set_author(name=f"{usr}", url=f"https://letterboxd.com/{user}", icon_url=f"{avt}")
                await ctx.respond(embed=embed)
            else:
                script = review.string
                script = script.replace('/* <![CDATA[ */', '')
                script = script.replace('/* ]]> */', '')
                script = json.loads(script)
                print(script)
                review = "reviewBody"
                image = script["itemReviewed"]
                poster = image["image"].split("-0", 1)[0].replace("resized/", "")
                print(poster)
                rating = 'reviewRating'

                published = json.dumps(script['datePublished'])
                published = published.replace('"', '')
                print(rating)
                # if reviewed the following is executed
                if review in script and rating in script:
                    regex = re.compile('.*rating rating-large.*')
                    for EachPart in soup.find_all("span", {"class": regex}):
                        rating = EachPart.get_text()
                    rating = rating.replace(" ", "")
                    review = script['reviewBody']
                    embed = discord.Embed(title=f"{title}", url=f"{r.url}", color=0x57e389)
                    embed.add_field(name=f"{published} {rating}", value=f"**`{review}`**", inline=False)
                    embed.set_thumbnail(url=f"{poster}")
                    embed.set_author(name=f"{usr}", url=f"https://letterboxd.com/{user}", icon_url=f"{avt}")
                    await ctx.respond(embed=embed)
                if review in script and rating not in script:
                    review = script['reviewBody']
                    embed = discord.Embed(title=f"{title}", url=f"{r.url}", color=0x57e389)
                    embed.add_field(name=f"{published}", value=f'{review}', inline=False)
                    embed.set_thumbnail(url=f"{poster}")
                    embed.set_author(name=f"{usr}", url=f"https://letterboxd.com/{user}", icon_url=f"{avt}")
                    await ctx.respond(embed=embed)
                if review not in script and rating in script:
                    regex = re.compile('.*rating rating-large.*')
                    for EachPart in soup.find_all("span", {"class": regex}):
                        rating = EachPart.get_text()
                    rating = rating.replace(" ", "")
                    embed = discord.Embed(title=f"{title}", url=f"{r.url}", color=0x57e389)
                    embed.add_field(name=f"{published} {rating}", value=f'test', inline=False)
                    embed.set_thumbnail(url=f"{poster}")
                    embed.set_author(name=f"{usr}", url=f"https://letterboxd.com/{user}", icon_url=f"{avt}")
                    await ctx.respond(embed=embed)

@bot.slash_command(
    name="list",
    description="Search for a users list",
    guild_ids=[847169717689122816])
async def embed(ctx, user, list):

# starts the discord bot
bot.run('')
