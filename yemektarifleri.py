import requests
from deep_translator import GoogleTranslator

print(" 🍳 Yemek Tarifleri Uygulamasına Hoşgeldiniz 🍳 ")

while True:
    
    aranan_yemek = input("Hangi yemek tarifini aramak istiyorsun? (Yemeği ingilizce yazınız veya Yemek önerisi için boş bırakın): ").strip()
    
    
    while True:
        secim = input("Türkçe mi İngilizce mi açıklasın? Türkçe = 1, İngilizce = 2: ")
        print("Lütfen Bekleyiniz! ")
        if secim == "1":
            translator = GoogleTranslator(source='en', target='tr')
            break
        elif secim == "2":
            translator = None
            break
        else:
            print("Hatalı seçim! Lütfen 1 veya 2 girin.")

    
    if aranan_yemek.lower() in ["", "öneri"]:
        url = "https://www.themealdb.com/api/json/v1/1/random.php"
        parametreler = None
    else:
        url = "https://www.themealdb.com/api/json/v1/1/search.php"
        parametreler = {'s': aranan_yemek}

   
    try:
        response = requests.get(url, params=parametreler)
        if response.status_code == 200:
            data = response.json()
            if data['meals']:
                tarif = data['meals'][0]

                
                metinler = [
                    tarif['strMeal'],
                    tarif['strCategory'],
                    tarif['strArea'],
                    tarif['strInstructions']
                ]
                for i in range(1, 21):
                    ing = tarif[f'strIngredient{i}']
                    meas = tarif[f'strMeasure{i}']
                    if ing and ing.strip():
                        metinler.append(f"{ing} : {meas}")

                cevrilmis = translator.translate_batch(metinler) if translator else metinler

                
                print("\n🍽 Tarif Bilgileri 🍽")
                print(f"Adı: {cevrilmis[0]}")
                print(f"Kategorisi: {cevrilmis[1]}")
                print(f"Mutfak Türü: {cevrilmis[2]}")
                print(f"Tarif Linki: {tarif['strYoutube']}")
                print(f"Yemek Resmi: {tarif['strMealThumb']}\n")
                print("🧂 Malzemeler:")
                for malzeme in cevrilmis[4:]:
                    print(f"- {malzeme}")
                print("\n📖 Tarif Adımları:")
                print(cevrilmis[3])
            else:
                print("Maalesef tarif bulunamadı.")
        else:
            print("Hata! Sunucuya ulaşılamadı.")
    except requests.exceptions.RequestException as e:
        print(f"Bağlantı Hatası: {e}")

    
    tekrar = input("\nBaşka tarif görmek ister misin? (Evet = e / Hayır = h): ").strip().lower()
    if tekrar != "e":
        print("Programdan çıkılıyor.")
        break

