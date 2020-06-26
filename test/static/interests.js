$(document).ready(function () {

  post_stocks();

});

function post_stocks() {

    console.log('hi')
        $.ajax({
        type: "GET",
        url: "/stock",
        data: {},
        success: function (response) {
          alert('통신 성공');
        }
    })
}

// $.ajax({
//   type: "POST",
//   url: "/article",
//   data: { url_give: 'https://kr.investing.com/news/most-popular-news' },
//   success: function (response) {
//       if (response['result'] == 'success') {

//           // 2. 성공했을 때 리뷰를 올바르게 화면에 나타내기
//       } else {
//           alert('리뷰를 받아오지 못했습니다');
//       }
//   }
// });

function make_card(name, symbol, exchange, price) {

  $('#stock_row').empty();

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
            <button type="button" class="btn btn-sm btn-outline-secondary">View</button>
            <button type="button" class="btn btn-sm btn-outline-secondary">Edit</button>
          </div>
          <small class="text-muted">9 mins</small>
        </div>
      </div>
    </div>
  </div>`;

  $('#stock_row').append(temp.html);

}
