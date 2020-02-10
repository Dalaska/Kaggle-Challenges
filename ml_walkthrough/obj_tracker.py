# define a car object
class car():
        def __init__(self):
            self.average_centroid= (0,0) # average centroid
            self.width = 0 # average box width
            self.height = 0 # average height
            self.detected = 0.5  # moving average

# caculate distance
def cal_dist(centroid1, centroid2):
    x1 = centroid1[0]
    y1 = centroid1[1]
    x2 = centroid2[0]
    y2 = centroid2[1]
    return np.sqrt((x1-x2)**2 + (y1-y2)**2)

# test the function
centroid1 = (1,2)
centroid2 = (2,5)
dist = cal_dist(centroid1, centroid2)
print('Distance:', dist)

# define a function to find nearby car object 
def track_car(cntrd,old_Cars):
    threshod_dist = 40 # the maxium distance to consider nearby
    Dist = [] # a list of distance
    if not old_Cars: # if the list of nearby cars is empty
        # return car not found 
        car_found = False 
        car_id = 0
        return car_found,car_id
    else:
        for car in old_Cars:
            # cacualte the distance
            dist = cal_dist(cntrd, car.average_centroid)
            Dist.append(dist)
        car_id = np.argmin(Dist)
        if Dist[car_id] < threshod_dist:
            car_found = True
        else:
            car_found = False
        return car_found, car_id

# find the centroid and size of a bounding box
def find_box_centroid_size(bboxes):
    box_centroids = []
    box_size = []
    
    for box in bboxes:
        x = int((box[0][0] + box[1][0])/2)
        y = int((box[0][1] + box[1][1])/2)
        box_centroids.append((x,y))

        width =  int((box[1][0] - box[0][0])/2)
        height = int((box[1][1] - box[0][1])/2)
        box_size.append((width,height))
    return box_centroids, box_size

# define bounding boxes of detacted cars
def find_car_box(Old_Cars, detected_threshold = 0.51):
    box2 = []
    for car2 in Old_Cars:
        if car2.detected > detected_threshold:
            offset = car2.average_centroid          
            width = car2.width
            height = car2.height
            bbox0 = (int(-width+offset[0]),
                     int(-height+offset[1]))
            bbox1 = (int(width+offset[0]),
                     int(height+offset[1]))
            box2.append((bbox0,bbox1))
    return box2

# video pipline
def process_img(image):
    # define car object
    class car():
        def __init__(self):
            self.average_centroid= (0,0) # average centroid
            self.width = 0 # average box width
            self.height = 0 # average height
            self.detected = 0.5  # moving average
    
    global Detected_Cars
    global heatmap
    
    # make a copy of the incial image
    draw_img = np.copy(image)
    
    # find windows that contains cars
    boxes = find_cars(image)
    
    # draw windows that contains cars
    draw_img = draw_boxes(draw_img, boxes, color=(0, 0, 255), thick=2)


    # create a new heat map
    heatmap_new = np.zeros_like(image[:,:,0]).astype(np.float)
    # increase heatmap value on windows contain cars
    heatmap_new = add_heat(heatmap_new, boxes)
    # truncate the value if it's greater than 1. 
    # It's easy to set the threshold value for the 
    # moving average funciton, if the values are bounded
    heatmap_new = apply_upper_threshold(heatmap_new,1)
    
    # update the heatmap with the moving average algorithm 
    # so that, if car image are no longer detacted, that area "cool" down
    heatmap = 0.9*heatmap + 0.1*heatmap_new
        
    
    # wrap heatmap to the orignal image
    wrap_img = np.zeros_like(image) # inicalize
    wrap_img[:,:,1] = heatmap[:]*250 # adding heat map
    # blend image with the heat map
    draw_img = cv2.addWeighted(draw_img, 1, wrap_img, 0.5, 0)

    # create a new heatmap to show the heatmap with more certainty 
    # by thresholding the heatmap value
    heatmap_sure = np.copy(heatmap)
    # get area of higher certainty by thredholding the heatmap
    heatmap_sure = apply_lower_threshold(heatmap_sure, 0.97)
    #labels of areas
    labels = label(heatmap_sure)
    # finding the bounding box of labeled area
    bounding_boxes = find_labeled_bboxes(image, labels)
    
     
    # find centroy and size of bounding box
    centroids,box_size = find_box_centroid_size(bounding_boxes)
    

    New_Cars = [] # inicalize a list of new found cars
    for n in range(len(centroids)):
        # find nearby car object          
        car_found, k = track_car(centroids[n],Detected_Cars) # return a number 
        if car_found  == True:
            # update detected car object
            # update centroid using moving average
            Detected_Cars[k].average_centroid = (int(0.9*Detected_Cars[k].average_centroid[0] + 0.1*centroids[n][0]),
                                    int(0.9*Detected_Cars[k].average_centroid[1] + 0.1*centroids[n][1]))         
            # update bounding box width using moving average
            Detected_Cars[k].width =   math.ceil(0.9*Detected_Cars[k].width + 0.1*box_size[n][0]) # round up
            # update bounding box height using moving average
            Detected_Cars[k].height =  math.ceil(0.9*Detected_Cars[k].height + 0.1*box_size[n][1])
            # update detected value
            Detected_Cars[k].detected = Detected_Cars[k].detected + 0.2

        else: # add new car
            new_car = car()
            # inicalize the car object using the size 
            # and centroid of the bounding box
            new_car.average_centroid = centroids[n]
            new_car.width =  box_size[n][0]
            new_car.height = box_size[n][1]            
            New_Cars.append(new_car)
            
    # combine new_cars to detected cars
    Detected_Cars2 = list(Detected_Cars) # make a copy
    Detected_Cars = New_Cars[:] # add new cars
    if Detected_Cars2: # if is not empty
        for car in Detected_Cars2:
            # if the detected value greater than the threshold add to the list
            # if not discard
            if car.detected > 0.17: 
                # add to the detected cars list
                Detected_Cars.append(car)
            
    # find car object that is consistent
    car_boxes = find_car_box(Detected_Cars, detected_threshold = 0.55) #0.51
    # draw bounding boxes on car object that is more certain
    draw_img = draw_boxes(draw_img, car_boxes, color=(255, 0, 0), thick=5)         
            
    # depreciate old car values, so if it no longer detacted the value fade away
    for car in Detected_Cars:
        car.detected = car.detected*0.8 # depreciate old value
    
    return draw_img