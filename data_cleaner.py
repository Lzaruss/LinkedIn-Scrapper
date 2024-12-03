import json
import re
from unidecode import unidecode
from geopy.geocoders import Nominatim


def load_data(file_path):
    """Carga los datos desde un archivo JSON y devuelve una lista de diccionarios."""
    try:
        with open(file_path, "r", encoding="utf-8") as file:
            data = json.load(file)
            if "persons" in data:
                return data["persons"]
            else:
                raise ValueError("El archivo JSON no contiene la clave 'persons'.")
    except Exception as e:
        print(f"Error al cargar los datos: {e}")
        return []


def clean_location(location):
    """Limpia el campo 'location' separando las tres partes de la ubicación."""
    if location:
        parts = location.split(", ")  # Separa por comas
        return {
            "city": parts[0] if len(parts) > 0 else None,
            "region": parts[1] if len(parts) > 1 else None,
            "country": parts[2] if len(parts) > 2 else None,
        }
    return {"city": None, "region": None, "country": None}


def geocode_location(location):
    """Obtiene coordenadas de una ubicación utilizando geopy."""
    geolocator = Nominatim(user_agent="location_cleaner")
    try:
        if location:
            geo_data = geolocator.geocode(location)
            if geo_data:
                return {"latitude": geo_data.latitude, "longitude": geo_data.longitude}
    except Exception as e:
        print(f"Error en la geocodificación: {e}")
    return {"latitude": None, "longitude": None}


def remove_emojis_and_symbols(text):
    """Elimina emoticonos y símbolos especiales de un texto."""
    if text:
        return re.sub(r'[\U00010000-\U0010FFFF]|[\*#@&<>\\/|]', '', text)
    return text


def clean_title(title, language="es"):
    """Limpia y procesa el campo 'title' gestionando separadores, sinónimos y idioma."""
    if title:
        title = remove_emojis_and_symbols(title)

        # Dividir por el separador | si existe
        parts = [t.strip() for t in title.split("|")]

        synonyms = {
            "es": {
                "Estudiante": ["Alumno", "Aprendiz"],
                "Universidad": ["Uni", "Facultad"],
                "Ingeniero": ["Engineer", "Eng."],
                "Desarrollador": ["Developer", "Dev"]
            },
            "en": {
                "Student": ["Learner", "Pupil"],
                "University": ["College", "Faculty"],
                "Engineer": ["Ingeniero", "Eng."],
                "Developer": ["Desarrollador", "Dev"]
            }
        }

        def replace_synonyms(text):
            for key, values in synonyms.get(language, {}).items():
                for value in values:
                    text = re.sub(rf"\b{value}\b", key, text, flags=re.IGNORECASE)
            return text

        cleaned_parts = [replace_synonyms(part) for part in parts]
        return cleaned_parts
    return []


def extract_keywords(title):
    """Extrae palabras clave de un título."""
    if title:
        keywords = re.findall(r"\b[A-Za-z0-9]+\b", title)
        return list(set(keywords))  # Elimina duplicados
    return []


def classify_title(title):
    """Clasifica el título en categorías predefinidas."""
    categories = {
        "Data Science": [
            "Data", "Machine Learning", "ETL", "Power BI", "Analytics", "Pandas", "AI", "Deep Learning", 
            "Big Data", "Analista de Datos", "Ciencia de Datos", "Inteligencia Artificial", "Análisis Predictivo"
        ],
        "Engineering": [
            "Engineer", "Desarrollador", "Developer", "Backend", "Frontend", "Software", "Fullstack", 
            "Cloud", "Arquitecto de Software", "Ingeniero", "DevOps", "Cloud Engineer"
        ],
        "Programming Languages": [
            "Python", "JavaScript", "Java", "C#", "C++", "Ruby", "PHP", "Go", "Swift", "Kotlin", 
            "TypeScript", "SQL", "Perl", "Rust", "Matlab", "Scala", "Lenguajes de Programación", 
            "Desarrollador Python", "Programador Java"
        ],
        "Cybersecurity": [
            "Cybersecurity", "Pentesting", "SOC", "Blue Team", "Red Team", "Incident Response", 
            "Threat", "SIEM", "MITRE", "Ciberseguridad", "Seguridad Informática", "Analista de Seguridad", 
            "Hacking Ético", "Ethical Hacking", "Auditor de Seguridad"
        ],
        "Marketing": [
            "SEO", "Marketing", "Content", "Social Media", "Growth", "Advertising", "Brand", 
            "Digital", "Publicidad", "Mercadeo", "Estrategia de Marca", "Marketing Digital"
        ],
        "Operations": [
            "Operations", "Supply Chain", "Logistics", "Project Management", "Process Improvement", 
            "Operaciones", "Cadena de Suministro", "Logística", "Gestión de Proyectos", "Mejora de Procesos"
        ],
        "Human Resources": [
            "HR", "Talent", "Recruitment", "People", "Payroll", "Employee", "Recursos Humanos", 
            "Gestión de Talento", "Selección", "Gestión de Personas"
        ],
        "Finance": [
            "Finance", "Financial", "Accounting", "Auditor", "Investment", "Banking", "Treasury", 
            "Finanzas", "Contabilidad", "Auditoría", "Inversiones", "Banca", "Asesor Financiero"
        ],
        "Education": [
            "Teacher", "Professor", "Educator", "Trainer", "Learning", "Instructor", "Docente", 
            "Profesor", "Educador", "Formador", "Tutor", "Catedrático", "Maestro", "Coach Educativo", 
            "Pedagogo", "Capacitación", "Entrenador de Habilidades"
        ],
        "Health": [
            "Healthcare", "Doctor", "Nurse", "Therapist", "Pharmacist", "Medical", "Salud", 
            "Médico", "Enfermero", "Terapeuta", "Farmacéutico", "Psiquiatra", "Fisioterapeuta"
        ],
        "Legal": [
            "Lawyer", "Attorney", "Legal", "Compliance", "Contract", "Abogado", "Jurídico", 
            "Cumplimiento", "Contrato", "Consultor Legal"
        ],
        "Creative": [
            "Designer", "Illustrator", "Photographer", "Videographer", "Art", "Creative", 
            "Diseñador", "Ilustrador", "Fotógrafo", "Videógrafo", "Arte", "Creativo", "Animador 3D", 
            "Diseñador UI/UX"
        ],
        "Sales": [
            "Sales", "Business Development", "Account Manager", "Customer", "Lead Generation", 
            "Ventas", "Desarrollo de Negocios", "Gestión de Cuentas", "Representante de Ventas"
        ],
        "IT Support": [
            "IT Support", "Helpdesk", "Service Desk", "Technical Support", "System Admin", 
            "Soporte IT", "Informatico", "Administrador de Sistemas", "Soporte Técnico"
        ],
        "Manufacturing": [
            "Production", "Manufacturing", "Factory", "Operations", "Quality Control", 
            "Producción", "Fábrica", "Operaciones", "Control de Calidad", "Gestión de Producción"
        ],
        "Consulting": [
            "Consultant", "Advisory", "Strategy", "Business Analysis", "Consultoría", 
            "Estrategia", "Análisis de Negocios", "Asesor"
        ],
        "Freelance/Independent": [
            "Freelance", "Self-employed", "Independent", "Autónomo", "Independiente", 
            "Consultor Independiente"
        ],
        "Customer Service": [
            "Customer Service", "Support Specialist", "Atención al Cliente", 
            "Especialista en Soporte", "Soporte al Cliente"
        ],
        "Public Sector": [
            "Public Sector", "Government", "Nonprofit", "Sector Público", 
            "Gobierno", "Organización sin Fines de Lucro", "ONG"
        ],
        "Entrepreneurship": [
            "Entrepreneur", "Startup", "Founder", "Co-Founder", "Emprendimiento", 
            "Empresario", "Startup", "Fundador"
        ],
        "Agriculture": [
            "Agriculture", "Farming", "Agronomist", "Agricultura", "Granja", "Agrónomo"
        ],
        "Other": [] 
    }

    if title:
        for category, keywords in categories.items():
            if any(keyword.lower() in title.lower() for keyword in keywords):
                return category
    return "Other"


def normalize_text(text):
    """Normaliza un texto eliminando tildes y convirtiéndolo a minúsculas."""
    if text:
        return unidecode(text).lower()
    return text


def process_data(data, language="es"):
    """Procesa y limpia los datos cargados."""
    for person in data:

        person["cleaned_location"] = clean_location(person.get("location"))

        # Agregar coordenadas a la ubicación
        geo_data = geocode_location(person.get("location"))
        person["location_coordinates"] = geo_data

        person["cleaned_title"] = clean_title(person.get("title"), language=language)

        person["title_category"] = classify_title(person.get("title"))

        person["title_keywords"] = extract_keywords(person.get("title"))

    return data


def main():
    file_path = "data_folder/connections_links.json"

    data = load_data(file_path)
    if not data:
        print("El archivo JSON no contiene datos válidos.")
        return

    cleaned_data = process_data(data)

    # Opcional: Guardar los datos procesados en un archivo nuevo
    output_path = "data_folder/cleaned_connections_links.json"
    try:
        with open(output_path, "w", encoding="utf-8") as file:
            json.dump({"persons": cleaned_data}, file, ensure_ascii=False, indent=4)
        print(f"Datos limpios guardados en {output_path}")
    except Exception as e:
        print(f"Error al guardar los datos limpios: {e}")


if __name__ == "__main__":
    main()
