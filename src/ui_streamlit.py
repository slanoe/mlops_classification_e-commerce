import streamlit as st
import requests
import json

st.title("Catégorisation de produits e-commerce")

# Saisie de la description
text = st.text_area("Description du produit")

# Variables de session pour stocker la prédiction et la description
if "predicted_category" not in st.session_state:
    st.session_state.predicted_category = None
if "description" not in st.session_state:
    st.session_state.description = ""

# Étape 1 : Prédire la catégorie
if st.button("Prédire la catégorie"):
    if text:
        response = requests.post(
            "http://fastapi:8000/predict",
            json={"text": text}
        )
        if response.status_code == 200:
            category = response.json()["category"]
            st.session_state.predicted_category = category
            st.session_state.description = text
            st.success(f"Catégorie prédite : {category}")
        else:
            st.error("Erreur lors de la prédiction.")
    else:
        st.warning("Veuillez entrer une description.")

# Étape 2 : Validation ou modification de la catégorie
if st.session_state.predicted_category:
    st.markdown("---")
    st.write(f"Catégorie proposée : {st.session_state.predicted_category}")

    # Charger la liste des catégories depuis l'API ou un fichier local
    # Ici, on suppose que le mapper est accessible en local
    try:
        with open("models/mapper.json", "r") as f:
            mapper = json.load(f)
        categories = list(mapper.values())
        cat_to_code = {v: k for k, v in mapper.items()}
    except Exception:
        categories = []
        cat_to_code = {}

    # Sélection de la catégorie (prédite par défaut)
    default_cat = mapper.get(str(st.session_state.predicted_category), str(st.session_state.predicted_category))
    selected_cat = st.selectbox(
        "Sélectionnez la catégorie à enregistrer",
        options=categories if categories else [str(st.session_state.predicted_category)],
        index=categories.index(default_cat) if default_cat in categories else 0
    )

    # Ajout du produit
    if st.button("Ajouter le produit"):
        # On récupère le code de la catégorie sélectionnée
        cat_code = cat_to_code[selected_cat] if selected_cat in cat_to_code else st.session_state.predicted_category
        response = requests.post(
            "http://fastapi:8000/add_product",
            json={
                "text": st.session_state.description,
                "category": selected_cat
            }
        )
        if response.status_code == 200:
            st.success(f"Produit ajouté avec catégorie : {selected_cat}")
            # Reset pour un nouveau workflow
            st.session_state.predicted_category = None
            st.session_state.description = ""
        else:
            st.error("Erreur lors de l'ajout du produit.")
