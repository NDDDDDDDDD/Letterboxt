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
