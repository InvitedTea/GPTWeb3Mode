from streamlit_chat import message
import streamlit as st
import pandas as pd
import numpy as np
from openai.error import OpenAIError
from wallet_connect import wallet_connect

from utils import (
    parse_txt,
    parse_csv,
    search_docs,
    embed_docs,
    text_to_docs,
    get_answer,
    parse_any,
    get_sources,
    wrap_text_in_html,
)

st.title('WEB3 ChatGPT with Updated Knowledge Base')

def clear_submit():
    st.session_state["submit"] = False

DATE_COLUMN = 'date/time'
DATA_URL = ('sample.txt')
st.session_state["OPENAI_API_KEY"] = 'YOUR KEY'

def parse():
    doc = parse_txt(DATA_URL)
    text = text_to_docs(doc)
    index = embed_docs(text)
    return index



index = parse()



### ACCESS CONTROL WITH EXISTING NFTS AND TOKENS

#### choose which token you want to use for access control and uncomment the appropriate line
# login_button_erc1155 = wallet_connect(label="login", key="login", message="Login with ERC1155", auth_token_contract_address="0x68085453B798adf9C09AD8861e0F0da96B908d81", chain_name="polygon", contract_type="ERC1155", num_tokens="0")
# login_button_erc20 = wallet_connect(label="login", key="login", message="Login with ERC20", auth_token_contract_address="0x967da4048cD07aB37855c090aAF366e4ce1b9F48", chain_name="ethereum", contract_type="ERC20", num_tokens="20")


### ACCESS CONTROL WITH CUSTOM ALGOVERA NFTS

#### uncomment this and run the app to initialize a new token (take note of the returned tokenId)
login_button_erc721 = wallet_connect(label="login", key="login", message="Connect Your Wallet to Validate Your NFT badge", auth_token_contract_address="0x967da4048cD07aB37855c090aAF366e4ce1b9F48", chain_name="base", contract_type="ERC721", num_tokens="0")

st.write('This Demo Powered By ChatGPT@OPENAI')
st.write('Bought you by InvitedTea')

if 'generated' not in st.session_state:
    st.session_state['generated'] = []

if 'past' not in st.session_state:
    st.session_state['past'] = []

def get_text():
    st.header("Ask me something about web3:")
    input_text = st.text_area("You:", on_change=clear_submit)
    return input_text


user_input = get_text()
button = st.button("Submit")

if button or st.session_state.get("submit"):
    if not user_input:
        st.error("Please enter a question!")
    else:
        st.session_state["submit"] = True
        sources = search_docs(index, user_input)
        try:
            answer = get_answer(sources, user_input)
            st.session_state.past.append(user_input)
            st.session_state.generated.append(answer["output_text"].split("SOURCES: ")[0])
            st.button('Mint this knowledge as new NFT token')

        except OpenAIError as e:
            st.error(e._message)
        if st.session_state['generated']:
            for i in range(len(st.session_state['generated'])-1, -1, -1):
                message(st.session_state["generated"][i], key=str(i))
                message(st.session_state['past'][i], is_user=True, key=str(i) + '_user')
