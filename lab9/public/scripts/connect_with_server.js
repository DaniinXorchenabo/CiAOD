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
            'sort': [
                `get_sorts_time?`,
                `get_history=${get_history}`,
                `&len_file=${len_file}`,
                `&count_of_read=${get_count_of_read}`,
                `&count_of_write=${get_count_of_write}`,
                `&type_internal_sort=${pre_sort_type}`,
                `&chink_size_for_internal_sort=${pre_sort_count}`,
                `&external_sort_type=${external_sort_type}`,
                `${unsorted_data ? '&data_=' + unsorted_data : ''}`,
            ].reduce((last, i) => last + i),
            "many_sorts": [
                "get_many_sorts?",
                `get_history=${get_history}`,
                `&len_file=${len_file}`,
                `&count_of_read=${get_count_of_read}`,
                `&count_of_write=${get_count_of_write}`,
                `&type_internal_sort=${pre_sort_type}`,
                `&external_sort_type=${external_sort_type}`,
                `${unsorted_data ? '&data_=' + unsorted_data : ''}`,
            ].reduce((last, i) => last + i),
        };

        const displayed_sorts_func = i => {
            const data_from_server = JSON.parse(i);

            const patent_box = document.getElementById("patent_box");
            [...patent_box.children]
                .filter(i => i.id && !(i.id in data_from_server))
                .map(i => patent_box.removeChild(i));
            const ids = [...patent_box.children]
                .filter(i => i.id)
                .map(i => i.id.toString());
            console.log(
                ids,
                [...Object.entries(data_from_server)]
                    .map(([k, v]) => (ids.some(id_ => id_.toString() === k.toString())))
            );

            const new_ids = [...Object.entries(data_from_server)]
                .filter(([k, v]) => !(ids.some(id_ => id_.toString() === k.toString())));

            if (new_ids.length > 0) {
                patent_box.innerHTML += new_ids
                    .map(([k, v]) => sort_displayed_gen(k))
                    .reduce((last, i) => last + i);
            }


            [...document.querySelectorAll('button')].map(
                el => el.addEventListener('click', button_handler, {once: false}))

            console.log(data_from_server);
            [...Object.entries(data_from_server)].map(([sort_type, v]) => {
                [...Object.entries(v)].map(([key, val]) => {
                    const el = document.getElementById(`${sort_type}_${key}`);
                    el.value = val;
                    el.textContent = val;

                });
            });

            document.getElementById("get_sorted_data").checked = get_history;
            document.getElementById("get_count_of_read").checked = get_count_of_read;
            document.getElementById("get_count_of_write").checked = get_count_of_write;
            document.getElementById("count_of_elements").value = len_file;
            document.getElementById("count_of_elements_for_internal_pre_sort").value = pre_sort_count;
            document.getElementById('change_internal_pre_sort_type').value = pre_sort_type;
            document.getElementById("change_external_sort_type").value = external_sort_type;
            document.getElementById(`part_of_file_from`).value = start;
            document.getElementById(`part_of_file_to`).value = end;
            document.getElementById('select_file').value = target_file;
            if (document.getElementById('unsorted_data')) {
                document.getElementById('unsorted_data').value = unsorted_data;
            }

            ["selection"].map(i => {
                if (data_from_server[i]) {
                    const item = document.getElementById(i);
                    if (item) {
                        item.style.display = '';
                    }
                } else {
                    const item = document.getElementById(i);
                    if (item) {
                        item.style.display = 'none';
                    }
                }
                return i;

            });
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