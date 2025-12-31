import streamlit as st
import pandas as pd
import random
import json
import os
import time

# --- CONFIGURAÇÃO DA PÁGINA ---
st.set_page_config(page_title="Concurso Mastery Pro", page_icon="🏆", layout="wide")

# --- CARREGAMENTO DE DADOS ---
@st.cache_data
def load_data():
    if os.path.exists("data_unificada.json"):
        with open("data_unificada.json", "r", encoding="utf-8") as f:
            return json.load(f)
    return []

# Inicialização das variáveis de estado (Session State)
if 'cards_data' not in st.session_state:
    st.session_state['cards_data'] = load_data()
if 'missed_cards' not in st.session_state:
    st.session_state['missed_cards'] = []
if 'stats' not in st.session_state:
    st.session_state['stats'] = {"correct": 0, "wrong": 0, "start_time": time.time()}
if 'current_idx' not in st.session_state:
    st.session_state['current_idx'] = 0
if 'flipped' not in st.session_state:
    st.session_state['flipped'] = False

# --- ESTILIZAÇÃO CSS ---
st.markdown("""
    <style>
    .main { background-color: #0f172a; }
    .flashcard {
        background-color: white; padding: 50px; border-radius: 25px;
        border-left: 10px solid #4f46e5; text-align: center; min-height: 300px;
        display: flex; flex-direction: column; justify-content: center;
        box-shadow: 0 10px 25px rgba(0,0,0,0.2);
    }
    .flashcard-back { background: linear-gradient(135deg, #1e1b4b, #312e81); color: white; }
    .metric-card { background: #1e293b; color: white; padding: 20px; border-radius: 15px; text-align: center; border: 1px solid #334155; }
    .level-tag { padding: 4px 12px; border-radius: 20px; font-weight: bold; font-size: 12px; background: #fbbf24; color: black; }
    </style>
""", unsafe_allow_html=True)

# --- SIDEBAR: CONTROLES E FILTROS ---
with st.sidebar:
    st.title("🏆 Mastery Control")
    st.write(f"Usuário: Samuel Almeida")
    
    modo_fluxo = st.radio("Foco de Estudo:", ["Ciclo Normal", "Modo Revisão (Somente Erros)"])
    
    st.divider()
    
    subjects = sorted(list(set(c['subject'] for c in st.session_state['cards_data'])))
    sel_subject = st.selectbox("📚 Matéria", ["Todas"] + subjects)
    
    search = st.text_input("🔍 Buscar no Banco")
    
    st.divider()
    
    if st.session_state['missed_cards']:
        csv = pd.DataFrame(st.session_state['missed_cards']).to_csv(index=False).encode('utf-8-sig')
        st.download_button("📥 Baixar Relatório de Erros", data=csv, file_name="revisao.csv", use_container_width=True)
    
    if st.button("🔄 Reiniciar Sessão"):
        st.session_state['stats'] = {"correct": 0, "wrong": 0, "start_time": time.time()}
        st.session_state['current_idx'] = 0
        st.rerun()

# --- LÓGICA DE FILTRAGEM ---
base = st.session_state['missed_cards'] if modo_fluxo == "Modo Revisão (Somente Erros)" else st.session_state['cards_data']
data = [c for c in base if 
        (sel_subject == "Todas" or c['subject'] == sel_subject) and
        (search.lower() in c['front'].lower() or search.lower() in c['back'].lower())]

# --- INTERFACE PRINCIPAL ---
if not data:
    st.info("Nenhum cartão encontrado. Verifique os filtros.")
else:
    # Métricas
    m1, m2, m3 = st.columns(3)
    with m1:
        total_v = st.session_state['stats']['correct'] + st.session_state['stats']['wrong']
        acc = (st.session_state['stats']['correct'] / total_v * 100) if total_v > 0 else 0
        st.markdown(f'<div class="metric-card">🎯 Precisão<br><h2>{acc:.1f}%</h2></div>', unsafe_allow_html=True)
    with m2:
        tempo = int((time.time() - st.session_state['stats']['start_time']) / 60)
        st.markdown(f'<div class="metric-card">⏱️ Tempo<br><h2>{tempo} min</h2></div>', unsafe_allow_html=True)
    with m3:
        restantes = len(data) - (st.session_state["current_idx"] % len(data))
        st.markdown(f'<div class="metric-card">📚 Restantes<br><h2>{restantes}</h2></div>', unsafe_allow_html=True)

    st.divider()

    # Cartão
    idx = st.session_state['current_idx'] % len(data)
    card = data[idx]

    _, center, _ = st.columns([0.1, 0.8, 0.1])
    with center:
        if not st.session_state['flipped']:
            st.markdown(f"""
                <div class="flashcard">
                    <p style="color:#6366f1; font-weight:bold;">{card['subject']}</p>
                    <h1 style="color:#1e293b;">{card['front']}</h1>
                </div>
            """, unsafe_allow_html=True)
            if st.button("👁️ REVELAR RESPOSTA", use_container_width=True, type="primary"):
                st.session_state['flipped'] = True
                st.rerun()
        else:
            st.markdown(f"""
                <div class="flashcard flashcard-back">
                    <h2 style="line-height:1.5;">{card['back']}</h2>
                </div>
            """, unsafe_allow_html=True)
            
            c1, c2 = st.columns(2)
            if c1.button("❌ ERREI", use_container_width=True):
                if card not in st.session_state['missed_cards']:
                    st.session_state['missed_cards'].append(card)
                st.session_state['stats']['wrong'] += 1
                st.session_state['flipped'] = False
                st.session_state['current_idx'] += 1
                st.rerun()
            if c2.button("✅ ACERTEI", use_container_width=True):
                if modo_fluxo == "Modo Revisão (Somente Erros)" and card in st.session_state['missed_cards']:
                    st.session_state['missed_cards'].remove(card)
                st.session_state['stats']['correct'] += 1
                st.session_state['flipped'] = False
                st.session_state['current_idx'] += 1
                st.rerun()
