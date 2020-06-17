$(document).ready(function () {

    save_article();
    get_article();
    post_index();
    get_index();

});

function save_article() {
    $.ajax({
        type: "POST",
        url: "/article",
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

    $.ajax({
        type: "POST",
        url: "/index",
        data: { url_give: 'https://kr.investing.com/indices/us-30' },
        success: function (response) {
            if (response['result'] == 'success') {
            }
        }
    })
}

function get_index() {

    $.ajax({
        type: "GET",
        url: "/index",
        data: {},
        success: function (response) {
            if (response['result'] == 'success') {
                let index = response['dow_index']
                make_index(index['dow_index'], index['date'] );
            }
        }
    })
}

function make_index(index, date) {

    let temp_html = `<div class="col p-4 d-flex flex-column position-static">
        <strong class="d-inline-block mb-2 text-primary">다우 지수</strong>
        <h3 class="mb-0">${index}</h3>
        <div class="mb-1 text-muted">${date}</div>
        <p class="card-text mb-auto">This is a wider card with supporting text below as a natural
                    lead-in to additional content.</p>
        <a href="#" class="stretched-link">Continue reading</a>
    </div>`;

    $('#index-card').append(temp_html);
}


