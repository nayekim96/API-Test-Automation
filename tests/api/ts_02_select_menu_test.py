import datetime
import pytest
import logging
import json
from conftest import CommonFunction


class TestSelectMenu:
    """
    메뉴 선택 API 테스트
    """

    common_func = CommonFunction()

    def test_case_017(self, api_post, _url, request_data_select):
        """
        정상 CASE
        """
        logging.info("메뉴 선택 정상 CASE - TEST 수행")

        res = api_post(_url, request_data_select)
        
        assert res.status_code == 200, "응답 코드 불일치"
        logging.info("200 정상 코드 반환 확인 완료")

        data = res.json()

        for key, value in data.items():
            assert value is not None, f"'{key}' 파라미터 값이 존재하지 않음"
        
        logging.info("파라미터 값 응답 확인 완료")

        assert data['status'] == 'SUCCESS', "응답 상태 불일치"
        logging.info("응답 상태 확인 완료")
        assert "완료" in data['message'], "응답 메세지 불일치"
        logging.info("응답 메세지 확인 완료")

        res_time = data['timestamp']
        exp_time = data['data']['reservationExpiresAt']

        dt_res_time = datetime.fromisoformat(res_time.replace('Z', '+00:00'))
        dt_exp_time = datetime.fromisoformat(exp_time.replace('Z', '+00:00'))

        diff = dt_res_time - dt_exp_time

        assert int(diff.total_seconds() / 60) == 5, "예약 만료 시간 불일치"
        logging.info("예약 만료 시간(5분) 확인 완료")

        assert data['data']['menuId'] == request_data_select['menuId'], "요청값과 응답값 불일치"
        logging.info("menuId 요청값 - 응답값 일치 확인 완료")
        assert data['data']['quantity'] == request_data_select['quantity'], "요청값과 응답값 불일치"
        logging.info("quantity 요청값 - 응답값 일치 확인 완료")
    
    def test_case_018(self, api_post, _url, request_data_select):
        """
        정상 CASE - 최대 주문 수량 입력
        """
        logging.info("메뉴 선택 정상 CASE - 최대 주문 수량 입력 TEST 수행")

        request_data_select['quantity'] = 99

        res = api_post(_url, request_data_select)
        
        assert res.status_code == 200, "응답 코드 불일치"
        logging.info("200 정상 코드 반환 확인 완료")

        data = res.json()

        for key, value in data.items():
            assert value is not None, f"'{key}' 파라미터 값이 존재하지 않음"

        logging.info("파라미터 값 응답 확인 완료")

        assert data['status'] == 'SUCCESS', "응답 상태 불일치"
        logging.info("응답 상태 확인 완료")
        assert "완료" in data['message'], "응답 메세지 불일치"
        logging.info("응답 메세지 확인 완료")

        assert data['data']['quantity'] == request_data_select['quantity'], "요청값과 응답값 불일치"
        logging.info("quantity 최대 수량 예약 확인 완료")

    def test_case_019(self, api_post, _url, request_data_select):
        """
        에러 CASE - menuId 값 누락
        """
        logging.info("메뉴 선택 에러 CASE - menuId 값 누락 TEST 수행")

        del request_data_select['menuId']

        res = api_post(_url, request_data_select)
        
        assert 400 <= res.status_code < 500, "응답 코드 불일치"
        logging.info("400 에러 코드 반환 확인 완료")

        data = res.json()

        self.common_func.action_check_error(des="상황별 에러 체크", data=data, code='INVALID_REQUEST')

    def test_case_020(self, api_post, _url, request_data_select):
        """
        에러 CASE - quantity 값 누락
        """
        logging.info("메뉴 선택 에러 CASE - quantity 값 누락 TEST 수행")

        del request_data_select['quantity']

        res = api_post(_url, request_data_select)
        
        assert 400 <= res.status_code < 500, "응답 코드 불일치"
        logging.info("400 에러 코드 반환 확인 완료")

        data = res.json()

        self.common_func.action_check_error(des="상황별 에러 체크", data=data, code='INVALID_REQUEST')

    def test_case_021(self, api_post, _url, request_data_select):
        """
        에러 CASE - shopId 값 누락
        """
        logging.info("메뉴 선택 에러 CASE - shopId 값 누락 TEST 수행")

        del request_data_select['shopId']

        res = api_post(_url, request_data_select)
        
        assert 400 <= res.status_code < 500, "응답 코드 불일치"
        logging.info("400 에러 코드 반환 확인 완료")

        data = res.json()

        self.common_func.action_check_error(des="상황별 에러 체크", data=data, code='INVALID_REQUEST')

    def test_case_022(self, api_post, _url, request_data_select):
        """
        에러 CASE - memberNo 값 누락
        """
        logging.info("메뉴 선택 에러 CASE - memberNo 값 누락 TEST 수행")

        del request_data_select['memberNo']

        res = api_post(_url, request_data_select)
        
        assert 400 <= res.status_code < 500, "응답 코드 불일치"
        logging.info("400 에러 코드 반환 확인 완료")

        data = res.json()

        self.common_func.action_check_error(des="상황별 에러 체크", data=data, code='INVALID_REQUEST')

    def test_case_023(self, api_post, _url, request_data_select):
        """
        에러 CASE - 최대 주문 수량 초과 입력
        """
        logging.info("메뉴 선택 에러 CASE - 최대 주문 수량 초과 입력 TEST 수행")

        request_data_select['quantity'] = 100

        res = api_post(_url, request_data_select)
        
        assert 400 <= res.status_code < 500, "응답 코드 불일치"
        logging.info("400 에러 코드 반환 확인 완료")

        data = res.json()
        
        self.common_func.action_check_error(des="상황별 에러 체크", data=data, code='INVALID_REQUEST')

    def test_case_024(self, api_post, _url, request_data_select):
        """
        에러 CASE - 최소 주문 수량 미만 입력
        """
        logging.info("메뉴 선택 에러 CASE - 최소 주문 수량 미만 입력 TEST 수행")

        request_data_select['quantity'] = 0

        res = api_post(_url, request_data_select)
        
        assert 400 <= res.status_code < 500, "응답 코드 불일치"
        logging.info("400 에러 코드 반환 확인 완료")

        data = res.json()

        self.common_func.action_check_error(des="상황별 에러 체크", data=data, code='INVALID_REQUEST')

    def test_case_025(self, api_post, _url, request_data_select):
        """
        에러 CASE - 주문 수량을 음수로 입력
        """
        logging.info("메뉴 선택 에러 CASE - 주문 수량을 음수로 입력 TEST 수행")

        request_data_select['quantity'] = -1

        res = api_post(_url, request_data_select)
        
        assert 400 <= res.status_code < 500, "응답 코드 불일치"
        logging.info("400 에러 코드 반환 확인 완료")

        data = res.json()

        self.common_func.action_check_error(des="상황별 에러 체크", data=data, code='INVALID_REQUEST')

    def test_case_026(self, api_post, _url, request_data_select):
        """
        에러 CASE - 주문 수량을 소수로 입력
        """
        logging.info("메뉴 선택 에러 CASE - 주문 수량을 소수로 입력 TEST 수행")

        request_data_select['quantity'] = 1.1

        res = api_post(_url, request_data_select)
        
        assert 400 <= res.status_code < 500, "응답 코드 불일치"
        logging.info("400 에러 코드 반환 확인 완료")

        data = res.json()

        self.common_func.action_check_error(des="상황별 에러 체크", data=data, code='INVALID_REQUEST')

    def test_case_027(self, api_post, _url, request_data_select):
        """
        에러 CASE - 주문 수량을 문자열로 입력
        """
        logging.info("메뉴 선택 에러 CASE - 주문 수량을 문자열로 입력 TEST 수행")

        request_data_select['quantity'] = "abcd"

        res = api_post(_url, request_data_select)
        
        assert 400 <= res.status_code < 500, "응답 코드 불일치"
        logging.info("400 에러 코드 반환 확인 완료")

        data = res.json()

        self.common_func.action_check_error(des="상황별 에러 체크", data=data, code='INVALID_REQUEST')

    def test_case_028(self, api_post, _url, request_data_select):
        """
        에러 CASE - 존재하지 않는 가게 ID 입력
        """
        logging.info("메뉴 선택 에러 CASE - 존재하지 않는 가게 ID 입력 TEST 수행")

        request_data_select['shopId'] = "ABABABAB"

        res = api_post(_url, request_data_select)
        
        assert 400 <= res.status_code < 500, "응답 코드 불일치"
        logging.info("400 에러 코드 반환 확인 완료")

        data = res.json()

        self.common_func.action_check_error(des="상황별 에러 체크", data=data, code='INVALID_REQUEST')

    def test_case_029(self, api_post, _url, request_data_select):
        """
        에러 CASE - 존재하지 않는 회원번호 입력
        """
        logging.info("메뉴 선택 에러 CASE - 존재하지 않는 회원번호 입력 TEST 수행")

        request_data_select['memberNo'] = "ABABABAB"

        res = api_post(_url, request_data_select)
        
        assert 400 <= res.status_code < 500, "응답 코드 불일치"
        logging.info("400 에러 코드 반환 확인 완료")

        data = res.json()

        self.common_func.action_check_error(des="상황별 에러 체크", data=data, code='INVALID_REQUEST')

    def test_case_030(self, api_post, _url, request_data_select):
        """
        에러 CASE - 주문 가능 수량 초과 입력 (주문 가능 수량 : 5)
        """
        logging.info("메뉴 선택 에러 CASE - 주문 가능 수량 초과 입력 TEST 수행")

        request_data_select['quantity'] = 6

        res = api_post(_url, request_data_select)
        
        assert 400 <= res.status_code < 500, "응답 코드 불일치"
        logging.info("400 에러 코드 반환 확인 완료")

        data = res.json()

        self.common_func.action_check_error(des="상황별 에러 체크", data=data, code='INSUFFICIENT_INGREDIENTS')

    def test_case_031(self, api_post, _url, request_data_select):
        """
        에러 CASE - 존재하지 않는 메뉴명 입력
        """
        logging.info("메뉴 선택 에러 CASE - 존재하지 않는 메뉴명 입력 TEST 수행")

        request_data_select['menuId'] = "ABABABAB"

        res = api_post(_url, request_data_select)
        
        assert 400 <= res.status_code < 500, "응답 코드 불일치"
        logging.info("400 에러 코드 반환 확인 완료")

        data = res.json()

        self.common_func.action_check_error(des="상황별 에러 체크", data=data, code='MENU_NOT_FOUND')
        