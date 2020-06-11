
const price = 1500; //물건 가격

function order() {

    let name = $('#name').val();
    let address = $('#address').val();
    let phone = $('#phone_num').val();
    let num = $('#num').val();
    let sum = 0;

    let inputBox = [['이름', name], ['주소', address], ['전화번호', phone]];
    let i;
    for (i = 0; i < inputBox.length; i++) {
        if (i == 2) {
            let temp = inputBox[i][1].split('-');
            console.log(temp.length);
            if (temp.length == 3) {
                if (temp[0] == '010' && temp[1].length == 4 && temp[2].length == 4) {
                    continue;
                }
                else {
                    alert('010-xxxx-xxxx 식으로 입력하세요'); return;
                }
            }
            else {
                alert('010-xxxx-xxxx 식으로 입력하세요'); return;
            }
        }
        else if (inputBox[i][1] == '') {
            alert(inputBox[i][0] + '을(를) 입력해 주세요');
            return;
        }
    }
    if (i == inputBox.length) {

        sum = $('#num').val() * price;

    }


    //ajax 통신
    $.ajax({
        type: "POST",
        url: "/order",
        data: {
            name_give: name,
            num_give: num,
            address_give: address,
            phone_give: phone
        },
        success: function (response) { // 성공하면
            if (response['result'] == 'success') {
                alert('주문 완료, 총 가격 : $ ' + sum);
                window.location.reload();
            }
        }
    });

    // if($('#name').val() == '')
    //     alert('이름을 입력해주세요');
    // else if($('#address').val() == '')
    //     alert('주소를 입력해주세요');
    // else if($('#phone_num').val() == '')
    //     alert('전화번호를 입력해주세요');
    // else
    //     alert('주문 완료'); 

    //poly fill, 웹 표준 맞추는것이 필요
    //poly fill이란 크롬에서는 A라는 코드만 쳐도 제대로 동작하는것을 IE에서는 a+b+c로 자동으로 코드가 변경되어 동일한 동작을 할 수 있도록 해줌   

}

//$document.ready는 한번만 실행됨
$(document).ready(function () {

    let temp = "가격 : $ " + price + " / 세트";

    $('#price').append(temp);

    updateData();
    listing();
});

function listing() {

    

    $.ajax({
        type: "GET",
        url: "/order",
        data: {},
        success: function (response) {
            if (response['result'] == 'success') {
                let orders = response['orders'];
                let i = 1;
                orders.forEach(curr => make_card(i++, curr['name'], curr['num'], curr['address'], curr['phone']));

                // 2. 성공했을 때 리뷰를 올바르게 화면에 나타내기
            } else {
                alert('리뷰를 받아오지 못했습니다');
            }
        }
    });
}

function make_card(i, name, num, address, phone) {

    let temp_html = `<tr>
    <th scope="row">${i}</th>
    <td>${name}</td>
    <td>${num}</td>
    <td>${address}</td>
    <td>${phone}</td>
  </tr>`

    $('#order_table').append(temp_html);

}

function updateData() {

    $('#append').empty();

    $.ajax({

        type: "GET", // GET 방식으로 요청한다.
        url: "https://api.manana.kr/exchange/rate.json",
        data: {}, // 요청하면서 함께 줄 데이터 (GET 요청시엔 비워두세요)

        success: function (r) { // 서버에서 준 결과를 response라는 변수에 담음
            console.log(r); // 서버에서 준 결과를 이용해서 나머지 코드를 작성

            let rate = r[1]['rate']; //일단 url만 넣어주고
            console.log(rate);
            let temp = " (USD 환율 : " + rate + ")";
            // let temp_html = `<span id = "ajax" class = "blue">${temp}</span>`

            $('#append').append(temp);

        }
    });

    /*setTimeout은 원래 한번만 실행되고 마는 메소드이지만
    매개함수로 가지고 있는 updateData()에 의해 재귀적으로 호출된다
    */
    timer = setTimeout("updateData()", 3000);
}
