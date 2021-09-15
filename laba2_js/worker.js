const arr = Array.apply(null, new Array(10e0)).map(ind=>Math.round(Math.random()*10e6))
arr.sort()
const processing = id_element => {
    const key = document.getElementById(id_element).value

}