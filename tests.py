import pytest
import csv
from main import load_csv, apply_filter, apply_aggregate, apply_sort

@pytest.fixture
def sample_csv_data(tmp_path):
    data = """name,brand,price,rating
iphone 15 pro,apple,999,4.9
galaxy s23 ultra,samsung,1199,4.8
redmi note 12,xiaomi,199,4.6
iphone 14,apple,799,4.7
galaxy a54,samsung,349,4.2
poco x5 pro,xiaomi,299,4.4
iphone se,apple,429,4.1
galaxy z flip 5,samsung,999,4.6
redmi 10c,xiaomi,149,4.1
iphone 13 mini,apple,599,4.5"""
    file_path = tmp_path / "phones.csv"
    file_path.write_text(data)
    return str(file_path)


def test_csv_columns(sample_csv_data):
    with open(sample_csv_data, mode='r', encoding='utf-8') as file:
        reader = csv.DictReader(file)
        assert reader.fieldnames == ['name', 'brand', 'price', 'rating']


def test_load_csv(sample_csv_data):
    data = load_csv(sample_csv_data)
    assert len(data) == 10
    assert data[0]["name"] == "iphone 15 pro"
    assert data[1]["brand"] == "samsung"
    assert float(data[2]["price"]) == 199

def test_load_csv(sample_csv_data):
    data = load_csv(sample_csv_data)
    assert len(data) == 10
    assert data[0]["name"] == "iphone 15 pro"
    assert data[1]["brand"] == "samsung"
    assert data[9]["brand"] == "apple"
    assert float(data[2]["price"]) == 199

def test_filter_by_brand(sample_csv_data):
    data = load_csv(sample_csv_data)
    filtered = apply_filter(data, "brand=apple")
    assert len(filtered) == 4
    assert all(phone["brand"] == "apple" for phone in filtered)

def test_filter_by_price_gt(sample_csv_data):
    data = load_csv(sample_csv_data)
    filtered = apply_filter(data, "price>500")
    assert len(filtered) == 5
    assert float(filtered[0]["price"]) > 500


def test_filter_by_rating_lt(sample_csv_data):
    data = load_csv(sample_csv_data)
    filtered = apply_filter(data, "rating<4.5")
    assert len(filtered) == 4

def test_aggregate_avg_price(sample_csv_data):
    data = load_csv(sample_csv_data)
    avg_price = apply_aggregate(data, "price=avg")
    assert avg_price == pytest.approx(602)

def test_aggregate_max_rating(sample_csv_data):
    data = load_csv(sample_csv_data)
    max_rating = apply_aggregate(data, "rating=max")
    assert max_rating == 4.9

def test_aggregate_min_price_xiaomi(sample_csv_data):
    data = load_csv(sample_csv_data)
    xiaomi_phones = apply_filter(data, "brand=xiaomi")
    min_price = apply_aggregate(xiaomi_phones, "price=min")
    assert min_price == 149


def test_sort_by_price_asc(sample_csv_data):
    data = load_csv(sample_csv_data)
    sorted_data = apply_sort(data, "price=asc")
    assert float(sorted_data[0]["price"]) == 149
    assert sorted_data[0]["name"] == "redmi 10c"


def test_sort_by_rating_desc(sample_csv_data):
    data = load_csv(sample_csv_data)
    sorted_data = apply_sort(data, "rating=desc")
    assert float(sorted_data[0]["rating"]) == 4.9
    assert sorted_data[0]["name"] == "iphone 15 pro"