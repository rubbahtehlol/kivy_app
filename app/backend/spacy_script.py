import spacy
import nb_core_news_lg
import process_img as prim

# nlp = spacy.load("nb_core_news_lg")
# nlp = nb_core_news_lg.load()

# doc = nlp("Dette er en test.")

# print([(w.text, w.pos_) for w in doc])

im_path = "backend/data/receipts/IMG_2159.JPG"

# get the image name and add "_processed" to it
image_name = im_path.split("/")[-1]
name = image_name.split(".")[0]

image = prim.load_image(im_path)

img_new = prim.preprocess_for_ocr(image)

processed_im = prim.save_image("backend/data/processed_img/" + image_name, img_new)

no_borders = prim.remove_borders(img_new)
prim.save_image("backend/data/test/no_borders.jpg", no_borders)

desweked = prim.deskew_image(img_new)
prim.save_image("backend/data/test/deskewed.jpg", desweked)

# prim.display("backend/data/processed_img/" + image_name)

text_desweked = prim.get_text_from_image(desweked)
print(text_desweked)

prim.save_raw_text(text_desweked, name + ".txt")

# text_no_borders = prim.get_text_from_image(no_borders)
# print(text_no_borders)

# prim.save_raw_text(text_no_borders, name + "_nb.txt")

# text = prim.get_text_from_image(img_new)
# print(text)

# prim.save_raw_text(text, name + ".txt")