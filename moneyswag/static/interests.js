$(document).ready(function () {
  $('#stock_row').html('');
  post_stocks();
});

function post_stocks() {

  $.ajax({
    type: "GET",
    url: "/stock",
    data: {},
    success: function (response) {
      if (response['result'] == 'success') {

        let stocks = response['stocks'];

        stocks.forEach(curr => make_card(curr['companyName'], curr['symbol'], curr['primaryExchange'], curr['close'], curr['_id']));
      }
    }
  });
}

function make_card(name, symbol, exchange, price, id) {

  let temp_html = `<div class="col-md-4">
    <div class="card mb-4 shadow-sm">
      <svg class="bd-placeholder-img card-img-top" width="100%" height="225" xmlns="http://www.w3.org/2000/svg"
        preserveAspectRatio="xMidYMid slice" focusable="false" role="img" aria-label="Placeholder: Thumbnail">
        <title>Placeholder</title>
        <rect width="100%" height="100%" fill="#55595c" /><text x="50%" y="50%" fill="#eceeef"
          dy=".3em">Thumbnail</text>
      </svg>
      <div class="card-body">
        <h3>${name}</h3>
        <h4>${symbol}</h4>
        <h5>${price}</h5>
        <p class="card-text">${exchange}</p>
        <div class="d-flex justify-content-between align-items-center">
          <div class="btn-group">
            <form action = "/dashboard" method = "POST">
              <input type = "hidden" name = "symbol" value = "${symbol}">
              <p><input class = "size" type = "submit" value = "보기" /></p>
            </form>
            <button id = "${id}" onClick = "delete_stock(this.id)" type="button" class="btn btn-sm btn-outline-secondary size">삭제</button>
            </div>
          <small class="text-muted">9 mins</small>
        </div>
      </div>
    </div>
  </div>`;

  $('#stock_row').append(temp_html);

}

//<button type="submit" href="#" onClick="location.href='dashboard.html'" class="btn btn-sm btn-outline-secondary">보기</button>

function delete_stock(id) {

  $.ajax({
    type: "DELETE",
    url: "/stock",
    data: { id_give: id },
    success: function (response) {
      if (response['result'] == 'success') {
        alert('삭제 완료');
        window.location.reload();
      } else {
        alert('서버 오류');
      }
    }
  })
}

function show_dashboard() {
 
  $.ajax({
    type: "POST",
    url: "/dashboard",
    data: { },
    success: function (response) {
      if (response['result'] == 'success') {
        
      } else {
        alert('서버 오류');
      }
    }
  })
}

