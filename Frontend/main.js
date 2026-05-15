let priceChart = null;

function loadPriceData(productId, days) {
    const url = `http://127.0.0.1:5000/api/price?product_id=${productId}&days=${days}`;
    fetch(url)
    .then(r => r.json())
    .then(prices => {
        const tbody = document.getElementById('price-body');
        tbody.innerHTML = '';
        prices.forEach(row => {
            const tr = document.createElement('tr');
            tr.innerHTML = `
                <td>${row.date}</td>
                <td>${parseFloat(row.price).toFixed(2)}</td>
                <td>${row.unit}</td>
            `;
            tbody.appendChild(tr);
        });

        const labels = prices.map(r => r.date);
        const data = prices.map(r => r.price);
        if (priceChart) priceChart.destroy();
        const ctx = document.getElementById('price-chart').getContext('2d');
        priceChart = new Chart(ctx, {
            type: 'line',
            data: {
                labels: labels,
                datasets: [{
                    label: 'Giá',
                    data: data,
                    borderColor: '#2d6b5e',
                    tension: 0.3,
                    fill: false
                }]
            }
        });
    });
}

// Load product dropdown
fetch('http://127.0.0.1:5000/api/product')
.then(r => r.json())
.then(products => {
    const select = document.getElementById('product-filter');
    products.forEach(p => {
        const option = document.createElement('option');
        option.value = p.id;
        option.text = p.name;
        select.appendChild(option);
    });
    loadPriceData(select.value, 30);
});

// Load news
fetch('http://127.0.0.1:5000/api/news')
.then(r => r.json())
.then(news => {
    const newsTbody = document.getElementById('news-body');
    news.forEach(row => {
        const tr = document.createElement('tr');
        tr.innerHTML = `
            <td>${row.title}</td>
            <td>${row.category}</td>
            <td>${row.date}</td>
        `;
        newsTbody.appendChild(tr);
    });
});

// Load economic
fetch('http://127.0.0.1:5000/api/economic')
.then(r => r.json())
.then(economic => {
    const reportTbody = document.getElementById('report-body');
    economic.forEach(row => {
        const tr = document.createElement('tr');
        tr.innerHTML = `
            <td>${row.name || '-'}</td>
            <td>${row.value || '-'}</td>
            <td>${row.unit || '-'}</td>
            <td>${row.category || '-'}</td>
            <td>${row.date || '-'}</td>
        `;
        reportTbody.appendChild(tr);
    });
});

// Filter button
document.getElementById('filter-btn').addEventListener('click', () => {
    const productId = document.getElementById('product-filter').value;
    const days = document.getElementById('days-filter').value;
    loadPriceData(productId, days);
});

// Navbar
const navLinks = document.querySelectorAll('nav a');
const sections = document.querySelectorAll('section');
navLinks.forEach(link => {
    link.addEventListener('click', function(e) {
        e.preventDefault();
        sections.forEach(s => s.classList.remove('active'));
        document.querySelector(this.getAttribute('href')).classList.add('active');
    });
});