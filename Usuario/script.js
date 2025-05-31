// Datos de productos simulados
// const products = [
//     {
//         id: 1,
//         name: "iPhone 15 Pro",
//         description: "El último iPhone con chip A17 Pro y cámara de 48MP",
//         price: 1199.99,
//         category: "smartphones",
//         image: "https://assets.swappie.com/cdn-cgi/image/width=600,height=600,fit=contain,format=auto/swappie-iphone-15-pro-black-titanium-back.png?v=9f7ae122",
//         featured: true
//     },
//     {
//         id: 2,
//         name: "MacBook Air M2",
//         description: "Laptop ultradelgada con chip M2 y pantalla Retina",
//         price: 1299.99,
//         category: "laptops",
//         image: "/placeholder.svg?height=200&width=200",
//         featured: true
//     },
//     {
//         id: 3,
//         name: "iPad Pro 12.9",
//         description: "Tablet profesional con chip M2 y pantalla Liquid Retina",
//         price: 1099.99,
//         category: "tablets",
//         image: "/placeholder.svg?height=200&width=200",
//         featured: true
//     },
//     {
//         id: 4,
//         name: "AirPods Pro",
//         description: "Auriculares inalámbricos con cancelación de ruido",
//         price: 249.99,
//         category: "accesorios",
//         image: "/placeholder.svg?height=200&width=200",
//         featured: false
//     },
//     {
//         id: 5,
//         name: "Samsung Galaxy S24",
//         description: "Smartphone Android con cámara de 200MP",
//         price: 999.99,
//         category: "smartphones",
//         image: "/placeholder.svg?height=200&width=200",
//         featured: false
//     },
//     {
//         id: 6,
//         name: "Dell XPS 13",
//         description: "Laptop ultrabook con procesador Intel Core i7",
//         price: 1199.99,
//         category: "laptops",
//         image: "/placeholder.svg?height=200&width=200",
//         featured: false
//     },
//     {
//         id: 7,
//         name: "Samsung Galaxy Tab S9",
//         description: "Tablet Android con S Pen incluido",
//         price: 799.99,
//         category: "tablets",
//         image: "/placeholder.svg?height=200&width=200",
//         featured: false
//     },
//     {
//         id: 8,
//         name: "Magic Mouse",
//         description: "Mouse inalámbrico con superficie Multi-Touch",
//         price: 79.99,
//         category: "accesorios",
//         image: "/placeholder.svg?height=200&width=200",
//         featured: false
//     }
// ];

const server = 'http://sine.djpyru.es:9876';

// Estado de la aplicación
let products = [];
let currentUser = null;
let cart = [];
let orders = [];
let currentSection = 'home';

// Inicialización
document.addEventListener('DOMContentLoaded', async function () {
    await loadUserData();
    await loadProductsData();
    await loadCartData();
    await loadOrdersData();

    updateUI();
    renderProducts();
    renderFeaturedProducts();
    setupEventListeners();
});
;

// Event Listeners
function setupEventListeners() {
    // Login form
    document.getElementById('login-form').addEventListener('submit', handleLogin);
    
    // Register form
    document.getElementById('register-form').addEventListener('submit', handleRegister);
    
    // Profile form
    document.getElementById('profile-form').addEventListener('submit', handleProfileUpdate);
    
    // Checkout form
    document.getElementById('checkout-form').addEventListener('submit', handleCheckout);
}

// Autenticación
async function handleLogin(e) {
    e.preventDefault();
    const email = document.getElementById('login-email').value;
    const password = document.getElementById('login-password').value;

    let url = `${server}/login/usuario?email=${email}&contrasena=${password}`;
    try{
        console.log("Ejecutando solicitud de login a:", url);
        const response = await fetch(url, {method: "GET"})
        const data = await response.json();
        console.log(data);
        if (data.success === false) {
            showNotification(data.error, 'error');
            return;
        }
        currentUser = data.data;
        console.log(currentUser);
        localStorage.setItem('currentUser', JSON.stringify(data.data));
        closeModal('login-modal');
        updateUI();
        showNotification('¡Bienvenido de vuelta!', 'success');
    }catch(e){
        console.error('Error al realizar la solicitud de login:', e);
        showNotification('Error al iniciar sesión. Inténtalo más tarde.', 'error');
        return;
    }
}

async function handleRegister(e) {
    e.preventDefault();
    const nombre = document.getElementById('register-name').value;
    const apellidos = document.getElementById('register-surname').value;
    const direccion = document.getElementById('register-address').value;
    const email = document.getElementById('register-email').value;
    const telefono = document.getElementById('register-phone').value;
    const password = document.getElementById('register-password').value;
    const confirmPassword = document.getElementById('register-confirm').value;

    const newUser = {
        email_usuario: email,
        nombre_usuario: nombre,
        apellidos: apellidos,
        direccion: direccion,
        telefono: telefono || '',
        contrasena: password
    }
    
    if (password !== confirmPassword) {
        showNotification('Las contraseñas no coinciden', 'error');
        return;
    }

    let url = server + '/add/usuario?email=' + email + '&nombre=' + nombre + '&apellidos=' + apellidos + '&direccion=' + direccion + '&contrasena=' + password;
    if (telefono) {
        url += '&telefono=' + telefono;
    }

    try{
        const response = await fetch(url, {method: "GET"});
        const data = await response.json();
        console.log(response);
        console.log(data);
        if (data.success === false) {
            showNotification(data.error, 'error');
            return;
        }
        currentUser = newUser;
        localStorage.setItem('currentUser', JSON.stringify(newUser));

        closeModal('register-modal');
        updateUI();
        showNotification('¡Cuenta creada exitosamente!', 'success');

    }catch (error) {
        console.log(error);
    }
}

function logout() {
    currentUser = null;
    localStorage.removeItem('currentUser');
    updateUI();
    showSection('home');
    showNotification('Sesión cerrada', 'info');
}

// Gestión de perfil
async function handleProfileUpdate(e) {
    e.preventDefault();
    
    if (!currentUser) return;
    
    const updatedUser = {
        ...currentUser,
        email_usuario: document.getElementById('profile-email').value,
        nombre_usuario: document.getElementById('profile-name').value,
        apellidos: document.getElementById('profile-surname').value,
        telefono: document.getElementById('profile-phone').value,
        direccion: document.getElementById('profile-address').value,
        contrasena: document.getElementById('profile-password').value
    };

    let url = `${server}/edit/usuario?email=${updatedUser.email_usuario}&nombre=${updatedUser.nombre_usuario}&apellidos=${updatedUser.apellidos}&direccion=${updatedUser.direccion}`;

    if (updatedUser.telefono) {
        url += `&telefono=${updatedUser.telefono}`;
    }
    if (updatedUser.contrasena) {
        url += `&contrasena=${updatedUser.contrasena}`;
    }

    console.log(url);

    fetch(url, { method: "GET" })
        .then(response => {
            if (!response.ok) throw new Error("Error en la respuesta del servidor");
            return response.json();
        })
        .then(data => {
            console.log("Usuario editado:", data);

        })
        .catch(error => console.error("Error al editar el usuario:", error));

    currentUser = updatedUser;
    localStorage.setItem('currentUser', JSON.stringify(updatedUser));
    updateUI();
    showNotification('Perfil actualizado exitosamente', 'success');
}

// Gestión de productos
function renderProducts() {
    const grid = document.getElementById('products-grid');
    grid.innerHTML = products.map(product => createProductCard(product)).join('');
}

function renderFeaturedProducts() {
    const grid = document.getElementById('featured-products-grid');
    const featuredProducts = products.slice(0, 3); //toDo: Cambiar a productos destacados reales
    grid.innerHTML = featuredProducts.map(product => createProductCard(product)).join('');
}

function createProductCard(product) {
    if (product.stock === 0){
        return `
            <div class="product-card out-of-stock" onclick="showProductDetail(${product.id_modelo})">
                <img src="${product.url_imagen}" alt="${product.nombre_modelo}" class="product-image">
                <div class="product-info">
                    <h3 class="product-title">${product.nombre_modelo}</h3>
                    <p class="product-description">${product.descripcion}</p>
                    <div class="product-price">${product.precio.toFixed(2)}€</div>
                    <div class="product-actions">
                        <button disabled class="btn btn-secondary">
                            <i class="fas fa-ban"></i> Agotado
                        </button>
                    </div>
                </div>
            </div>
        `;
    }
    return `
        <div class="product-card" onclick="showProductDetail(${product.id_modelo})">
            <img src="${product.url_imagen}" alt="${product.nombre_modelo}" class="product-image">
            <div class="product-info">
                <h3 class="product-title">${product.nombre_modelo}</h3>
                <p class="product-description">${product.descripcion}</p>
                <div class="product-price">${product.precio.toFixed(2)}€</div>
                <div class="product-actions">
                    <button onclick="event.stopPropagation(); addToCart(${product.id_modelo})" class="btn btn-primary">
                        <i class="fas fa-cart-plus"></i> Agregar
                    </button>
                </div>
            </div>
        </div>
    `;
}

function filterProducts() {
    const category = document.getElementById('category-filter').value;
    const search = document.getElementById('search-input').value.toLowerCase();
    
    let filteredProducts = products;
    
    if (category) {
        filteredProducts = filteredProducts.filter(p => p.categoria === category);
    }
    
    if (search) {
        filteredProducts = filteredProducts.filter(p => 
            p.nombre_modelo.toLowerCase().includes(search) ||
            p.descripcion.toLowerCase().includes(search)
        );
    }
    
    const grid = document.getElementById('products-grid');
    grid.innerHTML = filteredProducts.map(product => createProductCard(product)).join('');
}

// Gestión del carrito
function addToCart(productId) {
    if (!currentUser) {
        showLogin();
        showNotification('Debes iniciar sesión para agregar productos al carrito', 'info');
        return;
    }

    const product = products.find(p => Number(p.id_modelo) === Number(productId));
    if (!product) {
        console.error("Producto no encontrado:", productId);
        return;
    }

    const existingItem = cart.find(item => Number(item.id_modelo) === Number(productId));

    if (existingItem) {
        if (existingItem.quantity >= product.stock) {
            showNotification(`No hay más stock disponible para ${product.nombre_modelo}`, 'warning');
            return;
        }
        existingItem.quantity += 1;
    } else {
        if (product.stock < 1) {
            showNotification(`Producto sin stock: ${product.nombre_modelo}`, 'warning');
            return;
        }
        cart.push({
            ...product,
            quantity: 1
        });
    }

    saveCartData();
    updateCartUI();
    showNotification(`${product.nombre_modelo} agregado al carrito`, 'success');
}

function removeFromCart(productId) {
    cart = cart.filter(item => Number(item.id_modelo) !== Number(productId));
    saveCartData();
    updateCartUI();
    renderCart();
}

function updateQuantity(productId, change) {
    const item = cart.find(item => Number(item.id_modelo) === Number(productId));
    const product = products.find(p => Number(p.id_modelo) === Number(productId));

    if (item && product) {
        if (change > 0 && item.quantity >= product.stock) {
            showNotification(`No puedes agregar más. Stock máximo alcanzado para ${product.nombre_modelo}`, 'warning');
            return;
        }

        item.quantity += change;

        if (item.quantity <= 0) {
            removeFromCart(productId);
        } else {
            saveCartData();
            updateCartUI();
            renderCart();
        }
    }
}

function clearCart() {
    cart = [];
    saveCartData();
    updateCartUI();
    renderCart();
    showNotification('Carrito vaciado', 'info');
}

function renderCart() {
    const cartItems = document.getElementById('cart-items');
    const cartTotal = document.getElementById('cart-total');

    if (cart.length === 0) {
        cartItems.innerHTML = `
            <div class="empty-state">
                <i class="fas fa-shopping-cart"></i>
                <h3>Tu carrito está vacío</h3>
                <p>Agrega algunos productos para comenzar</p>
                <button onclick="showSection('products')" class="btn btn-primary">
                    Ver Productos
                </button>
            </div>
        `;
        cartTotal.innerHTML = '';
        return;
    }

    cartItems.innerHTML = cart.map(item => `
        <div class="cart-item">
            <img src="${item.url_imagen}" alt="${item.nombre_modelo}" class="cart-item-image">
            <div class="cart-item-info">
                <h4 class="cart-item-title">${item.nombre_modelo}</h4>
                <p class="cart-item-price">${item.precio.toFixed(2)} €</p>
            </div>
            <div class="cart-item-controls">
                <div class="quantity-controls">
                    <button class="quantity-btn" onclick="updateQuantity(${item.id_modelo}, -1)">-</button>
                    <span>${item.quantity}</span>
                    <button class="quantity-btn" onclick="updateQuantity(${item.id_modelo}, 1)">+</button>
                </div>
                <button onclick="removeFromCart(${item.id_modelo})" class="btn btn-outline">
                    <i class="fas fa-trash"></i>
                </button>
            </div>
        </div>
    `).join('');

    const total = cart.reduce((sum, item) => sum + (item.precio * item.quantity), 0);
    cartTotal.innerHTML = `
        <h3>Total: ${total.toFixed(2)} €</h3>
    `;
}


// Checkout
function setDefaultShippingAddress(address) {
    const input = document.getElementById('shipping-address');
    input.value = address; // valor por defecto
}

function showCheckout() {
    if (!currentUser) {
        showLogin();
        return;
    }
    
    if (cart.length === 0) {
        showNotification('Tu carrito está vacío', 'error');
        return;
    }
    setDefaultShippingAddress(currentUser.direccion)
    showSection('checkout');
    renderCheckoutSummary();
}

function renderCheckoutSummary() {
    const checkoutItems = document.getElementById('checkout-items');
    const checkoutTotal = document.getElementById('checkout-total');
    
    checkoutItems.innerHTML = cart.map(item => `
        <div class="order-item">
            <span>${item.nombre_modelo} x ${item.quantity}</span>
            <span>${(item.precio * item.quantity).toFixed(2)}€</span>
        </div>
    `).join('');
    
    const total = cart.reduce((sum, item) => sum + (item.precio * item.quantity), 0);
    checkoutTotal.innerHTML = `
        <div class="order-total">Total: ${total.toFixed(2)}€</div>
    `;
}

async function handleCheckout(e) {
    e.preventDefault();

    const orderNumber = 'ORD-' + Date.now() + Math.floor(Math.random() * 1000);
    console.log(currentUser);
    const order = {
        id: orderNumber,
        userId: currentUser.email_usuario,
        items: [...cart],
        date: new Date().toISOString(),
        address: document.getElementById('shipping-address').value,
        message: document.getElementById('shipping-message').value,
        paymentMethod: document.getElementById('payment-method').value
    };

    correcto = await realizarPedido(order);
    console.log(correcto);
    // Limpiar carrito
    cart = [];
    saveCartData();
    updateCartUI();
    if (correcto) {
        // Mostrar confirmación
        document.getElementById('order-number').textContent = orderNumber;
        showModal('success-modal');

        showNotification('¡Pedido realizado exitosamente!', 'success');
    }else{
        showSection('home');
    }
}

async function realizarPedido(order) {

    let url = server + '/add/pedido?id_pedido=' + order.id + '&email_usuario=' + order.userId + '&direccion=' + order.address + '&fecha_pedido=' + order.date +'&mensaje=' + order.message;
    console.log(url);
    try{
        const response = await fetch(url, {method: "GET"});
        const data = await response.json();
        console.log(response);
        console.log(data);
        if (data.success === false) {
            showNotification(data.error, 'error');
            return false;
        }

        // Agregar los items del pedido

        for(let item of order.items) {
            for (let i = 0; i < item.quantity; i++) {
                let itemUrl = server + '/add/item?id_pedido=' + order.id + '&id_modelo=' + item.id_modelo;
                const itemResponse = await fetch(itemUrl, {method: "GET"});
                const itemData = await itemResponse.json();
                console.log("Item: ", itemData);
                if (itemData.success === false) {
                    showNotification("No hay stock suficiente de todos los productos", 'error');
                    //toDo // Si falla al agregar un item, debemos revertir los items que ya se han agregado
                    let url = server + '/remove/pedido?id_pedido=' + order.id;
                    const removeResponse = await fetch(url, {method: "GET"});
                    const removeData = await removeResponse.json();
                    console.log(removeData);
                    return false;
                }
            }
        }

        let updateUrl = server + '/edit/pedido?estado_pedido=p&id_pedido=' + order.id;
        const updateResponse = await fetch(updateUrl, {method: "GET"});
        const updateData = await updateResponse.json();
        console.log("Pedido actualizado:", updateData);
        return true;

    }catch (error) {
        console.log(error);
    }
}

// Gestión de pedidos
async function renderOrders() {
    const ordersList = document.getElementById('orders-list');
    const userOrders = await obtenerPedidosUsuario();

    if (!userOrders || userOrders.length === 0) {
        ordersList.innerHTML = `
            <div class="empty-state">
                <i class="fas fa-receipt"></i>
                <h3>No tienes pedidos aún</h3>
                <p>Realiza tu primera compra para ver tus pedidos aquí</p>
                <button onclick="showSection('products')" class="btn btn-primary">
                    Ver Productos
                </button>
            </div>
        `;
        return;
    }

    ordersList.innerHTML = userOrders.map(order => {
        const entregaHTML = (order.status.toLowerCase() === "terminado" && order.deliveryDate)
            ? `<div class="order-delivery-date">Entregado el ${new Date(order.deliveryDate).toLocaleDateString()}</div>`
            : "";

        return `
            <div class="order-card">
                <div class="order-header">
                    <div>
                        <div class="order-number">Pedido ${order.id}</div>
                        <div class="order-date">${new Date(order.date).toLocaleDateString()}</div>
                    </div>
                    <div>
                        <div class="order-status">${order.status}</div>
                        ${entregaHTML}
                    </div>
                </div>
                <div class="order-items">
                    ${order.items.map(item => `
                        <div class="order-item">
                            <span>${item.name} x ${item.quantity}</span>
                            <span>${(item.price * item.quantity).toFixed(2)}€</span>
                        </div>
                    `).join('')}
                </div>
                <div class="order-total">Total: ${order.total.toFixed(2)}€</div>
            </div>
        `;
    }).join('');
}

async function obtenerPedidosUsuario() {
    if (!currentUser) return [];
    const url = `${server}/find/pedido?email_usuario=${currentUser.email_usuario}`;
    console.log(url);
    let orders = [];
    try {
        const response = await fetch(url, { method: "GET" });

        if (!response.ok) {
            throw new Error("Error en la respuesta del servidor");
        }
        const data = await response.json();
        if (data.success === false) {
            showNotification(data.error || 'No se encontraron pedidos', 'error');
            return [];
        }
        let pedidos = data.data;
        console.log("Pedidos obtenidos:", pedidos);

        for(let pedido of pedidos) {
            let order = {
                id: pedido.id_pedido,
                userID: pedido.email_usuario,
                date: pedido.fecha,
                address: pedido.direccion,
                message: pedido.message,
                status: pedido.estado_pedido,
                total: 0,
                deliveryDate: pedido.fecha_entrega
            };
            // Obtener los items del pedido
            const itemsUrl = `${server}/get/productos_por_pedido?id_pedido=${pedido.id_pedido}`;
            const itemsResponse = await fetch(itemsUrl, { method: "GET" });
            const itemsData = await itemsResponse.json();
            console.log("Productos del pedido: ", pedido.id_pedido , " = ", itemsData);
            if (itemsData.success === false) {
                showNotification(itemsData.error || 'Error al obtener los items del pedido', 'error');
                continue;
            }
            if (itemsData.data) {
                order.items = itemsData.data.map(item => ({
                    id_modelo: item.id_modelo,
                    name: item.nombre_modelo,
                    quantity: item.cantidad,
                    price: item.precio
                }));
                // Calcular el total del pedido
                order.total = order.items.reduce((sum, item) => sum + (item.price * item.quantity), 0);
            }else{
                order.items = [];
            }
            orders.push(order);

        }

        if (data.success === false) {
            showNotification(data.error || 'Pedido no encontrado', 'error');
            return null;
        }

        return orders;
    } catch (error) {
        console.error("Error al buscar el pedido:", error);
        showNotification("No se pudo recuperar el pedido. Inténtalo de nuevo más tarde.", 'error');
        return null;
    }

}

// Navegación
function showSection(sectionName) {
    // Ocultar todas las secciones
    document.querySelectorAll('.section').forEach(section => {
        section.classList.remove('active');
    });
    
    // Mostrar la sección seleccionada
    document.getElementById(sectionName).classList.add('active');
    
    // Actualizar navegación
    document.querySelectorAll('.nav-link').forEach(link => {
        link.classList.remove('active');
    });
    
    // Renderizar contenido específico
    switch(sectionName) {
        case 'cart':
            renderCart();
            break;
        case 'profile':
            if (!currentUser) {
                showLogin();
                return;
            }
            loadProfileData();
            break;
        case 'orders':
            if (!currentUser) {
                showLogin();
                return;
            }
            renderOrders();
            break;
    }
    
    currentSection = sectionName;
}

function showCart() {
    showSection('cart');
}

// Modales
function showModal(modalId) {
    document.getElementById(modalId).style.display = 'block';
}

function closeModal(modalId) {
    document.getElementById(modalId).style.display = 'none';
}

function showLogin() {
    showModal('login-modal');
}

function showRegister() {
    showModal('register-modal');
}

// Cerrar modales al hacer clic fuera
window.onclick = function(event) {
    if (event.target.classList.contains('modal')) {
        event.target.style.display = 'none';
    }
}

// Actualización de UI
function updateUI() {
    const loggedOut = document.getElementById('user-logged-out');
    const loggedIn = document.getElementById('user-logged-in');
    const userName = document.getElementById('user-name');
    
    if (currentUser) {
        loggedOut.style.display = 'none';
        loggedIn.style.display = 'flex';
        userName.textContent = currentUser.nombre_usuario;
    } else {
        loggedOut.style.display = 'flex';
        loggedIn.style.display = 'none';
    }
    
    updateCartUI();
}

function updateCartUI() {
    const cartCount = document.getElementById('cart-count');
    const totalItems = cart.reduce((sum, item) => sum + item.quantity, 0);
    cartCount.textContent = totalItems;
}

function loadProfileData() {
    if (!currentUser) return;

    document.getElementById('profile-email').value = currentUser.email_usuario || '';
    document.getElementById('profile-name').value = currentUser.nombre_usuario || '';
    document.getElementById('profile-surname').value = currentUser.apellidos || '';
    document.getElementById('profile-phone').value = currentUser.telefono || '';
    document.getElementById('profile-address').value = currentUser.direccion || '';
}

// Persistencia de datos
function loadUserData() {
    const savedUser = localStorage.getItem('currentUser');
    if (savedUser) {
        currentUser = JSON.parse(savedUser);
    }
}
async function loadProductsData() {
    try {
        let url = server + '/modelos';
        console.log(url);

        const response = await fetch(url, { method: "GET" });
        if (!response.ok) throw new Error("Error en la respuesta del servidor");

        const data = await response.json();
        console.log("Productos cargados:", data);

        products = data.data;
        renderProducts();
        renderFeaturedProducts();
    } catch (error) {
        console.error("Error al cargar los productos:", error);
    }
}

function loadCartData() {
    const savedCart = localStorage.getItem('cart');
    if (savedCart) {
        cart = JSON.parse(savedCart);
    }
}

function saveCartData() {
    localStorage.setItem('cart', JSON.stringify(cart));
}

function loadOrdersData() {
    const savedOrders = localStorage.getItem('orders');
    if (savedOrders) {
        orders = JSON.parse(savedOrders);
    }
}

function saveOrdersData() {
    localStorage.setItem('orders', JSON.stringify(orders));
}

// Notificaciones
function showNotification(message, type = 'info') {
    // Crear elemento de notificación
    const notification = document.createElement('div');
    notification.className = `notification notification-${type}`;
    notification.innerHTML = `
        <i class="fas fa-${getNotificationIcon(type)}"></i>
        <span>${message}</span>
    `;
    
    // Estilos para la notificación
    notification.style.cssText = `
        position: fixed;
        top: 100px;
        right: 20px;
        background: ${getNotificationColor(type)};
        color: white;
        padding: 1rem 1.5rem;
        border-radius: 8px;
        box-shadow: 0 4px 12px rgba(0,0,0,0.2);
        z-index: 3000;
        display: flex;
        align-items: center;
        gap: 0.5rem;
        font-weight: 500;
        transform: translateX(100%);
        transition: transform 0.3s ease;
    `;
    
    document.body.appendChild(notification);
    
    // Animar entrada
    setTimeout(() => {
        notification.style.transform = 'translateX(0)';
    }, 100);
    
    // Remover después de 3 segundos
    setTimeout(() => {
        notification.style.transform = 'translateX(100%)';
        setTimeout(() => {
            document.body.removeChild(notification);
        }, 300);
    }, 3000);
}

function getNotificationIcon(type) {
    switch(type) {
        case 'success': return 'check-circle';
        case 'error': return 'exclamation-circle';
        case 'warning': return 'exclamation-triangle';
        default: return 'info-circle';
    }
}

function getNotificationColor(type) {
    switch(type) {
        case 'success': return '#28a745';
        case 'error': return '#dc3545';
        case 'warning': return '#ffc107';
        default: return '#007bff';
    }
}


//Product Detail Functions
let currentDetailProduct = null;
let detailQuantity = 1;

function showProductDetail(productId) {
    const product = products.find(p => Number(p.id_modelo) === Number(productId));
    if (!product) {
        console.error("Producto no encontrado:", productId);
        return;
    }

    currentDetailProduct = product;
    detailQuantity = 1;

    // Update product detail information
    document.getElementById('detail-product-name').textContent = product.nombre_modelo;
    document.getElementById('detail-product-price').textContent = `${product.precio.toFixed(2)}€`;
    document.getElementById('detail-product-description').textContent = product.descripcion;
    document.getElementById('detail-product-category').textContent = product.categoria;
    document.getElementById('detail-quantity').textContent = detailQuantity;

    // Update stock information
    const stockElement = document.getElementById('detail-product-stock');
    if (product.stock > 0) {
        document.getElementById('stock-check').innerHTML = `<i class="fas fa-check-circle"></i>`;
        if (product.stock < 5) {
            stockElement.innerHTML = `En stock (${product.stock} disponibles)`;
        }else{
            stockElement.innerHTML = `En stock`;
        }
        stockElement.className = 'product-stock';
        document.getElementById('detail-add-to-cart').disabled = false;
    } else {
        stockElement.innerHTML = 'Sin stock';
        stockElement.className = 'product-stock out-of-stock';
        const btn = document.getElementById('detail-add-to-cart');
        btn.disabled = true;
        btn.style.backgroundColor = 'gray';
        btn.style.borderColor = 'gray';
        btn.style.cursor = 'not-allowed';
    }
    const imageUrls = [product.url_imagen, product.imagen2, product.imagen3].filter(Boolean); // Filtra valores nulos o vacíos
    //toDo: Areglar imagenes de producto
    // Update images (using the same image for all three thumbnails as placeholder)
    const mainImage = document.getElementById('main-product-image');
    const thumbnails = document.querySelectorAll('.thumbnail');

    mainImage.src = product.url_imagen;
    mainImage.alt = product.nombre_modelo;

    thumbnails.forEach((thumbnail, index) => {
        if (imageUrls[index]) {
            thumbnail.src = imageUrls[index];
            thumbnail.alt = `${product.nombre_modelo} - Vista ${index + 1}`;
            thumbnail.style.display = ''; // Asegúrate de mostrarla
        } else {
            thumbnail.style.display = 'none'; // Oculta las miniaturas que no se usan
        }
        if (index === 0) {
            thumbnail.classList.add('active');
        } else {
            thumbnail.classList.remove('active');
        }
    });

    showSection('product-detail');
}

function changeMainImage(thumbnail) {
    // Remove active class from all thumbnails
    document.querySelectorAll('.thumbnail').forEach(thumb => {
        thumb.classList.remove('active');
    });

    // Add active class to clicked thumbnail
    thumbnail.classList.add('active');

    // Update main image
    const mainImage = document.getElementById('main-product-image');
    mainImage.src = thumbnail.src;
    mainImage.alt = thumbnail.alt;
}

function updateDetailQuantity(change) {
    if (!currentDetailProduct) return;

    const newQuantity = detailQuantity + change;

    if (newQuantity < 1) {
        detailQuantity = 1;
    } else if (newQuantity > currentDetailProduct.stock) {
        showNotification(`Solo hay ${currentDetailProduct.stock} unidades disponibles`, 'warning');
        detailQuantity = currentDetailProduct.stock;
    } else {
        detailQuantity = newQuantity;
    }

    document.getElementById('detail-quantity').textContent = detailQuantity;
}

function addToCartFromDetail() {
    if (!currentDetailProduct) return;

    if (!currentUser) {
        showLogin();
        showNotification('Debes iniciar sesión para agregar productos al carrito', 'info');
        return;
    }

    const existingItem = cart.find(item => Number(item.id_modelo) === Number(currentDetailProduct.id_modelo));
    const totalQuantityInCart = existingItem ? existingItem.quantity : 0;
    const availableStock = currentDetailProduct.stock - totalQuantityInCart;

    if (detailQuantity > availableStock) {
        showNotification(`Solo puedes agregar ${availableStock} unidades más al carrito`, 'warning');
        return;
    }

    if (existingItem) {
        existingItem.quantity += detailQuantity;
    } else {
        cart.push({
            ...currentDetailProduct,
            quantity: detailQuantity
        });
    }

    saveCartData();
    updateCartUI();
    showNotification(`${detailQuantity} x ${currentDetailProduct.nombre_modelo} agregado al carrito`, 'success');

    // Reset quantity to 1
    detailQuantity = 1;
    document.getElementById('detail-quantity').textContent = detailQuantity;
}