let nodes = [];
document.addEventListener('DOMContentLoaded', async () => {
    try {
        // First API call to fetch graph data (matrix and nodes)
        const graphDataResponse = await fetch('http://localhost:8000/route');
        if (!graphDataResponse.ok) {
            throw new Error('Failed to fetch graph data');
        }
        const graphData = await graphDataResponse.json();

        // Draw the graph based on the fetched data
        nodes = graphData.nodes
        drawGraph(graphData);
    } catch (error) {
        console.error('Error:', error.message);
        alert('An error occurred while fetching graph data. Please try again.');
    }
});

document.getElementById('process-json-btn').addEventListener('click', async () => {
    const jsonData = document.getElementById('json-input').value;
    if (!jsonData) {
        alert('Please enter JSON data.');
        return;
    }

    try {
        // Second API call to fetch paths
        const pathsResponse = await fetch('http://localhost:8000/navigate', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: jsonData
        });
        if (!pathsResponse.ok) {
            throw new Error('Failed to fetch paths');
        }
        const pathsData = await pathsResponse.json();

        // Highlight the best path on the graph
        drawBestPath(pathsData.path);
        showDetails(pathsData.odds, pathsData.duration)
    } catch (error) {
        console.error('Error:', error.message);
        alert('An error occurred while fetching paths. Please try again.');
    }
});
;

function drawGraph(data, showLabels = false) {
    const graphComponent = document.querySelector('#graph-component');
    const adjacencyMatrix = data.matrix;

    const elements = [
        ...nodes.map(node => ({data: {id: node}})),
        ...getEdges(adjacencyMatrix, nodes, showLabels)
    ];

    const cy = cytoscape({
        container: graphComponent,
        elements: elements,
        style: [
            {
                selector: 'node',
                style: {
                    'background-color': 'white',
                    'label': 'data(id)',
                    'text-valign': 'center',
                    'color': 'red',
                    'width': 30,
                    'height': 30
                }
            },
            {
                selector: 'edge',
                style: {
                    'width': 2,
                    'line-color': '#D3D3D3',
                    'curve-style': 'bezier'
                }
            },
            {
                selector: "edge[label]",
                css: {
                    "label": "data(label)",
                    "text-rotation": "autorotate",
                    "text-margin-x": "0px",
                    "text-margin-y": "0px"
                }
            }
        ],
        layout: {name: 'random'}
    });

    cy.layout({name: 'cose'}).run();
}

function getEdges(matrix, nodes, showLabel = false) {
    const edges = [];
    const size = nodes.length;

    for (let i = 0; i < size; i++) {
        for (let j = i; j < size; j++) { // Start j from i + 1 to avoid duplicate and self-referencing edges
            if (matrix[i][j] > 0) {
                edges.push({
                    data: {
                        id: `${nodes[i]}-${nodes[j]}`,
                        source: nodes[i],
                        target: nodes[j],
                        label: showLabel ? (matrix[i][j] === 1 ? "" : `Stay ${matrix[i][j]} days`) : ""
                    },
                    style: {}
                });
            }
        }
    }

    return edges;
}

function drawBestPath(bestPath) {
    let matrix = [];
    for (let i = 0; i < nodes.length; i++) {
        let row = [];
        for (let j = 0; j < nodes.length; j++) {
            row.push(0);
        }
        matrix.push(row);
    }

    for (let idx = 1; idx < bestPath.length; idx++) {
        let previous = nodes.indexOf(bestPath[idx - 1]);
        let current = nodes.indexOf(bestPath[idx]);
        matrix[previous][current] += 1; // Update the value for the edge between previous and current nodes
        matrix[current][previous] += 1; // Update the value for the edge between current and previous nodes (if necessary)
    }
    console.log(matrix)

    drawGraph({matrix: matrix}, true);
}


function showDetails(odds, duration) {
    let alertClass = ""
    switch (odds) {
        case 1.0:
            alertClass = "alert-success";
            break
        case 0:
            alertClass = "alert-danger";
            break
        default:
            alertClass = "alert-warning";
            break

    }

    document.querySelector("#path-details").innerHTML = `
    <div class="alert ${alertClass}" role="alert">
        Odds to arrive without being captured: ${odds * 100} %
        Time needed : ${duration !== -1 ? duration : "N/A"}
    </div>
    
    `
}