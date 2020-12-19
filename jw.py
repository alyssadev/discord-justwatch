#!/usr/bin/env python3
import discord
from justwatch import JustWatch

jw = JustWatch(country="AU")

providers = {p["id"]: p for p in jw.get_providers()}

client = discord.Client()

@client.event
async def on_message(message):
    if message.author == client.user:
        return

    if message.content.startswith("!watch"):
        args = message.content.split()[1:]
        if not args:
            await message.channel.send("!watch <name> [:(movie/show)] [+number_of_results(default 3)] [=provider(e.g stn,nfx,dnp)] [&&]")
            await message.channel.send("Options that aren't flat rate or free are excluded. To include those options, add && to the query")
            return
        c = []
        p = []
        result_count = 3
        dontskip = True
        for a in list(args):
            if a[0] == ":":
                c.append(a[1:])
                args.remove(a)
            if a[0] == "+":
                if a[1:].isdigit():
                    result_count = int(a[1:])
                args.remove(a)
            if a[0] == "=":
                p.append(a[1:])
                args.remove(a)
            if a == "&&":
                dontskip = False
                args.remove(a)
        req = {
            "query": " ".join(args),
            "content_types": c or ["movie", "show"],
            "providers": p or ['dnp', 'ivw', 'nfx', 'nnw', 'prv', 'sbs', 'spl', 'stn', 'tpl'],
            "monetization_types": ["free", "flatrate"]
        }
        print(req)
        resp = jw.search_for_item(**req)
        embeds = []
        for item in resp["items"][:result_count]:
            embed = discord.Embed(title="{title} ({original_release_year})".format(**item), url="https://www.justwatch.com{full_path}".format(**item))
            if dontskip:
                offers = [o for o in item["offers"] if o["monetization_type"] in req["monetization_types"]]
            else:
                offers = item["offers"]
            for offer in sorted(offers, key=lambda o: o["presentation_type"])[:5]:
                provider = providers[offer["provider_id"]]
                embed.add_field(name=provider["clear_name"], value="{presentation_type}: {urls[standard_web]}".format(**offer))
            filtered_count = len(item["offers"]) - len(offers)
            await message.channel.send(content="filtered {} results for not being free or flatrate".format(filtered_count) if filtered_count else None, embed=embed)

@client.event
async def on_connect():
    print("connected")

if __name__ == "__main__":
    with open(".bottoken") as f:
        client.run(f.read().strip())
