from requests_html import HTMLSession

session = HTMLSession()
r = session.get("https://www.borse.it/fondi/quotazione/Schroder-GAIA-Helix-C-Cap-EUR-Hedged/Schroder-GAIA-Helix-C-Cap-EUR-Hedged__LU1809996553.EUR/")
html = r.content
print(html)