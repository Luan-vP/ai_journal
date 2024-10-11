from fastapi.testclient import TestClient
from unittest.mock import patch
import pytest

import ai_journal

client = TestClient(ai_journal.server.app)

@pytest.mark.parametrize("therapy_topic", ["stress management"])
def test_get_writing_prompt(therapy_topic, mocker):
    mocker.patch('ai_journal.therapy.generate_writing_prompt', return_value="Mocked prompt")
        
    response = client.get(f"/writing_prompt?therapy_topic={therapy_topic}")
    
    assert response.status_code == 200
    assert response.json() == {"data": "Mocked prompt"}
    ai_journal.therapy.generate_writing_prompt.assert_called_once_with(therapy_topic)
