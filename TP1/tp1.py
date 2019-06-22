import cv2
import face_recognition
import math 
import os

imagemModelo = cv2.imread('jimCarrey.jpg')
file = open("time_reporting.txt","w") 
if not os.path.exists('Match Frames'):
    os.makedirs('Match Frames')

face_encoding = face_recognition.face_encodings(imagemModelo)[0]

faces_conhecidas =  [face_encoding]
face_locations = []

vidcap = cv2.VideoCapture('Sonic.mp4')    # Leitura do vídeo original
fps = vidcap.get(cv2.CAP_PROP_FPS)

success,image = vidcap.read()
height, width, layers = image.shape
videoFace = cv2.VideoWriter('FaceVideo.avi', 0, fps, (width,height))
count = 0
minutes = 0
seconds = 0
success = True

while success:
    
    rgb_frame = image[:, :, ::-1]

    # Detecta todas as faces em uma imagem
    face_locations = face_recognition.face_locations(rgb_frame)
    face_encodings = face_recognition.face_encodings(rgb_frame, face_locations)
    
    face_names = []
    match = False
    for face_encoding in face_encodings:
       # Compara a imagem de busca com todos os rostos existentes na imagem atual.
       match = face_recognition.compare_faces(faces_conhecidas, face_encoding, tolerance=0.6)

    name = None
    if match:
        name = "Jim Carrey"
        face_names.append(name)
        
        # Aplica a label nas faces encontradas
        for (top, right, bottom, left), name in zip(face_locations, face_names):
            if not name:
               continue
        
        # Desenha um retangulo  em torno da face
        cv2.rectangle(image, (left, top), (right, bottom), (0, 127, 255), 2)
        
        # Inclui o nome da face identificada
        cv2.rectangle(image, (left, bottom - 25), (right, bottom), (0, 127, 255), cv2.FILLED)
        font = cv2.FONT_HERSHEY_DUPLEX
        cv2.putText(image, name, (left + 6, bottom - 6), font, 0.5, (255, 255, 255), 1)
        
        # Obtém o tempo do frame
        minutes = 0
        seconds = 0
        tempo_segundos = (vidcap.get(cv2.CAP_PROP_POS_MSEC) / 1000)
        if tempo_segundos >= 60:
            minutes = (tempo_segundos // 60)
            seconds = (tempo_segundos % 60)
        else:
            seconds = tempo_segundos
            
        file.write("Jim Carrey | tempo " + str(minutes) + ":" + str(math.trunc(seconds)) + " | frame " + str(count) + "\n")
        cv2.imwrite("Match Frames/%d.jpg" % count, image)
                       
    videoFace.write(image)
    success,image = vidcap.read()
    count += 1
            
file.close()    
videoFace.release()
