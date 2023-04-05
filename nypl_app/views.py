import json
from collections import defaultdict
from os import getenv

import requests
from django.db import connection
from django.http import HttpResponse, HttpResponseBadRequest
from django.shortcuts import render
from django.views.generic import TemplateView
from dotenv import load_dotenv


class IndexView(TemplateView):
    template_name = "nyplsite/index.jinja"


def index(request):
    """
    Retrieve data from API endpoint, write to dictionary, return call to index
    jinja file.

    Would have loved to exand this by writing to database and only making calls
    when, say, the last time the request was made was over two weeks ago, but
    time did not allow.
    """

    if request.method == "GET":
        if "query" in request.GET:
            search_term = request.GET.get("query")
        else:
            return HttpResponseBadRequest(
                "The query string was malformed. Please try again. "
                "A proper call is https://address?query=search_term."
            )
    if search_term:
        # The query was well-formed and valid.
        load_dotenv()
        TOKEN = getenv("TOKEN")
        request.session["search_term"] = search_term
        url = "https://api.repo.nypl.org/api/v2/items/search"
        headers = {
            "Content-Type": "application/json",
            "Authorization": f'Token token="{TOKEN}"',
        }
        # Note, only search public domain records. No real reason for that; I
        # just didn't change it from the example on the API usage page.
        # Also, only getting a single record on the first call because we just
        # need the number of results.
        params = {"publicDomainOnly": True, "q": search_term, "per_page": 1000}
        r = requests.get(url=url, headers=headers, params=params)
        if r.status_code == 200:
            # We've received a good response from the api. Now process it.
            resource_types = {} # This will be a dict of resourceType: count.
            num_items = int(r.json()["nyplAPI"]["response"]["numResults"])
            for page in range(num_items // 1000 + 1):
                # 1000 items per page in order to cut down on the total number
                # of queries, which is rate limited.
                params = {
                    "publicDomainOnly": True,
                    "q": search_term,
                    "per_page": 1000,
                    "page": page,
                }
                r = requests.get(url=url, headers=headers, params=params)
                for result in r.json()["nyplAPI"]["response"]["result"]:
                    if "typeOfResource" not in result:
                        resource_types["not specified"] = (
                            resource_types.get("not specified", 0) + 1
                        )
                        # print('missing typeOfResource')
                        # print(result)
                    else:
                        resource_types[result["typeOfResource"]] = (
                            resource_types.get(result["typeOfResource"], 0) + 1
                        )
            return render(
                request,
                "nyplsite/index.jinja",
                {
                    "resource_types": resource_types,
                    "search_term": search_term,
                    "num_items": num_items,
                },
            )
        return HttpResponse(
            f"<h2>Search request for {search_term} failed with code {r.status_code}.</h2>"
        )
    else:
        return HttpResponseBadRequest(
            "<h2>Please enter a search term into the url, as such: </h2>"
            "https://address?query=search_term."
        )
