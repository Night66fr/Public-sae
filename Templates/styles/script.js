let allParkings = {}; 
let allVelos = {};
let chartInstance = null;

const locations = {
    "Antigone": [43.6074, 3.8885],
    "Arc de Triomphe": [43.6110, 3.8731],
    "Charles de Gaulle": [43.6145, 3.8815],
    "Circe": [43.6046, 3.9218],
    "Comedie": [43.6085, 3.8802],
    "Corum": [43.6131, 3.8821],
    "Euromedecine": [43.6390, 3.8280],
    "Europa": [43.6033, 3.8942],
    "Foch": [43.6108, 3.8761],
    "Gambetta": [43.6063, 3.8712],
    "Garcia Lorca": [43.5905, 3.8905],
    "Gare": [43.6036, 3.8790],
    "GAUMONT EST": [43.6050, 3.9230],
    "GAUMONT OUEST": [43.6040, 3.9195],
    "Gaumont-Circe": [43.6045, 3.9215],
    "Montpellier": [43.6110, 3.8767],
    "Mosson": [43.6165, 3.8190],
    "Occitanie": [43.6345, 3.8490],
    "Pitot": [43.6130, 3.8715],
    "Polygone": [43.6103, 3.8858],
    "Sabines": [43.5835, 3.8600],
    "Sablassou": [43.6340, 3.9500],
    "Saint Jean Le Sec": [43.6170, 3.9280],
    "Triangle": [43.6095, 3.8830],
    "Vicarello": [43.6100, 3.8800],
    "Aiguelongue": [43.6262, 3.8970],
    "Albert 1er - Cathédrale": [43.6140, 3.8730],
    "Antigone centre": [43.6075, 3.8905],
    "Beaux-Arts": [43.6165, 3.8850],
    "Boutonnet": [43.6225, 3.8725],
    "Celleneuve": [43.6120, 3.8310],
    "Charles Flahault": [43.6210, 3.8700],
    "Cité Mion": [43.6025, 3.8860],
    "Comedie Baudin": [43.6080, 3.8815],
    "Comédie": [43.6089, 3.8803],
    "Corum (V)": [43.6136, 3.8824],
    "Deux Ponts - Gare Saint-Roch": [43.6040, 3.8825],
    "Emile Combes": [43.6185, 3.8935],
    "Euromédecine": [43.6385, 3.8275],
    "Fac de Lettres": [43.6300, 3.8680],
    "FacdesSciences": [43.6315, 3.8635],
    "Halles Castellane": [43.6095, 3.8770],
    "Hôtel de Ville": [43.5991, 3.8968],
    "Hôtel du Département": [43.6220, 3.8360],
    "Jardin de la Lironde": [43.6000, 3.9170],
    "Jean de Beins": [43.6098, 3.8838],
    "Jeu de Mail des Abbés": [43.6200, 3.8900],
    "Les Arceaux": [43.6125, 3.8685],
    "Les Aubes": [43.6145, 3.8955],
    "Louis Blanc": [43.6150, 3.8785],
    "Malbosc": [43.6335, 3.8335],
    "Marie Caizergues": [43.6190, 3.8760],
    "Médiathèque Emile Zola": [43.6075, 3.8955],
    "Nombre d'Or": [43.6078, 3.8890],
    "Nouveau Saint-Roch": [43.5995, 3.8755],
    "Observatoire": [43.6065, 3.8775],
    "Odysseum": [43.6030, 3.9235],
    "Parvis Jules Ferry - Gare Saint-Roch": [43.6050, 3.8815],
    "Place Albert 1er - St Charles": [43.6167, 3.8732],
    "Place Viala": [43.6135, 3.8540],
    "Plan Cabanes": [43.6083, 3.8688],
    "Pont de Lattes - Gare Saint-Roch": [43.6045, 3.8805],
    "Port Marianne": [43.6005, 3.9055],
    "Providence - Ovalie": [43.5880, 3.8510],
    "Prés d Arènes": [43.5900, 3.8940],
    "Père Soulas": [43.6210, 3.8580],
    "Pérols Etang de l Or": [43.5590, 3.9610],
    "Renouvier": [43.6030, 3.8680],
    "Richter": [43.5985, 3.8995],
    "Rondelet": [43.6035, 3.8745],
    "Rue Jules Ferry - Gare Saint-Roch": [43.6053, 3.8813],
    "Saint-Denis": [43.6055, 3.8720],
    "Saint-Guilhem - Courreau": [43.6092, 3.8735],
    "Sud De France": [43.5955, 3.9231],
    "Tonnelles": [43.6135, 3.8355],
    "Vert Bois": [43.6350, 3.8710],
    "Voltaire": [43.6040, 3.8895]
};

const map = L.map('map').setView([43.6107, 3.8767], 13);
L.tileLayer('https://{s}.basemaps.cartocdn.com/light_all/{z}/{x}/{y}{r}.png').addTo(map);
let markersLayer = L.layerGroup().addTo(map);

const clean = (v) => typeof v === 'string' ? parseFloat(v.replace('%', '')) : parseFloat(v);

async function loadData() {
    try {
        const [resP, resV] = await Promise.all([
            fetch('../../Data-processing/Donnée_SAE_Parking'),
            fetch('../../Data-processing/Donnée_SAE_velo')
        ]);
        const dataP = await resP.json();
        const dataV = await resV.json();

        allParkings = {}; allVelos = {};
        dataP.forEach(e => {
            if (!allParkings[e.id]) allParkings[e.id] = [];
            if (e.place) allParkings[e.id].push(clean(e.place.occupation));
        });
        dataV.forEach(e => {
            if (!allVelos[e.id]) allVelos[e.id] = [];
            if (e.place) allVelos[e.id].push(clean(e.place.occupation));
        });

        document.getElementById('total-parkings').innerText = Object.keys(allParkings).length;
        document.getElementById('total-velos').innerText = Object.keys(allVelos).length;

        const pSel = document.getElementById('select-parking');
        const vSel = document.getElementById('select-velo');
        pSel.innerHTML = ""; vSel.innerHTML = "";
        Object.keys(allParkings).sort().forEach(id => pSel.add(new Option(id, id)));
        Object.keys(allVelos).sort().forEach(id => vSel.add(new Option(id, id)));

        updateAnalysis();
    } catch (err) { console.error(err); }
}

function updateAnalysis() {
    const pId = document.getElementById('select-parking').value;
    const vId = document.getElementById('select-velo').value;
    const mode = document.getElementById('view-mode').value;

    markersLayer.clearLayers();
    Object.keys(locations).forEach(name => {
        const isSelected = (name === pId || name === vId);
        if (allParkings[name] || allVelos[name]) {
            L.circleMarker(locations[name], {
                radius: isSelected ? 12 : 6,
                color: allParkings[name] ? '#1e293b' : '#f97316',
                fillOpacity: isSelected ? 1 : 0.3,
                weight: isSelected ? 4 : 1
            }).addTo(markersLayer).bindPopup(name);
        }
    });

    let dP = allParkings[pId] || [];
    let dV = allVelos[vId] || [];
    document.getElementById('correlation-val').innerText = calculateCorrelation(dP, dV);

    if (mode === "average") { dP = getAvg(dP); dV = getAvg(dV); }

    if (chartInstance) chartInstance.destroy();
    chartInstance = new Chart(document.getElementById('mainChart'), {
        type: 'line',
        data: {
            labels: dP.map((_, i) => mode === "average" ? i + "h" : i + 1),
            datasets: [
                { label: 'Parking %', data: dP, borderColor: '#1e293b', tension: 0.2, pointRadius: 0 },
                { label: 'Vélo %', data: dV, borderColor: '#f97316', tension: 0.2, pointRadius: 0 }
            ]
        },
        options: { responsive: true, maintainAspectRatio: false }
    });
}

function getAvg(arr) {
    let res = new Array(24).fill(0), count = new Array(24).fill(0);
    arr.forEach((v, i) => { res[i % 24] += v; count[i % 24]++; });
    return res.map((v, i) => count[i] > 0 ? (v / count[i]).toFixed(2) : 0);
}

function calculateCorrelation(d1, d2) {
    const n = Math.min(d1.length, d2.length);
    if (n < 2) return "0.000";
    const m1 = d1.reduce((a, b) => a + b, 0) / n;
    const m2 = d2.reduce((a, b) => a + b, 0) / n;
    let num = 0, den1 = 0, den2 = 0;
    for (let i = 0; i < n; i++) {
        num += (d1[i] - m1) * (d2[i] - m2);
        den1 += Math.pow(d1[i] - m1, 2);
        den2 += Math.pow(d2[i] - m2, 2);
    }
    const r = num / Math.sqrt(den1 * den2);
    return isNaN(r) ? "0.000" : r.toFixed(3);
}

function openCorrelationModal() {
    const modal = document.getElementById('corrModal');
    const listDiv = document.getElementById('corr-list');
    modal.style.display = "block";
    listDiv.innerHTML = "Calcul en cours...";

    setTimeout(() => {
        let scores = [];
        const pIds = Object.keys(allParkings);
        const vIds = Object.keys(allVelos);

        pIds.forEach(p => {
            vIds.forEach(v => {
                const r = calculateCorrelation(allParkings[p], allVelos[v]);
                scores.push({ p, v, r: parseFloat(r) });
            });
        });

        scores.sort((a, b) => Math.abs(b.r) - Math.abs(a.r));

        let html = '<table class="corr-table"><tr><th>Rang</th><th>Parking</th><th>Vélo</th><th>Pearson</th></tr>';
        scores.slice(0, 30).forEach((s, i) => {
            html += `<tr><td>#${i+1}</td><td>${s.p}</td><td>${s.v}</td><td><span class="score-badge">${s.r.toFixed(3)}</span></td></tr>`;
        });
        html += '</table>';
        listDiv.innerHTML = html;
    }, 100);
}

function closeCorrelationModal() {
    document.getElementById('corrModal').style.display = "none";
}

loadData();