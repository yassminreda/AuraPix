import sys
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
from logic import selected_count
from i18n import EN,AR

def test_count_cannot_exceed_uploaded_images():
    assert selected_count(20,2)==2

def test_requested_count_is_respected():
    assert selected_count(5,12)==5

def test_languages_have_matching_keys():
    assert set(EN)==set(AR)

