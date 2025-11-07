import requests
import deep_translator
from deep_translator import GoogleTranslator


def get_meal(query):
    """
    TheMealDB API üzerinden yemek tarifini getirir.
    Eğer kullanıcı boş bırakırsa rastgele bir tarif döner.
    """
    if query.lower() in ["", "öneri"]:
        url = "https://www.themealdb.com/api/json/v1/1/random.php"
        params = None
    else:
        url = "https://www.themealdb.com/api/json/v1/1/search.php"
        params = {'s': query}

    try:
        response = requests.get(url, params=params)
        response.raise_for_status()
        data = response.json()
        if data['meals']:
            return data['meals'][0]
        else:
            print("❌ Maalesef tarif bulunamadı.")
            return None
    except requests.exceptions.RequestException as e:
        print(f"⚠️ Bağlantı Hatası: {e}")
        return None


def translate_texts(texts, lang):
    """
    Metinleri belirtilen dile çevirir.
    lang = 'tr' → Türkçe, 'en' → İngilizce
    """
    if lang == 'tr':
        translator = GoogleTranslator(source='en', target='tr')
        return translator.translate_batch(texts)
    else:
        return texts


def show_recipe(recipe, texts):
    """
    Tarif bilgilerini ekrana yazdırır.
    """
    print("\n🍽 Tarif Bilgileri 🍽")
    print(f"Adı: {texts[0]}")
    print(f"Kategorisi: {texts[1]}")
    print(f"Mutfak Türü: {texts[2]}")
    print(f"Tarif Linki: {recipe['strYoutube']}")
    print(f"Yemek Resmi: {recipe['strMealThumb']}\n")

    print("🧂 Malzemeler:")
    for item in texts[4:]:
        print(f"- {item}")

    print("\n📖 Tarif Adımları:")
    print(texts[3])


def main():
    """
    Kullanıcıdan giriş alır, tarifleri getirir, çeviri seçeneğine göre gösterir.
    """
    print("🍳 Yemek Tarifleri Uygulamasına Hoşgeldiniz 🍳")

    while True:
        query = input("\nHangi yemek tarifini aramak istiyorsun? (Yemeği İngilizce yaz veya öneri için boşluk bırak): ").strip()

        while True:
            lang_choice = input("Türkçe mi İngilizce mi açıklasın? (Türkçe = 1, İngilizce = 2): ")
            if lang_choice in ["1", "2"]:
                lang = 'tr' if lang_choice == "1" else 'en'
                print("Lütfen Bekleyiniz...")
                break
            else:
                print("❗ Hatalı seçim! Lütfen 1 veya 2 girin.")

        recipe = get_meal(query)
        if recipe:
            # Çevrilecek metinler
            texts = [
                recipe['strMeal'],
                recipe['strCategory'],
                recipe['strArea'],
                recipe['strInstructions']
            ]
            # Malzemeleri listele
            for i in range(1, 21):
                ing = recipe[f'strIngredient{i}']
                meas = recipe[f'strMeasure{i}']
                if ing and ing.strip():
                    texts.append(f"{ing} : {meas}")

            translated = translate_texts(texts, lang)
            show_recipe(recipe, translated)

        again = input("\nBaşka tarif görmek ister misin? (Evet = e / Hayır = h): ").strip().lower()
        if again != "e":
            print("👋 Programdan çıkılıyor.")
            break


if __name__ == "__main__":
    main()

