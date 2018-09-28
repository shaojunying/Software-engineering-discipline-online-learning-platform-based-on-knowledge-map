$(function () {
   'use strict';

   window.Input = function (selector) {
        //要进行验证的元素
        let $ele,
        $error_ele,
        me = this,
        //规则对象
        rule = {
            required:true,
        };

        this.load_validator = function () {
            let val = this.get_val();
            this.validator = new Validator(val,rule);

        };
        this.get_val = function () {
            return $ele.val();
        };


        function init() {
            find_ele();
            find_error_ele();
            parse_rule();
            me.load_validator();
            listen();
        }

        function listen() {
            $ele.on('change',function () {
                let valid = me.validator.is_valid(me.get_val());
                console.log("valid",valid);
                if (valid) {
                    $error_ele.hide();
                    console.log("隐藏");
                }else {
                    $error_ele.show();
                    console.log("显示");
                }
            })
        }

        function find_error_ele() {
            $error_ele = $(get_error_selector())
        }

        function get_error_selector() {
            return '#'+$ele.attr("name")+'-input-error'
        }

        function find_ele(){
            if (selector instanceof jQuery){
                $ele = selector;
            } else {
                $ele = $(selector);
            }
        }


       function parse_rule() {
            let i;
            let rule_string = $ele.data('rule');
            if (!rule_string) return;

            //这里会将规则生成数组
            let rule_arr = rule_string.split("|");
            //将数组转为对象
            for (i = 0; i < rule_arr.length; i++) {
                let item_str =rule_arr[i];
                let item_arr = item_str.split(":");
                //JSON.parse('10')将会返回数字10,
                //JSON.parse('"10"')将会返回"10"
                rule[item_arr[0]]=JSON.parse(item_arr[1]);
            }

       }

        init();
   }
});
