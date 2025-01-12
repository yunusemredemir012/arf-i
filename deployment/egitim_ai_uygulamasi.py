
from flask import Flask, request, jsonify
import random

app = Flask(__name__)

# Basit bir soru bankası (örnek veriler)
soru_bankasi = [
    {"id": 1, "ders": "Matematik", "soru": "2 + 2 kaç eder?", "cevap": "4"},
    {"id": 2, "ders": "Fen Bilgisi", "soru": "Su hangi bileşikle temsil edilir?", "cevap": "H2O"},
    {"id": 3, "ders": "Tarih", "soru": "Cumhuriyet hangi yılda ilan edildi?", "cevap": "1923"},
    {"id": 4, "ders": "Coğrafya", "soru": "Dünyanın en uzun nehri hangisidir?", "cevap": "Nil"}
]

# Kullanıcıları kaydetmek için basit bir veri yapısı
kullanicilar = []

# Kullanıcı kaydet
@app.route('/kullanici_kayit', methods=['POST'])
def kullanici_kayit():
    veri = request.get_json()
    kullanici_adi = veri.get('kullanici_adi')
    email = veri.get('email')

    if not kullanici_adi or not email:
        return jsonify({"mesaj": "Kullanıcı adı ve email zorunludur."}), 400

    yeni_kullanici = {"id": len(kullanicilar) + 1, "kullanici_adi": kullanici_adi, "email": email}
    kullanicilar.append(yeni_kullanici)

    return jsonify({"mesaj": "Kullanıcı başarıyla kaydedildi.", "kullanici": yeni_kullanici})

# Tüm kullanıcıları listele
@app.route('/kullanicilar', methods=['GET'])
def tum_kullanicilar():
    return jsonify(kullanicilar)

# Kullanıcının çalışma istatistiklerini kaydet
calisma_istatistikleri = []

@app.route('/istatistik_kaydet', methods=['POST'])
def istatistik_kaydet():
    veri = request.get_json()
    kullanici_id = veri.get('kullanici_id')
    dogru_sayisi = veri.get('dogru_sayisi')
    yanlis_sayisi = veri.get('yanlis_sayisi')

    if not kullanici_id or dogru_sayisi is None or yanlis_sayisi is None:
        return jsonify({"mesaj": "Eksik bilgi gönderildi."}), 400

    yeni_istatistik = {
        "kullanici_id": kullanici_id,
        "dogru_sayisi": dogru_sayisi,
        "yanlis_sayisi": yanlis_sayisi
    }
    calisma_istatistikleri.append(yeni_istatistik)

    return jsonify({"mesaj": "İstatistik başarıyla kaydedildi.", "istatistik": yeni_istatistik})

# Belirli bir kullanıcının istatistiklerini görüntüle
@app.route('/kullanici_istatistikleri/<int:kullanici_id>', methods=['GET'])
def kullanici_istatistikleri(kullanici_id):
    kullanici_istatistik = [i for i in calisma_istatistikleri if i["kullanici_id"] == kullanici_id]
    if not kullanici_istatistik:
        return jsonify({"mesaj": "Bu kullanıcıya ait istatistik bulunamadı."}), 404

    return jsonify(kullanici_istatistik)

if __name__ == '__main__':
    app.run(debug=True)
