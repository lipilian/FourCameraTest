#%%
import cv2
import threading
from colorama import Fore , Back, Style
import os 
import time
# %%
class camThread(threading.Thread):
    def __init__(self, previewName, camID):
        threading.Thread.__init__(self)
        self.previewName = previewName
        self.camID = camID
    def run(self):
        print("Starting " + self.previewName)
        camPreview(self.previewName, self.camID)

def camPreview(previewName, camID):
    cv2.namedWindow(previewName)
    cam = cv2.VideoCapture(camID)
    fps = cam.get(cv2.CAP_PROP_FPS)
    width = cam.get(cv2.CAP_PROP_FRAME_WIDTH)
    height = cam.get(cv2.CAP_PROP_FRAME_HEIGHT)
    print("intial {} frame rate {}, resolution {} X {}".format(previewName, fps, width, height ))
    # !! try to change the resolution of camera
    #cam.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
    #cam.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)
    cam.set(cv2.CAP_PROP_FPS,120)
    fps = cam.get(cv2.CAP_PROP_FPS)
    width = int(cam.get(cv2.CAP_PROP_FRAME_WIDTH))
    height = int(cam.get(cv2.CAP_PROP_FRAME_HEIGHT))
    print(Fore.RED + "Modified {} frame rate {}, resolution {} X {}".format(previewName, fps, width, height))
    
    # save the result to video file
    fourcc = cv2.VideoWriter_fourcc(*'XVID')
    saveVideo = cv2.VideoWriter(os.path.join('./Data', previewName + '.avi'),fourcc,fps
    ,(width,height))
    
    if cam.isOpened():
        rval, frame = cam.read()
    else:
        rval = False
    start = time.time()
    count = 0    
    while rval and count < 1200:
        rval, frame = cam.read()
        saveVideo.write(frame)
        #key = cv2.waitKey(20)
        #if key == 27:  # exit on ESC
        #    break
        #if cv2.getWindowProperty(previewName,cv2.WND_PROP_VISIBLE) < 1:        
        #    break 
    end = time.time()
    print("fps of {} is {}".format(previewName,1200/(end-start)))
    cam.release()
    saveVideo.release()
    if cv2.getWindowProperty(previewName,cv2.WND_PROP_VISIBLE) >= 1:    
        cv2.destroyWindow(previewName)
# %%
thread1 = camThread("Camera 1", 0)
thread2 = camThread("Camera 2", 1)
thread3 = camThread("Camera 3", 2)
thread4 = camThread("Camera 4", 3)
thread1.start()
thread2.start()
thread3.start()
thread4.start()

# %%
