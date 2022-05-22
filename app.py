from flask import Flask, render_template, request
from keras.models import load_model
from keras.preprocessing import image
import tensorflow as tf
import numpy as np


def create_app():

	app = Flask(__name__)
	dic = {0 : 'hap', 1 : 'sui'}
	model = load_model('final_model.h5')
	model.make_predict_function()
	def predict_label(img_path):
		input = tf.keras.preprocessing.image.load_img(img_path, target_size=(224,224))
		i = tf.keras.preprocessing.image.img_to_array(input)/255.0
		i = i.reshape(1, 224,224,3)
		p = model.predict(i)
		print(p)
		labels = np.array(p)
		labels[labels>=0.5]=1
		labels[labels<0.5]=0
		print(labels)
		final = np.array(labels)
		if final[0][0] == 1:
			return "Suicidal"
		else:
			return "Non Suicidal"
	@app.route("/", methods=['GET', 'POST'])
	def main():
		return render_template("index.html")
	@app.route("/about")
	def about_page():
		return "Suicidal Image classification"
	@app.route("/submit", methods = ['GET', 'POST'])
	def get_output():
		if request.method == 'POST':
			img = request.files['my_image']
			img_path = "static/" + img.filename	
			img.save(img_path)
			predict_final = predict_label(img_path)
		return render_template("index.html", prediction = predict_final, img_path = img_path)
	return app
if __name__ =='__main__':
	app=create_app()
	app.run(debug = True)








