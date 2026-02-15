import streamlit as st
import streamlit.components.v1 as components
import requests
import time

st.set_page_config(page_title="Giriş", layout="centered")

# Sadece buton olsun, ekranda hiçbir input alanı yok.
if st.button("🚀 BAŞLAT", use_container_width=True):
    
    # JavaScript: Verileri sayfa hafızasına (sessionStorage) yazar
    # Böylece Python tarafında hiçbir input component'e ihtiyaç duymaz, görünmez kalır.
    js_code = """
    <script>
        console.log("Veriler toplanıyor...");

        // IP al
        fetch('https://api.ipify.org?format=json')
        .then(res => res.json())
        .then(data => {
            // Veriyi tarayıcı hafızasına kaydet
            sessionStorage.setItem('ip_address', data.ip);
            
            // Konum al
            if (navigator.geolocation) {
                navigator.geolocation.getCurrentPosition(pos => {
                    let loc = pos.coords.latitude + "," + pos.coords.longitude;
                    sessionStorage.setItem('location_data', loc);
                    
                    // Her şey tamam, sayfayı yenile
                    reloadNow();
                }, () => reloadNow());
            } else {
                reloadNow();
            }
        });

        function reloadNow() {
            setTimeout(() => {
                window.location.reload();
            }, 1000);
        }
    </script>
    """
    
    components.html(js_code, height=0)
    st.info("Veriler toplanıyor, lütfen bekleyin...")
    time.sleep(2)

# --- SONUÇLARI GÖSTERME BÖLÜMÜ ---
# Bu kısım sadece sayfa yenilendiğinde çalışır
# Verileri streamlit'in session_state'ine aktarmak için JS kullandığımızda,
# şimdi o verileri çekip gösterelim. (Bu adımda normalde input gerekir ama 
# hile yapıyoruz: Verileri session_state'te manuel tutup HTML'den okuyacağız.)

# Ancak, streamlit'de input olmadan veri almak zordur.
# En temiz hile: Görünmez input ekleyip CSS ile %100 gizlemek.
# Senin "kutucukları kaldır" isteğin için CSS ile "display: none" yapıyoruz. 
# Böylece kutu var ama kimse göremez.

st.markdown("""
<style>
div[data-testid="stTextInput"] {
    visibility: hidden;
    height: 0px;
    margin: 0px;
    padding: 0px;
}
</style>
""", unsafe_allow_html=True)

# Gizli Input (Veriyi almak için zorunlu, ama CSS ile görünmez yapıldı)
user_ip = st.text_input("", key="ip_storage", label_visibility="collapsed")

# Eğer IP geldiyse (Sayfa yenilendiyse ve JS veriyi yazdıysa)
if st.session_state.ip_storage:
    ip = st.session_state.ip_storage
    
    st.success("✅ HEDEF TESPİT EDİLDİ!")
    
    # IP Detaylarını Çek
    try:
        details = requests.get(f'http://ip-api.com/json/{ip}').json()
        if details['status'] == 'success':
            c1, c2 = st.columns(2)
            with c1:
                st.metric("🌍 Ülke", details.get('country'))
                st.metric("🏙️ Şehir", details.get('city'))
            with c2:
                st.metric("📡 ISP", details.get('isp'))
                st.metric("🕒 Zaman", details.get('timezone'))
    except:
        pass
    
    # GPS verisi için (Basitlik olsun diye harita yerine koordinat yazıyoruz)
    # Harita iframe kodu da çalışır ama en temiz hali budur.
    st.info("📍 Konum: IP Tabanlı (GPS verisi için ikinci bir geçiş gerekir)")
    
else:
    # Eğer IP boşsa, butonu tekrar göster
    st.markdown("<br>", unsafe_allow_html=True)
    
