// task1
const point_position = {悟空:{x:0, y:0, line: "left"}, 丁滿: {x:-1, y:4, line: "right"}, 
                  辛巴:{x:-3, y:3, line: "left"}, 貝吉塔:{x:-4, y:-1, line: "left"},
                  特南克斯: {x:1, y:-2, line: "left"}, 弗利沙:{x:4, y:-1, line: "right"}};

function func1(name){
    point_distance = [];
    nameList = [];
    for (const key in point_position){
        if (name == key){
            continue;
        }
        
        // 計算每個位置的距離
        // 如果帶入的對應key值是用變數呈現， 需要使用[]中括號包裹變數，不能使用.的方式連接取值
        // 辛巴 -> point_position.辛巴.x -> OK
        // name(為變數值) -> point_position.name.x -> ERROR
        x_distance = point_position[name].x - point_position[key].x;
        y_distance = point_position[name].y - point_position[key].y;

        //  判斷計算過後的x, y軸是否有負號，如果有負號要轉為正號
        if (x_distance < 0){
            x_distance = -(x_distance);
        }
        if (y_distance < 0){
            y_distance = -(y_distance);
        }
        
        // 加總步數
        total_distance = x_distance + y_distance;
        // 判斷兩者是否在線的同一邊，若不在同一邊，距離步數就加2
        if (point_position[name].line != point_position[key].line){
            total_distance += 2;
        }

        point_distance.push(total_distance);
        nameList.push(key);
    }

    // 找最遠距離
    // 需要使用 展開運算子 (...) 將陣列中的所有元素展開成單獨的參數，然後傳給 Math.max()
    // Math.max(10, 50, 2, 99, 35)
    max_step = Math.max(...point_distance);
    max_distance_name = "";
    // 找最近距離
    min_step = Math.min(...point_distance);
    min_distance_name = "";
    for (let i =0; i < point_distance.length; i++){
        //console.log(max_step);
        if (point_distance[i] == max_step){
            if (max_distance_name != ""){
                max_distance_name += "、" + nameList[i];
            }
            else{
                max_distance_name = nameList[i];
            }
            //console.log(max_distance_name);
        }

        if (point_distance[i] == min_step){
            if (min_distance_name != ""){
                min_distance_name += "、" + nameList[i];
            }
            else{
                min_distance_name = nameList[i];
            }
            //console.log(min_distance_name);
        }
    }

    let print_string = "最遠"+max_distance_name+"；最近"+min_distance_name;
    console.log(print_string);

}
func1("辛巴"); // print 最遠弗利沙；最近丁滿、貝吉塔
func1("悟空"); // print 最遠丁滿、弗利沙；最近特南克斯
func1("弗利沙"); // print 最遠辛巴，最近特南克斯
func1("特南克斯"); // print 最遠丁滿，最近悟空
console.log("===============================================================================");




// task2
let services_time={S1:[], S2:[], S3:[]};
function func2(ss, start, end, criteria){
    let service_len = ss.length;
    let compare_A = "";
    let compare_B = "";
    let expression_pass = [];
    // 儲存數值的差距
    let num_distance_list = [];
    // 紀錄比對的條件
    let operation_symbols = "";

    // 先將比對的字串轉為可以判斷的內容
    let split_criteria = null;
    if (criteria.includes(">=")){           
        let split_criteria = criteria.split(">=");
        compare_A = split_criteria[0];
        operation_symbols = ">=";
        if (compare_A != "name"){
            compare_B = parseFloat(split_criteria[1]);
        }
        else{
            compare_B = split_criteria[1];
        }
    }

    if (criteria.includes("<=") && compare_A == ""){
        split_criteria = criteria.split("<=");
        compare_A = split_criteria[0];
        operation_symbols = "<=";
        if (compare_A != "name"){
            compare_B = parseFloat(split_criteria[1]);
        }
        else{
            compare_B = split_criteria[1] 
        }
    } 

    if (criteria.includes("=") && compare_A == ""){
        split_criteria = criteria.split("=");
        compare_A = split_criteria[0];
        if (compare_A != "name"){
            compare_B = parseFloat(split_criteria[1]);
        }
        else{
            compare_B = split_criteria[1];  
        }
    }

    // 確認要判斷的物件是否不為name，若為name，就直接判斷對應的services
    if (compare_A != "name"){
        for (let i=0; i < service_len; i++){
            let num_distance = null;
            // 找出符合的services，並進行計算
            if (operation_symbols === ">="){
                if (ss[i][compare_A] >= compare_B){
                    num_distance = ss[i][compare_A] - compare_B;
                }
            }

            if (operation_symbols === "<="){
                if (ss[i][compare_A] <= compare_B){
                    num_distance = ss[i][compare_A] - compare_B;
                }
            }
            
            // 如果有符合的才會有差距值，然後在這一塊判斷從最符合到符合的方式排序
            if (num_distance != null){
                if (num_distance < 0){
                    num_distance = -(num_distance)
                }
                        
                let list_idx = 0;
                if (num_distance_list != []){
                    for (let k =0; k < num_distance_list.length; k++){
                        if (num_distance_list[k] < num_distance){
                            list_idx += 1;
                            //console.log(list_idx);
                        }
                    }
                    num_distance_list.splice(list_idx, 0,num_distance);
                }
                else{
                    num_distance_list.push(num_distance);  
                }          
                
                // 已按照差距最小到差距最大排列
                expression_pass.splice(list_idx, 0, ss[i]["name"]);
                //console.log(expression_pass);  
            } 
        }      
    }
    else if (compare_A == "name"){
        expression_pass.push(compare_B);
    }
          
    let time = [];
    time.push(start);
    let start_num = start;
    while (start_num < end){
        start_num += 1;
        time.push(start_num);
    }

    let best_match_services = null;
    for (let l=0; l < expression_pass.length; l++){
        // 判斷時間是否都沒被預訂走
        let time_warm = 0;
        for (let j=0; j < time.length; j++){
            if (services_time[expression_pass[l]].includes(time[j])){
                time_warm += 1;
                break;
            }
        }

        if (time_warm == 0){
            best_match_services = expression_pass[l];
            services_time[expression_pass[l]].push(...time); // 將預約的時間新增至list中，藉此後續判斷是否被約走了
            console.log(expression_pass[l]);
            break;
        }
    }

    // 如果每一個符合的services，與對應的時間都已被預約，就會印出sorry的字樣
    if (best_match_services === null){
        console.log("Sorry");
    }
    
}
const services=[
{"name":"S1", "r":4.5, "c":1000},
{"name":"S2", "r":3, "c":1200},
{"name":"S3", "r":3.8, "c":800}
];
func2(services, 15, 17, "c>=800"); // S3
func2(services, 11, 13, "r<=4"); // S3
func2(services, 10, 12, "name=S3"); // Sorry
func2(services, 15, 18, "r>=4.5"); // S1
func2(services, 16, 18, "r>=4"); // Sorry
func2(services, 13, 17, "name=S1"); // Sorry
func2(services, 8, 9, "c<=1500"); // S2
func2(services, 8, 9, "c<=1500"); // S1
console.log("===============================================================================");




// task3
let sequence_rule = [-2, -3, 1, 2];
function func3(index){
    let value = 25;
    let sequence_rule_idx = 0;
    let idx_len = index+1;
    for (let i=0; i < idx_len; i++){
        if (i === 0){
            continue;
        }

        sequence_rule_idx =(i % 4);
        if (sequence_rule_idx === 0){
            sequence_rule_idx = 3;
        }
        else{
            sequence_rule_idx -= 1;
        }
        value = value + sequence_rule[sequence_rule_idx];
    }

    console.log(value);
}
func3(1); // print 23
func3(5); // print 21
func3(10); // print 16
func3(30); // print 6
console.log("===============================================================================");




// task4
function func4(sp, stat, n){
    let best_vacancy_idx = null;
    let people_num = 0;
    for (let i = 0; i < stat.length; i++){
        if (stat[i] === "1"){
            continue;
        }
       
        if (best_vacancy_idx === null){
            people_num = sp[i] - n;
            best_vacancy_idx = i;
        }
        else{
            num = sp[i] - n;
            // 如果剛好找到吻合的空卻位置，直接用該區的位置，且不往下執行後續判斷。
            if (num === 0){
                best_vacancy_idx = i;
                break;
            }
            if (people_num === 0){
                break;
            }

            // 如果都沒有非常符合的，就找差距最小的位置。
            if ( num > 0){
                if (people_num > num){
                    best_vacancy_idx = i;
                }
                if (people_num < num){
                    continue;
                }
            }
            else if (num < 0){
                if (people_num > num){
                    continue;
                }
                if (people_num < num){
                    best_vacancy_idx = i;
                }
            }
        }
    }
    console.log(best_vacancy_idx);
}
func4([3, 1, 5, 4, 3, 2], "101000", 2); // print 5
func4([1, 0, 5, 1, 3], "10100", 4); // print 4
func4([4, 6, 5, 8], "1000", 4); // print 2
console.log("===============================================================================");