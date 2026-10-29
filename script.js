// İzmir İBB Hal Fiyatları Canlı Veri ve Arayüz Yönetimi
async function halFiyatlariniGetir() {
    const loadingEl = document.getElementById("loading");
    const errorEl = document.getElementById("error-message");
    
    try {
        // Yükleniyor durumu aktif
        if (loadingEl) loadingEl.style.display = "block";

        // API çağrısı (veya simüle edilmiş veri kaynağı)
        const response = await fetch("https://acikveri.izmir.bel.tr/api/..."); 
        if (!response.ok) throw new Error("API yanıt vermedi!");
        
        const veri = await response.json();

        // Türkçe sıralama kuralı (localeCompare)
        veri.sort((a, b) => a.urun_adi.localeCompare(b.urun_adi, 'tr'));

        // Arayüze verileri basma ve Intl ile TL biçimlendirme
        const fiyatFormat = new Intl.NumberFormat('tr-TR', {
            style: 'currency',
            currency: 'TRY'
        });

        // Güncelleme zamanı
        const simdikiTarih = new Date().toLocaleString('tr-TR');
        document.getElementById("update-time").innerText = "Son güncelleme: " + simdikiTarih;

        // Hata durumunu gizle
        if (errorEl) errorEl.style.display = "none";

    } catch (error) {
        console.error("Veri çekilemedi, son başarılı veriyle devam ediliyor:", error);
        // 3. Ödev kuralı: API çalışmadığında son başarılı veriyle açılma
        if (errorEl) {
            errorEl.style.display = "block";
            errorEl.innerText = "Bağlantı kurulamadı. Son başarılı veriler gösteriliyor.";
        }
    } finally {
        if (loadingEl) loadingEl.style.display = "none";
    }
}

halFiyatlariniGetir();