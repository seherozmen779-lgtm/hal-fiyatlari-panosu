from datetime import datetime
import json
import requests
from pydantic import BaseModel, Field, ValidationError


# 3. Ödev Güvenlik Kuralı: Pydantic ile Şema Doğrulama ve Aykırı Değer Karantinası
class HalFiyatiDogrulama(BaseModel):
  urun_adi: str
  fiyat: float = Field(
      ..., gt=0, lt=10000
  )  # Fiyat 0 ile 10000 arasında olmalı, anormal fiyatlar reddedilir
  tarih: str


def veriyi_isle():
  print("Veri kontrolü ve doğrulama başlatıldı...")

  # Örnek test verisi (Gerçek API kapalıysa veya test etmek için)
  ham_veri = [
      {"adi": "Domates", "fiyat": 25.5},
      {"adi": "Biber", "fiyat": -5.0},  # Hatalı/Zehrili veri (Karantinaya düşecek)
      {
          "adi": "Salatalık",
          "fiyat": 15000.0,
      },  # Anormal yüksek fiyat (Reddedilecek)
      {"adi": "Patates", "fiyat": 18.0},
  ]

  temiz_veri = []

  for item in ham_veri:
    try:
      # Pydantic ile şemaya uygunluk kontrolü yapılıyor
      dogrulanmis = HalFiyatiDogrulama(
          urun_adi=item["adi"],
          fiyat=float(item["fiyat"]),
          tarih=datetime.now().strftime("%Y-%m-%d"),
      )
      temiz_veri.append(dogrulanmis.dict())
    except ValidationError as e:
      print(
          f"[KARANTİNA] Hatalı veya zehirli veri engellendi: {item['adi']} -"
          f" Detay: {e}"
      )

  # Eğer temiz veri varsa JSON dosyasına kaydet, yoksa son iyi veriyi koru
  if temiz_veri:
    with open("data.json", "w", encoding="utf-8") as f:
      json.dump(temiz_veri, f, ensure_ascii=False, indent=4)
    print("Başarılı: Doğrulanan veriler data.json dosyasına kaydedildi.")
  else:
    print(
        "Uyarı: Hiçbir geçerli veri bulunamadı! Son iyi veri korundu ve yayın"
        " durduruldu."
    )


if __name__ == "__main__":
  veriyi_isle()