import streamlit as st 

st.title("Chai Maker App")

if st.button("Make Chai"):
    st.success("Your Chai is being brewed")
    
add_masala = st.checkbox("Add Masala")

if add_masala:
    st.write("Masala added to your chai")
    
tea_type = st.radio("Pick your chai base: ", ["Milk", "Water", "Almond Milk"])

st.write(f'Selected base: {tea_type}')

flavour = st.selectbox("Choose flavour: ", ["Adrak", "Kesar", "Tulsi"])
st.write(f'Selected flavour: {flavour}')

sugar = st.slider("Sugar Spoons", 0, 5, 2)
st.write(f"Selected sugar spoons: {sugar}")

cups = st.number_input("How many cups: ", min_value=1, max_value= 10, step= 1)

st.write(f"Number of cups: {cups}")

name = st.text_input("Enter Name")
if name:
    st.write(f"Welcome, {name}! Your chai is on the way")
    
dob = st.date_input("Select your date of birth")
st.write(f"Your date of birth is: {dob}")