---
title: "Classification multimodale de produits Rakuten"
author: "Lanoë Steven, Gisèle, Tom"
date: "09/05/2025"
geometry: margin=1in
fig_caption: true
bibliography: references.bib
header-includes:
  - \setcounter{tocdepth}{3}
---

\newpage


# 1. Introduction et objectifs

## 1.1 Aperçu des spécifications

Le projet Rakuten vise à automatiser la classification de produits à l’aide de données textuelles et visuelles. Le système cible les administrateurs et les clients du site Rakuten France. Il est basé sur une architecture MLOps complète et doit répondre à des contraintes de performance, de traçabilité, de supervision et d’évolution.

## 1.2 Objectifs de qualité

Les objectifs de qualité du projet sont définis selon les caractéristiques ISO 25010 :

- **Efficacité** : temps de réponse API < 500 ms, inférence IA < 1s/image
- **Fiabilité** : disponibilité > 99.5%, redondance et supervision continue
- **Utilisabilité** : interface intuitive pour administrateurs via Streamlit
- **Sécurité** : chiffrement, OAuth2, logs d’accès, RGPD
- **Maintenabilité** : architecture modulaire, CI/CD, tests automatisés
- **Adaptabilité** : ajustement du modèle selon le drift via Evidently

L’approche MLOps est essentielle pour garantir la qualité, la reproductibilité et la scalabilité du modèle déployé. Elle permet de :
- Assurer l’automatisation complète du pipeline de développement jusqu’au déploiement ;
- Suivre les performances en production et détecter les dérives ;
- Faciliter la collaboration entre les équipes Data, Dev et Ops ;
- Intégrer les bonnes pratiques DevOps dans les workflows IA (tests, CI/CD, monitoring, etc.) ;
- Maintenir un cycle de vie de modèle durable et traçable.

## 1.3 Parties prenantes

- Équipe data (modèle, ingestion, MLOps)
- Équipe dev (UI/UX, API)
- Architecte et DevOps (infrastructure, CI/CD)
- Métiers (utilisateurs finaux : clients & admins Rakuten)

# 2. Contraintes

## 2.1 Contraintes techniques
L'objectif est de mettre en oeuvre les technologies vues lors des sprints de formation :
- Environnement :
  - Git & GitHub : Gestion de version du code source et collaboration entre développeurs,
  - FastAPI : Framework Python moderne pour créer des API,
- Suivi d'expérience & versioning :
  - DVC & DagsHub : Versionning des données, des modèles et pipelines ML, avec traçabilité sur Git (DVC) et interface graphique collaborative (DagsHub),
  - MLflow : Suivi des expériences, des métriques de performance, enregistrement des modèles et visualisation de leur historique,
- Orchestration & déploiement :
  - Airflow : Outil d’orchestration de workflows pour automatiser les tâches répétitives (préprocessing, entraînement, sauvegardes, etc.),
  - BentoML : Framework de packaging et de déploiement de modèles IA sous forme d’API REST prêtes pour la production,
- Monitoring : 
  - Prometheus & Grafana : Prometheus collecte les métriques système et applicatives, Grafana permet leur visualisation via des dashboards temps réel,
  - Evidently : Surveillance des performances des modèles IA et détection automatique de dérive des données (data drift, concept drift),
- Scaling & MLOPS plateform :
  - Kubernetes : Orchestrateur de conteneurs pour le déploiement scalable, la répartition de charge et la tolérance aux pannes,
  - ZenML : Framework pour structurer des pipelines MLOps modulaires, traçables et portables, compatible avec de nombreux outils comme MLflow, Airflow et Kubernetes.

## 2.2 Contraintes organisationnelles
L'implémentation est organisée sous forme de sprints :
- Sprint 1 : Créer l’environnement d’exécution avec Docker
- Sprint 2 : Développer le modèle, structurer les données et suivre les expériences avec MLflow, DVC, tracking, versioning
- Sprint 3 : Automatiser le pipeline de bout en bout et rendre le modèle accessible via Airflow, déploiement API et BentoML
- Sprint 4 : Mettre en place le monitoring (Prometheus, Grafana, Evidently)
- Sprint 5 : Assurer la scalabilité avec ZenML et Kubernetes pour l’orchestration et la montée en charge

## 2.3 Conventions

- Langue de développement : anglais (code, variables, commentaires)
- Respect du Software Craftsmanship : code propre, lisible, testé, principe KISS, YAGNI, DRY
- Nommage camelCase (code) et kebab-case (fichiers)
- Conventions MLOps standardisées : modularité, traçabilité, sécurité

# 3. Contexte

## 3.1 Contexte métier

Le projet est une réponse aux besoins de Rakuten de fiabiliser la catégorisation de ses produits pour améliorer la recherche, la recommandation, la gestion du catalogue et le référencement. Le dataset contient 99k produits à classer automatiquement selon plus de 1000 catégories.

## 3.2 Contexte technique

Le projet utilise les données du challenge Rakuten (texte : 60 MB, images : 2.2 GB). L’objectif est de concevoir une architecture modulaire, conteneurisée, supervisée, avec modèle réentraînable.

# 4. Cas d'utilisation (Use-cases)

## 4.1 UC1 — Rechercher un produit
- **Acteur** : Client  
- **Préconditions** : Accès au site en ligne  
- **Scénario principal** :
  1. Le client saisit un mot-clé dans la barre de recherche.  
  2. Le système interroge la base et retourne les produits correspondants.  
  3. Le client consulte un produit.  
- **Flux alternatifs** :  
  - A1 Aucun résultat → Suggestions ou message d’erreur.  

---

## 4.2 UC2 — Recevoir des recommandations
- **Acteur** : Client  
- **Préconditions** : Historique de navigation existant  
- **Scénario principal** :
  1. Le client consulte un produit.  
  2. Le système affiche des produits similaires.  
- **Flux alternatifs** :  
  - A1 Pas de recommandations → Afficher produits populaires.  

---

## 4.3 UC3 — Ajouter un produit au catalogue
- **Acteur** : Admin / MLOps  
- **Préconditions** : Connexion à l’interface d’admin  
- **Scénario principal** :
  1. L’admin saisit les informations produit + image.  
  2. Le système stocke le produit et déclenche la classification.  
  3. Le code produit prédit est affiché.  
- **Flux alternatifs** :  
  - A1 Image absente → Message d’erreur  
  - A2 Score de confiance faible → Demande de validation manuelle  

---

## 4.4 UC4 — Classifier automatiquement un produit
- **Acteur** : Système  
- **Préconditions** : Produit complet avec image + texte  
- **Scénario principal** :
  1. Le modèle IA reçoit les données.  
  2. Une classe parmi 1500 est prédite.  
  3. Le résultat est stocké et associé au produit.  
- **Flux alternatifs** :  
  - A1 Prédiction impossible → File d’attente pour traitement ultérieur  

---

## 4.5 UC5 — Déployer un modèle
- **Acteur** : Admin / MLOps  
- **Préconditions** : Modèle validé via MLflow  
- **Scénario principal** :
  1. L’équipe crée un bento avec BentoML.  
  2. L’image est envoyée sur le registre.  
  3. Kubernetes déploie l’API sur le cluster.  
- **Flux alternatifs** :  
  - A1 Échec → Rollback automatique via CI/CD  

---

## 4.6 UC6 — Monitorer le modèle
- **Acteur** : Admin / MLOps  
- **Préconditions** : API de prédiction active  
- **Scénario principal** :
  1. Prometheus collecte les métriques.  
  2. Grafana les affiche.  
  3. Evidently détecte les dérives.  
  4. L’équipe reçoit une alerte.  
- **Flux alternatifs** :  
  - A1 Inactivité → Redémarrage automatique ou alerte  

---

## 4.7 UC7 — Réentraîner un modèle
- **Acteur** : Admin / MLOps  
- **Préconditions** : Nouvelles données, dérive détectée  
- **Scénario principal** :
  1. ZenML ou Airflow déclenche la pipeline.  
  2. Un nouveau modèle est entraîné et validé.  
  3. Il est enregistré avec MLflow et déployé.  
- **Flux alternatifs** :  
  - A1 Échec d’un job → Reprise partielle ou notification d’erreur  

# 5. Architecture fonctionnelle / logique

Cette vue décrit l’aspect métier de l’architecture. Elle est structurée selon les quatre axes fondamentaux suivants :

## 5.1 Utilisateurs

### 5.1.1 Admin MLOps Rakuten
Gère l’ensemble du cycle de vie des données et du modèle :
- Téléversement des produits dans le catalogue
- Supervision du modèle
- Réentraînement
- Déploiement et maintenance

### 5.1.2 Clients Rakuten
Naviguent sur le site pour rechercher et consulter les produits du catalogue
Ils bénéficient indirectement du système de classification automatique pour la recherche et les recommandations.


## 5.2 Données utilisées / persistées

- **Données textuelles et structurées** :
    - `X_train` : 84 916 lignes, colonnes : `id`, `designation`, `description`, `productid`, `imageid`
    - `X_test` : 13 812 lignes, même structure
    - `y_train` : 84 016 labels associés (`id`, `prdtypecode`)
- **Données images** :
    - Environ 2,2 Go d’images JPEG liées aux produits, référencées par `imageid`

## 5.3 Traitements réalisés / services métier

- Téléversement multimodal (texte + image)
- Enrichissement automatique via modèle IA
- Recherche texte/catégorie
- Accès et consultation produit via front Streamlit

## 5.4 Interfaces avec d'autres applications

Aucune interface avec d'autres applications n’est prévue dans ce projet. Le système est autonome.

# 6. Architecture applicative / logicielle

Cette vue est structurée par application (unité de déploiement).

## 6.1 Application Web (UI)

| Framework | Simplicité | Déploiement | Intégration IA | Accessibilité | Note globale |
| --- | --- | --- | --- | --- | --- |
| Streamlit | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐ |
| Angular | ⭐⭐ | ⭐⭐ | ⭐⭐ | ⭐⭐⭐ | ⭐⭐ |
| React | ⭐⭐⭐ | ⭐⭐⭐ | ⭐⭐⭐ | ⭐⭐⭐⭐ | ⭐⭐⭐ |
| Dash | ⭐⭐⭐ | ⭐⭐⭐⭐ | ⭐⭐⭐⭐ | ⭐⭐⭐ | ⭐⭐⭐⭐ |

Justification : Streamlit permet de créer rapidement une interface performante et adaptée à une application de démonstration IA.

## 6.2 API Backend

| Framework | Performance | Async Support | Documentation Auto | Courbe d’apprentissage | Note globale |
| --- | --- | --- | --- | --- | --- |
| FastAPI | ⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ | ⭐⭐⭐ | ⭐⭐⭐⭐ |
| Flask | ⭐⭐⭐ | ⭐⭐ | ⭐⭐ | ⭐⭐⭐⭐⭐ | ⭐⭐⭐ |
| Django REST | ⭐⭐ | ⭐ | ⭐⭐ | ⭐⭐ | ⭐⭐ |

Choix : FastAPI pour sa rapidité, sa documentation automatique Swagger et son support de l’asynchrone.

## 6.3 Service IA

| Framework | Courbe d'apprentissage | Compatibilité | Communauté | Performance | Note globale |
| --- | --- | --- | --- | --- | --- |
| Keras | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐ | ⭐⭐⭐⭐ |
| PyTorch | ⭐⭐⭐ | ⭐⭐⭐⭐ | ⭐⭐⭐⭐ | ⭐⭐⭐⭐ | ⭐⭐⭐ |
| Sklearn | ⭐⭐⭐⭐ | ⭐⭐ | ⭐⭐⭐⭐ | ⭐⭐ | ⭐⭐ |

Choix : Keras pour la simplicité et son intégration avec TensorFlow. Idéal pour projets à livrer rapidement.

## 6.4 Base de données

| BDD | Performance | SQL Support | ORM Compatibility | Scalabilité | Note globale |
| --- | --- | --- | --- | --- | --- |
| PostgreSQL | ⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐ | ⭐⭐⭐⭐ |
| MySQL | ⭐⭐⭐ | ⭐⭐⭐⭐ | ⭐⭐⭐ | ⭐⭐⭐ | ⭐⭐⭐ |
| SQLite | ⭐⭐ | ⭐⭐ | ⭐⭐ | ⭐ | ⭐⭐ |

Choix : PostgreSQL pour sa robustesse, son support d'extensions et sa compatibilité ORM avancée.

## 6.5 Stockage objets

| Outil | Simplicité | Coût | Partage | API supportée | Note globale |
| --- | --- | --- | --- | --- | --- |
| Google Drive | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐ | ⭐⭐⭐⭐ | ⭐⭐ | ⭐⭐⭐⭐ |
| MinIO | ⭐⭐⭐ | ⭐⭐⭐ | ⭐⭐ | ⭐⭐⭐⭐ | ⭐⭐⭐ |
| Amazon S3 | ⭐⭐ | ⭐ | ⭐⭐ | ⭐⭐⭐⭐⭐ | ⭐⭐⭐ |

Choix : Google Drive pour la gratuité, la simplicité d'accès et la collaboration directe.

## 6.6 Suivi d’expériences

| Outil | Visualisation | Intégration | Versioning | Documentation | Note globale |
| --- | --- | --- | --- | --- | --- |
| MLflow + DVC | ⭐⭐⭐⭐ | ⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐ | ⭐⭐⭐⭐ |
| W&B | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐ | ⭐⭐ | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐ |

Choix : MLflow + DVC pour leur nature open-source et leur intégration avec Git/DagsHub.

## 6.7 CI/CD

| Outil | Simplicité | Intégration GitHub | Documentation | Coût | Note globale |
| --- | --- | --- | --- | --- | --- |
| GitHub Actions | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐ | ⭐⭐⭐⭐ | ⭐⭐⭐⭐ |
| GitLab CI | ⭐⭐⭐⭐ | ⭐⭐ | ⭐⭐⭐⭐ | ⭐⭐⭐ | ⭐⭐⭐ |
| Jenkins | ⭐ | ⭐⭐ | ⭐⭐ | ⭐⭐⭐⭐ | ⭐⭐ |

Choix : GitHub Actions pour l'intégration native GitHub, les templates publics et la rapidité d'exécution.

# 7. Architecture technique

## 7.1 Infrastructure

- Kubernetes (EKS AWS)
- Noeuds API/UI : 4 vCPU / 8 Go RAM
- Noeuds IA : 1 GPU / 16 Go RAM
- Services managés : PostgreSQL RDS
- Stockage objets : Google Drive

## 7.2 Réseau et interconnexion

- Débit 1 Gbps
- Ingress Nginx, HTTPS, pare-feu namespace

## 7.3 Containerisation

| Outil | Sécurité | Intégration CI | Compatibilité K8s | Licence | Note globale |
| --- | --- | --- | --- | --- | --- |
| Podman | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐ | ⭐⭐⭐⭐ | Open | ⭐⭐⭐⭐ |
| Docker | ⭐⭐⭐ | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ | Freemium | ⭐⭐⭐⭐ |

Choix : Podman pour sa nature rootless, sa compatibilité OCI, et sa meilleure sécurité par défaut.

## 7.4 Dimensionnement

- 500 requêtes API/min
- 1000 images/jour < 24h de traitement
- Utilisation cloud-first et scalable

# 8. Architecture opérationnelle

## 8.1 CI/CD

- GitHub Actions (build, test via `pytest`, deployment)
- ArgoCD ou kubectl manuel (GitOps simplifié)

## 8.2 Monitoring

- Prometheus : métriques API/IA
- Grafana : dashboards
- Evidently : dérive modèle et données

## 8.3 Sauvegarde

- Google Drive : snapshot des entrées + résultats IA
- PostgreSQL : dump quotidien (pg_dump via Airflow)

## 8.4 Maintenance

- Airflow planifie réentraînement
- Alertes seuils Prometheus → Slack/email

# 9. Vue des décisions

| ID | Sujet | Décision | Justification |
| --- | --- | --- | --- |
| D1 | UI | Streamlit | rapide, intégrable, peu de code |
| D2 | API | FastAPI | async, rapide, adapté aux ML APIs |
| D3 | Stockage objet | Google Drive | simplicité + gratuité + partage |
| D4 | Tracking | MLflow + DVC | open-source, intégré à DagsHub |
| D5 | CI/CD | GitHub Actions | YAML simple, intégré à GitHub |
| D6 | Containerisation | Podman | rootless, sécurisé, moderne |

# 10. Qualité

- **Performance** : inférence < 1s/image, API < 500 ms
- **Sécurité** : OAuth2 + firewall namespace + audit logs
- **Fiabilité** : testée via CI, tolérance via K8s
- **Scalabilité** : pods scalables, cloud storage
- **Utilisabilité** : interface Streamlit simple et ergonomique

# 11. Risques & atténuation

| Risque | Impact | Proba | Mitigation |
| --- | --- | --- | --- |
| Drift IA | Élevé | Moyen | retrain auto + Evidently |
| Latence Drive | Moyen | Faible | bufferisation Airflow, cache local |
| Charge GPU | Élevé | Moyen | autoscaling + priorisation |
| API failure | Élevé | Moyen | CI tests + fallback modes |

# 12. Conclusion et évolutions possibles

## 12.1 Résumé

Le projet fournit une architecture MLOps complète pour classifier automatiquement des produits e-commerce selon des données multimodales (texte + image), avec déploiement, supervision et scalabilité.

## 12.2 Ouvertures / axes d’amélioration

- Utilisation de GPU spot instances pour optimisation coûts.
- Déploiement multi-région pour haute disponibilité.
- Enrichissement par moteur de recherche sémantique (ex. : vecteurs Faiss)
- Version entreprise de Google Drive pour quota élevé.
- Mise en œuvre du framework ZenML pour abstraction des pipelines.

# 13. Glossaire

- **CI/CD** : Continuous Integration / Continuous Delivery
- **API** : Application Programming Interface
- **IA** : Intelligence Artificielle
- **MLOps** : Pratiques DevOps appliquées aux projets IA
- **Docker/Podman** : Conteneurs d’exécution isolés
- **GPU** : Processeur graphique, utilisé pour l'entraînement IA

# 14. Annexes

## 14.1 Diagramme C4 (Structurizr)

*En annexe figure un diagramme C4 décrivant les éléments principaux de l’architecture logique, technique et applicative selon les 4 niveaux : Context, Container, Component, Code.*

## 14.2 Critères d’évaluation

1. Proposition de projet claire
2. Documentation technique détaillée (slides et README)
3. Nettoyage des données complet
4. Versionnage des données implémenté
5. Sélection de modèle appropriée
6. Feature engineering pertinent
7. Validation du modèle correcte
8. Résultats reproductibles
9. Utilisation du contrôle de version de code
10. Pipelines CI/CD fonctionnelles
11. Infrastructure scalable
12. Outils de surveillance en place
13. Mesures de détection des dérives et biais
14. Mesures de confidentialité des données
15. Stratégie de déploiement claire
16. Plan de maintenance défini
17. Collaboration d'équipe efficace
18. Communication claire
19. Suivi d'expérience d'entraînement
20. Sécurisation de l'architecture (API)