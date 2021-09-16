let arr = [];
setTimeout(() => {
    let i = 0;
    while (i <  10e5){
        // arr.push(Math.random().toString().substr(3, 7));
        arr.push(i)
        i++;
    }
    // arr.sort()
    // arr = arr.map(i => parseInt(i));
    console.log(arr);
})
const count_iter = 10000;

const processing = id_element => {
    const key = Number(document.getElementById(id_element).value);

    console.time('time_1');
    let [index, time] = consistent_search(key);
    console.timeEnd('time_1');
    time = Math.round(time);


    document.getElementById("time_1").textContent = `${time} ms`;
    document.getElementById("index_1").textContent = index.toString();

    console.time('time_2');
    [index, time] = binary_search(key);
    console.timeEnd('time_2');
    time = Math.round(time);


    document.getElementById("time_2").textContent = `${time} ms`;
    document.getElementById("index_2").textContent = index.toString();

    console.time('time_3');
    [index, time] = opt_binary_search(key);
    console.timeEnd('time_3');
    time = Math.round(time);

    document.getElementById("time_3").textContent = `${time} ms`;
    document.getElementById("index_3").textContent = index.toString();

    console.time('time_4');
    [index, time] = inter_binary_search(key);
    console.timeEnd('time_4');
    time = Math.round(time);

    document.getElementById("time_4").textContent = `${time} ms`;
    document.getElementById("index_4").textContent = index.toString();

    console.time('time_5');
    [index, time] = opt_inter_binary_search(key);
    console.timeEnd('time_5');
    time = Math.round(time);

    document.getElementById("time_5").textContent = `${time} ms`;
    document.getElementById("index_5").textContent = index.toString();
    console.log("------------------------");

}



const consistent_search = element => {
    arr.push(element + 1)
    const start_time = performance.now();
    let i = 0;
    let ans;
    let index = 0;
    let current_el = arr[index];
    while (i < count_iter) {
        index = 0;
        current_el = arr[index];
        while (element > current_el) {
            index++;
            current_el = arr[index];
        }
        i++;
    }
    if (current_el === element) {
        ans = [index, performance.now() - start_time];
    } else {
        ans = ["Не найден", performance.now() - start_time];
    }

    arr.pop();
    return ans
}


const binary_search = element => {
    arr.push(element + 1);
    const start_time = performance.now();
    let i = 0;
    let ans;
    let L = 0;
    let R = arr.length -1;
    let current_el;
    let current_ind;
    while (i < count_iter) {
        L = 0;
        R = arr.length - 1;
        current_el = null;
        current_ind = null;

        while (L <= R) {
            current_ind = Math.floor((L + R) / 2);
            current_el = arr[current_ind];
            if (current_el == element) {
                break
            } else if (element < current_el) {
                R = current_ind - 1
            } else {
                L = current_ind + 1
            }
        }
        i++;

    }
    if (current_el === element) {
        ans = [current_ind, performance.now() - start_time];
    } else {
        ans = ["Не найден", performance.now() - start_time];
    }
    arr.pop();
    return ans

}


const opt_binary_search = element => {
    arr.push(element + 1);
    const start_time = performance.now();
    let i = 0;
    let ans;
    let L = 0;
    let R = arr.length - 1;
    let current_el;
    let current_ind;
    while (i < count_iter) {
        L = 0;
        R = arr.length - 1;
        current_el = null;
        current_ind = null;

        while (L < R) {
            current_ind = Math.floor((L + R) / 2);
            current_el = arr[current_ind];
            if (element <= current_el) {
                R = current_ind
            } else {
                L = current_ind + 1
            }
        }
        i++;
    }
    // current_ind = Math.floor((L + R) / 2);
    // current_el = arr[current_ind];
    if (arr[R] === element) {
        ans = [current_ind, performance.now() - start_time];
    } else {
        ans = ["Не найден", performance.now() - start_time];
    }
    arr.pop();
    return ans
}


const inter_binary_search = element => {
    arr.push(element + 1);
    const start_time = performance.now();
    let i = 0;
    let ans;
    let L = 0;
    let R = arr.length -1;
    let current_el;
    let current_ind;
    while (i < count_iter) {
        L = 0;
        R = arr.length -1;
        current_el = null;
        current_ind = null;

        while (L <= R) {
            current_ind = Math.round(L + (element - arr[L]) * (R - L) / (arr[R] - arr[L]));
            current_el = arr[current_ind];
            if (current_el == element) {
                break
            } else if (element < current_el) {
                R = current_ind - 1
            } else {
                L = current_ind + 1
            }
        }
        i++;

    }
    if (current_el === element) {
        ans = [current_ind, performance.now() - start_time];
    } else {
        ans = ["Не найден", performance.now() - start_time];
    }
    arr.pop();
    return ans

}


const opt_inter_binary_search = element => {
    arr.push(element + 1);
    const start_time = performance.now();
    let i = 0;
    let ans;
    let L = 0;
    let R = arr.length -1;
    let current_el;
    let current_ind;
    while (i < count_iter) {
        L = 0;
        R = arr.length - 1;
        current_el =  null;
        current_ind = null;
        let k = null
        while (L < R) {

            current_ind = Math.round(L + (R - L) * (element - arr[L]) / (arr[R] - arr[L]));
            current_el = arr[current_ind];

            if (element <= current_el) {
                R = current_ind;
            } else {
                L = current_ind + 1;
            }

            if (L >= R){
                break
            }

            current_ind = Math.round(L + (R - L) * (element - arr[L]) / (arr[R] - arr[L]));
            current_el = arr[current_ind];

            if (element < current_el) {
                R = current_ind - 1;
            } else {
                L = current_ind;
            }

        }
        i++;
    }
    // current_ind = Math.round(L + ((element - arr[L]) * (R - L) / (arr[R] - arr[L])));
    // current_el = arr[current_ind];
    if (arr[R] === element) {
        ans = [current_ind, performance.now() - start_time];
    } else {
        ans = ["Не найден", performance.now() - start_time];
    }
    arr.pop();
    return ans
}

console.log(arr);
console.log("parseInt(\"000003\") is", parseInt("000003"));