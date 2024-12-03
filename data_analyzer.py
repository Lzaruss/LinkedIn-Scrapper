import json
from collections import Counter, defaultdict
import re
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px

def load_cleaned_data(file_path):
    """Carga los datos limpios desde un archivo JSON."""
    try:
        with open(file_path, "r", encoding="utf-8") as file:
            data = json.load(file)
            if "persons" in data:
                return data["persons"]
            else:
                raise ValueError("El archivo JSON no contiene la clave 'persons'.")
    except Exception as e:
        print(f"Error al cargar los datos limpios: {e}")
        return []

def count_occurrences(data, key):
    """Cuenta la frecuencia de valores en una clave específica."""
    counts = Counter()
    for person in data:
        value = person.get(key)
        if isinstance(value, dict):
            counts.update(value.values())
        elif isinstance(value, list):
            counts.update(value)
        elif value:
            counts[value] += 1
    return counts

def analyze_most_frequent_titles(data, top_n=10):
    """Identifica las palabras clave más frecuentes en los títulos."""
    keyword_counts = Counter()
    for person in data:
        titles = person.get("cleaned_title", [])
        for title in titles:
            words = re.findall(r'\b\w+\b', title.lower())
            keyword_counts.update(words)
    stopwords = {"and", "of", "in", "on", "at", "to", "for", "with", "a", "an", "the", "de", "en", "y", "el", "la", "los", "las"}
    filtered_keywords = {word: count for word, count in keyword_counts.items() if word not in stopwords}
    return Counter(filtered_keywords).most_common(top_n)

def analyze_province_distribution(data):
    """Analiza la distribución por provincias (España) y regiones (resto del mundo)."""
    province_mapping = {
        "Madrid": "Madrid",
        "Community of Madrid": "Madrid",
        "Barcelona": "Barcelona",
        "Catalonia": "Barcelona",
    }
    province_counts = defaultdict(int)
    for person in data:
        location = person.get("cleaned_location", {}).get("region")
        if location:
            province = province_mapping.get(location, location)
            province_counts[province] += 1
    total = len(data)
    return {province: round((count / total) * 100, 2) for province, count in province_counts.items()}

def analyze_country_percentage(data):
    """Calcula el porcentaje de personas por país."""
    country_counts = Counter()
    for person in data:
        location = person.get("cleaned_location", {}).get("country")
        if location:
            country_counts[location] += 1
    total = len(data)
    return {country: round((count / total) * 100, 2) for country, count in country_counts.items()}

def calculate_completion_percentage(data, key):
    """Calcula el porcentaje de personas que tienen un dato específico."""
    total = len(data)
    if total == 0:
        return 0
    count = sum(1 for person in data if person.get(key))
    return round((count / total) * 100, 2)

def plot_province_distribution(province_distribution):
    """Crea un gráfico de barras para la distribución por provincias o regiones."""
    plt.figure(figsize=(10, 6))
    provinces = list(province_distribution.keys())
    percentages = list(province_distribution.values())
    sns.barplot(x=percentages, y=provinces, palette="viridis")
    plt.title("Distribución por Provincias o Regiones", fontsize=16)
    plt.xlabel("Porcentaje (%)")
    plt.ylabel("Provincia o Región")
    plt.show()

def plot_country_percentage(country_percentage):
    """Crea un gráfico de pastel para la distribución por países."""
    countries = list(country_percentage.keys())
    percentages = list(country_percentage.values())
    fig = px.pie(
        names=countries,
        values=percentages,
        title="Porcentaje de Personas por País",
        hole=0.4,
    )
    fig.show()

def plot_completion_percentage(email_percentage, phone_percentage, website_percentage):
    """Crea un gráfico de barras para el porcentaje de datos completados."""
    categories = ["Correo", "Teléfono", "Website"]
    percentages = [email_percentage, phone_percentage, website_percentage]
    plt.figure(figsize=(8, 5))
    sns.barplot(x=categories, y=percentages, palette="coolwarm")
    plt.title("Porcentaje de Datos Completados", fontsize=16)
    plt.ylabel("Porcentaje (%)")
    plt.ylim(0, 100)
    plt.show()

def main():
    file_path = "data_folder/cleaned_connections_links.json"

    data = load_cleaned_data(file_path)
    if not data:
        print("El archivo JSON no contiene datos válidos.")
        return

    print(len(data))
    
    # Análisis por provincias/regiones
    province_distribution = analyze_province_distribution(data)
    print("\nDistribución por provincias o regiones (%):")
    for province, percentage in province_distribution.items():
        print(f"{province}: {percentage}%")
    #plot_province_distribution(province_distribution)

    # Porcentaje por países
    country_percentage = analyze_country_percentage(data)
    print("\nPorcentaje de personas por país:")
    for country, percentage in country_percentage.items():
        print(f"{country}: {percentage}%")
    #plot_country_percentage(country_percentage)

    # Porcentaje de datos completados
    email_percentage = calculate_completion_percentage(data, "email")
    phone_percentage = calculate_completion_percentage(data, "phone")
    website_percentage = calculate_completion_percentage(data, "website")
    print("\nPorcentaje de datos completados:")
    print(f"Correo electrónico: {email_percentage}%")
    print(f"Teléfono: {phone_percentage}%")
    print(f"Website: {website_percentage}%")
    #plot_completion_percentage(email_percentage, phone_percentage, website_percentage)

if __name__ == "__main__":
    main()
