$(document).ready(function () {

    post_index(); //각 시장의 지수 가져오기
    save_article();
    get_article();

});

function save_article() {
    $.ajax({
        type: "POST",
        url: "/article",
        sync: false,
        data: { url_give: 'https://kr.investing.com/news/most-popular-news' },
        success: function (response) {
            if (response['result'] == 'success') {

                // 2. 성공했을 때 리뷰를 올바르게 화면에 나타내기
            } else {
                alert('리뷰를 받아오지 못했습니다');
            }
        }
    });
}

function get_article() {

    $.ajax({
        type: "GET",
        url: "/article",
        data: {},
        success: function (response) {
            if (response['result'] == 'success') {
                let articles = response['articles']
                make_card(articles['url'], articles['image'], articles['title'], articles['desc']);

            }
        }
    })
}

function make_card(url, image, title, desc) {

    let urll = 'https://kr.investing.com/equities/apple-computer-inc'
    let temp_html = `<div class="px-0">
                        <img class = "rounded article-img" src="${image}">
                        <div>
                            <h1 class="display-4 font-italic">${title}</h1>
                            <p class="lead my-3">${desc}</p>
                            <p class="lead mb-0"><a href="${url}" class="text-white font-weight-bold">Contiue reading ...</a></p>
                        </div>               
                </div>`;

    $('#main-box').append(temp_html);
}

function post_index() {

    //다우, 나스닥 지수 db에 저장
    $.ajax({
        type: "POST",
        url: "/index",
        data: { url_give_dow: 'https://kr.investing.com/indices/us-30', url_give_nasdaq: 'https://kr.investing.com/indices/nq-100' },
        success: function (response) {
            if (response['result'] == 'success') {
                let index = response['result_index'];
                make_index_dow(index[0]['index'], index[0]['change'], index[0]['percent'], index[0]['date']);
                make_index_nasdaq(index[1]['index'], index[1]['change'], index[1]['percent'], index[1]['date']);
            }
        }
    })
}

function make_index_dow(index, change, percent, date) {

    let temp_html;
    if (change < 0) {
        temp_html = `<div class="col p-4 d-flex flex-column position-static">
        <strong class="d-inline-block mb-2 text-primary">다우 존스</strong>
        <h3 class="mb-0">${index}</h3>
        <div class="mb-1 text-muted">${date}</div>
        <p class="exchange-blue card-text mb-auto">${change}</p>
        <p class="exchange-blue card-text mb-auto">${percent}</p>
    </div>`;
    }
    else if (change == 0) {
        temp_html = `<div class="col p-4 d-flex flex-column position-static">
        <strong class="d-inline-block mb-2 text-primary">다우 존스</strong>
        <h3 class="mb-0">${index}</h3>
        <div class="mb-1 text-muted">${date}</div>
        <p class="exchange card-text mb-auto">${change}</p>
        <p class="exchange card-text mb-auto">${percent}</p>
    </div>`;
    } 
    else {
        temp_html = `<div class="col p-4 d-flex flex-column position-static">
        <strong class="d-inline-block mb-2 text-primary">다우 존스</strong>
        <h3 class="mb-0">${index}</h3>
        <div class="mb-1 text-muted">${date}</div>
        <p class="exchange-red card-text mb-auto">${change}</p>
        <p class="exchange-red card-text mb-auto">${percent}</p>
    </div>`;
    }

    $('#dow-index-card').append(temp_html);
}

function make_index_nasdaq(index, change, percent, date) {

    let temp_html;
    if (change < 0) {
        temp_html = `<div class="col p-4 d-flex flex-column position-static">
        <strong class="d-inline-block mb-2 text-primary">나스닥</strong>
        <h3 class="mb-0">${index}</h3>
        <div class="mb-1 text-muted">${date}</div>
        <p class="exchange-blue card-text mb-auto">${change}</p>
        <p class="exchange-blue card-text mb-auto">${percent}</p>
    </div>`;
    }
    else if (change == 0) {
        temp_html = `<div class="col p-4 d-flex flex-column position-static">
        <strong class="d-inline-block mb-2 text-primary">나스닥</strong>
        <h3 class="mb-0">${index}</h3>
        <div class="mb-1 text-muted">${date}</div>
        <p class="exchange card-text mb-auto">${change}</p>
        <p class="exchange card-text mb-auto">${percent}</p>
    </div>`;
    } 
    else {
        temp_html = `<div class="col p-4 d-flex flex-column position-static">
        <strong class="d-inline-block mb-2 text-primary">나스닥</strong>
        <h3 class="mb-0">${index}</h3>
        <div class="mb-1 text-muted">${date}</div>
        <p class="exchange-red card-text mb-auto">${change}</p>
        <p class="exchange-red card-text mb-auto">${percent}</p>
    </div>`;
    }

    $('#nasdaq-index-card').append(temp_html);
}

function search() {

    let url = 'https://kr.investing.com/search/?q=';
    let stock_name = $('#stock').val();

    $.ajax({
        type: "POST",
        url: "/search",
        data: { url_give: url, stock_give: stock_name },
        success: function (response) { // 성공하면
            if (response['result'] == 'success') {
                $('#stock_table').empty();
                let datas = response['dictionary'];
                datas.forEach(curr => make_board(curr['href'], curr['symbol'], curr['name'], curr['exchange']));
            } else if (response['result'] == 'fail') {
                window.location.reload();
            } else {
                alert('서버오류남ㅋㅋㅋ');
            }
        }
    })
}

function make_board(href, symbol, name, exchange) {
    let base_url = 'https://kr.investing.com';
    let url = base_url + href;

    let temp_html = `<tr style="cursor:pointer;" onClick="show_stock('${symbol}')">
    <td>${name}</td>
    <td>${symbol}</td>
    <td>${exchange}</td>
  </tr>`;

    $('#stock_table').append(temp_html);

}

function get_stock_value(symbol, token) {

    let stock_value;

    url = `https://cloud.iexapis.com/stable/stock/${symbol}/quote?token=${token}`;
    //url = "https://cloud.iexapis.com/stable/stock/aapl/quote?token=pk_31c6148666914eaf9e526964898f75ab";

    $.ajax({
        type: "GET",
        url: url,
        async: false,
        data: {},
        success: function (response) { // 성공하면
            show_stock_value(response['symbol'], response['companyName'], response['primaryExchange'], response['close']);
            stock_value = {
                'symbol': response['symbol'], 'companyName': response['companyName'],
                'primaryExchange': response['primaryExchange'], 'close': response['close']
            };
        }
    })
    return stock_value;
}

function get_stock_info(symbol, token) {

    let stock_info;

    url = `https://cloud.iexapis.com/stable/stock/${symbol}/company?token=${token}`
    console.log(url);
    $.ajax({
        type: "GET",
        url: url,
        async: false,
        data: {},
        success: function (response) { // 성공하면
            show_stock_info(response['industry'], response['website'], response['description'], response['sector']);
            stock_info = {
                'industry': response['industry'],
                'website': response['website'], 'description': response['description'], 'sector': response['sector']
            };
        }
    })

    return stock_info;
}

//symbol, companyName, primaryExchange, close
function show_stock_info(industry, website, description, sector) {

    //<div class="col p-4 d-flex flex-column position-static">

    let temp_html = `<div class="col p-4 d-flex flex-column position-static">
    <h5 id = "industry" class="mb-0">${industry}</h5>
    <div id = "website" class="mb-1 text-muted">${website}</div>
    <div id = "sector" class="mb-1 text-muted">${sector}</div>
    <p id = "description" class="mb-auto">${description}</p>
</div>`;

    $('#main-right').append(temp_html);
}

function show_stock_value(symbol, companyName, primaryExchange, close) {

    let temp_html = `<div class="col p-4 d-flex flex-column position-static">
    <h5 id = "symbol" class="mb-0">${symbol}</h5>
    <div id = "companyName" class="mb-1 text-muted">${companyName}</div>
    <div id = "primaryExchange" class="mb-1 text-muted">${primaryExchange}</div>
    <p id = "close" class="mb-auto">${close}</p>
    <a href="#" onClick="save_stock()" class="stretched-link">관심종목 추가</a>
    </div>`;

    $('#main-right').prepend(temp_html);
}

function show_stock(symbol) {

    let token = "pk_31c6148666914eaf9e526964898f75ab";

    $('#main-right').empty();

    get_stock_value(symbol, token);
    get_stock_info(symbol, token);

}

function save_stock() {

    let companyName = $('#companyName').text();
    let symbol = $('#symbol').text();
    let primaryExchange = $('#primaryExchange').text();
    let close = $('#close').text();
    let industry = $('#industry').text();
    let website = $('#website').text();
    let sector = $('#sector').text();
    let description = $('#description').text();

    $.ajax({
        type: "POST",
        url: "/stock",
        data: {
            companyName: companyName, symbol: symbol, primaryExchange: primaryExchange, close: close,
            industry: industry, website: website, sector: sector, description: description
        },
        success: function (response) {
            if (response['result'] == 'success') {
                alert('관심종목에 추가 완료')
            }
        }
    })
}

