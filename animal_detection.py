import tensorflow as tf
import cv2
import numpy as np
from includes import message
from time import sleep

interpreter = tf.lite.Interpreter(model_path="model.tflite")
interpreter.allocate_tensors()

input_details = interpreter.get_input_details()
output_details = interpreter.get_output_details()

current = None
class_labels = ['Cow', 'Deer', 'Mongoose', 'Nothing', 'Sheep', 'Elephant', 'WildPork']

confidence_history = []

def classify_frame(frame):
    img = cv2.resize(frame, (input_details[0]['shape'][1], input_details[0]['shape'][2]))
    img = np.expand_dims(img, axis=0)
    img = img.astype(np.uint8)

    interpreter.set_tensor(input_details[0]['index'], img)

    interpreter.invoke()

    output_data = interpreter.get_tensor(output_details[0]['index'])

    class_idx = np.argmax(output_data[0])

    class_label = class_labels[class_idx]

    confidence = max(output_data[0])

    confidence_history.append(confidence)

    if len(confidence_history) > 10:
        confidence_history.pop(0)

    confidence_avg = sum(confidence_history) / len(confidence_history)

    return class_label, confidence_avg

cap = cv2.VideoCapture('http://192.168.47.24:8080/video')

while True:
    ret, frame = cap.read()
    if not ret:
        break

    class_label, confidence = classify_frame(frame)

    if confidence > 200 and class_label != 'Nothing' and current!=class_label and class_label != 'Sheep':
        current = class_label
        print("_______{}:{}_______".format(current, confidence))
        message.make_call('+919629930357', current)
        sleep(10)

        
    # cv2.putText(frame, f'{class_label} {confidence:.2f}', (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)

    cv2.imshow('Frame', frame)

    if cv2.waitKey(1) == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
