import json
import pytest
import logging
import requests


class Environment:
    """
    환경변수
    """
    head = {'Authoriztion': 'Bearer test-api-token-12345', 'Content-Type': 'application/json;charset=UTF-8'}
    select_endpoint = '/api/v1/menu/select'
    create_endpoint = '/api/v1/order/create'


class CommonFunction(object):
    """
    Common 함수
    """
    def action_check_error(self, data, des="", code=""):
        """
        상황별 에러 체크

        :param des: 함수 설명
        :param data: 응답 본문
        :param code: 확인하려는 코드 ex) INVALID_REQUEST, RESERVATION_EXPIRED...
        """
        if code == 'INVALID_REQUEST':
            message = '잘못된 요청'
        elif code == 'INSUFFICIENT_INGREDIENTS':
            message = '재료가 부족'
        elif code == 'MENU_NOT_FOUND':
            message = '메뉴가 존재하지 않습니다'
        elif code == ' RESERVATION_EXPIRED':
            message = '만료된 예약'
        elif code == 'INGREDIENTS_EXHAUSTED':
            message = '재료가 소진'
        elif code == 'INVALID_RESERVATION':
            message = '유효하지 않은 예약'
            

        assert data['status'] == 'ERROR', "응답 상태 불일치"
        logging.info("에러 상태 확인 완료")

        assert message in data['message'], "응답 메세지 불일치"
        logging.info("에러 메세지 확인 완료")

        assert data['errorCode'] == code, "에러 코드 불일치"
        logging.info("에러 코드 확인 완료")


@pytest.fixture(scope="session")
def _url():
    """
    Common API URL
    """
    return "https://api-test.fooddelivery.com"

@pytest.fixture(scope="session")
def api_client():
    """
    API 클라이언트 - requests session
    """
    session = requests.Session()
    session.headers.update(Environment.head)
    session.timeout = 10
    yield session
    session.close()

@pytest.fixture
def api_post(api_client):
    """
    API POST - POST 수행 후 report에 log 출력
    """
    def _call(_url, request_data):
        response = api_client.post(_url, json=request_data)
        
        # 응답 본문 log 출력
        try:
            formatted_body = json.dumps(response.json(), indent=4, ensure_ascii=False)
            logging.info(f"POST 성공! 응답 본문:\n{formatted_body}")
        except json.JSONDecodeError:
            logging.info(f"POST 성공! 응답 본문:\n{formatted_body}")

        return response
    
    return _call

@pytest.fixture(scope="session")
def get_reservation_id(api_post, _url, request_data_select):
    """
    메뉴 선택 후 reservationId 반환
    """
    logging.info("메뉴 선택 정상 CASE - TEST 수행")

    res = api_post(_url, request_data_select)
    res.raise_for_status()

    data = res.json()
    reservationId = data['data']['reservationId']

    if reservationId is not None:
        return reservationId

    else:
        return "예약 ID가 응답 본문에 없습니다."

@pytest.fixture
def request_data_select():
    """
    메뉴 예약 요청 데이터
    """
    
    return {
        "menuId":"menu_001",
        "quantity":2,
        "shopId":"shop_001",
        "memberNo":"member_123"
    }

@pytest.fixture
def request_data_create():
    """
    주문 생성 요청 데이터
    """
    
    return  {
        "reservationId":"RSV_A7K9M2X8",
        "memberNo":"member_123"
    }