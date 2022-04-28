const sort_displayed_gen = (sort_type) => {

    const headers = {
        "one": "Однофазная",
        "two": "Двухфазная",
        "selection": "Слиянием"
    }
//+ (sort_type.endsWith("_percent")? " (" + sort_type.split("_")[1] + " процентов)": "")
    const data = `
        <div class="array_box" id="${sort_type}">
            <h2>${
                    [...Object.entries(headers)]
                    .filter(([k, v]) => sort_type.toString().startsWith(k))
                    .map(([k, v]) => v.toString())[0].toString() 
            }</h2>
            <div class="output_box">
                <text>Время (в наносекундах):</text>
                <text id="${sort_type}_time">?</text>
            </div>
            <div class="output_box">
                <text>количество чтений из файла</text>
                <text id="${sort_type}_count_of_read">?</text>
            </div>
            <div class="output_box">
                <text>количество записей в файл</text>
                <text id="${sort_type}_count_of_write">?</text>
            </div>
            <div class="output_box">
                <textarea disabled id="${sort_type}_history"></textarea>
            </div>
        </div>
    `;
    return data;
}