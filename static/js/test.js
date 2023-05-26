let limit = 3;

function pre() {
    window.location.href = '/applications/?limit=' + limit;
}

function next() {
    window.location.href = '/applications/?limit=' + limit
}
function test() {

    $("#test").on('change keydown paste input', function (e) {
        limit = (e.target.value);
        window.location.href = '/applications/?page={{page_apps.page_number-1}}&limit' = '+limit

    })
}

console.log('working');
function deleteRow() {
    let table = document.getElementById("applicationtable");
    table.deleteRow(0)
}
function insertRow() {
    let table = document.getElementById("applicationtable");
    let row = table.insertRow(-1);
    // Create table cells
    let c1 = row.insertCell(0);
    let c2 = row.insertCell(1);
    let c3 = row.insertCell(2);
    let c4 = row.insertCell(3)
    let c5 = row.insertCell(4)
    let c6 = row.insertCell(5)
    // Add data to c1 and c2
    console.log({{ applications| length}});

c1.innterText = 45
c2.innerText = 45
c3.innerText = "Houston"
c4.innerText = "Houston"
c3.innerText = "Houston"
// Append row to table body
table.appendChild(row)
}
async function logJSONData() {
    const response = await fetch("http://127.0.0.1:8001/jobs/applications/?page=1&limit=10");
    const jsonData = await response.json();
    console.log(jsonData);
}
logJSONData();