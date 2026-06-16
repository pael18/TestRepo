import pandas as pd
import os

def nettoyer_fichier_csv(fichier_entree, fichier_sortie=None):
    """
    Nettoie un fichier CSV :
    - supprime certaines colonnes
    - réorganise les colonnes
    - nettoie les lignes vides
    """

    # Colonnes à supprimer
    colonnes_a_supprimer = [
        'screen name',
        'verified',
        'client',
        'region',
        'city',
        'quoting',
        'permalink',
        'replies to',
        'quotes'
    ]

    # Ordre souhaité
    ordre_colonnes = [
        'display name',
        'followers',
        'bio',
        'date',
        'lang',
        'text',
        'country',
        'original id',
        'sentiment',
        'impressions',
        'views',
        'retweets'
    ]

    try:
        print("📖 Lecture du fichier CSV...")

        # Tentatives de lecture
        try:
            df = pd.read_csv(
                fichier_entree,
                sep=';',
                encoding='utf-8'
            )

        except UnicodeDecodeError:
            df = pd.read_csv(
                fichier_entree,
                sep=';',
                encoding='latin1'
            )

        except pd.errors.ParserError:
            df = pd.read_csv(
                fichier_entree,
                sep=',',
                encoding='utf-8'
            )

        print(f"✅ Fichier chargé : {df.shape[0]} lignes, {df.shape[1]} colonnes")

        # Nettoyage des noms de colonnes
        df.columns = df.columns.str.strip()

        print("\n📋 Colonnes détectées :")
        for i, col in enumerate(df.columns, 1):
            print(f"{i}. {col}")

        # Supprimer colonnes inutiles
        colonnes_existantes = [
            col for col in colonnes_a_supprimer
            if col in df.columns
        ]

        if colonnes_existantes:
            df.drop(columns=colonnes_existantes, inplace=True)

            print("\n🗑️ Colonnes supprimées :")
            for col in colonnes_existantes:
                print(f"- {col}")

        else:
            print("\n⚠️ Aucune colonne à supprimer trouvée")

        # Supprimer lignes totalement vides
        print("\n🧹 Nettoyage des données...")
        df.dropna(how='all', inplace=True)

        # Réinitialiser index
        df.reset_index(drop=True, inplace=True)

        # Réorganisation des colonnes
        print("\n🔄 Réorganisation des colonnes...")

        colonnes_finales = []

        # Colonnes dans l'ordre souhaité
        for col in ordre_colonnes:
            if col in df.columns:
                colonnes_finales.append(col)

        # Ajouter le reste
        for col in df.columns:
            if col not in colonnes_finales:
                colonnes_finales.append(col)

        # Réorganisation
        df = df[colonnes_finales]

        print("\n📋 Colonnes finales :")
        for i, col in enumerate(df.columns, 1):
            print(f"{i}. {col}")

        # Nom du fichier de sortie
        if fichier_sortie is None:
            nom_base = os.path.splitext(fichier_entree)[0]
            fichier_sortie = f"{nom_base}_nettoye.csv"

        # Sauvegarde
        print(f"\n💾 Sauvegarde : {fichier_sortie}")

        df.to_csv(
            fichier_sortie,
            index=False,
            encoding='utf-8-sig',
            sep=';'
        )

        print("\n✅ Nettoyage terminé avec succès !")

        print("\n📊 Résumé :")
        print(f"Lignes   : {df.shape[0]}")
        print(f"Colonnes : {df.shape[1]}")

        return df

    except FileNotFoundError:
        print(f"❌ Fichier introuvable : {fichier_entree}")

    except Exception as e:
        print(f"❌ Erreur : {e}")

        return None


# =========================
# EXÉCUTION
# =========================

if __name__ == "__main__":

    print("🔧 Nettoyage CSV")
    print("=" * 40)

    fichier_entree = input(
        "📁 Nom du fichier CSV : "
    ).strip()

    if not os.path.exists(fichier_entree):

        print(f"\n❌ Le fichier '{fichier_entree}' n'existe pas.")

        fichiers_csv = [
            f for f in os.listdir('.')
            if f.endswith('.csv')
        ]

        if fichiers_csv:

            print("\n📂 Fichiers CSV disponibles :")

            for i, fichier in enumerate(fichiers_csv, 1):
                print(f"{i}. {fichier}")

        else:
            print("\n⚠️ Aucun fichier CSV trouvé.")

    else:
        nettoyer_fichier_csv(fichier_entree)

    input("\nAppuyez sur Entrée pour quitter...")