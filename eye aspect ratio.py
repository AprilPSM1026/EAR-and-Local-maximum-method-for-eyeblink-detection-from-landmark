def eyeblink_EARdetection(lefteye,righteye,head_rotation):#one question all frames
    
    yaw_rotation=head_rotation[:,1]#-----euler angle are radians
    roll_rotation=head_rotation[:,0]
    pitch_rotation=head_rotation[:,2]
    
    
    constant_threshold=0.3
    eyeblink_pointstep=[]
   
    local_ws=10
    raw_eye=[]
    for key,yaw in enumerate(yaw_rotation):
       '''within the acceptant range yaw rotation about 30 degree is acceptable range for EAR,we use average EAR distance of both eyes'''
        if yaw>=-0.5 and yaw<=0.5: 
        
            aver_earrate=(lefteye[key]+righteye[key])/2 
            raw_eye.append(aver_earrate)
            
            if aver_earrate<=constant_threshold and lefteye[key]>=0 and righteye[key]>=0:
                eyeblink_pointstep.append(1)
            elif aver_earrate>constant_threshold and lefteye[key]>=0 and righteye[key]>=0 and aver_earrate<=1:
                eyeblink_pointstep.append(0)
            else:
                eyeblink_pointstep.append(-1)
                
        if yaw>0.5: #--turn right direction then using lefteye value
            earrate=lefteye[key]
            raw_eye.append(earrate)
            if earrate<=constant_threshold and earrate>=0:
                eyeblink_pointstep.append(1)
            elif earrate>constant_threshold and earrate>=0 and earrate<=1:
                eyeblink_pointstep.append(0)
            else:
                eyeblink_pointstep.append(-1)
        if yaw<-0.5: #--turn to left using right eye value
            earrate=righteye[key]
            raw_eye.append(earrate)
            if earrate<=constant_threshold and earrate>=0:
                eyeblink_pointstep.append(1)
            elif earrate>constant_threshold and earrate>=0 and earrate<=1:
                eyeblink_pointstep.append(0)
            else:
                eyeblink_pointstep.append(-1)
        
    eyeblink2arr=np.array(eyeblink_pointstep)
    
    #----search for eyeblink frames
    sinslide_ws=4 #0.3*30 #(single side) #330ms current(+_4) set 9 frame as window size
    eyeblink_ind=[]
    for key,eye in enumerate(eyeblink2arr):
        if key>=10 and key<=len(eyeblink2arr)-10:
            curr_action=eye
            left_frame=list(eyeblink2arr[key-sinslide_ws:key])
            right_frame=list(eyeblink2arr[key+1:key+sinslide_ws+1])
            if curr_action==1 and left_frame.count(1)==sinslide_ws and right_frame.count(1)==sinslide_ws:
                eyeblink_ind.append(key)
    
    eyeblinkind2arr=np.array(eyeblink_ind)    
    
    return eyeblinkind2arr
