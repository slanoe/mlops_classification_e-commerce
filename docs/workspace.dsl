workspace "Rakuten Product Categorization System" {
    model {
        vendeur = person "Vendeur" {
            tags "Utilisateur"
            description "Ajoute des produits, valide ou modifie la catégorie proposée."
        }
        administrateur = person "Administrateur" {
            tags "Utilisateur"
            description "Supervise, corrige les catégories, accède à des fonctions avancées de monitoring."
        }

        rakutenSystem = softwareSystem "Système de catégorisation de produits Rakuten" {
            interfaceUtilisateur = container "Interface utilisateur" "Application web pour l'interaction utilisateur (authentification, ajout/validation produit, visualisation, feedback)" "Streamlit" {
                tags "WebApp"
                composantAuthentification = component "Interface d'authentification" "Gère l'authentification des utilisateurs" {
                    tags "Composant"
                }
                composantAjoutProduit = component "Interface d'ajout de produit" "Gère l'ajout de produits (texte + image)" {
                    tags "Composant"
                }
                composantVisualisation = component "Interface de catégorisation" "Affiche la catégorie prédite, permet la validation ou correction, collecte le feedback utilisateur" {
                    tags "Composant"
                }
            }
            apiBackend = container "API Backend" "API REST pour la gestion des utilisateurs, produits, logs et communication avec les autres services" "FastAPI" {
                tags "API"
                composantGestionRequetes = component "Composant de gestion des requêtes" "Gère les requêtes d'authentification, d'ajout/modification de produits, de prédiction de catégories" {
                    tags "Composant"
                }
                composantGestionLogs = component "Composant de gestion des logs" "Centralise les logs applicatifs et les événements pour la traçabilité et l'audit" {
                    tags "Composant"
                }
            }
            servicePrediction = container "Service de prédiction" "Service de prédiction déployé avec BentoML, utilisant TensorFlow/Keras" "BentoML, TensorFlow/Keras" {
                tags "IA"
                composantReceptionDonnees = component "Composant de réception des données" "Reçoit les données de produits (texte, image)" {
                    tags "Composant"
                }
                composantPrediction = component "Composant de prédiction" "Prédit les catégories à partir des données multimodales" {
                    tags "Composant"
                }
                composantRetourResultats = component "Composant de retour des résultats" "Retourne les catégories prédites et les scores de confiance" {
                    tags "Composant"
                }
            }
            pipelineML = container "Pipeline ML et versioning" "Pipeline d'entraînement, validation, détection de dérive, versioning (MLflow, DVC, Airflow)" "MLflow, DVC, Airflow" {
                tags "Pipeline"
                composantCollectePredictions = component "Composant de collecte des prédictions" "Collecte les prédictions et corrections manuelles pour l'entraînement et la détection de dérive" {
                    tags "Composant"
                }
                composantReentrainement = component "Composant de réentraînement" "Réentraîne les modèles à partir des nouvelles données" "Scikit-Learn, Keras" {
                    tags "Composant"
                }
                composantGestionVersioning = component "Composant de gestion du versioning" "Versionne les modèles et les données d'entraînement (MLflow, DVC)" {
                    tags "Composant"
                }
            }
            monitoringAlerting = container "Monitoring & alerting" "Surveillance, détection de dérive, alerting (Evidently, Prometheus, Grafana)" "Evidently, Prometheus, Grafana" {
                tags "Monitoring"
                composantCollecteMetriques = component "Composant de collecte des métriques" "Collecte les métriques de performance et d'usage" {
                    tags "Composant"
                }
                composantDetectionDerives = component "Composant de détection des dérives" "Détecte les dérives de données et de concept" {
                    tags "Composant"
                }
                composantAlerting = component "Composant d'alerting" "Alerte en cas de dérive détectée ou d'incident" {
                    tags "Composant"
                }
            }
            baseDonnees = container "Base de données" "Stockage des produits, utilisateurs, logs, feedback, images (PostgreSQL, stockage objet)" "PostgreSQL, stockage objet" {
                tags "BDD"
            }
            stockageExterne = container "Stockage externe" "Stockage des modèles, datasets, backups (Google Drive, S3...)" "Google Drive" {
                tags "Stockage"
            }
        }

        // Relations utilisateurs
        vendeur -> interfaceUtilisateur "Ajoute un produit, valide ou modifie la catégorie, donne un feedback"
        administrateur -> interfaceUtilisateur "Supervise, corrige les catégories, accède au monitoring"

        // Flux principaux
        interfaceUtilisateur -> apiBackend "HTTPS, JSON, REST API"
        apiBackend -> servicePrediction "HTTPS, JSON, REST API"
        apiBackend -> baseDonnees "PostgreSQL, SQL, stockage objet"
        apiBackend -> monitoringAlerting "Envoie des métriques d'usage et feedback utilisateur"
        servicePrediction -> pipelineML "HTTPS, HDF5/CSV, REST API"
        pipelineML -> monitoringAlerting "HTTPS, JSON, REST API"
        pipelineML -> stockageExterne "Synchronise modèles et datasets (Google Drive API)"
        baseDonnees -> pipelineML "Fournit données pour l'entraînement et la détection de dérive"
        pipelineML -> baseDonnees "Enregistre les corrections et feedbacks"
        monitoringAlerting -> apiBackend "Alerte, notifications"
        monitoringAlerting -> interfaceUtilisateur "Affiche alertes ou feedback qualité"
        interfaceUtilisateur -> monitoringAlerting "Remonte feedback utilisateur"

        // Flux internes
        composantAuthentification -> composantAjoutProduit "Authentification"
        composantAjoutProduit -> composantVisualisation "Ajout de produit"
        composantGestionRequetes -> interfaceUtilisateur "Gestion des requêtes"
        composantGestionRequetes -> servicePrediction "Gestion des requêtes"
        composantGestionLogs -> baseDonnees "Stocke les logs"
        composantReceptionDonnees -> composantPrediction "Réception des données"
        composantPrediction -> composantRetourResultats "Prédiction des catégories"
        composantCollectePredictions -> composantDetectionDerives "Collecte des prédictions"
        composantDetectionDerives -> composantReentrainement "Détection de dérive"
        composantCollecteMetriques -> composantDetectionDerives "Collecte des métriques"
        composantDetectionDerives -> composantAlerting "Détection des dérives"
        composantGestionVersioning -> stockageExterne "Synchronise modèles et datasets"

    }

    views {
        systemContext rakutenSystem {
            include *
        }

        container rakutenSystem {
            include *
        }

        component interfaceUtilisateur {
            include *
            autoLayout
        }

        component apiBackend {
            include *
            autoLayout
        }

        component servicePrediction {
            include *
            autoLayout
        }

        component pipelineML {
            include *
            autoLayout
        }

        component monitoringAlerting {
            include *
            autoLayout
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
                shape "Hexagon"
                background "#C25704"
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
