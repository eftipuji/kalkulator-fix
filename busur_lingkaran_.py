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
    
    # --- Fungsi untuk Membuat Visualisasi Lingkaran dengan Animasi ---
    def plot_lingkaran_juring_animated(radius, max_sudut_animasi):
        fig = go.Figure(
            data=[go.Scatter(x=[], y=[], mode='lines', name='Lingkaran',
                             line=dict(color='lightgray', width=2)),
                  go.Scatter(x=[0, radius], y=[0, 0], mode='lines', name='Radius 1', line=dict(color='darkblue', width=2)),
                  go.Scatter(x=[], y=[], mode='lines', name='Radius 2', line=dict(color='darkblue', width=2)),
                  go.Scatter(x=[0], y=[0], mode='markers+text',
                             marker=dict(size=8, color='black'),
                             text=['O'], textposition='bottom right', textfont=dict(size=14, color='black')),
                  go.Scatter(x=[radius], y=[0], mode='markers+text',
                             marker=dict(size=8, color='red'),
                             text=['A'], textposition='top right', textfont=dict(size=14, color='red')),
                  go.Scatter(x=[], y=[], mode='markers+text',
                             marker=dict(size=8, color='red'),
                             text=['B'], textposition='top left', textfont=dict(size=14, color='red')),
                  go.Scatter(x=[], y=[], mode='text',
                             text=[r'$\theta$'],
                             textposition='middle center', textfont=dict(size=20, color='darkgreen'))],
            layout=go.Layout(
                xaxis=dict(range=[-radius * 1.2, radius * 1.2], showgrid=False, zeroline=False, showticklabels=False, fixedrange=True),
                yaxis=dict(range=[-radius * 1.2, radius * 1.2], showgrid=False, zeroline=False, showticklabels=False, scaleanchor="x", scaleratio=1, fixedrange=True),
                title='Visualisasi Lingkaran dan Juring (Animasi)', showlegend=False,
                plot_bgcolor='rgba(0,0,0,0)', paper_bgcolor='rgba(0,0,0,0)'
            ),
            frames=[go.Frame(
                data=[go.Scatter(x=radius * np.cos(np.linspace(0, 2 * np.pi, 100)),
                                 y=radius * np.sin(np.linspace(0, 2 * np.pi, 100))),
                      go.Scatter(x=[0, radius * math.cos(math.radians(sudut))],
                                 y=[0, radius * math.sin(math.radians(sudut))]),
                      go.Scatter(x=[radius * math.cos(math.radians(sudut))],
                                 y=[radius * math.sin(math.radians(sudut))]),
                      go.Scatter(x=[radius * 0.4 * math.cos(math.radians(sudut) / 2)],
                                 y=[radius * 0.4 * math.sin(math.radians(sudut) / 2)])
                ],
                name=f'frame{i}'
            )
                for i, sudut in enumerate(np.linspace(0, max_sudut_animasi, 100))]
        )
    
        fig.update(frames=fig.frames,
                   layout_updatemenus=[{
                       "type": "buttons",
                       "buttons": [
                           {
                               "label": "Play",
                               "method": "animate",
                               "args": [None, {"frame": {"duration": 50, "redraw": True},
                                                "fromcurrent": True, "transition": {"duration": 0,
                                                                                    "easing": "linear"}}]},
                           {
                               "label": "Pause",
                               "method": "animate",
                               "args": [[None], {"frame": {"duration": 0, "redraw": False},
                                                 "mode": "immediate",
                                                 "transition": {"duration": 0}}]}
                       ]
                   }])
    
        return fig
    
    
    # --- Halaman Menu 1: Kalkulator Busur & Juring ---
    def kalkulator_menu():
        st.title("📏 Kalkulator Panjang Busur & Luas Juring Lingkaran 📐")
        st.markdown("""
        Selamat datang di kalkulator interaktif! Masukkan nilai **jari-jari** lingkaran dan **sudut pusat** juring
        (dalam derajat) untuk menemukan panjang busur dan luas juringnya.
        **Visualisasi akan berubah secara interaktif!**
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
        
        st.header("👁️ Visualisasi Interaktif")
        fig_lingkaran = plot_lingkaran_juring_animated(radius, sudut_derajat)
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
                    Panjang Busur: <span style="color: yellow;">{panjang_busur:.4f}</span> unit
                </p>
                <p style="font-size: 36px; font-weight: bolder; color: white;">
                    Luas Juring: <span style="color: yellow;">{luas_juring:.4f}</span> unit²
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
