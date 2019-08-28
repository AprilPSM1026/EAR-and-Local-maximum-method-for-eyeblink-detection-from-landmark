def eye_blinkdetection_localpeak(lefteye,righteye,head_rotation):
    yaw_rotation=head_rotation[:,1]
    roll_rotation=head_rotation[:,0]
    pitch_rotation=head_rotation[:,2]
    raw_eye_=[]

    '''parameter setup'''
    height=0
    wlen=5
    peak_distance=12#
    peak_width=0.1  #----eyeblink time is from 100mes to 400mes
    peak_height=0.2
    filter_ws=5
    poly=3
    for key,yaw in enumerate(yaw_rotation):
        
        
        if yaw>=-0.5 and yaw<=0.5 and lefteye[key]>=0 and righteye[key]>=0: # within the acceptant range yaw rotation 
        
            Ear_distance=(lefteye[key]+righteye[key])/2

        elif yaw>0.5 and lefteye[key]>=0 and righteye[key]>=0: #--turn right then usinglefteye value
            Ear_distance=lefteye[key]
            
            
        elif yaw<-0.5 and lefteye[key]>=0 and righteye[key]>=0: #--turn to left using right eye value
            Ear_distance=righteye[key]
        else:
            Ear_distance=2
        
        raw_eye_.append(Ear_distance)
        

    Ear_distance2arr=np.array(raw_eye_)
    #-------remove noise
    filtered_ear=scipy.signal.savgol_filter(Ear_distance2arr,filter_ws,poly)
    #---reverse data for find peak
    reverse_earfiltered=np.array([(1-i) for i in filtered_ear])
    #---using reverse data to find peak
    peaks_flitered,properties_filtered =scipy.signal.find_peaks(reverse_earfiltered,width=peak_width,distance=peak_distance,height=peak_height)
    

    return filtered_ear,peaks_flitered,properties_filtered 
