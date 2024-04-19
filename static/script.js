let networkDiv = document.getElementById("networks");
let networks;
function scanNetworks() {
    fetch('/api/scan', {})
        .then(async res => {
            // Handle Fetch response here.
            networks = await res.json();
            for (let i = 0; i < networks.length; i++) {
                let line = document.createElement("p");
                line.textContent = network[i];
                networkDiv.appendChild(line);
            }
        })
        .catch(error => {
            // If there's an error, handle it here
        })
}

async function fetchData() {
    try {
        const response = await fetch('/api/scan');
        const data = await response.json();
        return data;
    } catch (error) {
        console.error('Error fetching data:', error);
    }
}

function buildNetworkList(jsonData) {
    const container = document.createElement('div');

    // Loop through each item in the JSON data
    jsonData.forEach(item => {
        // Create elements based on each item
        const itemElement = document.createElement('div');
        itemElement.classList.add('item');

        const titleElement = document.createElement('h2');
        titleElement.textContent = item[0];

        const descriptionElement = document.createElement('p');
        descriptionElement.textContent = item[1];

        // Append elements to the container
        itemElement.appendChild(titleElement);
        itemElement.appendChild(descriptionElement);
        container.appendChild(itemElement);
    });

    // Append the container to the document
    document.body.appendChild(container);
}

function scanNetworks() {
    fetchData()
    .then(data => {
        // Call the function to create HTML elements from the fetched JSON data
        buildNetworkList(data);
    })
    .catch(error => {
        console.error('Error:', error);
    });
}

