// get all the buttons with a class of update-cart
let updateCartBtns = document.getElementsByClassName('update-cart')

//adds an event listener to all the updateCartBtns
for(let i = 0; i < updateCartBtns.length; i++){

    updateCartBtns[i].addEventListener('click', function(){
        productId = this.dataset.product_id
        action = this.dataset.action

        if(user == 'AnonymousUser'){
            addCookieItem(productId, action)
        }else{
            updateUserCart(productId, action)
        }

    })

}

function addCookieItem(productId, action){
    console.log('Guest user..')
    if(action == 'add'){
        if(cart[productId] == undefined){
            cart[productId] = {'quantity':1}
        }else{
            cart[productId]['quantity'] += 1
        }
    }

    if(action == 'remove'){

        cart[productId]['quantity'] -= 1
        if(cart[productId]['quantity'] <= 0){
            console.log('remove product')
            delete cart[productId]
        }
    }
    console.log('Cart', cart)
    document.cookie = 'cart=' + JSON.stringify(cart) + ";domain=;path=/"
    location.reload()

}

function updateUserCart(productId, action){
    url = '/update-cart/'

    fetch(url, {
        'method': 'POST',
        'headers':{
            'Content-Type':'application/json',
            'X-CSRFToken': csrftoken,
        },
        body: JSON.stringify({'productId' : productId,'action' : action})
     })
     .then((response)=>{
       return response.json()
     })

     .then((data)=>{
        location.reload()
     })

}

