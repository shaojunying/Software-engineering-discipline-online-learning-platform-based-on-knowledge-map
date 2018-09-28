$(function () {
    'use strict';

    // let validator = new Validator('aaa',{
    //     // max:100,
    //     // min:10,
    //     // maxlength: 5,
    //     pattern:"^[a-zA-Z0-9]*$",
    // });
    //
    // // let result = validator.validate_numeric();
    // let result = validator.validate_pattern();
    // console.log("result:",result);

    // let test = new Input('#test');
    // let valid = test.validator.is_valid();
    // console.log("valid",valid);

    let $inputs = $('[data-rule]');
    let $form = $('#signup');
    let inputs = [];

    $inputs.each(function (index, node) {
        inputs.push(new Input(node))
    });

    $form.on('submit',function (e) {
        e.preventDefault();
        $inputs.trigger("blur");
        for (let i = 0; i < inputs.length; i++){
            let item = inputs[i];
            let r = item.validator.is_valid();
            if (!r){
                alert('注册失败');
                return;
            }
        }
        alert("注册成功");
    })

    function signup() {

    }

});

