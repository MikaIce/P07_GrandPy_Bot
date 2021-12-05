""" This module will test the views file """
from flask_testing import TestCase
from tests.service import manage_send_answer


class TestViews(TestCase):


    render_templates = False

    def create_app(self):

        from app.views import app
        app.config['TESTING'] = True
        return app

    def test_return_index_template(self):  # REQUIRE BLINKER LIBRARY TO WORK

        response = self.client.get("/")
        assert response.status_code == 200
        self.assert_template_used('index.html')

    def test_assert_not_process_the_template(self):
        response = self.client.get("/")
        assert b"" == response.data


def test_send_answer():

    result = manage_send_answer(
        "Ou ce trouve Cayenne")
    for element in result['answer']:
        assert "Cayenne" in element

    assert result['lat'] == '4.93461'
    assert result['lng'] == '-52.33033'
