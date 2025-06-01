import streamlit as st
import tensorflow as tf
import requests

st.title("Teste")

def predicao(arq):

    classes = ['aerosol_cans', 'aluminum_food_cans', 'aluminum_soda_cans', 'cardboard_boxes', 'cardboard_packaging', 'clothing', 'coffee_grounds', 'disposable_plastic_cutlery', 'eggshells', 'food_waste', 'glass_beverage_bottles', 'glass_cosmetic_containers', 'glass_food_jars', 'magazines', 'newspaper', 'office_paper', 'paper_cups', 'plastic_cup_lids', 'plastic_detergent_bottles', 'plastic_food_containers', 'plastic_shopping_bags', 'plastic_soda_bottles', 'plastic_straws', 'plastic_trash_bags', 'plastic_water_bottles', 'shoes', 'steel_food_cans', 'styrofoam_cups', 'styrofoam_food_containers', 'tea_bags']

    model = tf.keras.models.load_model("C:\\ProjetoSmartBio\\resNet.keras")
    img = tf.keras.preprocessing.image.load_img(arq, target_size=(224, 224))
    img_array = tf.keras.preprocessing.image.img_to_array(img)
    img_array = tf.expand_dims(img_array, axis=0)
    img_array = tf.keras.applications.resnet50.preprocess_input(img_array)

    preds = model.predict(img_array)
    predicted_class_index = tf.argmax(preds, axis=1)
    predicted_label_index = predicted_class_index[0].numpy()

    return classes[predicted_label_index]


uploaded_files = st.file_uploader("Insira um ou mais arquivos",
                       accept_multiple_files=True,
                       type=["png", "jpg", "jpeg", "gif", "bmp", "webp"]
                       )

if uploaded_files:
    for uploaded_file in uploaded_files:
        resultado = predicao(uploaded_file)
        st.image(uploaded_file, caption = "Predição: " + resultado)
        prompt = f"O objeto detectado é um {resultado}. Você é um especialista em energia renovável e biodigestores. Avalie se esse objeto é apropriado para ser utilizado em um biodigestor anaeróbico. Se for adequado, forneça: Uma breve justificativa da adequação. A estimativa da energia que pode ser gerada (em kWh ou m³ de biogás), considerando uma quantidade padrão (ex: 1 kg). Se não for adequado, apresente um alerta explicando por que não deve ser colocado no biodigestor (por exemplo: presença de metais, plásticos, objetos não biodegradáveis, risco de contaminação, etc). Responda de forma objetiva e clara, com foco em aplicações práticas para gestão de resíduos e geração de energia. Responda em pt-br."
        response = requests.post(
            "http://localhost:11434/api/generate",
            json={
                "model": "llama3",
                "prompt": prompt,
                "stream": False
            }
        )
        st.write(response.json()["response"])
