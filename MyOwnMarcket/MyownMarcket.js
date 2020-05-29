
const price = 1500; //물건 가격

function order() {

    let inputBox = [['이름', $('#name').val()], ['주소', $('#address').val()], ['전화번호', $('#phone_num').val()]];
    let i;
    for (i = 0; i < inputBox.length; i++) {
        if (inputBox[i][1] == '') {
            alert(inputBox[i][0] + '을(를) 입력해 주세요');
            break;
        }
    }
    if (i == inputBox.length){
        
        let sum = $('#num').val() * price;

        alert('주문 완료, 총 가격 : $ ' + sum);
    }

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
});

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
