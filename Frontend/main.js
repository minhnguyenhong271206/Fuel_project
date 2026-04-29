// api lay data gia
fetch('http://127.0.0.1:5000/api/price' )

// chuyen response thanh json
.then(response => response.json())

// xu ly data
.then(data => {

    // lay the tbody trong bang
    const tbody= document.getElementById('price-body');

    // Duyet tung dong data
    data.forEach(row => {
        // Tao 1 dong <tr>
        const tr = document.createElement('tr');

        // Thêm các ô <td> vào dòng
        tr.innerHTML = `
            <td>${row.product_id}</td>
            <td>${row.date}</td>
            <td>${row.price}</td>
            <td>${row.unit}</td>
        `;

        // Them dong vao bang
        tbody.appendChild(tr);
    });
});
