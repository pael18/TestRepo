import pandas as pd
import requests
import feedparser
from datetime import datetime, timezone
from urllib.parse import urlparse

# Paramètres du rapport
compte_collab = "DiplomatieTogo"
date_debut = datetime(2025, 10, 1, tzinfo=timezone.utc)
date_fin = datetime.now(timezone.utc)

print(f"Analyse du compte {compte_collab}...")

try:
    url_rss = f"https://nitter.net/{compte_collab}/rss"
    headers = {"User-Agent": "Mozilla/5.0"}
    reponse = requests.get(url_rss, headers=headers, timeout=30)
    reponse.raise_for_status()

    feed = feedparser.parse(reponse.content)
    donnees = []

    for entry in feed.entries:
        date_pub = entry.get("published_parsed")
        if not date_pub:
            continue

        date_tweet = datetime(
            date_pub.tm_year,
            date_pub.tm_mon,
            date_pub.tm_mday,
            date_pub.tm_hour,
            date_pub.tm_min,
            date_pub.tm_sec,
            tzinfo=timezone.utc,
        )

        if date_tweet < date_debut or date_tweet > date_fin:
            continue

        texte = entry.get("title", "")
        texte = texte.split(" - ", 1)[-1] if " - " in texte else texte
        texte = " ".join(texte.split())

        link = entry.get("link", "")
        parsed = urlparse(link)
        tweet_id = parsed.path.split("/")[-1] if parsed.path else ""

        donnees.append(
            {
                "Date": date_tweet.strftime("%Y-%m-%d %H:%M"),
                "ID Tweet": tweet_id,
                "Texte": texte[:280],
                "URL": link,
                # Les métriques exactes ne sont pas disponibles via le flux RSS public
                "Likes": None,
                "Retweets": None,
                "Réponses": None,
            }
        )

    df = pd.DataFrame(donnees)

    if not df.empty:
        nom_fichier = f"rapport_{compte_collab}.xlsx"
        df.to_excel(nom_fichier, index=False)

        print("\n--- RÉSUMÉ DU RAPPORT ---")
        print(f"Nombre de posts récupérés : {len(df)}")
        print("Métriques exactes : non disponibles via ce flux public")
        print(f"\n✅ Fichier Excel sauvegardé : {nom_fichier}")
    else:
        print("Aucune publication trouvée sur cette période.")

except Exception as e:
    print(f"Erreur : {e}")
    print(
        "Conseil : vérifie que le compte est public et que le flux RSS est accessible."
    )