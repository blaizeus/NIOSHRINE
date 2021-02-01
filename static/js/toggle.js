var slider = document.querySelector(".toggle")
var month = document.querySelector(".month-span")
var year = document.querySelector(".year-span")
var graph = document.querySelector(".graph-year")
var heading = document.querySelector(".chart-heading")

month.classList.add("selected")
year.classList.add("unselected")

slider.addEventListener('change', function() {
    if(slider.checked == false) {
        month.classList.remove("unselected")
        month.classList.add("selected")
        year.classList.remove("selected")
        year.classList.add("unselected")
        graph.style.zIndex = -1
        heading.innerHTML = "NIO this month"
    }
    else {
        month.classList.remove("selected")
        month.classList.add("unselected")
        year.classList.remove("unselected")
        year.classList.add("selected")
        graph.style.zIndex = 5
        heading.innerHTML = "NIO this year"
    }
})
