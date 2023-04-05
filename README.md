# NYPL Digital Collections Project
This is a simple Django app to read data from the NYPL digital collections and chart some info. Specifically, it retrieves all data for a given search term and gives a pie chart of the counts of the resource types for the returned data.

This is only a single view and template. Chart.js is used to display the chart.

Currently no data is written to the database. Originally, I was intending to add each query term to a database, so that if a given query were attempted again within some time period, say two weeks since the last query, the results could be gotten from the database rather than hitting the API again needlessly. There was not time to complete that, but I did build the models for the three tables necessary, and there are settings for a postgres database in `settings.py`.

Three unit tests are included, two for bad requests and a third for a good request/response. At least one additional test is needed, where mocked API response json is used, but I didn't have time to suss out the mock capabilities in Django to get that running.

