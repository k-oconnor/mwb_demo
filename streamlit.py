import streamlit as st
from query import get_recs
from PIL import Image

logo = Image.open('logo.jpg')
bee = Image.open('bee.png')

def main():
    # streamlit code
    # create main page with YouTorial logo
    st.set_page_config(layout="wide")
    st.image(logo)
    st.header('Knowledge Graph Search Demo Environment')
    st.markdown('#')
    # create sidebar with link to Github repo

    # create user search bar and return video ids from database
    input_query = st.text_input('Enter search:', value='')
    query_ids = get_recs(input_query)

    st.markdown('#')
    st.markdown('#')
    st.subheader(
        'We have retreived the following recommendations from the graph:')

    # embed recommended videos in grid
    
    if len(query_ids) > 0:
        for rec in query_ids:
            st.text(rec)
    else:
        st.text("Enter a query")

    st.image(bee)

# to run: streamlit run gui/streamer.py
if __name__ == "__main__":
    main()