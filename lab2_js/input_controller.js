const bad_val = "Недопустивое значение";
const unreal_calc = "Невозможно вычислить";

function corrected_number(input_id){
    "use strict"; // для браузеров с поддержкой строгого режима

    const val = document.getElementById(input_id).value.toString();
    const testing_num = new RegExp("^([-]?[0-9]{1,}([.][0-9]{1,})?|" + bad_val + "|" + unreal_calc + ")$");
    const edit_num = new RegExp("^([-]?[0-9]{1,}([.][0-9]{1,})" + bad_val + "|" + unreal_calc + ")?");
    if (!testing_num.test(val)){
        if (edit_num.test(val)){
            document.getElementById(input_id).value = edit_num.exec(val)[0];
        } else {
            document.getElementById(input_id).value = "";
        }
    }

}

function correcting_number(input_id){
    "use strict"; // для браузеров с поддержкой строгого режима

    const val = document.getElementById(input_id).value.toString();
    const testing_num = new RegExp("^([-]?[0-9]+([.][0-9]*)?|[-]?[0-9]+[.]?|[-]?)$");
    const edit_num = new RegExp("^([-]?[0-9]+([.][0-9]*)?|[-]?[0-9]+[.]?|[-]?)");
    if (!testing_num.test(val)){
        if (edit_num.test(val)){
            document.getElementById(input_id).value = edit_num.exec(val)[0];
        } else {
            document.getElementById(input_id).value = "";
        }
    }
}

