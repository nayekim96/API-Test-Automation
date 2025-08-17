import pytest
import requests
import logging
import json
from conftest import Environment as env


class TestCommonHeader:
    """
    헤더 API 테스트
    """

    def test_case_001(self, api_client, request_data_select):
        """
        [헤더 - 메뉴 선택] 정상 CASE
        """
        logging.info("메뉴 선택 헤더 정상 CASE - TEST 수행")

        url = "https://api-test.fooddelivery.com" + env.select_endpoint
        header = env.head

        res = api_client.post(url, headers=header, json=request_data_select)
        
        assert res.status_code == 200, "응답 코드가 일치하지 않습니다."
        logging.info("200 정상 코드 반환 확인 완료")

    def test_case_002(self, api_client, request_data_select):
        """
        [헤더 - 메뉴 선택] 에러 CASE - Authorization 값 누락
        """
        logging.info("메뉴 선택 헤더 에러 CASE - Authorization 값 누락 TEST 수행")

        url = "https://api-test.fooddelivery.com" + env.select_endpoint
        header = {'Content-Type': 'application/json;charset=UTF-8'}

        res = api_client.post(url, headers=header, json=request_data_select)
        
        assert 400 <= res.status_code < 500, "응답 코드가 일치하지 않습니다."
        logging.info("4xx 에러 코드 반환 확인 완료")

    def test_case_003(self, api_client):
        """
        [헤더 - 메뉴 선택] 에러 CASE - Host 값 누락
        """
        logging.info("메뉴 선택 헤더 에러 CASE - Host 값 누락 TEST 수행")

        url = ""

        with pytest.raises(requests.exceptions.MissingSchema):
            api_client.get(url)

        logging.info("예외 발생 확인 완료")

    def test_case_004(self, api_client, request_data_select):
        """
        [헤더 - 메뉴 선택] 에러 CASE - 만료된 Authorization 값 입력
        """
        logging.info("메뉴 선택 헤더 에러 CASE - 만료된 Authorization 값 입력 TEST 수행")

        url = "https://api-test.fooddelivery.com" + env.select_endpoint
        # 가상의 만료된 토큰
        header = {'Authoriztion': 'expired-api-token', 'Content-Type': 'application/json;charset=UTF-8'}

        res = api_client.post(url, headers=header, json=request_data_select)
        
        assert 400 <= res.status_code < 500, "응답 코드가 일치하지 않습니다."
        logging.info("4xx 에러 코드 반환 확인 완료")

    def test_case_005(self, api_client):
        """
        [헤더 - 메뉴 선택] 에러 CASE - 만료된 Host 값 입력
        """
        logging.info("메뉴 선택 헤더 에러 CASE - 만료된 Host 값 입력 TEST 수행")

        # 가상의 만료된 URL
        url = "https://expired-api-test.fooddelivery.com"
    
        with pytest.raises(requests.exceptions.ConnectionError):
            api_client.get(url)

        logging.info("예외 발생 확인 완료")

    def test_case_006(self, api_client, request_data_select):
        """
        [헤더 - 메뉴 선택] 에러 CASE - 잘못된 Authorization 값 입력
        """
        logging.info("메뉴 선택 헤더 에러 CASE - 잘못된 Authorization 값 입력 TEST 수행")

        url = "https://api-test.fooddelivery.com" + env.select_endpoint
        header = {'Authoriztion': 'Bearertest-api-token-45678', 'Content-Type': 'application/json;charset=UTF-8'}

        res = api_client.post(url, headers=header, json=request_data_select)
        
        assert 400 <= res.status_code < 500, "응답 코드가 일치하지 않습니다."
            
        logging.info("4xx 에러 코드 반환 확인 완료")

    def test_case_007(self, api_client, request_data_select):
        """
        [헤더 - 메뉴 선택] 에러 CASE - 잘못된 Host 값 입력
        """
        logging.info("메뉴 선택 헤더 에러 CASE - 잘못된 Host 값 입력 TEST 수행")

        url = "https://api-test.fooddelivery.com123" + env.select_endpoint
        header = {'Authoriztion': 'Bearertest-api-token-12345', 'Content-Type': 'application/json;charset=UTF-8'}

        res = api_client.post(url, headers=header, json=request_data_select)
        
        assert 400 <= res.status_code < 500, "응답 코드가 일치하지 않습니다."
            
        logging.info("4xx 에러 코드 반환 확인 완료")

    def test_case_008(self, api_client, request_data_select):
        """
        [헤더 - 메뉴 선택] 에러 CASE - 잘못된 Content-Type 값 입력
        """
        logging.info("메뉴 선택 헤더 에러 CASE - 잘못된 Content-Type 값 입력 TEST 수행")

        url = "https://api-test.fooddelivery.com123" + env.select_endpoint
        header = {'Authoriztion': 'Bearertest-api-token-12345', 'Content-Type': 'application/xml'}

        res = api_client.post(url, headers=header, json=request_data_select)
        
        assert 400 <= res.status_code < 500, "응답 코드가 일치하지 않습니다."
            
        logging.info("4xx 에러 코드 반환 확인 완료")

    def test_case_009(self, api_client, request_data_select):
        """
        [헤더 - 주문 생성] 정상 CASE
        """
        logging.info("주문 생성 헤더 정상 CASE - TEST 수행")

        url = "https://api-test.fooddelivery.com" + env.create_endpoint
        header = env.head

        res = api_client.post(url, headers=header, json=request_data_select)
        
        assert res.status_code == 200, "응답 코드가 일치하지 않습니다."
        logging.info("200 정상 코드 반환 확인 완료")

    def test_case_010(self, api_client, request_data_select):
        """
        [헤더 - 주문 생성] 에러 CASE - Authorization 값 누락
        """
        logging.info("주문 생성 헤더 에러 CASE - Authorization 값 누락 TEST 수행")

        url = "https://api-test.fooddelivery.com" + env.create_endpoint
        header = {'Content-Type': 'application/json;charset=UTF-8'}

        res = api_client.post(url, headers=header, json=request_data_select)
        
        assert 400 <= res.status_code < 500, "응답 코드가 일치하지 않습니다."
        logging.info("4xx 에러 코드 반환 확인 완료")

    def test_case_011(self, api_client):
        """
        [헤더 - 주문 생성] 에러 CASE - Host 값 누락
        """
        logging.info("주문 생성 헤더 에러 CASE - Host 값 누락 TEST 수행")

        url = ""

        with pytest.raises(requests.exceptions.MissingSchema):
            api_client.get(url)

        logging.info("예외 발생 확인 완료")

    def test_case_012(self, api_client, request_data_select):
        """
        [헤더 - 주문 생성] 에러 CASE - 만료된 Authorization 값 입력
        """
        logging.info("주문 생성 헤더 에러 CASE - 만료된 Authorization 값 입력 TEST 수행")

        url = "https://api-test.fooddelivery.com" + env.create_endpoint
        # 가상의 만료된 토큰
        header = {'Authoriztion': 'expired-api-token', 'Content-Type': 'application/json;charset=UTF-8'}

        res = api_client.post(url, headers=header, json=request_data_select)
        
        assert 400 <= res.status_code < 500, "응답 코드가 일치하지 않습니다."
        logging.info("4xx 에러 코드 반환 확인 완료")

    def test_case_013(self, api_client):
        """
        [헤더 - 주문 생성] 에러 CASE - 만료된 Host 값 입력
        """
        logging.info("주문 생성 헤더 에러 CASE - 만료된 Host 값 입력 TEST 수행")

        # 가상의 만료된 URL
        url = "https://expired-api-test.fooddelivery.com"
    
        with pytest.raises(requests.exceptions.ConnectionError):
            api_client.get(url)

        logging.info("예외 발생 확인 완료")

    def test_case_014(self, api_client, request_data_select):
        """
        [헤더 - 주문 생성] 에러 CASE - 잘못된 Authorization 값 입력
        """
        logging.info("주문 생성 헤더 에러 CASE - 잘못된 Authorization 값 입력 TEST 수행")

        url = "https://api-test.fooddelivery.com" + env.create_endpoint
        header = {'Authoriztion': 'Bearertest-api-token-45678', 'Content-Type': 'application/json;charset=UTF-8'}

        res = api_client.post(url, headers=header, json=request_data_select)
        
        assert 400 <= res.status_code < 500, "응답 코드가 일치하지 않습니다."
            
        logging.info("4xx 에러 코드 반환 확인 완료")

    def test_case_015(self, api_client, request_data_select):
        """
        [헤더 - 주문 생성] 에러 CASE - 잘못된 Host 값 입력
        """
        logging.info("주문 생성 헤더 에러 CASE - 잘못된 Host 값 입력 TEST 수행")

        url = "https://api-test.fooddelivery.com123" + env.create_endpoint
        header = {'Authoriztion': 'Bearertest-api-token-12345', 'Content-Type': 'application/json;charset=UTF-8'}

        res = api_client.post(url, headers=header, json=request_data_select)
        
        assert 400 <= res.status_code < 500, "응답 코드가 일치하지 않습니다."
            
        logging.info("4xx 에러 코드 반환 확인 완료")

    def test_case_016(self, api_client, request_data_select):
        """
        [헤더 - 주문 생성] 에러 CASE - 잘못된 Content-Type 값 입력
        """
        logging.info("주문 생성 헤더 에러 CASE - 잘못된 Content-Type 값 입력 TEST 수행")

        url = "https://api-test.fooddelivery.com123" + env.create_endpoint
        header = {'Authoriztion': 'Bearertest-api-token-12345', 'Content-Type': 'application/xml'}

        res = api_client.post(url, headers=header, json=request_data_select)
        
        assert 400 <= res.status_code < 500, "응답 코드가 일치하지 않습니다."
            
        logging.info("4xx 에러 코드 반환 확인 완료")
