// API Base URL
const API_URL = 'http://localhost:8000';

// Global variables
let products = [];
let currentSort = null;
let isEditMode = false;
let editingProductId = null;

// Initialize app
document.addEventListener('DOMContentLoaded', () => {
    loadProducts();
});

// Load all products
async function loadProducts() {
    try {
        showLoading();
        const response = await fetch(`${API_URL}/products/`);
        
        if (!response.ok) {
            throw new Error('Error al cargar productos');
        }
        
        products = await response.json();
        displayProducts(products);
        updateStats(products);
        hideLoading();
    } catch (error) {
        console.error('Error:', error);
        showToast('Error al cargar productos', 'error');
        hideLoading();
        showEmptyState();
    }
}

// Display products in grid
function displayProducts(productsToDisplay) {
    const grid = document.getElementById('productsGrid');
    const emptyState = document.getElementById('emptyState');
    
    if (productsToDisplay.length === 0) {
        grid.style.display = 'none';
        emptyState.style.display = 'block';
        return;
    }
    
    grid.style.display = 'grid';
    emptyState.style.display = 'none';
    
    grid.innerHTML = productsToDisplay.map(product => `
        <div class="product-card" data-id="${product.id}">
            <div class="product-header">
                <div>
                    <h3 class="product-name">${product.nombre}</h3>
                    <span class="product-badge ${getStockBadgeClass(product.stock)}">
                        ${getStockStatus(product.stock)}
                    </span>
                </div>
            </div>
            
            <div class="product-details">
                ${product.talla ? `
                    <div class="product-detail">
                        <i class="fas fa-ruler"></i>
                        <span>Talla: ${product.talla}</span>
                    </div>
                ` : ''}
                
                ${product.color ? `
                    <div class="product-detail">
                        <i class="fas fa-palette"></i>
                        <span>Color: ${product.color}</span>
                    </div>
                ` : ''}
                
                <div class="product-detail">
                    <i class="fas fa-boxes"></i>
                    <span>Stock: ${product.stock || 0} unidades</span>
                </div>
                
                ${product.proveedor ? `
                    <div class="product-detail">
                        <i class="fas fa-truck"></i>
                        <span>${product.proveedor}</span>
                    </div>
                ` : ''}
            </div>
            
            <div class="product-price">
                $${parseFloat(product.precio).toFixed(2)}
            </div>
            
            <div class="product-actions">
                <button class="btn btn-success" onclick="editProduct(${product.id})">
                    <i class="fas fa-edit"></i> Editar
                </button>
                <button class="btn btn-danger" onclick="confirmDelete(${product.id})">
                    <i class="fas fa-trash"></i> Eliminar
                </button>
            </div>
        </div>
    `).join('');
}

// Get stock status
function getStockStatus(stock) {
    if (!stock || stock === 0) return 'Sin Stock';
    if (stock < 10) return 'Stock Bajo';
    return 'En Stock';
}

// Get stock badge class
function getStockBadgeClass(stock) {
    if (!stock || stock === 0) return 'badge-out-stock';
    if (stock < 10) return 'badge-low-stock';
    return 'badge-in-stock';
}

// Update statistics
function updateStats(products) {
    const totalProducts = products.length;
    const totalStock = products.reduce((sum, p) => sum + (p.stock || 0), 0);
    const avgPrice = products.length > 0 
        ? products.reduce((sum, p) => sum + parseFloat(p.precio), 0) / products.length 
        : 0;
    const totalValue = products.reduce((sum, p) => sum + (parseFloat(p.precio) * (p.stock || 0)), 0);
    
    document.getElementById('totalProducts').textContent = totalProducts;
    document.getElementById('totalStock').textContent = totalStock;
    document.getElementById('avgPrice').textContent = `$${avgPrice.toFixed(2)}`;
    document.getElementById('totalValue').textContent = `$${totalValue.toFixed(2)}`;
}

// Filter products by search
function filterProducts() {
    const searchTerm = document.getElementById('searchInput').value.toLowerCase();
    
    const filtered = products.filter(product => {
        return (
            product.nombre.toLowerCase().includes(searchTerm) ||
            (product.color && product.color.toLowerCase().includes(searchTerm)) ||
            (product.proveedor && product.proveedor.toLowerCase().includes(searchTerm)) ||
            (product.talla && product.talla.toLowerCase().includes(searchTerm))
        );
    });
    
    displayProducts(filtered);
}

// Sort products
function sortProducts(field) {
    const buttons = document.querySelectorAll('.filter-btn');
    buttons.forEach(btn => btn.classList.remove('active'));
    event.target.closest('.filter-btn').classList.add('active');
    
    const sorted = [...products].sort((a, b) => {
        if (field === 'nombre') {
            return a.nombre.localeCompare(b.nombre);
        } else if (field === 'precio') {
            return parseFloat(a.precio) - parseFloat(b.precio);
        } else if (field === 'stock') {
            return (b.stock || 0) - (a.stock || 0);
        }
        return 0;
    });
    
    displayProducts(sorted);
}

// Filter by category
function filterByCategory(category) {
    const buttons = document.querySelectorAll('.filter-btn');
    buttons.forEach(btn => btn.classList.remove('active'));
    event.target.classList.add('active');
    
    if (category === 'all') {
        displayProducts(products);
    }
}

// Open modal for create/edit
function openModal(productId = null) {
    const modal = document.getElementById('productModal');
    const modalTitle = document.getElementById('modalTitle');
    const form = document.getElementById('productForm');
    
    form.reset();
    
    if (productId) {
        isEditMode = true;
        editingProductId = productId;
        modalTitle.innerHTML = '<i class="fas fa-edit"></i> Editar Producto';
        
        const product = products.find(p => p.id === productId);
        if (product) {
            document.getElementById('nombre').value = product.nombre;
            document.getElementById('talla').value = product.talla || '';
            document.getElementById('color').value = product.color || '';
            document.getElementById('precio').value = product.precio;
            document.getElementById('stock').value = product.stock || '';
            document.getElementById('proveedor').value = product.proveedor || '';
            document.getElementById('productId').value = product.id;
        }
    } else {
        isEditMode = false;
        editingProductId = null;
        modalTitle.innerHTML = '<i class="fas fa-plus-circle"></i> Nuevo Producto';
    }
    
    modal.classList.add('active');
}

// Close modal
function closeModal() {
    const modal = document.getElementById('productModal');
    modal.classList.remove('active');
    document.getElementById('productForm').reset();
    isEditMode = false;
    editingProductId = null;
}

// Save product (create or update)
async function saveProduct(event) {
    event.preventDefault();
    
    const formData = {
        nombre: document.getElementById('nombre').value,
        talla: document.getElementById('talla').value || null,
        color: document.getElementById('color').value || null,
        precio: parseFloat(document.getElementById('precio').value),
        stock: parseInt(document.getElementById('stock').value) || null,
        proveedor: document.getElementById('proveedor').value || null
    };
    
    try {
        let response;
        
        if (isEditMode) {
            // Update existing product
            response = await fetch(`${API_URL}/products/update/${editingProductId}`, {
                method: 'PUT',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify(formData)
            });
        } else {
            // Create new product
            response = await fetch(`${API_URL}/products/create`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify(formData)
            });
        }
        
        if (!response.ok) {
            throw new Error('Error al guardar el producto');
        }
        
        const savedProduct = await response.json();
        
        showToast(
            isEditMode ? 'Producto actualizado exitosamente' : 'Producto creado exitosamente',
            'success'
        );
        
        closeModal();
        loadProducts();
        
    } catch (error) {
        console.error('Error:', error);
        showToast('Error al guardar el producto', 'error');
    }
}

// Edit product
function editProduct(productId) {
    openModal(productId);
}

// Confirm delete
function confirmDelete(productId) {
    const product = products.find(p => p.id === productId);
    
    if (confirm(`¿Estás seguro de que deseas eliminar "${product.nombre}"?`)) {
        deleteProduct(productId);
    }
}

// Delete product
async function deleteProduct(productId) {
    try {
        const response = await fetch(`${API_URL}/products/delete/${productId}`, {
            method: 'DELETE'
        });
        
        if (!response.ok) {
            throw new Error('Error al eliminar el producto');
        }
        
        showToast('Producto eliminado exitosamente', 'success');
        loadProducts();
        
    } catch (error) {
        console.error('Error:', error);
        showToast('Error al eliminar el producto', 'error');
    }
}

// Show toast notification
function showToast(message, type = 'success') {
    const toast = document.getElementById('toast');
    const toastMessage = document.getElementById('toastMessage');
    const icon = toast.querySelector('i');
    
    // Remove previous classes
    toast.classList.remove('success', 'error', 'warning');
    icon.classList.remove('fa-check-circle', 'fa-exclamation-circle', 'fa-exclamation-triangle');
    
    // Add new classes based on type
    toast.classList.add(type);
    
    if (type === 'success') {
        icon.classList.add('fa-check-circle');
    } else if (type === 'error') {
        icon.classList.add('fa-exclamation-circle');
    } else if (type === 'warning') {
        icon.classList.add('fa-exclamation-triangle');
    }
    
    toastMessage.textContent = message;
    toast.classList.add('show');
    
    setTimeout(() => {
        toast.classList.remove('show');
    }, 3000);
}

// Show loading state
function showLoading() {
    document.getElementById('loadingState').style.display = 'block';
    document.getElementById('productsGrid').style.display = 'none';
    document.getElementById('emptyState').style.display = 'none';
}

// Hide loading state
function hideLoading() {
    document.getElementById('loadingState').style.display = 'none';
}

// Show empty state
function showEmptyState() {
    document.getElementById('productsGrid').style.display = 'none';
    document.getElementById('emptyState').style.display = 'block';
}

// Close modal when clicking outside
window.onclick = function(event) {
    const modal = document.getElementById('productModal');
    if (event.target === modal) {
        closeModal();
    }
}

// Keyboard shortcuts
document.addEventListener('keydown', (event) => {
    // ESC to close modal
    if (event.key === 'Escape') {
        closeModal();
    }
    
    // Ctrl/Cmd + N to open new product modal
    if ((event.ctrlKey || event.metaKey) && event.key === 'n') {
        event.preventDefault();
        openModal();
    }
});