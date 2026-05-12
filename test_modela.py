import google.generativeai as genai

# Ovdje pod navodnike stavi svoj pravi API ključ
MOJ_KLJUC = "AIzaSyB5H5Q-yZ2R1jO6JPaw9023S6TX8j3I3ik"

genai.configure(api_key=MOJ_KLJUC)

print("Spajam se na Google servere...")
print("Dostupni modeli za tvoj ključ su:")
print("-" * 30)

try:
    for m in genai.list_models():
        if 'generateContent' in m.supported_generation_methods:
            print(m.name)
    print("-" * 30)
except Exception as e:
    print("❌ Greška prilikom spajanja:", e)