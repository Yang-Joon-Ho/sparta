/* globals Chart:false, feather:false */

$(document).ready(function () {
  //$('#stock_row').html('');
  $('#table_price').html('');
  let symbol = $('#stock_symbol').text();

  stock_price(symbol);
  current_price(symbol);
  order_record(symbol);
  test();
});


// let stock_info;

//     url = `https://cloud.iexapis.com/stable/stock/${symbol}/company?token=${token}`
//     console.log(url);
//     $.ajax({
//         type: "GET",
//         url: url,
//         async: false,
//         data: {},
//         success: function (response) { // 성공하면
//             show_stock_info(response['industry'], response['website'], response['description'], response['sector']);
//             stock_info = {'industry' : response['industry'], 
//             'website': response['website'], 'description' :  response['description'], 'sector' : response['sector']};
//         }
//     })


function stock_price(symbol) {

  //url = `https://finance.yahoo.com/quote/${symbol}/history?period1=1488412800&period2=1593043200&interval=1d&filter=history&frequency=1d`;
  url = `https://finance.yahoo.com/quote/${symbol}/history?p=${symbol}`;

  $.ajax({
    type: "POST",
    url: "/stock_price",
    data: { url_give: url },
    success: function (response) { // 성공하면

      let temp = response['dictionary'];
      temp.forEach(curr => list_price(curr['date'], curr['open'], curr['close'], curr['low'], curr['high'], curr['volume']));

    }
  })
}

function list_price(date, open, close, low, high, volume) {

  let temp_html = `<tr>
    <td>${date}</td>
    <td>${close}</td>
    <td>${open}</td>
    <td>${high}</td>
    <td>${low}</td>
  </tr>`;

  $('#table_price').append(temp_html);

}

function current_price(symbol) {

  url = `https://finance.yahoo.com/quote/${symbol}/history?period1=1488412800&period2=1593043200&interval=1d&filter=history&frequency=1d`

  $.ajax({
    type: "POST",
    url: "/current_price",
    data: { url_give: url },
    success: function (response) { // 성공하면

      $('#price').empty();
      $('#rate').empty();

      let temp = response['price_rate'];

      $('#price').append(temp['price']);
      $('#rate').append(temp['rate']);
    }
  })

  //timer = setTimeout(current_price, 1000, symbol);
}

function calculate() {

  $('#total_price').empty();

  let price = $('#input_price').val();
  let quantity = $('#input_quantity').val();

  $('#total_price').append(price * quantity);

}

function buy() {

  let symbol = $('#stock_symbol').text()
  let date = $('#input_date').val();
  let price = $('#input_price').val();
  let quantity = $('#input_quantity').val();
  let total = $('#total_price').text();

  let inputBox = [['date', date], ['price', price], ['quantity', quantity], ['total', total]];
  let i;
  for (i = 0; i < inputBox.length; i++) {

    if (inputBox[i][1] == '') {
      alert(inputBox[i][0] + '을(를) 입력해라');
      return;
    }
  }


  $.ajax({
    type: "POST",
    url: "/order",
    data: { symbol_give: symbol, date_give: date, price_give: price, quantity_give: quantity, total_give: total },
    success: function (response) { // 성공하면

      if (response['result'] == 'success')
        alert('주문 완료');
      order_record(symbol);
    }
  })


}

function order_record(symbol) {

  $.ajax({
    type: "POST",
    url: "/get_order",
    data: { symbol_give: symbol },
    success: function (response) { // 성공하면

      $('#order_record').empty();
      temp = response['orders'];

      // 개별 매수 기록
      temp.forEach(curr => list_orders(curr['_id'], curr['date'], curr['price'], curr['quantity'], curr['total']));

    }
  })
}

function total_orders(temp) {

  // let total_price = 0;

  // for (i = 0; i < temp.length; i++){
  //   total_price += 
  // }
}

function list_orders(id, date, price, quantity, total) {

  let temp_html = `<tr>
    <td>${date}</td>
    <td>${price}</td>
    <td>${quantity}</td>
    <td>${total}</td>
  </tr>`

  $('#order_record').append(temp_html);

}

function sell_stock(id) {

  let today = new Date();

  let year = today.getFullYear(); // 년도
  let month = today.getMonth() + 1;  // 월
  let date = today.getDate();  // 날짜

  let day = year + '/' + month + '/' + date;



  // $.ajax({
  //   type: "POST",
  //   url: "/sell_stock",
  //   async: false,
  //   data: { symbol_give: symbol, date_give: date, price_give: price, quantity_give: quantity, total_give: total },
  //   success: function (response) {
  //     if (response['result'] == 'success') {
  //       alert('삭제 완료');
  //       window.location.reload();
  //     } else {
  //       alert('서버 오류');
  //     }
  //   }
  // })

  // $.ajax({
  //   type: "DELETE",
  //   url: "/sell_stock",
  //   data: { id_give: id },
  //   success: function (response) {
  //     if (response['result'] == 'success') {
  //       alert('삭제 완료');
  //       window.location.reload();
  //     } else {
  //       alert('서버 오류');
  //     }
  //   }
  // })
}


function test() {
  'use strict'

  feather.replace()

  // Graphs
  var ctx = document.getElementById('myChart')
  // eslint-disable-next-line no-unused-vars
  var myChart = new Chart(ctx, {
    type: 'line',
    data: {
      labels: [
        '선데이',
        'Monday',
        'Tuesday',
        'Wednesday',
        'Thursday',
        'Friday',
        'Saturday'
      ],
      datasets: [{
        data: [
          15339,
          21345,
          18483,
          24003,
          23489,
          24092,
          12034
        ],
        lineTension: 0,
        backgroundColor: 'transparent',
        borderColor: '#007bff',
        borderWidth: 4,
        pointBackgroundColor: '#007bff'
      }]
    },
    options: {
      scales: {
        yAxes: [{
          ticks: {
            beginAtZero: false
          }
        }]
      },
      legend: {
        display: false
      }
    }
  })
}
