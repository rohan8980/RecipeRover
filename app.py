import os
import pickle
import streamlit as st
from sklearn.metrics.pairwise import cosine_similarity
import gdown


# Load preprocessed Pickle (data and model) from Google Drive
# Caching: https://docs.streamlit.io/develop/concepts/architecture/caching
@st.cache_resource(ttl = 60*60 *24 *7, show_spinner="Fetching model from cloud...")
def load_model_from_google_drive(fileid, save_path):
    # Download and Save Model
    pickle_url = f'https://drive.google.com/uc?id={fileid}'
    gdown.download(pickle_url, save_path, quiet=True)
    # Load and Return Model
    try:
        with open(save_path, "rb") as f:
            df, tfidf_matrix = pickle.load(f)
    except Exception as e:
        st.error(f"Error loading the model: {e}")
    return df, tfidf_matrix

save_path = 'model_pickle.pkl'
google_drive_file_id = st.secrets["GOOGLE_DRIVE_FILE_ID"]
df, tfidf_matrix = load_model_from_google_drive(google_drive_file_id, save_path)

# # Local Save and load
# save_path = 'model_pickle.pkl'
# model_path = os.path.join(os.getcwd(), 'Model', save_path)
# with open(model_path, "rb") as f:
#     df, tfidf_matrix = pickle.load(f)

# Calculating Cosine Similarity
@st.cache_resource(ttl = 60*60 *24 *7, show_spinner=False)      # @st.cache_data(ttl = 60*60 *24 *7, max_entries=2)
def calculate_cosine_similarity(_tfidf_matrix):
    return cosine_similarity(tfidf_matrix, tfidf_matrix)
cosine_sim = calculate_cosine_similarity(tfidf_matrix)


# Function to get recommendations based on recipe name
def get_recommendations(recipe_name, n_recommendations=6, cosine_sim=cosine_sim):
    total_pages = 5
    idx = df[df['Recipe Name'] == recipe_name].index[0]
    sim_scores = list(enumerate(cosine_sim[idx]))
    sim_scores = sorted(sim_scores, key=lambda x: x[1], reverse=True)
    sim_scores = sim_scores[1:(n_recommendations*total_pages)+1] 
    recipe_indices = [i[0] for i in sim_scores]
    return recipe_indices

# Function to fetch recipe details by index
def get_recipe_details(index):
    recipe_name = df.loc[index, 'Recipe Name']
    image_url = df.loc[index, 'Image URL']
    recipe_url = df.loc[index, 'Recipe URL']
    return recipe_name, image_url, recipe_url


# Initialize global variables
n_recommendations = 6
n_columns = 3

# Initialize the state variables
if "num_recommendations_displayed" not in st.session_state:
    st.session_state.num_recommendations_displayed = n_recommendations
if "recommendations_displayed" not in st.session_state:
    st.session_state.recommendations_displayed = False
if "selected_recipe" not in st.session_state:
    st.session_state.selected_recipe = ''
if "first_load_more" not in st.session_state:
    st.session_state.first_load_more = False

# Streamlit UI
st.title("🍵🧆🍲 Recipe Rover 🥘🥣🥧")
st.write(f'<p style="font-size: large">Recipe Recommendation System</p>', unsafe_allow_html=True)
st.sidebar.title("Selected Recipe Details")
sidebar_recipe_name = st.sidebar.empty()
sidebar_recipe_image = st.sidebar.empty()

# Text input box for recipe search and selection
selected_recipe_name = st.selectbox("Select Recipe", [""] + df['Recipe Name'].tolist())    

# Reset num_recommendations_displayed if a new recipe is selected
if st.session_state.get('selected_recipe', '') != selected_recipe_name:
    st.session_state.num_recommendations_displayed = n_recommendations
    st.session_state.selected_recipe = selected_recipe_name
    st.session_state.first_load_more = False

# Show details of the selected recipe
if selected_recipe_name:
    selected_recipe_idx = df[df['Recipe Name'] == selected_recipe_name].index[0]
    recipe_name, image_url, recipe_url = get_recipe_details(selected_recipe_idx)
    sidebar_recipe_name.write(f'<p style="font-size: large">{recipe_name}</p>', unsafe_allow_html=True)
    sidebar_recipe_image.write(f'<a href="{recipe_url}" target="_blank"><img src="{image_url}" alt="{recipe_name}"></a>', unsafe_allow_html=True)
# Till no recipe is selected
else: 
    st.sidebar.write('')
    st.sidebar.write(" Select a recipe ☛")


# Fetch and show recommendations
if st.session_state.selected_recipe and st.button("Get Recommendations") and selected_recipe_name != "":
    st.session_state.recommendations_displayed = True
    st.session_state.num_recommendations_displayed = n_recommendations

# If recommendations have been displayed
if st.session_state.recommendations_displayed:
    # Get recommendations
    num_recommendations = st.session_state.num_recommendations_displayed
    recommended_recipe_indices = get_recommendations(selected_recipe_name, num_recommendations)

    # Show details of the recommended Recipes
    st.subheader("Recommended Recipes:")
    num_rows = (num_recommendations - 1) // n_columns + 1
    for row in range(num_rows):
        cols = st.columns(n_columns)
        for col_index, col in enumerate(cols):
            recipe_index = row * n_columns + col_index
            if recipe_index < num_recommendations:
                recipe_name, image_url, recipe_url = get_recipe_details(recommended_recipe_indices[recipe_index])
                col.write(f'<p style="font-size: large">{recipe_name}</p>', unsafe_allow_html=True)
                col.write(f'<a href="{recipe_url}" target="_blank"><img src="{image_url}" alt="{recipe_name}" width="200"></a>', unsafe_allow_html=True)
            else:
                col.write("")

    # Update num_recommendations_displayed for initial load more press
    if not st.session_state.first_load_more:
        st.session_state.num_recommendations_displayed += n_recommendations
        st.session_state.first_load_more = True
    

# Add a button to load more recommendations only if recommendations have been initially displayed
if st.session_state.recommendations_displayed and st.button("Load More"):
    st.session_state.num_recommendations_displayed += n_recommendations
    # st.write(f'rec disp:"{st.session_state.recommendations_displayed}" #Rec:" {st.session_state.num_recommendations_displayed}')