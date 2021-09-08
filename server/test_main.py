import pytest
import main
import copy
import json
baseQueryOriginal = {'from': 'USD', 'to': 'JPY', 'amount': 1000}


@pytest.fixture
def client():
    main.app.config["TESTING"] = True
    client = main.app.test_client()
    yield client


def convert_to_query(baseQuery):
    flag = False
    st = ""
    for key, value in baseQuery.items():
        if flag:
            st = st + "&"
        st = st+str(key)+"="+str(value)
        flag = True

    return st


def test_hello(client):
    x = client.get('/')
    assert b"This Currency Exchange API is REST-ful and supports CORS, so it can also be used in web browsers." in x.data, "Looks like the Skeleton is broken"


def test_from_required(client):
    # test from param
    baseQuery = copy.deepcopy(baseQueryOriginal)
    baseQuery.update({"from": None})
    x = client.post('/convert?', query_string=baseQuery)
    assert 400 == x.status_code, "From is a required paramater"


def test_from_required(client):
    baseQuery = copy.deepcopy(baseQueryOriginal)
    baseQuery.update({"from": "ASH"})
    x = client.get('/convert?', query_string=baseQuery)
    assert 400 == x.status_code, " From Currency should be a currency supported by the ECB"


def test_to_required(client):
    baseQuery = copy.deepcopy(baseQueryOriginal)
    baseQuery.update({"to": None})
    x = client.get('/convert?', query_string=baseQuery)
    print(x.status_code)
    assert 400 == x.status_code, "to is required"


def test_to_supported(client):
    baseQuery = copy.deepcopy(baseQueryOriginal)
    baseQuery.update({"to": "ASH"})
    x = client.get('/convert?', query_string=baseQuery)
    print(x.status_code)
    assert 400 == x.status_code, " TO Currency should be a currency supported by the ECB"


def test_amount_required(client):
    baseQuery = copy.deepcopy(baseQueryOriginal)
    baseQuery.update({"amount": None})
    x = client.get('/convert?', query_string=baseQuery)
    print(x.status_code)
    assert 400 == x.status_code, "Amount value should be given"


def test_amount_number(client):
    baseQuery = copy.deepcopy(baseQueryOriginal)
    baseQuery.update({"amount": "ASH"})
    x = client.get('/convert?', query_string=baseQuery)
    print(x.status_code)
    assert 400 == x.status_code, "Amount should be a number"


def test_precision_default(client):
    baseQuery = copy.deepcopy(baseQueryOriginal)
    baseQuery.update({"from": "EUR", "to": "EUR", "amount": 1})
    x = client.get('/convert?', query_string=baseQuery)
    print(x.data)
    val = json.loads(x.data)["message"]
    assert len(val.split(".")[-1]) == 4, "Default presicion is not set to 4"
    assert 200 == x.status_code, "Wrong status code sent"


def test_precision_wrong(client):
    baseQuery = copy.deepcopy(baseQueryOriginal)
    baseQuery.update({"from": "EUR", "to": "EUR",
                      "amount": 1, "precision": -1})
    x = client.get('/convert?', query_string=baseQuery)
    val = json.loads(x.data)["message"]
    assert 400 == x.status_code, "Cannot use negative precision"


def test_precision_6(client):
    baseQuery = copy.deepcopy(baseQueryOriginal)
    baseQuery.update({"from": "EUR", "to": "EUR", "amount": 1, "precision": 6})
    x = client.get('/convert?', query_string=baseQuery)
    val = json.loads(x.data)["message"]
    assert len(val.split(".")[-1]
               ) == 6, "Presicion is not working when set to 6"
    assert 200 == x.status_code, "Wrong status code sent"


def test_convert_any(client):
    baseQuery = copy.deepcopy(baseQueryOriginal)
    baseQuery.update({"from": "USD", "to": "JPY", "amount": 1234})
    x = client.get('/convert?', query_string=baseQuery)
    assert 200 == x.status_code, " Should be able to convert supported currencies "


def test_return_same(client):
    baseQuery = copy.deepcopy(baseQueryOriginal)
    baseQuery.update({"from": "USD", "to": "USD", "amount": 588})
    x = client.get('/convert?', query_string=baseQuery)
    val = json.loads(x.data)["message"]
    assert len(val.split(".")[-1]) == 4, "Presicion is not working as default"
    assert val == "588.0000", "should return same amount"
    assert 200 == x.status_code, " Should be able to convert same currencies "
