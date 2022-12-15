function addToCart(id, name, price) {
    event.preventDefault()
    fetch('/api/add-cart', {
        method: 'post',
        body: JSON.stringify({
            'id': id,
            'name': name,
            'price': price
        }),
        headers: {
            'Content-Type': 'application/json'
        }
      }).then((res) => res.json()).then((data) => {
        console.info(data)
        let d = document.getElementsByClassName('cart-counter')
        for (let i = 0; i < d.length; i++)
            d[i].innerText = data.total_quantity
    }) // js promise
}

function updateCart(id, obj) {
   fetch('/api/update-cart', {
        method: "put",
        body: JSON.stringify({
            "id": id,
            "quantity": parseInt(obj.value)
        }),
        headers: {
            'Content-Type': 'application/json'
        }
    }).then(res => res.json()).then(data => {
        let d = document.getElementsByClassName('cart-counter')
        for (let i = 0; i < d.length; i++)
            d[i].innerText = data.total_quantity

        let d2 = document.getElementById('cart-amount')
        d2.innerText = new Intl.NumberFormat().format(data.total_amount)
    })
}

function deleteCart(id) {
//    alert(id)
    if (confirm("Bạn chắc chắn xóa không?") == true) {
        fetch('/api/delete-cart/' + id, {
            method: 'delete',
            headers: {
                'Content-Type': 'application/json'
            }
          }).then(res => res.json()).then(data => {
        let d = document.getElementsByClassName('cart-counter')
        for (let i = 0; i < d.length; i++)
            d[i].innerText = data.total_quantity

        let d2 = document.getElementById('cart-amount')
        d2.innerText = new Intl.NumberFormat().format(data.total_amount)

        let e = document.getElementById("product" + id)
        e.style.display = "none"
    }).catch(err => console.error(err))
}
}
function pay() {
    if (confirm('Bạn có chắc chắn thanh toán không?') == true) {
        fetch('/api/pay', {
            method: 'post'
        }).then(res => res.json()).then(data => {
            if (data.code === 200)
                location.reload()
        })
    }
}
function pay1() {
    if (confirm('Bạn có chắc chắn thanh toán online không?') == true) {
        fetch('/api/pay1', {
            method: 'post'
        }).then(res => res.json()).then(data => {
            if (data.code === 200)
                redirect('{{url_for("get_info"}}')
        })
    }
}

function addComment(productId) {
    let content = document.getElementById('commentId')
    if (content !== null) {
        fetch('/api/comments', {
            method: 'post',
            body: JSON.stringify({
                'product_id': productId,
                'content': content.value
            }),
            headers: {
                'Content-Type': 'application/json'
            }
        }).then(res => res.json()).then(data =>{
            if (data.status == 201) {
                let c = data.comment

                let area = document.getElementById('commentArea')

                area.innerHTML = `
                     <div class="row comment">
                         <div class="col-md-1 col-xs-4">
                            <img src="${c.user.avatar}"
                            class=" img-fluid rounded-circle" alt="demo" />
                        </div>
                        <div class="col-md-11 col-xs-8">
                            <p>${c.content}</p>
                            <p><em>${moment(c.created_date).locale('vi').fromNow()}</em></p>
                        </div>
                    </div>
                `+area.innerHTML
            } else if (data.status == 404)
                alert(data.err_msg)
        })
    }
}