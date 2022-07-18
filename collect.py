import mss
import time
import cv2
import numpy as np
from PIL import Image


start_time = time.time()

#screenshot location
mon = {'top': 40, 'left': 60, 'width': 1800, 'height': 1000}

duration = np.empty((1,))
count =0

with mss.mss() as sct:
    while True:
        count += 1
        last_time = time.time()
        im = sct.grab(mon)

        #convert mss image to PIL image, BRG OR RGB
        img = Image.frombytes('RGB', im.size, im.bgra, 'raw', 'BGRX')
        
        #img = img.convert('RGB', palette= Image.ADAPTIVE, colors =1)

        #less efficient conversion
        #img = Image.frombytes('RGB', im.size, im.rgb)

        #compress PIL image to (X,Y)
        img = img.resize((900,500))
        
        
        #sct.compression_level = 9

        wid, hgt = img.size

        duration = np.append(duration, time.time()*1000-last_time*1000)
        #print('The loop took: {:.0f}'.format(time.time()*1000-last_time*1000) + ' ms')

        cv2.imshow('test', np.array(img))
        
        #why are blue and red opposite of the live output
        img.save("data/" + str(count) + '.png')
        time.sleep(5)


        #break cycle w/ user input 'q'
        if cv2.waitKey(25) & 0xFF == ord('q'):
            cv2.destroyAllWindows()
            break
    

    print(str(wid) + "x" + str(hgt))
    print('Average time for each image: {:.0f}'.format(np.mean(duration)) + 'ms')