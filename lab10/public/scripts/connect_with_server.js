// import sort_displayed_gen;

const button_handler = (event) => {
    console.log(event.target.id);
    setTimeout(() => {
        const xhr = new XMLHttpRequest();
        // const start = document.getElementById(`part_of_file_from`).value;
        // const end = document.getElementById(`part_of_file_to`).value;
        // const setup_count = document.getElementById("iteration_count").value;
        // const graph_text = event.target.attributes.graph_text.nodeValue;
        const get_history = document.getElementById("get_sorted_data").checked;
        const get_count_of_read = document.getElementById("get_count_of_read").checked;
        const get_count_of_write = document.getElementById("get_count_of_write").checked;
        const len_file = document.getElementById("count_of_elements").value;
        const pre_sort_count = document.getElementById("count_of_elements_for_internal_pre_sort").value;
        const pre_sort_type = document.getElementById('change_internal_pre_sort_type').value;
        const external_sort_type = document.getElementById("change_external_sort_type").value;
        const start = document.getElementById(`part_of_file_from`).value;
        const end = document.getElementById(`part_of_file_to`).value;
        const target_file = document.getElementById('select_file').value;
        let unsorted_data = document.getElementById('unsorted_data')?.value;
        if (!unsorted_data || unsorted_data === "") {
            unsorted_data = null;
        }

        let alert_text = '';

        if ((Number(start)).toString() === start) {
            if (Number(start) >= 0) {

            } else {
                alert_text += 'Поле  "От" должно быть целым не отрицательным числом\n'
            }

        } else {
            alert_text += 'Поле "От" должно являться целым не отрицательным целым числом\n'
        }

        if ((Number(end)).toString() === end) {
            if (Number(end) > 0) {
                if ((Number(start)).toString() === start && (Number(end)).toString() === end && Number(start) < Number(end)) {

                } else {
                    alert_text += 'Поле  "До" должно быть целым не отрицательным числом, большим чем поле "От"\n'
                }

            } else {
                alert_text += 'Поле  "До" должно быть целым не отрицательным числом, большим чем поле "От"\n'
            }

        } else {
            alert_text += 'Поле "До" должно являться целым не отрицательным целым числом, большим чем поле "От"\n'
        }


        const id_to_url = {
            "part_of_file": `get_part_file?filename=${target_file}&from_=${start}&to_=${end}`,
            "many_sorts": [
                "get_many_sorts?",
                `len_file=${len_file}`,
                `${unsorted_data ? '&data_=' + unsorted_data : ''}`,
                `&get_history=${get_history}`,
                `&count_of_read=${get_count_of_read}`,
                `&count_of_write=${get_count_of_write}`,
                `&type_internal_sort=${pre_sort_type}`,
                `&start_len=${10}`,
                `&end_len=${100}`,
                `&count_iter=${5}`,

            ].reduce((last, i) => last + i),
        };

        const displayed_sorts_func = i => {
                const data_from_server = JSON.parse(i);

                console.log(data_from_server);
                const transform_data = {};
                const transform_for_graph = {};
                [...Object.entries(data_from_server)]
                    .map(([len_sorted_data, value_]) => [...Object.entries(value_)]
                        .map(([sort_type, data]) => {
                            data['size'] = len_sorted_data;
                            data['sort_type'] = sort_type;
                            transform_data[`${sort_type}__${len_sorted_data}`] = data;
                            if (transform_for_graph[sort_type] === undefined){
                                transform_for_graph[sort_type] = {};
                                transform_for_graph[sort_type]["size"] = [];
                                transform_for_graph[sort_type]["time"] = [];
                                transform_for_graph[sort_type]["count_of_read"] = [];
                                transform_for_graph[sort_type]["count_of_write"] = [];
                            }
                            transform_for_graph[sort_type]["size"].push(len_sorted_data);
                            if (data["time"] !== undefined){
                                transform_for_graph[sort_type]["time"].push(data["time"]);
                            }
                            if (data["count_of_read"]!== undefined){
                                transform_for_graph[sort_type]["count_of_read"].push(data["count_of_read"]);
                            }
                            if (data["count_of_write"]!== undefined){
                                transform_for_graph[sort_type]["count_of_write"].push(data["count_of_write"]);
                            }

                        }));
                console.log(transform_data);
                const patent_box =  document.getElementById("patent_box");
                [...patent_box.children].filter(i => i.id && !(i.id in transform_data)).map(i => patent_box.removeChild(i));
                const ids = [...patent_box.children].filter(i => i.id).map(i => i.id);
                patent_box.innerHTML += [...Object.entries(transform_data)]
                    .filter(([k, v]) => !(k in ids))
                    .map(([k, v]) => sort_displayed_gen(k))
                    .reduce((last, i) => last + i);


                // [...document.querySelectorAll('button')].map(
                //     el => el.addEventListener('click', button_handler, {once: false}))

                // console.log(transform_data);
                // [...Object.entries(transform_data)].map(([sort_type, v]) => {
                //     [...Object.entries(v)].map(([key, val]) => {
                //         const el = document.getElementById(`${sort_type}_${key}`);
                //         el.value = val;
                //         el.textContent = val;
                //
                //     });
                // });

                // ["one", "two"].map(i => {
                //     if (data_from_server[i]){
                //          const item = document.getElementById(i);
                //          if (item) {
                //              item.style.display = '';
                //          }
                //     } else {
                //         const item = document.getElementById(i);
                //          if (item) {
                //              item.style.display = 'none';
                //          }
                //     }
                //     return i;
                //
                // });

                draw_graph(transform_for_graph, transform_data );
            }

        const id_to_result_f = {
            "part_of_file": (data) => {
                document.getElementById('part_of_file_output').value += data + "\n"
            },
            "sort": displayed_sorts_func,
            "many_sorts": displayed_sorts_func,
        };

        if (alert_text === '') {
            xhr.open(
                'GET',
                `${document.location.protocol}//${document.location.host}/${id_to_url[event.target.id]}`,
                true);

            xhr.send();
            xhr.onreadystatechange = () => { // (3)
                if (xhr.readyState !== 4) return;

                // button.innerHTML = 'Готово!';

                if (xhr.status !== 200) {
                    console.log(xhr.status + ': ' + xhr.statusText);
                } else {
                    console.log(xhr.responseText);
                    id_to_result_f[event.target.id](xhr.responseText);
                    // draw_graph(JSON.parse(xhr.responseText), graph_text);
                }

            }
        } else {
            alert(alert_text);
        }
    });

}


[...document.querySelectorAll('button')].map(
    el => el.addEventListener('click', button_handler, {once: false}))

setTimeout(() => {
    const xhr = new XMLHttpRequest();
    xhr.open(
        'GET',
        `${document.location.protocol}//${document.location.host}/get_files`,
        true);

    xhr.send();
    xhr.onreadystatechange = () => { // (3)
        if (xhr.readyState !== 4) return;
        if (xhr.status !== 200) {
            console.log(xhr.status + ': ' + xhr.statusText);
        } else {
            console.log(xhr.responseText);
            document.getElementById('select_file').innerHTML = [...JSON.parse(xhr.responseText)].map(
                i => `<option value=${i}>${i}</option>`).reduce((last, x) => last + x);
        }
    }
});

setTimeout(() => {
    const xhr = new XMLHttpRequest();
    xhr.open(
        'GET',
        `${document.location.protocol}//${document.location.host}/get_sort_types`,
        true);

    xhr.send();
    xhr.onreadystatechange = () => { // (3)
        if (xhr.readyState !== 4) return;
        if (xhr.status !== 200) {
            console.log(xhr.status + ': ' + xhr.statusText);
        } else {
            console.log(xhr.responseText);
            document.getElementById('change_internal_pre_sort_type').innerHTML = [...JSON.parse(xhr.responseText)].map(
                i => `<option value=${i}>${i}</option>`).reduce((last, x) => last + x);
        }
    }
});