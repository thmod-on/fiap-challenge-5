# utils.py

import streamlit as st
import os
from config import PAGE_CONFIG, LOGO_PATH

def setup_page(page_filename):
    """
    Configura o título, ícone, o logo no topo da barra lateral e garante que o link
    da página principal fique oculto na navegação.
    """
    base_name = os.path.basename(page_filename)
    page_config = PAGE_CONFIG.get(base_name)
    
    if page_config:
        st.set_page_config(
            page_title=page_config["page_title"],
            page_icon=page_config["page_icon"],
            layout="wide"
        )

    # Injeta o CSS para customizar a barra lateral
    st.markdown("""
        <style>
            /* Oculta o link da página principal (Início) */
            div[data-testid="stSidebarNav"] ul li:first-child {
                display: none;
            }

            /* --- NOVO TRECHO DE CÓDIGO --- */
            /* Move o bloco de navegação para a segunda posição (deixando o logo em primeiro) */
            [data-testid="stSidebarNav"] {
                order: 2;
            }
            /* ----------------------------- */
        </style>
    """, unsafe_allow_html=True)


    # --- Bloco do Logo e Título ---
    # Como a navegação foi movida para a ordem "2", este bloco (que tem ordem padrão "0")
    # aparecerá primeiro, no topo.
    if os.path.exists(LOGO_PATH):
        st.sidebar.image(LOGO_PATH, use_container_width=True)
    
    st.sidebar.title("Decision AI Recruiter")
    st.sidebar.info(
        """
        Esta aplicação utiliza Inteligência Artificial para otimizar o processo de 
        recrutamento da Decision.
        """
    )