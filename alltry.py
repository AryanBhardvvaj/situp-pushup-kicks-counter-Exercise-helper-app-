import cv2
import mediapipe as md

md_drawing=md.solutions.drawing_utils
md_drawing_styles=md.solutions.drawing_styles
md_pose=md.solutions.pose

pushupcount=0
situpcount=0
rkcount=0
lkcount=0
position_p=None
position_s=None
position_rk=None
position_lk=None

#vedio capture function 0 means there is no
# input till now we will have input from camera
cap=cv2.VideoCapture(0) 
with md_pose.Pose(
    min_detection_confidence=0.6,
    min_tracking_confidence=0.6)as pose:
    # while loop for the time the camera is running
    while cap.isOpened():
        #success will tel if the input is coming or not
        success,image=cap.read()
        if not success:
            print("no input found error!!")
            break
        #mediapipe reads in rgb form this is to convert that to an image
        image=cv2.cvtColor(cv2.flip(image,1),cv2.COLOR_BGR2RGB)
        result=pose.process(image)
        #the following list contains all info about
        #the pose cordidates present in mediapipe
        imlist=[]
        #if there is any body in the vedio : true/false
        if result.pose_landmarks:
            md_drawing.draw_landmarks(
                image,result.pose_landmarks,md_pose.POSE_CONNECTIONS)
            for id,im in enumerate(result.pose_landmarks.landmark):#we will get 2 vals from this
               #this willl create long list of landmarks then we will iterate those values then we will get
               #2 valuse id and and the landmarks that are x,y that are the hight and width of the vedio
                h,w,_=image.shape#to get shape and size of our vedio
                X,Y=int(im.x*w),int(im.y*h)#then we multiply the 2 h n w with the ratio to get exact cordinates of the subject
                                        #append all this data in im list variable
                                        #finally we got all 32 pts of the mediapipe 
                imlist.append([id,X,Y])
        imgdisp = cv2.cvtColor(image,cv2.COLOR_RGB2BGR)
        if len (imlist)!=0:
            if(imlist[12][2] and imlist[11][2]>=imlist[14][2]and imlist[13][2]):
                position_p="down_p"
            if(imlist[12][2] and imlist[11][2]<=imlist[14][2]and imlist[13][2])and position_p=="down_p":
                position_p="up_p"
                pushupcount+=1
                print("Total pushups -> ",pushupcount)
                
                
            if(imlist[24][2] and imlist[23][2]>=imlist[26][2]and imlist[25][2]):
                position_s="down_s"
            if(imlist[24][2] and imlist[23][2]<=imlist[26][2]and imlist[25][2])and position_s=="down_s":
                position_s="up_s"
                situpcount+=1
                print("Total situps -> ",situpcount)
                
                
            if(imlist[24][2]>=imlist[32][2]):
                position_rk="up_rk"
            if(imlist[24][2]<=imlist[32][2])and position_rk=="up_rk":
                position_rk="down_rk"
                rkcount+=1
                print("Total right kicks -> ",rkcount)
                
            if(imlist[23][2]>=imlist[31][2]):
                position_lk="up_lk"
            if(imlist[23][2]<=imlist[31][2])and position_lk=="up_lk":
                position_lk="down_lk"
                lkcount+=1
                print("Total left kicks -> ",lkcount)
                
        # else:
        #     cv2.imshow("push-up counter",imgdisp)
        #     print("Nobody present on camera closing in 5 seconds...")
        #     cv2.waitKey(5000)
        #     break
                
        cv2.imshow("push-up counter",imgdisp)
        key=cv2.waitKey(1)
        if key==ord('x'):
            break
cap.release()