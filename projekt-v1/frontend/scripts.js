document.getElementById('receipt-form').addEventListener('submit', async function(event) {
    event.preventDefault();

    const image = document.getElementById('image').files[0];
    const name = document.getElementById('name').value;
    const category = document.getElementById('category').value;
    const purchaseDate = document.getElementById('purchase-date').value;
    const entryDate = document.getElementById('entry-date').value;

    const formData = new FormData();
    formData.append('file', image);

    try {
        const response = await fetch('http://212.101.137.103:8000/upload', {
            method: 'POST',
            body: formData,
        });
        if (!response.ok) {
            throw new Error('Network response was not ok');
        }
        const result = await response.json();

        const receiptData = {
            image_url: result.filename, // Ensure this is correct
            name,
            category,
            purchase_date: purchaseDate,
            entry_date: entryDate,
        };

        const receiptResponse = await fetch('http://212.101.137.103:8000/receipts/', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify(receiptData),
        });

        if (!receiptResponse.ok) {
            throw new Error('Network response was not ok');
        }

        const newReceipt = await receiptResponse.json();
        displayReceipt(newReceipt);
    } catch (error) {
        console.error('There was a problem with the fetch operation:', error);
    }
});

function displayReceipt(receipt) {
    const receiptsList = document.getElementById('receipts-list');
    const receiptRow = document.createElement('tr');

    receiptRow.innerHTML = `
        <td><a href="http://212.101.137.103:8000/${receipt.image_url}" target="_blank"><img src="http://212.101.137.103:8000/${receipt.image_url}" alt="${receipt.name}" /></a></td>
        <td>${receipt.name}</td>
        <td>${receipt.category}</td>
        <td>${receipt.purchase_date}</td>
        <td>${receipt.entry_date}</td>
    `;

    receiptsList.appendChild(receiptRow);
}

// Fetch and display existing receipts on page load
async function fetchReceipts() {
    try {
        const response = await fetch('http://212.101.137.103:8000/receipts/');
        const receipts = await response.json();
        receipts.forEach(receipt => {
            displayReceipt(receipt);
        });
    } catch (error) {
        console.error('There was a problem with fetching receipts:', error);
    }
}

// Fetch existing receipts when the page loads
window.onload = fetchReceipts;

// Add event listener for the delete button
document.getElementById('delete-all').addEventListener('click', async function() {
    try {
        const response = await fetch('http://212.101.137.103:8000/receipts/', {
            method: 'DELETE',
        });
        if (!response.ok) {
            throw new Error('Network response was not ok');
        }
        document.getElementById('receipts-list').innerHTML = ''; // Clear the table
        alert('All receipts have been deleted.');
    } catch (error) {
        console.error('There was a problem with the delete operation:', error);
    }
});
