# 🏆 Concurso Mastery Pro - ConPrev Assessoria

Este é um ecossistema de repetição espaçada desenvolvido para o domínio de conteúdos de alto nível para concursos fiscais e de controle. O aplicativo utiliza a biblioteca Streamlit para transformar uma base unificada de dados em uma interface de flashcards interativa.

## 📊 Estrutura de Dados
O aplicativo consome uma base de **1.379 cartões** unificados, cobrindo as seguintes áreas:
* [cite_start]**Auditoria Fiscal**: Foco em omissão de receita e cruzamento de dados (EFD/ECD)[cite: 1, 7, 11].
* [cite_start]**AFO**: Ciclo orçamentário (PPA, LDO, LOA) e estágios da despesa[cite: 167, 171, 179].
* [cite_start]**Administração Pública**: Evolução (Patrimonialismo ao Gerencialismo) e Accountability[cite: 74, 78, 102].
* [cite_start]**Auditoria Governamental**: Normas ISSAI e controle externo[cite: 134, 148].
* **Business English**: Vocabulário executivo e termos de Tax Compliance.

## 🛠️ Como Atualizar o Banco de Dados
Para adicionar novas "listas" ou atualizar os cartões existentes:
1. Adicione o novo arquivo `.docx` na sua pasta local.
2. Execute o script `unificar_listas.py` para gerar um novo `data_unificada.json`.
3. Faça o upload do novo `data_unificada.json` para este repositório no GitHub.
4. O Streamlit Cloud detectará a mudança e atualizará o app automaticamente.

## 🔒 Segurança
O acesso é restrito via tela de login. As credenciais são gerenciadas através dos **Secrets** do Streamlit Cloud para garantir a proteção da propriedade intelectual da ConPrev Assessoria.

---
*Desenvolvido por Samuel Almeida*
