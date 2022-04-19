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
