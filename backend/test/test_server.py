from fastapi.testclient import TestClient
from unittest.mock import patch
import pytest

import ai_journal

client = TestClient(ai_journal.server.app)

@pytest.mark.parametrize("therapy_topic", ["stress management"])
def test_get_writing_prompt(therapy_topic, mocker):
    mocked_return_value = "Mocked writing prompt"
    mocker.patch('ai_journal.therapy.generate_writing_prompt', return_value=mocked_return_value)
        
    response = client.get(f"/writing_prompt?therapy_topic={therapy_topic}")
    
    assert response.status_code == 200
    assert response.json() == {"data": mocked_return_value}
    ai_journal.therapy.generate_writing_prompt.assert_called_once_with(therapy_topic)


@pytest.mark.parametrize("text_input", ["This is a test journal entry"])
def test_get_post_writing_analysis(text_input, mocker):
    mocked_return_value = "Mocked analysis"
    mocker.patch("ai_journal.therapy.generate_post_writing_analysis", return_value=mocked_return_value)

    response = client.post(
        "/post_writing_analysis",
        json={"text_input": text_input}
    )

    assert response.status_code == 200
    assert response.json() == {"message": mocked_return_value}
    ai_journal.therapy.generate_post_writing_analysis.assert_called_once_with(text_input)