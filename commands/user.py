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
