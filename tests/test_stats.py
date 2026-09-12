"""
Тесты для статистики.
"""

import pytest


class TestOverallStats:
    """Тесты общей статистики."""

    def test_get_overall_stats(self, client, auth_headers, test_habit):
        """Получение общей статистики."""
        response = client.get(
            "/api/v1/stats/overall",
            headers=auth_headers
        )
        assert response.status_code == 200
        data = response.json()
        assert data["total_habits"] == 1
        assert data["active_habits"] == 1
        assert data["completed_habits"] == 0
        assert data["total_days_completed"] == 0

    def test_get_overall_stats_empty(self, client, auth_headers):
        """Статистика без привычек."""
        response = client.get(
            "/api/v1/stats/overall",
            headers=auth_headers
        )
        assert response.status_code == 200
        data = response.json()
        assert data["total_habits"] == 0
