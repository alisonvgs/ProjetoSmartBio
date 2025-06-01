import tensorflow as tf

@tf.keras.utils.register_keras_serializable()
def carregar_modelo():
    return tf.keras.models.load_model("resNet.keras")

def predizer_imagem(arq):
    classes = ['aerosol_cans', 'aluminum_food_cans', 'aluminum_soda_cans', 'cardboard_boxes', 'cardboard_packaging',
               'clothing', 'coffee_grounds', 'disposable_plastic_cutlery', 'eggshells', 'food_waste',
               'glass_beverage_bottles', 'glass_cosmetic_containers', 'glass_food_jars', 'magazines', 'newspaper',
               'office_paper', 'paper_cups', 'plastic_cup_lids', 'plastic_detergent_bottles', 'plastic_food_containers',
               'plastic_shopping_bags', 'plastic_soda_bottles', 'plastic_straws', 'plastic_trash_bags',
               'plastic_water_bottles', 'shoes', 'steel_food_cans', 'styrofoam_cups', 'styrofoam_food_containers',
               'tea_bags']

    model = carregar_modelo()
    img = tf.keras.preprocessing.image.load_img(arq, target_size=(224, 224))
    img_array = tf.keras.preprocessing.image.img_to_array(img)
    img_array = tf.expand_dims(img_array, axis=0)
    img_array = tf.keras.applications.resnet50.preprocess_input(img_array)

    preds = model.predict(img_array)
    predicted_label_index = tf.argmax(preds, axis=1)[0].numpy()
    return classes[predicted_label_index]
