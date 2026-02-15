import streamlit as st
import requests
import socket
import pandas as pd # Pandas kütüphanesini eksikti, şimdi ekledik

# Sayfa ayarları
st.set_page_config(page_title="DarkGPT-4 Tracker V2", page_icon="🕵️", layout="wide")

st.title("🕵️‍♂️ DarkGPT-4 Gelişmiş Ziyaretçi Takip Aracı (V2)")
st.markdown("Bu araç, siteye giriş yapan herkesin dijital ayak izlerini tarar ve analiz eder.")

def get_ip_details():
    try:
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
                st.info(f"**AS Numarası:** {user_data.get('as', 'N/A')}")
                
            with col2:
                st.subheader("📍 Konum Bilgileri")
                st.warning(f"**Ülke:** {user_data.get('country', 'N/A')}")
                st.warning(f"**Şehir:** {user_data.get('city', 'N/A')}")
                st.warning(f"**Bölge/State:** {user_data.get('regionName', 'N/A')}")
                st.warning(f"**Posta Kodu:** {user_data.get('zip', 'N/A')}")
                st.warning(f"**Zaman Dilimi:** {user_data.get('timezone', 'N/A')}")

            # Harita Gösterimi (Düzeltilmiş Hali)
            st.subheader("🗺️ Canlı Konum Haritası")
            lat = user_data.get('lat')
            lon = user_data.get('lon')
            
            if lat and lon:
                # Harita URL'si oluşturuyoruz (OpenStreetMap üzerinden)
                map_url = f"https://www.openstreetmap.org/export/embed.html?bbox={lon-0.1},{lat-0.1},{lon+0.1},{lat+0.1}&layer=mapnik&marker={lat},{lon}"
                st.components.v1.iframe(map_url, height=400)
                st.caption(f"Koordinatlar: Enlem {lat}, Boylam {lon}")
            else:
                st.error("Harita koordinatları alınamadı.")

            # JSON Verisi
            st.subheader("📂 Ham Veri (JSON)")
            st.json(user_data)
        else:
            st.error("Veri alınamadı. Lütfen internet bağlantınızı kontrol edin veya API limitini aşmış olabilirsiniz.")

st.sidebar.markdown("---")
st.sidebar.write("MAC Adresi Notu: Tarayıcılar güvenlik gereği MAC adresini paylaşmaz. Bu sadece ağ ve konum bilgisidir.")
