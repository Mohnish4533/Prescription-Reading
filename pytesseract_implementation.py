import pytesseract
import argparse 
import cv2 
  
# pass arguements
ap = argparse.ArgumentParser() 
  
ap.add_argument("-i", "--image", 
                required=True, 
                help="path to input image to be OCR'd") 
ap.add_argument("-c", "--min-conf", 
                type=int, default=0, 
                help="minimum confidence value to filter weak text detection") 
args = vars(ap.parse_args()) 
  
# use pytesseract on image
images = cv2.imread(args["image"]) 
rgb = cv2.cvtColor(images, cv2.COLOR_BGR2RGB) 
results = pytesseract.image_to_data(rgb, output_type=pytesseract.Output.DICT) 
  
# Loop over each of the individual text localizations 
for i in range(0, len(results["text"])): 
      
    # Extract bounding boxes
    x = results["left"][i] 
    y = results["top"][i] 
    w = results["width"][i] 
    h = results["height"][i] 
      
    # Get text and confidence
    text = results["text"][i] 
    conf = int(results["conf"][i]) 
      
    # filter out weak confidence text localizations 
    if conf > args["min_conf"]: 
          
        print("Confidence: {}".format(conf)) 
        print("Text: {}".format(text), end="\n\n") 
          
        # We then strip out non-ASCII text so we can 
        # draw the text on the image We will be using 
        # OpenCV, then draw a bounding box around the 
        # text along with the text itself 
        text = "".join(text).strip() 
        cv2.rectangle(images, 
                      (x, y), 
                      (x + 1, y + h), 
                      (0, 0, 255), 1) 
        # cv2.putText(images, 
        #             text, 
        #             (x, y - 10),  
        #             cv2.FONT_HERSHEY_SIMPLEX, 
        #             1.2, (0, 255, 255), 3) 
          
# After all, we will show the output image 
cv2.imshow("Image", images) 
cv2.imwrite("1.jpg", images)
cv2.waitKey(0) 