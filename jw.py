#!/usr/bin/env python3
from justwatch import JustWatch
from flask import Flask, request, jsonify
from os import environ
from discord_interactions import verify_key_decorator, InteractionType, InteractionResponseType
from discord import Embed

jw = JustWatch(country="AU")

providers = {p["id"]: p for p in jw.get_providers()}

app = Flask(__name__)
PUBKEY = environ["JWBOT_PUBKEY"]

@app.route("/", methods=["POST"])
@verify_key_decorator(PUBKEY)
def route():
    if not "type" in request.json:
        return jsonify({})
    if request.json["type"] == InteractionType.PING:
        return jsonify({"type": InteractionResponseType.PONG})
    elif request.json["type"] == InteractionType.APPLICATION_COMMAND:
        if request.json["data"]["name"] == "watch":
            kwargs = {d["name"]:d["value"] for d in request.json["data"]["options"]}
            filtered_count = 0
            embeds = []
            for count, embed in watch(**kwargs):
                filtered_count += count
                embeds.append(embed)
            return jsonify({
                "type": InteractionResponseType.CHANNEL_MESSAGE_WITH_SOURCE,
                "data": {
                    "tts": False,
                    "content": "{} results skipped".format(filtered_count) if filtered_count else None,
                    "embeds": embeds,
                    "allowed_mentions": []
                }
            })
        print(request.json)
        return jsonify({
            "type": InteractionResponseType.CHANNEL_MESSAGE_WITH_SOURCE,
            "data": {
                "tts": False,
                "content": "Command received",
                "embeds": [],
                "allowed_mentions": []
            }
        })

def watch(name, _type=["movie", "show"], result_count=3, dontskipnonfree=False):
    if type(_type) is not list:
        _type = [_type]
    skipnonfree = not dontskipnonfree
    req = {
        "query": name,
        "content_types": _type or ["movie", "show"],
        "providers": ['dnp', 'ivw', 'nfx', 'nnw', 'prv', 'sbs', 'spl', 'stn', 'tpl'],
        "monetization_types": ["free", "flatrate"]
    }
    print(req)
    resp = jw.search_for_item(**req)
    urls = []
    for item in resp["items"][:result_count]:
        embed = Embed(title="{title} ({original_release_year})".format(**item), url="https://www.justwatch.com{full_path}".format(**item))
        if skipnonfree:
            offers = [o for o in item["offers"] if o["monetization_type"] in req["monetization_types"]]
        else:
            offers = item["offers"]
        for offer in sorted(offers, key=lambda o: o["presentation_type"])[:5]:
            provider = providers[offer["provider_id"]]
            if provider["short_name"] not in req["providers"]:
                continue
            if offer["urls"]["standard_web"] in urls:
                continue
            urls.append(offer["urls"]["standard_web"])
            embed.add_field(name=provider["clear_name"], value="{presentation_type}: {urls[standard_web]}".format(**offer))
        filtered_count = len(item["offers"]) - len(offers)
        yield filtered_count, embed.to_dict()

if __name__ == "__main__":
    app.run(port=8001, debug=True)
