let $answer = $("#answer");
function getAdvCourses() {
    let $question = $('#question');
    if ($question.val() === ""){
        return false;
    }
    $.ajax({
        async:true,
        type:"GET",
        datatype: 'json',
        url: 'http://127.0.0.1:5000/query',
        data:{
            'question':$question.val()
        },
        error : function(XMLHttpRequest, textStatus, errorThrown) {
            console.log(XMLHttpRequest);
            console.log(textStatus);
            console.log(errorThrown);
        },
        success: function (response) {
            let response_json = $.parseJSON(response);
            $answer.empty();
            if (response_json['code'] === "0000"){
                let data = response_json['data'];
                let question_type = data['type'];
                let answer_info = data['result'];
                console.log(question_type,data);
                switch (question_type) {
                    case 0:
                        /*返回的是课程的详细介绍*/
                        $answer.append(answer_info);
                        break;
                    case 1:
                        /*返回的是先修课程*/
                        let courses = answer_info['courses'];
                        let html_text = '该课程的先修课程有 ';
                        if (courses.length === 1){
                            $answer.append("该课程没有先修课程");
                            break
                        }
                        for (let i=1;i<courses.length;i++){
                            let course = courses[i];
                            html_text+=course+" ";
                        }
                        $answer.append(html_text);
                        break;
                    case 2:
                        /*开课学期*/
                        $answer.append("该课程的开课学期是"+answer_info);
                        break;
                    case 3:
                        /*选修必修*/
                        if (answer_info === "n"){
                            $answer.append("该门课程是必修")
                        }else {
                            $answer.append("该门课程是选修")
                        }
                        break;
                    case 4:
                        /*学分*/
                        $answer.append("该门课程是"+answer_info+"学分");
                        break;
                    case 5:
                        /*学时*/
                        $answer.append("该门课程总共"+answer_info+"学时");
                        break;
                    case 6:
                        /*课程编号*/
                        $answer.append("该门课程的课程编号是 "+answer_info);
                        break;
                    case 7:
                        /*英文名称*/
                        $answer.append("该门课程的英文名称是 "+answer_info);
                        break;
                    case 8:
                        /*授课老师姓名*/
                        $answer.append("该门课程的老师是 "+answer_info);
                        break
                }
            }
            else {
                $answer.val(response_json['message']);
            }
        },
        crossDomain: true
    });
}
