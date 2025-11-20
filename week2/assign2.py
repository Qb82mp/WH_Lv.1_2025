
# task1
point_position = {"悟空":{'x':0, 'y':0, "line": "left"}, "丁滿": {'x':-1, 'y':4, "line": "right"}, 
                  "辛巴":{'x':-3, 'y':3, "line": "left"}, "貝吉塔":{'x':-4, 'y':-1, "line": "left"},
                  "特南克斯": {'x':1, 'y':-2, "line": "left"}, "弗利沙":{'x':4, 'y':-1, "line": "right"}}

def func1(name):
    point_distance = []
    nameList = []
    for key in point_position:
        if name == key:
            continue

        # 計算每個位置的距離
        x_distance = point_position[name]['x'] - point_position[key]['x']
        y_distance = point_position[name]['y'] - point_position[key]['y']

        # 判斷計算過後的x, y軸是否有負號，如果有負號要轉為正號
        if "-" in str(x_distance):
            x_distance = -(x_distance)
        if "-" in str(y_distance):
            y_distance = -(y_distance)

        # 加總步數
        total_distance = x_distance + y_distance
        # 判斷兩者是否在線的同一邊，若不在同一邊，距離步數就加2
        if point_position[name]["line"] != point_position[key]["line"]:
            total_distance += 2


        point_distance.append(total_distance)
        nameList.append(key)

    # 找最遠距離
    max_step = max(point_distance)
    max_distance_name = ""
    # 找最近距離
    min_step = min(point_distance)
    min_distance_name = ""
    for i in range(len(point_distance)):
        if point_distance[i] == max_step:
            if max_distance_name != "":
                 max_distance_name += "、" + nameList[i]
            else:
                max_distance_name = nameList[i]

        if point_distance[i] == min_step:
            if min_distance_name != "":
                min_distance_name += "、" + nameList[i]
            else:
                min_distance_name = nameList[i]

    print_str = "最遠"+max_distance_name+"；最近"+min_distance_name
    print(print_str)

func1("辛巴") # print 最遠弗利沙；最近丁滿、貝吉塔
func1("悟空") # print 最遠丁滿、弗利沙；最近特南克斯
func1("弗利沙") # print 最遠辛巴，最近特南克斯
func1("特南克斯") # print 最遠丁滿，最近悟空
print("===============================================================================")




# task2
services_time={"S1":[], "S2":[], "S3":[]}
def func2(ss, start, end, criteria):
    service_len = len(ss)
    compare_A = ""
    compare_B = ""
    expression_pass = []
    # 儲存數值的差距
    num_distance_list = []
    # 紀錄比對的條件
    operation_symbols = ""

    # 先將比對的字串轉為可以判斷的內容
    split_criteria = None
    if ">=" in criteria:           
        split_criteria = criteria.split(">=")
        compare_A = split_criteria[0]
        operation_symbols = ">="

    if "<=" in criteria and compare_A == "":
        split_criteria = criteria.split("<=")
        compare_A = split_criteria[0]
        operation_symbols = "<="

    if "=" in criteria  and compare_A == "":
        split_criteria = criteria.split("=")
        compare_A = split_criteria[0]
        
    if compare_A != "name":
            compare_B = float(split_criteria[1])
    else:
            compare_B = split_criteria[1]


    # 確認要判斷的物件是否不為name，若為name，就直接判斷對應的services
    if compare_A != "name":
        for i in range(service_len):
            num_distance = None
            if operation_symbols == ">=":
                if ss[i][compare_A] >= compare_B:
                    num_distance = ss[i][compare_A] - compare_B
            if operation_symbols == "<=":
                if ss[i][compare_A] <= compare_B:
                    num_distance = ss[i][compare_A] - compare_B
            
            # 比對之後有符合的，才會進行差距的計算，並判斷從差距最小排到差距最大
            if num_distance != None:
                if num_distance < 0:
                    num_distance = -(num_distance)
                        
                list_idx = 0
                if num_distance_list != []:
                    for k in range(len(num_distance_list)):
                        if num_distance_list[k] < num_distance:
                            list_idx = list_idx+1
                    num_distance_list.insert(list_idx, num_distance)
                else:
                    num_distance_list.append(num_distance)                                   
                            
                # 已按照差距最小到差距最大排列
                expression_pass.insert(list_idx, ss[i]["name"])       
    elif compare_A == "name":
        expression_pass.append(compare_B)
          
    time = []
    time.append(start)
    start_num = start
    while start_num < end:
        start_num += 1
        time.append(start_num)

    best_match_services = None
    for key in expression_pass:
        # 判斷時間是否都沒被預訂走，每一個services都要重新計算時間是否沒有撞到
        time_warm = 0
        for j in range(len(time)):
            if time[j] in services_time[key]:
                time_warm += 1
                break

        if time_warm == 0:
            best_match_services = key
            services_time[key].extend(time) # 將預約的時間新增至list中，藉此後續判斷是否被約走了
            print(key)
            break

    # 如果每一個符合的services，與對應的時間都已被預約，就會印出sorry的字樣
    if best_match_services == None:
        print("Sorry")



services=[
{"name":"S1", "r":4.5, "c":1000},
{"name":"S2", "r":3, "c":1200},
{"name":"S3", "r":3.8, "c":800}
]
func2(services, 15, 17, "c>=800") # S3
func2(services, 11, 13, "r<=4") # S3
func2(services, 10, 12, "name=S3") # Sorry
func2(services, 15, 18, "r>=4.5") # S1
func2(services, 16, 18, "r>=4") # Sorry
func2(services, 13, 17, "name=S1") # Sorry
func2(services, 8, 9, "c<=1500") # S2
func2(services, 8, 9, "c<=1500") # S1
print("===============================================================================")




# task3
sequence_rule = [-2, -3, 1, 2]
def func3(index):
    value = 25
    sequence_rule_idx = None
    i = 0
    while i <= index:
        if i == 0:
            i += 1
            continue
        
        sequence_rule_idx =(i % 4)
        if sequence_rule_idx == 0:
            sequence_rule_idx = 3
        else:
            sequence_rule_idx -= 1
        
        value = value + sequence_rule[sequence_rule_idx]
        i += 1
    
    print(value)

func3(1) # print 23
func3(5) # print 21
func3(10) # print 16
func3(30) # print 6
print("===============================================================================")




# task4
def func4(sp, stat, n):
    best_vacancy_idx = None
    people_num = 0
    
    for i in range(len(stat)):
        if stat[i] == "1":
            continue

        if best_vacancy_idx == None:
            people_num = sp[i] - n
            best_vacancy_idx = i
        else:
            num = sp[i] - n
            # 如果剛好找到吻合的空卻位置，直接用該區的位置，且不往下執行後續判斷。
            if num == 0:
                best_vacancy_idx = i
                break

            if people_num == 0:
                break
        
            # 如果都沒有非常符合的，就找差距最小的位置。
            if num > 0:
                if people_num > num:
                    best_vacancy_idx = i
                
                if people_num < num:
                    continue
            elif num < 0:
                if people_num > num:
                    continue

                if people_num < num:
                    best_vacancy_idx = i
    
    print(str(best_vacancy_idx))


func4([3, 1, 5, 4, 3, 2], "101000", 2) # print 5
func4([1, 0, 5, 1, 3], "10100", 4) # print 4
func4([4, 6, 5, 8], "1000", 4) # print 2
print("===============================================================================")
