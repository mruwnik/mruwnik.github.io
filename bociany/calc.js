const diameter = document.getElementById("diameter");
const height = document.getElementById("height");
const density = document.getElementById("density");

function formatNum(num) {
    return num ? (Math.round((num + 0.00001) * 100) / 100) : '';
}

function makeRow(model, values, style){
    [low_95, low_90, low_80, av, high_80, high_90, high_95] = values || [];
    style = style || "light";
    return '<tr class="resultsRow ' + style + '">' +
        `      <td class="model">${model}</td>` +
        `      <td class="low-95 number">${formatNum(low_95)}</td>` +
        `      <td class="low-90 number">${formatNum(low_90)}</td>` +
        `      <td class="low-80 number">${formatNum(low_80)}</td>` +
        `      <td class="avg number">${formatNum(av)}</td>` +
        `      <td class="high-80 number">${formatNum(high_80)}</td>` +
        `      <td class="high-90 number">${formatNum(high_90)}</td>` +
        `      <td class="high-95 number">${formatNum(high_95)}</td>` +
        '</tr>';
}

function updateResults(results) {
    const rowsContainer = document.getElementById("resultsRows");
    rowsContainer.innerHTML = models.reduce(function(rows, model, i) {
        var style = (i % 2 ? 'light' : 'dark');
        return rows + makeRow(model, results[i], style);
    }, '');
}


function updateAvgs() {
    var weight;
    try {
        weight = weights[density.value][Math.round(diameter.value)][Math.round(height.value)];
    } catch(error) {
        console.log(weight);
    }
    updateResults(weight || []);
};

diameter.addEventListener("change", updateAvgs);
height.addEventListener("change", updateAvgs);
density.addEventListener("change", updateAvgs);

updateAvgs();
