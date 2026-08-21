import streamlit as st
import os
from PIL import Image
from google import genai
from google.genai import types

st.set_page_config(
    page_title="EletroAgent - Assistente de Painéis Elétricos",
    page_icon="⚡",
    layout="wide"
)

def dimensionar_circuito_monofasico(potencia_watts: float, tensao_volts: float = 220.0) -> str:
    """Calcula a corrente e sugere bitola de cabo e disjuntor para circuito monofásico residencial/comercial conforme NBR 5410."""
    if tensao_volts <= 0:
        return "Erro: Tensão deve ser maior que zero."
    
    corrente = potencia_watts / tensao_volts
    
    if corrente <= 10:
        cabo = "1.5 mm²"
        disjuntor = "10 A"
    elif corrente <= 15:
        cabo = "2.5 mm²"
        disjuntor = "16 A"
    elif corrente <= 21:
        cabo = "4.0 mm²"
        disjuntor = "20 A ou 25 A"
    elif corrente <= 28:
        cabo = "6.0 mm²"
        disjuntor = "32 A"
    elif corrente <= 36:
        cabo = "10.0 mm²"
        disjuntor = "40 A"
    else:
        cabo = "Acima de 10.0 mm² (requer cálculo detalhado de queda de tensão e agrupamento)"
        disjuntor = "A dimensionar conforme projeto"

    return (
        f"⚡ Resultado do Dimensionamento Técnico:\n"
        f"- Corrente nominal: {corrente:.2f} A\n"
        f"- Bitola de cabo de cobre mínima sugerida: {cabo}\n"
        f"- Disjuntor termomagnético recomendado: {disjuntor}\n"
        f"*(Valores de referência NBR 5410 - Método B1)*"
    )

SYSTEM_PROMPT = """
Você é o EletroAgent, um assistente especialista em engenharia elétrica, montagem de painéis, diagramas unifilares/multifilares e normas ABNT (NBR 5410, NR-10).

Suas principais funções:
1. Interpretar esquemas elétricos e fotos de painéis/componentes enviados pelo usuário.
2. Explicar passo a passo como montar, distribuir e organizar quadros elétricos (Disjuntor Geral -> DPS -> IDR -> Disjuntores dos Circuitos).
3. Utilizar a ferramenta de dimensionamento para calcular correntes e sugerir bitolas de cabo e disjuntores quando o usuário informar potência e tensão.
4. Manter uma postura didática, encorajadora e focada em boas práticas e segurança.

Regras de Segurança:
- Sempre oriente o usuário a desenergizar os circuitos e utilizar multímetro/voltímetro para certificar-se da ausência de tensão antes de qualquer contato físico.
- Lembre que intervenções em quadros de alta potência exigem profissionais habilitados.
"""

# Verificar se a chave foi configurada nos Secrets ou no Ambiente
secret_key = st.secrets.get("GEMINI_API_KEY") if hasattr(st, "secrets") and "GEMINI_API_KEY" in st.secrets else os.environ.get("GEMINI_API_KEY")

with st.sidebar:
    st.title("⚡ EletroAgent")
    st.caption("Assistente Inteligente de Esquemas e Painéis Elétricos")
    
    if secret_key:
        st.success("🔒 Chave de API ativa no servidor!")
        api_key_input = secret_key
    else:
        api_key_input = st.text_input(
            "Gemini API Key:",
            type="password",
            placeholder="Cole sua chave aqui...",
            help="Insira sua chave da API do Google Gemini"
        )
    
    st.divider()
    st.subheader("📋 Regras Rápidas de Segurança")
    st.markdown("""
    - 🔴 **Desenergize** a rede antes de mexer.
    - ⚡ **Teste a tensão** com multímetro.
    - 🛡️ Use **DPS** contra surtos e **IDR** contra choques.
    - 🏷️ Identifique todos os circuitos com anilhas e plaquetas.
    """)
    
    if st.button("🗑️ Limpar Conversa"):
        st.session_state.messages = []
        st.rerun()

if "messages" not in st.session_state:
    st.session_state.messages = [
        {
            "role": "assistant",
            "content": "Olá! Eu sou o **EletroAgent** ⚡. Posso te ajudar a interpretar diagramas elétricos, dimensionar condutores, organizar o trilho DIN do seu painel e tirar dúvidas sobre componentes. Como posso te ajudar hoje?"
        }
    ]

for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])
        if "image" in msg:
            st.image(msg["image"], caption="Imagem enviada", use_container_width=True)

uploaded_file = st.file_uploader("📷 Envie a foto de um esquema elétrico ou painel (opcional):", type=["jpg", "jpeg", "png"])
uploaded_image = None

if uploaded_file:
    uploaded_image = Image.open(uploaded_file)
    st.image(uploaded_image, caption="Prévia do esquema elétrico carregado", width=400)

user_prompt = st.chat_input("Digite sua dúvida sobre o painel elétrico ou esquema...")

if user_prompt:
    if not api_key_input:
        st.error("Por favor, insira sua chave da API do Gemini na barra lateral para continuar.")
        st.stop()

    user_msg_data = {"role": "user", "content": user_prompt}
    if uploaded_image:
        user_msg_data["image"] = uploaded_image
    
    st.session_state.messages.append(user_msg_data)
    
    with st.chat_message("user"):
        st.markdown(user_prompt)
        if uploaded_image:
            st.image(uploaded_image, caption="Esquema enviado", use_container_width=True)

    with st.chat_message("assistant"):
        with st.spinner("Analisando esquema e calculando parâmetros..."):
            try:
                client = genai.Client(api_key=api_key_input)
                
                contents = []
                if uploaded_image:
                    contents.append(uploaded_image)
                contents.append(user_prompt)
                
                config = types.GenerateContentConfig(
                    system_instruction=SYSTEM_PROMPT,
                    tools=[dimensionar_circuito_monofasico],
                    temperature=0.3
                )
                
                response = client.models.generate_content(
                    model="gemini-3.6-flash",
                    contents=contents,
                    config=config
                )
                
                agent_reply = response.text
                st.markdown(agent_reply)
                
                st.session_state.messages.append({
                    "role": "assistant",
                    "content": agent_reply
                })
            except Exception as e:
                st.error(f"Erro ao processar com o agente: {e}")
