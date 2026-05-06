// Fetch cả product và price cùng lúc
Promise.all([
    fetch('http://127.0.0.1:5000/api/product').then(r => r.json()),
    fetch('http://127.0.0.1:5000/api/price').then(r => r.json()),
    fetch('http://127.0.0.1:5000/api/news').then(r => r.json()),
    fetch('http://127.0.0.1:5000/api/economic').then(r => r.json())
])
.then(([products, prices, news, economic]) => {
    // Tạo map product_id -> name
    const productMap = {};
    products.forEach(p => {
        productMap[p.id] = p.name;
    });

    // Xử lý prices
    const tbody = document.getElementById('price-body');
    prices.forEach(row => {
        const tr = document.createElement('tr');
        tr.innerHTML = `
            <td>${productMap[row.product_id] || row.product_id}</td>
            <td>${row.date}</td>
            <td>${parseFloat(row.price).toFixed(2)}</td>
            <td>${row.unit}</td>
        `;
        tbody.appendChild(tr);
    });

    // Xử lý news — thử tự viết phần này!
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

    // Xử lý economic — thử tự viết phần này!
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

// Ẩn/hiện section khi click navbar
const navLinks = document.querySelectorAll('nav a');
const sections = document.querySelectorAll('section');

navLinks.forEach(link => {
    link.addEventListener('click', function(e) {
        e.preventDefault();
        sections.forEach(s => s.classList.remove('active'));
        const target = this.getAttribute('href');
        document.querySelector(target).classList.add('active');
    });
});
