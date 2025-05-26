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

        rakutenSystem = softwareSystem "Catégorisation de produits Rakuten" {
            group "Application" {
            interfaceUtilisateur = container "Interface utilisateur" "Application web pour l'interaction utilisateur (authentification, ajout/validation produit et visualisation)" "Streamlit" {
                tags "WebApp"
            }
            apiBackend = container "API Backend" "API REST pour la gestion des utilisateurs, produits, logs et communication avec les autres services" "FastAPI" {
                tags "API"
            }
            servicePrediction = container "Modèle ML de catégorisation" "Service de prédiction déployé avec BentoML" "BentoML, TensorFlow/Keras" {
                tags "IA"
            }
            baseDonnees = container "Base de données application" "Stockage des produits, utilisateurs, logs, images de l'application" "PostgreSQL, stockage objet" {
                tags "BDD"
            }
            }
            pipelineML = container "ML Workflow" "Pipeline d'entraînement, validation, versioning des données et des modèles" "MLflow, DVC, Airflow" {
                tags "WebApp"
            }
            stockageExterne = container "Base de données ML" "Stockage des données d'entrainement" "Google Drive" {
                tags "BDD"
            }
        }

        // Relations utilisateurs
        vendeur -> interfaceUtilisateur "Ajoute un produit, valide ou modifie la catégorie"
        administrateur -> interfaceUtilisateur "Corrige les catégories"
        administrateur -> pipelineML "Supervise les pipelines MLOps"

        // Flux principaux
        interfaceUtilisateur -> apiBackend "Envoie les informations du produit renseignées par l'utilisateur"
        apiBackend -> interfaceUtilisateur "Envoie la catégorisation du produit"
        apiBackend -> servicePrediction "Demande la catégorisation d'un produit"
        servicePrediction -> apiBackend "Envoie la catégorisation du produit"
        apiBackend -> baseDonnees "Stocke les informations et la catégorie des produits de l'application"
        pipelineML -> servicePrediction "Déploit le modèle ML de catégorisation"
        pipelineML -> stockageExterne "Gère en configuration les données d'entrainement"

    }

    views {
        systemContext rakutenSystem {
            include *
        }

        container rakutenSystem {
            include *
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
