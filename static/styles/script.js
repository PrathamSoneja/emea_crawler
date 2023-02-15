const options = document.querySelector('.options');
const select = document.querySelector('#select');

// button
const button = document.querySelector('#btn');

// input files
const first_file = document.querySelector('#first-file');
const second_file = document.querySelector('#second-file');

// option to shows the input file data
// function myFunction() {
// document.getElementsByClassName("hi").style.backgroundImage = "url(https://images.pexels.com/photos/255379/pexels-photo-255379.jpeg?auto=compress&cs=tinysrgb&w=1260&h=750&dpr=1)";
// }
// const images = ['https://c1.wallpaperflare.com/preview/740/70/428/white-aesthetic-table-vase.jpg', 'https://c4.wallpaperflare.com/wallpaper/271/986/465/nature-plants-macro-depth-of-field-wallpaper-preview.jpg', 'https://images.pexels.com/photos/992734/pexels-photo-992734.jpeg?auto=compress&cs=tinysrgb&w=1260&h=750&dpr=1','https://c0.wallpaperflare.com/preview/265/77/78/apple-macbook-laptop-minimum.jpg','https://c0.wallpaperflare.com/preview/190/14/367/plant-windowsill-pot-succulent.jpg'];
// let currentIndex = 0;

// function changeBackground() {
//   document.getElementById('bg').style.backgroundImage = `url(${images[currentIndex]})`;
//   currentIndex = (currentIndex + 1) % images.length;
// }

// setInterval(changeBackground, 8000);
options.addEventListener('click', () => {
    if (select.value != 'null')
        document.querySelector('.data').classList.remove('hidden');

});

button.addEventListener('click', () => {
    if (first_file.files.length == 0 || second_file.files.length == 0) {
        alert("File are empty");
    }
});



function addTable(key, e) {
    const div = document.createElement('div');
    div.className = 'dataForOne';

    const para = document.createElement('p');
    para.className = 'paraForData';

    let table = document.createElement("table");
    let tableBody = document.createElement("tbody");

    let row = document.createElement("tr");

    data[e.target.innerText.toLowerCase()][0].forEach((item, index) => {

        if (index % 10 == 0) {
            row = document.createElement('tr');
            tableBody.appendChild(row);
        }

        const cell = document.createElement('td');
        cell.innerHTML = item;
        cell.addEventListener('click', (e) => {
            if (cell.style.backgroundColor == "red") {
                cell.style.removeProperty('background-color');

            }
            else
                cell.style.backgroundColor = "red";
        });
        // function myFunction() {
        //  }
        row.appendChild(cell);
        tableBody.appendChild(row);
    });

    table.appendChild(tableBody);
    para.appendChild(table);

    const label = document.createElement('label');
    label.className = 'lableForData';
    label.innerHTML = key;

    div.append(label, para);

    dataToShow.appendChild(div);
}


if (data != '{{ dataFromFlask|safe }}') {

    const keys = Object.keys(data);
    const dataTOShow = document.querySelector('.btn-show');

    keys.forEach(key => {
        if (data[key].length != 0) {
            const btn = document.createElement('button');
            btn.className = 'btn';
            btn.innerText = key;
            btn.innerHTML = key;
            dataTOShow.appendChild(btn);

            btn.addEventListener('click', (e) => {
                const dataToShow = document.querySelector('#dataToShow');
                dataToShow.innerHTML = '';


                if (e.target.innerText.toLowerCase().includes('indices')) {
                    addTable(key, e);
                }
                else {

                    const innerKeys = Object.keys(data[e.target.innerText.toLowerCase()][0]);
                    const innerValues = Object.values(data[e.target.innerText.toLowerCase()][0]);
                    innerKeys.forEach((key, index) => {

                        const div = document.createElement('div');
                        div.className = 'dataForOne';

                        const para = document.createElement('p');
                        para.className = 'paraForData';

                        let table = document.createElement("table");
                        table.style.width = '500px';
                        let tableBody = document.createElement("tbody");

                        let outer_row = document.createElement("tr");

                        const outer_cell = document.createElement('td');

                        if (innerValues[index].length > 1) {
                            innerValues[index].forEach((item, index) => {

                                let inner_row = document.createElement('tr');
                                let inner_cell = document.createElement('td');

                                inner_cell.innerHTML = item;
                                inner_cell.style.width = '500px';

                                inner_row.appendChild(inner_cell);
                                outer_cell.appendChild(inner_row);

                                inner_cell.addEventListener('click', (e) => {
                                    if (inner_cell.style.backgroundColor == "red") {
                                        inner_cell.style.removeProperty('background-color');
                                    }
                                    else
                                        inner_cell.style.backgroundColor = "red";
                                });
                            });
                        } else {
                            outer_cell.innerHTML = innerValues[index];
                            outer_cell.addEventListener('click', (e) => {
                                if (outer_cell.style.backgroundColor == "red") {
                                    outer_cell.style.removeProperty('background-color');
                                }
                                else
                                    outer_cell.style.backgroundColor = "red";
                            });
                        }
                        outer_row.appendChild(outer_cell);
                        tableBody.appendChild(outer_row);
                        table.appendChild(tableBody);
                        para.appendChild(table);

                        const label = document.createElement('label');
                        label.className = 'lableForData';
                        label.innerHTML = key;

                        div.append(label, para);

                        dataToShow.appendChild(div);

                    });
                }
            });
        }
    });
}