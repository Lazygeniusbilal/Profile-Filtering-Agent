# In this file we will mention everything that will remain constant throughout the whole project so we can minimize defining it again and again in the project
from pathlib import Path

# titles we want to exclude from our dataset
title_to_remove = [
        "consultant", "sales", "account", "b2b", "marketing", "business", "development",
        "designer", "architect", "engineer", "engineering", "scientist", "professor",
        "finance", "financing", "hr", "recruitment", "talent", "training", "learning",
        "sales", "business development", "client", "revenue", "acquisition", "customer relationship",
        "consulting", "Advisory", "financial services", "audit", " finances", "health and safety", "associate",
        "pipeline", "quota", "deals", "increase revenue", "target"
    ]

# words that we will use to exclude rows if they are present in summary or jobDescription
profile_elimination_words= [
        "sales", "business development", "client", "revenue", "acquisition", "customer relationship",
        "consulting", "Advisory", "financial services", "audit", " finances", "health and safety", "associate",
        "pipeline", "quota", "deals", "increase revenue", "target"
    ]

# countries we will select by default 
eu_countries = [
        "Austria", "Belgium", "Bulgaria", "Croatia", "Cyprus", "Czech Republic",
        "Denmark", "Estonia", "Finland", "France", "Germany", "Greece", "Hungary",
        "Ireland", "Italy", "Latvia", "Lithuania", "Luxembourg", "Malta",
        "Netherlands", "Poland", "Portugal", "Romania", "Slovakia", "Slovenia",
        "Spain", "Sweden", "Switzerland", "United Kingdom"
    ]

# Valid county names 
valid_countries = [
    "afghanistan", "albania", "algeria", "andorra", "angola", "antigua and barbuda",
    "argentina", "armenia", "australia", "austria", "azerbaijan", "bahamas", "bahrain", 
    "bangladesh", "barbados", "belarus", "belgium", "belize", "benin", "bhutan", "bolivia",
    "bosnia and herzegovina", "botswana", "brazil", "brunei", "bulgaria", "burkina faso",
    "burundi", "cabo verde", "cambodia", "cameroon", "canada", "central african republic", 
    "chad", "chile", "china", "colombia", "comoros", "congo", "costa rica", "croatia", "cuba",
    "cyprus", "czech republic", "denmark", "djibouti", "dominica", "dominican republic", "ecuador",
    "egypt", "el salvador", "equatorial guinea", "eritrea", "estonia", "eswatini", "ethiopia", "fiji", 
    "finland", "france", "gabon", "gambia", "georgia", "germany", "ghana", "greece", "grenada", "guatemala", 
    "guinea", "guinea-bissau", "guyana", "haiti", "honduras", "hungary", "iceland", "india", "indonesia", "iran",
    "iraq", "ireland", "israel", "italy", "jamaica", "japan", "jordan", "kazakhstan", "kenya", "kiribati", "korea", 
    "kuwait", "kyrgyzstan", "laos", "latvia", "lebanon", "lesotho", "liberia", "libya", "liechtenstein", "lithuania", 
    "luxembourg", "madagascar", "malawi", "malaysia", "maldives", "mali", "malta", "marshall islands", "mauritania", 
    "mauritius", "mexico", "micronesia", "moldova", "monaco", "mongolia", "montenegro", "morocco", "mozambique", "myanmar",
    "namibia", "nauru", "nepal", "netherlands", "new zealand", "nicaragua", "niger", "nigeria", "north macedonia", "norway",
    "oman", "pakistan", "palau", "palestine", "panama", "papua new guinea", "paraguay", "peru", "philippines", "poland", "portugal",
    "qatar", "romania", "russia", "rwanda", "saint kitts and nevis", "saint lucia", "saint vincent and the grenadines", 
    "samoa", "san marino", "sao tome and principe", "saudi arabia", "senegal", "serbia", "seychelles", "sierra leone", "singapore", 
    "slovakia", "slovenia", "solomon islands", "somalia", "south africa", "south sudan", "spain", "sri lanka", "sudan", "suriname",
    "sweden", "switzerland", "syria", "taiwan", "tajikistan", "tanzania", "thailand", "timor-leste", "togo", "tonga", 
    "trinidad and tobago", "tunisia", "turkey", "turkmenistan", "tuvalu", "uganda", "ukraine", "united arab emirates", 
    "united kingdom", "united states", "uruguay", "uzbekistan", "vanuatu", "vatican city", "venezuela", "vietnam", "yemen",
    "zambia", "zimbabwe"
]

# seniority check from each category
# 6. Seniority filter
cat_a = ["director", "head", "vp", "senior", "manager", "lead", "chief"]
cat_b = ["director", "head", "vp", "senior", "manager", "chief"]
cat_c = ["director", "head", "vp", "chief"]

# list of columns for elimination of keywords
columns_list= ['summary', 'titleDescription']

# paths for the datasets
companies_to_remove= Path('data/companies to remove.xlsx')
companies_a= Path('data/companies_a.csv')
companies_b= Path('data/companies_b.csv')

# List of generic words to exclude from keyword extraction
GENERIC_WORDS = {
    "business", "organization", "organizational", "culture", "capabilities",
    "process", "system", "management", "operations", "building"
}