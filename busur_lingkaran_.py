import streamlit as st
import math
import time
import random
import pandas as pd
import numpy as np
import plotly.graph_objects as go

# --- Fungsi Inti Perhitungan ---
def hitung_busur_juring(radius, sudut_derajat):
    """
    Menghitung panjang busur dan luas juring lingkaran.
    Mengembalikan tuple (panjang_busur, luas_juring) atau (None, None) jika input tidak valid.
    """
    if radius <= 0:
        return None, None # Jari-jari harus positif

    sudut_radian = math.radians(sudut_derajat)
    panjang_busur = radius * sudut_radian
    luas_juring = 0.5 * (radius**2) * sudut_radian
    return panjang_busur, luas_juring

# --- Fungsi untuk Membuat Visualisasi Lingkaran ---
def plot_lingkaran_juring(radius, sudut_derajat):
    fig = go.Figure()

    # Gambar Lingkaran Penuh
    theta_full = np.linspace(0, 2 * np.pi, 100)
    x_full = radius * np.cos(theta_full)
    y_full = radius * np.sin(theta_full)
    fig.add_trace(go.Scatter(x=x_full, y=y_full, mode='lines', name='Lingkaran',
                             line=dict(color='lightgray', width=2)))

    # Gambar Juring
    if sudut_derajat != 0 and radius > 0:
        sudut_radian = math.radians(sudut_derajat)
        
        # Batasi sudut agar tidak terlalu berputar dalam visualisasi jika melebihi 360
        visual_sudut_radian = sudut_radian % (2 * math.pi)
        if visual_sudut_radian < 0:
            visual_sudut_radian += 2 * math.pi

        # Titik-titik untuk juring
        theta_juring = np.linspace(0, visual_sudut_radian, 50)
        x_juring_busur = radius * np.cos(theta_juring)
        y_juring_busur = radius * np.sin(theta_juring)

        x_juring = np.concatenate([[0], x_juring_busur, [0]])
        y_juring = np.concatenate([[0], y_juring_busur, [0]])

        fig.add_trace(go.Scatter(x=x_juring, y=y_juring, mode='lines', fill='toself', name='Juring',
                                 fillcolor='rgba(100, 149, 237, 0.5)',
                                 line=dict(color='cornflowerblue', width=2)))
        
        # Garis radius
        fig.add_trace(go.Scatter(x=[0, radius * math.cos(0)], y=[0, radius * math.sin(0)],
                                 mode='lines', name='Radius 1', line=dict(color='darkblue', width=2)))
        if visual_sudut_radian > 0:
             fig.add_trace(go.Scatter(x=[0, radius * math.cos(visual_sudut_radian)], y=[0, radius * math.sin(visual_sudut_radian)],
                                  mode='lines', name='Radius 2', line=dict(color='darkblue', width=2)))
        
        # --- Menambahkan Label pada Visualisasi ---
        # Titik Pusat O
        fig.add_trace(go.Scatter(x=[0], y=[0], mode='markers+text',
                                 marker=dict(size=8, color='black'),
                                 text=['O'], textposition='bottom right', textfont=dict(size=14, color='black')))
        
        # Titik A (pada sudut 0)
        fig.add_trace(go.Scatter(x=[radius * math.cos(0)], y=[radius * math.sin(0)],
                                 mode='markers+text',
                                 marker=dict(size=8, color='red'),
                                 text=['A'], textposition='top right', textfont=dict(size=14, color='red')))
        
        # Titik B (pada sudut visual_sudut_radian)
        fig.add_trace(go.Scatter(x=[radius * math.cos(visual_sudut_radian)], y=[radius * math.sin(visual_sudut_radian)],
                                 mode='markers+text',
                                 marker=dict(size=8, color='red'),
                                 text=['B'], textposition='top left', textfont=dict(size=14, color='red')))
                                 
        # Posisi Teks Sudut Alfa (di tengah juring)
        mid_angle = visual_sudut_radian / 2
        label_radius_offset = radius * 0.4
        fig.add_trace(go.Scatter(x=[label_radius_offset * math.cos(mid_angle)],
                                 y=[label_radius_offset * math.sin(mid_angle)],
                                 mode='text',
                                 text=[r'$\alpha$'],
                                 textposition='middle center', textfont=dict(size=20, color='darkgreen')))


    # Pengaturan layout
    max_val = radius * 1.2
    fig.update_xaxes(range=[-max_val, max_val], showgrid=False, zeroline=False, showticklabels=False)
    fig.update_yaxes(range=[-max_val, max_val], showgrid=False, zeroline=False, showticklabels=False, scaleanchor="x", scaleratio=1)
    fig.update_layout(title='Visualisasi Lingkaran dan Juring', showlegend=False,
                      plot_bgcolor='rgba(0,0,0,0)', paper_bgcolor='rgba(0,0,0,0)')

    return fig


# --- Halaman Menu 1: Kalkulator Busur & Juring ---
def kalkulator_menu():
    st.title("📏 Kalkulator Panjang Busur & Luas Juring Lingkaran 📐")
    st.markdown("""
    Selamat datang di kalkulator interaktif! Masukkan nilai **jari-jari** lingkaran dan **sudut pusat** juring
    (dalam derajat) untuk menemukan panjang busur dan luas juringnya.
    **Visualisasi akan berubah secara *real-time*!**
    """)

    st.write("---")

    st.header("⚙️ Masukkan Data Lingkaran")

    col1, col2 = st.columns(2)

    with col1:
        radius = st.number_input(
            "Masukkan Jari-jari Lingkaran (r)",
            min_value=0.01,
            value=10.0,
            format="%.2f",
            help="Jari-jari lingkaran harus bernilai positif."
        )
    with col2:
        sudut_derajat = st.slider(
            "Pilih Sudut Pusat (derajat)",
            min_value=0.0,
            max_value=720.0,
            value=90.0,
            step=0.5,
            format="%.1f",
            help="Sudut pusat juring dalam derajat. 360 derajat adalah satu lingkaran penuh."
        )

    st.write("---")
    
    st.header("👁️ Visualisasi")
    fig_lingkaran = plot_lingkaran_juring(radius, sudut_derajat)
    st.plotly_chart(fig_lingkaran, use_container_width=True)


    st.header("✨ Hasil Perhitungan ✨")

    panjang_busur, luas_juring = hitung_busur_juring(radius, sudut_derajat)

    if panjang_busur is not None:
        colors = ["#4CAF50", "#2196F3", "#FFC107", "#9C27B0", "#E91E63"]
        selected_color = random.choice(colors)

        st.markdown(f"""
        <div style="background-color:{selected_color}; padding: 25px; border-radius: 12px; text-align: center; margin-top: 20px; box-shadow: 0 4px 8px 0 rgba(0,0,0,0.2);">
            <h3 style="color: white; margin-bottom: 15px; font-size: 28px;">✅ Hasil Ditemukan! ✅</h3>
            <p style="font-size: 22px; font-weight: normal; color: white;">
                Dengan Jari-jari **{radius:.2f}** dan Sudut Pusat **{sudut_derajat:.1f}°**:
            </p>
            <p style="font-size: 36px; font-weight: bolder; color: white; margin-top: 15px;">
                Panjang Busur: <span style="color: yellow;">{panjang_busur:.4f}</span> cm
            </p>
            <p style="font-size: 36px; font-weight: bolder; color: white;">
                Luas Juring: <span style="color: yellow;">{luas_juring:.4f}</span> cm²
            </p>
        </div>
        """, unsafe_allow_html=True)
        
        st.info(f"Sudut pusat **{sudut_derajat:.1f}°** setara dengan **{math.radians(sudut_derajat):.4f} radian**.")


    else:
        st.error("❌ Input tidak valid! Jari-jari harus lebih besar dari nol.")
    
    st.markdown("---")


# --- Halaman Menu 2: Penjelasan Rumus ---
def penjelasan_rumus_menu():
    st.title("💡 Penjelasan Rumus Kalkulator 💡")
    st.markdown("""
    Di bagian ini, kita akan membahas lebih dalam mengenai rumus matematika yang digunakan
    dalam kalkulator ini untuk menghitung panjang busur dan luas juring lingkaran.
    """)

    st.write("---")

    st.header("1. Panjang Busur Lingkaran ($s$)")
    st.markdown("""
    Panjang busur adalah bagian dari keliling lingkaran yang dibatasi oleh dua titik pada lingkaran
    dan sudut pusat tertentu. Bayangkan Anda memotong sepotong "kue pizza" dari lingkaran,
    panjang busur adalah panjang kulit luarnya.
    """)
    st.latex(r'''s = r \times \theta_{radian}''')
    st.markdown("""
    Di mana:
    * $s$ = Panjang Busur
    * $r$ = Jari-jari lingkaran (jarak dari pusat ke tepi lingkaran)
    * $\\theta_{radian}$ = Sudut pusat juring dalam satuan **radian**

    **Penting:** Jika sudut yang Anda miliki dalam **derajat**, Anda harus mengubahnya terlebih dahulu ke radian menggunakan rumus konversi:
    """)
    st.latex(r'''\theta_{radian} = \text{sudut dalam derajat} \times \frac{\pi}{180}''')

    st.header("2. Luas Juring Lingkaran ($A$)")
    st.markdown("""
    Luas juring adalah luas daerah yang dibatasi oleh dua jari-jari dan busur lingkaran.
    Ini adalah luas dari potongan "kue pizza" itu sendiri.
    """)
    st.latex(r'''A = \frac{1}{2} r^2 \times \theta_{radian}''')
    st.markdown("""
    Di mana:
    * $A$ = Luas Juring
    * $r$ = Jari-jari lingkaran
    * $\\theta_{radian}$ = Sudut pusat juring dalam satuan **radian**

    Sama seperti panjang busur, jika sudut Anda dalam **derajat**, Anda perlu mengonversinya ke radian terlebih dahulu.
    """)

    st.write("---")
    st.info("""
    **Mengapa Menggunakan Radian?**
    Dalam banyak rumus matematika yang melibatkan lingkaran dan trigonometri, penggunaan radian menyederhanakan perhitungan dan secara alami sesuai dengan definisi turunan dan integral fungsi trigonometri. Satu radian adalah sudut ketika panjang busur sama dengan jari-jari lingkaran.
    """)
    st.markdown(f"Untuk nilai $\\pi$ (pi) yang digunakan di sini, sekitar **{math.pi:.6f}**.")


# --- Main Aplikasi Streamlit ---
def main():
    # Konfigurasi halaman umum
    st.set_page_config(
        page_title="Aplikasi Geometri Lingkaran Interaktif 🌌",
        page_icon="🧭",
        layout="wide",
        initial_sidebar_state="expanded"
    )

    st.sidebar.title("Navigasi Aplikasi")
    menu_selection = st.sidebar.radio(
        "Pilih Menu:",
        ["Kalkulator Busur & Juring", "Penjelasan Rumus"]
    )

    if menu_selection == "Kalkulator Busur & Juring":
        kalkulator_menu()
    elif menu_selection == "Penjelasan Rumus":
        penjelasan_rumus_menu()

    current_time = time.strftime("%A, %d %B %Y", time.localtime())
    st.sidebar.markdown("---")
    st.sidebar.caption(f"Versi Aplikasi v2.3. Dibuat dengan ❤️ di Pekalongan, {current_time}.")

if __name__ == "__main__":
    main()
