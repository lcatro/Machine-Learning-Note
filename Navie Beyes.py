
'''

    x1 = 1,1,1,1,2 ,2 ,2 ,1 ,2,2 ,2,3,3 ,1 ,2 ,3,3
    x2 = A,A,A,A,A ,A ,B ,B ,B,C ,B,C,A ,B ,A ,A,C
    y  = 1,1,1,1,-1,-1,-1,-1,1,-1,1,1,-1,-1,-1,1,1

'''


x1 = [1,1,1,1,2 ,2 ,2 ,1 ,2,2 ,2,3,3 ,1 ,1 ,2 ,3,3]#[1,1,1,1,1,2,2,2,2,2,3,3,3,3,3]
x2 = [7,7,7,7,7 ,7 ,8 ,8 ,8,9 ,8,9,7 ,8 ,8 ,7 ,7,9]#[4,5,5,4,4,4,5,5,6,6,6,5,5,6,6]
y  = [1,1,1,1,-1,-1,-1,-1,1,-1,1,1,-1,-1,-1,-1,1,1]#[-1,-1,1,1,-1,-1,-1,1,1,1,1,1,1,1,-1]

alpha = 1


def static_diffrence_value_set(data_set) :
    list = []
    
    for index in data_set :
        if not index in list :
            list.append(index)
            
    return list

def static_diffrence_value(data_set) :
    return len(static_diffrence_value_set(data_set))

def calcu_all_probability(feature_data_set) :
    p = {}
    
    for value_index in static_diffrence_value_set(feature_data_set) :
        count_x_y1  = 0
        count_x_y_1 = 0
        feature_data_set_length = len(static_diffrence_value_set(feature_data_set))
        
        for index in range(len(feature_data_set)) :
            if value_index == feature_data_set[index] and 1 == y[index] :
                count_x_y1 += 1
            elif value_index == feature_data_set[index] and -1 == y[index] :
                count_x_y_1 += 1
             
        p[value_index] = {
            1  : (count_x_y1  + alpha) / float(y.count( 1) + feature_data_set_length * alpha) ,
            -1 : (count_x_y_1 + alpha) / float(y.count(-1) + feature_data_set_length * alpha) ,
        }
        
    return p

def train_model() :
    p_y1  = (y.count( 1) + alpha) / float(len(y) + static_diffrence_value(y) * alpha)
    p_y_1 = (y.count(-1) + alpha) / float(len(y) + static_diffrence_value(y) * alpha)
    
    p_x1 = calcu_all_probability(x1)
    p_x2 = calcu_all_probability(x2)
    
    return p_y1 , p_y_1 , p_x1 , p_x2
    
def try_classify(data_x1,data_x2,model) :
    p_y1  = model[0] * model[2][data_x1][1]  * model[3][data_x2][1]
    p_y_1 = model[1] * model[2][data_x1][-1] * model[3][data_x2][-1]
    
    print p_y1 , p_y_1
    
    if p_y1 > p_y_1 :
        return 1
    elif p_y1 == p_y_1 :
        return 0
    
    return -1
    
    
if __name__ == '__main__' :
    model = train_model()
    
    print try_classify(1,7,model) , 1,7
    print try_classify(1,8,model) , 1,8
    print try_classify(1,9,model) , 1,9
    print try_classify(2,7,model) , 2,7
    print try_classify(2,8,model) , 2,8
    print try_classify(2,9,model) , 2,9
    print try_classify(3,7,model) , 3,7
    print try_classify(3,8,model) , 3,8
    print try_classify(3,9,model) , 3,9
    
#    print try_classify(2,4,model) , 2,4
