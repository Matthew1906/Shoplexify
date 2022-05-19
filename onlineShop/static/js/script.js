function addedToCart(){
    alert("Product has been added to cart!");
    document.getElementById('cart_form').submit();
}

function redirectPayment(result){
    let f = document.createElement('form');
    f.action = 'https://matthew1906-shoplexify.herokuapp.com/payment/notifications';
    f.method = 'POST';
    let order_id = document.createElement('input');
    order_id.type = 'hidden';
    order_id.name = 'order_id';
    order_id.value = result.order_id;
    let payment_type = document.createElement('input');
    payment_type.type = 'hidden';
    payment_type.name = 'payment_type';
    payment_type.value = result.payment_type;
    f.appendChild(order_id);
    f.appendChild(payment_type)
    document.body.appendChild(f)
    f.submit()
}