# -*- coding: utf-8 -*-

"""Tests for `grmaster.http`."""

#   group-master - tool for dividing students into groups
#   Copyright (C) 2015  Lutov V. S. <vslutov@yandex.ru>
#
#   This program is free software: you can redistribute it and/or modify
#   it under the terms of the GNU Affero General Public License as published by
#   the Free Software Foundation, either version 3 of the License, or
#   (at your option) any later version.
#
#   This program is distributed in the hope that it will be useful,
#   but WITHOUT ANY WARRANTY; without even the implied warranty of
#   MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#   GNU Affero General Public License for more details.
#
#   You should have received a copy of the GNU Affero General Public License
#   along with this program.  If not, see <http://www.gnu.org/licenses/>.

from grmaster import server, data
import pytest

@pytest.fixture
def app():
    """Fixture for easy testing."""
    return server.APP.test_client()

def test_index(app):
    """Index must return static index html."""
    assert data.readbytes('index.html') == app.get('/').data

def test_template(app):
    """Template must return static template csv."""
    assert data.readbytes('template.csv') == app.get('/template.csv').data

def test_result(app):
    """Result must return anything."""
    assert app.post('/result.csv').status_code == 400
    with data.openfile('students.csv', 'rb') as studentfile:
        response = app.post('/result.csv',
                            data=dict(studentfile=(studentfile, 'students.csv')))
        assert response.status_code == 200
        assert response.mimetype == 'text/csv'
