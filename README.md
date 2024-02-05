# Binance Trader Bot - Analyse et Scrap

Ce projet Python est conçu pour interagir avec l'API de Binance pour récupérer et analyser les données des traders sur la plateforme. Il permet aux utilisateurs de suivre les performances des traders de futures sur Binance, incluant les données détaillées de trading comme les positions, le montant, le levier et le prix d'entrée.

## Fonctionnalités

- **Récupération des Données des Traders**: Extrait les données en temps réel des traders sur Binance.
- **Analyse des Performances**: Analyse les données récupérées pour fournir des insights sur les performances des traders.
- **Logging**: Enregistre les événements et les données importantes pour un suivi facilité.

## Installation

1. Clonez ce dépôt sur votre système.
2. Assurez-vous que Python 3.x est installé sur votre machine.
3. Installez les dépendances requises en exécutant `pip install -r requirements.txt` dans le répertoire du projet.
4. (Optionnel) Configurez `logging` en modifiant le fichier de configuration selon vos besoins.

## Configuration

- Assurez-vous que le module `requests` et `colorama` sont installés pour permettre l'exécution des requêtes HTTP et l'affichage en couleur dans le terminal.
- Configurez le fichier `trader_info.py` pour définir les informations spécifiques du trader que vous souhaitez suivre.

## Utilisation

Lancez le script principal pour démarrer le bot :

```sh
python <nom_du_script>.py
```

Remplacez `<nom_du_script>` par le nom de fichier approprié.

## Commandes et Fonctionnalités

- Le bot ne fonctionne pas avec des commandes Telegram directes mais se base sur des interactions programmées pour récupérer et analyser les données.
- Consultez les logs dans le dossier `LOG` pour suivre les activités du bot et les données des traders récupérées.

## Développement

Pour ajouter de nouvelles fonctionnalités ou améliorer le bot, modifiez les modules Python selon vos besoins. Les contributions externes sont également bienvenues.

## Licence

Ce projet est distribué sous une licence open source. Veuillez consulter le fichier `LICENSE` pour plus de détails.
