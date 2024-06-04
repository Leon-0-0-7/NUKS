async function uploadFile() {
    const formData = new FormData();
    formData.append('file', document.querySelector('input[type="file"]').files[0]);
    formData.append('category', document.getElementById('category').value);
    formData.append('description', document.getElementById('description').value);
    formData.append('purchase_date', document.getElementById('purchase-date').value); // Add purchase_date field
    formData.append('entry_date', document.getElementById('entry-date').value); // Add entry_date field
   

    try {
        const response = await fetch('/upload-bill', {
            method: 'POST',
            body: formData,
        });
        if (response.ok) {
            alert('File uploaded successfully');
            location.reload(); // Refresh the page to update the file list
        } else {
            throw new Error('Failed to upload file');
        }
    } catch (error) {
        console.error(error);
        alert('An error occurred while uploading the file');
    }
}
function displayReceipt(receipt) {
    const receiptsList = document.getElementById('receipts-list');
    const receiptRow = document.createElement('tr');

    receiptRow.innerHTML = `
        <td><a href="/show/${receipt.description}" target="_blank"><img src="/show/${receipt.description}" alt="${receipt.description}" /></a></td>
        <td>${receipt.description}</td>
        <td>${receipt.category}</td>
        <td>${receipt.purchase_date}</td>
        <td>${receipt.entry_date}</td>
    `;

    receiptsList.appendChild(receiptRow);
}

// Fetch and display existing receipts on page load
async function fetchReceipts() {
    try {
        const response = await fetch('/api/bills');
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

document.getElementById("delete-all").addEventListener("click", async function() {
    try {
        const response = await fetch('/delete-all', {
            method: 'DELETE',
        });
        if (response.ok) {
            alert('All receipts deleted successfully');
            location.reload(); // Refresh the page to update the file list
        } else {
            throw new Error('Failed to delete receipts');
        }
    } catch (error) {
        console.error(error);
        alert('An error occurred while deleting the receipts');
    }
});
