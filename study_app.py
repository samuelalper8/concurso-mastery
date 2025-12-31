import streamlit as st
import pandas as pd
import random
import json
import os
import time

# --- CONFIGURAÇÃO DA PÁGINA ---
st.set_page_config(page_title="Concurso Mastery Pro", page_icon="🏆", layout="wide")

# --- BANCO DE DADOS DE INGLÊS (EXECUTIVE/TAX) ---
ENGLISH_DB = [
    {"subject": "English: Business", "front": "Due Diligence", "back": "Diligência prévia; processo de auditoria e investigação.", "level": "Top 1"},
    {"subject": "English: Tax", "front": "Tax Compliance", "back": "Conformidade Fiscal; cumprimento de obrigações tributárias.", "level": "Essencial"},
    {"subject": "English: Finance", "front": "Financial Statements", "back": "Demonstrações Financeiras; relatórios contábeis.", "level": "Frequente"}
]

# --- CARREGAMENTO DE DADOS ---
@st.cache_data
def load_data():
    if os.path.exists("data_unificada.json"):
        with open("data_unificada.json", "r", encoding="utf-8") as f:
            return json.load(f)
    return []

# --- INICIALIZAÇÃO DO ESTADO (SESSION STATE) ---
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
        box-shadow: 0 10px 15px rgba(0,0,0,0.3);
    }
    .flashcard-back { background: linear-gradient(135deg, #1e1b4b, #312e81); color: white; }
    .metric-card { background: #1e293b; color: white; padding: 20px; border-radius: 15px; text-align: center; border: 1px solid #334155; }
    </style>
""", unsafe_allow_html=True)

# --- SIDEBAR: CONTROLE TOTAL ---
with st.sidebar:
    st.title("🏆 Mastery Control")
    
    # 1. Modo de Estudo
    modo_fluxo = st.radio("Foco de Estudo:", ["Ciclo Normal", "Modo Revisão (Somente Erros)"])
    
    # 2. English Mode Toggle
    eng_on = st.toggle("🌐 English Mode (Business & Tax)")
    
    st.divider()
    
    # 3. Filtros Dinâmicos
    # Se modo English estiver ON, adicionamos os termos de inglês à lista
    pool_completo = st.session_state['cards_data'] + (ENGLISH_DB if eng_on else [])
    
    subjects = sorted(list(set(c['subject'] for c in pool_completo)))
    sel_subject = st.selectbox("📚 Matéria", ["Todas"] + subjects)
    
    levels = sorted(list(set(c.get('level', 'Geral') for c in pool_completo)))
    sel_levels = st.multiselect("⚡ Nível de Prioridade", levels, default=levels)
    
    search = st.text_input("🔍 Buscar no Banco (ex: LRF, SPED)")
    
    st.divider()
    
    # Botão de Exportação
    if st.session_state['missed_cards']:
        csv = pd.DataFrame(st.session_state['missed_cards']).to_csv(index=False).encode('utf-8-sig')
        st.download_button("📥 Baixar Relatório de Erros", data=csv, file_name="erros_revisao.csv", use_container_width=True)

# --- LÓGICA DE FILTRAGEM (O CORAÇÃO DO APP) ---
# Define a base (Normal ou Erros)
base = st.session_state['missed_cards'] if modo_fluxo == "Modo Revisão (Somente Erros)" else pool_completo

# Aplica os filtros em cascata
data = [c for c in base if 
        (sel_subject == "Todas" or c['subject'] == sel_subject) and
        (c.get('level', 'Geral') in sel_levels) and
        (search.lower() in c['front'].lower() or search.lower() in c['back'].lower())]

# --- INTERFACE PRINCIPAL ---
if not data:
    st.info("Nenhum cartão encontrado para os filtros selecionados.")
else:
    # Métricas (conforme suas imagens)
    m1, m2, m3 = st.columns(3)
    with m1:
        acc = (st.session_state['stats']['correct'] / (st.session_state['stats']['correct'] + st.session_state['stats']['wrong'] + 1e-9)) * 100
        st.markdown(f'<div class="metric-card">🎯 Precisão<br><h2>{acc:.1f}%</h2></div>', unsafe_allow_html=True)
    with m2:
        tempo = int((time.time() - st.session_state['stats']['start_time']) / 60)
        st.markdown(f'<div class="metric-card">⏱️ Tempo<br><h2>{tempo} min</h2></div>', unsafe_allow_html=True)
    with m3:
        st.markdown(f'<div class="metric-card">📚 Restantes<br><h2>{len(data) - (st.session_state["current_idx"] % len(data))}</h2></div>', unsafe_allow_html=True)

    st.divider()

    # Exibição do Flashcard
    idx = st.session_state['current_idx'] % len(data)
    card = data[idx]

    _, center, _ = st.columns([0.1, 0.8, 0.1])
    with center:
        if not st.session_state['flipped']:
            # FRENTE
            st.markdown(f"""
                <div class="flashcard">
                    <p style="color:#6366f1; font-weight:bold;">{card['subject']} ({card.get('level', 'Geral')})</p>
                    <h1 style="color:#1e293b;">{card['front']}</h1>
                    <p style="color:#94a3b8; font-style:italic; margin-top:20px;">Use a técnica Feynman: Explique em voz alta!</p>
                </div>
            """, unsafe_allow_html=True)
            if st.button("👁️ REVELAR CONCEITO", use_container_width=True, type="primary"):
                st.session_state['flipped'] = True
                st.rerun()
        else:
            # VERSO
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

    st.caption(f"Cartão {idx + 1} de {len(data)} | Base Total: 1379 cartões")