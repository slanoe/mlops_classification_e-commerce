workspace {

    model {
        user = person "Client Rakuten" {
            description "Client final du site Rakuten"
            tags "Utilisateur"
        }

        admin = person "Admin / MLOps" {
            description "Administrateur et équipe Data/DevOps"
            tags "Utilisateur"
        }

        rakutenSystem = softwareSystem "Système de classification Rakuten" {
            description "Plateforme MLOps de classification automatique de produits via données textuelles et images."

            webApp = container "Application Web" {
                description "Interface utilisateur (Streamlit) pour recherche, recommandations, visualisation, monitoring"
                technology "Streamlit"
                tags "WebApp"
            }

            api = container "API FastAPI" {
                description "API REST orchestrant les traitements (prédiction, ajout, requêtage)"
                technology "Python (FastAPI)"
                tags "API"

                classifier = component "Contrôleur de classification" {
                    description "Gère la logique de prédiction"
                    technology "Python"
                    tags "Composant"
                }

                modelWrapper = component "Model Wrapper" {
                    description "Appelle le modèle Keras pour effectuer la classification"
                    technology "Keras"
                    tags "Composant"
                }
            }

            mlModel = container "Modèle IA" {
                description "Modèle de classification (Keras + BentoML) entraîné sur données multimodales"
                technology "Keras + BentoML"
                tags "IA"
            }

            database = container "Base de Données PostgreSQL" {
                description "Stocke les produits, les prédictions et les logs"
                technology "PostgreSQL"
                tags "BDD"
            }

            storage = container "Stockage d'images" {
                description "Contient les images des produits (Google Drive intégré au pipeline)"
                technology "Google Drive"
                tags "Stockage"
            }

            monitoring = container "Monitoring & Supervision" {
                description "Composants de surveillance (Prometheus, Grafana, Evidently)"
                technology "Prometheus, Grafana, Evidently"
                tags "Monitoring"
            }

            pipeline = container "Pipeline MLOps" {
                description "Orchestration via Airflow, ZenML pour ingestion, entraînement, déploiement"
                technology "Airflow + ZenML"
                tags "Pipeline"
            }

            // Relations de niveau conteneur
            user -> webApp "Recherche, consulte, reçoit des recommandations"
            admin -> webApp "Ajoute des produits, supervise, déclenche réentraînements"
            admin -> pipeline "Planifie les entraînements"

            webApp -> api "Appelle l'API"
            api -> mlModel "Requête de prédiction"
            api -> database "Lit / écrit des données"
            api -> storage "Accède aux images"

            mlModel -> monitoring "Envoie des métriques"
            pipeline -> mlModel "Réentraîne le modèle"
            pipeline -> database "Utilise les jeux de données"
            pipeline -> monitoring "Surveille les performances"

            // Relations entre composants internes
            classifier -> modelWrapper "Appelle le modèle IA"
            modelWrapper -> mlModel "Requête de prédiction"
        }
    }

    views {

        systemContext rakutenSystem {
            include *
            autolayout lr
            title "Contexte Système Rakuten"
        }

        container rakutenSystem {
            include *
            autolayout lr
            title "Vue Conteneurs - Système Rakuten"
        }

        component api {
            include *
            autolayout lr
            title "Vue Composants - API FastAPI"
        }

        styles {
            element "Utilisateur" {
                shape "Person"
                background "#6d9eeb"
                color "#ffffff"
            }

            element "WebApp" {
                shape "WebBrowser"
                background "#1155cc"
                color "#ffffff"
            }

            element "API" {
                shape "Hexagon"
                background "#3c78d8"
                color "#ffffff"
            }

            element "Composant" {
                shape "Component"
                background "#cfe2f3"
                color "#000000"
            }

            element "IA" {
                shape "RoundedBox"
                background "#d9ead3"
                color "#000000"
            }

            element "BDD" {
                shape "Cylinder"
                background "#f9cb9c"
                color "#000000"
            }

            element "Monitoring" {
                shape "Pipe"
                background "#f4cccc"
                color "#000000"
            }

            element "Pipeline" {
                shape "Box"
                background "#d0e0e3"
                color "#000000"
            }

            element "Stockage" {
                shape "Folder"
                background "#f3f3f3"
                color "#333333"
            }
        }
    }
}
