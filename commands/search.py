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
