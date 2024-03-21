import spacy
import nb_core_news_lg
import process_img as prim

# nlp = spacy.load("nb_core_news_lg")
# nlp = nb_core_news_lg.load()

# doc = nlp("Dette er en test.")

# print([(w.text, w.pos_) for w in doc])

im_path = "backend/data/receipts/IMG_2142.JPG"

# get the image name and add "_processed" to it
image_name = im_path.split("/")[-1]

image = prim.load_image(im_path)

img_new = prim.preprocess_for_ocr(image)

processed_im = prim.save_image("backend/data/processed_img/" + image_name, img_new)

# prim.display("backend/data/processed_img/" + image_name)

text = prim.get_text_from_image(img_new)
print(text)

prim.save_raw_text(text, image_name + ".txt")