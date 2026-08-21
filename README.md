# ⚡ EletroAgent - Assistente Inteligente de Esquemas e Painéis Elétricos

O **EletroAgent** é um agente de Inteligência Artificial multimodal projetado para auxiliar eletricistas, estudantes e entusiastas de automação a interpretar diagramas elétricos, organizar a disposição de componentes em trilhos DIN e realizar dimensionamentos de condutores e proteções segundo a norma **NBR 5410**.

---

## 🚀 Funcionalidades

- 📷 **Análise Multimodal:** Upload de imagens de diagramas e quadros para identificação e explicação de componentes.
- ⚡ **Dimensionamento Técnico Automatizado:** Cálculo de corrente nominal e recomendação de bitola mínima de cabo e disjuntor termomagnético.
- 💬 **Chat Interativo:** Interface conversacional amigável desenvolvida em Streamlit com histórico de mensagens.
- 🛡️ **Foco em Segurança:** Diretrizes e alertas de segurança baseados na **NR-10**.

---

## 🛠️ Tecnologias Utilizadas

- **Python 3.12+**
- **Google Gemini API (gemini-3.6-flash)** - LLM Multimodal e Function Calling / Tools
- **Streamlit** - Interface web interativa e responsiva
- **Pillow (PIL)** - Processamento de imagens

---

## 💻 Como Rodar o Projeto Localmente

1. Clone o repositório:
   `ash
   git clone https://github.com/SEU_USUARIO/eletro-agent.git
   cd eletro-agent
   `

2. Crie e ative um ambiente virtual:
   `ash
   python -m venv venv
   # No Windows:
   .\venv\Scripts\Activate.ps1
   # No Linux/Mac:
   source venv/bin/activate
   `

3. Instale as dependências:
   `ash
   pip install -r requirements.txt
   `

4. Execute a aplicação:
   `ash
   streamlit run app.py
   `

---

## ⚠️ Aviso de Segurança
Este assistente possui finalidade educacional e consultiva. Intervenções em quadros de distribuição e instalações elétricas reais devem seguir as normas de segurança (NR-10) e ser validadas por profissionais habilitados.
