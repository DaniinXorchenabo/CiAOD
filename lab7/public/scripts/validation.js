var bad_val = "Недопустивое значение";
var unreal_calc = "Невозможно вычислить";
var result = [];

function corrected_number(input_id){
	"use strict"; // для браузеров с поддержкой строгого режима

	const val = document.getElementById(input_id).value?.toString();
	const testing_num = new RegExp("^([1-9][0-9]*|0|" + bad_val + "|" + unreal_calc + ")$");
	const edit_num = new RegExp("^0*?([1-9][0-9]*|0|" + bad_val + "|" + unreal_calc + ")$");
	console.log(edit_num.exec(val))

	if (val && !testing_num.test(val)){
		if (edit_num.test(val)){
			console.log('===', edit_num.exec(val)[1])
			document.getElementById(input_id).value = edit_num.exec(val)[1];
		} else {
			document.getElementById(input_id).value = "";
		}
	}

}

function correcting_number(input_id){
	"use strict"; // для браузеров с поддержкой строгого режима

	const val = document.getElementById(input_id).value?.toString();
	const testing_num = new RegExp("^0*?([1-9][0-9]*|0)$");
	const edit_num = new RegExp("^0*?([1-9][0-9]*|0)$");
	console.log(edit_num.exec(val))
	if (val && !testing_num.test(val)){
		if (edit_num.test(val)){
			document.getElementById(input_id).value = edit_num.exec(val)[1];
		} else {
			document.getElementById(input_id).value = "";
		}
	}
}
const change_count_items_with_unsorted_data = (event) => {
	let unsorted_data = document.getElementById('unsorted_data')?.value
	if (!unsorted_data || unsorted_data === ""){
		unsorted_data = null;
		document.getElementById('count_of_elements').disabled = false;
		console.log(unsorted_data)
	} else {
		const count_of_elements_field = document.getElementById('count_of_elements');
		count_of_elements_field.disabled = true;
		count_of_elements_field.value = unsorted_data.toString().length;
		console.log(unsorted_data)
	}
}