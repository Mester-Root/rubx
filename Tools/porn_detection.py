#!/bin/python

import cv2, joblib, numpy as np
#from sklearn.externals import * 

def detection(image: str) -> tuple:
    
    clf = joblib.load('porn_classifier.pkl')
    img = cv2.imread(image)
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    resized_image = cv2.resize(gray, (200, 200))
    flattened_image = resized_image.flatten()  
    
    if (clf.predict([flattened_image]) == 'porn'):
        return True, 'this image contains porn content'
    else:  
        return False, 'this image does not contain porn content'

print(detection('*.jpg'))
