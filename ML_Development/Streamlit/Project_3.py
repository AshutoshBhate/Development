import streamlit as st 

st.title("Chai Taste Poll")

col1, col2 = st.columns(2)

with col1:
    st.header("Masala Chai")
    st.image("https://foodandroad.com/wp-content/uploads/2021/04/masala-chai-indian-drink-3-500x500.jpg", width= 200)
    vote1 = st.button("Vote Masala Chai")

with col2:
    st.header("Adrak Chai")
    st.image("https://www.sharmispassions.com/wp-content/uploads/2019/07/cutting-chai4.jpg", width= 200)
    vote2 = st.button("Vote Adrak Chai")
    
if vote1:
    st.success("Thanks for voting Masala Chai")
elif vote2:
    st.success("Thanks for voting Adrak Chai")
    

name = st.sidebar.text_input("Enter your name")
tea = st.sidebar.selectbox("Choose you chai: ", ["Masala", "Kesar", "Adrak"])

st.write(f"Welcome {name} and your {tea} chai is getting ready")

with st.expander ("Show chai making instructions"):
    st.write(""" 
             1. Boil water with tea leaves
             2. Add milk with spices
             3. Serve hot
             """)
    
st.markdown('### Welcome to Chai App')
st.markdown('> Blockquote')