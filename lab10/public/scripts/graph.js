let layout = {
    title: 'Типы сортировок',
    uirevision: 'true',
    xaxis: {autorange: true},
    yaxis: {autorange: true}
};

Plotly.react('my_graph', [], layout);

const updating_graph_data = ([key, value, default_obj], index) => {
    // console.log(key, value, default_obj, index)
    return Object.assign(default_obj, {
        x: [...Object.keys(value)],
        y: [...Object.values(value)],
        name: key
    })
}

const get_data_for_showing_graph = (formatted_data, flag) => {
    return formatted_data
        .map(([key, value, default_obj], index) => {
            const new_value = {};
            [...value["size"]].map((item, index) => {
                new_value[item] = value[flag][index];
            });
            // console.log(key, value, default_obj);
            // [...Object.entries(value)].map(([k, v]) => {
            //     new_value[v["size"]] = v[flag];
            // });
            return [key, new_value, default_obj]
        })
        .map(updating_graph_data);
}

const draw_graph = (data_for_graph, sort_data, graph_text = "Типы сортировок") => {

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
    let local_data = get_data_for_showing_graph(formatted_data, "time");
    console.log(local_data);
    layout.title = graph_text;
    console.log(layout.title)
    layout.xaxis.autorange = true;
    layout.yaxis.autorange = true;

    // not changing uirevision will ensure that user interactions are unchanged
    // layout.uirevision = rand();

    Plotly.react('my_graph', local_data, layout);

    const is_drawing_item = (ind, all_arr) => ind % Math.max(Math.floor(all_arr.length / 10), 1) === 0

    const target_indexes = {};
    document.getElementById("result_table").innerHTML = `
                <caption>${graph_text}</caption>
                <thead>
                <tr>
                    <th>Количество элементов</th>
                    ${[...Object.keys(raw_data[0][1])]
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
                ${raw_data.reduce(
        (str, [key, val]) =>
            str + "<tr><td>" + key + "</td>" + [...Object.keys(target_indexes)].reduce(
                (last, number_) =>
                    last + "<td>" + Math.round(val[Number(number_)] * 1000) + "</td>", ""
            ) + "</tr>\n", ""
    )
    }
                </tbody>`;
}