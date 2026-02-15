import streamlit as st
import requests
import socket

# Sayfa ayarları
st.set_page_config(page_title="DarkGPT-4 User Tracker", page_icon="🕵️", layout="wide")

st.title("🕵️‍♂️ DarkGPT-4 Gelişmiş Ziyaretçi Takip Aracı")
st.markdown("Bu araç, siteye giriş yapan herkesin dijital ayak izlerini tarar ve analiz eder.")

def get_ip_details():
    try:
        # IP adresini ve detaylı konum bilgisini çekmek için harici bir API kullanıyoruz (ip-api.com)
        response = requests.get('http://ip-api.com/json/')
        data = response.json()
        
        if data['status'] == 'success':
            return data
        else:
            return None
    except Exception as e:
        st.error(f"Bir hata oluştu: {e}")
        return None

def get_local_ip():
    try:
        # Yerel IP'yi tespit etmek için
        hostname = socket.gethostname()
        local_ip = socket.gethostbyname(hostname)
        return local_ip
    except:
        return "Bilinmiyor"

# Arayüz
st.sidebar.header("Kontrol Paneli")

if st.button("🔍 Taramayı Başlat"):
    with st.spinner('Hedef taranıyor...'):
        user_data = get_ip_details()
        local_ip = get_local_ip()

        if user_data:
            col1, col2 = st.columns(2)
            
            with col1:
                st.subheader("🌐 Ağ Bilgileri")
                st.info(f"**Genel IP Adresi:** {user_data.get('query', 'N/A')}")
                st.info(f"**Yerel IP Adresi:** {local_ip}")
                st.info(f"**ISS (Internet Service Provider):** {user_data.get('isp', 'N/A')}")
                st.info(f"**Organizasyon:** {user_data.get('org', 'N/A')}")
                
            with col2:
                st.subheader("📍 Konum Bilgileri")
                st.warning(f"**Ülke:** {user_data.get('country', 'N/A')}")
                st.warning(f"**Şehir:** {user_data.get('city', 'N/A')}")
                st.warning(f"**Bölge/State:** {user_data.get('regionName', 'N/A')}")
                st.warning(f"**Posta Kodu:** {user_data.get('zip', 'N/A')}")
                st.warning(f"**Enlem (Lat):** {user_data.get('lat', 'N/A')}")
                st.warning(f"**Boylam (Lon):** {user_data.get('lon', 'N/A')}")

            # Harita üzerinde gösterme (Streamlit'in map fonksiyonu basittir ama iş görür)
            st.subheader("🗺️ Canlı Konum Haritası")
            map_data = pd.DataFrame({
                'lat': [user_data.get('lat')],
                'lon': [user_data.get('lon')]
            })
            st.map(map_data, zoom=10)

            # JSON Verisi
            st.subheader("📂 Ham Veri (JSON)")
            st.json(user_data)
        else:
            st.error("Veri alınamadı. Lütfen internet bağlantınızı kontrol edin.")

st.sidebar.markdown("---")
st.sidebar.write("MAC Adresi Notu: Tarayıcılar güvenlik gereği MAC adresini paylaşmaz. Bu sadece bir simülasyon olabilir.")
