// Plotly.react('my_graph_time', [], layout);

const updating_graph_data = ([key, value, default_obj], index) => {
    // console.log(key, value, default_obj, index)
    return Object.assign(default_obj, {
        x: [...Object.keys(value)],
        y: [...Object.values(value)],
        name: key
    })
}


const draw_graph = (data_for_graph, sort_data, data_from_server, graph_text = "Типы сортировок") => {

    const get_data_for_showing_graph = (formatted_data, flag) => {
        return formatted_data
            .map(([key, value, default_obj], index) => {
                const new_value = {};
                [...value["size"]].map((item, index) => {
                    new_value[item] = value[flag][index];
                });
                return [key, new_value, default_obj]
            })
            .map(updating_graph_data);
    }

    const layout_generator = (graph_name) => {
        return {
            title: graph_name,
            uirevision: 'true',
            xaxis: {autorange: true},
            yaxis: {autorange: true}
        };
    }

    const graph_drawer = (graph_id, graph_name, graph_flag, formatted_data) => {

        const layout = layout_generator(graph_name);

        let local_data = get_data_for_showing_graph(formatted_data, graph_flag);
        layout.title = graph_name;
        layout.xaxis.autorange = true;
        layout.yaxis.autorange = true;

        Plotly.react(graph_id, local_data, layout);
    }

    let graph_data = [
        {mode: 'lines', line: {color: "#fc7e0d"}},
        {mode: 'lines', line: {color: "#005cfa"}},
        {mode: 'lines', line: {color: "#27c400"}},
        {mode: 'lines', line: {color: "#7e5cec"}},
        {mode: 'lines', line: {color: "#ffdc63"}},
        {mode: 'lines', line: {color: "#c40000"}},
        {mode: 'lines', line: {color: "#28ffcd"}},
    ]
    const raw_data = [...Object.entries(data_for_graph)]
    let formatted_data = raw_data
        .map((el, ind) => el.concat([graph_data[ind]]));
    console.log(formatted_data);
    console.log("***", raw_data)

    if (raw_data[0][1]["time"] && [...raw_data[0][1]["time"]]
        .every(i => Number(i.toString()).toString() === i.toString())) {
        document.getElementById("my_graph_time").style.display = '';
        graph_drawer("my_graph_time", "Время сортировок", "time", formatted_data);
    } else {
        document.getElementById("my_graph_time").style.display = 'none';
    }

    if (raw_data[0][1]["count_of_read"] && [...raw_data[0][1]["count_of_read"]]
        .every(i => Number(i.toString()).toString() === i.toString())) {
        document.getElementById("my_graph_read").style.display = '';

        graph_drawer("my_graph_read", "Количество чтений", "count_of_read", formatted_data);
    } else {
        document.getElementById("my_graph_read").style.display = 'none';
    }

    if (raw_data[0][1]["count_of_write"] && [...raw_data[0][1]["count_of_write"]]
        .every(i => Number(i.toString()).toString() === i.toString())) {
        document.getElementById("my_graph_write").style.display = '';
        graph_drawer("my_graph_write", "Количество записей", "count_of_write", formatted_data);
    } else {
        document.getElementById("my_graph_write").style.display = 'none';
    }


    const is_drawing_item = (ind, all_arr) => ind % Math.max(Math.floor(all_arr.length / 10), 1) === 0

    const target_indexes = {};
    document.getElementById("result_table").innerHTML = `
                <caption>${graph_text}</caption>
                <thead>
                <tr>
                    <th>Количество элементов</th>
                    ${[...Object.keys(Object.values(data_from_server)[0])]
        .reduce(
            (str, el, ind, all_arr) => {
                if (is_drawing_item(ind, all_arr)) {
                    target_indexes[el] = true;
                    return str + "<th>" + el + "</th>\n"
                }
                return str
            }, "")}
                </tr>
                </thead>
                <tbody>
                ${[...Object.entries(data_from_server)].reduce(
        (str, [key, val]) =>
            str + "<tr><td>" + key + "</td>" + [...Object.entries(val)].reduce(
                (last, [k, v]) =>
                    last + "<td><div class='cell_flex_box_parent'>"
                    + "<div class='cell_part_flex_box_parent'><div class='x_left' >Время:</div>" + "<div class='x_right' >" + v['time'] + "</div></div>"
                    + "<div class='cell_part_flex_box_parent'><div class='x_left' >Чтений:</div>" + "<div class='x_right' >" + v['count_of_read'] + "</div></div>"
                    + "<div class='cell_part_flex_box_parent'><div class='x_left' >Записей:</div>" + "<div class='x_right' >" + v['count_of_write'] + "</div></div>"
                    + "</td>", ""
            ) + "</div></tr>\n", ""
    )
    }
                </tbody>`;
}