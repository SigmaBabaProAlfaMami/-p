import streamlit as st
import streamlit.components.v1 as components
import requests
import json

st.set_page_config(page_title="DarkGPT-4 Real Tracker", page_icon="🕵️", layout="wide")

st.title("🕵️‍♂️ DarkGPT-4 Gerçek Zamanlı Ziyaretçi Takibi")
st.markdown("Bu araç JavaScript API kullanarak ziyaretçinin doğrudan tarayıcı bilgisini alır.")

# JavaScript ile İstemci IP ve Konumunu Alma
html_code = """
<div id="user-info" style="font-family: monospace; padding: 10px; background-color: #0E1117; border-radius: 5px;">
    <h3 style="color: #00FF00;">Veriler Alınıyor...</h3>
    <p id="ip-address">IP: Bekleniyor...</p>
    <p id="location">Konum: Bekleniyor...</p>
</div>

<script>
    // 1. IP adresini al (ipify API üzerinden)
    fetch('https://api.ipify.org?format=json')
    .then(response => response.json())
    .then(data => {
        document.getElementById('ip-address').innerText = "IP: " + data.ip;
        
        // IP'yi Python'a göndermek için bir input'a yazıyoruz (Gizli yöntem)
        var event = new Event('input', { bubbles: true });
        window.parent.document.getElementById('ip_data').value = data.ip;
        window.parent.document.getElementById('ip_data').dispatchEvent(event);
    });

    // 2. Tarayıcı Konumunu (Geolocation API) al
    if (navigator.geolocation) {
        navigator.geolocation.getCurrentPosition(function(position) {
            var lat = position.coords.latitude;
            var lon = position.coords.longitude;
            document.getElementById('location').innerText = "Konum: " + lat + ", " + lon;
            
            // Konumu Python'a göndermek
            window.parent.document.getElementById('loc_data').value = lat + "," + lon;
            window.parent.document.getElementById('loc_data').dispatchEvent(event);
        }, function(error) {
            document.getElementById('location').innerText = "Konum İzni Reddedildi veya Hata.";
        });
    } else {
        document.getElementById('location').innerText = "Tarayıcı konum desteklemiyor.";
    }
</script>
"""

# Gizli input alanları (JS verilerini yakalamak için)
st.text_input("IP Verisi (Gizli)", key="ip_data", label_visibility="collapsed")
st.text_input("Konum Verisi (Gizli)", key="loc_data", label_visibility="collapsed")

# HTML/JS Bileşenini Render Et
components.html(html_code, height=200)

# Butona basınca verileri işle
if st.button("🔍 Verileri Analiz Et"):
    client_ip = st.session_state.ip_data
    client_loc = st.session_state.loc_data

    if client_ip:
        st.subheader("🕵️ Ziyaretçinin IP Bilgisi")
        st.success(f"IP: {client_ip}")
        
        # IP üzerinden detaylı bilgi almak için
        try:
            resp = requests.get(f'http://ip-api.com/json/{client_ip}')
            info = resp.json()
            if info['status'] == 'success':
                col1, col2 = st.columns(2)
                with col1:
                    st.info(f"**Ülke:** {info.get('country')}")
                    st.info(f"**Şehir:** {info.get('city')}")
                    st.info(f"**ISP:** {info.get('isp')}")
                with col2:
                    st.info(f"**Bölge:** {info.get('regionName')}")
                    st.info(f"**Zaman Dilimi:** {info.get('timezone')}")
                    
                # Harita (eğer varsa)
                lat = info.get('lat')
                lon = info.get('lon')
                if lat and lon:
                    map_url = f"https://www.openstreetmap.org/export/embed.html?bbox={lon-0.1},{lat-0.1},{lon+0.1},{lat+0.1}&layer=mapnik&marker={lat},{lon}"
                    components.v1.iframe(map_url, height=400)
        except:
            st.error("Detaylı bilgi alınamadı.")

    if client_loc:
        st.subheader("📱 Cihazdan Alınan GPS Konumu")
        st.info(f"Koordinatlar: {client_loc}")

st.sidebar.markdown("---")
st.sidebar.write("Not: GPS konumu için ziyaretçinin tarayıcıda 'İzin Ver' demesi gerekir.")
