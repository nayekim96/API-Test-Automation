import re
import datetime
import time
import pytest
import logging
import json
from conftest import CommonFunction


class TestCreateOrder:
    """
    주문 생성 API 테스트
    """

    common_func = CommonFunction()

    def test_case_032(self, api_post, _url, request_data_create, get_reservation_id):
        """
        정상 CASE
        """
        logging.info("주문 생성 정상 CASE - TEST 수행")

        reservationId = get_reservation_id
        request_data_create['reservationId'] = reservationId
    
        res = api_post(_url, request_data_create)
        
        assert res.status_code == 200, "응답 코드 불일치"
        logging.info("200 정상 코드 반환 확인 완료")

        data = res.json()

        for key, value in data.items():
            assert value is not None, f"'{key}' 파라미터 값이 존재하지 않음"
        
        logging.info("파라미터 값 응답 확인 완료")

        assert data['status'] == 'SUCCESS', "응답 상태 불일치"
        logging.info("응답 상태 확인 완료")

        assert "성공적으로 생성" in data['message'], "응답 메세지 불일치"
        logging.info("응답 메세지 확인 완료")

        orderNo = data['data']['orderNo']
        pattern = r'[A-Za-z0-9]+'

        assert len(orderNo) == 8 and re.fullmatch(pattern, orderNo), "응답 값이 영문/숫자 8자리 문자열이 아님"
        logging.info("주문번호 유효성 확인 완료")

        assert data['data']['orderStatus'] == 'INITIALIZING', "주문 상태 메세지 불일치"
        logging.info("주문 상태 메세지 확인 완료")

        assert data['data']['reservationId'] == request_data_create['reservationId'], "요청값과 응답값 불일치"
        logging.info("reservationId 요청값 - 응답값 일치 확인 완료")

        assert data['data']['memberNo'] == request_data_create['memberNo'], "요청값과 응답값 불일치"
        logging.info("memberNo 요청값 - 응답값 일치 확인 완료")

    def test_case_033(self, api_post, _url, request_data_create, get_reservation_id):  
        """
        에러 CASE - 중복 생성 요청
        """
        logging.info("주문 생성 에러 CASE - 중복 생성 요청 TEST 수행")

        reservationId = get_reservation_id
        request_data_create['reservationId'] = reservationId

        res = api_post(_url, request_data_create)
        
        assert 400 <= res.status_code < 500, "응답 코드 불일치"
        logging.info("400 에러 코드 반환 확인 완료")

        data = res.json()

        self.common_func.action_check_error(des="상황별 에러 체크", data=data, code='INVALID_REQUEST') 

    def test_case_034(self, api_post, _url, request_data_create):
        """
        에러 CASE - reservationId 값 누락
        """
        logging.info("주문 생성 에러 CASE - reservationId 값 누락 TEST 수행")
        
        del request_data_create['reservationId']

        res = api_post(_url, request_data_create)
        
        assert 400 <= res.status_code < 500, "응답 코드 불일치"
        logging.info("400 에러 코드 반환 확인 완료")

        data = res.json()

        self.common_func.action_check_error(des="상황별 에러 체크", data=data, code='INVALID_REQUEST')

    def test_case_035(self, api_post, _url, request_data_create, get_reservation_id):
        """
        에러 CASE - memberNo 값 누락
        """
        logging.info("주문 생성 에러 CASE - memberNo 값 누락 TEST 수행")

        reservationId = get_reservation_id
        request_data_create['reservationId'] = reservationId
        
        del request_data_create['memberNo']

        res = api_post(_url, request_data_create)
        
        assert 400 <= res.status_code < 500, "응답 코드 불일치"
        logging.info("400 에러 코드 반환 확인 완료")

        data = res.json()

        self.common_func.action_check_error(des="상황별 에러 체크", data=data, code='INVALID_REQUEST')

    def test_case_036(self, api_post, _url, request_data_create):
        """
        에러 CASE - 생성된 예약 ID와 다른 값 입력
        """
        logging.info("주문 생성 에러 CASE - 생성된 예약 ID와 다른 값 입력 TEST 수행")
        
        request_data_create['reservationId'] = 'RSV_ABAB9999'

        res = api_post(_url, request_data_create)
        
        assert 400 <= res.status_code < 500, "응답 코드 불일치"
        logging.info("400 에러 코드 반환 확인 완료")

        data = res.json()

        self.common_func.action_check_error(des="상황별 에러 체크", data=data, code='INVALID_RESERVATION')

    def test_case_037(self, api_post, _url, request_data_create, get_reservation_id):
        """
        에러 CASE - 예약한 회원번호와 다른 값 입력
        """
        logging.info("주문 생성 에러 CASE - 예약한 회원번호와 다른 값 입력 TEST 수행")

        reservationId = get_reservation_id
        request_data_create['reservationId'] = reservationId
        
        request_data_create['memberNo'] = 'member_321'

        res = api_post(_url, request_data_create)
        
        assert 400 <= res.status_code < 500, "응답 코드 불일치"
        logging.info("400 에러 코드 반환 확인 완료")

        data = res.json()

        self.common_func.action_check_error(des="상황별 에러 체크", data=data, code='INVALID_RESERVATION')

    def test_case_038(self, api_post, _url, request_data_create, get_reservation_id):
        """
        에러 CASE - 재료 소진 주문 실패 확인

        가게 재료 소진 상태 사전 설정 필요
        """
        logging.info("주문 생성 에러 CASE - 재료 소진 주문 실패 확인 TEST 수행")

        reservationId = get_reservation_id
        request_data_create['reservationId'] = reservationId
        
        res = api_post(_url, request_data_create)
        
        assert 400 <= res.status_code < 500, "응답 코드 불일치"
        logging.info("400 에러 코드 반환 확인 완료")

        data = res.json()

        self.common_func.action_check_error(des="상황별 에러 체크", data=data, code='INGREDIENTS_EXHAUSTED')

    def test_case_039(self, api_post, _url, request_data_create, get_reservation_id):
        """
        에러 CASE - 예약 만료 이후 주문 생성
        """
        logging.info("주문 생성 에러 CASE - 예약 만료 이후 주문 생성 TEST 수행")

        reservationId = get_reservation_id
        request_data_create['reservationId'] = reservationId

        logging.info("5분간 대기")
        time.sleep(300)
        
        res = api_post(_url, request_data_create)
        
        assert 400 <= res.status_code < 500, "응답 코드 불일치"
        logging.info("400 에러 코드 반환 확인 완료")

        data = res.json()

        self.common_func.action_check_error(des="상황별 에러 체크", data=data, code='RESERVATION_EXPIRED')
        