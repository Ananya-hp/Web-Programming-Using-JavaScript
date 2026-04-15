let cart = JSON.parse(localStorage.getItem("cart")) || [];

function addToCart(name, price) {
    let item = cart.find(p => p.name === name);

    if (item) {
        item.qty++;
    } else {
        cart.push({ name, price, qty: 1 });
    }

    saveCart();
    displayCart();
}

function displayCart() {
    let cartDiv = document.getElementById("cart-items");
    cartDiv.innerHTML = "";
    let total = 0;

    cart.forEach((item, index) => {
        let div = document.createElement("div");
        div.className = "cart-item";

        let itemTotal = item.price * item.qty;
        total += itemTotal;

        div.innerHTML = `
            ${item.name} - ₹${item.price} x ${item.qty} = ₹${itemTotal}
            <br>
            <button onclick="changeQty(${index},1)">+</button>
            <button onclick="changeQty(${index},-1)">-</button>
            <button onclick="removeItem(${index})">Remove</button>
        `;

        cartDiv.appendChild(div);
    });

    document.getElementById("total").innerText = total;
}

function changeQty(index, change) {
    cart[index].qty += change;

    if (cart[index].qty <= 0) {
        cart.splice(index, 1);
    }

    saveCart();
    displayCart();
}

function removeItem(index) {
    cart.splice(index, 1);
    saveCart();
    displayCart();
}

function saveCart() {
    localStorage.setItem("cart", JSON.stringify(cart));
}

function checkout() {
    let name = document.getElementById("name").value;

    if (cart.length === 0) {
        alert("Cart is empty!");
        return;
    }

    document.getElementById("message").innerText =
        "Thank you " + name + "! Your order has been placed.";

    cart = [];
    saveCart();
    displayCart();
}

// Load cart on refresh
displayCart();