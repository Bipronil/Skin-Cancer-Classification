# -*- coding: utf-8 -*-
"""
Created on Wed Aug  2 10:23:14 2023

@author: bipronil
"""
'''classes={
    0:('akiec', 'actinic keratoses and intraepithelial carcinomae'),
         
    1:('bcc' , 'basal cell carcinoma'),
         
    2:('bkl', 'benign keratosis-like lesions'),
         
    3:('df', 'dermatofibroma'),
         
    4:('nv', ' melanocytic nevi'),
         
    5:('vasc', ' pyogenic granulomas and hemorrhage'),
         
    6:('mel', 'melanoma'),
}'''


#Import necessary libraries
from flask import Flask, render_template, request
import PIL 
import numpy as np
import os

 

from keras.models import load_model
 
#load model
model =load_model("model/best_model_1.h5")
 
print('@@ Model loaded')
 
 
def pred_skin_dieas(skin_img):
   
  image=PIL.Image.open(skin_img)
  print("@@ Got Image for prediction")
   
  
  image=image.resize((28,28))
  
  img=np.array(image).reshape(-1,28,28,3)
   
  
  result=model.predict(img)
  print('@@ Raw result = ', result)
  
  result=result.tolist()
   
  
  max_prob=max(result[0])

  class_ind=result[0].index(max_prob)
  print('@@predicted class = ' ,class_ind)
 
  
  if class_ind == 0:
      return "akiec", 'akiec.html' 
  elif class_ind == 1:
      return 'bcc', 'bcc.html' 
  elif class_ind == 2:
      return 'bkl', 'bkl.html'  
  elif class_ind == 3:
      return "df", 'df.html'
  elif class_ind == 4:
      return "nv" , 'nv.html'
  elif class_ind == 5:
      return "vasc" , 'vasc.html'
  elif class_ind == 6: 
      return "mel" , 'mel.html'
  else:
      return "healthy" , 'healthy.html'
 
 
#------------>>pred_skin_dieas<<--end
     
 
# Create flask instance
app = Flask(__name__)
 
# render index.html page
@app.route("/", methods=['GET', 'POST'])
def home():
        return render_template('home.html')
     
  
# get input image from client then predict class and render respective .html page for solution
@app.route("/predict", methods = ['GET','POST'])
def predict():
     if request.method == 'POST':
        file = request.files['image'] # fet input
        filename = file.filename        
        print("@@ Input posted = ", filename)
         
        file_path = os.path.join('static/user uploaded', filename)
        file.save(file_path)
 
        print("@@ Predicting class......")
        class_ind, output_page = pred_skin_dieas(skin_img=file_path)
               
        return render_template(output_page, pred_output = class_ind, user_image = file_path)
     
# For local system & cloud
if __name__ == "__main__":
    app.run(threaded=False) 