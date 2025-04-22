import os

def get_prompt_for_theme(theme):
    if theme == "market_question":
        market_reports = [f for f in os.listdir('../../data/md/market_reports') if os.path.isfile(os.path.join('data/md/market_reports', f))]
        market_questions = [
            "Quelle est la production de tournesol en 2024 et comment a-t-elle évolué par rapport à 2023 ?",
            "Quelle région a enregistré la plus forte augmentation de la collecte de féverole ?",
            "Quel est le prix de référence du sucre ?",
            "Quelle est la répartition des volumes collectés pour les grains mouchetés en 2024 par rapport à la moyenne quinquennale 2018-2023 ?",
            "Quelle est la variation des exportations de blé tendre de l'UE par rapport à l'année précédente au 3 mars 2024 ?"
        ]

        return f"""
        Tu es un agent spécialisé dans la génération de questions pertinentes pour le finetuning d'un modèle de langage (LLM) qui servira de routeur de questions. Le domaine cible est l'agriculture, et plus précisément le thème "market_question".

        Ton objectif est de créer des questions pertinentes et variées qui couvrent divers aspects du marché agricole. Ces questions doivent être formulées de manière à aider le LLM à mieux comprendre et répondre aux interrogations liées au marché agricole.

        Voici la liste des documents disponibles qui sont en rapport avec le thème "market_question" :
        {market_reports}

        Pour t'inspirer, voici quelques exemples de questions pertinentes pour ce thème :
        {market_questions}

        Assure-toi que les questions générées sont diversifiées, couvrant différents aspects tels que les tendances du marché, les prix des produits agricoles, les prévisions de demande, les analyses concurrentielles, etc.
        Garde tes questions courtes et précises, en te concentrant sur les aspects pratiques du marché agricole.
        Tu génèrereras une vingtaine de questions.
        """

    elif theme == "policy_help":
        technical_reports = [f for f in os.listdir('../../data/md/technical_reports') if os.path.isfile(os.path.join('data/md/technical_reports', f))]
        technical_questions = [
            "Quelle est la largeur minimale requise pour une bande tampon le long d'un cours d'eau ?",
            "Quelle est la part minimale de terres arables que je dois consacrer à des éléments favorables à la biodiversité ?",
            "Suis-je concerné par les mesures de protection des eaux contre la pollution par les nitrates si mes terres sont situées en zone vulnérable ?",
            "Quelles sanctions sont prévues en cas de non-respect des limites maximales de résidus de pesticides lors des contrôles ?",
            "À partir de combien d'années une prairie temporaire devient-elle une prairie permanente selon la PAC ?"
        ]

        return f"""
        Tu es un agent spécialisé dans la génération de questions pertinentes pour le finetuning d'un modèle de langage (LLM) qui servira de routeur de questions. Le domaine cible est l'agriculture, et plus précisément le thème "policy_help".

        Ton objectif est de créer des questions pertinentes et variées qui couvrent divers aspects de la réglementation agricole. Ces questions doivent être formulées de manière à aider le LLM à mieux comprendre et répondre aux interrogations liées aux réglementations agricoles.

        Voici la liste des documents disponibles qui sont en rapport avec le thème "policy_help" :
        {technical_reports}

        Pour t'inspirer, voici quelques exemples de questions pertinentes pour ce thème :
        {technical_questions}

        Assure-toi que les questions générées sont diversifiées, couvrant différents aspects tels que les exigences réglementaires, les normes de sécurité alimentaire, les pratiques durables, les subventions agricoles, etc.
        Garde tes questions courtes et précises, en te concentrant sur les aspects pratiques de la réglementation agricole.
        Tu génèrereras une vingtaine de questions.
        """
    
    elif theme == "disease_diagnosis":
        return f"""

        Tu es un agent spécialisé dans la génération de questions pertinentes pour le finetuning d'un modèle de langage (LLM) qui servira de routeur de questions. Le domaine cible est l'agriculture, et plus précisément le thème "disease_diagnosis"
        
        Ton objectif est de créer des questions pertinentes et variées qui couvrent divers aspects du diagnostic des maladies des plantes. Ces questions doivent être formulées de manière à demander au LLM si des tomates ou des patates semblent malades.

        Pour t'inspirer, voici quelques exemples de questions pertinentes pour ce thème :
        - Comment savoir si ma tomate est malade ?
        - Comment savoir si ma patate est malade ?
        - Comment traiter les maladies des tomates ?
        - Comment traiter les maladies des patates ?
        - Quels sont les symptômes des maladies des tomates ?
        - Quels sont les symptômes des maladies des patates ?

        Garde tes questions courtes et précises, en te concentrant sur les aspects pratiques du diagnostic des maladies des plantes.
        Tu génèrereras une vingtaine de questions.
        """
    
    elif theme == "weather_management":
        return f"""

        Tu es un agent spécialisé dans la génération de questions pertinentes pour le finetuning d'un modèle de langage (LLM) qui servira de routeur de questions. Le domaine cible est l'agriculture, et plus précisément le thème "weather_management"
        
        Ton objectif est de créer des questions pertinentes et variées qui couvrent divers aspects de la gestion des conditions météorologiques. Ces questions doivent être formulées de manière à demander au LLM des questions en lien avec les conditions météorologiques.

        Pour t'inspirer, voici quelques exemples de questions pertinentes pour ce thème :
        - Dois-je récolter ma tomate aujourd'hui ou puis-je attendre la semaine prochaine ?
        - Y'aura-t-il de la grêle cette semaine ?
        - Que faire de mes patates s'il neige la semaine prochaine ?
        - Comment anticiper les conditions météorologiques pour la récolte ?

        Garde tes questions courtes et précises, en te concentrant sur les aspects pratiques de la gestion des conditions météorologiques.
        Tu génèrereras une vingtaine de questions.
        """

    elif theme == "other":
        return """

        Tu es un agent spécialisé dans la génération de questions pertinentes pour le finetuning d'un modèle de langage (LLM) qui servira de routeur de questions. Le domaine cible est l'agriculture, et plus précisément le thème "autre"
        
        Ton objectif est de créer des questions pertinentes et variées qui couvrent divers aspects de l'agriculture.

        Pour t'inspirer, voici quelques exemples de questions pertinentes pour ce thème :
        - Quelles sont les innovations technologiques récentes en matière d'agriculture de précision ?
        - Comment calculer le coût de production d'une tonne de blé dans mon exploitation ?
        - Comment mettre en place un système de vente directe efficace pour mes produits agricoles ?
        - Comment évaluer la rentabilité d'un investissement dans des panneaux solaires sur les bâtiments agricoles ?
        
        Garde tes questions courtes et précises, en te concentrant sur les aspects pratiques de l'agriculture.
        Tu génèrereras une vingtaine de questions.
        """