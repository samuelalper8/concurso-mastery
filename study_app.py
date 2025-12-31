import streamlit as st
import pandas as pd
import random
import json
import os
import time

# --- CONFIGURAÇÃO DA PÁGINA ---
st.set_page_config(page_title="Concurso Mastery Pro", page_icon="🏆", layout="wide")

# --- FUNÇÃO DE LOGIN ---
def check_password():
    """Retorna True se o usuário inseriu a senha correta."""
    def password_entered():
        # Verifica se as credenciais batem com o que você salvou no Streamlit Cloud Secrets
        if (st.session_state["username"] == st.secrets["credentials"]["username"] and
            st.session_state["password"] == st.secrets["credentials"]["password"]):
            st.session_state["password_correct"] = True
            del st.session_state["password"]  # Não guarda a senha na sessão
            del st.session_state["username"]
        else:
            st.session_state["password_correct"] = False

    if "password_correct" not in st.session_state:
        # Exibe formulário de login
        _, center, _ = st.columns([1, 1, 1])
        with center:
            st.title("🔒 Acesso Restrito")
            st.text_input("Usuário", on_change=password_entered, key="username")
            st.text_input("Senha", type="password", on_change=password_entered, key="password")
            st.info("Digite suas credenciais da ConPrev para acessar os 1.379 cartões.")
        return False
    elif not st.session_state["password_correct"]:
        # Senha errada
        st.error("😕 Usuário ou senha incorretos.")
        return False
    else:
        return True

# --- INÍCIO DO APP PROTEGIDO ---
if check_password():
    
    # --- CARREGAMENTO DE DADOS (JSON unificado) ---
    @st.cache_data
    def load_data():
        if os.path.exists("data_unificada.json"):
            with open("data_unificada.json", "r", encoding="utf-8") as f:
                return json.load(f)
        return []

    # Inicialização do Estado
    if 'cards_data' not in st.session_state:
        st.session_state['cards_data'] = load_data()
    if 'missed_cards' not in st.session_state:
        st.session_state['missed_cards'] = []
    if 'stats' not in st.session_state:
        st.session_state['stats'] = {"correct": 0, "wrong": 0, "start_time": time.time()}
    if 'current_idx' not in st.session_state: st.session_state['current_idx'] = 0
    if 'flipped' not in st.session_state: st.session_state['flipped'] = False

    # --- SIDEBAR E LÓGICA DE ESTUDO ---
    with st.sidebar:
        st.title(f"👋 Bem-vindo, Samuel")
        modo_fluxo = st.radio("Foco de Estudo:", ["Ciclo Normal", "Modo Revisão (Somente Erros)"]) # [cite: 114]
        eng_on = st.toggle("🌐 English Mode (Business & Tax)")
        
        st.divider()
        if st.button("🚪 Sair"):
            del st.session_state["password_correct"]
            st.rerun()

    # --- O RESTANTE DA SUA LÓGICA DE FILTRAGEM E FLASHCARDS VEM AQUI ---
    # (Mantenha a lógica de filtragem por matéria, busca e níveis que consolidamos anteriormente)
    
    st.success("Conectado à base de dados ConPrev.")
