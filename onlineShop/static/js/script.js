function notRegistered(){
    alert("You need to register an account to checkout!")
}

function addedToCart(){
    alert("Product has been added to cart!");
    document.getElementById('cart_form').submit();
}